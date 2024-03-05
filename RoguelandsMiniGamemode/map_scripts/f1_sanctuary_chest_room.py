import time
import threading
from typing import Tuple

import unrealsdk  # type: ignore

from Mods.MapLoader import placeablehelper

from ..game_state import GameState
from ..util import distance

def check_button(hitloc) -> None:
    pawn: unrealsdk.UObject = unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn
    plate: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["EE Plate"][0].uobj
    if pawn.Weapon:
        if distance(hitloc, placeablehelper.static_mesh.get_location(plate)) < 75 and GameState.current_map.custom_map_data[2] == False:
            GameState.current_map.custom_map_data[2] = True
            unrealsdk.GetEngine().GamePlayers[0].Actor.PlayUIAkEvent(
                unrealsdk.FindObject("AkEvent", "Ake_UI.UI_HUD.Ak_Play_UI_Alert_CoOp_Ding"),
            )
            threading.Thread(target=move_curtain).start()

def move_curtain() -> None:
    done: bool = False
    curtain: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS["Curtain EE"][0].uobj

    while not done:
        if GameState.travel_timer == 1:
            done = True
        curtainpos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(curtain)
        if curtainpos[2] < 3154:
            newcurtainpos: Tuple[float, float, float] = (curtainpos[0], curtainpos[1], curtainpos[2] + 1)
            placeablehelper.static_mesh.set_location(curtain, newcurtainpos)
            time.sleep(0.01)
        else:
            done = True