import threading
import time
from typing import List, Tuple

import unrealsdk  # type: ignore

import Mods.UserFeedback as uFeed
from Mods.MapLoader import placeablehelper

from ..game_state import GameState
from ..maps import MAP_DATA, MapData, MapType
from .. import util

class secret_boss:
    door_is_open: bool = False
    candisplaytip: bool = False

    def open_door() -> None:
        door: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["Raid Door"][0].uobj
        done: bool = False
        while not done:
            doorrot: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(door)
            if doorrot[2] <= -2798:
                newpos: Tuple[float, float, float] = (doorrot[0], doorrot[1], doorrot[2] + 5)
                placeablehelper.static_mesh.set_location(door, newpos)
            else:
                done = True
                secret_boss.door_is_open = True
            time.sleep(0.01)
        door = None

    def warning() -> None:
        thebutt: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["Final Message"][0].uobj
        if thebutt is None:
            return
        
        location: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(thebutt)
        if util.distance(util.get_player_location(), location) < 250:
            if not secret_boss.candisplaytip:
                secret_boss.candisplaytip = True
                uFeed.ShowHUDMessage(
                    Title="Buttstallion:",
                    Message="One final challenge lies ahead. Good luck!",
                    Duration=7,
                    MenuHint=0,
                )
        else:
            secret_boss.candisplaytip = False
        thebutt = None

    def move_door_2() -> None:
        door: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["EE Door"][0].uobj
        done: bool = False
        while not done:
            doorrot: Tuple[int, int, int] = placeablehelper.static_mesh.get_rotation(door)
            if doorrot[1] >= 3800:
                newpos: Tuple[int, int, int] = (doorrot[0], doorrot[1] - 100, doorrot[2])
                placeablehelper.static_mesh.set_rotation(door, newpos)
            else:
                done = True
                door = None
            time.sleep(0.01)

    def check_buttons() -> None:
        button_enter: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["EE Entrance"][0].uobj
        button_door: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["EE Door Switch"][0].uobj
        button_exit: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["EE Exit Button"][0].uobj
        if util.distance(util.get_player_location(), placeablehelper.interactive_objects.get_location(button_enter)) <= 750:
            unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn.Location = (-513.8223266601562, -23112.46484375, -29816.712890625)
            unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn.Controller.Rotation = (65171, 67, 0)
        if util.distance(util.get_player_location(), placeablehelper.interactive_objects.get_location(button_door)) <= 750 and GameState.current_map.custom_map_data[2] == False:
            GameState.current_map.custom_map_data[2] = True
            threading.Thread(target=secret_boss.move_door_2).start()
        if util.distance(util.get_player_location(), placeablehelper.interactive_objects.get_location(button_exit)) <= 750:
            unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn.Location = (310.5557556152344, -23007.0234375, -3667.004638671875)
            unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn.Controller.Rotation = (64702, -38768, 0)
        button_enter = None
        button_door = None
        button_exit = None

    def spawn_something_idk() -> None:
        if GameState.current_map.custom_map_data[3] == False:
            GameState.current_map.custom_map_data[3] == True
            bsl_obj = unrealsdk.ConstructObject("Behavior_SpawnLootAroundPoint")
            i: int = 0
            drops: list = []
            while i < 20:
                i += 1
                drops.append(unrealsdk.FindObject("ItemPoolDefinition", "GD_Sage_ItemPools.SeraphCrystal.Pool_SeraphCrystal_1_Drop"))
            bsl_obj.ItemPools = drops
            bsl_obj.SpawnVelocityRelativeTo = 0
            bsl_obj.bTorque = False
            bsl_obj.CircularScatterRadius = 350.0
            bsl_obj.CustomLocation = ((-346.90673828125, -13988.5771484375, -4018.62890625), None, "")
            bsl_obj.ApplyBehaviorToContext(unrealsdk.GetEngine().GamePlayers[0].Actor, (), None, None, None, ())