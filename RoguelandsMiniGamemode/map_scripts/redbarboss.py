import threading
from typing import List, Optional, Tuple

import unrealsdk  # type: ignore

from Mods.MapLoader import placeablehelper

from .. import util
from ..game_state import GameState


class State:
    gift_box: Optional[List[placeablehelper.TaggedObject]] = None
    happy_couples: bool = False

    @staticmethod
    def reset() -> None:
        State.gift_box = None
        State.happy_couples = False


def move_gift_box() -> None:
    if State.gift_box is None:
        State.gift_box = placeablehelper.TAGGED_OBJECTS.get("Gift Box")
    if State.gift_box is not None and not State.happy_couples and GameState.map_is_loaded:
        boxpos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(State.gift_box[0].uobj)
        hellopos: Tuple[float, float, float] = (boxpos[0], boxpos[1], boxpos[2] + 10000)
        placeablehelper.static_mesh.set_location(State.gift_box[0].uobj, hellopos)
        State.happy_couples = True


def open_gift_box(hitloc) -> None:
    if State.gift_box is None:
        State.gift_box = placeablehelper.TAGGED_OBJECTS.get("Gift Box")
    if State.gift_box is not None and GameState.map_is_loaded:
        pc: unrealsdk.UObject = unrealsdk.GetEngine().GamePlayers[0].Actor
        if (util.distance(hitloc, placeablehelper.static_mesh.get_location(State.gift_box[0].uobj)) < 150):
            boxpos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(State.gift_box[0].uobj)
            pos: Tuple[float, float, float] = (boxpos[0], boxpos[1], boxpos[2] + 50)
            bsl = unrealsdk.ConstructObject("Behavior_SpawnLootAroundPoint")
            if GameState.level_offset == 2:
                bsl.ItemPools = [unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_06_Legendary"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_06_Legendary"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_06_Legendary"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_06_Legendary"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_06_Legendary"), unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_06_Legendary")]
            else:
                bsl.ItemPools = [unrealsdk.FindObject("ItemPoolDefinition", "GD_CustomItemPools_MainGame.Siren.TedioreUncommon"), unrealsdk.FindObject("ItemPoolDefinition", "GD_CustomItemPools_MainGame.Siren.TedioreUncommon"), unrealsdk.FindObject("ItemPoolDefinition", "GD_CustomItemPools_MainGame.Siren.TedioreUncommon"), unrealsdk.FindObject("ItemPoolDefinition", "GD_CustomItemPools_MainGame.Siren.TedioreUncommon"), unrealsdk.FindObject("ItemPoolDefinition", "GD_CustomItemPools_MainGame.Siren.TedioreUncommon"), unrealsdk.FindObject("ItemPoolDefinition", "GD_CustomItemPools_MainGame.Siren.TedioreUncommon")]
            bsl.SpawnVelocityRelativeTo = 0
            bsl.bTorque = False
            bsl.CircularScatterRadius = 100.0
            bsl.CustomLocation = (pos, None, "")
            bsl.ApplyBehaviorToContext(unrealsdk.GetEngine().GamePlayers[0].Actor, (), None, None, None, ())
            pc.PlayUIAkEvent(unrealsdk.FindObject("AkEvent", "Ake_UI.UI_HUD.Ak_Play_UI_Alert_CoOp_Ding"))
            goodbyepos: Tuple[float, float, float] = (boxpos[0], boxpos[1], boxpos[2] - 10000)
            placeablehelper.static_mesh.set_location(State.gift_box[0].uobj, goodbyepos)
