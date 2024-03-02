import time
from typing import List, Tuple

import unrealsdk  # type: ignore

from Mods.MapLoader import placeablehelper

from ..game_state import GameState


def move_floors_for_floors_minigame() -> None:
    floors_even: List[unrealsdk.UObject] = []
    floors_odd: List[unrealsdk.UObject] = []
    flipflop: bool = True
    i = 1
    while i <= 25:
        if i % 2 == 0:
            floors_even.append(placeablehelper.TAGGED_OBJECTS[f"Floor {i}"][0].uobj)
        else:
            floors_odd.append(placeablehelper.TAGGED_OBJECTS[f"Floor {i}"][0].uobj)
        i += 1

    for oddfloor in floors_odd:
        floorpos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(oddfloor)
        newpos: Tuple[float, float, float] = (floorpos[0], floorpos[1], floorpos[2] - 10000)
        placeablehelper.static_mesh.set_location(oddfloor, newpos)

    while not GameState.mission_complete:
        offset: float = -10000 if flipflop else 10000
        for floor in floors_even:
            floorpos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(floor)
            newpos: Tuple[float, float, float] = (floorpos[0], floorpos[1], floorpos[2] + offset)
            placeablehelper.static_mesh.set_location(floor, newpos)
        for otherfloor in floors_odd:
            floorpos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(otherfloor)
            newpos: Tuple[float, float, float] = (floorpos[0], floorpos[1], floorpos[2] - offset)
            placeablehelper.static_mesh.set_location(otherfloor, newpos)

        pc: unrealsdk.UObject = unrealsdk.GetEngine().GamePlayers[0].Actor
        ploc = pc.Pawn.Location
        pc.Pawn.Location = (
            ploc.X,
            ploc.Y,
            ploc.Z + 0.01,
        )
        pc.PlayUIAkEvent(unrealsdk.FindObject("AkEvent", "Ake_UI.UI_Generic.Ak_Play_UI_Generic_Countdown"))
        flipflop = not flipflop
        time.sleep(2)
