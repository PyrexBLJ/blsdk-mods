import threading
import time
from typing import List, Tuple

import unrealsdk  # type: ignore

import Mods.UserFeedback as uFeed
from Mods.MapLoader import placeablehelper

from ..game_state import GameState
from ..maps import MAP_DATA, MapData, MapType
from .. import util

def drop_raid_loot() -> None:
    if GameState.current_map.map_file == "D3 Terramorphous Raid Boss.json":
        bsl_obj = unrealsdk.ConstructObject("Behavior_SpawnLootAroundPoint")
        bsl_obj.ItemPools = [unrealsdk.FindObject("ItemPoolDefinition", "GD_CustomItemPools_MainGame.Mercenary.TedioreUncommon"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_06_Legendary"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_06_Legendary"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_04_Rare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_04_Rare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_04_Rare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_04_Rare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_04_Rare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_04_Rare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_04_Rare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare")]
        bsl_obj.SpawnVelocityRelativeTo = 0
        bsl_obj.bTorque = False
        bsl_obj.CircularScatterRadius = 350.0
        bsl_obj.CustomLocation = ((-27962.642578125, 5593.248046875, 5918.83349609375), None, "")
        bsl_obj.ApplyBehaviorToContext(unrealsdk.GetEngine().GamePlayers[0].Actor, (), None, None, None, ())
    if GameState.current_map.map_file == "D4 Son of Craw Raid Boss.json":
        bsl_obj = unrealsdk.ConstructObject("Behavior_SpawnLootAroundPoint")
        bsl_obj.ItemPools = [unrealsdk.FindObject("ItemPoolDefinition", "GD_CustomItemPools_MainGame.Mercenary.TedioreUncommon"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_06_Legendary"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_06_Legendary"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_04_Rare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_04_Rare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_04_Rare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_04_Rare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_04_Rare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_04_Rare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_04_Rare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare"),
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare")]
        bsl_obj.SpawnVelocityRelativeTo = 0
        bsl_obj.bTorque = False
        bsl_obj.CircularScatterRadius = 350.0
        bsl_obj.CustomLocation = ((42266.7421875, -755.392333984375, -1942.8280029296875), None, "")
        bsl_obj.ApplyBehaviorToContext(unrealsdk.GetEngine().GamePlayers[0].Actor, (), None, None, None, ())