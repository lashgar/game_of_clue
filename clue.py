import random

# define the game board
board = [
    ["Study", "Hallway", "Library", "Hall", "Lounge"],
    ["Kitchen", "Ballroom", "Conservatory", "Billiard Room", "Dining Room"],
    ["Cellar", "Secret Passage", "Cellar", "Secret Passage", "Cellar"]
]

# define the suspects, weapons, and rooms
suspects = ["Colonel Mustard", "Miss Scarlett", "Professor Plum", "Mr. Green", "Mrs. Peacock", "Mrs. White"]
weapons = ["Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", "Wrench"]
rooms = ["Study", "Kitchen", "Ballroom", "Conservatory", "Billiard Room", "Library", "Hall", "Lounge", "Dining Room", "Cellar"]

# create a dictionary to map cards to their categories
card_types = {"suspect": suspects, "weapon": weapons, "room": rooms}

player_names = ["Ahmad", "Arghavan", "Babak", "Mina", "Mostafa", "Ebad"]

class DetectiveSheet:
    def __init__(self, num_players):
        self.players_have = []
        self.players_not_have = []
        for i in range(0,num_players):
            self.players_have.append([])
            self.players_not_have.append([])

    def inform_have(self, player_id, card):
        if card in self.players_have[player_id]:
            return # already exists
        self.players_have[player_id].append(card)

    def inform_not_have(self, player_id, card):
        if card in self.players_not_have[player_id]:
            return # already exists
        self.players_not_have[player_id].append(card)

    def summarize_findings(self):
        for i, have in enumerate(self.players_have):
            print(f"  Player {i} have {have}")
        for i, not_have in enumerate(self.players_not_have):
            print(f"  Player {i} doesn't have {not_have}")
        print(f"  possible accusation: {self.get_suspeciouns()}")

    def get_suspeciouns(self):
        definit_accusation = []
        resolved_types = []
        for card in suspects + weapons + rooms:
            none_have = True
            for not_have in self.players_not_have:
                if card not in not_have:
                    none_have = False # one player might still have this
                    break
            if none_have:
                definit_accusation.append(card)
                if card in suspects:
                    resolved_types.append('suspect')
                elif card in weapons:
                    resolved_types.append('weapon')
                elif card in rooms:
                    resolved_types.append('room')

        # while making possible accusation, keep no other card of a type we know definitely
        unresolved_cards = []
        if 'suspect' not in resolved_types:
            unresolved_cards += suspects
        if 'weapon' not in resolved_types:
            unresolved_cards += weapons
        if 'room' not in resolved_types:
            unresolved_cards += rooms

        possible_accusation = [] + definit_accusation
        for card in unresolved_cards:
            one_have = False
            for haves in self.players_have:
                if card in haves:
                    one_have = True
                    break
            if not one_have:
                possible_accusation.append(card)

        random.shuffle(possible_accusation)
        return possible_accusation

    def get_suggestion(self):
        suspeciouns = self.get_suspeciouns()
        murderer, weapon, room = None, None, None
        for a in suspeciouns:
            if a in suspects:
                murderer = a
            elif a in weapons:
                weapon = a
            elif a in rooms:
                room = a
        assert murderer != None
        assert weapon != None
        assert room != None
        assurance = 3/len(suspeciouns)
        return assurance, (murderer, weapon, room)



# define the player class
class Player:
    def __init__(self, name, game_piece, num_players):
        self.name = name
        self.game_piece = game_piece
        self.hand = []
        self.detective_sheet = DetectiveSheet(num_players)

    def init_detective_sheet(self, player_id):
        for card in self.hand:
            self.detective_sheet.inform_have(player_id, card[1])
        for card in suspects+weapons+rooms:
            if card not in [c[1] for c in self.hand]:
                self.detective_sheet.inform_not_have(player_id, card)

    def get_suggestion(self):
        # suspect = suspects[int(random.random()*len(suspects))]
        # weapon  = weapons[int(random.random()*len(weapons))]
        # room    = rooms[int(random.random()*len(rooms))]
        # return (suspect, weapon, room)
        return self.detective_sheet.get_suggestion()

    # poll if player has any of the card in the suggestion
    def get_player_response(self, suggestion):
        random.shuffle(self.hand) # TODO: shuffle to suggestion randomly, if multiple suggesions exists.
        for hand_card in self.hand:
            for suggestion_card in suggestion:
                if hand_card[1] == suggestion_card:
                    return hand_card
        return None

    def inform_have(self, player_id, card):
        self.detective_sheet.inform_have(player_id, card)

    def inform_not_have(self, player_id, card):
        self.detective_sheet.inform_not_have(player_id, card)

    def summarize_findings(self):
        self.detective_sheet.summarize_findings()

    def __str__(self):
        return self.name

# define the game class
class ClueGame:
    def __init__(self, num_players):
        self.num_players = num_players
        self.players = []
        self.murderer = None
        self.murder_weapon = None
        self.murder_room = None
        self.current_player_index = 0
        self.board = board
        self.deck = []
        self.turns = 0
        self.suspects = suspects
        self.weapons = weapons
        self.rooms = rooms

    # function to set up the game
    def setup(self):
        # choose the murderer, weapon, and room cards at random
        self.murderer = random.choice(suspects)
        self.murder_weapon = random.choice(weapons)
        self.murder_room = random.choice(rooms)

        # create the player objects
        self.create_players()

        # create the deck of cards
        self.create_deck()

        # shuffle the deck and deal the cards to the players
        self.deal_cards()

        # print the murder solution
        print(f"The murderer is {self.murderer}, the weapon is {self.murder_weapon}, and the room is {self.murder_room}.")

    # function to create the player objects
    def create_players(self):
        for i in range(self.num_players):
            name = player_names[i] # input(f"Enter the name of player {i+1}: ")
            game_piece = suspects[i] # input(f"Enter the game piece for player {name}: ")
            self.players.append(Player(name, game_piece,self.num_players))

    # function to create the deck of cards
    def create_deck(self):
        for card_type, cards in card_types.items():
            for card in cards:
                if card not in [self.murderer, self.murder_weapon, self.murder_room]:
                    self.deck.append((card_type, card))
        random.shuffle(self.deck)

    # function to deal the cards to the players
    def deal_cards(self):
        total_cards = len(self.deck)
        # deal equal numbers to all players
        num_cards_per_player = total_cards // self.num_players
        for player in self.players:
            player.hand = self.deck[:num_cards_per_player]
            self.deck = self.deck[num_cards_per_player:]
        # deal remaining cards
        remainder = total_cards - num_cards_per_player * self.num_players
        for i in range(0,remainder):
            self.players[i].hand += [self.deck[0]]
            self.deck = self.deck[1:]
        # initialize the detective sheets
        for i in range(0,len(self.players)):
            self.players[i].init_detective_sheet(i)

    # function to get the current player
    def get_current_player(self):
        return self.players[self.current_player_index]

    # function to get the next player
    def get_next_player(self):
        self.current_player_index = (self.current_player_index + 1) % self.num_players

    # function to run the game
    def run(self):
        self.setup()

        # continue playing until someone wins
        while True:
            self.turns += 1
            print(f"\n===============================\nTurn {self.turns}:")
            current_player = self.get_current_player()
            print(f"It's {current_player}'s turn.")

            # display the game board and the player's hand
            # self.display_board()
            # self.display_hand(current_player)

            # print findings of current player
            print(f"Here is what {self.players[self.current_player_index]} knows so far:")
            current_player.summarize_findings()

            # get the player's suggestion
            assurance, suggestion = current_player.get_suggestion()
            print(f"{current_player} made a suggestion: {suggestion}, assurance: {assurance}")

            # other players respond to the suggestion
            self.make_suggestion(suggestion, current_player)

            #now  check if the player has an accusation
            assurance, accusation = current_player.get_suggestion()
            if assurance > 0.8:
                # accuse!
                print(f"{current_player} made an accusation: {accusation}, assurance: {assurance}")
                if accusation == (self.murderer, self.murder_weapon, self.murder_room):
                    print(f"\nCongratulations, {current_player} has solved the murder mystery!")
                    print("The game is over.")
                    return

            # move on to the next player
            self.get_next_player()

    # function to display the game board
    def display_board(self):
        print("\n".join(" | ".join(cell.center(10) for cell in row) for row in self.board))

    # function to display a player's hand
    def display_hand(self, player):
        print(f"\n{player}'s hand:", ", ".join(card[1] for card in player.hand))

    # function to make a suggestion to the other players
    def make_suggestion(self, suggestion, current_player):
        print(f"\n {current_player} suggests that the murder was committed by {suggestion[0]} in the {suggestion[2]} with the {suggestion[1]}.")
        # poll from immediately next player and continue
        for i in range(1,self.num_players):
            turn_id = (self.current_player_index + i) % self.num_players
            player = self.players[turn_id]
            response = player.get_player_response(suggestion)
            # process information
            if response:
                print(f"  {player} showed {response[1]} to {current_player}.")
                current_player.inform_have(turn_id, response[1])
                break # stop when first player made a suggestion
            else:
                print(f"  {player} didn't have any of the suggestion card, player hand: {[c[1] for c in player.hand]}.")
                for card in suggestion:
                    # this is an information for all players cause we know none of the card existed
                    for k in range(0,self.num_players):
                        self.players[k].inform_not_have(turn_id, card)

    # function to get the next player
    def get_next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    # function to get the current player
    def get_current_player(self):
        return self.players[self.current_player_index]

if __name__ == "__main__":
    random.seed()
    g = ClueGame(len(player_names))
    g.run()
