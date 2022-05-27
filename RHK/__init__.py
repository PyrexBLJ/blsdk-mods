import unrealsdk

from Mods import ModMenu

class Main(ModMenu.SDKMod):
    Name: str = "Respec HotKey"
    Description: str = "<font size='20' color='#00ffe8'>Respec HotKey</font>\n\n" \
    "Respec your skills from anywhere with a hotkey\n\n" \
        "Default keys:\n\n" \
            "Respec: <b>Num-1</b>\n\n" \
                "Key can be rebound in modded key bindings"
    Author: str = "PyrexBLJ"
    Version: str = "1.0.0"
    SaveEnabledState: ModMenu.EnabledSaveType = ModMenu.EnabledSaveType.LoadWithSettings

    Types: ModMenu.ModTypes = ModMenu.ModTypes.Utility
    SupportedGames: ModMenu.Game = ModMenu.Game.TPS | ModMenu.Game.BL2

    RespecBind = ModMenu.Keybind("Respec", "Num-1")

    Keybinds = [ RespecBind ]

    def __init__(self) -> None:
        super().__init__()

    def GameInputPressed(self, bind: ModMenu.Keybind, event: ModMenu.InputEvent) -> None:
        if bind == self.RespecBind and event == ModMenu.InputEvent.Pressed:
            controller = unrealsdk.GetEngine().GamePlayers[0].Actor
            controller.VerifySkillRespec()

    def Enable(self) -> None:
        super().Enable()

    def Disable(self) -> None:
        super().Disable()

instance = Main()

ModMenu.RegisterMod(instance)