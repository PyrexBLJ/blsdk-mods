import unrealsdk

from Mods import ModMenu

class Main(ModMenu.SDKMod):
    Name: str = "Audio Control"
    Description: str = "<font size='20' color='#00ffe8'>Audio Control</font>\n\n" \
    "Toggle Bee shield & Bore impact sound\n\n" \
        "Toggles in Options > Mods > Audio Control"
    Author: str = "Pyrex"
    Version: str = "1.0.1"
    SaveEnabledState: ModMenu.EnabledSaveType = ModMenu.EnabledSaveType.LoadWithSettings

    Types: ModMenu.ModTypes = ModMenu.ModTypes.Utility
    SupportedGames: ModMenu.Game = ModMenu.Game.BL2

    def __init__(self) -> None:
        super().__init__()
        self.doBeeSound = ModMenu.Options.Boolean(
            Caption="Bee Shield Impact Sound",
            Description="Enables/Disables Bee Sounds",
            StartingValue=True,
            Choices=["Off", "On"]  # False, True
        )
        self.doBoreSound = ModMenu.Options.Boolean(
            Caption="Bore Sound",
            Description="Enables/Disables Bore Sounds",
            StartingValue=True,
            Choices=["Off", "On"]  # False, True
        )
        self.Options = [
                self.doBeeSound,
                self.doBoreSound
            ]
        

    def ModOptionChanged(self, option: ModMenu.Options.Base, new_value) -> None:
        if option == self.doBoreSound:
            if new_value == True:
                unrealsdk.GetEngine().GamePlayers[0].Actor.GetWillowGlobals().GetGlobalsDefinition().BulletPenetratedEnemyAkEvent = unrealsdk.FindObject("AkEvent", "Ake_FX_Player_Assassin.Ak_Play_FX_Assassin_Bore_Impact")
                #unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("set GD_Globals.General.Globals BulletPenetratedEnemyAkEvent AkEvent'Ake_FX_Player_Assassin.Ak_Play_FX_Assassin_Bore_Impact'")
            elif new_value == False:
                unrealsdk.GetEngine().GamePlayers[0].Actor.GetWillowGlobals().GetGlobalsDefinition().BulletPenetratedEnemyAkEvent = None
                #unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("set GD_Globals.General.Globals BulletPenetratedEnemyAkEvent None")
                

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