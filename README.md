# Group project

Blackjack with Python by Hugo Casademont, Thibaud Mottier and Francisco Broccard.

## About

This is a student project of the university of St. Gallen of the course Introduction to Programming.
The goal of the project was to create a blackjack game simulator.

We used object-oriented programming to realize the game: for the card, deck, player and pot instance.
The whole game can be started by calling: `python main()`

## Pre-requisites

The program works with Python3.
In order to run it, the random library needs to be installed.

## Rules

In this version of the game, the dealer faces only one player. The basic goal is to have a hand value close to 21 without going over that number. If the player's hand value is lower or equal to 21 and is greated than the dealer's cards value, the player wins the pot.

**Values of Cards:**

- The cards from 2 through 10 are valued at their face value
- The Jack, Queen, King are all valued at 10.
- The Ace can be counted as either 1 or 11. It is assumed that its value is 11 until the player goes over 21, in which case the value changes from 11 to 1.

**Kickoff:**

First, the player has to bet before receiving the cards. Then, the dealer distributes two face-up cards to the player and two cards (one face-up and one face-down) to himself.
Once the cards have been distributed, the player has the following options:

1. hit
2. stand
3. double (Only showed when the player has two cards and has enough money to double the bet)
4. split (Only showed when the player has two cards with the same face value and has enough money to double the bet)

Hit: The dealer distributes another card to the player. He can repeat this strategy as many times as he wants.
Stand: The player does not ask another card
Double: The player can double his bet but then he has to and can only hit once.
Split: If the player receives two cards with the same face value, he can split them into two separate games.

Once the player stands and his hand value is not bigger than 21, it is the dealer's turn.

The dealer has no freedom in his strategy. If his hand value is less or equal than 16, he hits. If the hand value is equal to 17, 18, 19, 20 or 21, he stands.

Finally, the two final hand values are compared. To win, the player strictly has to have a bigger value than the dealer.

We know the player's amount of chips. Then, he can choose how much he wants to bet, but it still needs to be equal or less than all of his chips.
When the players has bet, the dealer is obliged to put the same amount in the pot.
e.g. if the player bets 10, the dealer will also be required to put that much in the pot. Thus, the winner will win 20 (=the amount of the pot).

When the player and the dealer have drawn their 2 cards, the player can decide to hit, to stand, to double (if his chips amount is big enough to bet a second time the initial amount), to split if he has two cards with the same face value.
The dealer always hits until he has more than 16.

The winner of the game (the player only wins if he has a strictly bigger value than the dealer) takes the whole pot of this game.
The player can then decide to play again (only allowed if he has at least 1 chip left, if not he's not allowed to play again).
