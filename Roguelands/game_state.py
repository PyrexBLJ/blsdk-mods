from .maps import MAP_DATA, MapData, MapType

from Mods.ModMenu import Keybind

DebugBind: Keybind = Keybind("Debug")
ResetRunBind: Keybind = Keybind("End Run On Death", "F1")
ClaimRewardBind: Keybind = Keybind("Continue to Next Map", "F2")
RespecBind: Keybind = Keybind("Respec Skill Points", "F3")


class _GameState:
    def __init__(self) -> None:
        self.map_type: MapType = MapType.StartRoom
        self.current_map: MapData = MAP_DATA[MapType.StartRoom][0]

        self.level_offset: int = 0

        self.mission_complete: bool = False
        self.mission_complete_sound_played: bool = False

        self.travel_timer: int = 3
        self.map_is_loaded: bool = False

    def reset(self, reset_level_offset: bool = False) -> None:
        self.current_map.bosses_killed = 0
        self.current_map.kill_challenge_count = 0

        self.mission_complete = False
        self.mission_complete_sound_played = False

        self.travel_timer = 3
        self.map_is_loaded = False

        if reset_level_offset:
            self.level_offset = 0
        self.map_type = MapType.StartRoom
        self.current_map = MAP_DATA[MapType.StartRoom][self.level_offset]


GameState: _GameState = _GameState()
