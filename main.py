
import io
from contextlib import redirect_stdout
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/play_game', methods=['POST'])
def play_game():
    f = io.StringIO()
    with redirect_stdout(f):
        start_game()
    output = f.getvalue()
    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(debug=True)

count = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/increment', methods=['POST'])
def increment():
    global count
    count += 1
    return jsonify({'count': count})


@app.route('/flip_case', methods=['POST'])
def flip_case():
    text = request.json['text']
    flipped_text = ''.join(c.lower() if c.isupper() else c.upper() for c in text)
    return jsonify({'flipped_text': flipped_text})

import json
import sys
import random
from typing import List, Optional, Tuple
from enum import Enum
import os


class EventStatus(Enum):
    UNKNOWN = "unknown"
    PASS = "pass"
    FAIL = "fail"
    PARTIAL_PASS = "partial_pass"


class Statistic:
    def __init__(self, name: str, value: int = 0, description: str = "", min_value: int = 0, max_value: int = 100):
        self.name = name
        self.value = value
        self.description = description
        self.min_value = min_value
        self.max_value = max_value

    def __str__(self):
        return f"{self.name}: {self.value}"

    def modify(self, amount: int):
        self.value = max(self.min_value, min(self.max_value, self.value + amount))


class Character:
    def __init__(self, name: str = "Bob", strength_value: int = 10, intelligence_value: int = 10, stamina_value: int = 10, agility_value: int = 10):
        self.name = name
        self.is_invisible = False
        self.strength = Statistic("Strength", value=strength_value, description="Strength is a measure of physical power.")
        self.intelligence = Statistic("Intelligence", value=intelligence_value, description="Intelligence is a measure of cognitive ability.")
        self.stamina = Statistic("Stamina", value = stamina_value, description="Stamina is a measure of endurance")
        self.agility = Statistic("Agility", value = agility_value, description="Agility is a measure of nimbleness")

    def __str__(self):
        return f"Character: {self.name}, Strength: {self.strength}, Intelligence: {self.intelligence}"

    def get_stats(self):
        return [self.strength, self.intelligence, self.stamina, self.agility]  # Extend this list if there are more stats
    
total_characters = [
    Character(name="Jonathan Davis", strength_value= 40, intelligence_value=50, stamina_value=20, agility_value=10),
    Character(name="Fred Durst", strength_value=50, intelligence_value=10, stamina_value=35, agility_value=25),
    Character(name="Solana SZA", strength_value=25, intelligence_value=40, stamina_value=20, agility_value=35),
    Character(name="Soobin Choi", strength_value=15, intelligence_value=25, stamina_value=45, agility_value=35),
    Character(name="Chappell Roan", strength_value=20, intelligence_value=35, stamina_value=40, agility_value=25),
    Character(name="Sabrina Carpenter", strength_value=40, intelligence_value=20, stamina_value=25, agility_value=35),
    Character(name="Beyoncé", strength_value=35, intelligence_value=40, stamina_value=20, agility_value=25),
    Character(name="Ariana Grande", strength_value=50, intelligence_value=35, stamina_value=20, agility_value=25),
    Character(name="Theo James", strength_value=35, intelligence_value=45, stamina_value=20, agility_value=30),
    Character(name="Anne Hathaway", strength_value=15, intelligence_value=25, stamina_value=30, agility_value=50)
]

class Event:
    def __init__(self, primary_attribute, secondary_attribute, prompt_text, pass_message, fail_message, partial_pass_message):
        self.primary_attribute = primary_attribute
        self.secondary_attribute = secondary_attribute
        self.prompt_text = prompt_text
        self.pass_message = pass_message
        self.fail_message = fail_message
        self.partial_pass_message = partial_pass_message
        self.status = EventStatus.UNKNOWN

    def execute(self, party: List[Character], parser, game):
        print(self.prompt_text)
        character = parser.select_party_member(party)
        chosen_stat = parser.select_stat(character)
        self.resolve_choice(character, chosen_stat, game)

    def resolve_choice(self, character: Character, chosen_stat: Statistic, game):
        if chosen_stat.name == self.primary_attribute:
            self.status = EventStatus.PASS
            print(self.pass_message)
        elif chosen_stat.name == self.secondary_attribute:
            self.status = EventStatus.PARTIAL_PASS
            print(self.partial_pass_message)
        else: 
        # Instead of outright failing, give a secondary challenge
            if random.random() < 0.5:  # 50% chance to let them try again with another stat
                print("You nearly made a mistake, but you're given the opputunity to try again...")
                new_stat = game.parser.select_stat(character)  # Re-select a stat
                if new_stat.name in [self.primary_attribute, self.secondary_attribute]:
                    print("💡 You found another way to complete the task!")
                    self.status = EventStatus.PARTIAL_PASS
                    print(self.partial_pass_message)
                    return
        
            self.status = EventStatus.FAIL 
            print(self.fail_message)

        # Winning condition
        if "win the game" in self.pass_message:
            print("🏆 You captured the flag and WON the game!")
            game.continue_playing = False

        if "eliminate" in self.pass_message:
            if game.opposing_team:
                eliminated_enemy = random.choice(game.opposing_team)
                game.opposing_team.remove(eliminated_enemy)
                print(f"You eliminated {eliminated_enemy.name} from the opposing team!")    
      
        if self.status == EventStatus.FAIL:
            if character in game.party:
                game.party.remove(character)
                print(f"{character.name} has been captured and removed from your team!")

        if not game.party:
            print("❌ Your entire team has been captured! GAME OVER.")
            game.continue_playing = False

class Location:
    def __init__(self, events: List[Event]):
        self.events = events
        self.max_events = 3

    def get_event(self) -> Event:
        return random.choice(self.events)
    
    def is_completed(self, completed_events: int) -> bool:
        return completed_events >= self.max_events

def create_recon_events():
    return [
        Event(primary_attribute="Intelligence",
            secondary_attribute="Agility",
            prompt_text="You need to send a party member to do recon on the other team, who will you send?",
            pass_message="Your party member was successful in collecting info and returned safely, here is what they learned: "
            "Jonathan Davis; Strength: 50 Intelligence: 50 Stamina: 10 Agility: 10 /"
            "/ Fred Durst; Strength: 50 Intelligence: 10 Stamina: 30 Agility: 30 /"
            "/ Solana SZA; Strength: 30 Intelligence: 40 Stamina: 20 Agility: 30 /"
            "/ Soobin Choi; Strength: 20 Intelligence: 20 Stamina: 45 Agility: 35 /"
            "/ Chappell Roan; Strength: 30 Intelligence: 30 Stamina: 30 Agility: 30 /"
            "/ Sabrina Carpenter; Strength: 40 Intelligence: 20 Stamina: 30 Agility: 30 /"
            "/ Beyoncé; Strength: 30 Intelligence: 30 Stamina: 30 Agility_: 30 /"
            "/ Ariana Grande; Strength: 50 Intelligence: 30 Stamina: 20 Agility: 30 /"
            "/ Theo James; Strength: 30 Intelligence: 40 Stamina: 30 Agility: 30 /"
            "/ Anne Hathaway; Strength: 20 Intelligence: 20 Stamina: 30 Agility: 50",
            fail_message="Your party member failed to collect information and was captured by the other team!",
            partial_pass_message="Your party member returned safely but was unable to learn anything."
                ),
        Event(
            primary_attribute="Intelligence",
            secondary_attribute="Agility",
            prompt_text="You decipher enemy signals to predict their moves. What stat do you rely on?",
            pass_message="You outsmart the enemy, avoiding their trap entirely!",
            fail_message="You walk right into their ambush. One team member is taken!",
            partial_pass_message="You evade the trap but they know you're nearby!"
        ),
        Event(
            primary_attribute="Strength",
            secondary_attribute="Intelligence",
            prompt_text="You encounter a guard while reconning. Do you engage?",
            pass_message="You successfully bypass the guard.",
            fail_message="The guard catches you and you are thrown out.",
            partial_pass_message="You manage to sneak past, but the guard notices you."
        )
    ]

def create_mid_events():
        return [
        Event(
            primary_attribute="Agility",
            secondary_attribute="Strength",
            prompt_text="You sneak through a minefield guarding the enemy base. What stat do you rely on?",
            pass_message="You make it through the minefield without a scratch!",
            fail_message="BOOM! You trigger a mine and lose a teammate!",
            partial_pass_message="You get through but take a minor hit. Lose 10 stamina."
        ),
        Event(
            primary_attribute="Strength",
            secondary_attribute="Agility",
            prompt_text="You attempt to ambush a member of the enemy team. Which stat do you rely on?",
            pass_message="You overpower your opponent and eliminate them from the game!",
            fail_message="They turn the tables and capture one of your team members!",
            partial_pass_message="You surprise them, but they escape injured!"
        ),
        Event(
            primary_attribute="Agility",
            secondary_attribute="Stamina",
            prompt_text="You attempt to hide in the shadows. Do you succeed?",
            pass_message="You blend perfectly into the shadows.",
            fail_message="You fail and are noticed.",
            partial_pass_message="You hide, but not completely, and are half-noticed."
            )
        ]

def create_final_events():
    return [
        Event(
            primary_attribute="Agility",
            secondary_attribute="Intelligence",
            prompt_text="You attempt to stealthily infiltrate the enemy camp to steal their flag. What stat do you rely on?",
            pass_message="You slip in unnoticed, grab the flag, and make it back safely!",
            fail_message="You're caught! One of your party members is captured!",
            partial_pass_message="You grab the flag but trigger an alarm! Be careful!"
        ),
        Event(
            primary_attribute="Strength",
            secondary_attribute="Stamina",
            prompt_text="A boulder blocks your path! How do you get past?",
            pass_message="You lift the boulder like a champ! Clear path ahead.",
            fail_message="You can't move it, and your delay costs a team member!",
            partial_pass_message="You shove it aside, but you’re exhausted. Lose 10 stamina."
        ),
        Event( 
            primary_attribute="Stamina",
            secondary_attribute="Agility",
            prompt_text="With the flag in hand, you sprint back toward your base. How do you push through?",
            pass_message="You cross the finish line! Your team wins the game!",
            partial_pass_message="You’re close but get surrounded. Time to fight!",
            fail_message="You’re tackled, lose the flag, and one teammate is captured!")
    ]

class Game:
    def __init__(self, parser, characters: List[Character], locations: List[Location], chosen_party, opposing_team):
        self.is_invisible = None
        self.parser = parser
        self.total_characters = total_characters
        self.party = self.parser.party
        self.locations = locations
        self.continue_playing = True
        self.round_count = 0  # Track the number of rounds
        self.max_rounds = 10  # Set a limit for the game
        self.chosen_part = chosen_party
        self.opposing_team = opposing_team
        self.completed_events = 0  # Track how many events have been completed in the current location
        self.current_location = locations[0]  # Start with the first location
        self.is_insisible = False 

    def start(self):
        self.check_team_synergy()

        while self.continue_playing and self.round_count < self.max_rounds:
            print(f"\n🔹 Round {self.round_count + 1} 🔹")
            if self.round_count == 3:
                self.trigger_mini_boss(boss_number=1)
            elif self.round_count == 7:
                self.trigger_mini_boss(boss_number=2)
            elif self.round_count == self.max_rounds - 1:
                self.trigger_final_boss()

            location = random.choice(self.locations)
            event = location.get_event()
            event.execute(self.party, self.parser, self)

            if self.round_count == 6:
                self.trigger_special_event()
            
            self.check_game_over()
            self.round_count += 1
            if self.is_invisible:
                self.deactivate_invisibility()
        
        print("Game Over.")

    def check_team_synergy(self):
        print("✨ Checking team synergy!")
        if all(member.agility.value > 30 for member in self.party):
            print("💨 Your team is highly agile! +5 agility boost.")
            for member in self.party:
                member.agility.modify(5)

    def add_character_to_party(self):
        chosen_character = self.parser.make_your_party(self.total_characters)
        self.party.append(chosen_character)  # Add the selected character to the party
        print(f"{chosen_character.name} has been added to your party!")

    def display_party(self):
        print("\nYour current party members:")
        for member in self.party:
            print(f"{member.name} - Strength: {member.strength.value}, Intelligence: {member.intelligence.value}, Stamina: {member.stamina.value}, Agility: {member.agility.value}")

        print("Game Over.")

    def move_to_new_location(self):
        print("\nYou have completed the required number of events. Moving to a new location...\n")
        
        # Move to the next location
        next_location = self.locations[(self.locations.index(self.current_location) + 1) % len(self.locations)]
        self.current_location = next_location
        self.completed_events = 0  # Reset the event counter for the new location
        print(f"Now at a new location! ({self.current_location})")

    def check_game_over(self):
        if self.did_succeed():
            self.continue_playing = True

        # Add a chance for a special encounter
        if random.random() < 0.2:  # 20% chance for a surprise event
            self.trigger_special_event()

        return len(self.party) == 0
    
    def trigger_special_event(self):
        print("\n💥 A surprise event has occurred! 💥")

    # List of traps and power-ups (expanded)
        surprise_events = [
            {"description": "You stepped on a hidden trap! Lose 10 stamina.", "effect": lambda player: player.stamina.modify(-10)},
            {"description": "You find a Speed Boost potion! Gain +10 agility.", "effect": lambda player: player.agility.modify(10)},
            {"description": "A spiked pit appears! Lose 5 agility escaping it.", "effect": lambda player: player.agility.modify(-5)},
            {"description": "You find a Strength Gauntlet! Gain +15 strength.", "effect": lambda player: player.strength.modify(15)},
            {"description": "A sudden rockslide hits you! Lose 10 stamina.", "effect": lambda player: player.stamina.modify(-10)},
            {"description": "You discover an Invisibility Cloak! Sneak past obstacles next round.", "effect": lambda _: self.activate_invisibility()},
            {"description": "A lightning strike charges you up! Gain +5 strength and +5 agility.", "effect": lambda player: (player.strength.modify(5), player.agility.modify(5))},
            {"description": "An enemy sniper takes a shot! One random teammate loses 15 stamina.", "effect": lambda _: self.random_team_damage(15)},
            {"description": "You find a Medkit! Restore 20 stamina.", "effect": lambda player: player.stamina.modify(20)},
            {"description": "An adrenaline rush hits you! Gain +10 stamina and +10 agility.", "effect": lambda player: (player.stamina.modify(10), player.agility.modify(10))},
            {"description": "A bear suddenly appears! Lose 15 stamina while running away.", "effect": lambda player: player.stamina.modify(-15)},
            {"description": "You find an Ancient Amulet! ALL your stats increase by +5.", "effect": lambda player: (
                player.strength.modify(5), player.intelligence.modify(5),
                player.stamina.modify(5), player.agility.modify(5))},
        {"description": "You fall into a pit trap! Lose 5 agility and 5 stamina.", "effect": lambda player: (player.agility.modify(-5), player.stamina.modify(-5))},
        {"description": "You drink mysterious water... Gain +10 intelligence!", "effect": lambda player: player.intelligence.modify(10)},
    ]

        # Pick a random event
        selected_event = random.choice(surprise_events)

        # Print the event description
        print(f"⚡ {selected_event['description']}")

     # Apply the effect to the party
        if "Invisibility" in selected_event['description']:
            selected_event['effect'](None)  # Invisibility affects the team, not individual players
        elif "sniper" in selected_event['description']:
            selected_event['effect'](None)  # Sniper targets one random teammate
        else:
            for player in self.party:
                selected_event['effect'](player)


    def did_succeed(self):
        if self.round_count == 7:
            return True

    def activate_invisibility(self):
        self.is_invisible = True
        for member in self.party:
            member.is_invisible = True

    def deactivate_invisibility(self):
        self.is_invisible = False
        for member in self.party:
            member.is_invisible = False


    def random_team_damage(self, damage_amount):
        if self.party:
            unlucky_player = random.choice(self.party)
            unlucky_player.stamina.modify(-damage_amount)
            print(f"⚠️ {unlucky_player.name} was hit and lost {damage_amount} stamina!")
            if unlucky_player.stamina.value <= 0:
                print(f"💀 {unlucky_player.name} has collapsed from exhaustion and is out of the game!")
                self.party.remove(unlucky_player)

    def trigger_mini_boss(self, boss_number=1):
        if boss_number == 1:
            print("\n⚔️ MINI-BOSS BATTLE! ⚔️")
            boss_strength = random.randint(75, 100)
        else:
            print("\n🔥 FINAL MINI-BOSS APPROACHES! 🔥")
            boss_strength = random.randint(100, 130)

        print(f"The Mini-Boss has {boss_strength} strength!")

        total_team_strength = sum([member.strength.value for member in self.party])

        if total_team_strength > boss_strength:
            print("🎉 You defeated the Mini-Boss and earned +10 stamina and +10 agility for everyone!")
            for player in self.party:
                player.stamina.modify(10)
                player.agility.modify(10)
        else:
            print("💀 The Mini-Boss overpowered your team! You lose one random team member.")
            if self.party:
                unlucky = random.choice(self.party)
                print(f"{unlucky.name} was captured by the Mini-Boss!")
                self.party.remove(unlucky)

        
    def trigger_final_boss(self):
        print("\n👑 THE FINAL BOSS HAS ARRIVED! 👑")
        boss_strength = random.randint(150, 200)
        print(f"The Final Boss has {boss_strength} strength!")

        total_team_strength = sum([member.strength.value for member in self.party])

        if total_team_strength > boss_strength:
            print("🏆 You defeated the Final Boss and won the game!")
            self.continue_playing = False

        else:
            print("💀 The Final Boss crushes your team. GAME OVER.")
            self.party.clear()
            self.continue_playing = False



class UserInputParser:
    def __init__(self, max_party_size: int):
        self.party = []
        self.max_party_size = max_party_size

    def parse(self, prompt: str) -> str:
        return input(prompt)

    def make_your_party(self, total_characters: List[Character]) -> Tuple[List[Character], List[Character]]:
        unchosen_characters = total_characters.copy()
        while len(self.party) < self.max_party_size:
            print(f"\nParty size: {len(self.party)}/{self.max_party_size}")
            for idx, char in enumerate(total_characters):
                print(f"{idx + 1}. {char.name}")
            try:
                choice = int(self.parse("Choose a character: ")) - 1
                selected = total_characters[choice]
                if selected in self.party:
                    print("Already selected.")
                    continue
                self.party.append(selected)
                unchosen_characters.remove(selected)
            except (ValueError, IndexError):
                print("Invalid input.")
        return self.party, unchosen_characters

    def select_party_member(self, party: List[Character]) -> Character:
        while True:
            print("Choose a party member:")
            for idx, member in enumerate(party):
                print(f"{idx + 1}. {member.name}")
            user_input = self.parse("Enter the number of the chosen party member: ")

            if user_input.isdigit():  # Ensures the input is a valid number
                choice = int(user_input) - 1
                if 0 <= choice < len(party):  # Ensures the number is in range
                    return party[choice]
                else:
                    print("❌ Invalid choice. Please enter a number from the list.")
            else:
                print("❌ Invalid input. Please enter a number.")

    def select_stat(self, character: Character) -> Statistic:
        while True:
            print(f"Choose a stat for {character.name}:")
            stats = character.get_stats()
            for idx, stat in enumerate(stats):
                print(f"{idx + 1}. {stat.name} ({stat.value})")
            user_input = self.parse("Enter the number of the stat to use: ")

            if user_input.isdigit():  # Check if input is a valid number
                choice = int(user_input) - 1
                if 0 <= choice < len(stats):  # Ensure input is within valid range
                    return stats[choice]
                else:
                    print("❌ Invalid choice. Please enter a number from the list.")
            else:
                print("❌ Invalid input. Please enter a number.")    

def start_game():
    parser = UserInputParser(max_party_size=5)
    chosen_party, opposing_team = parser.make_your_party(total_characters)
    recon_events = create_recon_events()
    mid_events = create_mid_events()
    final_events = create_final_events()

    # Create locations with their respective events
    locations = [
        Location(recon_events), 
        Location(mid_events), 
        Location(final_events)
    ]
    game = Game(parser, total_characters, locations, chosen_party, opposing_team)
    game.start()


    print(f"\nYou have chosen the following characters for your party:")
    for character in chosen_party:
        print(f"{character.name}")


# if __name__ == "__main__":
#     start_game()

if __name__ == '__main__':
    app.run(debug=True)