from typing import List
from random import randint
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

class QuoteLib:

    STORY_QUOTES: List[str] = [
        "That shiny pony was relentless!",
        "Beware of the shining one!",
        "Turn back before it's too late!",
        "DO NOT PET THE HORSE!",
        "Tina said this would be easy.",
        "It was a mistake coming here!",
        "Why did I agree to help with this?",
        "Who's bright idea was it to come here?",
        "I hate it here!",
        "I think something is following me.",
        "I think I saw something on the cliffsides looking at me.",
        "I fear that we are not alone!",
        "Something is watching!",
        "An evil presence is near!",
        "I think we're in grave danger!.",
        "I swear I saw shadows in the caves.",
        "I felt something breathe down my neck! It sent a chill down my spine!",
        "Ouch! Something bit me!",
        "It's so hot here… I'm so getting sunburn.",
        "Don't tell anyone, but sometimes I like to lay on my roof and pretend I'm a hamster.",
        "Bark! Bark! I'm a fish.",
        "One time, I balanced a whole stack of pancakes on my head.",
        "This place is driving me crazy!",
        "If I get thrown back to the start one more time…",
        "Some of these trivia questions are so stupid.",
        "Tina is an interesting person.",
        "Tina threatened to blow me up if I didn't help.",
        "I've been stuck here for days!",
        "I'm seeing a lot of dead people here. This is concerning.",
        "A pony made of diamonds? I'm gonna be rich!",
        "A pony made of diamonds? I somehow doubt that.",
        "Aww! Look at the diamond pony… AAAAH SHE BITES!!",
        "9 out of 10 voices in my head tell me I'm crazy. The tenth is just humming. ",
        "6:30 is the best time on a clock, hands down.",
        "Don't worry if plan A fails. There are 25 more letters in the alphabet!",
        "Earth is like the insane asylum for the universe.",
        "I don't suffer from insanity! I enjoy every minute of it.",
        "Always remember that you're unique...just like everyone else is.",
        "I sold my vacuum cleaner because all it was doing was gathering dust.",
        "Whiteboards really are remarkable.",
        "If history repeats itself, I'm getting a pet dinosaur.",
        "I'm out of my mind. I'll be back in five minutes.",
        "I tried to be normal once… worst two minutes of my entire life.",
        "Pobody's nerfect!",
        "I try to have an open mind, but my brain keeps falling out.",
        "It's official! I'm in love with POPTARTS!",
        "I prefer Coke over Pepsi.",
        "Sometimes your kitchen sink makes me really angry!",
        "After Tuesday, even the calendar says WTF.",
        "Why aren't shorts half the price of pants?",
    ]

    COMMUNITY_NAMES: List[str] = [
        "Pyrex",
        "JoltzDude139", 
        "Ki11erSix",
        "Juso",
        "Flare2V",
        "Moxsy",
        "Mopioid",
        "Exotek",
        "LilGasmask666",
        "WholyMilk",
        "bisnap",
        "EpicNNG",
        "ShadowEvil",
        "BadKarma",
        "PilotPlaysGames",
        "Termx",
        "Deceptix_",
        "Darksmoke11",
        "GageHC",
        "Kai_TW",
        "LazyData",
        "Bgm_",
        "Cashew1405",
        "Miqueagal",
        "EruptionFang",
        "MaskedVillainGaming",
        "CptnFooFoo",
        "TweetyExpert",
        "Gunther",
        "Utsuwu",
        "kXrtoshka",
        "UnjustAction",
        "zeubiess",
        "Chadly99",
        "Byrdman778",
        "SchviftyFive",
        "Mitsu",
        "Tessachka",
        "amyrlinn",
        "Spunky117",
        "Shockwve",
        "D2H",
        "UnbrokenFist",
        "EpicDan22",
        "MystiqueSiren",
        "ZubsterTV",
        "paskaroni",
        "SpeakingLion",
        "MoonBaseTom",
        "JewFye",
        "v0cal_Assassin",
        "ES3TH",
        "donanzador911",
        "playdohkid69",
        "Jambi_TS",
        "bzk25",
        "ADudeNamedArc",
        "Garrit",
        "iStockingKit",
        "NoName",
        "Bikkelz",
        "Darkdemon8910",
        "Flamer",
        "M4sterFun",
        "shinloki555",
        "KnoticalMenace",
        "WeirdScienceX",
        "rriot",
        "apple1417",
        "ZetaDaemon",
        "Dr. Bones",
        "Sparrow",
        "gamechanger97",
    ]

    ENEMY_TYPES: List[str] = [
        "Psycho",
        "Goliath",
        "Nomad",
        "Engineer",
        "Berserker",
        "Commando",
        "Siren",
        "Assassin",
        "Lunatic",
        "Tink",
        "Enforcer",
        "Maniac",
        "Outlaw",
        "Trooper",
        "Bruiser",
        "Archer",
        "Pirate",
        "Savage",
        "Witch Doctor",
        "Commander",
        "Goober",
        "Darksider",
        "Defiler",
        "Major",
        "Fanatic",
        "Lawbringer",
        "Scrap-Trap",
        "Gladiator",
        "Fiend",
        "Looter",
        "Gunner",
        "Skullsplitter",
        "Hawk",
        "Infiltrator",
        "Sniper",
        "Soldier",
        "Body Double",
        "Jawbreaker",
        "Fleshripper",
        "Scout",
        "Medic",
        "Marine",
        "Fighter",
        "Smasher",
        "Shotgunner",
        "Blaster",
        "Rocketeer",
        "Pyro",
        "Infantry",
        "Defender",
        "Slicer",
        "Torturer",
        "Officer",
        "Thief",
        "Raider",
        "Knuckleduster",
        "Head Hunter",
        "Hunter",
        "Rioter",
        "Warrior",
        "Scavenger",
        "Rustler",
        "Warden",
        "Stabber",
        "Mobster",
        "Operative",
        "Beastmaster",
        "Doppelganger",
    ]

    canShowQuote: bool = True
    quoteTriggered: int = 0
    triggeredQuotes: List[int] = []
    usedQuotes: List[int] = []
    usedNames: List[int] = []
    usedTypes: List[int] = []

    def build_story() -> str:
        quote: int = 0
        name: int = 0
        etype: int = 0
        while True:
            quote = randint(0, len(QuoteLib.STORY_QUOTES)-1)
            if quote not in QuoteLib.usedQuotes:
                QuoteLib.usedQuotes.append(quote)
                break
        while True:
            name = randint(0, len(QuoteLib.COMMUNITY_NAMES)-1)
            if name not in QuoteLib.usedNames:
                QuoteLib.usedNames.append(name)
                break
        while True:
            etype = randint(0, len(QuoteLib.ENEMY_TYPES)-1)
            if etype not in QuoteLib.usedTypes:
                QuoteLib.usedTypes.append(etype)
                break
        return f"{QuoteLib.STORY_QUOTES[quote]}\n-{QuoteLib.COMMUNITY_NAMES[name]} the {QuoteLib.ENEMY_TYPES[etype]}"

    def check_echos() -> bool:
        if QuoteLib.canShowQuote == False:
            if distance(get_player_location(), placeablehelper.static_mesh.get_location(placeablehelper.TAGGED_OBJECTS[f"Story {str(QuoteLib.quoteTriggered)}"][0].uobj)) > 350:
                QuoteLib.canShowQuote = True
        for echo in range(1, 11):
            if distance(get_player_location(), placeablehelper.static_mesh.get_location(placeablehelper.TAGGED_OBJECTS[f"Story {str(echo)}"][0].uobj)) < 150 and QuoteLib.canShowQuote and echo not in QuoteLib.triggeredQuotes:
                QuoteLib.triggeredQuotes.append(echo)
                QuoteLib.quoteTriggered = echo
                QuoteLib.canShowQuote = False
                uFeed.ShowHUDMessage(
                    Title="ECHO Recorder Reads:",
                    Message=QuoteLib.build_story(),
                    Duration=8,
                    MenuHint=0,
                )
        return True