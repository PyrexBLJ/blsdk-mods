from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Tuple


class MapType(Enum):
    Mobbing = 0
    MiniBoss = auto()
    RedBarBoss = auto()
    RaidBoss = auto()
    MiniGame = auto()
    Special = auto()
    FinalBoss = auto()
    StartRoom = auto()
    Hoard = auto()


@dataclass
class MapData:
    name: str
    package: str
    travel_object_name: str
    spawn_location: Tuple[float, float, float]
    spawn_rotation: Tuple[float, float, float]
    kill_challenge_count: int
    kill_challenge_goal: int
    bosses_killed: int
    total_bosses_in_map: int
    custom_map_data: List[Any]
    map_file: str
    has_been_visited_in_current_rotation: bool = False
    minigame_string: str = ""
    should_show_timer: bool = False
    is_easy: bool = False


MISSION_TYPE_READABLE: Dict[MapType, str] = {
    MapType.Mobbing: "Mobbing ",
    MapType.MiniBoss: "Mini Boss ",
    MapType.RedBarBoss: "Boss ",
    MapType.RaidBoss: "Raid Boss ",
    MapType.MiniGame: "Mini Game ",
    MapType.Special: "Reward ",
    MapType.FinalBoss: "Final Raid Boss ",
    MapType.StartRoom: "Starting ",
    MapType.Hoard: "Hoard ",
}


# fmt: off
MAP_DATA: Dict[MapType, List[MapData]] = { 
    MapType.Mobbing:[
        MapData("Southern Shelf", "southernshelf_p", "GD_FastTravelStations.Zone1.SouthernShelfTown", (11023.16015625, -27289.98828125, 953.4178466796825), (65060, 58501, 0), 0, 10, 0, 0, [False, False, False], "A1 Southern Shelf Mobbing 1.json", False, "", False, True),
        MapData("Southern Shelf", "southernshelf_p", "GD_FastTravelStations.Zone1.SouthernShelfTown", (72702.0390625, -43663.19921875, 1471.6229248046875), (64764, 28725, 0), 0, 15, 0, 0, [False, False, False], "A2 Southern Shelf Mobbing 2.json", False, "", False, True),
        MapData("Three Horns Divide", "ice_p", "GD_FastTravelStations.Zone1.IceEast", (-24243.75, 28081.41796875, 1172.033203125), (63855, -22553, 0), 0, 15, 0, 0, [False, False, False], "A3 Three Horns Divide Mobbing 1.json", False, "", False, True),
        MapData("Three Horns Divide", "ice_p", "GD_FastTravelStations.Zone1.IceEast", (-756.2860107421875, 23787.75390625, 2045.7357177734375), (439, 322, 0), 0, 15, 0, 0, [False, False, False], "A4 Three Horns Divide Mobbing 2.json"),
        MapData("Three Horns Valley", "frost_p", "GD_FastTravelStations.Zone1.IceWest", (-5716.23779296875, -16642.73046875, 610.8543701171875), (53, -22060, 0), 0, 15, 0, 0, [False, False, False], "A5 Three Horns Valley Mobbing 1.json"),
        MapData("Three Horns Valley", "frost_p", "GD_FastTravelStations.Zone1.IceWest", (-1139.935302734375, -1729.6339111328125, 2227.14990234375), (64721, 23437, 0), 0, 10, 0, 0, [False, False, False], "A6 Three Horns Valley Mobbing 2.json"),
        MapData("Frostburn Canyon", "icecanyon_p", "GD_FastTravelStations.Zone1.IceCanyon", (14857.6181640625, 11037.859375, -784.7105102539062), (31, -101594, 0), 0, 15, 0, 0, [False, False, False], "A7 Frostburn Canyon Mobbing 1.json", False, "", False, False),
        MapData("Frostburn Canyon", "icecanyon_p", "GD_FastTravelStations.Zone1.IceCanyon", (-1902.07177734375, 7972.1923828125, -1425.33447265625), (1098, -102790, 0), 0, 10, 0, 0, [False, False, False], "A8 Frostburn Canyon Mobbing 2.json", False, "", False, True),
        MapData("Frostburn Canyon", "icecanyon_p", "GD_FastTravelStations.Zone1.IceCanyon", (-11244.82421875, -7983.71533203125, 2193.81298828125), (270, -83246, 0), 0, 10, 0, 0, [False, False, False], "A9 Frostburn Canyon Mobbing 3.json", False, "", False, True),
        MapData("The Dust", "interlude_p", "GD_FastTravelStations.Interlude.Interlude", (-20662.64648375, 41168.25390625, -978.2523803710938), (65506, 11479, 0), 0, 15, 0, 0, [False, False, False], "A10 The Dust Mobbing 1.json", False, "", False, True),
        MapData("The Dust", "interlude_p", "GD_FastTravelStations.Interlude.Interlude", (9847.63118359375, 9473.2451171875, 2666.936767578125), (65097, -9530, 0), 0, 10, 0, 0, [False, False, False], "A11 The Dust Mobbing 2.json"),
        MapData("The Dust", "interlude_p", "GD_FastTravelStations.Interlude.Interlude", (7255.39306640625, 5436.0966796875, 2256.099853515625), (62745, 35157, 0), 0, 10, 0, 0, [False, False, False], "A12 The Dust Mobbing 3.json"),
        MapData("Friendship Gulag", "hypinterlude_p", "GD_LevelTravelStations.Interlude.HypInterToInterlude", (30122.88671875, 36552.98046875, 870.8934936523438), (65049, 69376, 0), 0, 10, 0, 0, [False, False, False], "A13 Friendship Gulag Mobbing 1.json", False, "", False, True),
        MapData("Friendship Gulag", "hypinterlude_p", "GD_LevelTravelStations.Interlude.HypInterToInterlude", (43251.04296875, 46589.6953125, 1077.626220703125), (65107, -1764, 0), 0, 10, 0, 0, [False, False, False], "A14 Friendship Gulag Mobbing 2.json"),
        MapData("Bloodshot Stronghold", "dam_p", "GD_FastTravelStations.Zone1.GoshDam", (-20712.9453125, 6925.21435546875, -764.1131591796875), (65244, 65476, 0), 0, 10, 0, 0, [False, False, False], "A15 Bloodshot Stronghold Mobbing 1.json"),
        MapData("Bloodshot Stronghold", "dam_p", "GD_FastTravelStations.Zone1.GoshDam", (-12872.740234375, 7850.85546875, -938.8500366210938), (65275, -5867, 0), 0, 10, 0, 0, [False, False, False], "A16 Bloodshot Stronghold Mobbing 2.json"),
        MapData("Bloodshot Stronghold", "dam_p", "GD_FastTravelStations.Zone1.GoshDam", (2124.275390625, -948.2235107421875, 93.57274627685547), (65055, -31057, 0), 0, 10, 0, 0, [False, False, False], "A17 Bloodshot Stronghold Mobbing 3.json"),
        MapData("Tundra Express", "tundraexpress_p", "GD_FastTravelStations.Zone1.TundraExpress", (-8717.740234375, 27135.87890625, 606.9339599609375), (64770, -55877, 0), 0, 10, 0, 0, [False, False, False], "A18 Tundra Express Mobbing 1.json"),
        MapData("Tundra Express", "tundraexpress_p", "GD_FastTravelStations.Zone1.TundraExpress", (-22344.51953125, 6240.91796875, 634.2890625), (77, -19114, 0), 0, 10, 0, 0, [False, False, False], "A19 Tundra Express Mobbing 2.json"),
        MapData("Tundra Express", "tundraexpress_p", "GD_FastTravelStations.Zone1.TundraExpress", (-7823.2607421875, 11024.740234375, 663.8499755859375), (65187, 47329, 0), 0, 15, 0, 0, [False, False, False], "A20 Tundra Express Mobbing 3.json"),
        MapData("Tundra Express", "tundraexpress_p", "GD_FastTravelStations.Zone1.TundraExpress", (960.5100708007812, 20647.15625, 1004.15478515625), (65146, 8812, 0), 0, 10, 0, 0, [False, False, False], "A21 Tundra Express Mobbing 4.json"),
        MapData("The Fridge", "fridge_p", "GD_FastTravelStations.Zone2.TheFridge", (6593.560546875, 17266.37109375, 10119.5556640625), (65443, -21361, 0), 0, 10, 0, 0, [False, False, False], "A22 The Fridge Mobbing 1.json"),
        MapData("The Fridge", "fridge_p", "GD_FastTravelStations.Zone2.TheFridge", (10723.4150390625, 14977.7734375, 10083.9892578125), (64916, -53262, 0), 0, 12, 0, 0, [False, False, False], "A23 The Fridge Mobbing 2.json", False, "", False, True),
        MapData("The Highlands Overlook", "grass_p", "GD_FastTravelStations.Zone2.Grass_B", (33227.17578125, 25636.052734375, 3245.69482421875), (65531, -65492, 0), 0, 15, 0, 0, [False, False, False], "A24 The Highlands Overlook Mobbing 1.json"),
        MapData("The Highlands Overlook", "grass_p", "GD_FastTravelStations.Zone2.Grass_B", (38293.41015625, 26388.376953125, 4805.7294921875), (134, -58593, 0), 0, 15, 0, 0, [False, False, False], "A25 The Highlands Overlook Mobbing 2.json"),
        MapData("Wildlife", "pandorapark_p", "GD_FastTravelStations.Zone2.PandoraPark", (-5126.951171875, 38851.62109375, -3370.150390625), (65315, -114492, 0), 0, 15, 0, 0, [False, False, False], "A26 Wildlife Mobbing 1.json"),
        MapData("Wildlife", "pandorapark_p", "GD_FastTravelStations.Zone2.PandoraPark", (-36193.58984375, 17656.044921875, -220.15000915527344), (50, -63871, 0), 0, 10, 0, 0, [False, False, False], "A27 Wildlife Mobbing 2.json", False, "", False, True),
        MapData("Wildlife", "pandorapark_p", "GD_FastTravelStations.Zone2.PandoraPark", (-32565.984375, 38420.71875, -395.91082763671875), (63988, 80484, 0), 0, 15, 0, 0, [False, False, False], "A28 Wildlife Mobbing 3.json", False, "", False, True),
        MapData("Wildlife", "pandorapark_p", "GD_FastTravelStations.Zone2.PandoraPark", (-25868.640625, 43404.1953125, -516.8499145507812), (64763, 49290, 0), 0, 10, 0, 0, [False, False, False], "A29 Wildlife Mobbing 4.json"),
        MapData("Thousand Cuts", "grass_cliffs_p", "GD_FastTravelStations.Zone2.Cliffs", (6.961424350738525, 2180.63232421875, 1431.8245849609375), (2670, 201306, 0), 0, 15, 0, 0, [False, False, False], "A30 Thousand Cuts Mobbing 1.json"),
        MapData("Thousand Cuts", "grass_cliffs_p", "GD_FastTravelStations.Zone2.Cliffs", (-15702.89453125, -9687.87890625, 1105.021728515625), (65170, 85310, 0), 0, 10, 0, 0, [False, False, False], "A31 Thousand Cuts Mobbing 2.json"),
        MapData("Thousand Cuts", "grass_cliffs_p", "GD_FastTravelStations.Zone2.Cliffs", (-26032.58203125, -9602.2578125, 1815.5933837890625), (506, 33266, 0), 0, 10, 0, 0, [False, False, False], "A32 Thousand Cuts Mobbing 3.json"),
        MapData("Lynchwood", "grass_lynchwood_p", "GD_FastTravelStations.Interlude.Lynchwood", (6430.12255859375, 4772.53955078125, 817.9797973632812), (65109, 17207, 0), 0, 10, 0, 0, [False, False, False], "A33 Lynchwood Mobbing 1.json", False, "", False, False),
        MapData("Lynchwood", "grass_lynchwood_p", "GD_FastTravelStations.Interlude.Lynchwood", (11911.0625, -19135.705078125, -3343.85009765625), (65287, 146673, 0), 0, 15, 0, 0, [False, False, False], "A34 Lynchwood Mobbing 2.json"),
        MapData("Lynchwood", "grass_lynchwood_p", "GD_FastTravelStations.Interlude.Lynchwood", (20030.673828125, -11784.8408203125, -2678.77734375), (63558, 105196, 0), 0, 15, 0, 0, [False, False, False], "A35 Lynchwood Mobbing 3.json"),
        MapData("Opportunity", "hyperioncity_p", "GD_FastTravelStations.Zone2.HyperionCity", (14384.1962890625, -3451.92041015625, 1176.3221435546875), (84, -28488, 0), 0, 10, 0, 0, [False, False, False], "A36 Opportunity Mobbing 1.json"),
        MapData("Opportunity", "hyperioncity_p", "GD_FastTravelStations.Zone2.HyperionCity", (16949.87109375, 3181.3193359375, 1943.8834228515625), (65261, 24522, 0), 0, 10, 0, 0, [False, False, False], "A37 Opportunity Mobbing 2.json", False, "", False, False),
        MapData("Opportunity", "hyperioncity_p", "GD_FastTravelStations.Zone2.HyperionCity", (3594.867919921875, 14916.7060546875, -300.8500061035156), (85, -48333, 0), 0, 15, 0, 0, [False, False, False], "A38 Opportunity Mobbing 3.json"),
        MapData("Opportunity", "hyperioncity_p", "GD_FastTravelStations.Zone2.HyperionCity", (9621.7373046875, -983.3734741210938, 1751.8094482421875), (136, -54991, 0), 0, 10, 0, 0, [False, False, False], "A39 Opportunity Mobbing 4.json"),
        MapData("Eridium Blights", "ash_p", "GD_FastTravelStations.Zone3.Ash", (40934.25390625, -28454.390625, -1997.64990234375), (65380, 193151, 0), 0, 10, 0, 0, [False, False, False], "A40 Eridium Blights Mobbing 1.json"),
        MapData("Eridium Blights", "ash_p", "GD_FastTravelStations.Zone3.Ash", (23827.607421875, -48207.56640625, 1590.76220703125), (1, 103198, 0), 0, 10, 0, 0, [False, False, False], "A41 Eridium Blights Mobbing 2.json"),
        MapData("Eridium Blights", "ash_p", "GD_FastTravelStations.Zone3.Ash", (-12131.5712890625, -8331.513671875, -2537.83251953125), (65381, -48982, 0), 0, 10, 0, 0, [False, False, False], "A42 Eridium Blights Mobbing 3.json"),
        MapData("Sawtooth Cauldron", "craterlake_p", "GD_FastTravelStations.Zone3.CraterLake", (7455.65283203125, 29509.123046875, 1313.012451171875), (1767, -15053, 0), 0, 15, 0, 0, [False, False, False], "A43 Sawtooth Cauldron Mobbing 1.json"),
        MapData("Sawtooth Cauldron", "craterlake_p", "GD_FastTravelStations.Zone3.CraterLake", (22380.060546875, 35432.13671875, 5278.49365234375), (65472, -1694, 0), 0, 10, 0, 0, [False, False, False], "A44 Sawtooth Cauldron Mobbing 2.json"),
        MapData("Sawtooth Cauldron", "craterlake_p", "GD_FastTravelStations.Zone3.CraterLake", (24532.666015625, 33943.19140625, 1620.5882568359375), (64267, 32561, 0), 0, 10, 0, 0, [False, False, False], "A45 Sawtooth Cauldron Mobbing 3.json"),
        MapData("Sawtooth Cauldron", "craterlake_p", "GD_FastTravelStations.Zone3.CraterLake", (11594.37890625, 12318.0322265625, 3882.158935546875), (65291, 41026, 0), 0, 15, 0, 0, [False, False, False], "A46 Sawtooth Cauldron Mobbing 4.json"),
        MapData("Arid Nexus Boneyard", "fyrestone_p", "GD_FastTravelStations.Zone3.OnFireStone", (-48338.97265625, 46482.90234375, -5034.14990234375), (65524, -98136, 0), 0, 10, 0, 0, [False, False, False], "A47 Arid Nexus Boneyard Mobbing 1.json"),
        MapData("Arid Nexus Boneyard", "fyrestone_p", "GD_FastTravelStations.Zone3.OnFireStone", (-57963.4375, 45556.203125, -1840.73388671875), (606, 180497, 0), 0, 10, 0, 0, [False, False, False], "A48 Arid Nexus Boneyard Mobbing 2.json"),
        MapData("Arid Nexus Boneyard", "fyrestone_p", "GD_FastTravelStations.Zone3.OnFireStone", (-48762.90234375, 26324.232421875, -2450.43798828125), (116, 84343, 0), 0, 10, 0, 0, [False, False, False], "A49 Arid Nexus Boneyard Mobbing 3.json", False, "", False, True),
        MapData("Arid Nexus Boneyard", "fyrestone_p", "GD_FastTravelStations.Zone3.OnFireStone", (-50252.9296875, 13006.9541015625, -2795.663818359375), (65471, 65700, 0), 0, 15, 0, 0, [False, False, False], "A50 Arid Nexus Boneyard Mobbing 4.json"),
        MapData("Arid Nexus Badlands", "stockade_p", "GD_FastTravelStations.FyrestoneOneWay", (-20271.205078125, 22251.921875, 604.0128173828125), (64776, -22548, 0), 0, 10, 0, 0, [False, False, False], "A51 Arid Nexus Badlands Mobbing 1.json"),
        MapData("Arid Nexus Badlands", "stockade_p", "GD_FastTravelStations.FyrestoneOneWay", (-21742.6953125, 41026.40234375, 857.916015625), (64628, -74794, 0), 0, 15, 0, 0, [False, False, False], "A52 Arid Nexus Badlands Mobbing 2.json", False, "", False, True),
        MapData("Arid Nexus Badlands", "stockade_p", "GD_FastTravelStations.FyrestoneOneWay", (-18066.896484375, 32032.056640625, 93.77349090576172), (26, -197349, 0), 0, 10, 0, 0, [False, False, False], "A53 Arid Nexus Badlands Mobbing 3.json"),
        MapData("Arid Nexus Badlands", "stockade_p", "GD_FastTravelStations.FyrestoneOneWay", (-21274.212890625, 24512.05859375, 443.664794921875), (664, 155437, 0), 0, 10, 0, 0, [False, False, False], "A54 Arid Nexus Badlands Mobbing 4.json", False, "", False, True),
        MapData("Hero's Pass", "finalbossascent_p", "GD_FastTravelStations.Zone3.FinalBossAscent", (-3977.930908203125, 18863.658203125, 6201.87451171875), (65489, 4150, 0), 0, 15, 0, 0, [False, False, False], "A55 Hero's Pass Mobbing 1.json"),
        MapData("Oasis", "orchid_oasistown_p", "GD_Orchid_FastTravel.OasisTown.OasisTown", (-15936.5380859375, 31653.49609375, 6303.7724609375), (64657, -37474, 0), 0, 15, 0, 0, [False, False, False], "A56 Oasis Mobbing 1.json"),
        MapData("Oasis", "orchid_oasistown_p", "GD_Orchid_FastTravel.OasisTown.OasisTown", (-33996.10546875, 37693.46875, 3580.158447265625), (309, 15681, 0), 0, 10, 0, 0, [False, False, False], "A57 Oasis Mobbing 2.json"),
        MapData("Oasis", "orchid_oasistown_p", "GD_Orchid_FastTravel.OasisTown.OasisTown", (20468.0625, -10430.4677734375, 7889.849609375), (64568, 168792, 0), 0, 10, 0, 0, [False, False, False], "A58 Oasis Mobbing 3.json"),
        MapData("Wurmwater", "orchid_saltflats_p", "GD_Orchid_FastTravel.SaltFlats.SaltFlats", (-49689.453125, -32373.68359375, 2894.479436328125), (64809, -1870, 0), 0, 10, 0, 0, [False, False, False], "A59 Wurmwater Mobbing 1.json"),
        MapData("Wurmwater", "orchid_saltflats_p", "GD_Orchid_FastTravel.SaltFlats.SaltFlats", (47723.921875, 4043.66455078125, -830.6511840820312), (25, -56098, 0), 0, 15, 0, 0, [False, False, False], "A60 Wurmwater Mobbing 2.json"),
        MapData("Wurmwater", "orchid_saltflats_p", "GD_Orchid_FastTravel.SaltFlats.SaltFlats", (-27364.87890625, 32095.203125, 2214.000732421875), (401, -103430, 0), 0, 10, 0, 0, [False, False, False], "A61 Wurmwater Mobbing 3.json", False, "", False, True),
        MapData("Wurmwater", "orchid_saltflats_p", "GD_Orchid_FastTravel.SaltFlats.SaltFlats", (43722.984375, -57726.26171875, 3973.85009765625), (65532, -34763, 0), 0, 10, 0, 0, [False, False, False], "A62 Wurmwater Mobbing 4.json"),
        MapData("Hater's Folley", "orchid_caves_p", "GD_Orchid_FastTravel.Caves", (1670.505615234375, 6664.62744140625, -4081.461181640625), (65488, 59600, 0), 0, 15, 0, 0, [False, False, False], "A63 Hater's Folley Mobbing 1.json", False, "", False, True),
        MapData("Hater's Folley", "orchid_caves_p", "GD_Orchid_FastTravel.Caves", (-7181.837890625, -8138.18359375, -3163.651123046875), (65212, 36924, 0), 0, 15, 0, 0, [False, False, False], "A64 Hater's Folley Mobbing 2.json"),
        MapData("The Rustyards", "orchid_shipgraveyard_p", "GD_Orchid_FastTravel.ShipGraveyard", (-24880.8671875, 21464.701171875, -1668.159912109375), (2457, -22634, 0), 0, 15, 0, 0, [False, False, False], "A65 The Rustyards Mobbing 1.json"),
        MapData("The Rustyards", "orchid_shipgraveyard_p", "GD_Orchid_FastTravel.ShipGraveyard", (-12638.400390625, 5867.021484375, 1059.1500244140625), (431, 4478, 0), 0, 10, 0, 0, [False, False, False], "A66 The Rustyards Mobbing 2.json"),
        MapData("The Rustyards", "orchid_shipgraveyard_p", "GD_Orchid_FastTravel.ShipGraveyard", (26319.216796875, 15915.7138671875, -1423.570556640625), (65360, 45004, 0), 0, 15, 0, 0, [False, False, False], "A67 The Rustyards Mobbing 3.json"),
        MapData("The Rustyards", "orchid_shipgraveyard_p", "GD_Orchid_FastTravel.ShipGraveyard", (10339.5595703125, 3632.4501953125, 2005.105712890625), (445, 36801, 0), 0, 10, 0, 0, [False, False, False], "A68 The Rustyards Mobbing 4.json", False, "", False, True),
        MapData("Washburne Refinery", "orchid_refinery_p", "GD_Orchid_FastTravel.Refinary", (30749.814453125, -15067.6279296875, 1203.935791015625), (64837, -65386, 0), 0, 10, 0, 0, [False, False, False], "A69 Washburne Refinery Mobbing 1.json", False, "", False, True), # nice
        MapData("Washburne Refinery", "orchid_refinery_p", "GD_Orchid_FastTravel.Refinary", (45688.4453125, -13724.599609375, 1523.1500244140625), (65392, 18777, 0), 0, 15, 0, 0, [False, False, False], "A70 Washburne Refinery Mobbing 2.json", False, "", False, True),
        MapData("Magnys Lighthouse", "orchid_spire_p", "GD_Orchid_FastTravel.Spire", (-15461.859375, -3712.231689453125, 2030.6749267578125), (65254, -64733, 0), 0, 10, 0, 0, [False, False, False], "A71 Magny's Lighthouse Mobbing 1.json"),
        MapData("Badass Crater", "iris_hub_p", "GD_Iris_FastTravelStations.Hub.IrisCrater", (21087.29296875, 11995.4599609375, -1240.1502685546875), (273, -124104, 0), 0, 15, 0, 0, [False, False, False], "A72 Badass Crater Mobbing 1.json"),
        MapData("The Forge", "iris_dl3_p", "GD_Iris_FastTravelStations.Forge", (37433.8828125, 14833.42578125, 1076.7711181640625), (64979, -97664, 0), 0, 10, 0, 0, [False, False, False], "A73 The Forge Mobbing 1.json"),
        MapData("The Forge", "iris_dl3_p", "GD_Iris_FastTravelStations.Forge", (22206.51953125, 25316.26953125, 1805.8538818359375), (65515, 37859, 0), 0, 15, 0, 0, [False, False, False], "A74 The Forge Mobbing 2.json"),
        MapData("The Forge", "iris_dl3_p", "GD_Iris_FastTravelStations.Forge", (49680.015625, 21373.693359375, -144.39321899414062), (76, -65187, 0), 0, 15, 0, 0, [False, False, False], "A75 The Forge Mobbing 3.json"),
        MapData("The Forge", "iris_dl3_p", "GD_Iris_FastTravelStations.Forge", (26545.08203125, 12437.669921875, 1541.0233154296875), (159, 72831, 0), 0, 10, 0, 0, [False, False, False], "A76 The Forge Mobbing 4.json", False, "", False, True),
        MapData("Ardortion Station", "sage_powerstation_p", "GD_Sage_FastTravel.PowerStation", (-23703.1593125, -12586.6748046875, 3166.949951171875), (65458, 29914, 0), 0, 10, 0, 0, [False, False, False], "A77 Ardorton Station Mobbing 1.json", False, "", False, False),
        MapData("Unassuming Docks", "docks_p", "GD_Aster_FastTravel.Docks", (14692.53125, -11302.1376953125, -10992.828125), (484, 26541, 0), 0, 10, 0, 0, [False, False, False], "A78 Unassuming Docks Mobbing 1.json"),
        MapData("Immortal Woods", "dead_forest_p", "GD_Aster_FastTravel.DeadForest", (-13430.66796875, -23158.68359375, -9545.1796875), (65512, -98125, 0), 0, 15, 0, 0, [False, False, False], "A79 Immortal Woods Mobbing 1.json"),
        MapData("Mines of Avarice", "mines_p", "GD_Aster_FastTravel.Mines", (-24774.951171875, -14707.3115234375, -2820.1279296875), (730, -37797, 0), 0, 10, 0, 0, [False, False, False], "A80 Mines Of Avarice Mobbing 1.json"),
        MapData("Lair of Infinite Agony", "dungeon_p", "GD_Aster_FastTravel.Dungeons", (2939.875244140625, 3216.75341796875, 6105.6552734375), (65445, -85115, 0), 0, 10, 0, 0, [False, False, False], "A81 Lair Of Infinite Agony Mobbing 1.json"),
        ],
    MapType.MiniBoss:[
        MapData("Boom & Bewm", "southernshelf_p", "GD_FastTravelStations.Zone1.SouthernShelfTown", (41634.8359375, -26136.025390625, 740.4281616210938), (2061, -64180, 0), 0, 12, 0, 2, [["AIClassDefinition GD_BoomBoom.Character.CharClass_Boom", "AIClassDefinition GD_BoomBoom.Character.CharClass_BoomBoom"], "Beer Bottles", 0, False, False], "B1 Boom + Bewm Mini Boss.json"),
        MapData("Assassin Wot", "southpawfactory_p", "GD_FastTravelStations.Zone1.SouthpawFactory", (-4594.017578125, 21639.896484375, -6062.24609375), (140, 3487, 0), 0, 8, 0, 1, [["AIClassDefinition GD_Assassin1.Character.CharClass_Assassin1"], "Psycho Masks", 0, False, False], "B2 Wot Mini Boss.json"),
        MapData("Assassin Oney", "southpawfactory_p", "GD_FastTravelStations.Zone1.SouthpawFactory", (-4591.6494140625, 26944.0859375, -5509.685546875), (65420, 12287, 0), 0, 10, 0, 1, [["AIClassDefinition GD_Assassin2.Character.CharClass_Assassin2"], "Oil Cans", 0, False, False], "B3 Oney Mini Boss.json"),
        MapData("Assassin Reeth", "southpawfactory_p", "GD_FastTravelStations.Zone1.SouthpawFactory", (1937.488037109375, 26544.328125, -6476.8623046875), (123, 32792, 0), 0, 10, 0, 1, [["AIClassDefinition GD_Assassin3.Character.CharClass_Assassin3"], "Tires", 0, False, False], "B4 Reeth Mini Boss.json"),
        MapData("Assassin Rouf", "southpawfactory_p", "GD_FastTravelStations.Zone1.SouthpawFactory", (-8973.576171875, 23892.111328125, -6224.85009765625), (720, -8352, 0), 0, 15, 0, 1, [["AIClassDefinition GD_Assassin4.Character.CharClass_Assassin4"], "Buckets", 0, False, False], "B5 Rouf Mini Boss.json"),
        MapData("Mad Mike", "dam_p", "GD_FastTravelStations.Zone1.GoshDam", (-3634.196044921875, 8714.2734375, -929.135986328125), (63560, -486, 0), 0, 15, 0, 1, [["AIClassDefinition GD_Prospector.Character.CharClass_Prospector"], "Televisions", 0, False, False], "B6 Mad Mike Mini Boss.json"),
        MapData("Mortar", "craterlake_p", "GD_FastTravelStations.Zone3.CraterLake", (16878.5703125, 19743.271484375, 1578.757080078125), (64241, 75935, 0), 0, 8, 0, 1, [["AIClassDefinition GD_Mortar.Character.CharClass_Mortar"], "Medicine Bottles", 0, False, False], "B7 Mortar Mini Boss.json"),
        MapData("Bloodtail", "sage_cliffs_p", "GD_Sage_FastTravel.SageCliffs", (75807.375, -15136.673828125, -10006.046875), (63516, -9646, 0), 0, 10, 0, 1, [["AIClassDefinition GD_Sage_SM_NowYouSeeItData.Creature.CharClass_Sage_NowYouSeeIt_Creature"], "Drifter Eggs", 0, False, False], "B8 Bloodtail Mini Boss.json"),
        MapData("Big Sleep & Sandman", "orchid_caves_p", "GD_Orchid_FastTravel.Caves", (-16544.802734375, 3040.375244140625, -2008.9376220703125), (199, 58874, 0), 0, 8, 0, 2, [["AIClassDefinition GD_Orchid_Master.Character.CharClass_Orchid_MarauderMaster", "AIClassDefinition GD_Orchid_BigSleep.Character.CharClass_Orchid_BigSleep"], "Shovels", 0, False, False], "B9 Big Sleep + Sandman Mini Boss.json"),
        MapData("Incinerator Clayton", "icecanyon_p", "GD_FastTravelStations.Zone1.IceCanyon", (-8565.5869140625, -11110.86328125, 1965.44775390625), (62893, -4907, 0), 0, 15, 0, 1, [["AIClassDefinition GD_IncineratorVanya_Combat.Character.CharClass_IncineratorVanya_Combat"], "Radios", 0, False, False], "B10 Incinerator Clayton Mini Boss.json"),
        MapData("Rakkman", "fridge_p", "GD_FastTravelStations.Zone2.TheFridge", (1667.0147705078125, 7437.67626953125, 10611.0634765625), (63583, 196317, 0), 0, 12, 0, 1, [["AIClassDefinition GD_RakkMan.Character.CharClass_RakkMan"], "Brains", 0, False, False], "B11 Rakkman Mini Boss.json"),
        MapData("Mad Dog", "grass_lynchwood_p", "GD_FastTravelStations.Interlude.Lynchwood", (-12474.6533203125, -25261.40234375, -159.25877380371094), (408, 114800, 0), 0, 10, 0, 1, [["AIClassDefinition GD_MadDog.Character.CharClass_MadDog"], "Tina Bombs", 0, False, False], "B12 Mad Dog Mini Boss.json"),
        MapData("Spycho", "icecanyon_p", "GD_FastTravelStations.Zone1.IceCanyon", (-2045.6678466796875, 18266.212890625, 1368.5540771484375), (53, -18414, 0), 0, 10, 0, 1, [["AIClassDefinition gd_monstermash1.Character.CharClass_MonsterMash1"], "Banjos", 0, False, False], "B13 Spycho Mini Boss.json"),
        MapData("Bone Head 2.0", "stockade_p", "GD_FastTravelStations.FyrestoneOneWay", (-11263.3486328125, 25994.7421875, 379.73516845703125), (65118, 1293, 0), 0, 4, 0, 1, [["AIClassDefinition GD_BoneHead2.Character.CharClass_BoneHead2"], "Skulls", 0, False, False], "B14 Bone Head 2.0 Mini Boss.json"),
        ], 
    MapType.RedBarBoss:[
        MapData("Captain Flynt", "southernshelf_p", "GD_FastTravelStations.Zone1.SouthernShelfTown", (66685.0625, -44549.8125, 6929.82275390625), (65497, -56928, 0), 0, 0, 0, 1, [["AIClassDefinition GD_Flynt.Character.CharClass_Flynt"]], "C1 Captain Flynt Boss.json"),
        MapData("Doc Mercy", "frost_p", "GD_FastTravelStations.Zone1.IceWest", (3241.085205078125, 4407.25537109375, 3136.1376953125), (1570, 1195, 0), 0, 0, 0, 1, [["AIClassDefinition GD_MrMercy.Character.CharClass_MrMercy"]], "C2 Doc Mercy Boss.json"),
        MapData("Scorch", "icecanyon_p", "GD_FastTravelStations.Zone1.IceCanyon", (-11238.3359375, 16298.080078125, -544.4419555664062), (927, -155650, 0), 0, 0, 0, 1, [["AIClassDefinition GD_SpiderantScorch.Character.CharClass_SpiderantScorch"]], "C3 Scorch Boss.json"),
        MapData("Smash Head", "fridge_p", "GD_FastTravelStations.Zone2.TheFridge", (-7792.41748046875, 8808.92578125, 10670.3828125), (606, -8167, 0), 0, 0, 0, 1, [["AIClassDefinition gd_bluntcrack.Character.CharClass_BluntCrack"]], "C4 Smash-Head Boss.json"),
        #MapData("Motor Mama", "iris_hub2_p", "GD_Iris_FastTravelStations.SouthernRaceway", (-42478.54296875, 43019.8984375, -4666.150390625), (55, 61813, 0), 0, 0, 0, 1, [["AIClassDefinition GD_Iris_MotorMama.Character.CharClass_Iris_MotorMama"]], "C5 Motor Mama Boss.json"), # rest in piss
        MapData("Sorcerer's Daughter", "dungeon_p", "GD_Aster_FastTravel.Dungeons", (21.008975982666016, -17616.1796875, 4077.85009765625), (607, -16326, 0), 0, 0, 0, 1, [["AIClassDefinition GD_AngelBoss.Character.CharClass_AngelBoss"]], "C6 Sorcerer's Daughter Boss.json"),
        MapData("Gold Golem", "mines_p", "GD_Aster_FastTravel.Mines", (-15005.345703125, 26002.318359375, -7283.15234375), (30, -49001, 0), 0, 0, 0, 1, [["AIClassDefinition GD_GolemGold.Character.CharClass_GolemGold"]], "C7 Gold Golem Boss.json"),
        MapData("Uranus", "helios_p", "GD_Anemone_FastTravel.FastTravelStations.Helios", (37449.6171875, -106473.125, 17807.001953125), (65317, 59284, 0), 0, 0, 0, 1, [["AIClassDefinition GD_Anemone_UranusBOT.Character.CharClass_Anemone_UranusBOT"]], "C8 Uranus Boss.json"),
        MapData("Handsome Sorcerer", "castlekeep_p", "GD_Aster_FastTravel.CastleKeep", (137157.03125, -14321.9853515625, 135194.421875), (1206, 98132, 0), 0, 0, 0, 3, [["AIClassDefinition GD_JackWarlock.Character.CharClass_JackWarlock"]], "C9 Handsome Sorcerer Boss.json"),
        MapData("Wattle Gobbler", "hunger_p", "GD_Allium_FastTravel.Hunger", (-1250.6363525390625, -5547.27587890625, -7716.1259765625), (65501, -6073, 0), 0, 0, 0, 1, [["AIClassDefinition GD_BigBird.Character.CharClass_BigBird"]], "C10 Wattle Gobbler Boss.json"),
        MapData("Cassius", "researchcenter_p", "GD_Anemone_FastTravel.ResearchCenter_OneWay", (1040.9761962890625, 79.00605773925781, 4415.77734375), (49, 32705, 0), 0, 0, 0, 1, [["AIClassDefinition GD_Anemone_Cassius.Character.CharClass_Anemone_Cassius"]], "C11 Cassius Boss.json"),
        MapData("Saturn", "stockade_p", "GD_FastTravelStations.FyrestoneOneWay", (-9582.171875, 45400.71484375, 144.2803497314453), (65142, -67981, 0), 0, 0, 0, 1, [["AIClassDefinition GD_LoaderUltimateBadass.Character.CharClass_LoaderUltimateBadass"]], "C12 Saturn Boss.json"),
        MapData("Tinder Snowflake", "xmas_p", "GD_Allium_FastTravel.Xmas", (9787.7880859375, 798.6428833007812, 168.18917846679688), (65267, 8343, 0), 0, 0, 0, 1, [["AIClassDefinition GD_Snowman.Character.CharClass_Snowman"]], "C13 Tinder Snowflake Boss.json"),
        MapData("Happy Couple", "distillery_p", "GD_Nasturtium_FastTravel.Vday", (-34599.7109375, -7409.6845703125, 3277.45849609375), (214, 57442, 0), 0, 0, 0, 1, [["AIClassDefinition GD_GoliathGroom.Character.CharClass_GoliathGroom", "AIClassDefinition GD_GoliathBride.Character.CharClass_GoliathBride"]], "C14 Happy Couple Boss.json"),
        MapData("Wilhelm", "tundratrain_p", "GD_FastTravelStations.Wilhelm", (-44454.515625, 35651.66015625, 2073.850341796875), (542, -3129, 0), 0, 0, 0, 1, [["AIClassDefinition GD_Willhelm.Character.CharClass_Willhelm"]], "C15 Wilhelm Boss.json"),
        ], 
    MapType.RaidBoss:[
        MapData("Pyro Pete", "iris_dl2_interior_p", "GD_Iris_LevelTravelStations.PyroPeteToBeatdown", (319.1189270019531, -7810.9814453125, -7444.849609375), (65526, -40119, 0), 0, 0, 0, 1, [["AIClassDefinition GD_Iris_Raid_PyroPete.Character.CharClass_Iris_Raid_PyroPete"]], "D1 Pete Raid Boss.json"),
        MapData("Hyperius", "orchid_refinery_p", "GD_Orchid_FastTravel.Refinary", (37024.70703125, 4878.318359375, 2070.233154296875), (319, 25381, 0), 0, 0, 0, 1, [["AIClassDefinition GD_Orchid_RaidEngineer.Character.CharClass_Orchid_RaidEngineer"]], "D2 Hyperius Raid Boss.json"),
        MapData("Terramorphous", "thresherraid_p", "GD_LevelTravelStations.Zone2.ThresherRaidToCliffs", (-28635.990234375, 11633.3876953125, 2376.100341796875), (1765, 83293, 0), 0, 0, 0, 1, [["AIClassDefinition GD_Thresher_Raid.Character.CharClass_Thresher_Raid"]], "D3 Terramorphous Raid Boss.json"),
        MapData("Son of Crawmerax", "easter_p", "GD_Nasturtium_FastTravel.EasterTravel", (41317.0859375, 2786.37353515625, -3388.067626953125), (745, -61962, 0), 0, 0, 0, 1, [["AIClassDefinition GD_Crawmerax_Son.Character.CharClass_Crawmerax_Son"]], "D4 Son of Craw Raid Boss.json"),
        ],
    MapType.MiniGame:[
        MapData("Reach Buttstallion", "sage_rockforest_p", "GD_Sage_FastTravel.RockForest", (24800.384765625, -52369.7890625, 12577.9189453125), (65385, 32970, 0), 0, 99999, 0, 0, [(24409.185546875, -48907.15625, 12583.9189453125), False], "E1A Scyllas Grove Hidden Lever 1.json", False, "Find The Lever", False),
        MapData("Reach Buttstallion", "sage_rockforest_p", "GD_Sage_FastTravel.RockForest", (24800.384765625, -52369.7890625, 12577.9189453125), (65385, 32970, 0), 0, 99999, 0, 0, [(24409.185546875, -48907.15625, 12583.9189453125), False], "E1B Scyllas Grove Hidden Lever 2.json", False, "Find The Lever", False),
        MapData("Reach Buttstallion", "sage_rockforest_p", "GD_Sage_FastTravel.RockForest", (24800.384765625, -52369.7890625, 12577.9189453125), (65385, 32970, 0), 0, 99999, 0, 0, [(24409.185546875, -48907.15625, 12583.9189453125), False], "E1C Scyllas Grove Hidden Lever 3.json", False, "Find The Lever", False),
        MapData("Reach Buttstallion", "iris_moxxi_p", "GD_Iris_FastTravelStations.BadassBar", (32178.732421875, -735.8997802734375, 4072.61572265625), (64691, -16291, 0), 0, 99999, 0, 0, [(32196.09765625, -2513.668701171875, 4072.01171875), False, False, False, False, False, False, False, False, False, False], "E2A Crater Bar Glass Floor 1.json", False, "Reach Buttstallion", False),
        MapData("Reach Buttstallion", "iris_moxxi_p", "GD_Iris_FastTravelStations.BadassBar", (32178.732421875, -735.8997802734375, 4072.61572265625), (64691, -16291, 0), 0, 99999, 0, 0, [(32196.09765625, -2513.668701171875, 4072.01171875), False, False, False, False, False, False, False, False, False, False], "E2B Crater Bar Glass Floor 2.json", False, "Reach Buttstallion", False),
        MapData("Reach Buttstallion", "iris_moxxi_p", "GD_Iris_FastTravelStations.BadassBar", (32178.732421875, -735.8997802734375, 4072.61572265625), (64691, -16291, 0), 0, 99999, 0, 0, [(32196.09765625, -2513.668701171875, 4072.01171875), False, False, False, False, False, False, False, False, False, False], "E2C Crater Bar Glass Floor 3.json", False, "Reach Buttstallion", False),
        MapData("Find Buttstallion", "glacial_p", "GD_FastTravelStations.Zone1.GlacialIgloo", (13090.2421875, 39381.95703125, 11546.41796875), (65291, -35307, 0), 0, 99999, 0, 0, [(10564.64453125, 40098.37890625, 11552.41796875)], "E3A Windshear Maze 1.json", False, "Find Buttstallion!", False),
        MapData("Find Buttstallion", "glacial_p", "GD_FastTravelStations.Zone1.GlacialIgloo", (12182.6611328125, 39888.03125, 11546.41796875), (65271, 109348, 0), 0, 99999, 0, 0, [(11046.95703125, 37776.9140625, 11552.41796875)], "E3B Windshear Maze 2.json", False, "Find Buttstallion!", False),
        MapData("Find Buttstallion", "glacial_p", "GD_FastTravelStations.Zone1.GlacialIgloo", (11080.220703125, 37911.7265625, 11546.41796875), (65231, -58989, 0), 0, 99999, 0, 0, [(13058.697265625, 39488.93359375, 11552.41796875)], "E3C Windshear Maze 3.json", False, "Find Buttstallion!", False),
        MapData("Error F1nD BuTTSta11i0n", "dark_forest_p", "GD_Aster_FastTravel.DarkForest", (3166.709228515625, -23734.240234375, -2337.60205078125), (65447, -36224, 0), 0, 99999, 0, 0, [(1954.9144287109375, -21409.3125, -2331.60205078125)], "E4A Forest Glitch 1.json", False, "Find the Real Buttstallion", False),
        MapData("Error F1nD BuTTSta11i0n", "dark_forest_p", "GD_Aster_FastTravel.DarkForest", (3166.709228515625, -23734.240234375, -2337.60205078125), (65447, -36224, 0), 0, 99999, 0, 0, [(906.675048828125, -23034.9453125, -2265.29443359375)], "E4B Forest Glitch 2.json", False, "Find the Real Buttstallion", False),
        MapData("Error F1nD BuTTSta11i0n", "dark_forest_p", "GD_Aster_FastTravel.DarkForest", (3166.709228515625, -23734.240234375, -2337.60205078125), (65447, -36224, 0), 0, 99999, 0, 0, [(1117.9180908203125, -21613.951171875, -1971.1300048828125)], "E4C Forest Glitch 3.json", False, "Find the Real Buttstallion", False),
        MapData("Reach Buttstallion", "dungeon_p", "GD_Aster_FastTravel.Dungeons", (-5458.9794921875, 2980.408935546875, 557.5320434570312), (1280, -98333, 0), 0, 9999, 0, 0, [(-17931.072265625, 1417.010009765625, -12.561384201049805), False, False, False], "E5A Lair of Infinite Agony Puzzle Rooms 1.json", False, "Reach Buttstallion!", False),
        MapData("Reach Buttstallion", "dungeon_p", "GD_Aster_FastTravel.Dungeons", (-5920.673828125, 3041.10498046875, 545.7273559570312), (1280, -98333, 0), 0, 9999, 0, 0, [(-17931.072265625, 1417.010009765625, -12.561384201049805), False, False, False], "E5B Lair of Infinite Agony Puzzle Rooms 2.json", False, "Reach Buttstallion!", False),
        MapData("Reach Buttstallion", "dungeon_p", "GD_Aster_FastTravel.Dungeons", (-5920.673828125, 3041.10498046875, 545.7273559570312), (1280, -98333, 0), 0, 9999, 0, 0, [(-17931.072265625, 1417.010009765625, -12.561384201049805), False, False, False], "E5C Lair of Infinite Agony Puzzle Rooms 3.json", False, "Reach Buttstallion!", False),
        MapData("Complete Parkour", "hyperioncity_p", "GD_FastTravelStations.Zone2.HyperionCity", (47103.1015625, 22272.216796875, 1914.6287841796875), (65300, 103796, 0), 0, 35, 0, 0, [(44683.10546875, 20873.853515625, 2816.50634765625)], "E6 Opportunity (Parkour 1).json", False, "Climb!", False),
        MapData("Reach Buttstallion", "iris_dl2_p", "GD_Iris_FastTravelStations.Beatdown", (22996.02734375, -9467.2568359375, -4105.7646484375), (65471, -49212, 0), 0, 30, 0, 0, [(23045.16796875, -4900.4375, -4105.7646484375)], "E7A Beatdown Shifting Floors 1.json", False, "Reach Buttstallion!", False), # 3 variations
        MapData("Reach Buttstallion", "iris_dl2_p", "GD_Iris_FastTravelStations.Beatdown", (22996.02734375, -9467.2568359375, -4105.7646484375), (65471, -49212, 0), 0, 30, 0, 0, [(23045.16796875, -4900.4375, -4105.7646484375)], "E7B Beatdown Shifting Floors 2.json", False, "Reach Buttstallion!", False),
        MapData("Reach Buttstallion", "iris_dl2_p", "GD_Iris_FastTravelStations.Beatdown", (22996.02734375, -9467.2568359375, -4105.7646484375), (65471, -49212, 0), 0, 30, 0, 0, [(23045.16796875, -4900.4375, -4105.7646484375)], "E7C Beatdown Shifting Floors 3.json", False, "Reach Buttstallion!", False),
        #MapData("Find Buttstallion", "dam_p", "GD_FastTravelStations.Zone1.GoshDam", (-28915.439453125, 18473.8046875, 2108.46044921875), (64740, -58809, 0), 0, 99999, 0, 0, [(-28618.25390625, 19602.751953125, 2108.46044921875), False, False, False], "E8 Bloodshot Secret Rooms 1.json", False, "Break Out!", False),
        MapData("Reach Buttstallion", "testingzone_p", "GD_Lobelia_FastTravel.TestingZone", (38222.2734375, 48020.37109375, 6136.5380859375), (65355, -32000, 0), 0, 9999, 0, 0, [(36713.07421875, 47913.1953125, 6850.8193359375), False, False, False, False, False, 0], "E9 Digipeak Trivia Mini Game 1.json", False, "Trivia Time!", False),
        ],
    MapType.Special:[
        MapData("Golden Chest", "sanctuaryair_p", "GD_FastTravelStations.Sanctuary.Sanctuary", (-5116.1533203125, -16532.931640625, 2681.26904296875), (201, 98146, 0), 0, 0, 0, 0, ["yay a reward", False, False], "F1 Sanctuary (Gold Chest Room).json", False),
        MapData("Finish", "castleexterior_p", "GD_Aster_FastTravel.CastleExterior", (31115.2421875, 32096.10546875, 2115.923828125), (2778, 8103, 0), 0, 0, 0, 0, ["yay a reward?", False, False], "G1 Hatreds Shadow Victory Room.json", False),
        ],
    MapType.FinalBoss:[
        MapData("Ancient Dragons", "dungeonraid_p", "GD_Aster_LevelTravel.DungeonRaidToDungeon", (0.691972017288208, 713.7623901367188, 4205.14990234375), (145, 49069, 0), 0, 0, 0, 4, [["AIClassDefinition GD_DragonRed_Raid.Character.CharClass_DragonRed_Raid", "AIClassDefinition GD_DragonBlue_Raid.Character.CharClass_DragonBlue_Raid", "AIClassDefinition GD_DragonPurple_Raid.Character.CharClass_DragonPurple_Raid", "AIClassDefinition GD_DragonGreen_Raid.Character.CharClass_DragonGreen_Raid"]], "H1 Ancient Dragons Raid Boss.json"),
        MapData("???????????", "grass_lynchwood_p", "GD_FastTravelStations.Interlude.Lynchwood", (4153.42626953125, -23613.98828125, -3288.936767578125), (65296, -34234, 0), 0, 3, 0, 1, [["AIClassDefinition GD_Skagzilla.Character.CharClass_Skagzilla"], False, False, False], "H2 Secret Raid Boss.json"),
    ],
    MapType.StartRoom:[
        MapData("Starting Room", "orchid_wormbelly_p", "GD_Orchid_LevelTravel.WormBelly.WormBellyToOasisTown", (5813.95947265625, -45436.44140625, -4841.07470703125), (65215, 16584, 0), 0, 0, 0, 0, ["buh", False, False, False], "G2 Leviathans Lair Starting Room 1.json", False),
        MapData("Starting Room", "orchid_wormbelly_p", "GD_Orchid_LevelTravel.WormBelly.WormBellyToOasisTown", (5813.95947265625, -45436.44140625, -4841.07470703125), (65215, 16584, 0), 0, 0, 0, 0, ["buh", False, False, False], "G3 Leviathans Lair Starting Room 2.json", False),
        MapData("Starting Room", "orchid_wormbelly_p", "GD_Orchid_LevelTravel.WormBelly.WormBellyToOasisTown", (5813.95947265625, -45436.44140625, -4841.07470703125), (65215, 16584, 0), 0, 0, 0, 0, ["buh", False, False, False], "G4 Leviathans Lair Starting Room 3.json", False),
    ],
    MapType.Hoard:[
        MapData("Token of Wealth", "templeslaughter_p", "GD_Aster_LevelTravel.TempleOfSlaughterToVillage", (5122.0810546875, 17701.6484375, 3766.596435546875), (339, 107377, 0), 0, 25, 0, 0, [False], "J1 Murderlin's Temple Hoard Round.json", False),
        MapData("Token of Giving", "xmas_p", "GD_Allium_FastTravel.Xmas", (-5622.00048828125, -13358.798828125, 1642.35400390625), (65339, -116798, 0), 0, 25, 0, 0, [False], "J2 Frost Bottom Hoard Round.json", False),
        MapData("Token of Vitality", "easter_p", "GD_Nasturtium_FastTravel.EasterTravel", (5853.2470703125, -7339.46826171875, 2488.447021484375), (1582, -9622, 0), 0, 30, 0, 0, [False, False], "J3 Wam Bam Hoard Round.json", False),
    ],
}
# fmt: on


def reset_visited_maps(reset_raid_bosses: bool) -> None: # false
    if reset_raid_bosses:
        for the_map in MAP_DATA[MapType.Mobbing]:
            the_map.has_been_visited_in_current_rotation = False
            the_map.custom_map_data[0] = False
            the_map.custom_map_data[1] = False
            the_map.custom_map_data[2] = False
        for the_map in MAP_DATA[MapType.MiniBoss]:
            the_map.has_been_visited_in_current_rotation = False
            the_map.custom_map_data[2] = 0
            the_map.custom_map_data[3] = False
            the_map.custom_map_data[4] = False
        for the_map in MAP_DATA[MapType.RedBarBoss]:
            the_map.has_been_visited_in_current_rotation = False
        for the_map in MAP_DATA[MapType.Special]:
            the_map.has_been_visited_in_current_rotation = False
            the_map.custom_map_data[1] = False
            the_map.custom_map_data[2] = False
        for the_map in MAP_DATA[MapType.FinalBoss]:
            the_map.has_been_visited_in_current_rotation = False
        for the_map in MAP_DATA[MapType.RaidBoss]:
            the_map.has_been_visited_in_current_rotation = False
        for the_map in MAP_DATA[MapType.MiniGame]:
            the_map.has_been_visited_in_current_rotation = False
        for the_map in MAP_DATA[MapType.Hoard]:
            the_map.has_been_visited_in_current_rotation = False

    for minigame in MAP_DATA[MapType.MiniGame]:
        if minigame.map_file == "E8 Bloodshot Secret Rooms 1.json":
            # Reset the 3 breakable walls
            minigame.custom_map_data[1] = False
            minigame.custom_map_data[2] = False
            minigame.custom_map_data[3] = False
        elif minigame.map_file in ("E2A Crater Bar Glass Floor 1.json", "E2B Crater Bar Glass Floor 2.json", "E2C Crater Bar Glass Floor 3.json"):
            # Reset the 10 glass floors
            for i in range(1, 11):
                minigame.custom_map_data[i] = False
        elif minigame.map_file == "E9 Digipeak Trivia Mini Game 1.json":
            for i in range(1, 6):
                minigame.custom_map_data[i] = False
            minigame.custom_map_data[6] = 0
        elif minigame.map_file in ("E1A Scyllas Grove Hidden Lever 1.json", "E1B Scyllas Grove Hidden Lever 2.json", "E1C Scyllas Grove Hidden Lever 3.json"):
            # Reset levers
            minigame.custom_map_data[1] = False

    for the_map in MAP_DATA[MapType.StartRoom]:
        the_map.has_been_visited_in_current_rotation = False
        the_map.custom_map_data[1] = False
        the_map.custom_map_data[2] = False
        the_map.custom_map_data[3] = False
    for map in MAP_DATA[MapType.Special]:
        map.custom_map_data[1] = False
        map.custom_map_data[2] = False
    for map in MAP_DATA[MapType.Hoard]:
        map.custom_map_data[0] = False
    
    MAP_DATA[MapType.FinalBoss][1].custom_map_data[2] = False
    MAP_DATA[MapType.FinalBoss][1].custom_map_data[3] = False
    MAP_DATA[MapType.Hoard][2].custom_map_data[1] = False
