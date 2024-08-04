from typing import Tuple

import unrealsdk  # type: ignore

from Mods.MapLoader import placeablehelper

from .. import maps, util


def glass_break_minigame(this_map: maps.MapData) -> None:
    """Glass Floor Break Minigame. Some floors break upon standing on them."""
    pc: unrealsdk.UObject = unrealsdk.GetEngine().GamePlayers[0].Actor
    pawn: unrealsdk.UObject = pc.Pawn
    location: unrealsdk.FStruct = pawn.Location

    # odd left, even right
    """
    Floor 1: 32026.0703125, -997.4097290039062, 4066.887451171875
    Floor 2: 32345.875, -994.6356811523438, 4066.8916015625
    Floor 3: 32025.7578125, -1309.262451171875, 4066.8798828125
    Floor 4: 32346.451171875, -1305.0458984375, 4066.886474609375
    Floor 5: 32027.2890625, -1616.6373291015625, 4066.87939453125
    Floor 6: 32349.49609375, -1615.2686767578125, 4066.88134765625
    Floor 7: 32026.12890625, -1915.8193359375, 4066.88671875
    Floor 8: 32345.84765625, -1918.456787109375, 4066.882568359375
    Floor 9: 32028.259765625, -2226.9990234375, 4066.885009765625
    Floor 10: 32349.84765625, -2226.63720703125, 4066.885498046875
    """

    glass_tiles_variant_1 = [
        ("floor 2", 1, (32345.875, -994.6356811523438, 4066.8916015625)),
        ("floor 3", 2, (32025.7578125, -1309.262451171875, 4066.8798828125)),
        ("floor 5", 3, (32027.2890625, -1616.6373291015625, 4066.87939453125)),
        ("floor 8", 4, (32345.84765625, -1918.456787109375, 4066.882568359375)),
        ("floor 9", 5, (32028.259765625, -2226.9990234375, 4066.885009765625)),
    ]

    glass_tiles_variant_2 = [
        ("floor 1", 1, (32026.0703125, -997.4097290039062, 4066.887451171875)),
        ("floor 4", 2, (32346.451171875, -1305.0458984375, 4066.886474609375)),
        ("floor 5", 3, (32027.2890625, -1616.6373291015625, 4066.87939453125)),
        ("floor 7", 4, (32026.12890625, -1915.8193359375, 4066.88671875)),
        ("floor 10", 5, (32349.84765625, -2226.63720703125, 4066.885498046875)),
    ]

    glass_tiles_variant_3 = [
        ("floor 2", 1, (32345.875, -994.6356811523438, 4066.8916015625)),
        ("floor 4", 2, (32346.451171875, -1305.0458984375, 4066.886474609375)),
        ("floor 6", 3, (32349.49609375, -1615.2686767578125, 4066.88134765625)),
        ("floor 8", 4, (32345.84765625, -1918.456787109375, 4066.882568359375)),
        ("floor 9", 5, (32028.259765625, -2226.9990234375, 4066.885009765625)),
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

    if this_map.map_file == "E2A Crater Bar Glass Floor 1.json":
        for tile in glass_tiles_variant_1:
            check_glass_tile(*tile)
    elif this_map.map_file == "E2B Crater Bar Glass Floor 2.json":
        for tile in glass_tiles_variant_2:
            check_glass_tile(*tile)
    elif this_map.map_file == "E2C Crater Bar Glass Floor 3.json":
        for tile in glass_tiles_variant_3:
            check_glass_tile(*tile)
