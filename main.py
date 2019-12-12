import random
import numpy as np


class Card:
    heads = ["Ace", "Jack", "Queen", "King"]

    def __init__(self, suit, nb):
        self.suit = suit
        self.number = nb
        if nb in [11, 12, 13]:
            self.number = Card.heads[nb-10]
            self.value = 10
        elif nb == 1:
            self.number = Card.heads[nb-1]
            self.value = 11
        else:
            self.value = nb

    def show(self):
        print("%s of %s" % (self.number, self.suit))

    def __add__(self, o):
        return self.value + o.value


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for s in ['Hearts', 'Spades', 'Diamonds', 'Clubs']:
            for nb in range(1, 14):
                self.cards.append(Card(s, nb))

    def shuffle(self):
        n = len(self.cards)
        newDeck = []
        for i in range(1, n+1):
            r = random.randint(0, n-i)
            newDeck.append(self.cards[r])
            del self.cards[r]
        self.cards = newDeck

    def show(self):
        for c in self.cards:
            c.show()

    def draw(self):
        return self.cards.pop()


class Player:
    def __init__(self, chips=0):
        self.chips = chips
        self.cards = []
        self.aces = 0

    def draw(self, deck):
        tempCard = deck.draw()
        self.cards.append(tempCard)
        if tempCard.value == 11:
            self.aces += 1

    def showCards(self):
        for c in self.cards:
            c.show()

    def showChips(self):
        print("You currently have %d chips" % self.chips)

    def bet(self, amt, pot):
        self.chips -= amt
        pot.add(amt)

    def wins(self, pot):
        print("You won!")
        self.chips += pot.chips

    def getCardsValue(self):
        val = sum(c.value for c in self.cards)
        remainingAces = self.aces
        while val > 21 and remainingAces != 0:
            val = val - 10
            remainingAces -= 1
        if val > 21:
            return 0
        else:
            return(val)


class Pot:
    def __init__(self):
        self.chips = 0

    def add(self, chips):
        self.chips += chips


def betting(player, dealer, pot):
    player.showChips()
    try:
        bet = input("How much do you want to bet? ")
        bet = int(bet)
        player.bet(bet, pot)
        dealer.bet(bet, pot)
    except:
        print("Please enter a valid number")


def strategy(player, dealer, deck, pot):
    print("1) Hit")
    print("2) Stand")
    print("3) Double")
    if len(player.cards) == 2 and player.cards[0].number == player.cards[1].number:
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
        elif choice == 3 and len(player.cards) == 2:
            player.bet(pot.chips/2, pot)
            dealer.bet(pot.chips/2, pot)
            player.draw(deck)
            player.showCards()
            return True
        else:
            print("Please enter a number between 1 and 4")
            return False

    except:
        print("Please enter a number between 1 and 4")


def dealerStrategy(player, deck):
    val = player.getCardsValue()
    while val <= 16:
        player.draw(deck)
        val = player.getCardsValue()


def game(player):
    dealer = Player(1000)
    deck = Deck()
    deck.shuffle()
    pot = Pot()

    # Players bet
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
    done = False
    while not done:
        done = strategy(player, dealer, deck, pot)

    # check whether player wins or not
    cardsValue = player.getCardsValue()
    if cardsValue:
        dealerStrategy(dealer, deck)
        print("Dealer's cards:")
        dealer.showCards()
        if (cardsValue > dealer.getCardsValue()) or not dealer.getCardsValue():
            if cardsValue == 21:
                print("BlackJack")
            player.wins(pot)
        else:
            print("You lost!")
    else:
        print("You lost!")

    player.showChips()


def main():
    player = Player(1000)
    wannaPlay = True
    while wannaPlay and player.chips > 0:
        player = Player(player.chips)
        game(player)
        choice = input("Would you like to play again? (y/n) ")
        if choice != "y":
            wannaPlay = False


main()
