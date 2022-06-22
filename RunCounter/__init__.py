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
    Version: str = "1.0.8"
    SaveEnabledState: ModMenu.EnabledSaveType = ModMenu.EnabledSaveType.LoadWithSettings

    Types: ModMenu.ModTypes = ModMenu.ModTypes.Utility
    SupportedGames: ModMenu.Game = ModMenu.Game.BL2 | ModMenu.Game.TPS

    MainBind = ModMenu.Keybind("Toggle Counter", "Num-7")

    Keybinds = [ MainBind ]

    debug: bool = False

    doCounting: bool = True

    Runs: int = 1
    skipthisDrop: bool = False
    legendaries: int = 0
    pearls: int = 0
    seraph: int = 0
    effervescent: int = 0
    glitch: int = 0
    NumDisplayedCounters: int = 0
    x = 50
    y = 50
    yinc: int = 50
    alpha: int = 255
    rarity: int = 0
    basepath: str = "Mods/RunCounter/Farms/"
    currentFarm: str = "farminfo"
    lastFarm:str = "None"
    itemmodel:str = "nothing to see here"
    trackitem:str = ""
    trackedItemCount:int = 0
    trackedItems: str = []
    trackedItemCounts:int = []
    trackmodes: str = ["Rarity", "Item"]
    #trackmode: str = "Rarity"
    needsupdate: bool = True

    blackcolor = (0, 0, 0, 255)
    whitecolor = (255, 255, 255, alpha)
    goldcolor = (0, 165, 255, alpha)
    raincolor = (0, 0, 0, 255)
    glowin = (50, 10) # idk just tryin stuff
    glowout = (210, 90)


    backgroundImages: str = [
        "None",
        "EngineResources.WhiteSquareTexture",
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
        ]

    def __init__(self) -> None:
        super().__init__()
        self.TextureSlider = ModMenu.Options.Spinner(
            Caption="Background Tex",
            Description="A few to choose from",
            StartingValue = self.backgroundImages[0],
            Choices = self.backgroundImages,
        )
        self.trackingSlider = ModMenu.Options.Spinner(
            Caption="Tracking Mode",
            Description="How to track item drops, add items with .rc item <name of item> in chat",
            StartingValue = self.trackmodes[0],
            Choices = self.trackmodes,
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
        self.currentWidth = ModMenu.Options.Slider(
            Caption="shader width",
            Description="you shouldnt see this",
            StartingValue=100,
            MinValue = 10,
            MaxValue = 10000,
            Increment = 1,
            IsHidden = True
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
                self.trackingSlider,
                self.TextureSlider,
                self.OpacitySlider,
                self.currentWidth,
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
                self.trackingSlider,
                self.TextureSlider,
                self.OpacitySlider,
                self.currentWidth,
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
        if option == self.OpacitySlider:
            self.alpha = new_value
            self.goldcolor = (0, 165, 255, self.alpha)

    def ResetFarm(self, runs, drops) -> None:
        if runs is True:
            self.Runs = 1
        if drops is True:
            self.legendaries = 0
            self.pearls = 0
            self.seraph = 0
            self.effervescent = 0
            self.trackedItemCount = 0
            self.trackitem = ""
            self.lcount.CurrentValue = True
            self.countdrops.CurrentValue = True
            self.countboxes.CurrentValue = True
            if ModMenu.Game.GetCurrent() == ModMenu.Game.BL2:
                self.pcount.CurrentValue = True
                self.scount.CurrentValue = True
                self.ecount.CurrentValue = True
            if ModMenu.Game.GetCurrent() == ModMenu.Game.TPS:
                self.gcount.CurrentValue = True
        self.currentWidth.CurrentValue = 100
        
    def DrawText(self, canvas, text, x, y, color, scalex, scaley) -> None:
        w, h = canvas.TextSize(text, 0, 0)
        if w > self.currentWidth.CurrentValue:
            self.currentWidth.CurrentValue = w + 25
        canvas.SetPos(x, y + self.NumDisplayedCounters * self.yinc, 50)
        canvas.SetDrawColorStruct(color) #b, g, r, a
        canvas.DrawText(text, 1, scalex, scaley, (1, 1, (1, self.blackcolor, self.glowin, self.glowout)))
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
            self.runcount.CurrentValue = farmdata["showRunInfo"]
            self.lcount.CurrentValue = farmdata["showlegendaries"]
            if ModMenu.Game.GetCurrent() == ModMenu.Game.BL2:
                self.pcount.CurrentValue = farmdata["showpearls"]
                self.scount.CurrentValue = farmdata["showseraphs"]
                self.ecount.CurrentValue = farmdata["showeffervescents"]
            if ModMenu.Game.GetCurrent() == ModMenu.Game.TPS:
                self.gcount.CurrentValue = farmdata["showglitches"]
            self.x = farmdata["displayx"]
            self.y = farmdata["displayy"]
            self.countdrops.CurrentValue = farmdata["countEntDrops"]
            self.countboxes.CurrentValue = farmdata["countBoxDrops"]
            self.TextureSlider.CurrentValue = farmdata["bgimg"]
            self.trackingSlider.CurrentValue = str(farmdata["trackanitem"])
            #self.trackmode = farmdata["trackanitem"]
            self.trackedItemCount = farmdata["trackedItemCount"]
            self.trackitem = farmdata["trackitem"]
            self.trackedItems = farmdata["trackeditem"]
            self.trackedItemCounts = farmdata["trackeditemcounts"]
            file.close()
        self.needsupdate = True

    def saveFarm(self, filename) -> None:
        if ModMenu.Game.GetCurrent() == ModMenu.Game.BL2:
            databl2 = {
                "farmname": filename,
                "runs": self.Runs,
                "legendaries":  self.legendaries,
                "pearls": self.pearls,
                "seraphs": self.seraph,
                "effervescents": self.effervescent,
                "showRunInfo": self.runcount.CurrentValue,
                "showlegendaries": self.lcount.CurrentValue,
                "showpearls": self.pcount.CurrentValue,
                "showseraphs": self.scount.CurrentValue,
                "showeffervescents": self.ecount.CurrentValue,
                "displayx": self.x,
                "displayy": self.y,
                "countEntDrops": self.countdrops.CurrentValue,
                "countBoxDrops": self.countboxes.CurrentValue,
                "bgimg": self.TextureSlider.CurrentValue,
                "trackanitem": self.trackingSlider.CurrentValue,
                "trackedItemCount": self.trackedItemCount,
                "trackitem": self.trackitem,
                "trackeditem": self.trackedItems,
                "trackeditemcounts": self.trackedItemCounts
            }
        if ModMenu.Game.GetCurrent() == ModMenu.Game.TPS:    
            datatps = {
                "farmname": filename,
                "runs": self.Runs,
                "legendaries":  self.legendaries,
                "pearls": self.pearls,
                "seraphs": self.seraph,
                "effervescents": self.effervescent,
                "showRunInfo": self.runcount.CurrentValue,
                "showlegendaries": self.lcount.CurrentValue,
                "showglitches": self.gcount.CurrentValue,
                "displayx": self.x,
                "displayy": self.y,
                "countEntDrops": self.countdrops.CurrentValue,
                "countBoxDrops": self.countboxes.CurrentValue,
                "bgimg": self.TextureSlider.CurrentValue,
                "trackanitem": self.trackingSlider.CurrentValue,
                "trackedItemCount": self.trackedItemCount,
                "trackitem": self.trackitem,
                "trackeditem": self.trackedItems,
                "trackeditemcounts": self.trackedItemCounts
            }

        
        if os.path.exists(self.basepath + filename + ".json"):
            os.remove(self.basepath + filename + ".json")

        create = open(self.basepath + filename + ".json", "x")
        if ModMenu.Game.GetCurrent() == ModMenu.Game.BL2:
            farmdata = json.dumps(databl2)
        if ModMenu.Game.GetCurrent() == ModMenu.Game.TPS:
            farmdata = json.dumps(datatps)
        create.write(farmdata)
        create.close()


    def SetLastSessionData(self) -> None:
        data = {
            "farmname": self.currentFarm,
            #"trackingmode": self.trackmode
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

                x = self.x - 15
                y = self.y - 15
                
                canvas.Font = unrealsdk.FindObject("Font", "ui_fonts.font_willowbody_18pt")
                
                self.DrawShader(canvas, x, y, self.currentWidth.CurrentValue, float(50 * self.NumDisplayedCounters) + 20, self.whitecolor, self.TextureSlider.CurrentValue)

                self.NumDisplayedCounters = 0

                if ModMenu.Game.GetCurrent() == ModMenu.Game.BL2:
                    if self.runcount.CurrentValue is True:
                        self.DrawText(canvas, "Farming: " + self.currentFarm, self.x, self.y, self.goldcolor, 1, 1)
                        self.DrawText(canvas, "Run # " + str(self.Runs), self.x, self.y, self.goldcolor, 1, 1)
                        

                    if self.trackingSlider.CurrentValue == "Rarity":
                        if self.lcount.CurrentValue is True:
                            self.DrawText(canvas, "Legendaries: " + str(self.legendaries), self.x, self.y, self.goldcolor, 1, 1)

                        if self.pcount.CurrentValue is True:
                            self.DrawText(canvas, "Pearlescents: " + str(self.pearls), self.x, self.y, self.goldcolor, 1, 1)

                        if self.scount.CurrentValue is True:
                            self.DrawText(canvas, "Seraphs: " + str(self.seraph), self.x, self.y, self.goldcolor, 1, 1)

                        if self.ecount.CurrentValue is True:
                            self.DrawText(canvas, "Effervescents: " + str(self.effervescent), self.x, self.y, self.goldcolor, 1, 1)

                    if self.trackingSlider.CurrentValue == "Item":
                        self.DrawText(canvas, str(self.trackitem) + "s: " + str(self.trackedItemCount), self.x, self.y, self.goldcolor, 1, 1)
                if ModMenu.Game.GetCurrent() == ModMenu.Game.TPS:
                    if self.runcount.CurrentValue is True:
                        self.DrawText(canvas, "Farming: " + self.currentFarm, self.x, self.y, self.goldcolor, 1, 1)
                        self.DrawText(canvas, "Run # " + str(self.Runs), self.x, self.y, self.goldcolor, 1, 1)

                    if self.trackingSlider.CurrentValue == "Rarity":
                        if self.lcount.CurrentValue is True:
                            self.DrawText(canvas, "Legendaries: " + str(self.legendaries), self.x, self.y, self.goldcolor, 1, 1)

                        if self.gcount.CurrentValue is True:
                            self.DrawText(canvas, "Glitch: " + str(self.seraph), self.x, self.y, self.goldcolor, 1, 1)

                    if self.trackingSlider.CurrentValue == "Item":
                        self.DrawText(canvas, str(self.trackitem) + "s: " + str(self.trackedItemCount), self.x, self.y, self.goldcolor, 1, 1)

                if self.debug is True:
                    self.DrawText(canvas, "Rarity: " + str(self.rarity), self.x, self.y, (0, 255, 0, 255), 1, 1)
                    self.DrawText(canvas, "Item 'readable' name: " + str(self.itemmodel), self.x, self.y, (0, 255, 0, 255), 1, 1)
                    self.DrawText(canvas, "tracking slider cur value: " + self.trackingSlider.CurrentValue, self.x, self.y, (0, 255, 0, 255), 1, 1)
                    self.DrawText(canvas, "max text width: " + str(self.currentWidth.CurrentValue), self.x, self.y, (0, 255, 0, 255), 1, 1)
                
                return True

            def onSaveQuit(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> None:
                if self.doCounting is False:
                    return True
                if self.runcount.CurrentValue is True:
                    self.Runs += 1
                self.saveFarm(str(self.currentFarm))
                self.SetLastSessionData()
                return True

            def onQuitWithoutSaving(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
                if self.doCounting is False:
                    return True
                if self.runcount.CurrentValue is True:
                    self.Runs += 1
                self.saveFarm(str(self.currentFarm))
                self.SetLastSessionData()
                return True

            def onNewDrop(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
                if self.doCounting is False:
                    return True

                if self.countdrops.CurrentValue == False:
                    return True

                if self.debug is True:
                    self.rarity = caller.InventoryRarityLevel
                    self.itemmodel = caller.Inventory.GenerateHumanReadableName()

                if self.skipthisDrop is True:
                    self.skipthisDrop = False
                    return True

                if self.trackingSlider.CurrentValue == "Rarity":
                    if self.lcount.CurrentValue is True:
                        if caller.InventoryRarityLevel > 4 and caller.InventoryRarityLevel < 11 and caller.InventoryRarityLevel is not 6: #Legendaries, idk what 6 is but i dont think its one of these
                            self.legendaries += 1
                    if ModMenu.Game.GetCurrent() == ModMenu.Game.BL2:
                        if self.pcount.CurrentValue is True:
                            if caller.InventoryRarityLevel == 500: #Pearls
                                self.pearls += 1
                        if self.scount.CurrentValue is True:
                            if caller.InventoryRarityLevel == 501: #Seraphs & Glitch (tps)
                                self.seraph += 1
                        if self.ecount.CurrentValue is True:
                            if caller.InventoryRarityLevel == 506: #Effervescents
                                self.effervescent += 1
                    if ModMenu.Game.GetCurrent() == ModMenu.Game.TPS:
                        if self.gcount.CurrentValue is True:
                            if caller.InventoryRarityLevel == 501: #Seraphs & Glitch (tps)
                                self.seraph += 1
                else:
                    if caller.Inventory.GenerateHumanReadableName().find(self.trackitem) is not -1:
                        self.trackedItemCount += 1
                

                return True

            def onChestDrop(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> None:
                if self.doCounting is False:
                    return True

                if self.countboxes.CurrentValue == False:
                    return True

                if self.debug is True:
                    self.rarity = caller.InventoryRarityLevel
                    self.itemmodel = caller.Inventory.GenerateHumanReadableName()
                
                if self.trackingSlider.CurrentValue == "Rarity":
                    if self.lcount.CurrentValue is True:
                        if caller.InventoryRarityLevel > 4 and caller.InventoryRarityLevel < 11 and caller.InventoryRarityLevel is not 6: #Legendaries, idk what 6 is but i dont think its one of these
                            self.legendaries += 1
                    if ModMenu.Game.GetCurrent() == ModMenu.Game.BL2:
                        if self.pcount.CurrentValue is True:
                            if caller.InventoryRarityLevel == 500: #Pearls
                                self.pearls += 1
                        if self.scount.CurrentValue is True:
                            if caller.InventoryRarityLevel == 501: #Seraphs & Glitch (tps)
                                self.seraph += 1
                        if self.ecount.CurrentValue is True:
                            if caller.InventoryRarityLevel == 506: #Effervescents
                                self.effervescent += 1
                    if ModMenu.Game.GetCurrent() == ModMenu.Game.TPS:
                        if self.gcount.CurrentValue is True:
                            if caller.InventoryRarityLevel == 501: #Seraphs & Glitch (tps)
                                self.seraph += 1
                else:
                    if caller.Inventory.GenerateHumanReadableName().find(self.trackitem) is not -1:
                        self.trackedItemCount += 1

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
                        self.trackingSlider.CurrentValue = "Rarity"
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
                            self.runcount.CurrentValue = not self.runcount.CurrentValue
                        elif splitstring[2].lower() == "enemy":
                            self.countdrops.CurrentValue = not self.countdrops.CurrentValue
                        elif splitstring[2].lower() == "chest":
                            self.countboxes.CurrentValue = not self.countboxes.CurrentValue
                        elif splitstring[2].lower() == "l":
                            self.lcount.CurrentValue = not self.lcount.CurrentValue
                        elif splitstring[2].lower() == "p":
                            self.pcount.CurrentValue = not self.pcount.CurrentValue
                        elif splitstring[2].lower() == "s":
                            self.scount.CurrentValue = not self.scount.CurrentValue
                        elif splitstring[2].lower() == "e":
                            self.ecount.CurrentValue = not self.ecount.CurrentValue
                        elif splitstring[2].lower() == "g":
                            self.gcount.CurrentValue = not self.gcount.CurrentValue
                    elif splitstring[1].lower() == "x":
                        self.x = int(splitstring[2])
                    elif splitstring[1].lower() == "y":
                        self.y = int(splitstring[2])
                    elif splitstring[1].lower() == "a":
                        self.alpha = int(splitstring[2])
                    elif splitstring[1].lower() == "w":
                        self.currentWidth.CurrentValue = int(splitstring[2])
                    elif splitstring[1].lower() == "help":
                        if splitstring[2].lower() == "create":
                            unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say Create usage: .rc create <farm name>, Makes a new tracked farm", 0)
                        elif splitstring[2].lower() == "load":
                            unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say Load usage: .rc load <farm name>, Opens a previously made farm", 0)
                        elif splitstring[2].lower() == "reset":
                            unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say Reset usage: .rc Reset <Runs/Drops>, Will reset either run count or drop count in currently loaded farm", 0)
                        elif splitstring[2].lower() == "toggle":
                            unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say Toggle usage: .rc toggle <enemy/chest/r/l/p/s/e/g>, toggles item tracking modes, or toggles the display of certain counters for current farm", 0)
                        elif splitstring[2].lower() == "delete":
                            unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say Delete usage: .rc delete <farm name>, Removes all saved data for specified farm", 0)
                        elif splitstring[2].lower() == "me": 
                            unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say Run Counter Prefix: .rc, Commands: Create, Load, Reset, Toggle, Delete, X, Y, A, W, Item, Back", 0)
                        elif splitstring[2].lower() == "x": 
                            unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say X Usage: .rc X <number>, sets the pixel x value for the display, 50 by default", 0)
                        elif splitstring[2].lower() == "y": 
                            unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say Y Usage: .rc Y <number>, sets the pixel y value for the display, 50 by default", 0)
                        elif splitstring[2].lower() == "a": 
                            unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say A Usage: .rc A <number>, sets the alpha value for the display 20-255, 255 by default", 0)
                        elif splitstring[2].lower() == "item": 
                            unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say item Usage: .rc item <item name>, sets the current item being tracked and switches to item mode", 0)
                        elif splitstring[2].lower() == "w": 
                            unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say w Usage: .rc w <shader width>, sets the current background width, yes this is a bad workaround that shouldnt exist", 0)
                        elif splitstring[2].lower() == "back": 
                            unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("say Back Usage: .rc back <Texture2D Name>, sets the current background shader", 0)
                    elif splitstring[1].lower() == "back":
                        self.TextureSlider.CurrentValue = splitstring[2]
                    elif splitstring[1].lower() == "item":
                        self.trackingSlider.CurrentValue = "Item"
                        self.trackitem = splitstring[2]
                        #self.lcount.CurrentValue = False
                        #if ModMenu.Game.GetCurrent() == ModMenu.Game.TPS:
                            #self.pcount.CurrentValue = False
                            #self.scount.CurrentValue = False
                            #self.ecount.CurrentValue = False
                        #if ModMenu.Game.GetCurrent() == ModMenu.Game.TPS:
                            #self.gcount.CurrentValue = False
                    elif splitstring[1].lower() == "debug":
                        self.debug = not self.debug

                
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
        self.saveFarm(str(self.currentFarm))
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