# Imports
import pygame
import random

from classes import Card, Property


# List of cards. You can create more cards freely, but you need to add them to the board class!

# Property damaged card
def tsunami_actions(self):
    # Lose one of your properties at random

    # Get all the properties that the current user owns
    properties = [property for property in self.properties if type(property) == Property and property.owner == self.current_player]

    if len(properties) > 0:
        lost_property = random.choice(properties)

        self.prompt(f"A tsunami in Carcavelos has destroyed {lost_property.name} so it does not belong to you anymore.")
        pygame.time.wait(3000)


        self.properties[self.properties.index(lost_property)].owner = None
    else:
        self.prompt('A tsunami just hit Carcavelos, but luckily you did not have any property.')
        pygame.time.wait(3000)
tsunami = Card('Tsunami', tsunami_actions)


# Birthday card
def birthday_actions(self):
    # Receive 25$ from all players that have at least 25 in their balance

    self.prompt('You will receive 25$ from all the players.')

    # Wait 2.5 seconds before removing balances
    pygame.time.wait(2500)

    for i, player in enumerate(self.players):
        # The amount that the current player will receive
        birthday_amount = 0

        if i != self.current_player:
            # Make sure every player has enough money
            if player.balance >= 25:
                birthday_amount += 25
                player.balance -= 25

        self.players[self.current_player].balance += birthday_amount
birthday = Card('It\'s your birthday', birthday_actions)


# Pay a special tax card
def pay_tax_actions(self):
    # Pay a special tax of 75$

    self.prompt('You need to pay a special tax of 75$.')

    # Wait 2.5 seconds before removing tax from balance
    pygame.time.wait(2500)

    self.players[self.current_player].balance -= 75
pay_tax = Card('Pay a special tax', pay_tax_actions)


# Donate money to Santander
def donate_santander_actions(self):
    # Donate money to the Santander bank

    self.prompt('You need to donate money to Santander. 50$ will be removed from your balance.')

    # Wait 2.5 seconds before donating money to Santander
    pygame.time.wait(2500)

    self.santander_money += 50
    self.players[self.current_player].balance -= 50
donate_santander = Card('Santander money', donate_santander_actions)


# Library pass card
def library_card_actions(self):
    # Add one out of library card to the user

    self.prompt('You won a library card!')

    # Wait 2.5 seconds before adding library card
    pygame.time.wait(2500)

    self.players[self.current_player].out_of_library_cards += 1
library_card = Card('Library card', library_card_actions)


# Extra student fee
def extra_fees_actions(self):
    # User needs to pay an extra fee of 100

    self.prompt('You need to pay an extra fee of 100$.')

    # Wait 2.5 seconds before removing fee
    pygame.time.wait(2500)

    self.players[self.current_player].balance -= 100
extra_fees = Card('Extra fee', extra_fees_actions)


# Scholarship card
def scolarship_actions(self):
    # User received a scholarship and 50 $ will be added to his/hers balance

    self.prompt('You won a scholarship of 50$.')

    # Wait 2.5 seconds before adding to balance
    pygame.time.wait(2500)

    self.players[self.current_player].balance += 50
scolarship = Card('Scholarship', scolarship_actions)