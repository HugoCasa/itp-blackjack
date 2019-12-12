import random
import numpy as np
from itertools import combinations


class Card:
    def __init__(self, suit, nb):
        self.suit = suit
        self.number = nb

    def show(self):
        print("%s of %s" % (self.number, self.suit))

    def __add__(self, o):
        return self.number + o.number

    def __sub__(self, o):
        return self.number - o.number

    def __eq__(self, o):
        if(self.number == o.number):
            return True
        else:
            return False

    def __gt__(self, o):
        if(self.number > o.number):
            return True
        else:
            return False

    def __lt__(self, o):
        if(self.number < o.number):
            return True
        else:
            return False


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
    def __init__(self, tokens=0):
        self.tokens = tokens
        self.cards = []

    def draw(self, deck, draws=1):
        for _ in range(draws):
            self.cards.append(deck.draw())

    def showCards(self):
        for c in self.cards:
            c.show()

    def showTokens(self):
        print("You currently have %d tokens" % self.tokens)

    def bet(self, amt, pot):
        self.tokens -= amt
        pot.add(amt)


class Pot:
    def __init__(self):
        self.amount = 0

    def add(self, amt):
        self.amount += amt


def getCommunityCards(communityCards, fold, nb):
    fold.draw(deck, 1)
    communityCards.draw(deck, nb)
    communityCards.showCards()


def betting(player, pot):
    bet = input("How much do you want to bet? ")
    bet = int(bet)
    player.bet(bet, pot)
    player.showTokens()


def getScore(cards):
    for combi in combinations(cards, 5):
        # pair
        for two in combinations(combi, 2):
            if two[0] == two[1]:
                print("There is a pair")
        # threekind
        for three in combinations(combi, 3):
            if three[0] == three[1] and three[1] == three[2]:
                print("There is three of a kind")
        # carre
        for four in combinations(combi, 4):
            if four[0] == four[1] == four[2] == four[3]:
                print("There is four of a kind")
        # straight
        combi_sorted = sorted(combi)
        hp = np.array([c.number for c in combi_sorted[1:5]])
        lp = np.array([c.number for c in combi_sorted[0:4]])
        print(hp-lp)
        if np.array(hp-lp).all() == 1:
            print("There is a straight")
        # flush
        if combi[0].suit == combi[1].suit == combi[2].suit == combi[3].suit == combi[4].suit:
            print("There is a flush")


# deck = Deck()
# deck.shuffle()
# hugo = Player(1000)
# communityCards = Player()
# fold = Player()
# pot = Pot()

# hugo.draw(deck, 2)
# hugo.showCards()
# hugo.showTokens()

# betting(hugo, pot)
# getCommunityCards(communityCards, fold, 3)

# betting(hugo, pot)
# getCommunityCards(communityCards, fold, 1)

# betting(hugo, pot)
# getCommunityCards(communityCards, fold, 1)

testCards = [Card("Hearts", 1), Card("Hearts", 2), Card("Hearts", 3), Card(
    "Hearts", 10), Card("Hearts", 4), Card("Hearts", 7), Card("Hearts", 5)]
getScore(testCards)
