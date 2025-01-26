import unrealsdk

from Mods import ModMenu

class Main(ModMenu.SDKMod):
    Name: str = "Bank & Stash Anywhere"
    Description: str = "<font size='20' color='#00ffe8'>Bank & Stash Anywhere</font>\n\n" \
    "Use the bank and stash from anywhere with a hotkey\n\n" \
        "Default keys:\n\n" \
            "Open bank: <b>F10</b>\n" \
                "Open stash: <b>F11</b>\n\n" \
                    "Keys can be rebound in modded key bindings"
    Author: str = "PyrexBLJ"
    Version: str = "1.0.3"
    SaveEnabledState: ModMenu.EnabledSaveType = ModMenu.EnabledSaveType.LoadWithSettings

    Types: ModMenu.ModTypes = ModMenu.ModTypes.Utility
    SupportedGames: ModMenu.Game = ModMenu.Game.TPS | ModMenu.Game.BL2

    BankBind = ModMenu.Keybind("Open Bank", "F10")
    StashBind = ModMenu.Keybind("Open Stash", "F11")

    Keybinds = [ BankBind, StashBind ]

    def __init__(self) -> None:
        super().__init__()

    def ForceLoad(self) -> None:
        if ModMenu.Game.GetCurrent() == ModMenu.Game.BL2:
            unrealsdk.LoadPackage("Glacial_P")
            unrealsdk.LoadPackage("Glacial_Dynamic", 0, False)
        elif ModMenu.Game.GetCurrent() == ModMenu.Game.TPS:
            unrealsdk.LoadPackage("Spaceport_P", 0, False)
        else : raise RuntimeError("Unsupported Game")

        unrealsdk.KeepAlive(unrealsdk.FindObject("GFxMovieDefinition", "UI_TwoPanelInterface.BankDef"))
        unrealsdk.KeepAlive(unrealsdk.FindObject("GFxMovieDefinition", "UI_TwoPanelInterface.StashDef"))

    def GameInputPressed(self, bind: ModMenu.Keybind, event: ModMenu.InputEvent) -> None:
        if bind == self.BankBind and event == ModMenu.InputEvent.Pressed:
            controller = unrealsdk.GetEngine().GamePlayers[0].Actor
            controller.PlayGfxMovieDefinition("UI_TwoPanelInterface.BankDef")
        if bind == self.StashBind and event == ModMenu.InputEvent.Pressed:
            controller = unrealsdk.GetEngine().GamePlayers[0].Actor
            controller.PlayGfxMovieDefinition("UI_TwoPanelInterface.StashDef")

    def Enable(self) -> None:
        self.ForceLoad()
        super().Enable()

    def Disable(self) -> None:
        super().Disable()

instance = Main()

ModMenu.RegisterMod(instance)