import unrealsdk

from Mods import ModMenu

class Main(ModMenu.SDKMod):
    """
    Changes mouse and controller sensitivity by a percentage on weapon zoom in and out.
    """
    Name: str = "ADS Sensitivity"
    Description: str = "<font size='20' color='#00ffe8'>ADS Sensitivity</font>\n" \
            "Automatically changes sensitivity for mouse and controller when aiming down sights." \
            "\nChange rate can be modified in mod settings." \
            "\nToggle Snipers only in mod settings."
    Author: str = "PyrexBLJ, Siggles"
    Version: str = "1.1.0"
    SaveEnabledState: ModMenu.EnabledSaveType = ModMenu.EnabledSaveType.LoadWithSettings

    Types: ModMenu.ModTypes = ModMenu.ModTypes.Utility
    SupportedGames: ModMenu.Game = ModMenu.Game.BL2 | ModMenu.Game.TPS

    # Mouse Sensitivity
    defaultMouseSense: float #= 60
    # Controller Sensitivity
    defaultControllerX: float
    defaultControllerY: float
    # Changes
    aimRate = 100
    sniperOnly = False

    def __init__(self) -> None:
        super().__init__()
        self.MySlider = ModMenu.Options.Slider(
            Caption="Aim Modifier",
            Description="Percentage of normal sensitivity when ADS, from 10%-500% (100% is no change)",
            StartingValue = 100,
            MinValue = 10,
            MaxValue = 500,
            Increment = 10,
        )
        self.MyBoolean = ModMenu.Options.Boolean(
            Caption="Snipers Only",
            Description="If YES, only affects ADS with Snipers",
            StartingValue=False,
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
            self.sniperOnly = new_value
    
    
    @ModMenu.Hook("WillowGame.WillowScrollingListDataProviderKeyboardMouseOptions.OnPop")   # On exiting the KB/M options menu
    def MouseChanged(self, caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
        # The updated values don't get updated in the player Actor until we exit the menu, so we need to get new settings directly.
        playerSettings = params.TheList.MyOwnerMovie.WPCOwner.GetProfileSettings()
        self.defaultMouseSense = playerSettings.GetProfileSettingValueInt(121, 0)[1]
        return True
    
    @ModMenu.Hook("WillowGame.WillowScrollingListDataProviderGamepadOptions.OnPop")   # On exiting the controller options menu
    def ControllerChanged(self, caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
        # The updated values don't get updated in the player Actor until we exit the menu, so we need to get new settings directly.
        playerSettings = params.TheList.MyOwnerMovie.WPCOwner.GetProfileSettings()
        newX=playerSettings.GetProfileSettingValueInt(102, 0)[1]
        newY=playerSettings.GetProfileSettingValueInt(103, 0)[1]
        newX=0.25*(1+newX)  # CBA find where this mapping comes from
        newY=0.25*(1+newY)
        self.defaultControllerX = newX
        self.defaultControllerY = newY

        return True

    @ModMenu.Hook("WillowGame.WillowWeapon.SetZoomState")
    def ZoomChange(self, caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
        if (not self.sniperOnly) or self.IsValidWeaponType(caller):
            # ZoomState enums are:
            #   ZOOMED_OUT = 0
            #   ZOOMING_IN = 1
            #   ZOOMED_IN = 2
            #   ZOOMING_OUT = 3
            if params.NewZoomState == 2:
                # Zoomed In
                controller = unrealsdk.GetEngine().GamePlayers[0].Actor
                controller.PlayerInput.MouseSensitivity = self.defaultMouseSense * (self.aimRate / 100)
                controller.PlayerInput.ControllerSensitivityX = self.defaultControllerX * (self.aimRate / 100)
                controller.PlayerInput.ControllerSensitivityY = self.defaultControllerY * (self.aimRate / 100)
            elif params.NewZoomState == 0:
                # Zoomed Out
                controller = unrealsdk.GetEngine().GamePlayers[0].Actor
                controller.PlayerInput.MouseSensitivity = self.defaultMouseSense
                controller.PlayerInput.ControllerSensitivityX = self.defaultControllerX
                controller.PlayerInput.ControllerSensitivityY = self.defaultControllerY

        return True

    def IsValidWeaponType(self, item: unrealsdk.UObject) -> bool:
        # The WeaponType is actually stored in the Weapon's DefinitionData attributes
        # Nicked from EquipLocker mod https://github.com/apple1417/bl-sdk-mods/blob/master/EquipLocker/RestrictionSets/weap_item_type.py
        if item.DefinitionData.WeaponTypeDefinition is None:
            return False
        weap_type = item.DefinitionData.WeaponTypeDefinition.WeaponType
        # WeaponType enums are:
        #   WT_Pistol,
        #   WT_Shotgun,  
        #   WT_SMG,
        #   WT_SniperRifle,
        #   WT_AssaultRifle,
        #   WT_RocketLauncher,
        #   WT_MAX
        if weap_type == 3:  # Sniper weapon type only
            return True

        return False

    def Enable(self) -> None:
        controller = unrealsdk.GetEngine().GamePlayers[0].Actor
        self.defaultMouseSense = controller.PlayerInput.MouseSensitivity
        self.defaultControllerX = controller.PlayerInput.ControllerSensitivityX
        self.defaultControllerY = controller.PlayerInput.ControllerSensitivityY
        super().Enable()

    def Disable(self) -> None:
        super().Disable()


instance = Main()

ModMenu.RegisterMod(instance)
