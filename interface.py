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
        self.player_cards = [[["?" for _ in range(4)] for _ in range(3)] for _ in range(4)]  # Hidden cards
        self.create_game_board()

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
                    card_button = tk.Button(card_grid, text="?", width=5, height=2, font=("Helvetica", 10), command=lambda r=r, c=c, p=i: self.flip_card(r, c, p))
                    card_button.grid(row=r, column=c, padx=5, pady=5)
                    player_card_buttons.append(card_button)

            self.player_frames.append(player_frame)
            self.card_buttons.append(player_card_buttons)

        # Add a draw pile
        self.deck_frame = tk.Frame(self.root, pady=10)
        self.deck_frame.pack()

        self.draw_pile_button = tk.Button(self.deck_frame, text="Draw Card", font=("Helvetica", 12), command=self.draw_card)
        self.draw_pile_button.pack()

        # Add a status bar
        self.status_label = tk.Label(self.root, text="Game started! Player 1's turn.", font=("Helvetica", 12), pady=10)
        self.status_label.pack()

    def flip_card(self, row, col, player):
        """Handles card flip action."""
        if self.player_cards[player][row][col] == "?":
            if self.deck:
                card_value = self.deck.pop()
                self.player_cards[player][row][col] = card_value
                self.card_buttons[player][row * 4 + col].config(text=str(card_value))
                self.update_status(f"Player {player + 1} flipped a card: {card_value}.")
            else:
                self.update_status("The deck is empty!")
        else:
            messagebox.showinfo("Info", "This card has already been flipped!")

    def draw_card(self):
        """Handles drawing a card from the deck."""
        if self.deck:
            card = self.deck.pop()
            messagebox.showinfo("Draw Card", f"You drew a card: {card}")
            return card
        else:
            messagebox.showinfo("Deck Empty", "No more cards in the deck!")
            return None

    def update_status(self, message):
        """Updates the game status label."""
        self.status_label.config(text=message)

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = SkyjoGameUI(root)
    root.mainloop()
