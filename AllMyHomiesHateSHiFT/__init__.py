from typing import List
import unrealsdk

from Mods import ModMenu

class Main(ModMenu.SDKMod):
    Name: str = "All My Homies Hate SHiFT"
    Description: str = "<font size='20' color='#00ffe8'>All My Homies Hate SHiFT</font>\n\n" \
    "Start The Game In Offline/LAN Mode\n\nMode can be set in Options > Mods"
    Author: str = "Pyrex"
    Version: str = "1.0.0"
    SaveEnabledState: ModMenu.EnabledSaveType = ModMenu.EnabledSaveType.LoadWithSettings

    Types: ModMenu.ModTypes = ModMenu.ModTypes.Utility
    SupportedGames: ModMenu.Game = ModMenu.Game.TPS | ModMenu.Game.BL2

    networkmodename: List[str] = ["Offline", "LAN"]
    networkmodevalues: List[List[int]] = [[2, 2], [1, 2]]

    modewassetonboot: bool = False

    def __init__(self) -> None:
        super().__init__()
        self.NetworkMode = ModMenu.Options.Spinner(
            Caption="Preferred Network Mode",
            Description="What mode to set on game boot & save quit",
            StartingValue = self.networkmodename[0],
            Choices = self.networkmodename,
        )
        self.Options = [
            self.NetworkMode
        ]

    def Enable(self) -> None:
        def titlescreen(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> None:
            if self.modewassetonboot == True:
                return True
            
            self.modewassetonboot = True
            currentmode = self.networkmodename.index(str(self.NetworkMode.CurrentValue))
            unrealsdk.GetEngine().GamePlayers[0].Actor.AttemptNetworkTransition(self.networkmodevalues[currentmode][0], self.networkmodevalues[currentmode][1], True)
            return True
        
        unrealsdk.RegisterHook("WillowGame.WillowGFxMoviePressStart.BeginStartupProcess", "AtTitleScreen", titlescreen)
        super().Enable()

    def Disable(self) -> None:
        unrealsdk.RemoveHook("WillowGame.WillowGFxMoviePressStart.BeginStartupProcess", "AtTitleScreen")
        super().Disable()

instance = Main()

ModMenu.RegisterMod(instance)

"""
{NetworkType: 0, InviteType: 1, bPrompt: True} friends only
{NetworkType: 0, InviteType: 0, bPrompt: True} invite only
{NetworkType: 0, InviteType: 2, bPrompt: True} public
{NetworkType: 1, InviteType: 2, bPrompt: True} lan
{NetworkType: 2, InviteType: 2, bPrompt: True} offline
"""