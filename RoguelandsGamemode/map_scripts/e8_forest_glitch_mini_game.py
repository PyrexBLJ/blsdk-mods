import random
import time
from typing import Tuple

import unrealsdk  # type: ignore

from Mods.MapLoader import placeablehelper

from ..game_state import GameState


def glitch_room() -> None:
    glitch1: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["Glitch Effect 1"][0].uobj
    glitch2: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["Glitch Effect 2"][0].uobj
    glitch3: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["Glitch Effect 3"][0].uobj

    while not GameState.mission_complete:
        newrot: Tuple[float, float, float] = (
            random.randint(-65535, 65535),
            random.randint(-65535, 65535),
            random.randint(-65535, 65535),
        )
        placeablehelper.static_mesh.set_rotation(glitch1, newrot)
        time.sleep(random.randint(1, 100) / 100)
        newrot: Tuple[float, float, float] = (
            random.randint(-65535, 65535),
            random.randint(-65535, 65535),
            random.randint(-65535, 65535),
        )
        placeablehelper.static_mesh.set_rotation(glitch2, newrot)
        time.sleep(random.randint(1, 100) / 100)
        newrot: Tuple[float, float, float] = (
            random.randint(-65535, 65535),
            random.randint(-65535, 65535),
            random.randint(-65535, 65535),
        )
        placeablehelper.static_mesh.set_rotation(glitch3, newrot)
        time.sleep(random.randint(1, 100) / 100)
