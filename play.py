# Imports
import json
import os
# Do not print pygame inital message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import math
import sys
from pygame.locals import *

from classes import Player
from cards import *
from properties import *


# Settings
# Note: screen size can be changed but unexpected behaviors can occur. Change at your risk! Defauly size is 1280x720
screen_width = 1280
screen_height = 720
border = 30

# Boring setup settings
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Nova SBE Monopoly")
clock = pygame.time.Clock()

# _ms
font_l = pygame.font.SysFont('arial', 32)
font_m = pygame.font.SysFont('arial', 26)
font_s = pygame.font.SysFont('arial', 14)
font_s.set_bold(True)
font_xs = pygame.font.SysFont('arial', 12)

# Player's colors
colors = [
    (0, 191, 255),
    (255, 131, 0),
    (118, 185, 71),
    (168, 36, 111)
]


# Board class
# Needs to be in this file since it wasn't working in the classes.py file because reasons
class Board:
    def __init__(self):
        # All the cards that can be drawn
        self.cards = [
            tsunami,
            birthday,
            pay_tax,
            # Santander card shows up 3 times to increase odds of drawing it
            donate_santander,
            donate_santander,
            donate_santander,
            library_card,
            extra_fees,
            scolarship
        ]

        # All the properties that exist in the board. Be careful when adding/removing properties.
        # Refer to the comment on line 7 in properties.py for more information.
        self.properties = [
            hovione,
            the_cut,
            kpmg,
            beach,
            library,
            pingo_doce,                 
            student_union,
            fitness_hut,
            parking,
            padaria,
            haddad,
            windsurf,
            sagres_beachway,
            azure,
            westmont,
            milestone
        ]

        # Variable to save prompt text
        self.prompt_text = ""

        # Variable to check if the game is running
        self.running = True

    # Functions for loading and saving game
    def save_game(self):
        # Create dict with all the game information
        game = {
            'players': [player.as_dict() for player in self.players],
            'properties': [property.owner for property in self.properties if type(property) == Property],
            'current_player': self.current_player,
            'santander_money': self.santander_money
        }

        i = 0
        while True:
            if os.path.exists(f"saved_games/game{i}.json"):
                i += 1
            else:
                # Save file to saved_games
                with open(f"saved_games/game{i}.json", "w") as file:
                    json.dump(game, file, indent = 2)
                break

    def load_game(self, players, properties, current_player = 0, santander_money = 0):
        # Load all information to board
        self.players = players
        self.current_player = current_player
        self.santander_money = santander_money

        # Note: This assumes that the properties are loaded in the same order they are saved
        i = 0
        for property in self.properties:
            if type(property) == Property:
                property.owner = properties[i]
                i += 1
    
    # Functions responsible for game's mechanics
    def move_player(self, player, distance):
        # Move player to a new property

        # Calculate new position
        new_position = player.position + distance

        # If new position exceeds board length
        if new_position >= len(self.properties):
            # Correct new position so it is back inside board's length
            new_position -= len(self.properties)

            # Prompt to the user that he/she received money by going through Hovione
            self.prompt("You just went through Hovione. 200$ will be added to your balance.")
            self.draw_screen()
            pygame.time.wait(2500)

            # Add money to balance
            player.balance += 200

        # Assign new position to player
        player.position = new_position

        # Return new position
        return new_position

    def roll_dice(self):
        dice = random.randint(1,6)

        # Prompt rolled number
        self.prompt(f"Dice rolled a number {dice}")

        # Wait 1.7 seconds
        pygame.time.wait(1700)

        # Return a random value between 1 and 6
        return dice

    def get_monopolies(self):
        # Returns a list will all the monopolies. Each monopoly is represented by its color
        monopolies = []

        for property in self.properties:
            if type(property) == Property and property.color not in monopolies:
                monopolies.append(property.color)

        return monopolies

    def get_monopoly(self, color):
        # Returns all the properties that have a given color, i.e. all the properties within a monopoly
        monopoly_properties = []

        for property in self.properties:
            if type(property) == Property and property.color == color:
                monopoly_properties.append(property)
            
        return monopoly_properties

    def get_monopoly_owner(self, color):
        # Returns the index of the player that owns the monopoly. If the monopoly has no
        # owner None is returned instead
        properties = self.get_monopoly(color)

        owner = properties[0].owner if all(property.owner == properties[0].owner for property in properties) else None

        return owner

    def next_player(self):
        # If current player is the last one, go back to the first player
        if self.current_player == len(self.players) - 1:
            self.current_player = 0
        # Else just skip to next player
        else:
            self.current_player += 1

        # Skip bankrupt players
        if self.players[self.current_player].bankrupt:
            self.next_player()

    def random_card(self):
        # Select random card
        card = random.choice(self.cards)

        # Prompt user for what the drawn card was
        self.prompt(f"Drawn card was \"{card.name}\".")

        # Wait 2 seconds befor executing card's actions
        pygame.time.wait(2000)

        # Execute card's actions
        card.actions(self)

    def next_round(self):
        # While game is still running
        while self.running:
            # Finish game when user clicks X to close window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # Track player pressing "s" to save game
                elif event.type == KEYDOWN:
                    if event.key == K_s:
                        self.save_game()

            # Draw screen on the beginning of the round
            self.draw_screen()
            
            # Get current player
            current_player = self.players[self.current_player]

            # Check if player is stuck in the library
            rounds_in_library_left = current_player.rounds_in_library_left
            if rounds_in_library_left > 0:
                # Prompt user for the amount of rounds he's still stuck
                self.prompt(f"{current_player.name} is still stuck in the library for {rounds_in_library_left} rounds.")

                # Redraw screen
                self.draw_screen()
                pygame.time.wait(2500)

                # Decrease amount of rounds stuck
                current_player.rounds_in_library_left -= 1

                # Move to next player
                self.next_player()

                # Skip to next round
                continue

            # Prompt user to roll the dice
            board.prompt(f"It's {current_player.name}'s turn. Press \"r\" to roll the dice")
            self.draw_screen()

            # Wait for user to press "r"
            while True:
                event = pygame.event.wait()
                if event.type == KEYDOWN:
                    if event.key == K_r:
                        break
                    elif event.key == K_s:
                        self.save_game()
                elif event.type == pygame.QUIT:
                    self.running = False
                    break
            # Check if game was stopped
            if self.running == False:
                continue

            # Clear text prompt and redraw screen
            board.prompt("")
            self.draw_screen()

            # Roll dice and move player to position
            distance = self.roll_dice()
            new_position = self.move_player(current_player, distance)
            new_property = self.properties[new_position]

            # Redraw screen so user shows up in the new position
            self.draw_screen()

            # Check type of property
            if type(new_property) == Property:
                # Prompt to buy property if no one owns it
                if new_property.owner == None:

                    # Prompt buy instructions
                    board.prompt(f'{new_property.name} is up for sale. Do you want to buy?(y/n)')
                    self.draw_screen()

                    # Wait for user to press "y" or "n"
                    while True:
                        event = pygame.event.wait()
                        if event.type == KEYDOWN:
                            # If user presses "y"
                            if event.key == K_y:
                                # Update balance of current player and owner of property
                                current_player.balance -= new_property.value
                                new_property.owner = self.current_player

                                # Prompt info that the user bought the property
                                board.prompt(f"{current_player.name} bought {new_property.name}")
                                self.draw_screen()
                                pygame.time.wait(2500)
                                break
                            # If user presses "n"
                            elif event.key == K_n:
                                # Prompt info that the user did not buy the property
                                board.prompt(f"{current_player.name} did not buy {new_property.name}")
                                self.draw_screen()
                                pygame.time.wait(2500)
                                break
                        elif event.type == pygame.QUIT:
                            self.running = False
                            break
                    # Check if game was stopped
                    if self.running == False:
                        continue

                # If it has an owner pay the rent to him
                else:
                    # Get the owner of new property
                    owner = self.players[new_property.owner]

                    # Check that owner and current player are different
                    if current_player.name != owner.name:
                        # Calculate rent
                        rent = math.ceil(new_property.value * 0.3)

                        # Prompt user that rent will be paid
                        self.prompt(f"{self.players[self.current_player].name} just landed on {owner.name}'s property and will pay him {rent}$.")
                        self.draw_screen()
                        pygame.time.wait(2000)

                        # Remove fee from current player's balance and pay owner
                        current_player.balance -= rent
                        owner.balance += rent
            else:
                # Run actions if it they exist for this special property
                if new_property.actions != None:
                    new_property.actions(self)

                # Redraw screen and wait
                self.draw_screen()
                pygame.time.wait(3500)

            # Detect negative balances
            for player in self.players:
                if player.balance < 0 and player.bankrupt == False:
                    # Keep selling properties until user has positive balance
                    while player.balance < 0:
                        # Get user properties
                        properties = [property for property in self.properties if type(property) == Property and property.owner == self.current_player]

                        # If player does not have properties, he is bankrupt
                        if len(properties) == 0:
                            # Change player to bankrupt
                            player.bankrupt = True

                            # Prompt that player is bankrupt and wait 2 seconds
                            self.prompt(f"{player.name} is now bankrupt!")
                            pygame.time.wait(2000)
                            break

                        # Get cheapest property, the one that will be sold
                        sold_property = min(properties, key=lambda x: x.value)

                        # Prompt that property will be sold
                        self.prompt(f"{player.name} has a negative balance. Your property {sold_property} will be sold.")

                        # Wait 3 seconds before selling
                        pygame.time.wait(3000)

            # Detect if only one player left
            players_left = sum(1 for player in self.players if player.bankrupt == False)

            if players_left == 1:
                for player in self.players:
                    if player.bankrupt == False:
                        winning_player = player

                        # Prompt that player one
                        self.prompt(f"{winning_player.name} won the game because there is no other player left!")

                        # Wait for player to close window
                        while True:
                            event = pygame.event.wait()
                            if event.type == pygame.QUIT:
                                self.running = False
                                break

            # Detect if someone owns 2 monopolies
            monopolies_owned = {}

            for monopoly in self.get_monopolies():
                monopoly_owner = self.get_monopoly_owner(monopoly)

                if monopoly_owner != None:
                    if monopoly_owner in monopolies_owned:
                        monopolies_owned[monopoly_owner] += 1
                    else:
                        monopolies_owned[monopoly_owner] = 1

            for player, monopolies_owned_by_player in monopolies_owned.items():
                if monopolies_owned_by_player >= 2:
                    winning_player = self.players[player]

                    # Prompt that player one
                    self.prompt(f"{winning_player.name} won the game because he/she has 2 monopolies!")

                    # Wait for player to close window
                    while True:
                        event = pygame.event.wait()
                        if event.type == pygame.QUIT:
                            self.running = False
                            break

            # Move to next player
            self.next_player()

        # Quit game is self.running is false
        pygame.quit()

    # Functions responsible to help in the visual display
    def center_shape(self, shape_size, parent_size):
        # Function to auxiliate in the centering of a shape in regards to its parent
        x = (parent_size[0] - shape_size[0]) // 2
        y = (parent_size[1] - shape_size[1]) // 2

        return (x, y)

    def draw_screen(self):
        # Finish game when user clicks X to close window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                board.running = False

        # Fill the screen black to wipe away anything from last frame
        screen.fill("black")

        # Display players
        point_y = border
        for i, player in enumerate(board.players):
            # Draw player name
            player_name = font_l.render(player.name, 1, (255, 255, 255))
            player_name_width, player_name_height = font_l.size(player.name)
            screen.blit(player_name, (border, point_y))

            # Draw player color
            color_x = border + 10 + player_name_width
            color_y = point_y
            pygame.draw.rect(screen, colors[i], [color_x, color_y, player_name_height, player_name_height], 0, border_radius=4)

            # Draw player's number of library cards
            library_cards = font_m.render(f"{player.out_of_library_cards}", 1, (255, 255, 255))
            library_cards_width, library_cards_height = font_m.size(f"{player.out_of_library_cards}")
            library_cards_x, library_cards_y = self.center_shape((library_cards_width, library_cards_height), (player_name_height, player_name_height))
            screen.blit(library_cards, (color_x + library_cards_x, color_y + library_cards_y))

            # Increase point_y
            point_y += border + 10

            # Check if player is bankrupt
            if player.bankrupt:
                player_subtext = font_m.render("Bankrupt", 1, (255, 255, 255))
            else:
                player_subtext = font_m.render(f"{player.balance} $", 1, (255, 255, 255))
            screen.blit(player_subtext, (border, point_y))

            point_y += border + 35

        # Calculate side of the board
        board_size = screen_height - 2 * border

        # Number of properties on each side
        n = int((len(self.properties) - 4) / 4 + 2)

        property_size = board_size / n
        
        # Upper left corner for board space
        starting_x = screen_width - screen_height + border
        starting_y = screen_height - property_size - border

        pygame.draw.rect(screen, (204, 228, 207),
                [screen_width - border - board_size, border, board_size, board_size], 0)

        # Draw left side of the board
        t = 0
        for i in range(n - 1):
            self.draw_property(t, starting_x, starting_y, property_size)
            starting_y -= property_size
            t += 1
            
        # Draw top column
        for i in range(n - 1):
            self.draw_property(t, starting_x, starting_y, property_size)
            starting_x += property_size
            t += 1
            
        # Draw right side
        for i in range(n - 1):
            self.draw_property(t, starting_x, starting_y, property_size)
            starting_y += property_size
            t += 1
            
        # Draw bottom column
        for i in range(n - 1):
            self.draw_property(t, starting_x, starting_y, property_size)
            starting_x -= property_size
            t += 1

        # Draw logo
        logo = pygame.image.load("assets/logo.png")

        image_x = logo.get_rect().width
        image_y = logo.get_rect().height

        new_width = math.floor(board_size * 0.3)
        new_height = image_y * (new_width / image_x)
        new_size = (new_width, new_height)

        scaled_image = pygame.transform.scale(logo, new_size)

        x, y = self.center_shape(new_size, (board_size, board_size))
        screen.blit(scaled_image, (screen_width - border - board_size + x, screen_height - border - board_size +  y))

        # Draw santander money
        santander_money = font_s.render(f"Santander Money: {self.santander_money}$", 1, (0, 0, 0))

        text_width, text_height = font_s.size(f"Santander Money: {self.santander_money}$")
        x, y = self.center_shape((text_width, text_height), (board_size, board_size))

        screen.blit(santander_money, (screen_width - border - board_size + x, screen_height - border - board_size +  y + new_height // 2 + 10))


        # Draw prompt
        available_width = screen_width - 3 * border - board_size

        collection = [word.split(' ') for word in self.prompt_text.splitlines()]
        space = font_m.size(' ')[0]
        x = border
        y = math.floor(0.7 * screen_height)
        for lines in collection:
            for words in lines:
                word_surface = font_m.render(words, True, (255, 255, 255))
                word_width , word_height = word_surface.get_size()
                if x + word_width >= available_width:
                    x = border
                    y += word_height
                screen.blit(word_surface, (x,y))
                x += word_width + space
            x = border
            y += word_height


        # Update content on screen
        pygame.display.flip()

    def draw_property(self, index, x, y, size):
        # Settings
        property_border = 6
        player_square_size = 20

        # Get current property
        property = self.properties[index]

        # If property is Property draw its color in the background
        if type(property) == Property:
            pygame.draw.rect(screen, property.color,
                    [x, y, size, size], 0)
        # Else draw the standard green
        else:
            pygame.draw.rect(screen, (204, 228, 207),
                    [x, y, size, size], 0)
        
        # Draw name
        property_name = font_s.render(property.name, 1, (0, 0, 0))
        property_name_height, property_name_height = property_name.get_size()
        screen.blit(property_name, (x + property_border, y + property_border))

        # Draw subtext of property (owner or description)
        subtext = font_xs.render('', 1, (0, 0, 0))
        # If property is Property draw its owner or its value
        if type(property) == Property:
            if property.owner != None:
                subtext = font_xs.render(self.players[property.owner].name, 1, (0, 0, 0))
            else:
                subtext = font_xs.render(f"{property.value}$", 1, (0, 0, 0))
        elif property.name in ['KPMG Gallery', 'Haddad', 'Westmont']:
            subtext = font_xs.render('Random Card', 1, (0, 0, 0))
        elif property.name == 'Student Union':
            subtext = font_xs.render('SU fees: -50$', 1, (0, 0, 0))

        # Display subtext
        screen.blit(subtext, (x + property_border, y + property_name_height + property_border))

        # Calculate margin between players
        margin_between_players = (size - 2 * property_border - 4 * player_square_size) // 3

        # Draw players
        for p in range(len(self.players)):
            # If player is in this property, draw him
            if self.players[p].position == index:

                # Draw player background color
                player_color_x = x + property_border + p * margin_between_players + p * player_square_size
                player_color_y = y + size - border
                pygame.draw.rect(screen, colors[p], [player_color_x, player_color_y, player_square_size, player_square_size], 0, border_radius=4)
                
                # Draw player's initial
                player_initial = font_xs.render(self.players[p].name[0].upper(), 1, (255, 255, 255))
                player_initials_x = player_color_x + ((player_square_size - player_initial.get_width()) // 2)
                player_initials_y = player_color_y + ((player_square_size - player_initial.get_height()) // 2)

                
                screen.blit(player_initial, ([player_initials_x, player_initials_y]))

                player_color_x += 3

    def prompt(self, text):
        # Change prompt_text variable
        self.prompt_text = text

        # Redraw screen
        self.draw_screen()


###### Initialize game ######

# Create or load game
board = Board()

# Remove play.py from argv
sys.argv.pop(0)

# Make sure arguments exist
if len(sys.argv) == 0:
    print('Input either the name of the players or the name of the saved game')
    sys.exit()

# If only one argument load saved game
elif len(sys.argv) == 1:
    # Make sure file exists
    if not os.path.exists(f"saved_games/{sys.argv[0]}.json"):
        print(f"Saved game {sys.argv[0]} does not exist")
        sys.exit()
    
    else:
        # Load data
        with open(f"saved_games/{sys.argv[0]}.json", "r") as file:
            data = json.load(file)

            players = [Player(player['name'], player['position'], player['balance'], player['out_of_library_cards'], player['rounds_in_library_left']) for player in data['players']]

            board.load_game(players,  data['properties'], data['current_player'], data['santander_money'])

# Max 4 players
elif len(sys.argv) > 4:
    print('4 players maximum!')
    sys.exit()

# Otherwise create a game with each argument being a player (this only runs if 2 to 4 players)
else:
    # Create board and players
    board = Board()

    # Shuffle players' order
    players = [Player(player_name) for player_name in sys.argv]
    random.shuffle(players)

    # Load game board
    board.load_game(players, [None for i in range(len(board.properties))])

# Start game loop
board.next_round()