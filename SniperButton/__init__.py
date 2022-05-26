from locale import atof
import unrealsdk

from Mods import ModMenu

class Main(ModMenu.SDKMod):
    Name: str = "Sniper Button"
    Description: str = "<font size='20' color='#00ffe8'>Sniper Button</font>\n\n" \
    "Automatically changes aim sensitivity while aiming\n\n" \
        "Default rate halves sensitivity\n\n" \
            "change rate can be modified in mod settings"
    Author: str = "PyrexBLJ"
    Version: str = "1.0.0"
    SaveEnabledState: ModMenu.EnabledSaveType = ModMenu.EnabledSaveType.LoadWithSettings

    Types: ModMenu.ModTypes = ModMenu.ModTypes.Utility
    SupportedGames: ModMenu.Game = ModMenu.Game.TPS | ModMenu.Game.BL2

    aimRate = "0.5"
    aimRateNum = 0.5
    defaultMouseSense = 60

    def __init__(self) -> None:
        super().__init__()
        self.MySpinner = ModMenu.Options.Spinner(
            Caption="Aimed Rate",
            Description="How much sensitivity should be multiplied by while aiming",
            StartingValue="0.5",
            Choices=[ "0.1", "0.25", "0.5", "0.75", "1.5", "2.0"]
        )
        
        self.Options = [
            self.MySpinner,
        ]

    def ModOptionChanged(self, option: ModMenu.Options.Base, new_value) -> None:
        if option == self.MySpinner:
            self.aimRate = new_value
            self.aimRateNum = atof(new_value)

    @ModMenu.Hook("WillowGame.WillowWeapon.StartZoom")
    def onStartZoom(self, caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
        controller = unrealsdk.GetEngine().GamePlayers[0].Actor
        self.defaultMouseSense = controller.PlayerInput.MouseSensitivity
        controller.PlayerInput.MouseSensitivity = self.defaultMouseSense * self.aimRateNum
        unrealsdk.Log("onStartZoom called")
        return True

    @ModMenu.Hook("WillowGame.WillowWeapon.StopZoom")
    def onStopZoom(self, caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
        unrealsdk.Log("onSpawn called")
        controller = unrealsdk.GetEngine().GamePlayers[0].Actor
        controller.PlayerInput.MouseSensitivity = self.defaultMouseSense
        return True

    def Enable(self) -> None:
        super().Enable()

    def Disable(self) -> None:
        super().Disable()

instance = Main()

ModMenu.RegisterMod(instance)