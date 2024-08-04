import time
from typing import List, Tuple

import unrealsdk  # type: ignore

import Mods.UserFeedback as uFeed
from Mods.MapLoader import placeablehelper

from ..game_state import GameState
from ..maps import MAP_DATA, MapData, MapType
from .. import util

class finish_room:
    abort_threads: bool = False
    can_show_hint: bool = False
    crystals_hit: int = 0
    hitcrystals: List[unrealsdk.UObject] = []

    def check_crystals(bullet) -> None:
        if finish_room.abort_threads == False:
            crystals: List[unrealsdk.UObject] = []
            i: int = 1
            while i <= 13:
                crystals.append(placeablehelper.TAGGED_OBJECTS[f"Crystal {i}"][0].uobj)
                i += 1
            for crystal in crystals:
                if util.distance(bullet, placeablehelper.static_mesh.get_location(crystal)) <= 350 and crystal not in finish_room.hitcrystals:
                    finish_room.hitcrystals.append(crystal)
                    finish_room.crystals_hit += 1
                    currentloc = placeablehelper.static_mesh.get_location(crystal)
                    newpos: Tuple[float, float, float] = (currentloc[0], currentloc[1], currentloc[2] - 10000)
                    placeablehelper.static_mesh.set_location(crystal, newpos)
                    unrealsdk.GetEngine().GamePlayers[0].Actor.PlayUIAkEvent(unrealsdk.FindObject("AkEvent", "Ake_Wep_Elemental_Shared.Ak_Play_EMP_Tech_SM_Fire"))
            if finish_room.crystals_hit >= 13:
                finish_room.abort_threads = True

    def boss_hint() -> None:
        bloodwing: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["Bloodwing Message"][0].uobj
        if bloodwing is None:
            return
    
        location: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(bloodwing)
        if util.distance(util.get_player_location(), location) < 250:
            if not finish_room.can_show_hint:
                finish_room.can_show_hint = True
                uFeed.ShowHUDMessage(
                    Title="Bloodwing says:",
                    Message="Those pesky pink crystals are ruining my vibe! Get rid of them for me.",
                    Duration=7,
                    MenuHint=0,
                )
        else:
            finish_room.can_show_hint = False

    def finish_cubes() -> None:
        cube1: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["Animated Cube 1"][0].uobj
        cube2: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["Animated Cube 2"][0].uobj
        cube1bool: bool = True
        cube2bool: bool = True

        i: int = 0
        k: int = 0
        while not GameState.mission_complete and not finish_room.abort_threads:
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
