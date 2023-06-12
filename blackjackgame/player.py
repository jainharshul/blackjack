"""A Class for Dealer and Users"""


class Player:
    """Player class to make dealer and player charectors in game"""

    def __init__(self, name, bank_balance=10000.00):
        """Constructor funtion to set name of player and initial balance as 10K"""
        self.name = name
        self.bank_balance = bank_balance
        self.hand = []

    def place_bet(self):
        """Function to place players bet"""
        while True:
            try:
                bet = float(
                    input(
                        f"{self.name}, enter your bet amount"
                        f" (minimum $1, maximum ${self.bank_balance}): "
                    )
                )
                if 1 <= bet <= self.bank_balance:
                    return bet
                print("Invalid bet amount. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid bet amount.")

    def update_bank_balance(self, amount):
        """Function to add an amount to the player's bank balance"""
        self.bank_balance += amount

    def add_card_to_hand(self, card):
        """Function to add a card to the player's hand (list)"""
        self.hand.append(card)

    def clear_hand(self):
        """Funtion to clear the player's hand"""
        self.hand = []
