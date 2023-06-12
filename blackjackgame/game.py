"""BlackJack Game with each player starting with 10k in bank balance"""

from blackjackgame.cards import Deck
from blackjackgame.player import Player


class BJGame:
    """Black Jack main class"""

    def __init__(self, num_players):
        """Constructor function to make dealer with infinite money and set deck and # of players"""
        dealer = Player("dealer", bank_balance=float("inf"))
        self.players = [dealer]
        self.deck = None
        self.num_players = num_players

    def initialize_players(self):
        """Function to initialize players with their given names"""
        for i in range(self.num_players):
            name = input(f"Enter the name for Player {i + 1}: ")
            player = Player(name)
            self.players.append(player)

    def play(self):
        """Function to play game contains game loop"""
        while True:
            self.deck = Deck(num_decks=8)
            self.deck.shuffle()
            self.deck.cut()

            for player in self.players:
                player.clear_hand()

            for _ in range(2):
                for player in self.players:
                    card = self.deck.deal()[0]
                    player.add_card_to_hand(card)

            for player in self.players[1:]:
                player_bet = player.place_bet()
                player.update_bank_balance(-player_bet)

            for player in self.players[1:]:
                print(f"\n{player.name}'s turn:")
                self.play_player_turn(player, player_bet)

            self.play_dealer_turn()
            self.evaluate_game(player_bet)

            play_again = input("play again? (y/n): ")
            if play_again.lower() != "y":
                break

    def play_player_turn(self, player, player_bet):
        """Function to play the players turn handling double down and more"""
        print(f"The Dealers Hand is: {self.players[0].hand[0]} and a turned over card")
        print(
            f"{player.name}'s Hand is: {', '.join(str(card) for card in player.hand)} "
            f"for a total of {self.calculate_hand_total(player.hand)}"
        )
        if (
            self.calculate_hand_total(player.hand) == 21
            and self.calculate_hand_total(self.players[0].hand) != 21
        ):
            print("You have 21! You WON!")
            player.update_bank_balance(2 * player_bet)
            return
        while True:
            if len(player.hand) == 2:
                double_down = input("Do you want to double down? (y/n): ")
                if double_down.lower() == "y":
                    player.update_bank_balance(-player_bet)
                    player_bet *= 2
                    card = self.deck.deal()[0]
                    player.add_card_to_hand(card)
                    print(
                        f"Player {player.name} doubled down. New hand: "
                        f"{' and '.join(str(card) for card in player.hand)} "
                        f"with total of {self.calculate_hand_total(player.hand)}"
                    )
                    if self.calculate_hand_total(player.hand) > 21:
                        print(f"{player.name} busted!")
                        break
                    if self.calculate_hand_total(player.hand) == 21:
                        print(f"{player.name} reached 21! You can not hit any longer\n")
                        break
                    self.play_dealer_turn()
                    self.evaluate_game(player_bet)
                    return
            action = input("Do you want to hit(1) or stand(2): ")
            if action == "1":
                card = self.deck.deal()[0]
                player.add_card_to_hand(card)
                print(
                    f"\nPlayer {player.name} Hits. New hand: "
                    f"{' and '.join(str(card) for card in player.hand)} "
                    f"for a total of {self.calculate_hand_total(player.hand)}"
                )
                if self.calculate_hand_total(player.hand) > 21:
                    print(f"{player.name} busted!")
                    break
                if self.calculate_hand_total(player.hand) == 21:
                    print(f"{player.name} reached 21! You can not hit any longer\n")
                    break
            elif action == "2":
                print(f"{player.name} stands.")
                break
            else:
                print("Invalid input. Please enter '1' to hit or '2' to stand.\n")

    def calculate_hand_total(self, hand):
        """Funtion to calculate the total of any given player's hand"""
        value = sum(card.value() for card in hand)
        aces = sum(card.is_ace() for card in hand)
        while value > 21 and aces:
            value -= 10
            aces -= 1
        if aces > 0 and value + 10 <= 21:
            value += 10

        return value

    def play_dealer_turn(self):
        """Function to play the dealers turn with logic for dealer to hit"""
        dealer = self.players[0]
        print("\nDealer's Turn:")
        print(f"Dealer's hand: {', '.join(str(card) for card in dealer.hand)}")
        print(f"Dealer's current total: {self.calculate_hand_total(dealer.hand)}")
        while self.calculate_hand_total(dealer.hand) < 17:
            card = self.deck.deal()[0]
            dealer.add_card_to_hand(card)
            print(
                f"Dealer hits. New hand: {', '.join(str(card) for card in dealer.hand)} "
                f"with a total of {self.calculate_hand_total(dealer.hand)}"
            )

    def evaluate_game(self, player_bet):
        """Function to evaluate game with player and
        dealer hand along with handling 2to1 bet money"""
        dealer = self.players[0]
        dealer_total = self.calculate_hand_total(dealer.hand)

        for player in self.players[1:]:
            player_total = self.calculate_hand_total(player.hand)

            if player_total > 21:
                print(f"{player.name} busted! {player.name} loses.\n")
            elif player_total == dealer_total:
                print("Dealer pushed. It's a tie.\n")
                player.update_bank_balance(player_bet)
            elif player_total > dealer_total or dealer_total > 21:
                print(f"{player.name} wins!\n")
                player.update_bank_balance(player_bet * 2)
