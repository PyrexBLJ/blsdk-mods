import time
from typing import Tuple

import unrealsdk  # type: ignore

from Mods.MapLoader import placeablehelper

from ..game_state import GameState


def move_boat() -> None:
    done: bool = False
    boat: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["EE Boat"][0].uobj
    buttstallion: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["EE Buttstallion"][0].uobj
    boatstartpos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(boat)
    buttstallonstartpos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(buttstallion)
    boattop: Tuple[float, float, float] = (boatstartpos[0], boatstartpos[1], boatstartpos[2] + 1803)
    buttstalliontop: Tuple[float, float, float] = (
        buttstallonstartpos[0],
        buttstallonstartpos[1],
        buttstallonstartpos[2] + 1803,
    )
    placeablehelper.static_mesh.set_location(boat, boattop)
    placeablehelper.static_mesh.set_location(buttstallion, buttstalliontop)
    while not done:
        if GameState.travel_timer == 1:
            done = True
        boatpos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(boat)
        buttstallonpos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(buttstallion)
        if boatpos[0] > 11326:
            newboatpos: Tuple[float, float, float] = (boatpos[0] - 10, boatpos[1], boatpos[2])
            newbuttstallionpos: Tuple[float, float, float] = (
                buttstallonpos[0] - 10,
                buttstallonpos[1],
                buttstallonpos[2],
            )
            placeablehelper.static_mesh.set_location(boat, newboatpos)
            placeablehelper.static_mesh.set_location(buttstallion, newbuttstallionpos)
            time.sleep(0.01)
        else:
            done = True
    boatbottom: Tuple[float, float, float] = (boatstartpos[0], boatstartpos[1], boatstartpos[2])
    buttstallionbottom: Tuple[float, float, float] = (
        buttstallonstartpos[0],
        buttstallonstartpos[1],
        buttstallonstartpos[2],
    )
    placeablehelper.static_mesh.set_location(boat, boatbottom)
    placeablehelper.static_mesh.set_location(buttstallion, buttstallionbottom)
