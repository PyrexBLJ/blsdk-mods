import math
import random
import time
from typing import Tuple

import unrealsdk  # type: ignore

def vec_distance(loc: unrealsdk.FStruct, goal: unrealsdk.FStruct) -> float:
    """Distance between two unreal vectors."""
    return math.sqrt(
        math.pow(float(goal.X) - float(loc.X), 2)
        + math.pow(float(goal.Y) - float(loc.Y), 2)
        + math.pow(float(goal.Z) - float(loc.Z), 2),
    )


def distance(loc: unrealsdk.FStruct, goal: Tuple[float, float, float]) -> float:
    """Distance between an unreal vector and a tuple."""
    return math.sqrt(
        math.pow(float(goal[0]) - float(loc.X), 2)
        + math.pow(float(goal[1]) - float(loc.Y), 2)
        + math.pow(float(goal[2]) - float(loc.Z), 2),
    )


def travel_to_destination(destination: str) -> None:
    """Initiate travel to a destination."""
    dest = unrealsdk.FindObject(
        "LevelTravelStationDefinition",
        destination,
    ) or unrealsdk.FindObject("FastTravelStationDefinition", destination)
    unrealsdk.GetEngine().GamePlayers[0].Actor.ServerTeleportPlayerToStation(dest)


def get_player_location() -> unrealsdk.FStruct:
    """Get the player's location."""
    return unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn.Location


def draw_shader(
    canvas: unrealsdk.UObject,
    x: float,
    y: float,
    w: float,
    h: float,
    color: Tuple[int, int, int, int],
    tex: unrealsdk.UObject,
) -> None:
    """Draws a rectangle at the specified location with a given color and texture."""
    canvas.SetPos(x, y)  # shader positionn X, Y
    canvas.SetDrawColorStruct(color)  # shader color
    canvas.DrawRect(w, h, tex)  # width, height, texture object


def draw_text(
    canvas: unrealsdk.UObject,
    text: str,
    x: float,
    y: float,
    x_xcale: float,
    y_scale: float,
    color: Tuple[int, int, int, int],
) -> None:
    """Draws text at the specified location with a given scale and color."""
    canvas.SetPos(x, y)  # text position X, Y
    canvas.SetDrawColorStruct(color)  # text color b g r a
    canvas.DrawText(
        text,  # text
        0,  # optionalCR?
        float(x_xcale),  # XScale
        float(y_scale),  # YScale
        (
            False,  # cliptext
            False,  # enable shadow
            (
                True,  # enable glow
                (0, 0, 255, 255),  # glow color
                (1, 1),  # glow outer radius
                (1, 1),  # glow inner radius
            ),
        ),
    )  # (text, optionalCR?, XScale, YScale, (cliptext, enable shadow, (enable glow, (glow color, (glow outer radius), (glow inner radius)))) no idea what optionalCR does, clip range mby?
