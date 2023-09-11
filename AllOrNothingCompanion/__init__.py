import unrealsdk

from Mods import ModMenu

class Main(ModMenu.SDKMod):
    Name: str = "AONCompanion"
    Description: str = "<font size='20' color='#00ffe8'>All Or Nothing Companion</font>\n\n" \
    "Joltz idea for a deception modifier in his AON run"
    Author: str = "Pyrex"
    Version: str = "1.0.2"
    SaveEnabledState: ModMenu.EnabledSaveType = ModMenu.EnabledSaveType.LoadWithSettings

    Types: ModMenu.ModTypes = ModMenu.ModTypes.Utility
    SupportedGames: ModMenu.Game = ModMenu.Game.BL2

    SpeedModifier: int = 50
    IsOn: bool = True
    AllChars: bool = False

    ResetTimescaleBind = ModMenu.Keybind("Reset Timescale", "F13")

    Keybinds = [ ResetTimescaleBind ]

    def __init__(self) -> None:
        self.Enabled = ModMenu.Options.Boolean(
            Caption="Enabled",
            Description="Enables/Disables The Mod",
            StartingValue=True,
            Choices=["No", "Yes"]
        )
        self.AC = ModMenu.Options.Boolean(
            Caption="All Characters Mode",
            Description="Enables/Disables The Mod For All Characters",
            StartingValue=False,
            Choices=["No", "Yes"]
        )
        self.GameSpeedSlider = ModMenu.Options.Slider(
            Caption="Deception Game Speed",
            Description="How much game speed should be slowed down by as a percentage",
            StartingValue = 50,
            MinValue = 0,
            MaxValue = 100,
            Increment = 1,
        )
        self.Options = [
            self.Enabled,
            self.AC,
            self.GameSpeedSlider
        ]
        super().__init__()

    def ModOptionChanged(self, option: ModMenu.Options.Base, new_value) -> None:
        if option == self.GameSpeedSlider:
            self.SpeedModifier = new_value
        if option == self.Enabled:
            self.IsOn = new_value
        if option == self.AC:
            self.AllChars = new_value

    def GameInputPressed(self, bind: ModMenu.Keybind, event: ModMenu.InputEvent) -> None:
        if bind == self.ResetTimescaleBind and event == ModMenu.InputEvent.Pressed:
            unrealsdk.GetEngine().GetCurrentWorldInfo().TimeDilation = float(1.0)

    def Enable(self) -> None:

        def StartAC(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> None:
            if self.IsOn == True:
                if self.AllChars == False and str(unrealsdk.GetEngine().GamePlayers[0].Actor.PlayerClass.SkillTreePath) == "GD_Assassin_Streaming.SkillTree.SkillTree_Assassin":
                    unrealsdk.GetEngine().GetCurrentWorldInfo().TimeDilation = float(self.SpeedModifier / 100)
                elif self.AllChars == True:
                    unrealsdk.GetEngine().GetCurrentWorldInfo().TimeDilation = float(self.SpeedModifier / 100)
            return True

        def EndAC(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> None:
            if self.IsOn == True:
                unrealsdk.GetEngine().GetCurrentWorldInfo().TimeDilation = float(1.0)
            return True

        #unrealsdk.RegisterHook("WillowGame.WillowPlayerController.StartActionSkill", "ACS", StartAC)
        unrealsdk.RegisterHook("WillowGame.ActionSkill.OnActionSkillActivated", "ACS", StartAC)
        unrealsdk.RegisterHook("WillowGame.ActionSkill.OnActionSkillEnded", "ACE", EndAC)
        super().Enable()

    def Disable(self) -> None:
        #unrealsdk.RemoveHook("WillowGame.WillowPlayerController.StartActionSkill", "ACS")
        unrealsdk.RemoveHook("WillowGame.ActionSkill.OnActionSkillActivated", "ACS")
        unrealsdk.RemoveHook("WillowGame.ActionSkill.OnActionSkillEnded", "ACE")
        super().Disable()

instance = Main()

ModMenu.RegisterMod(instance)