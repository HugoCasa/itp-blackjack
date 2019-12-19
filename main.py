"""A one player game of blackjack.

This is a program for playing blackjack. It's for 1 player to play against the dealer.

    To launch the game use main()
"""

import random
import numpy as np


class Card:
    """Playing card class.

    A class for each card

    Attributes:
        suit: The suit of the card.
        number: The rank of the card.
        value: The value of the card in blackjack.
    """
    heads = ["Ace", "Jack", "Queen", "King"]

    def __init__(self, suit, nb):
        """Inits Card with the suit, the rank and the value."""
        self.suit = suit
        self.rank = nb
        if nb in [11, 12, 13]:
            # assigns the rank and value for jack, queen and king
            self.rank = Card.heads[nb-10]
            self.value = 10
        elif nb == 1:
            # assigns the rank and value for ace
            self.rank = Card.heads[nb-1]
            self.value = 11
        else:
            # assigns the value for all other cards
            self.value = nb

    def show(self):
        """Prints the rank and the suit of the card."""
        print("%s of %s" % (self.rank, self.suit))

    def __add__(self, o):
        """Prints the rank and the suit of the card."""
        return self.value + o.value


class Deck:
    """Deck class.

    A class for a deck full of cards.

    Attributes:
        cards: list which contains all the cards.
    """

    def __init__(self):
        """Inits Deck with empty cards array and call the build function to fill the deck."""
        self.cards = []
        self.build()

    def build(self):
        """Fill up the deck with all the cards."""
        for s in ['Hearts', 'Spades', 'Diamonds', 'Clubs']:
            for nb in range(1, 14):
                self.cards.append(Card(s, nb))

    def shuffle(self):
        """Shuffle the deck."""
        n = len(self.cards)
        newDeck = []
        for i in range(1, n+1):
            r = random.randint(0, n-i)
            newDeck.append(self.cards[r])
            del self.cards[r]
        self.cards = newDeck

    def show(self):
        """Show all the cards in the deck."""
        for c in self.cards:
            c.show()

    def draw(self):
        """Remove and returns the last card of the deck."""
        return self.cards.pop()


class Player:
    """Player class.

    A class for the player.

    Attributes:
        chips: chips of the player.
        cards: list with the cards of the player.
        splitCards: in case of a split, list with the second hand of the player.
        aces: number of aces of the player.
        splitAces: in case of a split, the number of aces in the second hand of the player.
    """

    def __init__(self, chips=0):
        """Inits the Player with the number of chips given."""
        self.chips = chips
        self.cards = []
        self.splitCards = []
        self.aces = 0
        self.splitAces = 0

    def draw(self, deck, split=False):
        """Draw a card from the deck and add it to the player's hand.

        Draw a card from the deck and add it to the player's hand and update the number of aces.

        Args:
            deck: a deck class.
            split: boolean to specify whether to add a card to the main hand or the second hand (in case of split).
        """
        tempCard = deck.draw()
        #tempCard = Card("Hearts", 8)
        if split:
            self.splitCards.append(tempCard)
            if tempCard.value == 11:
                self.splitAces += 1
        else:
            self.cards.append(tempCard)
            if tempCard.value == 11:
                self.aces += 1

    def showCards(self, split=False):
        """Draw a card from the deck and add it to the player's hand.

        Draw a card from the deck and add it to the player's hand and update the number of aces.

        Args:
            deck: a deck class.
            split: boolean to specify whether to add a card to the main hand or the second hand (in case of split).
        """
        if not split:
            for c in self.cards:
                c.show()
        else:
            for c in self.splitCards:
                c.show()

    def showChips(self):
        """Print the number of chips of the player."""
        print("You currently have %d chips" % self.chips)

    def bet(self, amt, pot):
        """Remove chips from the player's and add it to the pot.

        Args:
            amt: amount to bet.
            pot: a pot class.

        Returns:
            A boolean containing whether the player has enough chips to bet or not.
        """
        # check if enough chips
        if amt > self.chips:
            print("You don't have enough money!")
            return False
        else:
            self.chips -= amt
            pot.add(amt)
            return True

    def wins(self, pot, share=1):
        """Give a share amount of the pot to the player's chips.

        Give a share amount of the pot to the player's chips and print the transaction.

        Args:
            pot: a pot class.
            share: the share of the pot to give to the player.
        """
        amt = share*pot.chips
        print("+ %d chips" % amt)
        self.chips += amt

    def getCardsValue(self, split=False):
        """Calculate the player's cards value.

        Calculate the player's cards value. The number of aces is needed as it can either take the 1 or 11.

        Args:
            split: boolean to know which hand to get the value in the case of a split.

        Returns:
            A value between 0 and 21. If the calculated value is greater than 21, returns 0.
        """
        val = 0
        remainingAces = 0
        if split:
            val = sum(c.value for c in self.splitCards)
            remainingAces = self.splitAces
        else:
            val = sum(c.value for c in self.cards)
            remainingAces = self.aces

        # if the calculated value is larger than 21 but as long as there are aces the value can be reduced by 10 (ace value: 11 to 1)
        while val > 21 and remainingAces != 0:
            val = val - 10
            remainingAces -= 1
        if val > 21:
            return 0
        else:
            return(val)

    def split(self):
        """Split the player's cards.

        Removes one card from the main hand and add it to the second hand and adjust the number of aces of each hand accordingly.
        """
        self.splitCards.append(self.cards.pop())
        for c in self.splitCards:
            if c.value == 11:
                self.splitAces += 1
                self.aces -= 1


class Pot:
    """Pot class.

    A class for the pot.

    Attributes:
        chips: chips in the pot.
    """

    def __init__(self):
        """Inits the pot with 0 chips."""
        self.chips = 0

    def add(self, chips):
        """Add chips to the pot."""
        self.chips += chips


def betting(player, dealer, pot):
    """Betting process.

    Ask for amount to bet, check if the player has enough money, call the player's bet function and print the transaction.

    Args:
        player: a Player class.
        dealer: a Player class.
        pot: a Pot class.
    """
    player.showChips()
    enoughMoney = False
    while not enoughMoney:
        try:
            bet = input("How much do you want to bet? ")
            bet = int(bet)
            enoughMoney = player.bet(bet, pot)
            dealer.bet(bet, pot)
            print("- %d chips" % bet)
        except:
            print("Please enter a valid number")


def splitStrategy(player, deck, secondHand=False):
    """Split decision process.

    Offers two choices and act accordingly.

    Args:
        player: a Player class.
        deck: a Deck class.
        secondHand: boolean to know for which hand it is.

    Returns:
        True when the overall process is done (when the player stands).
    """
    if secondHand:
        print("Second Hand:")
    else:
        print("First Hand:")
    player.showCards(split=secondHand)
    print("1) Hit")
    print("2) Stand")
    try:
        choice = input("What would you like to do? ")
        choice = int(choice)
        if choice == 1:
            player.draw(deck, split=secondHand)
            player.showCards(split=secondHand)
            return not player.getCardsValue(split=secondHand)
        elif choice == 2:
            return True
        else:
            print("Please enter a number between 1 and 2")
            return False
    except:
        print("Please enter a number between 1 and 2")
        return False


def strategy(player, dealer, deck, pot):
    """Decision process.

    Offers four choices and act accordingly.

    Args:
        player: a Player class.
        dealer: a Player class.
        deck: a Deck class.
        pot: a Pot class.

    Returns:
        True when the overall process is done (when the player stands or the end of the double choice).
    """
    print("1) Hit")
    print("2) Stand")
    if len(player.cards) == 2 and player.chips >= pot.chips/2:
        print("3) Double")
        if player.cards[0].rank == player.cards[1].rank:
            print("4) Split")

    try:
        choice = input("What would you like to do? ")
        choice = int(choice)
        if choice == 1:
            player.draw(deck)
            player.showCards()
            return not player.getCardsValue()
        elif choice == 2:
            return True
        elif len(player.cards) == 2 and player.chips >= pot.chips/2:
            if choice == 3:
                # double the bet of the player and thus of the dealer as well + print transaction
                doubleBet = pot.chips/2
                player.bet(doubleBet, pot)
                dealer.bet(doubleBet, pot)
                print("- %d chips" % doubleBet)
                # draw one card and end the overall process
                player.draw(deck)
                player.showCards()
                return True
            elif choice == 4 and player.cards[0].rank == player.cards[1].rank:
                # double the bet of the player and thus of the dealer as well + print transaction
                doubleBet = pot.chips/2
                player.split()
                player.bet(doubleBet, pot)
                dealer.bet(doubleBet, pot)
                print("- %d chips" % doubleBet)
                return False
            else:
                print("Please enter a valid number")
                return False
        else:
            print("Please enter a valid number")
            return False

    except:
        print("Please enter a valid number")
        return False


def dealerStrategy(dealer, deck):
    """Dealer automatic process.

    Hits if cards value is equal or lower than 16 and higher than 0 (reminder: 0 is returned when the cards value is over 21).

    Args:
        dealer: a Player class.
        deck: a Deck class.
    """
    val = dealer.getCardsValue()
    while val <= 16 and val > 0:
        dealer.draw(deck)
        val = dealer.getCardsValue()


def outcome(playerCardsValue, dealerCardsValue):
    """Get outcome of a round.

    Hits if cards value is equal or lower than 16 and higher than 0 (reminder: 0 is returned when the cards value is over 21).

    Args:
        playerCardsValue: the cards value of a Player class.
        dealerCardsValue: the cards value of a Player class.

    Returns: 
        True if the player's cards have a higher value than the dealer's or if the dealer's cards value is 0 (reminder: when calculated cards value is higher than 21).
    """
    if not dealerCardsValue or playerCardsValue > dealerCardsValue:
        if playerCardsValue == 21:
            print("You have BlackJack!")
        return True
    else:
        return False


def game(player):
    """Game Process.

    One round game process.

    Args:
      player: a Player instance.

    """
    # initiates the dealer (every round -> unlimited money), the deck and the pot
    dealer = Player(1000)
    deck = Deck()
    deck.shuffle()
    pot = Pot()

    # Player bets
    betting(player, dealer, pot)

    # distribute cards
    player.draw(deck)
    dealer.draw(deck)
    player.draw(deck)

    # show player's cards and 1st dealer's card
    print("Your cards: ")
    player.showCards()

    print("Dealer's card: ")
    dealer.showCards()

    # distribute dealer's second card
    dealer.draw(deck)

    # loop trough decision taking
    # if split, then first decision process trough 1st hand then 2nd hand
    done = False
    secondHand = False
    while not done:
        if not player.splitCards:
            done = strategy(player, dealer, deck, pot)
        else:
            if not secondHand:
                secondHand = splitStrategy(player, deck, secondHand)
            else:
                done = splitStrategy(player, deck, secondHand)

    # check whether player wins or not
    # if the all the cards value is 0 (reminder: calculated value greated 21) then looses
    playerCardsValue = player.getCardsValue()
    splitCardsValue = player.getCardsValue(split=True)
    if playerCardsValue or splitCardsValue:
        # dealer plays
        dealerStrategy(dealer, deck)
        print("Dealer's cards:")
        dealer.showCards()

        # get outcome for first hand
        firstOutcome = outcome(playerCardsValue, dealer.getCardsValue())

        if splitCardsValue:
            # if split, then check first outocome get and check second outcome
            splitOutcome = outcome(splitCardsValue, dealer.getCardsValue())
            if playerCardsValue and firstOutcome:
                print("You won your first hand!")
                player.wins(pot, share=0.5)
            else:
                print("You lost your first hand!")
            if splitCardsValue and splitOutcome:
                print("You won your second hand!")
                player.wins(pot, share=0.5)
            else:
                print("You lost your second hand!")
        elif firstOutcome:
            # if won main outcome then wins
            print("You won")
            player.wins(pot)
        else:
            # if not then loses
            print("You lost!")
    else:
        print("You lost!")

    player.showChips()


def main():
    """Overall game process.

    Launches a new round of the game as long as the player wants to play.
    """
    # initiates player with 1000 chips
    player = Player(1000)
    wannaPlay = True
    # as long as the player wants to play and has some chips left launch a new round of the game
    while wannaPlay and player.chips > 0:
        player = Player(player.chips)
        game(player)
        if player.chips <= 0:
            print("You don't have any money left! Go home!")
            break
        choice = input("Would you like to play again? (y/n) ")
        if choice != "y":
            wannaPlay = False


# start the game
main()
