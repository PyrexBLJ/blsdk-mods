import threading
from typing import Tuple

import unrealsdk  # type: ignore

from Mods.MapLoader import placeablehelper

from .. import maps, mission_display, util
from ..game_state import GameState


class State:
    miniboss_objects: unrealsdk.UObject = None


def miniboss_shootable_objects(this_map: maps.MapData, hitloc) -> None:
    pc: unrealsdk.UObject = unrealsdk.GetEngine().GamePlayers[0].Actor
    pawn: unrealsdk.UObject = pc.Pawn
    if State.miniboss_objects is None:
        State.miniboss_objects = placeablehelper.TAGGED_OBJECTS.get("Side Object 1")
    if State.miniboss_objects is None or not GameState.map_is_loaded or not pawn.Weapon:
        return
    sideobject1 = placeablehelper.TAGGED_OBJECTS["Side Object 1"][0].uobj
    sideobject2 = placeablehelper.TAGGED_OBJECTS["Side Object 2"][0].uobj
    sideobject3 = placeablehelper.TAGGED_OBJECTS["Side Object 3"][0].uobj
    sideobject4 = placeablehelper.TAGGED_OBJECTS["Side Object 4"][0].uobj
    if (
        util.distance(
            hitloc,
            placeablehelper.static_mesh.get_location(sideobject1),
        )
        < 150
    ):
        objplace: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(sideobject1)
        newplace: Tuple[float, float, float] = (objplace[0], objplace[1], objplace[2] - 10000)
        placeablehelper.static_mesh.set_location(sideobject1, newplace)
        pc.PlayUIAkEvent(unrealsdk.FindObject("AkEvent", "Ake_UI.UI_HUD.Ak_Play_UI_HUD_Objective_Increment"))
        this_map.custom_map_data[2] += 1
        mission_display.update_mission_display()
    if (
        util.distance(
            hitloc,
            placeablehelper.static_mesh.get_location(sideobject2),
        )
        < 150
    ):
        objplace: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(sideobject2)
        newplace: Tuple[float, float, float] = (objplace[0], objplace[1], objplace[2] - 10000)
        placeablehelper.static_mesh.set_location(sideobject2, newplace)
        pc.PlayUIAkEvent(unrealsdk.FindObject("AkEvent", "Ake_UI.UI_HUD.Ak_Play_UI_HUD_Objective_Increment"))
        this_map.custom_map_data[2] += 1
        mission_display.update_mission_display()
    if (
        util.distance(
            hitloc,
            placeablehelper.static_mesh.get_location(sideobject3),
        )
        < 150
    ):
        objplace: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(sideobject3)
        newplace: Tuple[float, float, float] = (objplace[0], objplace[1], objplace[2] - 10000)
        placeablehelper.static_mesh.set_location(sideobject3, newplace)
        pc.PlayUIAkEvent(unrealsdk.FindObject("AkEvent", "Ake_UI.UI_HUD.Ak_Play_UI_HUD_Objective_Increment"))
        this_map.custom_map_data[2] += 1
        mission_display.update_mission_display()
    if (
        util.distance(
            hitloc,
            placeablehelper.static_mesh.get_location(sideobject4),
        )
        < 350
    ):
        objplace: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(sideobject4)
        newplace: Tuple[float, float, float] = (objplace[0], objplace[1], objplace[2] - 10000)
        placeablehelper.static_mesh.set_location(sideobject4, newplace)
        pc.PlayUIAkEvent(unrealsdk.FindObject("AkEvent", "Ake_UI.UI_Mission.Ak_Play_UI_Mission_Reward"))
        droppos: Tuple[float, float, float] = (objplace[0], objplace[1], objplace[2] + 50)
        bsl = unrealsdk.ConstructObject("Behavior_SpawnLootAroundPoint")
        if GameState.level_offset == 2:
            bsl.ItemPools = [unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare_Alien"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare_Alien"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare_Alien"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare_Alien"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare_Alien")]
        else:
            bsl.ItemPools = [unrealsdk.FindObject("ItemPoolDefinition", "GD_CustomItemPools_MainGame.Soldier.TedioreUncommon"), unrealsdk.FindObject("ItemPoolDefinition", "GD_CustomItemPools_MainGame.Soldier.TedioreUncommon"), unrealsdk.FindObject("ItemPoolDefinition", "GD_CustomItemPools_MainGame.Soldier.TedioreUncommon"), unrealsdk.FindObject("ItemPoolDefinition", "GD_CustomItemPools_MainGame.Soldier.TedioreUncommon"), unrealsdk.FindObject("ItemPoolDefinition", "GD_CustomItemPools_MainGame.Soldier.TedioreUncommon")]
        bsl.SpawnVelocityRelativeTo = 0
        bsl.bTorque = False
        bsl.CircularScatterRadius = 100.0
        bsl.CustomLocation = (droppos, None, "")
        bsl.ApplyBehaviorToContext(unrealsdk.GetEngine().GamePlayers[0].Actor, (), None, None, None, ())
    if this_map.custom_map_data[2] == 3 and this_map.custom_map_data[3] is False:
        objplace: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(sideobject4)
        newplace: Tuple[float, float, float] = (objplace[0], objplace[1], objplace[2] + 10000)
        placeablehelper.static_mesh.set_location(sideobject4, newplace)
        this_map.custom_map_data[3] = True
