import threading
from typing import Tuple

import unrealsdk  # type: ignore

import Mods.UserFeedback as uFeed
from Mods.MapLoader import placeablehelper

from .. import util
from ..game_state import GameState


class State:
    prismatic_plate: unrealsdk.UObject = None
    vault_symbol: unrealsdk.UObject = None

    @staticmethod
    def reset() -> None:
        State.prismatic_plate = None
        State.vault_symbol = None


def check_plates() -> None:
    if State.prismatic_plate is None:
        State.prismatic_plate = placeablehelper.TAGGED_OBJECTS.get("Pressure Plate")
    if State.prismatic_plate is not None and not GameState.current_map.custom_map_data[0]:
        pc: unrealsdk.UObject = unrealsdk.GetEngine().GamePlayers[0].Actor
        ploc = pc.Pawn.Location
        if (
            util.distance(
                ploc,
                placeablehelper.static_mesh.get_location(State.prismatic_plate[0].uobj),
            )
            < 125
        ):
            pos: Tuple[float, float, float] = (
                ploc.X,
                ploc.Y,
                ploc.Z + 50,
            )
            bsl_obj = unrealsdk.ConstructObject("Behavior_SpawnLootAroundPoint")
            bsl_obj.ItemPools = [unrealsdk.FindObject("ItemPoolDefinition", "GD_Aster_ItemPools.WeaponPools.Pool_Weapons_04_Gemstone"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Aster_ItemPools.WeaponPools.Pool_Weapons_04_Gemstone"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Aster_ItemPools.WeaponPools.Pool_Weapons_04_Gemstone"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar")]
            bsl_obj.SpawnVelocityRelativeTo = 0
            bsl_obj.bTorque = False
            bsl_obj.CircularScatterRadius = 50.0
            bsl_obj.CustomLocation = (pos, None, "")
            bsl_obj.ApplyBehaviorToContext(unrealsdk.GetEngine().GamePlayers[0].Actor, (), None, None, None, ())
            uFeed.ShowHUDMessage(
                Title="Prismatic Plate Found",
                Message="Buttstallion smiles upon you. Look for hidden prismatic plates in mobbing rounds.",
                Duration=7,
                MenuHint=0,
            )
            pc.PlayUIAkEvent(unrealsdk.FindObject("AkEvent", "Ake_UI.UI_HUD.Ak_Play_UI_Alert_CoOp_Ding"))
            GameState.current_map.custom_map_data[0] = True


def check_vault_symbols() -> None:
    if State.vault_symbol is None:
        State.vault_symbol = placeablehelper.TAGGED_OBJECTS.get("Vault Symbol Reward")
    if State.vault_symbol is not None and GameState.map_is_loaded and not GameState.current_map.custom_map_data[1]:
        pc: unrealsdk.UObject = unrealsdk.GetEngine().GamePlayers[0].Actor
        pawn: unrealsdk.UObject = pc.Pawn
        if (
            util.distance(
                util.get_player_location(),
                placeablehelper.interactive_objects.get_location(State.vault_symbol[0].uobj),
            )
            < 300
            or util.distance(
                pawn.GetPawnViewLocation(),
                placeablehelper.interactive_objects.get_location(State.vault_symbol[0].uobj),
            )
            < 300
        ):
            pos: Tuple[float, float, float] = (
                util.get_player_location().X,
                util.get_player_location().Y,
                util.get_player_location().Z + 50,
            )
            bsl_obj = unrealsdk.ConstructObject("Behavior_SpawnLootAroundPoint")
            if GameState.level_offset > 0:
                bsl_obj.ItemPools = [unrealsdk.FindObject("ItemPoolDefinition", "GD_CustomItemPools_MainGame.Assassin.TedioreUncommon"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar")]
            else:
                bsl_obj.ItemPools = [unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.ArtifactPools.Pool_Artifacts_03_Rare"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar")]
            bsl_obj.SpawnVelocityRelativeTo = 0
            bsl_obj.bTorque = False
            bsl_obj.CircularScatterRadius = 150.0
            bsl_obj.CustomLocation = (pos, None, "")
            bsl_obj.ApplyBehaviorToContext(unrealsdk.GetEngine().GamePlayers[0].Actor, (), None, None, None, ())
            uFeed.ShowHUDMessage(
                Title="Vault Symbol Found",
                Message="The Eridians give you power. Look for hidden vault symbols in mobbing rounds.",
                Duration=7,
                MenuHint=0,
            )
            pc.PlayUIAkEvent(unrealsdk.FindObject("AkEvent", "Ake_UI.UI_HUD.Ak_Play_UI_Alert_CoOp_Ding"))
            GameState.current_map.custom_map_data[1] = True
