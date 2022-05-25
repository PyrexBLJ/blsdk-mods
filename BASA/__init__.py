import unrealsdk
from unrealsdk import *

from ..ModMenu import EnabledSaveType, SDKMod, KeybindManager, ModTypes, Game, RegisterMod

class Main(SDKMod):
    Name: str = "Bank & Stash Anywhere"
    Description: str = "<font size='20' color='#00ffe8'>Bank & Stash Anywhere</font>\n\n" \
    "Use the bank and stash from anywhere with a hotkey\n\n" \
        "Default keys:\n\n" \
            "Open bank: <b>F10</b>\n" \
                "Open stash: <b>F11</b>\n\n" \
                    "Keys can be rebound in modded key bindings"
    Author: str = "PyrexBLJ"
    Version = "1.0.0"
    SaveEnabledState: EnabledSaveType = EnabledSaveType.LoadWithSettings

    Types: ModTypes = ModTypes.Utility
    SupportedGames = Game.TPS | Game.BL2

    Keybinds = [KeybindManager.Keybind("Open Bank", "F10"), 
                KeybindManager.Keybind("Open Stash", "F11")]

    def __init__(self):
        super().__init__()

    def ForceLoad(self):
        if Game.GetCurrent() == Game.BL2:
            unrealsdk.LoadPackage("Glacial_Dynamic")
        elif Game.GetCurrent() == Game.TPS:
            unrealsdk.LoadPackage("Spaceport_P")
        else : raise RuntimeError("Unsupported Game")

        unrealsdk.KeepAlive(unrealsdk.FindObject("GFxMovieDefinition", "UI_TwoPanelInterface.BankDef"))
        unrealsdk.KeepAlive(unrealsdk.FindObject("GFxMovieDefinition", "UI_TwoPanelInterface.StashDef"))

    def GameInputPressed(self, input):
        if input.Name == "Open Bank":
            controller = unrealsdk.GetEngine().GamePlayers[0].Actor
            controller.PlayGfxMovieDefinition("UI_TwoPanelInterface.BankDef")
        if input.Name == "Open Stash":
            controller = unrealsdk.GetEngine().GamePlayers[0].Actor
            controller.PlayGfxMovieDefinition("UI_TwoPanelInterface.StashDef")

    def Enable(self):
        self.ForceLoad()
        super().Enable()

    def Disable(self):
        super().Disable()



RegisterMod(Main())