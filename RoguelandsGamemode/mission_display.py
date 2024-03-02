import threading
import time
from typing import List

import unrealsdk  # type: ignore

from .game_state import GameState, ClaimRewardBind
from .maps import MapType


def _cmd(command: str) -> None:
    unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand(command)


class MissionStuff:
    WorkingMissionName: str = "GD_Z1_ShootMeInTheFace.M_ShootMeInTheFace"
    Line1: str = "GD_Z1_ShootMeInTheFace.M_ShootMeInTheFace:ShootInFace"
    Line2: str = "GD_Z1_ShootMeInTheFace.M_ShootMeInTheFace:NotInTheArm"
    Line3: str = "GD_Z1_ShootMeInTheFace.M_ShootMeInTheFace:NotInTheLeg"
    Line4: str = "GD_Z1_ShootMeInTheFace.M_ShootMeInTheFace:NotInTheChest"

    @staticmethod
    def refresh_mission_display() -> None:
        mission_tracker: unrealsdk.UObject = unrealsdk.GetEngine().GetCurrentWorldInfo().GRI.MissionTracker
        mission_tracker.ActiveMission = unrealsdk.FindObject("MissionDefinition", "WillowGame.Default__MissionDefinition")
        time.sleep(0.1)
        mission_tracker.ActiveMission = unrealsdk.FindObject("MissionDefinition", "GD_Z1_ShootMeInTheFace.M_ShootMeInTheFace")

    @staticmethod
    def set_mission_name(text: str) -> None:
        _cmd(
            f"set {MissionStuff.WorkingMissionName} MissionName {text}",
        )

    @staticmethod
    def set_objective_text(forceupdate: bool, objective: str, text: str) -> None:
        _cmd(f"set {objective} ProgressMessage {text}")

        if forceupdate:
            threading.Thread(target=MissionStuff.refresh_mission_display).start()

    @staticmethod
    def set_objective_required(objective_line: str) -> None:
        _cmd(f"set {objective_line} bObjectiveIsOptional False")

    @staticmethod
    def set_number_of_objectives(count: int) -> None:
        objectives: List[str] = [
            "MissionObjectiveDefinition'GD_Z1_ShootMeInTheFace.M_ShootMeInTheFace:ShootInFace'",
            "MissionObjectiveDefinition'GD_Z1_ShootMeInTheFace.M_ShootMeInTheFace:NotInTheArm'",
            "MissionObjectiveDefinition'GD_Z1_ShootMeInTheFace.M_ShootMeInTheFace:NotInTheLeg'",
            "MissionObjectiveDefinition'GD_Z1_ShootMeInTheFace.M_ShootMeInTheFace:NotInTheChest'",
        ]
        command: str = f"set GD_Z1_ShootMeInTheFace.M_ShootMeInTheFace:ShootMeInTheFaceSet ObjectiveDefinitions ({','.join(objectives[:count])})"
        _cmd(command)


def update_mission_display() -> None:
    if GameState.map_type == MapType.Mobbing:
        MissionStuff.set_objective_text(
            False,
            MissionStuff.Line1,
            f"Kill Enemies: {GameState.current_map.kill_challenge_count} / {GameState.current_map.kill_challenge_goal}",
        )
        if not GameState.mission_complete_sound_played:
            MissionStuff.set_number_of_objectives(1)
        else:
            MissionStuff.set_objective_text(
                False,
                MissionStuff.Line2,
                f"Round Complete! Press [{ClaimRewardBind.Key}] To Continue",
            )
            MissionStuff.set_objective_required(MissionStuff.Line2)
            MissionStuff.set_number_of_objectives(2)
    elif GameState.map_type == MapType.MiniBoss:
        MissionStuff.set_objective_text(
            False,
            MissionStuff.Line1,
            f"Kill {GameState.current_map.name}: {GameState.current_map.bosses_killed} / {GameState.current_map.total_bosses_in_map}",
        )
        MissionStuff.set_objective_text(
            False,
            MissionStuff.Line2,
            f"Kill Enemies: {GameState.current_map.kill_challenge_count} / {GameState.current_map.kill_challenge_goal}",
        )
        MissionStuff.set_objective_text(
            False,
            MissionStuff.Line3,
            f"Shoot {GameState.current_map.custom_map_data[1]}: {GameState.current_map.custom_map_data[2]} / 3",
        )
        MissionStuff.set_objective_required(MissionStuff.Line2)

        if not GameState.mission_complete_sound_played:
            MissionStuff.set_number_of_objectives(3)
        else:
            MissionStuff.set_objective_text(
                False,
                MissionStuff.Line4,
                f"Round Complete! Press [{ClaimRewardBind.Key}] To Continue",
            )
            MissionStuff.set_objective_required(MissionStuff.Line4)
            MissionStuff.set_number_of_objectives(4)
    elif GameState.map_type in (MapType.RedBarBoss, MapType.RaidBoss, MapType.FinalBoss):
        MissionStuff.set_objective_text(
            False,
            MissionStuff.Line1,
            f"Kill {GameState.current_map.name}: {GameState.current_map.bosses_killed} / {GameState.current_map.total_bosses_in_map}",
        )
        if not GameState.mission_complete_sound_played:
            MissionStuff.set_number_of_objectives(1)
        else:
            MissionStuff.set_objective_text(
                False,
                MissionStuff.Line2,
                f"Round Complete! Press [{ClaimRewardBind.Key}] To Continue",
            )
            MissionStuff.set_objective_required(MissionStuff.Line2)
            MissionStuff.set_number_of_objectives(2)
    elif GameState.map_type == MapType.MiniGame:
        MissionStuff.set_objective_text(
            False,
            MissionStuff.Line1,
            GameState.current_map.minigame_string,
        )
        if not GameState.mission_complete_sound_played:
            MissionStuff.set_number_of_objectives(1)
        else:
            MissionStuff.set_objective_text(
                False,
                MissionStuff.Line2,
                f"Round Complete! Press [{ClaimRewardBind.Key}] To Continue",
            )
            MissionStuff.set_objective_required(MissionStuff.Line2)
            MissionStuff.set_number_of_objectives(2)
    elif GameState.map_type == MapType.StartRoom:
        MissionStuff.set_objective_text(False, MissionStuff.Line1, "Welcome!")
        MissionStuff.set_number_of_objectives(1)
    else:
        MissionStuff.set_objective_text(False, MissionStuff.Line1, "Reward Round")
        MissionStuff.set_objective_text(
            False,
            MissionStuff.Line2,
            f"Round Complete! Press [{ClaimRewardBind.Key}] To Continue",
        )
        MissionStuff.set_objective_required(MissionStuff.Line2)
        MissionStuff.set_number_of_objectives(2)
    threading.Thread(target=MissionStuff.refresh_mission_display).start()
