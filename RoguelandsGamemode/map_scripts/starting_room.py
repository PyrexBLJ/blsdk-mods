import random
import threading
import time
from typing import List, Tuple

import unrealsdk  # type: ignore

import Mods.UserFeedback as uFeed
from Mods.MapLoader import placeablehelper

from .. import maps, util
from ..game_state import GameState

__all__ = ["start_loot_thread", "check_for_tip"]


TIPS: List[str] = [
    "Be sure to explore maps! I heard there are some cool, hidden easter eggs lying around.",
    "Have you found my hidden Prismatic Plates yet? I'll give you nice loot if you stand on them.",
    "As you progress, loot rewards will get better.",
    "Be on the lookout for vault symbols. They now give nice loot if you approach them.",
    "Enemies have a chance to drop rare candies! They give very powerful effects, but they only last for a short duration.",
    "Slag has been reduced to a 50% damage bonus. It still helps, but you don't have to rely heavily on it.",
    "I heard a rumor about rare, loot enemies roaming the Roguelands. I've never actually seen one though.",
    "I hope you enjoy my mini games! There are many more to check out at the end of each rotation.",
    "Difficulty has been completely reworked! Don't fear soloing a raid boss.",
    "Defeating a boss rewards an ethereal gift box. Shoot them open for nice rewards!",
    "Your ammo is refilled at the beginning of every round. However, grenades and launcher ammo get a smaller portion back.",
]


class State:
    candisplaytip: bool = False

    @staticmethod
    def reset() -> None:
        State.candisplaytip = False


def start_loot_thread() -> None:
    """Thread job to drop the starting gear in the starting room."""
    #time.sleep(random.randint(200, 300) / 100)
    sbsl_obj = unrealsdk.ConstructObject("Behavior_SpawnLootAroundPoint")
    sbsl_obj.ItemPools = [unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_Pistols_02_Uncommon"), 
                          unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_Shotguns_02_Uncommon"), 
                          unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_SniperRifles_02_Uncommon"), 
                          unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_Launchers_02_Uncommon"), 
                          unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.ShieldPools.Pool_Shields_All_02_Uncommon"), 
                          unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.GrenadeModPools.Pool_GrenadeMods_02_Uncommon"), 
                          unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.ClassModPools.Pool_ClassMod_02_Uncommon"), 
                          unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.ArtifactPools.Pool_Artifacts_02_Uncommon")]
    sbsl_obj.SpawnVelocityRelativeTo = 0
    sbsl_obj.bTorque = False
    sbsl_obj.CircularScatterRadius = 300
    sbsl_obj.CustomLocation = ((5789, -44759, -4841), None, "")
    sbsl_obj.ApplyBehaviorToContext(unrealsdk.GetEngine().GamePlayers[0].Actor, (), None, None, None, ())
    """pos = (6189.056640625, -44646.37890625, -4841.07470703125)
    util.drop_from_pool("GD_Itempools.WeaponPools.Pool_Weapons_Pistols_02_Uncommon", pos, 80)
    pos = (pos[0] - 100, pos[1], pos[2])
    time.sleep(0.5)
    util.drop_from_pool("GD_Itempools.WeaponPools.Pool_Weapons_Shotguns_02_Uncommon", pos, 80)
    pos = (pos[0] - 100, pos[1], pos[2])
    time.sleep(0.5)
    util.drop_from_pool("GD_Itempools.WeaponPools.Pool_Weapons_SniperRifles_02_Uncommon", pos, 80)
    pos = (pos[0] - 100, pos[1], pos[2])
    time.sleep(0.5)
    util.drop_from_pool("GD_Itempools.WeaponPools.Pool_Weapons_Launchers_02_Uncommon", pos, 80)
    pos = (pos[0] - 100, pos[1], pos[2])
    time.sleep(0.5)
    util.drop_from_pool("GD_Itempools.ShieldPools.Pool_Shields_All_02_Uncommon", pos, 80)
    pos = (pos[0] - 100, pos[1], pos[2])
    time.sleep(0.5)
    util.drop_from_pool("GD_Itempools.GrenadeModPools.Pool_GrenadeMods_02_Uncommon", pos, 80)
    pos = (pos[0] - 100, pos[1], pos[2])
    time.sleep(0.5)
    util.drop_from_pool("GD_Itempools.ClassModPools.Pool_ClassMod_02_Uncommon", pos, 80)
    pos = (pos[0] - 100, pos[1], pos[2])
    time.sleep(0.5)
    util.drop_from_pool("GD_Itempools.ArtifactPools.Pool_Artifacts_02_Uncommon", pos, 80)
    pos = (pos[0] - 100, pos[1], pos[2])
    time.sleep(0.5)"""


def check_for_tip() -> None:
    """Shows a random tip in the starting room if the player is close to Buttstallion."""
    thebutt = placeablehelper.TAGGED_OBJECTS.get("ButtStallion")
    if thebutt is None:
        return
    
    location: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(
        placeablehelper.TAGGED_OBJECTS["ButtStallion"][0].uobj,
    )
    if util.distance(util.get_player_location(), location) < 250:
        if not State.candisplaytip:
            State.candisplaytip = True
            uFeed.ShowHUDMessage(
                Title="Buttstallion says:",
                Message=TIPS[random.randint(0, len(TIPS) - 1)],
                Duration=7,
                MenuHint=0,
            )
    else:
        State.candisplaytip = False


def lel_gubs(this_map: maps.MapData, hitloc) -> None:
    """Spawns bunch of gubs in the starting room in the third rotation? yes"""
    if this_map.map_file != "G4 Leviathans Lair Starting Room 3.json":
        return
    target = placeablehelper.TAGGED_OBJECTS.get("Target 1")
    if target is None or not GameState.map_is_loaded:
        return
    if (util.distance(hitloc, placeablehelper.static_mesh.get_location(target[0].uobj)) < 150 and not this_map.custom_map_data[3]):
        this_map.custom_map_data[3] = True
        ploc = util.get_player_location()
        pos: Tuple[float, float, float] = (
            ploc.X,
            ploc.Y,
            ploc.Z + 200,
        )
        bsl_obj = unrealsdk.ConstructObject("Behavior_SpawnLootAroundPoint")
        bsl_obj.ItemPools = [unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.Runnables.Pool_Laney"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.Runnables.Pool_Laney"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.Runnables.Pool_Laney"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.Runnables.Pool_Laney"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.Runnables.Pool_Laney")]
        bsl_obj.SpawnVelocityRelativeTo = 0
        bsl_obj.bTorque = False
        bsl_obj.CircularScatterRadius = 150.0
        bsl_obj.CustomLocation = (pos, None, "")
        bsl_obj.ApplyBehaviorToContext(unrealsdk.GetEngine().GamePlayers[0].Actor, (), None, None, None, ())
