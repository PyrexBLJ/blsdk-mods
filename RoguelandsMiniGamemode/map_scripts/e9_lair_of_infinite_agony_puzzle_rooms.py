import threading
from typing import Tuple

import unrealsdk  # type: ignore

from Mods.MapLoader import placeablehelper

from .. import maps, util
import time


def loia_puzzle(this_map: maps.MapData, hitloc) -> None:
    playerpawn = unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn
    if playerpawn.Weapon and (
        util.distance(
            hitloc,
            (placeablehelper.static_mesh.get_location(placeablehelper.TAGGED_OBJECTS["Button 2"][0].uobj)),
        )
        <= 150
        and not this_map.custom_map_data[2]
    ):
        this_map.custom_map_data[2] = True
        unrealsdk.GetEngine().GamePlayers[0].Actor.PlayAkEvent(
            unrealsdk.FindObject("AkEvent", "Ake_Seq_Missions.Missions.Misc.Ak_Play_Seq_Earthquake_Rumble"),
        )
        e = threading.Thread(target=loia_puzzle_door_2)
        e.start()

def loia_puzzle_player(this_map: maps.MapData) -> None:
    if (
        util.distance(util.get_player_location(), (placeablehelper.static_mesh.get_location(placeablehelper.TAGGED_OBJECTS["Button 1"][0].uobj))) <= 150
        and not this_map.custom_map_data[1]
    ):
        this_map.custom_map_data[1] = True
        unrealsdk.GetEngine().GamePlayers[0].Actor.PlayAkEvent(
            unrealsdk.FindObject("AkEvent", "Ake_Seq_Missions.Missions.Misc.Ak_Play_Seq_Earthquake_Rumble"),
        )
        d = threading.Thread(target=loia_puzzle_door_1)
        d.start()
    if (
        util.distance(util.get_player_location(), (placeablehelper.static_mesh.get_location(placeablehelper.TAGGED_OBJECTS["Button 3"][0].uobj))) <= 150
        and not this_map.custom_map_data[3]
    ):
        this_map.custom_map_data[3] = True
        unrealsdk.GetEngine().GamePlayers[0].Actor.PlayAkEvent(
            unrealsdk.FindObject("AkEvent", "Ake_Seq_Missions.Missions.Misc.Ak_Play_Seq_Earthquake_Rumble"),
        )
        f = threading.Thread(target=loia_puzzle_statue_1)
        f.start()

def loia_puzzle_door_1() -> None:
    door1: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["Door 1"][0].uobj
    done: bool = False
    while not done:
        door1pos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(door1)
        if door1pos[2] <= 1114:
            newpos: Tuple[float, float, float] = (door1pos[0], door1pos[1], door1pos[2] + 2)
            placeablehelper.static_mesh.set_location(door1, newpos)
        else:
            done = True
        time.sleep(0.01)


def loia_puzzle_door_2() -> None:
    door2: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["Door 2"][0].uobj
    done: bool = False
    while not done:
        door2pos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(door2)
        if door2pos[2] <= 1403:
            newpos: Tuple[float, float, float] = (door2pos[0], door2pos[1], door2pos[2] + 2)
            placeablehelper.static_mesh.set_location(door2, newpos)
        else:
            done = True
        time.sleep(0.01)


def loia_puzzle_statue_1() -> None:
    statue: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["Statue 1"][0].uobj
    done: bool = False
    while not done:
        statuepos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(statue)
        if statuepos[0] >= -17722:
            newpos: Tuple[float, float, float] = (statuepos[0] - 2, statuepos[1], statuepos[2])
            placeablehelper.static_mesh.set_location(statue, newpos)
        else:
            done = True
        time.sleep(0.01)
