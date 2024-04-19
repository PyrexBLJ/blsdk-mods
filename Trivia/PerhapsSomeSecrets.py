import threading
import time
from typing import Tuple
import unrealsdk
from .Util import distance, get_player_location
try:
    from Mods.MapLoader import placeablehelper
except ImportError:
    import webbrowser

    webbrowser.open("https://bl-sdk.github.io/mods/MapLoader/")
    raise ImportError("Trivia requires the most recent version of MapLoader to be installed")

class Secrets:

    candosecret1: bool = True
    candosecret2: bool = True

    def check_button1() -> None:
        button = placeablehelper.TAGGED_OBJECTS[f"Secret Area Button 1"][0].uobj
        if distance(get_player_location(), placeablehelper.interactive_objects.get_location(button)) < 700:
            unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn.Location = (30273.06640625, 39703.97265625, 8709.2646484375)
            unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn.Controller.Rotation = (65463, -73802, 0)
    
    def check_button2() -> None:
        button = placeablehelper.TAGGED_OBJECTS[f"Secret Area Button 2"][0].uobj
        if distance(get_player_location(), placeablehelper.interactive_objects.get_location(button)) < 700:
            unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn.Location = (25211.806640625, 34481.76953125, 7427.22900390625)
            unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn.Controller.Rotation = (65117, -446174, 0)

    def check_button3() -> None:
        button = placeablehelper.TAGGED_OBJECTS[f"Secret Area Button 3"][0].uobj
        if distance(get_player_location(), placeablehelper.interactive_objects.get_location(button)) < 700:
            unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn.Location = (32611.873046875, 30878.685546875, 5964.35498046875)
            unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn.Controller.Rotation = (64556, -53991, 0)

    def check_pos1() -> None:
        if distance(get_player_location(), (28970.8828125, 38821.171875, 8362.798828125)) < 350 and Secrets.candosecret1:
            Secrets.candosecret1 = False
            threading.Thread(target=Secrets.move_butt1).start()
    
    def check_pos2() -> None:
        if distance(get_player_location(), (29199.439453125, 33558.609375, 6443.32421875)) < 350 and Secrets.candosecret2:
            Secrets.candosecret2 = False
            threading.Thread(target=Secrets.move_butt2).start()

    def move_butt1() -> None:
        butt = placeablehelper.TAGGED_OBJECTS[f"Runaway 1"][0].uobj
        done: bool = False
        up: bool = True
        #unrealsdk.GetEngine().GamePlayers[0].Actor.PlayAkEvent(
            #unrealsdk.FindObject("AkEvent", "Ake_Aster_Seq.SQ.Ak_Play_Seq_SQ_Buttstallion_Talk"),
        #)
        while not done:
            buttpos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(butt)
            if buttpos[0] >= 27300:
                newpos: Tuple[float, float, float] = (buttpos[0] - 8, buttpos[1], buttpos[2])
                if up == True:
                    if newpos[2] <= 9174:
                        newerpos: Tuple[float, float, float] = (newpos[0], newpos[1], newpos[2] + 4)
                    else:
                        up = False
                else:
                    if newpos[2] >= 9124:
                        newerpos: Tuple[float, float, float] = (newpos[0], newpos[1], newpos[2] - 4)
                    else:
                        up = True
                placeablehelper.static_mesh.set_location(butt, newerpos)
            else:
                done = True
            time.sleep(0.01)

    def move_butt2() -> None:
        butt = placeablehelper.TAGGED_OBJECTS[f"Runaway 2"][0].uobj
        done: bool = False
        up: bool = True
        #unrealsdk.GetEngine().GamePlayers[0].Actor.PlayAkEvent(
            #unrealsdk.FindObject("AkEvent", "Ake_Aster_Seq.SQ.Ak_Play_Seq_SQ_Buttstallion_Pet_01"),
        #)
        while not done:
            buttpos: Tuple[float, float, float] = placeablehelper.static_mesh.get_location(butt)
            if buttpos[1] <= 34809:
                newpos: Tuple[float, float, float] = (buttpos[0] , buttpos[1] + 8, buttpos[2])
                if up == True:
                    if newpos[2] <= 6618:
                        newerpos: Tuple[float, float, float] = (newpos[0], newpos[1], newpos[2] + 4)
                    else:
                        up = False
                else:
                    if newpos[2] >= 6568:
                        newerpos: Tuple[float, float, float] = (newpos[0], newpos[1], newpos[2] - 4)
                    else:
                        up = True
                placeablehelper.static_mesh.set_location(butt, newerpos)
            else:
                done = True
            time.sleep(0.01)