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
        self.splitCards = []
        self.aces = 0
        self.splitAces = 0

    def draw(self, deck, split=False):
        # tempCard = deck.draw()
        tempCard = Card("Hearts", 8)
        if split:
            self.splitCards.append(tempCard)
            if tempCard.value == 11:
                self.splitAces += 1
        else:
            self.cards.append(tempCard)
            if tempCard.value == 11:
                self.aces += 1

    def showCards(self, split=False):
        if not split:
            for c in self.cards:
                c.show()
        else:
            for c in self.splitCards:
                c.show()

    def showChips(self):
        print("You currently have %d chips" % self.chips)

    def bet(self, amt, pot):
        if amt > self.chips:
            print("You don't have enough money!")
            return False
        else:
            self.chips -= amt
            pot.add(amt)
            return True

    def wins(self, pot, share=1):
        amt = share*pot.chips
        print("+ %d chips" % amt)
        self.chips += amt

    def getCardsValue(self, split=False):
        val = 0
        remainingAces = 0
        if split:
            val = sum(c.value for c in self.splitCards)
            remainingAces = self.splitAces
        else:
            val = sum(c.value for c in self.cards)
            remainingAces = self.aces

        while val > 21 and remainingAces != 0:
            val = val - 10
            remainingAces -= 1
        if val > 21:
            return 0
        else:
            return(val)

    def split(self):
        self.splitCards.append(self.cards.pop())
        for c in self.splitCards:
            if c.value == 11:
                self.splitAces += 1
                self.aces -= 1


class Pot:
    def __init__(self):
        self.chips = 0

    def add(self, chips):
        self.chips += chips


def betting(player, dealer, pot):
    player.showChips()
    try:
        enoughMoney = False
        while not enoughMoney:
            bet = input("How much do you want to bet? ")
            bet = int(bet)
            enoughMoney = player.bet(bet, pot)
        dealer.bet(bet, pot)
        print("- %d chips" % bet)
    except:
        print("Please enter a valid number")


def splitStrategy(player, deck, secondHand=False):
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


def strategy(player, dealer, deck, pot):
    print("1) Hit")
    print("2) Stand")
    if len(player.cards) == 2 and not player.splitCards:
        if player.chips >= pot.chips/2:
            print("3) Double")
            if player.cards[0].number == player.cards[1].number:
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
        elif choice == 3:
            doubleBet = pot.chips/2
            player.bet(doubleBet, pot)
            dealer.bet(doubleBet, pot)
            print("- %d chips" % doubleBet)
            player.draw(deck)
            player.showCards()
            return True
        elif choice == 4:
            doubleBet = pot.chips/2
            player.split()
            player.bet(doubleBet, pot)
            dealer.bet(doubleBet, pot)
            print("- %d chips" % doubleBet)
            return False
        else:
            print("Please enter a number between 1 and 4")
            return False

    except:
        print("Please enter a number between 1 and 4")


def dealerStrategy(dealer, deck):
    val = dealer.getCardsValue()
    while val <= 16 and val > 0:
        dealer.draw(deck)
        val = dealer.getCardsValue()


def outcome(playerCardsValue, dealerCardsValue):
    if not dealerCardsValue or playerCardsValue > dealerCardsValue:
        if playerCardsValue == 21:
            print("You have BlackJack!")
        return True
    else:
        print("You lost!")
        return False


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
    playerCardsValue = player.getCardsValue()
    splitCardsValue = player.getCardsValue(split=True)
    if playerCardsValue or splitCardsValue:
        dealerStrategy(dealer, deck)
        print("Dealer's cards:")
        dealer.showCards()

        firstOutcome = outcome(playerCardsValue, dealer.getCardsValue())

        if splitCardsValue:
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
            print("You won")
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
