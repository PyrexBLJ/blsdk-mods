import json
from pathlib import Path
from random import randint
import threading
import time
import unrealsdk
from typing import List, Tuple
from .Util import distance, get_player_location
try:
    from Mods.MapLoader import placeablehelper
except ImportError:
    import webbrowser

    webbrowser.open("https://bl-sdk.github.io/mods/MapLoader/")
    raise ImportError("Trivia requires the most recent version of MapLoader to be installed")
try:
    import Mods.UserFeedback as uFeed
except ImportError:
    import webbrowser

    webbrowser.open("https://bl-sdk.github.io/mods/UserFeedback/")
    raise ImportError("Trivia requires the most recent version of UserFeedback to be installed")

class QuestionLib:

    HARD_TRIVIA_QUESTIONS: List[list] = [
        ["What year did Borderlands 2 launch?", "2009", "2010", "2012", 3],
        ["Who drops the Pitchfork in BL2?", "Master Gee", "Sparky Flynt", "Gettle", 1],
        ["What element is most effective on armored enemies?", "shock", "corrosion", "fire", 2],
        ["What element is most effective on shielded enemies?", "fire", "explosive", "shock", 3],
        ["What quote is written in Bunker's cutscene card?", "00101010", "10200100", "10010030", 1],
        ["Which map is Mad Mel located in?", "Eridium Blights", "Bloodshot Stronghold", "Sawtooth Cauldron", 2],
        ["What weapon cannot be obtained from Moxxi's tip jar?", "Good Touch", "Crit", "Bad Touch", 2],
        ["What is the first thing Claptrap says when you meet him at Windshear Wastes?", "Handsome Jack's been busy.", "Great - another dead Vault Hunter.", "Wait a minute! - you're not dead!", 2],
        ["What is the optional objective for Reeth on the mission \"Assassinate the Assassins\"?", "Assassinate Reeth with Melee", "Assassinate Reeth with a Sniper Rifle", "Assassinate Reeth with a Pistol", 1],
        ["Who drops the Gub in BL2?", "Rakkman", "Doc Mercy", "Laney White", 3],
        ["What is the drop chance from Savage Lee for an Unkempt Harold?", "8%", "10%", "15%", 2],
        ["Which raid boss cannot drop the Norfleet?", "Vermivorous the Invincible", "Master Gee the Invincible", "Hyperius the Invincible", 2],
        ["Which boss doesn't have the Pyrophobia as a dedicated drop source?", "Clark the Combustible", "Hyperius the Invincible", "Scorch", 3],
        ["What is the name of Salvador's right skill tree?", "Brawn", "Gun Lust", "Rampage", 1],
        ["What is the name of Maya's left skill tree?", "Cataclysm", "Harmony", "Motion", 3],
        ["What is the name of Krieg's middle skill tree?", "Hellborn", "Mania", "Bloodlust", 2],
        ["What is the elemental multiplier for fire on flesh enemies?", "1.5x", "1.75x", "2.0x", 2],
        ["What is the minimum amount of bullets needed in the magazine for Salvador to receive a full moneyshot skill bonus?", "8", "10", "12", 3],
        ["Handsome Jack almost forgot what element during your fight with Bloodwing?", "Slag", "Corrosive", "Explosive", 3],
        ["What is the minimum level you can find a rocket launcher at?", "8", "10", "15", 2],
        ["How many pellets does a Rustler's Quad have?", "18", "20", "21", 2],
        ["Vladof sight can roll on everything except...", "Torgue Assault Rifles", "Hyperion Pistols", "Vladof Rocket Launchers", 2],
        ["What is the drop chance from Saturn for a Hive?", "3.3%", "10%", "33%", 1],
        ["Which map is Sparky Flynt located in?", "Southern Shelf", "Bloodshot Stronghold", "Wam Bam Island", 3],
        ["How many seraph crystals does it cost to buy a weapon from a seraph vendor?", "90", "120", "150", 2],
        ["Which grip gives the Heartbreaker the fastest reload speed?", "Tediore grip", "Hyperion grip", "Jakobs grip", 2 ],
        ["Tediore grip can roll on everything except...", "Jakobs Pistols", "Vladof Rocket Launchers", "Maliwan SMGs", 1],
        ["How much of your total money spent on respawning fees?", "5%", "7%", "10%", 2],
        ["What element does the Jakobs manufacturer lack in BL2?", "Corrosive", "Shock", "Slag", 3],
        ["What did Axton name his turret?", "Jessica", "Rachael", "Sarah", 3],
        ["Who killed Lucky Zaford?", "Hodunk Clan", "Scooter", "Moxxi", 2],
        ["What is not a listed crime on Salvador's wanted poster?", "Robbery", "Cannibalism", "Profanity", 1],
        ["What enemy cannot be a tubby variant?", "Stalker", "Rakk", "Bullymong", 3],
        ["Which mission reward is obtain from the quest \"Splinter Group\"?", "Storm Front", "RokSalt", "Dog", 2],
        ["Which enemy can slag not be applied to by the player?", "Slag Turret", "Bedrock Bullymong", "Slagged Skag", 3],
        ["What is the name of Gaige's right skill tree?", "Little Big Trouble", "Best Friends Forever", "Ordered Chaos", 3],
        ["What is the maximum level the Lascaux SMG can be scaled to in normal mode?", "9", "10", "11", 3],
        ["What quote is written in Tiny Tina's base game cutscene card?", "Pop Goes the Bandit", "World's Deadliest 13 Year Old", "Mildly Insane", 2],
        ["The Minecraft easter egg is found in which map?", "Thousand Cuts", "Caustic Caverns", "Wildlife Preserve", 2],
        ["What is the name of the blue loader that rarely spawns from containers?", "Jimmy J3NKN5", "J1mmy JENKNS", "JIMMY J3NKN5", 1],
        ["Foreman Jasper spawns in during what mission?", "Hell Hath No Fury", "Rocko's Modern Strife", "Capture the Flags", 1],
        ["What does the Intense prefix on the Unkempt Harold give?", "Bonus Reload Speed", "Bonus Magazine Size", "Bonus Fire Rate", 3],
        ["Which enemy doesn't have the Whisky Tango Foxtrot as a dedicated drop?", "Hyperius the Invincible", "Tubby Skag", "Pimon", 3],
        ["Which band played the BL2 intro song \"Short Change Hero\"?", "Foo Fighters", "The Heavy", "Taylor Swift", 2],
        ["What gun type does Maliwan not make in BL2?", "Snipers", "Pistols", "Shotguns", 3],
        ["What does the \"E\" in E-tech stand for?", "Eridian", "Energy", "Ectoplasm", 1],
        ["Who drops Zero's \"C0al Train\" head cosmetic?", "Bunker", "Terramorphous the Invincible", "Tinder Snowflake", 2],
        ["What does the binary boss at Digi-peak translate to?", "OMGWTH", "WTFLOL", "OMGWTF", 1],
        ["What absorb chance is a Hyperion + Dahl + Tediore parted Sham?", "78%", "80%", "81%", 3],
        ["Which one of these cannot be boosted by Badass Rank?", "Gun Accuracy", "Gun Swap Speed", "Grenade Damage", 2],
        ["How much eridium does a tier 4 weapon SDU cost?", "12", "16", "20", 3],
        ["How many digits + characters does a SHiFT code have not including the dashes?", "16", "20", "25", 3],
        ["What are the vehicles in Scarlett DLC called?", "Sandboats", "Runners", "Sandskiffs", 3],
        ["How many maps are in Scarlett DLC?", "5", "7", "8", 2],
        ["How do you spell the name of the giant loader boss at the end of Washburne Refinery?", "H3RL-E", "HERL-3", "H3RL-3", 1],
        ["What is the name of Captain Blade's stalker pet?", "Tanner", "Twinkle", "Tinkles", 3],
        ["What is the chance of rolling a matching grip fire Pimpernel?", "10%", "8%", "5%", 3],
        ["How many Message in a Bottle quests are there in Scarlett DLC?", "3", "5", "7", 2],
        ["How much eridium does it cost to open Master Gee's arena door?", "4", "8", "12", 2],
        ["Which one of these items can Master Gee not drop?", "Storm Front", "The Bee", "Veruc", 3],
        ["How many new weapons were introduced in Torgue DLC?", "5", "6", "7", 1],
        ["How many maps are there in Torgue DLC?", "5", "7", "9", 2],
        ["How many Torgue Tokens does it cost to buy a legendary from a Torgue vendor?", "120", "250", "613", 3],
        ["Which one of these contestants are not on the top ten badass board in Torgue DLC?", "Exploding Adam", "Skullcrusher", "The Iron Trousers", 1],
        ["Which one of these enemies can you fight in Torgue DLC?", "Flyboy", "Pyre Pete", "Game Critic", 3],
        ["What is the drop chance for the CHOPPER from Dexiduous the Invincible?", "10%", "33%", "50%", 2],
        ["Which one of these raid bosses is not a seraph guardian?", "Dexiduous the Invincible", "Voracidous the Invincible", "Ancient Dragons of Destruction", 1],
        ["Which dedicated drop does Voracidous the Invincible have?", "Rough Rider", "Lead Storm", "Legendary Engineer", 2],
        ["What is the chance that an Ultimate Badass Savage can evolve into Triple O?", "5%", "10%", "1%", 3],
        ["How many experience points are rewarded per revive?", "100xp", "500xp", "1000xp", 1],
        ["What is the final story mission in the Fight for Sanctuary DLC called?", "Fight for Sanctuary", "Paradise Lost", "Paradise Found", 3],
        ["How many red chests are in Terramorphous's Lair?", "2", "3", "4", 1],
        ["How many total spawn points does Michael Mamaril have in Sanctuary?", "5", "8", "10", 3],
        ["How much HP is lost upon activating Gaige's Blood Soaked Shields skill if 5 points are applied?", "5%", "7%", "10%", 1],
        ["How many vault symbol challenges are in Arid Nexus Boneyard?", "0", "2", "3", 1],
        ["What is the drop chance for the Infection Cleaner SMG from a New Pandoran enemy?", "1%", "5%", "10%", 1],
        ["Which one of these enemies cannot drop the Infection Cleaner SMG?", "Lt. Angvar", "Lt. Bolson", "Lt. Tetra", 2],
        ["What is the drop chance for the Infinity pistol from Lt. Angvar?", "10%", "12.5%", "15%", 2],
        ["What is the drop chance for the Retainer shield from a Sandworm Queen in Fight for Sanctuary DLC?", "5%", "10%", "20%", 3],
        ["What is the drop chance for the Toothpick from a Sandworm in Fight for Sanctuary DLC while in TVHM?", "1%", "2%", "3%", 2],
        ["How many different stat rolls are there for the Deputy Badge?", "3", "4", "6", 2],
        ["What is the area called in Three Horns Divide where the guarateed Savage Lee spawns?", "Frostbite Tundra", "Marrowfield", "Icy Bottoms", 2],
        ["What sniper scope manufacturer has the most zoom?", "Dahl", "Vladof", "Hyperion", 3],
        ["What level do blue rarity class mods give +4 and +3 on their skill boosts?", "25", "38", "50", 1],
        ["What is the minimum level for blue rarity class mods to give you +6 and +5 on skill boosts?", "38", "50", "61", 2],
        ["What is the minimum level to be able to spec into a tier 3 skill tree skill?", "11", "15", "16", 3],
        ["What is the maxiumum percentage you can roll on an OP10 Moxxi's Endowment relic?", "9.9%", "11.6%", "12.5%", 2],
        ["How much bonus damage is given to the Toothpick assault rifle while wearing the Mouthwash relic?", "100%", "200%", "300%", 2],
        ["What is the fastest recharge delay you can roll on a Bee shield?", "5.04", "6.16", "6.66", 1],
        ["What is the fastest vehicle in Borderlands 2?", "Runner", "Fanboat", "Bandit Barrel Technical", 3],
        ["When does the game drop ammo in your favor?", "40%", "50%", "60%", 1],
        ["How many grenades are given from a single grenade ammo purchase from an ammo vendor?", "1", "2", "3", 3],
        ["What is the healing percentage of the Rubi pistol?", "10%", "12%", "15%", 2],
        ["What is the healing percentage of the Grog Nozzle?", "12%", "25%", "65%", 3],
        ["Which one of these are not a dedicated drop from the Handsome Sorcerer boss?", "The Bee", "Non-Unique Blue Relic", "Purple Rarity Magic Missile", 3],
        ["How long is the timer countdown for the side mission Claptrap's Birthday Bash?", "1:30", "2:10", "2:30", 2],
        ["What is the drop chance for a Storm Front from a Splinter Group rat?", "2.5%", "5%", "10%", 1],
        ["What is the maximum damage bonus you can receieve from Salvador's No Kill Like Overkill skill?", "100%", "250%", "500%", 3],
        ["How many different locations can the Gwen's Head pistol box spawn at?", "3", "4", "5", 3],
        ["What is the slag chance percentage on a maliwan gripped Grog Nozzle?", "26.5%", "50.4%", "65%", 2],
    ]

    EASY_TRIVIA_QUESTIONS: List[list] = [
        ["Who has the Unkempt Harold as a dedicated drop?", "Rakkman", "Savage Lee", "Mick Zaford", 2],
        ["What map is the Lascaux found in?", "Lynchwood", "Southern Shelf", "Frostburn Canyon", 3],
        ["What is Mr. Torgue's last name?", "Explosions", "High Five", "Flexington", 3],
        ["Who steals Claptrap's eye at Windshear Wastes?", "Captain Flynt", "Knuckledragger", "Hammerlock", 2],
        ["Where is the TMNT easter egg located?", "Wildlife Preserve", "Washburne Refinery", "Bloodshot Stronghold", 3],
        ["How many playable vault hunters are in BL2?", "4", "6", "8", 2],
        ["Who is responsible for taking Hammerlock's original arm and leg?", "Dribbles", "Old Slappy", "Captain Flynt", 2],
        ["What is the drop chance for a Badaboom from King Mong?", "3%", "5%", "10%", 2],
        ["What is the drop chance for a Striker from Old Slappy?", "5%", "10%", "15%", 2],
        ["Who is the main antagonist in BL2?", "Handsome Jack", "Ransom Back", "Phantom Hack", 1],
        ["What map is the double rainbow easter egg located in?", "The Highlands", "Thousand Cuts", "Caustic Caverns", 1],
        ["What is the maximum amount of eridium the player can hold?", "200", "250", "500", 3],
        ["How much eridium does it cost to feed Buttstallion once?", "4", "5", "8", 2],
        ["Who can you purchase the Mysterious Amulet from?", "Mr. Miz", "Sir Hamlet", "Mr. Mister", 1],
        ["What is Mick Zaford's dedicated legendary drop?", "Slagga", "Veruc", "Maggie", 3],
        ["Which unique enemy doesn't respawn?", "Sully the Blacksmith", "Saturn", "Black Queen", 1],
        ["What mission spawns in the boss Henry?", "Stalker of Stalkers", "Cold Shoulder", "Best Mother's Day Ever", 3],
        ["Which NPC is met for the first time during the quest A Dam Fine Rescue?", "Brick", "Roland", "Mordecai", 2],
        ["How much ammo does a Double Penetrating Unkempt Harold consume per shot?", "3", "4", "6", 3],
        ["Who runs the bandit slaughter?", "Moxxi", "Fink", "Jack", 2],
        ["Torgue doesn't manufacture which weapon type in Borderlands 2?", "Sniper Rifles", "Shotguns", "Pistols", 1],
        ["Which one of these are not a rollable prefix on Dahl SMGs?", "Flying", "Neutralizing", "Stopping", 2],
        ["How many Overpowered levels are there?", "5", "8", "10", 3],
        ["Who gives you the side mission \"Do No Harm\"?", "Tannis", "Zed", "Lilith", 2],
        ["How many injectors are connected to Angel at Control Core?", "3", "4", "5", 1],
        ["What level is Terramorphous the Invincible in Normal Mode?", "40", "50", "52", 3],
        ["What mission reward can be obtained for completing the side mission \"Safe and Sound\"?", "Fabled Tortoise", "Heart Breaker", "Rubi", 2],
        ["What enemy cannot be a tubby variant?", "Spiderant", "Bullymong", "Rakk", 2],
        ["Who gives the side mission \"Perfectly Peaceful\"?", "Tannis", "Claptrap", "Hammerlock", 3],
        ["Turtle shields have a high shield capacity at the cost of what?", "Movement Speed", "Health", "Fight For Your Life Duration", 2],
        ["How many legs does a Crystalisk enemy have?", "3", "4", "5", 1],
        ["What is the maximum amount of backpack slots you can unlock?", "33", "36", "39", 3],
        ["How many times does a Larval Varkid have to evolve to become Vermivorous the Invincible?", "4", "5", "6", 2],
        ["What manufacturer logo is found on any lootable green dumpster?", "Atlas", "Jakobs", "Dahl", 3],
        ["How many Bullymong furs must be collected for the side mission \"Bad Hair Day\"?", "3", "4", "5", 2],
        ["The Wattle Gobbler Headhunter DLC is a reference to what movie?", "The Hunger Games", "Charlie and the Chocolate Factory", "Mouse Hunt", 1],
        ["What is Maya's action skill called?", "Phasesock", "Phasemock", "Phaselock", 3],
        ["Who has the Volcano as a dedicated drop?", "Sully the Blacksmith", "Warrior", "Incinerator Clayton", 2],
        ["How many red chests are in Marcus's loot room after Control Core?", "2", "3", "4", 2],
        ["Krieg as the-", "Bandit", "Psycho", "Marauder", 2],
        ["My Siren's name is _____ and she is the prettiest.", "Maya", "Angel", "Brick", 3],
        ["What weapon manufacturer has you throw your gun upon reloading?", "Jakobs", "Tediore", "Maliwan", 2],
        ["What weapon manufacturer is known for having high rates of fire?", "Dahl", "Torgue", "Vladof", 3],
        ["Who gives you the Fibber mission reward?", "Mel", "Mal", "Mil", 2],
        ["How much eridium does it cost to open the door to Terramorphous's Lair?", "4", "5", "8", 3],
        ["The ______ on Digistruct Peak", "Assault", "War", "Raid", 3],
        ["Which one of these are not a weapon element in Borderlands 2?", "Fire", "Cryo", "Shock", 2],
        ["What element does Captain Flynt resist?", "Shock", "Slag", "Fire", 3],
        ["Jakobs manufacturer makes all weapon types except-", "Snipers", "SMGs", "Shotguns", 2],
        ["What gemstone type are Dahl weapons in Tina DLC?", "Citrine", "Aquamarine", "Emerald", 3],
        ["Anshin manufactures everything except-", "Grenades", "Shields", "Class Mods", 1],
        ["What is Krieg's middle tree capstone skill called?", "Release the Demon", "Release the Beast", "Release the Babies", 2],
        ["Axton's Metal Storm skill gives him bonus fire rate and-", "Damage Reduction", "Reload Speed", "Recoil Reduction", 3],
        ["Gaige's companion is called-", "Sabre Turret", "Noob Saibot", "Deathtrap", 3],
        ["Which candy gives you bonus movement speed in the Bloody Harvest Headhunter DLC?", "Blue Candy", "Green Candy", "Yellow Candy", 3],
        ["What is the frozen town called in the Mercenary Day Headhunter DLC?", "Snowy Peak", "Gingerton", "Frozen Valley", 2],
        ["What is the name of the pastor in the Wedding Day Massacre Headhunter DLC?", "Sigmand", "Innuendobot 5000", "Ed", 2],
        ["Who drops the Thunderball Fist in the Son of Crawmerax Headhunter DLC?", "Captain Flynt", "Sparky Flynt", "Zane Flynt", 2],
        ["What is the name of Mordecai's newest pet?", "Bloodwing", "Talon", "Pidgey", 2],
        ["The Invincible Son of ________ the Invincible", "Flynt", "Crawmerax", "Mothrakk", 2],
        ["How many different playthrough modes are in Borderlands 2?", "2", "3", "4", 2],
        ["Who has the Rolling Thunder as a dedicated drop?", "Boom Bewm", "Motor Mama", "Wilhelm", 3],
        ["Who has the Big Boom Blaster as a dedicated drop?", "Ancient Dragons of Destruction", "Master Gee the Invincible", "Pyro Pete the Invincible", 3],
        ["Which one of these non-unique weapons are not manufactured by Vladof?", "Muckamuck", "Anarchist", "Droog", 1],
        ["Which manufacturer makes the PBFG rocket launcher?", "Maliwan", "Torgue", "Vladof", 1],
        ["Who has the Mongol as a dedicated drop?", "Dukino's Mom", "Black Queen", "King Mong", 1],
        ["The legendary Infinity pistol cannot roll which element?", "Fire", "Slag", "Corrosive", 2],
        ["Which unique enemy does not spawn at The Fridge?", "Knuckledragger", "Laney White", "Rakkman", 1],
        ["Wildlife ___________ Preserve", "Exploration", "Exploitation", "Emulsification", 2],
        ["Where does Angel die?", "Eridium Blights", "Control Core", "Vault of the Warrior", 2],
        ["What shields are known for giving elemental resistance?", "Roid Shields", "Adaptive Shields", "Nova Shields", 2],
        ["How many loaders need to be wounded during the story to open the door at the start of the Wildlife Preserve?", "3", "4", "5", 1],
        ["Who are we on a rescue mission for at the Wildlife Preserve?", "Mordecai", "Bloodwing", "Brick", 2],
        ["Brick the ___ King", "Punch", "Slab", "Prettiest", 2],
        ["How many mortar beacons are destroyed during the Once in Future Slab story mission?", "3", "4", "5", 1],
        ["Which one of these are not a loader type?", "WAR Loader", "LWT Loader", "FUN Loader", 3],
        ["How many voice samples are collected during the story mission The Man Who Would Be Jack?", "3", "4", "5", 2],
        ["How many Auto Cannons do you destroy right before the Bunker boss fight?", "8", "10", "11", 3],
        ["How many guns can Salvador equip?", "2", "3", "4", 3],
        ["What is Zer0's action skill called?", "Fade Away", "Deception", "Into the Shadows", 2],
        ["What is the password used to open the door to Control Core?", "Open Sesame", "I Love You", "Abracadabra", 2],
        ["Who doesn't have the legendary Bee shield as a dedicated drop?", "Hunter Hellquist", "Gold Golem", "Treants", 2],
        ["Which one of these enemies can be a rabid variant?", "Spiderant", "Stalker", "Rakk", 2],
        ["How many Ambush Commanders do you need to kill during the story mission at Sawtooth Cauldron?", "4", "5", "6", 1],
        ["How many spawn locations does King Mong have?", "2", "3", "4", 1],
        ["Face McShooty wants you to shoot him in the-", "Face", "Arm", "Leg", 1],
        ["What grenade manufacturer doesn't make a MIRV variant?", "Tediore", "Bandit", "Torgue", 1],
        ["Proficiency relics provide you with bonus-", "Melee Damage", "Cooldown", "Shield Capacity", 2],
        ["How many different pearlescents are there in Borderlands 2?", "8", "12", "16", 2],
        ["Axton as the ________", "Commando", "Soldier", "Sentry", 1],
        ["Which element is best for damaging enemy shields?", "Shock", "Fire", "Corrosive", 1],
        ["Which element is best for damaging enemy armor?", "Corrosive", "Explosive", "Shock", 1],
        ["\"It's our new torture doll boys. Let's turn up the ____!\"", "PAIN", "HEAT", "BASS", 2],
        ["Which weapon can Moxxi not give you from tipping her in Borderlands 2?", "Hail", "Good Touch", "Bad Touch", 1],
        ["What is the rare loot drop percentage on the Vault Hunter Relic?", "5%", "7%", "10%", 1],
        ["Who drops the Yellowjacket as a dedicated drop?", "Jackenstein", "Hunter Hellquist", "Scorch", 1],
        ["Who drops the Rough Rider as a dedicated drop?", "Bulwark", "Bulstoss", "Arizona", 1],
        ["Who drops the Antifection as a dedicated drop?", "Mortar", "Cassius", "Uranus", 2],
        ["What is the drop chance for a Bonus Package from Boom Bewm?", "5%", "10%", "15%", 2],
        ["What item cannot be found in a Torgue vendor?", "Nukem", "Rolling Thunder", "Meteor Shower", 3],
        ["Which relic increases pistol fire rate?", "Deputy Badge", "Hard Carry", "Sheriff's Badge", 3],
    ]

    #                               -z    -z    -z    -z    -z    -z     +y    -z    -z    -z
    doorEndPositions: List[int] = [7216, 7076, 8059, 6966, 6889, 6029, 35813, 5207, 3881, 3510]

    inTrivia: bool = False
    currentTriviaQuestion: int = 0
    triviaStreak: int = 1
    canShowQuestion: bool = True
    gaveLoot: bool = False
    isHardMode: bool = True
    usedQuestions: List[int] = []

    def move_doors() -> None:
        doornum = QuestionLib.triviaStreak
        door = placeablehelper.TAGGED_OBJECTS[f"Door {str(doornum)}"][0].uobj
        done = False
        if doornum == 7:
            while not done:
                doorpos = placeablehelper.static_mesh.get_location(door)
                if doorpos[1] < QuestionLib.doorEndPositions[doornum - 1]:
                    newdoorpos: Tuple = (doorpos[0], doorpos[1] + 3, doorpos[2])
                    placeablehelper.static_mesh.set_location(door, newdoorpos)
                else:
                    done = True
                time.sleep(0.01)
        else:
            while not done:
                doorpos = placeablehelper.static_mesh.get_location(door)
                if doorpos[2] > QuestionLib.doorEndPositions[doornum - 1]:
                    newdoorpos: Tuple = (doorpos[0], doorpos[1], doorpos[2] - 3)
                    placeablehelper.static_mesh.set_location(door, newdoorpos)
                else:
                    done = True
                time.sleep(0.01)

    def check_plates() -> None:
        currentplatepos = placeablehelper.static_mesh.get_location(placeablehelper.TAGGED_OBJECTS[f"Plate {QuestionLib.triviaStreak}"][0].uobj)
        if distance(get_player_location(), currentplatepos) < 150 and QuestionLib.canShowQuestion == True:
            QuestionLib.canShowQuestion = False
            QuestionLib.show_trivia_question()

    def complete_run() -> None:
        menu: uFeed.OptionBox = uFeed.OptionBox(
            Title="Question:",
            Caption="You found Buttstallion! She rushes at you in a full force rage. How do you choose to dodge?",
            PreventCanceling = True,
            Buttons=[
                uFeed.OptionBoxButton(Name="Strafe to the left", Tip=""),
                uFeed.OptionBoxButton(Name="Do a sick backflip", Tip=""),
                uFeed.OptionBoxButton(Name="Shield yourself for impact", Tip=""),
            ],
        )
        menu.OnPress = lambda button: {
            "Strafe to the left": QuestionLib.kill_player,
            "Do a sick backflip": QuestionLib.kill_player,
            "Shield yourself for impact": QuestionLib.kill_player,
        }.get(button.Name, lambda _: None)()
        menu.Show()

    def set_hard() -> None:
        QuestionLib.isHardMode = True

    def set_easy() -> None:
        QuestionLib.isHardMode = False

    def start_run() -> None:
        menu: uFeed.OptionBox = uFeed.OptionBox(
            Title="Tiny Tina Says:",
            Caption="Hey Vaulty Vault!\nButtstallion is in a moooood. I maaaybe tried to feed her chocolate chip cookies and forgot she only consumes precious gems.\nCan you find her for me? Pleeeease! Please please please! She ran off around these parts. The locals call this place the Murderous Mesa. It sounds lovely.\nGOOD LUCK SUCKA!!\n\nNow, pick a difficulty:",
            PreventCanceling = True,
            Buttons=[
                uFeed.OptionBoxButton(Name="Easy", Tip=""),
                uFeed.OptionBoxButton(Name="Hard", Tip=""),
            ],
        )
        menu.OnPress = lambda button: {
            "Easy": QuestionLib.set_easy,
            "Hard": QuestionLib.set_hard,
        }.get(button.Name, lambda _: None)()
        menu.Show()

    def load_trivia_map() -> None:
        loaded_map: str = unrealsdk.GetEngine().GetCurrentWorldInfo().GetStreamingPersistentMapName().lower()
        map_file_path: Path = Path(__file__).parent.resolve() / "Borderlands Trivia.json"
        if loaded_map == "testingzone_p":
            if map_file_path.is_file():
                with open(map_file_path) as mapfile:
                    maptoload = json.load(mapfile)
                    loadplease = maptoload.get(
                        loaded_map,
                        None,
                    )
                unrealsdk.FindObject("InteractiveObjectDefinition", "GD_Balance_Shopping.VendingMachines.InteractiveObj_VendingMachine_GrenadesAndAmmo").CompassIcon = 0
                placeablehelper.load_map(loadplease)
                QuestionLib.inTrivia = True
            else:
                unrealsdk.Log(str(map_file_path) + " Doesnt Exist")

    def kill_player() -> None:
        QuestionLib.inTrivia = False
        unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn.Location = (6949.154296875, 5518.8662109375, 5690.0478515625)
        unrealsdk.GetEngine().GamePlayers[0].Actor.GetWillowPlayerPawn().CausePlayerDeath(True)
        QuestionLib.triviaStreak = 1
        QuestionLib.gaveLoot = False
        QuestionLib.canShowQuestion = True
        unrealsdk.FindObject("InteractiveObjectDefinition", "GD_Balance_Shopping.VendingMachines.InteractiveObj_VendingMachine_GrenadesAndAmmo").CompassIcon = 4
        placeablehelper.unload_map()

    def check_trivia_answer(selectedanswer) -> None:
        if QuestionLib.isHardMode == True:
            if selectedanswer != QuestionLib.HARD_TRIVIA_QUESTIONS[QuestionLib.currentTriviaQuestion][4]:
                QuestionLib.kill_player()
                uFeed.ShowHUDMessage(
                    Title="Borderlands Trivia:",
                    Message="Incorrect",
                    Duration=3,
                    MenuHint=0,
                )
            else:
                threading.Thread(target=QuestionLib.move_doors).start()
                QuestionLib.triviaStreak += 1
                QuestionLib.canShowQuestion = True
                uFeed.ShowHUDMessage(
                    Title="Borderlands Trivia:",
                    Message="Correct!",
                    Duration=3,
                    MenuHint=0,
                )
                if QuestionLib.triviaStreak == 11 and QuestionLib.gaveLoot == False:
                    QuestionLib.gaveLoot = True
                    sbsl_obj = unrealsdk.ConstructObject("Behavior_SpawnLootAroundPoint")
                    sbsl_obj.ItemPools = [unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_06_Legendary"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_06_Legendary"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_06_Legendary")]
                    sbsl_obj.SpawnVelocityRelativeTo = 0
                    sbsl_obj.bTorque = False
                    sbsl_obj.CircularScatterRadius = 100
                    sbsl_obj.CustomLocation = ((27118, 35004, 4250), None, "")
                    sbsl_obj.ApplyBehaviorToContext(unrealsdk.GetEngine().GamePlayers[0].Actor, (), None, None, None, ())
        else:
            if selectedanswer != QuestionLib.EASY_TRIVIA_QUESTIONS[QuestionLib.currentTriviaQuestion][4]:
                QuestionLib.kill_player()
                uFeed.ShowHUDMessage(
                    Title="Borderlands Trivia:",
                    Message="Incorrect",
                    Duration=3,
                    MenuHint=0,
                )
            else:
                threading.Thread(target=QuestionLib.move_doors).start()
                QuestionLib.triviaStreak += 1
                QuestionLib.canShowQuestion = True
                uFeed.ShowHUDMessage(
                    Title="Borderlands Trivia:",
                    Message="Correct!",
                    Duration=3,
                    MenuHint=0,
                )
                if QuestionLib.triviaStreak == 11 and QuestionLib.gaveLoot == False:
                    QuestionLib.gaveLoot = True
                    sbsl_obj = unrealsdk.ConstructObject("Behavior_SpawnLootAroundPoint")
                    sbsl_obj.ItemPools = [unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_05_VeryRare"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_05_VeryRare"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_05_VeryRare")]
                    sbsl_obj.SpawnVelocityRelativeTo = 0
                    sbsl_obj.bTorque = False
                    sbsl_obj.CircularScatterRadius = 100
                    sbsl_obj.CustomLocation = ((27118, 35004, 4250), None, "")
                    sbsl_obj.ApplyBehaviorToContext(unrealsdk.GetEngine().GamePlayers[0].Actor, (), None, None, None, ())

    def trivia_answer_1() -> None:
        QuestionLib.check_trivia_answer(1)

    def trivia_answer_2() -> None:
        QuestionLib.check_trivia_answer(2)

    def trivia_answer_3() -> None:
        QuestionLib.check_trivia_answer(3)

    def show_trivia_question() -> None:
        if QuestionLib.isHardMode == True:
            while True:
                QuestionLib.currentTriviaQuestion = randint(0, len(QuestionLib.HARD_TRIVIA_QUESTIONS) - 1)
                if QuestionLib.currentTriviaQuestion not in QuestionLib.usedQuestions:
                    QuestionLib.usedQuestions.append(QuestionLib.currentTriviaQuestion)
                    break
            menu: uFeed.OptionBox = uFeed.OptionBox(
                Title="Question:",
                Caption=QuestionLib.HARD_TRIVIA_QUESTIONS[QuestionLib.currentTriviaQuestion][0],
                PreventCanceling = True,
                Buttons=[
                    uFeed.OptionBoxButton(Name=QuestionLib.HARD_TRIVIA_QUESTIONS[QuestionLib.currentTriviaQuestion][1], Tip=""),
                    uFeed.OptionBoxButton(Name=QuestionLib.HARD_TRIVIA_QUESTIONS[QuestionLib.currentTriviaQuestion][2], Tip=""),
                    uFeed.OptionBoxButton(Name=QuestionLib.HARD_TRIVIA_QUESTIONS[QuestionLib.currentTriviaQuestion][3], Tip=""),
                ],
            )
            menu.OnPress = lambda button: {
                QuestionLib.HARD_TRIVIA_QUESTIONS[QuestionLib.currentTriviaQuestion][1]: QuestionLib.trivia_answer_1,
                QuestionLib.HARD_TRIVIA_QUESTIONS[QuestionLib.currentTriviaQuestion][2]: QuestionLib.trivia_answer_2,
                QuestionLib.HARD_TRIVIA_QUESTIONS[QuestionLib.currentTriviaQuestion][3]: QuestionLib.trivia_answer_3,
            }.get(button.Name, lambda _: None)()
            menu.Show()
        else:
            while True:
                QuestionLib.currentTriviaQuestion = randint(0, len(QuestionLib.HARD_TRIVIA_QUESTIONS) - 1)
                if QuestionLib.currentTriviaQuestion not in QuestionLib.usedQuestions:
                    QuestionLib.usedQuestions.append(QuestionLib.currentTriviaQuestion)
                    break
            menu: uFeed.OptionBox = uFeed.OptionBox(
                Title="Question:",
                Caption=QuestionLib.EASY_TRIVIA_QUESTIONS[QuestionLib.currentTriviaQuestion][0],
                PreventCanceling = True,
                Buttons=[
                    uFeed.OptionBoxButton(Name=QuestionLib.EASY_TRIVIA_QUESTIONS[QuestionLib.currentTriviaQuestion][1], Tip=""),
                    uFeed.OptionBoxButton(Name=QuestionLib.EASY_TRIVIA_QUESTIONS[QuestionLib.currentTriviaQuestion][2], Tip=""),
                    uFeed.OptionBoxButton(Name=QuestionLib.EASY_TRIVIA_QUESTIONS[QuestionLib.currentTriviaQuestion][3], Tip=""),
                ],
            )
            menu.OnPress = lambda button: {
                QuestionLib.EASY_TRIVIA_QUESTIONS[QuestionLib.currentTriviaQuestion][1]: QuestionLib.trivia_answer_1,
                QuestionLib.EASY_TRIVIA_QUESTIONS[QuestionLib.currentTriviaQuestion][2]: QuestionLib.trivia_answer_2,
                QuestionLib.EASY_TRIVIA_QUESTIONS[QuestionLib.currentTriviaQuestion][3]: QuestionLib.trivia_answer_3,
            }.get(button.Name, lambda _: None)()
            menu.Show()
        