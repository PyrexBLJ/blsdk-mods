from typing import Tuple

import unrealsdk  # type: ignore

from Mods.MapLoader import placeablehelper

from .. import util
from ..game_state import GameState


def check_wall_hit(hit_loc) -> None:
    checks = [
        ("Unbroken Wall 1", "Broken Wall 1", (-28171.73828125, 18362.421875, 2164.306884765625), 1),
        ("Unbroken Wall 2", "Broken Wall 2", (-27389.712890625, 19056.484375, 2161.650146484375), 2),
        ("Unbroken Wall 3", "Broken Wall 3", (-28106.728515625, 19841.458984375, 2162.153076171875), 3),
    ]

    def check_wall(wall: str, broken_wall: str, goal: Tuple[float, float, float], index: int) -> None:
        if util.distance(hit_loc, goal) <= 150 and not GameState.current_map.custom_map_data[index]:
            # unrealsdk.Log(f"Shot Passed {wall} Check")
            wallnum = wall[-1]
            normalwall: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS[wall][0].uobj
            brokenwall: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS[broken_wall][0].uobj
            wallcracks: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS[f"Wall Cracks {wallnum}"][0].uobj
            normalwallpos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(normalwall)
            brokenwallpos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(brokenwall)
            placeablehelper.static_mesh.set_location(wallcracks, brokenwallpos)
            placeablehelper.static_mesh.set_location(brokenwall, normalwallpos)
            placeablehelper.static_mesh.set_location(normalwall, brokenwallpos)
            GameState.current_map.custom_map_data[index] = True  # Wall 1 broken
            normalwall = None
            brokenwall = None
            wallcracks = None

    for check in checks:
        check_wall(*check)
