import time
from typing import Any, List, Tuple
import unrealsdk  # type: ignore
import threading
from pathlib import Path

try:
    import Mods.UserFeedback as uFeed
except ImportError:
    import webbrowser

    webbrowser.open("https://bl-sdk.github.io/mods/UserFeedback/")
    raise ImportError("Trivia requires the most recent version of UserFeedback to be installed")
try:
    from Mods.MapLoader import placeablehelper
except ImportError:
    import webbrowser

    webbrowser.open("https://bl-sdk.github.io/mods/MapLoader/")
    raise ImportError("Trivia requires the most recent version of MapLoader to be installed")

from Mods import ModMenu
from Mods.ModMenu import Keybind
from .Questions import QuestionLib
from .Quotes import QuoteLib
from .PerhapsSomeSecrets import Secrets
from .Util import distance, get_player_location



class Main(ModMenu.SDKMod):
    Name: str = "Borderlands Trivia"
    Description: str = (
        "<font size='20' color='#ff0000'>Borderlands Trivia</font>\n"
        "So you're a Borderlands fan huh?\nName every gun.\n\nTest your knowledge while helping Tiny Tina rescue Buttstallion.\n\nGo to <font color='#079413'>Digistruct Peak</font> to start trivia."
    )
    Author: str = "JoltzDude139 | Pyrex"
    Version: str = "1.0.0"
    SaveEnabledState: ModMenu.EnabledSaveType = ModMenu.EnabledSaveType.NotSaved

    Types: ModMenu.ModTypes = ModMenu.ModTypes.Utility
    SupportedGames: ModMenu.Game = ModMenu.Game.BL2

    StartTriviaBind: Keybind = Keybind("Start Trivia", "F1")

    respawnPopped: bool = True

    def __init__(self) -> None:
        super().__init__()
        self.Keybinds: List[ModMenu.Keybind] = [
            self.StartTriviaBind,
        ]

    def reset_vars(self) -> None:
        QuestionLib.inTrivia = False
        QuestionLib.triviaStreak = 1
        QuestionLib.gaveLoot = False
        QuestionLib.canShowQuestion = True
        QuestionLib.usedQuestions = []
        QuoteLib.canShowQuote = True
        QuoteLib.triggeredQuotes = []
        QuoteLib.usedQuotes = []
        QuoteLib.usedNames = []
        QuoteLib.usedTypes = []
        Secrets.candosecret1 = True
        Secrets.candosecret2 = True
        unrealsdk.FindObject("InteractiveObjectDefinition", "GD_Balance_Shopping.VendingMachines.InteractiveObj_VendingMachine_GrenadesAndAmmo").CompassIcon = 4
        if QuestionLib.inTrivia == True:
            placeablehelper.unload_map()

    def GameInputPressed(self, bind: ModMenu.Keybind, event: ModMenu.InputEvent) -> None:
        if bind == self.StartTriviaBind and event == ModMenu.InputEvent.Pressed:
            if unrealsdk.GetEngine().GetCurrentWorldInfo().GetStreamingPersistentMapName().lower() == "testingzone_p":
                if QuestionLib.inTrivia == False and self.respawnPopped == True:
                    self.respawnPopped = False
                    QuestionLib.load_trivia_map()
                    pcon = unrealsdk.GetEngine().GamePlayers[0].Actor
                    pcon.Pawn.Location = (29020.78515625, 35473.859375, 7751.482421875)
                    pcon.Pawn.Controller.Rotation = (64923, 15204, 0)
                    QuestionLib.start_run()
                else:
                    uFeed.ShowHUDMessage(
                        Title="Borderlands Trivia",
                        Message=f"Cannot Start Trivia At This Time",
                        Duration=5,
                        MenuHint=0,
                    )
            else:
                uFeed.ShowHUDMessage(
                    Title="Borderlands Trivia",
                    Message=f"Go to [place]Digistruct Peak[-place] to Play Trivia",
                    Duration=5,
                    MenuHint=0,
                )

    def do_spawn_delayed(self) -> None:
        time.sleep(5)
        uFeed.ShowHUDMessage(
            Title="Borderlands Trivia",
            Message=f"Press [{self.StartTriviaBind.Key}] To Play Trivia!",
            Duration=5,
            MenuHint=0,
        )

    def Enable(self) -> None:
        def spawn(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, _params: unrealsdk.FStruct) -> bool:
            if unrealsdk.GetEngine().GetCurrentWorldInfo().GetStreamingPersistentMapName().lower() == "testingzone_p":
                threading.Thread(target=self.do_spawn_delayed).start()
            return True
        
        def playermove(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, _params: unrealsdk.FStruct) -> bool:
            if unrealsdk.GetEngine().GetCurrentWorldInfo().GetStreamingPersistentMapName().lower() != "testingzone_p":
                return True
            if _params.newAccel.X == 0 and _params.newAccel.Y == 0 and _params.newAccel.Z == 0:
                return True
            if QuestionLib.inTrivia == False:
                return True
            if QuestionLib.triviaStreak < 11:
                QuestionLib.check_plates()
            if distance(get_player_location(), (25716.41796875, 34589.1015625, 4398.685546875)) < 200:
                QuestionLib.complete_run()
            QuoteLib.check_echos()
            Secrets.check_pos1()
            Secrets.check_pos2()
            return True
        
        def died(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, _params: unrealsdk.FStruct) -> bool:
            if unrealsdk.GetEngine().GetCurrentWorldInfo().GetStreamingPersistentMapName().lower() == "testingzone_p" and QuestionLib.inTrivia == True:
                self.reset_vars()
            return True
        
        def died2(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, _params: unrealsdk.FStruct) -> bool:
            if unrealsdk.GetEngine().GetCurrentWorldInfo().GetStreamingPersistentMapName().lower() == "testingzone_p" and QuestionLib.inTrivia == True and int(_params.InjuredDeadStateVal) != 0:
                self.reset_vars()
            return True
        
        def died3(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, _params: unrealsdk.FStruct) -> bool:
            if unrealsdk.GetEngine().GetCurrentWorldInfo().GetStreamingPersistentMapName().lower() == "testingzone_p":
                self.respawnPopped = True
                self.reset_vars()
            return True
        
        def savequit(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, _params: unrealsdk.FStruct) -> bool:
            if QuestionLib.inTrivia == True:
                self.reset_vars()
            return True
        
        def use(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, _params: unrealsdk.FStruct) -> bool:
            if QuestionLib.inTrivia:
                Secrets.check_button1()
                Secrets.check_button2()
                Secrets.check_button3()
            return True

        unrealsdk.RegisterHook("WillowGame.WillowGameInfo.TeleportToFinalDestinationAfterLoad", "Spawn", spawn)
        unrealsdk.RegisterHook("Engine.PlayerController.AdjustPlayerWalkingMoveAccel", "PlayerMove", playermove)
        unrealsdk.RegisterHook("WillowGame.WillowPawn.CausePlayerDeath", "PlayerDied", died)
        unrealsdk.RegisterHook("WillowGame.WillowPlayerPawn.SetInjuredDeadState", "Death", died2)
        unrealsdk.RegisterHook("WillowGame.WillowHUD.ShowRespawnDialog", "ShowRespawnDialog", died3)
        unrealsdk.RegisterHook("WillowGame.PauseGFxMovie.PromptQuit_Ok", "SaveQuit", savequit)
        unrealsdk.RegisterHook("WillowGame.WillowInteractiveObject.UseObject", "Use", use) # WillowGame.WillowPlayerController.Use
        super().Enable()

    def Disable(self) -> None:
        unrealsdk.RemoveHook("WillowGame.WillowGameInfo.TeleportToFinalDestinationAfterLoad", "Spawn")
        unrealsdk.RemoveHook("Engine.PlayerController.AdjustPlayerWalkingMoveAccel", "PlayerMove")
        unrealsdk.RemoveHook("WillowGame.WillowPawn.CausePlayerDeath", "PlayerDied")
        unrealsdk.RemoveHook("WillowGame.WillowPlayerPawn.SetInjuredDeadState", "Death")
        unrealsdk.RemoveHook("WillowGame.WillowHUD.ShowRespawnDialog", "ShowRespawnDialog")
        unrealsdk.RemoveHook("WillowGame.PauseGFxMovie.PromptQuit_Ok", "SaveQuit")
        unrealsdk.RemoveHook("WillowGame.WillowInteractiveObject.UseObject", "Use")
        super().Disable()

instance = Main()

if __name__ == "__main__":
    unrealsdk.Log(f"[{instance.Name}] Manually loaded")
    for mod in ModMenu.Mods:
        if mod.Name == instance.Name:
            if mod.IsEnabled:
                mod.Disable()
            ModMenu.Mods.remove(mod)
            unrealsdk.Log(f"[{instance.Name}] Removed last instance")

            # Fixes inspect.getfile()
            instance.__class__.__module__ = mod.__class__.__module__
            break

ModMenu.RegisterMod(instance)