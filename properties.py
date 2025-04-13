# Imports
import pygame

from classes import Property, SpecialSpace


# List of properties. You can create more properties as you wish. Be careful when adding these to the
# self.properties array in the Board class. The number of properties can not be random. The number of
# properties in a board should be n such as (n - 4) / 4 is an integer number, i.e. remainder = 0.

# Function to draw a random card for KPMG, Haddad and Westmont
def random_card(self):
    self.prompt('Drawing a random a card...')

    pygame.time.wait(2000)

    self.random_card()


# Hovione Hall
hovione = SpecialSpace(
    'Hovione'
)


# The Cut Restaurant
the_cut = Property(
    'The Cut',
    60,
    (149, 83, 61)
)


# KPMG Gallery
kpmg = SpecialSpace(
    'KPMG Gallery',
    random_card
)


# Carcavelos Beach
beach = Property(
    'Carcavelos Beach',
    100,
    (149, 83, 61)
)


# Library
def library_actions(self):
    self.prompt('Careful with the library! You might be just visiting, but you can get stuck studying for 3 rounds.')
    pygame.time.wait(2000)
library = SpecialSpace(
    'Library',
    library_actions
)


# Pingo Doce
pingo_doce = Property(
    'Pingo Doce',
    140,
    (211, 64, 145)
)


# Student Union
def student_union_actions(self):
    self.prompt('You need to pay your SU fees. 50$ will be removed and added to Santander.')
    pygame.time.wait(2000)

    self.players[self.current_player].balance -= 50
    self.santander_money += 50
student_union = SpecialSpace(
    'Student Union',
    student_union_actions
)


# Fitness Hut
fitness_hut = Property(
    'Fitness Hut',
    350,
    (211, 64, 145)
)


# SABA Parking
def parking_actions(self):
    self.prompt('Parking can be expensive. Take the money from Santander to help you!')
    pygame.time.wait(2500)

    self.players[self.current_player].balance += self.santander_money
    self.santander_money = 0
parking = SpecialSpace(
    'Parking Saba',
    parking_actions
)


# Padaria do Bairro
padaria = Property(
    'Padaria do Bairro',
    220,
    (228, 37, 42)
)


# Haddad institute
haddad = SpecialSpace(
    'Haddad',
    random_card
)


# Windsurf Café
windsurf = Property(
    'Windsurf Café',
    280,
    (228, 37, 42)
)


# Sagres Beachway
def sagres_beachway_actions(self):
    # If player has library card he's free
    if self.players[self.current_player].out_of_library_cards > 0:
        self.prompt('You\'re lucky this time because you have a library card, but next time you might be stuck in a study session.')
        pygame.time.wait(3000)

        self.players[self.current_player].out_of_library_cards -= 1
    # If not he is sent to the library and gets 3 rounds stuck there
    else:
        self.prompt('Thought you might go to the beach to get some sun? Think again! You will be sent to the library to study for 3 rounds without going through Hovione.')
        pygame.time.wait(3000)

        self.players[self.current_player].position = 4
        self.players[self.current_player].rounds_in_library_left = 3
sagres_beachway = SpecialSpace(
    'Sagres Beach Way',
    sagres_beachway_actions
)


# Azure
azure = Property(
    'Azure',
    300,
    (3, 114, 185)
)


# Westmont Institute
westmont = SpecialSpace(
    'Westmont',
    random_card
)


# Milestone Residence
milestone = Property(
    'Milestone',
    400,
    (3, 114, 185)
)