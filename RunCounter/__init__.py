import unrealsdk

from Mods import ModMenu

class Main(ModMenu.SDKMod):
    Name: str = "Run Counter"
    Description: str = "<font size='20' color='#00ffe8'>Run Counter</font>\n\n" \
    "Adds 1 to the counter on save quit\n" \
        "Drop Counter will count any dropped object of at least legendary rarity\n\n" \
            "Reset Count: Num-5 (default)\n\n" \
                "WIP"
    Author: str = "PyrexBLJ"
    Version: str = "1.0.0"
    SaveEnabledState: ModMenu.EnabledSaveType = ModMenu.EnabledSaveType.LoadWithSettings

    Types: ModMenu.ModTypes = ModMenu.ModTypes.Utility
    SupportedGames: ModMenu.Game = ModMenu.Game.BL2 | ModMenu.Game.TPS

    Runs: int = 1
    DrawCounter: bool = False
    DrawLs: bool = False
    DrawPs: bool = False
    DrawSs: bool = False
    DrawEs: bool = False
    ResetDrops: bool = True
    legendaries: int = 0
    pearls: int = 0
    seraph: int = 0
    effervescent: int = 0
    NumDisplayedCounters: int = 0
    x: int = 50
    y: int = 50
    rarity: int = 0

    ResetCountBind = ModMenu.Keybind("Reset Count", "Num-5")

    Keybinds = [ ResetCountBind ]

    blackcolor = (0, 0, 0, 255)

    def __init__(self) -> None:
        super().__init__()
        self.runcount = ModMenu.Options.Boolean(
            Caption="Draw Counter",
            Description="Turn the counter on and off",
            StartingValue=False,
            Choices=["No", "Yes"]  # False, True
        )
        self.lcount = ModMenu.Options.Boolean(
            Caption="Draw Legendary Drop Counter",
            Description="Turn the drop counter on and off",
            StartingValue=False,
            Choices=["No", "Yes"]  # False, True
        )
        self.pcount = ModMenu.Options.Boolean(
            Caption="Draw Pearlescent Drop Counter",
            Description="Turn the drop counter on and off",
            StartingValue=False,
            Choices=["No", "Yes"]  # False, True
        )
        self.scount = ModMenu.Options.Boolean(
            Caption="Draw Seraph Drop Counter",
            Description="Turn the drop counter on and off",
            StartingValue=False,
            Choices=["No", "Yes"]  # False, True
        )
        self.ecount = ModMenu.Options.Boolean(
            Caption="Draw Effervescent Drop Counter",
            Description="Turn the drop counter on and off",
            StartingValue=False,
            Choices=["No", "Yes"]  # False, True
        )
        self.resetdropcounters = ModMenu.Options.Boolean(
            Caption="Reset Drops With Runs",
            Description="Will make the Reset Count reset the drops count as well",
            StartingValue=True,
            Choices=["No", "Yes"]  # False, True
        )
        
        self.Options = [
            self.runcount,
            self.lcount,
            self.pcount,
            self.scount,
            self.ecount,
            self.resetdropcounters
        ]

    def ModOptionChanged(self, option: ModMenu.Options.Base, new_value) -> None:
        if option == self.runcount:
            self.DrawCounter = new_value

        if option == self.lcount:
            self.DrawLs = new_value

        if option == self.pcount:
            self.DrawPs = new_value

        if option == self.scount:
            self.DrawSs = new_value

        if option == self.ecount:
            self.DrawEs = new_value

        if option == self.resetdropcounters:
            self.ResetDrops = new_value

    def GameInputPressed(self, bind: ModMenu.Keybind, event: ModMenu.InputEvent) -> None:
        if bind == self.ResetCountBind and event == ModMenu.InputEvent.Pressed:
            self.Runs = 1
            if self.ResetDrops is True:
                self.legendaries = 0
                self.pearls = 0
                self.seraph = 0
                self.effervescent = 0
        
    def DrawText(self, canvas, text, x, y, color, scalex, scaley) -> None:
        canvas.Font = unrealsdk.FindObject("Font", "UI_Fonts.Font_Willowbody_18pt")

        canvas.SetPos(x, y + (self.NumDisplayedCounters * y), 0)
        canvas.SetDrawColorStruct(color) #b, g, r, a
        canvas.DrawText(text, False, scalex, scaley, ())
        self.NumDisplayedCounters += 1

    def Enable(self) -> None:
            def onPostRender(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
                if not params.Canvas:
                    return True

                canvas = params.Canvas

                self.NumDisplayedCounters = 0

                if self.DrawCounter is True:
                    self.DrawText(canvas, "Run # " + str(self.Runs), self.x, self.y, (0, 165, 255, 255), 1, 1)

                if self.DrawLs is True:
                    self.DrawText(canvas, "Legendaries: " + str(self.legendaries), self.x, self.y, (0, 165, 255, 255), 1, 1)

                if self.DrawPs is True:
                    self.DrawText(canvas, "Pearlescents: " + str(self.pearls), self.x, self.y, (0, 165, 255, 255), 1, 1)

                if self.DrawSs is True:
                    self.DrawText(canvas, "Seraphs: " + str(self.seraph), self.x, self.y, (0, 165, 255, 255), 1, 1)

                if self.DrawEs is True:
                    self.DrawText(canvas, "Effervescents: " + str(self.effervescent), self.x, self.y, (0, 165, 255, 255), 1, 1)

                #self.DrawText(canvas, "Rarity: " + str(self.rarity), self.x, self.y, (0, 165, 255, 255), 1, 1)
                
                return True

            def onSaveQuit(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> None:
                if self.DrawCounter is True:
                    self.Runs += 1

                return True

            def onQuitWithoutSaving(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
                if self.DrawCounter is True:
                    self.Runs += 1

                return True

            def onNewDrop(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
                if self.DrawLs is True:
                    if caller.InventoryRarityLevel == 9: #Legendaries
                        self.legendaries += 1
                    if caller.InventoryRarityLevel == 5: #Legendary class mods
                        self.legendaries += 1
                if self.DrawPs is True:
                    if caller.InventoryRarityLevel == 500: #Pearls
                        self.pearls += 1
                if self.DrawSs is True:
                    if caller.InventoryRarityLevel == 501: #Seraphs
                        self.seraph += 1
                if self.DrawEs is True:
                    if caller.InventoryRarityLevel == 506: #Effervescents
                        self.effervescent += 1
                
                self.rarity = caller.InventoryRarityLevel

                return True

            unrealsdk.RegisterHook("WillowGame.WillowGameViewportClient.PostRender", "Postrender", onPostRender)
            unrealsdk.RegisterHook("WillowGame.PauseGFxMovie.CompleteQuitToMenu", "SaveQuit", onSaveQuit)
            unrealsdk.RegisterHook("Engine.PlayerController.NotifyDisconnect", "QuitWithoutSaving", onQuitWithoutSaving)
            unrealsdk.RegisterHook("WillowGame.WillowPickup.EnableRagdollCollision", "DropCounter", onNewDrop)
            super().Enable()

    def Disable(self) -> None:
        unrealsdk.RemoveHook("WillowGame.WillowGameViewportClient.PostRender", "Postrender")
        unrealsdk.RemoveHook("WillowGame.PauseGFxMovie.CompleteQuitToMenu", "SaveQuit")
        unrealsdk.RemoveHook("Engine.PlayerController.NotifyDisconnect", "QuitWithoutSaving")
        unrealsdk.RemoveHook("WillowGame.WillowPickup.EnableRagdollCollision", "DropCounter")
        super().Disable()

instance = Main()

ModMenu.RegisterMod(instance)