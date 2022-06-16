import json
import os
import unrealsdk

from Mods import ModMenu

class Main(ModMenu.SDKMod):
    Name: str = "Run Counter"
    Description: str = "<font size='20' color='#ffa600'>Run Counter</font>\n\n" \
    "Adds 1 to the counter on save quit\n" \
        "Drop Counter will count any dropped object of at least legendary rarity\n\n" \
            "Counters only increment while being drawn\n\n" \
                "Main toggle hotkey is Num-7 by default\n\n"
    Author: str = "PyrexBLJ"
    Version: str = "1.0.5"
    SaveEnabledState: ModMenu.EnabledSaveType = ModMenu.EnabledSaveType.LoadWithSettings

    Types: ModMenu.ModTypes = ModMenu.ModTypes.Utility
    SupportedGames: ModMenu.Game = ModMenu.Game.BL2 | ModMenu.Game.TPS

    MainBind = ModMenu.Keybind("Toggle Counter", "Num-7")

    Keybinds = [ MainBind ]

    doCounting: bool = True

    countRagdollDrops: bool = True
    countContainerDrops: bool = True

    Runs: int = 1
    DrawCounter: bool = True
    DrawLs: bool = True
    DrawPs: bool = True
    DrawSs: bool = True
    DrawEs: bool = True
    DrawGs: bool = True
    skipthisDrop: bool = False
    legendaries: int = 0
    pearls: int = 0
    seraph: int = 0
    effervescent: int = 0
    glitch: int = 0
    NumDisplayedCounters: int = 0
    x: int = 50
    y: int = 50
    yinc: int = 50
    alpha: int = 255
    rarity: int = 0
    basepath: str = "Mods/RunCounter/Farms/"
    currentFarm: str = "farminfo"
    lastFarm:str = "None"
    itemmodel:str = "nothing to see here"

    blackcolor = (0, 0, 0, 255)
    whitecolor = (255, 255, 255, 255)
    goldcolor = (0, 165, 255, alpha)

    background: str = "fx_shared_items.Textures.Customization_Skin"

    backgroundImages: str = [
        "fx_shared_items.Textures.Customization_Skin", 
        "fx_shared_items.Textures.Customization_Head", 
        "EngineMaterials.DefaultDiffuse", 
        "WillowHUD.Textures.Fixed_Marker_Flag", 
        "FX_Shared_Smoke.Textures.Tex_Fractal_Cloud", 
        "UI_Popup_DialogBox.DialogBox_I12", 
        "fx_shared_items.Textures.CommDeck_Dif",
        "FX_ENV_Misc.Textures.StarNebula_Dif", 
        "FX_Shared_Tech.Textures.Tex_Shield_Triangle_Pattern", 
        "FX_ENV_Misc.Textures.MissionSelect_Dif",
        "FX_Shared_Energy.Textures.Assassin_Dash_Screen_Tex",
        "Common_GunMaterials.Patterns.Pattern_JakobsEpic_SpaltedMaple", 
        "Common_GunMaterials.Patterns.Pattern_Jakobs_CaseHardened",
        "Common_GunMaterials.Patterns.Pattern_JakobsEpic_Zebrawood",
        "Common_GunMaterials.Logos.Logo_Logan5th",
        ""
        ]

    def __init__(self) -> None:
        super().__init__()
        self.TextureSlider = ModMenu.Options.Spinner(
            Caption="Background Tex",
            Description="A few to choose from",
            StartingValue = self.backgroundImages[0],
            Choices = self.backgroundImages,
        )
        self.OpacitySlider = ModMenu.Options.Slider(
            Caption="Text Opacity",
            Description="How see-thru the text is",
            StartingValue = 255,
            MinValue = 20,
            MaxValue = 255,
            Increment = 1,
        )
        self.countdrops = ModMenu.Options.Boolean(
            Caption="Count Enemy Drops",
            Description="Turn the counter on and off",
            StartingValue=True,
            Choices=["No", "Yes"]  # False, True
        )
        self.countboxes = ModMenu.Options.Boolean(
            Caption="Count Chest Drops",
            Description="Turn the counter on and off",
            StartingValue=True,
            Choices=["No", "Yes"]  # False, True
        )
        self.runcount = ModMenu.Options.Boolean(
            Caption="Draw Counter",
            Description="Turn the counter on and off",
            StartingValue=True,
            Choices=["No", "Yes"]  # False, True
        )
        self.lcount = ModMenu.Options.Boolean(
            Caption="Draw Legendary Drop Counter",
            Description="Turn the drop counter on and off",
            StartingValue=True,
            Choices=["No", "Yes"]  # False, True
        )
        if ModMenu.Game.GetCurrent() == ModMenu.Game.BL2:
            self.pcount = ModMenu.Options.Boolean(
                Caption="Draw Pearlescent Drop Counter",
                Description="Turn the drop counter on and off",
                StartingValue=True,
                Choices=["No", "Yes"]  # False, True
            )
            self.scount = ModMenu.Options.Boolean(
                Caption="Draw Seraph Drop Counter",
                Description="Turn the drop counter on and off",
                StartingValue=True,
                Choices=["No", "Yes"]  # False, True
            )
            self.ecount = ModMenu.Options.Boolean(
                Caption="Draw Effervescent Drop Counter",
                Description="Turn the drop counter on and off",
                StartingValue=True,
                Choices=["No", "Yes"]  # False, True
            )
            self.Options = [
                self.TextureSlider,
                self.OpacitySlider,
                self.countdrops,
                self.countboxes,
                self.runcount,
                self.lcount,
                self.pcount,
                self.scount,
                self.ecount
            ]
        if ModMenu.Game.GetCurrent() == ModMenu.Game.TPS:
            self.gcount = ModMenu.Options.Boolean(
                Caption="Draw Glitch Drop Counter",
                Description="Turn the drop counter on and off",
                StartingValue=True,
                Choices=["No", "Yes"]  # False, True
            )
            self.Options = [
                self.TextureSlider,
                self.OpacitySlider,
                self.countdrops,
                self.countboxes,
                self.runcount,
                self.lcount,
                self.gcount
            ]

        

    def GameInputPressed(self, bind: ModMenu.Keybind, event: ModMenu.InputEvent) -> None:
        if bind == self.MainBind and event == ModMenu.InputEvent.Pressed:
            self.doCounting = not self.doCounting


    def ModOptionChanged(self, option: ModMenu.Options.Base, new_value) -> None:
        if option == self.TextureSlider:
            self.background = new_value
        if option == self.OpacitySlider:
            self.alpha = new_value
            self.goldcolor = (0, 165, 255, self.alpha)
        if option == self.countdrops:
            self.countRagdollDrops = new_value
        if option == self.countboxes:
            self.countContainerDrops = new_value

        if option == self.runcount:
            self.DrawCounter = new_value
        if option == self.lcount:
            self.DrawLs = new_value
        
        if ModMenu.Game.GetCurrent() == ModMenu.Game.BL2:
            if option == self.pcount:
                self.DrawPs = new_value
            if option == self.scount:
                self.DrawSs = new_value
            if option == self.ecount:
                self.DrawEs = new_value

        if ModMenu.Game.GetCurrent() == ModMenu.Game.TPS:
            if option == self.gcount:
                self.DrawGs = new_value

    def ResetFarm(self, runs, drops) -> None:
        if runs is True:
            self.Runs = 1
        if drops is True:
            self.legendaries = 0
            self.pearls = 0
            self.seraph = 0
            self.effervescent = 0
        
    def DrawText(self, canvas, text, x, y, color, scalex, scaley) -> None:
        canvas.Font = unrealsdk.FindObject("Font", "ui_fonts.font_willowbody_18pt")
        yval = y + self.NumDisplayedCounters * self.yinc
        canvas.SetPos(x, yval, 0)
        canvas.SetDrawColorStruct(color) #b, g, r, a
        canvas.DrawText(text, False, scalex, scaley, ())
        self.NumDisplayedCounters += 1

    def DrawShader(self, canvas, x, y, w, h, color, shader) -> None:
        tex = unrealsdk.FindObject("Texture2D", shader)

        canvas.SetPos(x, y, 0)
        canvas.SetDrawColorStruct(color) #b, g, r, a
        canvas.DrawRect(w, h, tex)

    def loadFarm(self, filename) -> None:
        if os.path.exists(self.basepath + filename + ".json") is True:
            file = open(self.basepath + filename + ".json")
            farmdata = json.loads(file.read())
            self.currentFarm = farmdata["farmname"]
            self.Runs = farmdata["runs"]
            self.legendaries = farmdata["legendaries"]
            self.pearls = farmdata["pearls"]
            self.seraph = farmdata["seraphs"]
            self.effervescent = farmdata["effervescents"]
            self.DrawCounter = farmdata["showRunInfo"]
            self.DrawLs = farmdata["showlegendaries"]
            self.DrawPs = farmdata["showpearls"]
            self.DrawSs = farmdata["showseraphs"]
            self.DrawEs = farmdata["showeffervescents"]
            self.DrawGs = farmdata["showglitches"]
            self.x = farmdata["displayx"]
            self.y = ["displayy"]
            self.countRagdollDrops = farmdata["countEntDrops"]
            self.countContainerDrops = farmdata["countBoxDrops"]
            self.background = farmdata["bgimg"]
            file.close()

    def saveFarm(self, filename) -> None:
        data = {
            "farmname": filename,
            "runs": self.Runs,
            "legendaries":  self.legendaries,
            "pearls": self.pearls,
            "seraphs": self.seraph,
            "effervescents": self.effervescent,
            "showRunInfo": self.DrawCounter,
            "showlegendaries": self.DrawLs,
            "showpearls": self.DrawPs,
            "showseraphs": self.DrawSs,
            "showeffervescents": self.DrawEs,
            "showglitches": self.DrawGs,
            "displayx": self.x,
            "displayy": self.y,
            "countEntDrops": self.countRagdollDrops,
            "countBoxDrops": self.countContainerDrops,
            "bgimg": self.background
        }
        if os.path.exists(self.basepath + filename + ".json"):
            os.remove(self.basepath + filename + ".json")

            create = open(self.basepath + filename + ".json", "x")
            farmdata = json.dumps(data)
            create.write(farmdata)
            create.close()
        else:
            create = open(self.basepath + filename + ".json", "x")
            farmdata = json.dumps(data)
            create.write(farmdata)
            create.close()

    def SetLastSessionData(self) -> None:
        data = {
            "farmname": self.currentFarm
        }
        if os.path.exists(self.basepath + "defaultfarminfo.json"):
            os.remove(self.basepath + "defaultfarminfo.json")

        file = open(self.basepath + "defaultfarminfo.json", "w")
        farmdata = json.dumps(data)
        file.write(farmdata)
        file.close()

    def GetLastSessionData(self) -> None:
         if os.path.exists(self.basepath + "defaultfarminfo.json"):
            file = open(self.basepath + "defaultfarminfo.json")
            farmdata = json.loads(file.read())
            self.lastFarm = farmdata["farmname"]
            file.close()


    def Enable(self) -> None:
            if os.path.isdir(self.basepath) is False:
                os.mkdir(self.basepath)
            self.GetLastSessionData()
            self.loadFarm(self.lastFarm)
            def onPostRender(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
                if self.doCounting is False:
                    return True

                if not params.Canvas:
                    return True

                canvas = params.Canvas

                self.NumDisplayedCounters = 0

                if ModMenu.Game.GetCurrent() == ModMenu.Game.BL2:
                    if self.DrawCounter is True:
                        self.DrawShader(canvas, self.x - 25, self.y - 25, 400, 350, self.whitecolor, self.background)
                        self.DrawText(canvas, "Farming: " + self.currentFarm, self.x, self.y, self.goldcolor, 1, 1)
                        self.DrawText(canvas, "Run # " + str(self.Runs), self.x, self.y, self.goldcolor, 1, 1)

                    if self.DrawLs is True:
                        self.DrawText(canvas, "Legendaries: " + str(self.legendaries), self.x, self.y, self.goldcolor, 1, 1)

                    if self.DrawPs is True:
                        self.DrawText(canvas, "Pearlescents: " + str(self.pearls), self.x, self.y, self.goldcolor, 1, 1)

                    if self.DrawSs is True:
                        self.DrawText(canvas, "Seraphs: " + str(self.seraph), self.x, self.y, self.goldcolor, 1, 1)

                    if self.DrawEs is True:
                        self.DrawText(canvas, "Effervescents: " + str(self.effervescent), self.x, self.y, self.goldcolor, 1, 1)
                if ModMenu.Game.GetCurrent() == ModMenu.Game.TPS:
                    if self.DrawCounter is True:
                        self.DrawShader(canvas, self.x - 25, self.y - 25, 200, 200, self.whitecolor, self.background)
                        self.DrawText(canvas, "Farming: " + self.currentFarm, self.x, self.y, self.goldcolor, 1, 1)
                        self.DrawText(canvas, "Run # " + str(self.Runs), self.x, self.y, self.goldcolor, 1, 1)

                    if self.DrawLs is True:
                        self.DrawText(canvas, "Legendaries: " + str(self.legendaries), self.x, self.y, self.goldcolor, 1, 1)

                    if self.DrawGs is True:
                        self.DrawText(canvas, "Glitch: " + str(self.seraph), self.x, self.y, self.goldcolor, 1, 1)

                #self.DrawText(canvas, "Rarity: " + str(self.rarity), self.x, self.y, (0, 165, 255, 255), 1, 1)
                #self.DrawText(canvas, "Item Model: " + str(self.itemmodel), self.x, self.y, (0, 165, 255, self.alpha), 1, 1)
                
                return True

            def onSaveQuit(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> None:
                if self.doCounting is False:
                    return True
                if self.DrawCounter is True:
                    self.Runs += 1
                self.saveFarm(str(self.currentFarm))
                self.SetLastSessionData()
                return True

            def onQuitWithoutSaving(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
                if self.doCounting is False:
                    return True
                if self.DrawCounter is True:
                    self.Runs += 1
                self.saveFarm(str(self.currentFarm))
                self.SetLastSessionData()
                return True

            def onNewDrop(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
                if self.doCounting is False:
                    return True

                if self.countRagdollDrops is False:
                    return True

                if self.skipthisDrop is True:
                    self.rarity = caller.InventoryRarityLevel
                    self.skipthisDrop = False
                    return True

                if self.DrawLs is True:
                    if caller.InventoryRarityLevel > 4 and caller.InventoryRarityLevel < 11 and caller.InventoryRarityLevel is not 6: #Legendaries, idk what 6 is but i dont think its one of these
                        self.legendaries += 1
                if self.DrawPs is True:
                    if caller.InventoryRarityLevel == 500: #Pearls
                        self.pearls += 1
                if self.DrawSs is True or self.DrawGs is True:
                    if caller.InventoryRarityLevel == 501: #Seraphs & Glitch (tps)
                        self.seraph += 1
                if self.DrawEs is True:
                    if caller.InventoryRarityLevel == 506: #Effervescents
                        self.effervescent += 1
                
                self.rarity = caller.InventoryRarityLevel
                self.itemmodel = caller.Inventory.GenerateHumanReadableName()

                return True

            def onChestDrop(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> None:
                if self.doCounting is False:
                    return True

                if self.countContainerDrops is False:
                    return True

                if self.DrawLs is True:
                    if caller.InventoryRarityLevel > 4 and caller.InventoryRarityLevel < 11 and caller.InventoryRarityLevel is not 6: #Legendaries, idk what 6 is but i dont think its one of these
                        self.legendaries += 1
                if self.DrawPs is True:
                    if caller.InventoryRarityLevel == 500: #Pearls
                        self.pearls += 1
                if self.DrawSs is True or self.DrawGs is True:
                    if caller.InventoryRarityLevel == 501: #Seraphs & Glitch (tps)
                        self.seraph += 1
                if self.DrawEs is True:
                    if caller.InventoryRarityLevel == 506: #Effervescents
                        self.effervescent += 1
                
                self.rarity = caller.InventoryRarityLevel
                self.itemmodel = caller.Inventory.GenerateHumanReadableName()

                return True

            def onChatCommand(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
                if self.doCounting is False and params.msg.lower().startswith(".rc") is True:
                    unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say Please toggle the main keybind to use the chat commands", 0)
                    return True

                if params.msg.lower().startswith(".rc") is True:
                    splitstring = params.msg.split(" ", 2)
                    if splitstring[1].lower() == "create":
                        self.saveFarm(splitstring[2])
                        self.ResetFarm(True, True)
                        self.currentFarm = splitstring[2]
                        self.SetLastSessionData()
                    elif splitstring[1].lower() == "load":
                        self.loadFarm(splitstring[2])
                        self.SetLastSessionData()
                    elif splitstring[1].lower() == "delete":
                        if os.path.exists(self.basepath + splitstring[2] + ".json") is True:
                            os.remove(self.basepath + splitstring[2] + ".json")
                    elif splitstring[1].lower() == "reset":
                        if splitstring[2].lower() == "runs":
                            self.ResetFarm(True, False)
                        if splitstring[2].lower() == "drops":
                            self.ResetFarm(False, True)
                    elif splitstring[1].lower() == "toggle":
                        if splitstring[2].lower() == "r":
                            self.DrawCounter = not self.DrawCounter
                        elif splitstring[2].lower() == "enemy":
                            self.countRagdollDrops = not self.countRagdollDrops
                        elif splitstring[2].lower() == "chest":
                            self.countContainerDrops = not self.countContainerDrops
                        elif splitstring[2].lower() == "l":
                            self.DrawLs = not self.DrawLs
                        elif splitstring[2].lower() == "p":
                            self.DrawPs = not self.DrawPs
                        elif splitstring[2].lower() == "s":
                            self.DrawSs = not self.DrawSs
                        elif splitstring[2].lower() == "e":
                            self.DrawEs = not self.DrawEs
                        elif splitstring[2].lower() == "g":
                            self.DrawGs = not self.DrawGs
                    elif splitstring[1].lower() == "x":
                        self.x = int(splitstring[2])
                    elif splitstring[1].lower() == "y":
                        self.y = int(splitstring[2])
                    elif splitstring[1].lower() == "a":
                        self.alpha = int(splitstring[2])
                    elif splitstring[1].lower() == "help":
                        if splitstring[2].lower() == "create":
                            unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say Create usage: .rc create name, Makes a new tracked farm", 0)
                        elif splitstring[2].lower() == "load":
                            unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say Load usage: .rc load name, Opens a previously made farm", 0)
                        elif splitstring[2].lower() == "reset":
                            unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say Reset usage: .rc Reset Runs/Drops, Will reset either run count or drop count in currently loaded farm", 0)
                        elif splitstring[2].lower() == "toggle":
                            unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say Toggle usage: .rc toggle enemy/chest  r/l/p/s/e/g, toggles if the current farm tracks enemy or chest drops, or toggles the display of certain counters for current farm", 0)
                        elif splitstring[2].lower() == "delete":
                            unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say Delete usage: .rc delete name, Removes all saved data for specified farm", 0)
                        elif splitstring[2].lower() == "me": 
                            unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say Run Counter Prefix: .rc, Commands: Create, Load, Reset, Toggle, Delete, X, Y, A", 0)
                        elif splitstring[2].lower() == "x": 
                            unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say X Usage: .rc X number, sets the pixel x value for the display, 50 by default", 0)
                        elif splitstring[2].lower() == "y": 
                            unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say Y Usage: .rc Y number, sets the pixel y value for the display, 50 by default", 0)
                        elif splitstring[2].lower() == "a": 
                            unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say A Usage: .rc A number, sets the alpha value for the display 20-255, 255 by default", 0)
                    elif splitstring[1].lower() == "back":
                        self.background = splitstring[2]
                
                return True 

            def onIDroppedSomething(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
                if self.doCounting is False:
                    return True
                self.skipthisDrop = True
                return True

            unrealsdk.RegisterHook("WillowGame.WillowGameViewportClient.PostRender", "Postrender", onPostRender)
            unrealsdk.RegisterHook("WillowGame.PauseGFxMovie.CompleteQuitToMenu", "SaveQuit", onSaveQuit)
            unrealsdk.RegisterHook("Engine.PlayerController.NotifyDisconnect", "QuitWithoutSaving", onQuitWithoutSaving)
            unrealsdk.RegisterHook("WillowGame.WillowPickup.EnableRagdollCollision", "DropCounter", onNewDrop)
            unrealsdk.RegisterHook("WillowGame.TextChatGFxMovie.AddChatMessage", "ChatCommands", onChatCommand)
            unrealsdk.RegisterHook("WillowGame.WillowWeapon.DropFrom", "NotMyDrops", onIDroppedSomething)
            unrealsdk.RegisterHook("WillowGame.WillowPickup.AdjustPickupPhysicsAndCollisionForBeingAttached", "ChestDrops", onChestDrop)
            super().Enable()

    def Disable(self) -> None:
        unrealsdk.RemoveHook("WillowGame.WillowGameViewportClient.PostRender", "Postrender")
        unrealsdk.RemoveHook("WillowGame.PauseGFxMovie.CompleteQuitToMenu", "SaveQuit")
        unrealsdk.RemoveHook("Engine.PlayerController.NotifyDisconnect", "QuitWithoutSaving")
        unrealsdk.RemoveHook("WillowGame.WillowPickup.EnableRagdollCollision", "DropCounter")
        unrealsdk.RemoveHook("WillowGame.TextChatGFxMovie.AddChatMessage", "ChatCommands")
        unrealsdk.RemoveHook("WillowGame.WillowWeapon.DropFrom", "NotMyDrops")
        unrealsdk.RemoveHook("WillowGame.WillowPickup.AdjustPickupPhysicsAndCollisionForBeingAttached", "ChestDrops")
        super().Disable()

instance = Main()

ModMenu.RegisterMod(instance)