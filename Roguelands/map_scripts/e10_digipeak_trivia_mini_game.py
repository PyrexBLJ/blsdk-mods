import random
from typing import List, Tuple

import Mods.UserFeedback as uFeed
from Mods.MapLoader import placeablehelper

from .. import maps, util

TRIVIA_QUESTIONS: List[list] = [
    ["Who is the main antagonist in Borderlands 2?", "Ransom Slack", "Handsome Jack", "Phantom Rack", 2],
    ["What element is most effective on armor?", "Fire", "Shock", "Corrosive", 3],
    ["Which one of these enemies cannot be a tubby?", "Tubby Skag", "Tubby Bullymong", "Tubby Stalker", 2],
    ["What legendary can Wilhelm drop?", "Cradle", "Bonus Package", "Logan's Gun", 3],
    ["Who drops the Gub?", "Zaney Wipe", "Laney White", "Janey Might", 2],
    ["Where is Mad Mike located?", "Bloodshot Stronghold", "Lynchwood", "Eridium Blights", 1],
    ["Where is Mad Dog located?", "Bloodshot Stronghold", "Lynchwood", "Eridium Blights", 2],
    ["What is the highest percent roll you can get on the legendary Sham shield?", "92%", "94%", "96%", 2],
    ["Which food did Handsome Jack think sucks on your visit to Southern Shelf?", "Pretzels", "Pizza", "Pineapple", 1],
    ["Where did Face McShooty want you to shoot him?", "In the foot", "In the arm", "In the face", 3],
    ["How many playable characters are in Borderlands 2?", "4", "6", "8", 2],
    ["Where is the double rainbow easter egg located?", "The Highlands", "Wildlife Preserve", "Thousand Cuts", 1],
    ["What does Claptrap commonly refer to you as?", "Vault Hunter", "Friend", "Minion", 3],
    ["What blue unique does Big Sleep drop?", "12 Pounder", "Roaster", "Morningstar", 1],
    [
        "What element did Handsome Jack almost forget about during your fight with Bloodwing?",
        "Corrosion",
        "Slag",
        "Explosive",
        3,
    ],
    ["How many pistol manufacturers are there in Borderlands 2?", "4", "6", "8", 3],
    ["Crazy Earl is crazy about what object?", "Eridium", "Rainbow Crystals", "Diamond Tokens", 1],
    ["Who is the cute skag that resides at Lynchwood?", "Scrappy", "Mr. Chew", "Dukino", 3],
    [
        "Who cannot drop the legendary Norfleet rocket launcher?",
        "Vermivorous the Invincible",
        "Hyperius the Invincible",
        "Master Gee the Invincible",
        3,
    ],
    ["What weapon can Moxxi give you for tipping her?", "Heartbreaker", "Good Touch", "Rubi", 2],
]


class State:
    current_trivia_question: int = 0


def trivia_questions(this_map: maps.MapData) -> None:
    plates = placeablehelper.TAGGED_OBJECTS.get("Trivia Plate 1", None)
    ploc = util.get_player_location()
    if plates is not None:
        if (
            util.distance(
                ploc,
                placeablehelper.static_mesh.get_location(placeablehelper.TAGGED_OBJECTS["Trivia Plate 1"][0].uobj),
            )
            < 150
            and not this_map.custom_map_data[1]
        ):
            this_map.custom_map_data[1] = True
            show_trivia_question(this_map)
        if (
            util.distance(
                ploc,
                placeablehelper.static_mesh.get_location(placeablehelper.TAGGED_OBJECTS["Trivia Plate 2"][0].uobj),
            )
            < 150
            and not this_map.custom_map_data[2]
        ):
            this_map.custom_map_data[2] = True
            show_trivia_question(this_map)
        if (
            util.distance(
                ploc,
                placeablehelper.static_mesh.get_location(placeablehelper.TAGGED_OBJECTS["Trivia Plate 3"][0].uobj),
            )
            < 150
            and not this_map.custom_map_data[3]
        ):
            this_map.custom_map_data[3] = True
            show_trivia_question(this_map)
        if (
            this_map.custom_map_data[1]
            and this_map.custom_map_data[2]
            and this_map.custom_map_data[3]
            and not this_map.custom_map_data[4]
        ):
            this_map.custom_map_data[4] = True
            bridgeloc = placeablehelper.static_mesh.get_location(placeablehelper.TAGGED_OBJECTS["Bridge 1"][0].uobj)
            newbridgeloc: Tuple[float, float, float] = (bridgeloc[0], bridgeloc[1], bridgeloc[2] + 10000)
            placeablehelper.static_mesh.set_location(
                placeablehelper.TAGGED_OBJECTS["Bridge 1"][0].uobj,
                newbridgeloc,
            )


def check_trivia_answer(this_map: maps.MapData) -> None:
    if this_map.custom_map_data[6] != TRIVIA_QUESTIONS[State.current_trivia_question][4]:
        this_map.custom_map_data[5] = True
        # self.countdown_timer = 0
        uFeed.ShowHUDMessage(
            Title="Trivia:",
            Message="Incorrect",
            Duration=3,
            MenuHint=0,
        )
    else:
        uFeed.ShowHUDMessage(
            Title="Trivia:",
            Message="Correct!",
            Duration=3,
            MenuHint=0,
        )


def trivia_answer_1(this_map: maps.MapData) -> None:
    this_map.custom_map_data[6] = 1
    check_trivia_answer(this_map)


def trivia_answer_2(this_map: maps.MapData) -> None:
    this_map.custom_map_data[6] = 2
    check_trivia_answer(this_map)


def trivia_answer_3(this_map: maps.MapData) -> None:
    this_map.custom_map_data[6] = 3
    check_trivia_answer(this_map)


def show_trivia_question(this_map: maps.MapData) -> None:
    State.current_trivia_question = random.randint(0, len(TRIVIA_QUESTIONS) - 1)
    menu: uFeed.OptionBox = uFeed.OptionBox(
        Title="Question:",
        Caption=TRIVIA_QUESTIONS[State.current_trivia_question][0],
        Buttons=[
            uFeed.OptionBoxButton(Name=TRIVIA_QUESTIONS[State.current_trivia_question][1], Tip=""),
            uFeed.OptionBoxButton(Name=TRIVIA_QUESTIONS[State.current_trivia_question][2], Tip=""),
            uFeed.OptionBoxButton(Name=TRIVIA_QUESTIONS[State.current_trivia_question][3], Tip=""),
        ],
    )
    menu.OnPress = lambda button: {
        TRIVIA_QUESTIONS[State.current_trivia_question][1]: trivia_answer_1,
        TRIVIA_QUESTIONS[State.current_trivia_question][2]: trivia_answer_2,
        TRIVIA_QUESTIONS[State.current_trivia_question][3]: trivia_answer_3,
    }.get(button.Name, lambda _: None)(this_map)
    menu.Show()
