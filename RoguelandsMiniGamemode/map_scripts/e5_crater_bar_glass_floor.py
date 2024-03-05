from typing import Tuple

import unrealsdk  # type: ignore

from Mods.MapLoader import placeablehelper

from .. import maps, util


def glass_break_minigame(this_map: maps.MapData) -> None:
    """Glass Floor Break Minigame. Some floors break upon standing on them."""
    pc: unrealsdk.UObject = unrealsdk.GetEngine().GamePlayers[0].Actor
    pawn: unrealsdk.UObject = pc.Pawn
    location: unrealsdk.FStruct = pawn.Location

    glass_tiles = [
        ("floor 1", 1, (32026.0703125, -997.4097290039062, 4066.887451171875)),
        ("floor 3", 2, (32025.7578125, -1309.262451171875, 4066.8798828125)),
        ("floor 6", 3, (32349.49609375, -1615.2686767578125, 4066.88134765625)),
        ("floor 7", 4, (32026.12890625, -1915.8193359375, 4066.88671875)),
        ("floor 10", 5, (32349.84765625, -2226.63720703125, 4066.885498046875)),
        ("floor 12", 6, (32349.58984375, -2539.52001953125, 4066.88720703125)),
        ("floor 13", 7, (32023.939453125, -2855.940673828125, 4066.885009765625)),
        ("floor 16", 8, (32346.671875, -3170.296875, 4066.88134765625)),
        ("floor 18", 9, (32349.54296875, -3484.7998046875, 4066.882080078125)),
        ("floor 19", 10, (32025.66796875, -3796.82568359375, 4066.894287109375)),
    ]
    glass_break_sfx: unrealsdk.UObject = unrealsdk.FindObject(
        "AkEvent",
        "Ake_UI.UI_HUD.Ak_Play_UI_HUD_FastTravel_Cancel",
    )

    def check_glass_tile(tag: str, index: int, goal: Tuple[float, float, float]) -> None:
        if util.distance(location, goal) <= 100 and not this_map.custom_map_data[index]:
            glass_floor: unrealsdk.UObject = placeablehelper.TAGGED_OBJECTS[tag][0].uobj
            floorpos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(glass_floor)
            newpos: Tuple[float, float, float] = (floorpos[0], floorpos[1], floorpos[2] - 10000)
            placeablehelper.static_mesh.set_location(glass_floor, newpos)
            pc.PlayUIAkEvent(glass_break_sfx)
            this_map.custom_map_data[index] = True
            glass_floor = None

    for tile in glass_tiles:
        check_glass_tile(*tile)
