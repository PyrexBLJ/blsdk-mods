import time
from typing import Tuple
import threading

import unrealsdk  # type: ignore

import Mods.UserFeedback as uFeed
from Mods.MapLoader import placeablehelper

from ..game_state import GameState
from .. import util

def sg_door() -> None:
    door: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["Door"][0].uobj
    done: bool = False
    while not done:
        doorrot: Tuple[int, int, int] = placeablehelper.static_mesh.get_rotation(door)
        if doorrot[1] >= 0:
            newpos: Tuple[int, int, int] = (doorrot[0], doorrot[1] - 100, doorrot[2])
            placeablehelper.static_mesh.set_rotation(door, newpos)
        else:
            done = True
        time.sleep(0.01)

def check_lever() -> None:
    lever: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["Door Lever"][0].uobj
    if util.distance(util.get_player_location(), placeablehelper.interactive_objects.get_location(lever)) <= 700 and GameState.current_map.custom_map_data[1] == False:
        GameState.current_map.custom_map_data[1] = True
        threading.Thread(target=sg_door).start()
        uFeed.ShowHUDMessage(
                Title="",
                Message="A door has been opened.",
                Duration=5,
                MenuHint=0,
            )