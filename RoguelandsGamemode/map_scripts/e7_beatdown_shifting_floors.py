import time
from typing import List, Tuple

import unrealsdk  # type: ignore

from Mods.MapLoader import placeablehelper

from ..game_state import GameState


def move_floors_for_floors_minigame() -> None:
    floors: List[unrealsdk.UObject] = []
    i = 1
    while i <= 25:
        floors.append(placeablehelper.TAGGED_OBJECTS[f"Floor {i}"][0].uobj)
        i += 1
    
    def set_floor_level(floor: unrealsdk.UObject, level: str) -> None:
        floorpos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(floor)

        if str(level) == "low":
            newpos: Tuple[float, float, float] = (floorpos[0], floorpos[1], -14192.7548828)
        else:
            newpos: Tuple[float, float, float] = (floorpos[0], floorpos[1], -4192.7548828125)

        placeablehelper.static_mesh.set_location(floor, newpos)
    
    def bump_player() -> None:
        pc: unrealsdk.UObject = unrealsdk.GetEngine().GamePlayers[0].Actor
        ploc = pc.Pawn.Location
        pc.Pawn.Location = (
            ploc.X,
            ploc.Y,
            ploc.Z + 0.01,
        )
        pc.PlayUIAkEvent(unrealsdk.FindObject("AkEvent", "Ake_UI.UI_Generic.Ak_Play_UI_Generic_Countdown"))


    def variation_1() -> None:
        flipflop: bool = False

        for oddfloor in floors:
            if floors.index(oddfloor) % 2 is not 0:
                set_floor_level(oddfloor, "low")

        while not GameState.mission_complete:
            if flipflop is True:
                for floor in floors:
                    if floors.index(floor) % 2 is not 0:
                        set_floor_level(floor, "low")
                    else:
                        set_floor_level(floor, "high")
            else:
                for floor in floors:
                    if floors.index(floor) % 2 is 0:
                        set_floor_level(floor, "low")
                    else:
                        set_floor_level(floor, "high")
            bump_player()
            flipflop = not flipflop
            time.sleep(2)

    def variation_2() -> None:
        index = 0
        while not GameState.mission_complete:
            for floor in floors:
                if floors.index(floor) >= index and floors.index(floor) < index + 5:
                    set_floor_level(floor, "high")
                else:
                    set_floor_level(floor, "low")
            index = index + 5
            if index >= 25:
                index = 0
            bump_player()
            time.sleep(2)

    def variation_3() -> None:
        forward: bool = True
        stage: int = 0

        while not GameState.mission_complete:
            for floor in floors:
                if floors.index(floor) % 5 is not stage:
                    set_floor_level(floor, "low")
                else:
                    set_floor_level(floor, "high")
            if stage == 4:
                forward = False
            elif stage == 0:
                forward = True
            if forward == True:
                stage += 1
            else:
                stage -= 1
            bump_player()
            time.sleep(2)

    if GameState.current_map.map_file == "E7A Beatdown Shifting Floors 1.json":
        variation_1()
    elif GameState.current_map.map_file == "E7B Beatdown Shifting Floors 2.json":
        variation_2()
    elif GameState.current_map.map_file == "E7C Beatdown Shifting Floors 3.json":
        variation_3()