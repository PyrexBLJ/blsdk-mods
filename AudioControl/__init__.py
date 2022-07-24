import unrealsdk

from Mods import ModMenu

class Main(ModMenu.SDKMod):
    Name: str = "Audio Control"
    Description: str = "<font size='20' color='#00ffe8'>Audio Control</font>\n\n" \
    "Toggle Bee shield impact sound\n\n" \
        "Bore Sound will be added once I can find where its playing from lol"
    Author: str = "PyrexBLJ"
    Version: str = "1.0.0"
    SaveEnabledState: ModMenu.EnabledSaveType = ModMenu.EnabledSaveType.LoadWithSettings

    Types: ModMenu.ModTypes = ModMenu.ModTypes.Utility
    SupportedGames: ModMenu.Game = ModMenu.Game.BL2

    def __init__(self) -> None:
        self.doBeeSound = ModMenu.Options.Boolean(
            Caption="Bee Shield Impact Sound",
            Description="Enables/Disables Bee Sounds",
            StartingValue=True,
            Choices=["Off", "On"]  # False, True
        )
        self.Options = [
                self.doBeeSound
            ]
        super().__init__()

    def Enable(self) -> None:

        def onBeeSound(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> None:
            if "Play_UI_Shield_Impact_The_Bee" in str(params.Event):
                if self.doBeeSound.CurrentValue == False:
                    return False
                else:
                    return True
            else:
                return True


        unrealsdk.RegisterHook("Engine.PlayerController.ClientPlayAkEvent", "SoundControlBee", onBeeSound)
        super().Enable()

    def Disable(self) -> None:
        unrealsdk.RemoveHook("Engine.PlayerController.ClientPlayAkEvent", "SoundControlBee")
        super().Disable()

instance = Main()

ModMenu.RegisterMod(instance)