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

    def remainingCards(self):
        print(len(self.cards))

    def shuffle(self):
        n = len(self.cards)
        newDeck = []
        for i in range(1, n+1):
            r = random.randint(0, n-i)
            newDeck.append(self.cards[r])
            del self.cards[r]
        print(len(newDeck))
        self.cards = newDeck

    def show(self):
        for c in self.cards:
            c.show()

    def distribute(self, draws):
        cards_dist = self.cards[0:draws]
        del self.cards[0:draws]
        return cards_dist


class Player:
    def __init__(self, cards, tokens):
        self.cards = cards
        self.tokens = tokens

    def getCards(self):
        print(self.cards)


deck = Deck()
deck.shuffle()
deck.show()
deck.distribute(2)
