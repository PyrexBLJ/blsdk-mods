import threading
import time
from typing import Tuple

import unrealsdk  # type: ignore

import Mods.UserFeedback as uFeed
from Mods.MapLoader import placeablehelper

from .. import util
from ..game_state import GameState


class State:
    token: unrealsdk.UObject = None

    @staticmethod
    def reset() -> None:
        State.token = None

def check_token() -> None:
    if State.token == None:
        State.token = placeablehelper.TAGGED_OBJECTS["Token of Wealth Trigger"][0].uobj
    if State.token is not None and not GameState.current_map.custom_map_data[0]:
        if util.distance(util.get_player_location(), placeablehelper.interactive_objects.get_location(State.token)) <= 750:
            GameState.current_map.custom_map_data[0] = True
            unrealsdk.Log("Found Token")
            if GameState.current_map.map_file == "J2 Frost Bottom Hoard Round.json":
                chests: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS.get("Chest Reward")
                for chest in chests:
                    startloc = placeablehelper.interactive_objects.get_location(chest.uobj)
                    newloc: Tuple[float, float, float] = (startloc[0], startloc[1], startloc[2] + 10000)
                    placeablehelper.interactive_objects.set_location(chest.uobj, newloc)
            elif GameState.current_map.map_file == "J1 Murderlin's Temple Hoard Round.json":
                bsl_obj = unrealsdk.ConstructObject("Behavior_SpawnLootAroundPoint")
                bsl_obj.ItemPools = [unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"),
                                     unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"),
                                     unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"),
                                     unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"),
                                     unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"),
                                     unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"),
                                     unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"),
                                     unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar")]
                bsl_obj.SpawnVelocityRelativeTo = 0
                bsl_obj.bTorque = False
                bsl_obj.CircularScatterRadius = 350.0
                bsl_obj.CustomLocation = ((3931.542236328125, 17169.96875, 4162.85986328125), None, "")
                bsl_obj.ApplyBehaviorToContext(unrealsdk.GetEngine().GamePlayers[0].Actor, (), None, None, None, ())
            elif GameState.current_map.map_file == "J3 Wam Bam Hoard Round.json":
                table = placeablehelper.TAGGED_OBJECTS["Offering Table"][0].uobj
                offering = placeablehelper.TAGGED_OBJECTS["Eridium Offering"][0].uobj
                tableloc = placeablehelper.interactive_objects.get_location(table)
                offeringloc = placeablehelper.interactive_objects.get_location(offering)
                newtableloc: Tuple[float, float, float] = (tableloc[0], tableloc[1], tableloc[2] + 10000)
                newofferingloc: Tuple[float, float, float] = (offeringloc[0], offeringloc[1], offeringloc[2] + 10000)
                placeablehelper.interactive_objects.set_location(table, newtableloc)
                placeablehelper.interactive_objects.set_location(offering, newofferingloc)
            
            visibletoken = placeablehelper.TAGGED_OBJECTS["Token of Wealth"][0].uobj
            loc = placeablehelper.static_mesh.get_location(visibletoken)
            endloc: Tuple[float, float, float] = (loc[0], loc[1], loc[2] - 10000)
            placeablehelper.static_mesh.set_location(visibletoken, endloc)
            placeablehelper.interactive_objects.set_location(State.token, endloc)
            unrealsdk.GetEngine().GamePlayers[0].Actor.PlayUIAkEvent(unrealsdk.FindObject("AkEvent", "Ake_UI.UI_HUD.Ak_Play_UI_Alert_CoOp_Ding"))

def move_wall() -> None:
    door: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["Lowering Rock Wall"][0].uobj
    done: bool = False
    while not done:
        doorrot: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(door)
        if doorrot[2] >= 1164:
            newpos: Tuple[float, float, float] = (doorrot[0], doorrot[1], doorrot[2] - 5)
            placeablehelper.static_mesh.set_location(door, newpos)
        else:
            done = True
            door = None
        time.sleep(0.01)

def check_offering() -> None:
    if util.distance(util.get_player_location(), placeablehelper.interactive_objects.get_location(placeablehelper.TAGGED_OBJECTS["Offering Table"][0].uobj)) < 700 and GameState.current_map.custom_map_data[1] == False:
        GameState.current_map.custom_map_data[1] = True
        threading.Thread(target=move_wall).start()