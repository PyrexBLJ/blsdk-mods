from typing import Tuple
import unrealsdk
from math import sqrt, pow
def get_player_location() -> unrealsdk.FStruct:
        """Get the player's location."""
        return unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn.Location

def distance(loc: unrealsdk.FStruct, goal: Tuple[float, float, float]) -> float:
    """Distance between an unreal vector and a tuple."""
    return sqrt(
        pow(float(goal[0]) - float(loc.X), 2)
        + pow(float(goal[1]) - float(loc.Y), 2)
        + pow(float(goal[2]) - float(loc.Z), 2),
    )