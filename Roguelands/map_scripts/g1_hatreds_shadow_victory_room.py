import time
from typing import Tuple

import unrealsdk  # type: ignore

from Mods.MapLoader import placeablehelper

from ..game_state import GameState


def finish_cubes() -> None:
    cube1: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["Animated Cube 1"][0].uobj
    cube2: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["Animated Cube 2"][0].uobj
    cube1bool: bool = True
    cube2bool: bool = True

    i: int = 0
    k: int = 0
    while not GameState.mission_complete:
        if cube1bool:
            floorpos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(cube2)
            newpos: Tuple[float, float, float] = (floorpos[0] + 0.5, floorpos[1], floorpos[2])
            placeablehelper.static_mesh.set_location(cube2, newpos)
            if floorpos[0] >= 34532.83203125:
                cube1bool = False
        else:
            floorpos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(cube2)
            newpos: Tuple[float, float, float] = (floorpos[0] - 0.5, floorpos[1], floorpos[2])
            placeablehelper.static_mesh.set_location(cube2, newpos)
            if floorpos[0] <= 32082.310546875:
                cube1bool = True

        if not cube2bool:
            floorpos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(cube1)
            newpos: Tuple[float, float, float] = (floorpos[0], floorpos[1] + 0.5, floorpos[2])
            placeablehelper.static_mesh.set_location(cube1, newpos)
            if floorpos[1] >= 35552.38671875:
                cube2bool = True
        else:
            floorpos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(cube1)
            newpos: Tuple[float, float, float] = (floorpos[0], floorpos[1] - 0.5, floorpos[2])
            placeablehelper.static_mesh.set_location(cube1, newpos)
            if floorpos[1] <= 33074.94140625:
                cube2bool = False

        i += 15
        if i > 65535:
            i = -65535
        newrot: Tuple[float, float, float] = (i, i, i)
        placeablehelper.static_mesh.set_rotation(cube1, newrot)
        k -= 10
        if k > 65535:
            k = -65535
        newrot2: Tuple[float, float, float] = (k, k, k)
        placeablehelper.static_mesh.set_rotation(cube2, newrot2)

        time.sleep(0.0000001)
