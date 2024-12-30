import tkinter as tk
from tkinter import messagebox
import random

class SkyjoGameUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Skyjo Game")

        # Game setup
        self.deck = [i for i in range(-2, 13)] * 10  # Example deck of cards
        random.shuffle(self.deck)
        self.discard_pile = []
        self.player_cards = [[["?" for _ in range(4)] for _ in range(3)] for _ in range(4)]  # Hidden cards
        self.current_player = 0
        self.drawn_card = None  # Store the card drawn but not yet played
        self.revealing_phase_after_discard = False
        self.create_game_board()
        self.start_game()

    def create_game_board(self):
        """Creates the main game board."""
        self.board_frame = tk.Frame(self.root, padx=10, pady=10)
        self.board_frame.pack()

        # Add player areas
        self.player_frames = []
        self.card_buttons = []

        for i in range(4):  # Example for 4 players
            player_frame = tk.Frame(self.board_frame, relief=tk.RIDGE, borderwidth=2, padx=10, pady=10)
            player_frame.grid(row=i // 2, column=i % 2, padx=10, pady=10)

            player_label = tk.Label(player_frame, text=f"Player {i + 1}", font=("Helvetica", 14, "bold"))
            player_label.pack()

            # Create a grid for cards
            card_grid = tk.Frame(player_frame)
            card_grid.pack()

            player_card_buttons = []

            for r in range(3):
                for c in range(4):
                    card_button = tk.Button(card_grid, text="?", width=5, height=2, font=("Helvetica", 10), 
                                            command=lambda r=r, c=c, p=i: self.reveal_card(r, c, p))  # Reveal card on click
                    card_button.grid(row=r, column=c, padx=5, pady=5)
                    player_card_buttons.append(card_button)

            self.player_frames.append(player_frame)
            self.card_buttons.append(player_card_buttons)

        # Add a draw pile and discard pile
        self.deck_frame = tk.Frame(self.root, pady=10)
        self.deck_frame.pack()

        self.draw_pile_button = tk.Button(self.deck_frame, text="Draw Card from Pile", font=("Helvetica", 12), command=self.draw_card_from_pile, state=tk.DISABLED)
        self.draw_pile_button.pack(side=tk.LEFT, padx=10)

        self.discard_pile_button = tk.Button(self.deck_frame, text="Draw Card from Discard Pile", font=("Helvetica", 12), command=self.draw_card_from_discard_pile, state=tk.DISABLED)
        self.discard_pile_button.pack(side=tk.LEFT, padx=10)

        self.discard_pile_label = tk.Label(self.deck_frame, text="Discard Pile: Empty", font=("Helvetica", 12))
        self.discard_pile_label.pack(side=tk.LEFT, padx=10)

        # Add a status bar
        self.status_label = tk.Label(self.root, text="Game started! Player 1's turn.", font=("Helvetica", 12), pady=10)
        self.status_label.pack()

    def start_game(self):
        """Initializes the game by letting each player choose two cards to reveal."""
        self.status_label.config(text="Each player chooses 2 cards to reveal.")
        self.revealing_phase = True  # Flag for the revealing phase
        self.reveal_count = 0        # Counter for the number of reveals for the current player
        self.prompt_reveal()

    def prompt_reveal(self):
        """Prompt the current player to reveal two cards."""
        if self.reveal_count < 2:
            self.update_status(f"Player {self.current_player + 1}: Choose a card to reveal ({2 - self.reveal_count} left).")
        else:
            # Move to the next player
            self.current_player = (self.current_player + 1) % 4
            if self.current_player == 0:
                # All players have chosen their cards
                self.revealing_phase = False
                self.reveal_count = 0
                self.current_player = 0
                self.update_status("Game started! Player 1's turn.")
                return
            else:
                self.reveal_count = 0
                self.prompt_reveal()

    def reveal_card(self, row, col, player):
        """Gère l'action de retourner ou de remplacer une carte."""
        if self.revealing_phase:
            # Pendant la phase de révélation
            if player != self.current_player:
                messagebox.showinfo("Not Your Turn", "It's not your turn to reveal cards!")
                return
            if self.player_cards[player][row][col] != "?":
                messagebox.showinfo("Invalid Choice", "This card is already revealed!")
                return

            # Révéler la carte choisie
            self.player_cards[player][row][col] = self.deck.pop()
            self.card_buttons[player][row * 4 + col].config(text=str(self.player_cards[player][row][col]))
            self.reveal_count += 1

            # Vérifier si le joueur a révélé deux cartes
            if self.reveal_count < 2:
                self.update_status(f"Player {self.current_player + 1}: Choose another card to reveal.")
            else:
                self.prompt_reveal()
  
                if self.current_player == 0 and self.reveal_count == 0:
                    self.draw_pile_button.config(state=tk.NORMAL)
            
            

        elif self.revealing_phase_after_discard:
            # Pendant la phase de révélation après la carte tirée
            if player != self.current_player:
                messagebox.showinfo("Not Your Turn", "It's not your turn to reveal cards!")
                return
            if self.player_cards[player][row][col] != "?":
                messagebox.showinfo("Invalid Choice", "This card is already revealed!")
                return

            # Révéler la carte choisie
            self.player_cards[player][row][col] = self.deck.pop()
            self.card_buttons[player][row * 4 + col].config(text=str(self.player_cards[player][row][col]))
            self.reveal_count += 1
            
            self.revealing_phase_after_discard = False
            self.end_turn()  # Passer au prochain joueur

            


        else:
            
            # Logique de jeu normale
            if player != self.current_player:
                messagebox.showinfo("Not Your Turn", "It's not your turn!")
                return

            # Si une carte est tirée et en attente de remplacement
            if self.drawn_card is not None:
                current_card = self.player_cards[player][row][col]
                if current_card == "?":
                    # Révéler d'abord la carte
                    revealed_card = self.deck.pop() if self.deck else None
                    if revealed_card is not None:
                        current_card = revealed_card
                        self.player_cards[player][row][col] = revealed_card
                        self.card_buttons[player][row * 4 + col].config(text=str(revealed_card))
                        # Ajouter la carte révélée dans le deck
                        self.deck.append(revealed_card)
                        random.shuffle(self.deck)  # Mélanger le deck après avoir ajouté la carte révélée
                    else:
                        messagebox.showinfo("Deck Empty", "No more cards in the deck to reveal the hidden card!")
                        return

                # Remplacer la carte
                self.player_cards[player][row][col] = self.drawn_card
                self.card_buttons[player][row * 4 + col].config(text=str(self.drawn_card))

                # Ajouter la carte remplacée à la pile de défausse si ce n'est pas une carte cachée
                if current_card != "?":
                    self.discard_pile.append(current_card)
                    self.discard_pile_label.config(text=f"Discard Pile: {current_card}")

                # Réinitialiser la carte tirée et finir le tour
                self.drawn_card = None
                self.end_turn()
            else:
                # Logique de retournement
                if self.player_cards[player][row][col] == "?":
                    messagebox.showinfo("Flip Card", "You must choose an action to flip or replace a card!")
                else:
                    messagebox.showinfo("Info", "This card is already revealed!")

    def update_discard_pile_button_state(self):
        """Met à jour l'état du bouton de la pile de défausse."""
        if self.discard_pile:
            self.discard_pile_button.config(state=tk.NORMAL)
        else:
            self.discard_pile_button.config(state=tk.DISABLED)

    def draw_card_from_pile(self):
        """Tirer une carte de la pioche."""
        if not self.deck:
            messagebox.showinfo("Deck Empty", "No more cards in the deck!")
            return


        self.drawn_card = self.deck.pop()
        option = messagebox.askquestion("Card Drawn", f"You drew a {self.drawn_card}. Do you want to discard it?")
        
        if option == "yes":
            # Jeter la carte
            self.discard_pile.append(self.drawn_card)
            self.discard_pile_label.config(text=f"Discard Pile: {self.drawn_card}")
            self.drawn_card = None
            
            self.reveal_card_choice()  # Permet de révéler une carte aléatoire après avoir jeté la carte
        else:
            # Attendre que le joueur remplace une carte
            messagebox.showinfo("Card Drawn", f"You drew a {self.drawn_card}. Click on a card to replace it.")


        self.update_discard_pile_button_state()

    def reveal_card_choice(self):
        """Permet au joueur de choisir une carte cachée à révéler en cliquant dessus."""


        # Afficher un message pour inviter le joueur à cliquer sur une carte cachée
        self.update_status(f"Player {self.current_player + 1}: Choose a hidden card to reveal.")
        self.revealing_phase_after_discard = True  # Phase de révélation en cours
        self.reveal_count = 0  # Initialiser le compteur de cartes révélées

        # Maintenant, lorsqu'un joueur clique sur une carte, la méthode flip_card s'en occupera

    def draw_card_from_discard_pile(self):
        """Tirer une carte de la pile de défausse et permettre au joueur de l'échanger."""
        if not self.discard_pile:
            messagebox.showinfo("Discard Pile Empty", "The discard pile is empty!")
            return

        card_from_discard = self.discard_pile[-1]  # La dernière carte de la pile de défausse
        option = messagebox.askquestion("Card Drawn", f"You drew a {card_from_discard} from the discard pile. Do you want to replace a card with it?")
        
        if option == "yes":
            # Permettre au joueur de choisir une carte à remplacer
            self.update_status(f"Player {self.current_player + 1}: Choose a card to replace with {card_from_discard}.")
            self.drawn_card = card_from_discard  # La carte tirée est celle de la défausse
        else:
            # La carte tirée de la pile est simplement ignorée
            messagebox.showinfo("Card Discarded", f"You discarded the {card_from_discard}.")
            
        # Le bouton de la défausse reste activé tant qu'il y a des cartes dans la pile
        self.update_discard_pile_button_state()  # Met à jour l'état du bouton de défausse

    


    def end_turn(self):
        """Ends the current player's turn and moves to the next player."""
        self.current_player = (self.current_player + 1) % 4
        self.update_status(f"Player {self.current_player + 1}'s turn.")

    def update_status(self, message):
        """Updates the game status label."""
        self.status_label.config(text=message)

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = SkyjoGameUI(root)
    root.mainloop()
