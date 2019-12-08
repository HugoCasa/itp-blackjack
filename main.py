import random


class Card:
    def __init__(self, suit, nb):
        self.suit = suit
        self.number = nb

    def show(self):
        print("%s of %s" % (self.number, self.suit))


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


deck = Deck()
deck.shuffle()
hugo = Player(1000)
communityCards = Player()
fold = Player()
pot = Pot()

hugo.draw(deck, 2)
hugo.showCards()
hugo.showTokens()

betting(hugo, pot)
getCommunityCards(communityCards, fold, 3)

betting(hugo, pot)
getCommunityCards(communityCards, fold, 1)

betting(hugo, pot)
getCommunityCards(communityCards, fold, 1)
