import unrealsdk

from Mods import ModMenu

class Main(ModMenu.SDKMod):
    Name: str = "Super Screenshot"
    Description: str = "<font size='20' color='#00ffe8'>Super Screenshot</font>\n\n" \
    "Take high resolution screenshots, higher than your games resolution"
    Author: str = "Pyrex"
    Version: str = "1.0.0"
    SaveEnabledState: ModMenu.EnabledSaveType = ModMenu.EnabledSaveType.LoadWithSettings

    Types: ModMenu.ModTypes = ModMenu.ModTypes.Utility
    SupportedGames: ModMenu.Game = ModMenu.Game.TPS | ModMenu.Game.BL2

    ScreenshotBind = ModMenu.Keybind("High Res Screenshot", "F18")

    canvas = None

    ScreenshotSizes: str = [ "1440 - 2K", "2160 - 4K", "4320 - 8K", "8640 - 16K"]

    Keybinds = [ ScreenshotBind ]

    def __init__(self) -> None:
        self.scSizeSlider = ModMenu.Options.Spinner(
            Caption="Screenshot Resolution",
            Description="yea ik its a bit excessive idc",
            StartingValue = self.ScreenshotSizes[2],
            Choices = self.ScreenshotSizes,
        )
        self.Options = [
                self.scSizeSlider
            ]
        super().__init__()

    def GameInputPressed(self, bind: ModMenu.Keybind, event: ModMenu.InputEvent) -> None:
        if bind == self.ScreenshotBind and event == ModMenu.InputEvent.Pressed:
            if int(self.scSizeSlider.CurrentValue.split()[0]) > int(self.canvas.SizeY):
                unrealsdk.GetEngine().GamePlayers[0].Actor.UberDOFEffect.VignetteEnabled = 0
                unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("tiledshot " + str(round(int(self.scSizeSlider.CurrentValue.split()[0]) / int(self.canvas.SizeY))), 0)
                #unrealsdk.GetEngine().GamePlayers[0].Actor.UberDOFEffect.VignetteEnabled = 1 #reenabling directly after calling the console command is too soon, tiles the vignette in the screenshot
            else: unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say Requested screenshot less than or equal to game resolution, use steam/epic screenshot or increase requested size in settings.", 0)

    def Enable(self) -> None:
        def render(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> None:
            self.canvas = params.Canvas
            return True

        unrealsdk.RegisterHook("WillowGame.WillowGameViewportClient.PostRender", "Rendering", render)
        super().Enable()

    def Disable(self) -> None:
        unrealsdk.RemoveHook("WillowGame.WillowGameViewportClient.PostRender", "Rendering")
        super().Disable()

instance = Main()

ModMenu.RegisterMod(instance)