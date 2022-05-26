from locale import atof
import unrealsdk

from Mods import ModMenu

class Main(ModMenu.SDKMod):
    Name: str = "Sniper Button"
    Description: str = "<font size='20' color='#00ffe8'>Sniper Button</font>\n\n" \
    "Automatically changes aim sensitivity while aiming\n\n" \
            "change rate can be modified in mod settings"
    Author: str = "PyrexBLJ"
    Version: str = "1.0.1"
    SaveEnabledState: ModMenu.EnabledSaveType = ModMenu.EnabledSaveType.LoadWithSettings

    Types: ModMenu.ModTypes = ModMenu.ModTypes.Utility
    SupportedGames: ModMenu.Game = ModMenu.Game.BL2 | ModMenu.Game.TPS

    defaultMouseSense = 60
    aimRate = 1
    increase = False

    def __init__(self) -> None:
        super().__init__()
        self.MySlider = ModMenu.Options.Slider(
            Caption="Aimed Rate",
            Description="How much sensitivity should be modified by while aiming",
            StartingValue = 1,
            MinValue = 1,
            MaxValue = 5,
            Increment = 1,
        )
        self.MyBoolean = ModMenu.Options.Boolean(
            Caption="Increase Speed",
            Description="True = faster aiming   False = slower aiming",
            StartingValue=True,
            Choices=["No", "Yes"]  # False, True
        )
        
        self.Options = [
            self.MySlider,
            self.MyBoolean
        ]

    def ModOptionChanged(self, option: ModMenu.Options.Base, new_value) -> None:
        if option == self.MySlider:
            self.aimRate = new_value
        if option == self.MyBoolean:
            self.increase = new_value

    @ModMenu.Hook("WillowGame.WillowWeapon.StartZoom")
    def onStartZoom(self, caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> None:
        controller = unrealsdk.GetEngine().GamePlayers[0].Actor
        if self.increase == True:
            controller.PlayerInput.MouseSensitivity = controller.PlayerInput.MouseSensitivity * self.aimRate
        elif self.increase == False: 
            controller.PlayerInput.MouseSensitivity = controller.PlayerInput.MouseSensitivity / self.aimRate

        return True

    @ModMenu.Hook("WillowGame.WillowWeapon.StopZoom")
    def onStopZoom(self, caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> None:
        controller = unrealsdk.GetEngine().GamePlayers[0].Actor
        controller.PlayerInput.MouseSensitivity = self.defaultMouseSense
        return True

    def Enable(self) -> None:
        controller = unrealsdk.GetEngine().GamePlayers[0].Actor
        self.defaultMouseSense = controller.PlayerInput.MouseSensitivity
        super().Enable()

    def Disable(self) -> None:
        super().Disable()

instance = Main()

ModMenu.RegisterMod(instance)