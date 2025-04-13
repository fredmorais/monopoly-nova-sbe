# Handles players information
class Player:
    def __init__(self, name, position = 0, balance = 1500, out_of_library_cards = 0, rounds_in_library_left = 0, bankrupt = False):
        self.name = name
        self.position = position
        self.balance = balance
        self.out_of_library_cards = out_of_library_cards
        self.rounds_in_library_left = rounds_in_library_left
        self.bankrupt = bankrupt

    def as_dict(self):
        return {
            'name': self.name,
            'position': self.position,
            'balance': self.balance,
            'out_of_library_cards': self.out_of_library_cards,
            'rounds_in_library_left': self.rounds_in_library_left,
            'bankrupt': self.rounds_in_library_left
        }


# Handles card info and its actions
class Card:
    def __init__(self, name, actions):
        self.name = name
        self.actions = actions


# Handles property's information and its actions
class Property:
    def __init__(self, name, value, color, owner = None):
        self.name = name
        self.value = value
        self.color = color

        # Index of the user that owns the property
        self.owner = owner


# Handles special properties info that can not be owned but instead have specific actions
class SpecialSpace():
    def __init__(self, name, actions = None):
        self.name = name
        self.actions = actions