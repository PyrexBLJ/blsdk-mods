import json
from os import path
import random
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Optional, Tuple

import unrealsdk  # type: ignore

from Mods import ModMenu

from . import Looties, map_scripts, maps, mission_display, util
from .game_state import ClaimRewardBind, DebugBind, GameState, ResetRunBind, RespecBind

try:
    from Mods.MapLoader import placeablehelper
except ImportError:
    import webbrowser

    webbrowser.open("https://bl-sdk.github.io/mods/MapLoader/")
    raise ImportError("Roguelands requires the most recent version of MapLoader to be installed")

try:
    import Mods.UserFeedback as uFeed
except ImportError:
    import webbrowser

    webbrowser.open("https://bl-sdk.github.io/mods/UserFeedback/")
    raise ImportError("Roguelands requires the most recent version of UserFeedback to be installed")


from .maps import MAP_DATA, MISSION_TYPE_READABLE, MapData, MapType

EXCLUDED_ENEMIES: List[str] = [
    "AIClassDefinition GD_RolandSoldier.Character.CharClass_RolandSoldier",
    "AIClassDefinition GD_Anemone_InfectShared.Character.CharClass_InfectedPod_Static",
    "AIClassDefinition GD_Anemone_InfectedPodTendril.Character.CharClass_InfectedPodTendril",
    "None",
]

# rewards
REWARD_POOLS = {
    MapType.Mobbing: [
        "GD_Itempools.WeaponPools.Pool_Weapons_All_04_Rare",
        "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare",
        "GD_CustomItemPools_MainGame.Siren.TedioreUncommon",
    ],
    MapType.MiniBoss: [
        "GD_Itempools.ClassModPools.Pool_ClassMod_04_Rare",
        "GD_Itempools.ClassModPools.Pool_ClassMod_04_Rare",
        "GD_Lobelia_Itempools.ClassModPools.Pool_ClassMod_Lobelia_All",
    ],
    MapType.RedBarBoss: [
        "GD_Itempools.WeaponPools.Pool_Weapons_All_05_VeryRare",
        "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_06_Legendary",
    ],
    MapType.RaidBoss: ["GD_CustomItemPools_MainGame.Mercenary.TedioreUncommon"],
    MapType.MiniGame: "",
    MapType.Special: "",
}

DIFFICULTY: List[str] = ["Easy", "Normal", "Hard"]

'''def call_logger(func):
    def wrapper(*args, **kwargs):
        _cls = args[0].__class__.__name__
        unrealsdk.Log(f"*** Called: {_cls}.{func.__name__} ***")
        res = func(*args, **kwargs)
        unrealsdk.Log(f"*** End function  ***")
        return res

    return wrapper


def log_all_calls(decorator):
    def decorate(cls):
        for name, obj in vars(cls).items():
            if callable(obj):
                setattr(cls, name, decorator(obj))
        return cls

    return decorate

@log_all_calls(call_logger)'''
class Main(ModMenu.SDKMod):
    Name: str = "Roguelands"
    Description: str = (
        "<font size='20' color='#ff0000'>Roguelands</font>\n"
        "Welcome to Roguelands!\n"
        "In this game mode, you only have 1 life so play carefully.\n"
        "As you progress, challenges will get more and more difficult.\n"
        "Gear up, build your character, and take on the challenges that lie ahead.\n\n"
        "Good luck!\n\n"
        "Special Thanks: Juso, Mopioid, Abahbob, PilotPlaysGames, ZetaDæmon, Arin, Flare2V, Apple1417"
    )
    Author: str = "JoltzDude139 | Pyrex"
    Version: str = "1.0.5"
    SaveEnabledState: ModMenu.EnabledSaveType = ModMenu.EnabledSaveType.NotSaved

    Types: ModMenu.ModTypes = ModMenu.ModTypes.Utility
    SupportedGames: ModMenu.Game = ModMenu.Game.BL2

    in_game: bool = False  # im sorry for the damage to your brain/eyes my code is about to cause but i just cannot be bothered to make it better rn
    run_started: bool = False
    round_counter: int = 0
    isdead: bool = False
    isinffyl: bool = False
    text_size: Tuple[int, int] = (0, 0)
    mission_x: float = 93.5 / 100
    mission_y: float = 26 / 100
    travel_y: float = 78 / 100
    willow_hud: unrealsdk.UObject = None
    draw_timer: bool = False

    draw_minigame_text: int = 3

    distancetofinish: float = 0
    countdown_timer: int = 0
    bypass_loot: bool = False
    new_save_loaded: bool = True
    boss_pawn: Optional[unrealsdk.UObject] = None
    boss_bar_active: bool = False
    last_injured_state: int = 0
    current_trivia_question: int = random.randint(0, 19)
    

    force_travel: bool = False
    themodisdone: bool = False
    logallcalls: bool = False
    print_in_tick: bool = False

    # challenges

    kill_challenge_complete: bool = False
    boss_challenge_complete: bool = False

    white_knight_list = (
    "PawnBalance_Shootyface",
    )

    # py unrealsdk.GetEngine().GamePlayers[0].Actor.ServerTeleportPlayerToStation(unrealsdk.FindObject("LevelTravelStationDefinition", "GD_FastTravelStations.Zone1.GoshDam"))
    # py unrealsdk.GetEngine().GamePlayers[0].Actor.ServerTeleportPlayerToStation(unrealsdk.FindObject("FastTravelStationDefinition", "GD_FastTravelStations.Zone1.SouthpawFactory"))
    # py unrealsdk.Log(str(unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn.Location))

    def __init__(self) -> None:
        super().__init__()
        self.BypassTravelLockout = ModMenu.Options.Boolean(
            Caption="Disable Claim Reward Message",
            Description="Lets you skip having to claim your reward to travel to the next map",
            StartingValue=False,
            Choices=("No", "Yes"),  # False, True
        )
        self.KillOffExtras = ModMenu.Options.Boolean(
            Caption="Clear Enemies On Round End",
            Description="Kills extra enemies when a mission is completed and prevents more from spawning until the next round. Thx Mopi",
            StartingValue=True,
            Choices=("No", "Yes"),  # False, True
        )
        self.MissionTextX = ModMenu.Options.Slider(
            Caption="Mission Text Horizontal Location",
            Description="Horizontal location of the mission text",
            StartingValue=93,
            MinValue=14,
            MaxValue=99,
            Increment=1,
        )
        self.MissionTextY = ModMenu.Options.Slider(
            Caption="Mission Text Vertical Location",
            Description="Vertical location of the mission text",
            StartingValue=26,
            MinValue=0,
            MaxValue=94,
            Increment=1,
        )
        self.TravelTextY = ModMenu.Options.Slider(
            Caption="Travel Text Vertical Location",
            Description="Vertical location of the travel prompt",
            StartingValue=78,
            MinValue=0,
            MaxValue=95,
            Increment=1,
        )
        self.Keybinds: List[ModMenu.Keybind] = [
            ResetRunBind,
            ClaimRewardBind,
            RespecBind,
            # DebugBind,s
        ]
        self.Options = [
            self.BypassTravelLockout,
            self.KillOffExtras,
            # self.MissionTextX,
            # self.MissionTextY,
            # self.TravelTextY,
        ]

    def load_into_game(self) -> None:
        #unrealsdk.Log("Started Thread")
        time.sleep(10)
        unrealsdk.GetEngine().GamePlayers[0].Actor.GetFrontendMovie().LaunchSaveGame(2)

    def spawn_start_loot(self) -> None:
        map_scripts.starting_room.start_loot_thread()
        #startloot = threading.Thread(target=map_scripts.starting_room.start_loot_thread)
        #startloot.start()

    def reset_mod(self, forcetravel: bool, rlvloffset: bool, reset_raid_boss: bool) -> None:
        GameState.map_is_loaded = False
        placeablehelper.unload_map()
        self.round_counter = 0
        self.draw_timer = False

        self.draw_minigame_text = 3
        self.force_travel = forcetravel
        pcon = unrealsdk.GetEngine().GamePlayers[0].Actor
        pcon.UnclaimedRewards = []
        self.in_game = False
        pcon.ClientReturnToTitleScreen()
        self.kill_challenge_complete = False
        self.boss_challenge_complete = False

        self.last_injured_state = 0

        GameState.reset(reset_level_offset=rlvloffset)
        maps.reset_visited_maps(reset_raid_boss)

    def roll_new_map(self) -> None:
        map_scripts.mobbing.State.reset()
        map_scripts.redbarboss.State.reset()
        if GameState.level_offset == 0 and self.round_counter < 4:
            while True:
                temp_map: MapData = random.choice(MAP_DATA[GameState.map_type])
                if (
                    temp_map.has_been_visited_in_current_rotation is False
                    and temp_map.package != GameState.current_map.package
                    and temp_map.is_easy
                ):
                    GameState.current_map = temp_map
                    break
        else:
            while True:
                temp_map: MapData = random.choice(MAP_DATA[GameState.map_type])
                if (
                    temp_map.has_been_visited_in_current_rotation is False
                    and temp_map.package != GameState.current_map.package
                ):
                    GameState.current_map = temp_map
                    break

    def travel(self) -> None:
        # unrealsdk.FindObject("WillowGameInfo", "WillowGame.Default__WillowGameInfo").TravelCountdown()
        # unrealsdk.GetEngine().GamePlayers[0].Actor.PeerTravelAsHost(GameState.travel_timer, None)
        while GameState.travel_timer > 0 and not self.isinffyl:
            uFeed.ShowHUDMessage(
                Title="Travel",
                Message=f"Continuing Simulation in... {GameState.travel_timer}",
                Duration=1,
                MenuHint=0,
            )
            time.sleep(1)
            GameState.travel_timer -= 1
            # unrealsdk.GetEngine().GamePlayers[0].Actor.PlayUIAkEvent(
            # unrealsdk.FindObject("AkEvent", "Ake_UI.UI_Generic.Ak_Play_UI_Generic_Countdown"),
            # )

        if self.isinffyl:
            self.draw_timer = False
            GameState.travel_timer = 3
            return
        GameState.map_is_loaded = False
        placeablehelper.unload_map()

        for item in unrealsdk.FindAll("WillowPickup")[1:]:
            item.Behavior_Destroy()

        # Reset the current map data, so that when we roll it again it wont stay completed
        GameState.current_map.bosses_killed = 0
        GameState.current_map.kill_challenge_count = 0
        GameState.current_map.has_been_visited_in_current_rotation = True

        self.kill_challenge_complete = False
        self.boss_challenge_complete = False
        GameState.mission_complete = False
        GameState.mission_complete_sound_played = False

        self.round_counter += 1

        if self.round_counter % 13 == 0 and GameState.level_offset == 2:
            # unrealsdk.Log("Picking Finale For Round " + str(self.round_counter))
            GameState.map_type = MapType.Special
            GameState.current_map = MAP_DATA[GameState.map_type][1]
        elif self.round_counter % 13 == 0:
            # unrealsdk.Log("Picking Mini Game For Round " + str(self.round_counter))
            GameState.map_type = MapType.MiniGame
            self.roll_new_map()
        elif self.round_counter % 13 == 12 and GameState.level_offset == 2:
            # unrealsdk.Log("Picking Final Boss For Round " + str(self.round_counter))
            GameState.map_type = MapType.FinalBoss
            GameState.current_map = MAP_DATA[GameState.map_type][0]
        elif self.round_counter % 13 == 12:
            # unrealsdk.Log("Picking Raid Boss For Round " + str(self.round_counter))
            GameState.map_type = MapType.RaidBoss
            self.roll_new_map()
        elif self.round_counter % 13 == 11:
            # unrealsdk.Log("Picking Gold Chest For Round " + str(self.round_counter))
            GameState.map_type = MapType.Special
            GameState.current_map = MAP_DATA[GameState.map_type][0]
        elif self.round_counter % 13 in (5, 10):
            # unrealsdk.Log("Picking Red Bar Boss For Round " + str(self.round_counter))
            GameState.map_type = MapType.RedBarBoss
            self.roll_new_map()
        elif self.round_counter % 13 in (4, 9):
            # unrealsdk.Log("Picking Mini Boss For Round " + str(self.round_counter))
            GameState.map_type = MapType.MiniBoss
            self.roll_new_map()
        else:
            # unrealsdk.Log("Picking Mobbing For Round " + str(self.round_counter))
            GameState.map_type = MapType.Mobbing
            self.roll_new_map()

        self.draw_timer = False
        GameState.travel_timer = 3
        self.draw_minigame_text = 3
        map_scripts.redbarboss.State.reset()
        # unrealsdk.Log(
        # "New Map: " + str(self.round_counter) + " : " + str(GameState.map_type) + " : " + str(GameState.current_map),
        # )
        pcon = unrealsdk.GetEngine().GamePlayers[0].Actor
        pcon.UnclaimedRewards = []
        pcon.ConsoleCommand("camera 1st")

        unrealsdk.GetEngine().GameViewport.bDisableWorldRendering = True
        pcon.HideHUD()
        # pcon.bGodMode = not pcon.bGodMode
        # time.sleep(3)
        util.travel_to_destination(GameState.current_map.travel_object_name)

    def do_minigame_text(self) -> None:
        while self.draw_minigame_text > 0:
            time.sleep(1)
            self.draw_minigame_text -= 1
        uFeed.ShowHUDMessage(
            Title="Minigame",
            Message=str(GameState.current_map.minigame_string),
            Duration=5,
            MenuHint=0,
        )

    def do_countdown(self) -> None:
        while self.countdown_timer > 0:
            time.sleep(1)
            self.countdown_timer -= 1

    def do_spawn_delayed(self) -> None:
        pcon = unrealsdk.GetEngine().GamePlayers[0].Actor
        loaded_map: str = unrealsdk.GetEngine().GetCurrentWorldInfo().GetStreamingPersistentMapName().lower()

        # if GameState.map_type == MapType.Mobbing:
        # unrealsdk.Log("Reset Mobbing Spawns")
        # unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("set PopulationOpportunityDen IsEnabled True")
        # pcon.ConsoleCommand("set PopulationOpportunityDen bIsWaitingForRespawn True")
        # pcon.ConsoleCommand("set PopulationOpportunityDen RespawnDelayStartTime -10000")

        if loaded_map == "southpawfactory_p":  # instantly close the door so enemies dont get stuck out of bounds
            # unrealsdk.Log("southpawfactory_p pre spawn tps")
            pcon.Pawn.Location = (-3926.092529296875, 24686.87109375, -6822.24609375)
            pcon.Pawn.Controller.Rotation = (65427, 17204, 0)
            time.sleep(0.1)
            pcon.Pawn.Location = (-3933.71240234375, 24915.248046875, -6822.24609375)
            pcon.Pawn.Controller.Rotation = (65427, 17204, 0)
        # unrealsdk.Log("Waiting for spawn delay")
        time.sleep(0.1)  # sleep that the games spawn process completes, but the move the player to our custom spawn
        # unrealsdk.Log("Spawn delay over")

        # this should always be true I think?
        # unrealsdk.Log("if loaded_map == GameState.current_map.package")
        if loaded_map == GameState.current_map.package:
            # unrealsdk.Log("Setting Final Spawn Loc")
            pcon.Pawn.Location = GameState.current_map.spawn_location
            pcon.Pawn.Controller.Rotation = GameState.current_map.spawn_rotation
            # unrealsdk.Log("Teleported to spawn location")
            # unrealsdk.Log("Enable Rendering")
        # pcon.bGodMode = not pcon.bGodMode
        unrealsdk.GetEngine().GameViewport.bDisableWorldRendering = False
        # unrealsdk.Log("Enable Hud")
        pcon.DisplayHUD(False)
        # unrealsdk.Log("Delayed Spawn Done")

    def ModOptionChanged(self, option: ModMenu.Options.Base, new_value: Any) -> None:
        if option == self.MissionTextX:
            self.mission_x = new_value / 100
        if option == self.MissionTextY:
            self.mission_y = new_value / 100
        if option == self.TravelTextY:
            self.travel_y = new_value / 100
        if option == self.BypassTravelLockout:
            if new_value == "No":
                self.bypass_loot = False
            elif new_value == "Yes":
                self.bypass_loot = True

    def GameInputPressed(self, bind: ModMenu.Keybind, event: ModMenu.InputEvent) -> None:
        if bind == ResetRunBind and event == ModMenu.InputEvent.Pressed and self.isdead:
            unrealsdk.GetEngine().GamePlayers[0].Actor.UnclaimedRewards = []
            self.isinffyl = False
            self.isdead = False
            self.in_game = False
            self.reset_mod(False, True, True)
            unrealsdk.GetEngine().GamePlayers[0].Actor.ClientReturnToTitleScreen()

        if bind == ClaimRewardBind and event == ModMenu.InputEvent.Pressed and not self.isinffyl:
            if (
                not unrealsdk.GetEngine().GamePlayers[0].Actor.UnclaimedRewards
                or self.BypassTravelLockout.CurrentValue is True
            ):  # wtf is this truthey falsey bs i do not understand
                if GameState.mission_complete and not self.draw_timer:
                    if self.themodisdone:
                        self.reset_mod(False, True, True)
                    elif self.round_counter == 13:
                        self.print_in_tick = True
                        self.reset_mod(True, False, False)
                    else:
                        # unrealsdk.Log("Mission Complete, Continuing")
                        self.draw_timer = True
                        threading.Thread(target=self.travel).start()
                else:
                    unrealsdk.Log("Mission Not Complete, Not Continuing")
            else:
                uFeed.ShowHUDMessage(
                    Title="Unclaimed Rewards In Inventory",
                    Message="Collect Your Reward First!",
                    Duration=3,
                    MenuHint=0,
                )

        if bind == RespecBind and event == ModMenu.InputEvent.Pressed:
            unrealsdk.GetEngine().GamePlayers[0].Actor.VerifySkillRespec()

        if bind == DebugBind and event == ModMenu.InputEvent.Pressed:
            sbsl_obj = unrealsdk.ConstructObject("Behavior_SpawnLootAroundPoint")
            sbsl_obj.ItemPools = [unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_Pistols_02_Uncommon"), 
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_Shotguns_02_Uncommon"), 
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_SniperRifles_02_Uncommon"), 
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.WeaponPools.Pool_Weapons_Launchers_02_Uncommon"), 
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.ShieldPools.Pool_Shields_All_02_Uncommon"), 
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.GrenadeModPools.Pool_GrenadeMods_02_Uncommon"), 
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.ClassModPools.Pool_ClassMod_02_Uncommon"), 
                                unrealsdk.FindObject("ItemPoolDefinition", "GD_Itempools.ArtifactPools.Pool_Artifacts_02_Uncommon")]
            sbsl_obj.SpawnVelocityRelativeTo = 0
            sbsl_obj.bTorque = False
            sbsl_obj.CircularScatterRadius = 300
            sbsl_obj.CustomLocation = ((5789, -44759, -4841), None, "")
            sbsl_obj.ApplyBehaviorToContext(unrealsdk.GetEngine().GamePlayers[0].Actor, (), None, None, None, ())
            #bsl = unrealsdk.ConstructObject("Behavior_SpawnLootAroundPoint")
            #bsl.ItemPools = [unrealsdk.FindObject("ItemPoolDefinition", "GD_CustomItemPools_MainGame.Siren.TedioreUncommon"), unrealsdk.FindObject("ItemPoolDefinition", "GD_CustomItemPools_MainGame.Siren.TedioreUncommon"), unrealsdk.FindObject("ItemPoolDefinition", "GD_CustomItemPools_MainGame.Siren.TedioreUncommon")]
            #bsl.SpawnVelocityRelativeTo = 1
            #bsl.CircularScatterRadius = 50.0
            #bsl.CustomLocation = ((unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn.Location.X + 250, unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn.Location.Y, unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn.Location.Z), None, "")
            #bsl.ApplyBehaviorToContext(unrealsdk.GetEngine().GamePlayers[0].Actor, (), None, None, None, ())
            # MissionDisplay.MissionStuff.set_objective_text("GD_Z1_ShootMeInTheFace.M_ShootMeInTheFace:ShootInFace", "pls bro")
            # MissionDisplay.MissionStuff.refresh_mission_display()
            #unrealsdk.Log(str(GameState.current_map.map_file))
            # self.show_trivia_question()
            # pos: Tuple[float, float, float] = (util.get_player_location().X, util.get_player_location().Y, util.get_player_location().Z + 50)
            # self.drop_from_pool("GD_Flax_ItemPools.Items.ItemPool_Flax_Candy", pos, 80)
            # for i in range(1, 8):
            # time.sleep(0.01)
            # self.drop_from_pool("GD_Aster_ItemPools.WeaponPools.Pool_Weapons_04_Gemstone")
            # unrealsdk.Log(f"Mission Complete: {self.mission_complete} Boss Killed: {self.boss_challenge_complete} Kill Challenge: {self.kill_challenge_complete}")
            # for uobject in unrealsdk.FindAll("InteractiveObjectDefinition"):
            # unrealsdk.Log(str(uobject.Class.Name))
            # self.logallcalls = not self.logallcalls
            # unrealsdk.LogAllCalls(self.logallcalls)
            # self.levelOffset += 1
            # uFeed.TrainingBox(Title="Difficulty Increased", Message="You've unlocked <font color='#ff0000'>Awakened Level " + str(self.levelOffset) + "</font>!\nEnemies will grow stronger, but your gear will not.\nRefine and perfect your build to overcome the challenges that lie ahead.", MinDuration=0, PausesGame=True, MenuHint=0, Priority=255).Show()
            # placeablehelper.unload_map()
            # with open(os.path.join(Path(__file__).parent.resolve(), "assets\\Maps", str(self.mapData[self.mapType][self.currentMap][10]))) as mapfile:
            # maptoload = json.load(mapfile)
            # loadplease = maptoload.get(str(unrealsdk.GetEngine().GetCurrentWorldInfo().GetStreamingPersistentMapName().lower()), None)
            # placeablehelper.load_map(loadplease)
            # unrealsdk.Log(str(unrealsdk.GetEngine().GetCurrentWorldInfo().GetStreamingPersistentMapName().lower()))
            # unrealsdk.Log(str(self.currentMap))
            # self.mapType = 0
            # while True:
            # temp = random.randint(0, self.numberOfMobbingMaps)
            # if temp != self.currentMap:
            # self.currentMap = temp
            # break

    def disable_enemies(self) -> None:
        player: unrealsdk.UObject = unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn
        pawn: unrealsdk.UObject = unrealsdk.GetEngine().GetCurrentWorldInfo().PawnList
        while pawn:
            balance = pawn.BalanceDefinitionState.BalanceDefinition
            if balance and balance.Name not in self.white_knight_list:
                if pawn.GetOpinion and pawn.GetOpinion(player) != 2:
                    if pawn.MyWillowMind:
                        pawn.MyWillowMind.SpawnParent = None
                        pawn.MyWillowMind.SpawnChildren = ()
                    pawn.SpawnParent = None
                    pawn.Died(None, None, ())
            pawn = pawn.NextPawn

        for point in unrealsdk.FindAll("WillowPopulationPoint"):
            if point.Name != "Default__WillowPopulationPoint":
                point.IsEnabled = False

    def do_save_quit(self) -> None:
            unrealsdk.GetEngine().GamePlayers[0].Actor.UnclaimedRewards = []
            self.isinffyl = False
            self.isdead = False
            self.in_game = False
            self.reset_mod(False, True, True)
            unrealsdk.GetEngine().GamePlayers[0].Actor.ClientReturnToTitleScreen()
            return True
        
    def dont_save_quit(self) -> None:
        return True

    def reward(self, name: str, item: str) -> None:
        pcon = unrealsdk.GetEngine().GamePlayers[0].Actor
        mission = unrealsdk.FindObject("MissionDefinition", "GD_Episode01.M_Ep1_Champion")
        mission.GameStage = 80
        pcon.ConsoleCommand(f"set GD_Episode01.M_Ep1_Champion MissionName {name}")
        mission.Reward.RewardItems = []
        itempool = unrealsdk.FindObject("ItemPoolDefinition", item)
        mission.reward.RewardItemPools = [itempool, itempool]
        mission.Reward.CreditRewardMultiplier.BaseValueScaleConstant = 10
        pcon.ServerGrantMissionRewards(mission, False)
        # pcon.ShowStatusMenu()

    def fill_ammo(self) -> None:
        for ammopool in unrealsdk.GetEngine().GamePlayers[0].Actor.ResourcePoolManager.ResourcePools:
            if ammopool is None:
                continue
            # if ammopool.Definition.Resource.Name == "Ammo_Rocket_Launcher" and ammopool.GetUpgradeLevel() > 0:
            # ammopool.Definition.TotalUpgradeCount = 0
            # ammopool.ApplyUpgrades()
            # unrealsdk.Log(f"{ammopool.Definition.Resource.Name} Upgrade Level: {ammopool.GetUpgradeLevel()} Max Value:{ammopool.GetMaxValue(False)}")
            if (
                ammopool.Class.Name in ("AmmoResourcePool", "HealthResourcePool")
                or ammopool.Definition.Resource.Name == "Ammo_Grenade_Protean"
            ):
                # fill health and ammo
                if ammopool.Definition.Resource.Name == "Ammo_Rocket_Launcher":
                    ammopool.SetCurrentValue(min(ammopool.GetMaxValue(False), ammopool.GetCurrentValue() + 6))
                elif ammopool.Definition.Resource.Name == "Ammo_Grenade_Protean":
                    ammopool.SetCurrentValue(min(ammopool.GetMaxValue(False), ammopool.GetCurrentValue() + 3))
                else:
                    ammopool.SetCurrentValue(ammopool.GetMaxValue(False))
            elif ammopool.Definition.Resource.Name == "ActiveSkillCooldown":
                # reset action skill cooldown
                ammopool.SetCurrentValue(ammopool.GetMinValue(False))

    def mission_tracker(self) -> None:
        pcon = unrealsdk.GetEngine().GamePlayers[0].Actor
        hud = pcon.GetHUDMovie()
        if GameState.map_type == MapType.Mobbing:
            self.boss_challenge_complete = True
        if GameState.map_type not in (MapType.Mobbing, MapType.MiniBoss):
            self.kill_challenge_complete = True
        if GameState.map_type == MapType.Special and GameState.current_map.name == "Golden Chest":
            self.boss_challenge_complete = True
            self.kill_challenge_complete = True
            GameState.mission_complete = True

        if not self.boss_challenge_complete or not self.kill_challenge_complete:
            return

        if GameState.mission_complete_sound_played or GameState.mission_complete:
            GameState.mission_complete = True
            return

        GameState.mission_complete_sound_played = True
        if self.KillOffExtras.CurrentValue is True:
            self.disable_enemies()
        #if self.round_counter == 13:
            #unrealsdk.GetEngine().GamePlayers[0].Actor.GetHUDMovie().WPRI.Currency[8].CurrentAmount = GameState.level_offset
        mission_display.update_mission_display()
        # unrealsdk.Log("Set missionCompleteSoundPlayed True")
        if GameState.map_type not in (MapType.MiniGame, MapType.Special, MapType.FinalBoss):
            uFeed.ShowHUDMessage(Title="Reward Earned!", Message="Check Your Inventory", Duration=8, MenuHint=0)
        unrealsdk.GetEngine().GamePlayers[0].Actor.PlayUIAkEvent(
            unrealsdk.FindObject("AkEvent", "Ake_UI.UI_BackMenu.Ak_Play_UI_Badass_Rank_Up"),
        )
        if GameState.map_type != MapType.MiniGame:
            unrealsdk.GetEngine().GamePlayers[0].Actor.GetHUDMovie().WPRI.Currency[1].CurrentAmount += 25

        if GameState.map_type == MapType.RaidBoss:
            self.reward("Roguelands", REWARD_POOLS[MapType.RaidBoss][0])
        elif GameState.map_type == MapType.MiniGame:
            if GameState.current_map.should_show_timer:
                if self.countdown_timer > 0:
                    unrealsdk.GetEngine().GamePlayers[0].Actor.GetHUDMovie().WPRI.Currency[1].CurrentAmount += 50
                    uFeed.ShowHUDMessage(Title="Reward Earned!", Message="50 Eridium", Duration=3, MenuHint=0)
                    self.countdown_timer = 0
                else:
                    uFeed.ShowHUDMessage(
                        Title="Mini game failed!",
                        Message="You will not receive an eridium bonus for completion.",
                        Duration=3,
                        MenuHint=0,
                    )
            elif GameState.current_map.map_file == "E10 Digipeak Trivia Mini Game 1.json":
                if GameState.current_map.custom_map_data[5] is False:
                    unrealsdk.GetEngine().GamePlayers[0].Actor.GetHUDMovie().WPRI.Currency[1].CurrentAmount += 50
                    uFeed.ShowHUDMessage(Title="Reward Earned!", Message="50 Eridium", Duration=3, MenuHint=0)
                    self.countdown_timer = 0
                else:
                    uFeed.ShowHUDMessage(
                        Title="Mini game failed!",
                        Message="You will not receive an eridium bonus for completion.",
                        Duration=3,
                        MenuHint=0,
                    )
            else:
                unrealsdk.GetEngine().GamePlayers[0].Actor.GetHUDMovie().WPRI.Currency[1].CurrentAmount += 50
                uFeed.ShowHUDMessage(Title="Reward Earned!", Message="50 Eridium", Duration=3, MenuHint=0)
                self.countdown_timer = 0
        elif GameState.map_type == MapType.MiniBoss:
            self.reward("Roguelands", REWARD_POOLS[MapType.MiniBoss][GameState.level_offset])
        elif GameState.map_type == MapType.RedBarBoss:
            if GameState.level_offset < 1:
                self.reward("Roguelands", REWARD_POOLS[MapType.RedBarBoss][0])
            else:
                self.reward("Roguelands", REWARD_POOLS[MapType.RedBarBoss][1])
            map_scripts.redbarboss.move_gift_box()
        elif GameState.map_type == MapType.Mobbing:
            self.reward("Roguelands", REWARD_POOLS[MapType.Mobbing][GameState.level_offset])

        if hud.WPRI.Currency[7].CurrentAmount < 76 and GameState.map_type not in (
            MapType.StartRoom,
            MapType.Special,
            MapType.RaidBoss,
            MapType.MiniGame,
        ):
            if hud.WPRI.Currency[7].CurrentAmount + 5 > 76:
                hud.WPRI.Currency[7].CurrentAmount += 76 - hud.WPRI.Currency[7].CurrentAmount
            else:
                hud.WPRI.Currency[7].CurrentAmount += 5

        if pcon.GetHUDMovie().WPRI.Currency[1].CurrentAmount > 500:
            pcon.GetHUDMovie().WPRI.Currency[1].CurrentAmount = 500

        if self.round_counter == 13:
            if GameState.level_offset == 2:
                self.themodisdone = True
                uFeed.TrainingBox(
                    Title="Roguelands Complete!",
                    Message="Congratulations on beating Roguelands!\nYour run ends here and you will now be set back to the main menu.\n\nThanks for checking out the mod.",
                    MinDuration=0,
                    PausesGame=True,
                    MenuHint=0,
                    Priority=255,
                ).Show()
            else:
                GameState.level_offset += 1
                uFeed.TrainingBox(
                    Title="Difficulty Increased",
                    Message="You've unlocked <font color='#ff0000'>Difficulty Tier "
                    + str(GameState.level_offset + 1)
                    + "</font>!\nEnemies will grow stronger, but your gear will not.\nRefine and perfect your build to overcome the challenges that lie ahead.",
                    MinDuration=0,
                    PausesGame=True,
                    MenuHint=0,
                    Priority=255,
                ).Show()

        GameState.mission_complete = True

    # GD_CustomItemPools_MainGame.Siren.TedioreUncommon modded blue/purple unique pool

    def track_boss_kills_by_map(self, enemy: str) -> None:
        """
        Increment the boss kill counter for the current map
        if the killed enemy is a boss listed in the current map's custom_map_data
        """
        if (
            enemy in GameState.current_map.custom_map_data[0]
            and not GameState.current_map.bosses_killed + 1 > GameState.current_map.total_bosses_in_map
        ):
            GameState.current_map.bosses_killed += 1
            mission_display.update_mission_display()

        if (
            GameState.current_map.bosses_killed >= GameState.current_map.total_bosses_in_map
            and GameState.map_type != MapType.Special
        ):
            self.boss_challenge_complete = True

    def Enable(self) -> None:
        pc: unrealsdk.UObject = unrealsdk.GetEngine().GamePlayers[0].Actor
        dir_path = path.dirname(path.realpath(__file__))
        pc.ConsoleCommand(f'exec "{dir_path}\\assets\\rlc.txt"')
        unrealsdk.Log("Ran Text Mods")

        sdkversion = unrealsdk.GetVersion()
        versionint = int(str(sdkversion[0]) + str(sdkversion[1]) + str(sdkversion[2]))
        if versionint < 711:
            unrealsdk.Log(
                "Roguelands Requires at least SDK Version 0.7.11, Download page has been opened in your browser.",
            )
            uFeed.TrainingBox(
                Title="Out of Date SDK",
                Message="Roguelands Requires at least SDK Version 0.7.11, Download page has been opened in your browser.",
                MinDuration=1,
                PausesGame=False,
                MenuHint=0,
                Priority=255,
            ).Show()
            import webbrowser

            webbrowser.open("https://github.com/bl-sdk/bl2-mod-manager/releases")

        if "TAGGED_OBJECTS" not in placeablehelper.__all__:
            unrealsdk.Log(
                "You must update MapLoader for Roguelands to work properly. The mod page has been opened in your browser.",
            )
            import webbrowser

            webbrowser.open("https://bl-sdk.github.io/mods/MapLoader/")

        Looties.Enable()
        Looties.Rarity = 7
        Looties.AIRollBlacklist.append("CharClass_JohnMamaril")
        Looties.AIRollBlacklist.append("CharClass_DeathTrap")
        Looties.AIRollBlacklist.append("CharClass_RolandDeployableTurret")
        Looties.AIRollBlacklist.append("CharClass_Scorpio")
        Looties.AIRollBlacklist.append("CharClass_Assassin_Hologram")

        # unrealsdk.GetEngine().GamePlayers[0].Actor.bEnteredEasterEggCode
        # unrealsdk.GetEngine().GamePlayers[0].Actor.bEnabledEasterEggOption

        def render(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
            # if not self.in_game:
            # return True
            pc = unrealsdk.GetEngine().GamePlayers[0].Actor
            if (
                pc is None
                or pc.bViewingThirdPersonMenu
                or pc.IsPauseMenuOpen()
                or not self.in_game
                or not self.isdead
            ):
                return True

            params.Canvas.Font = unrealsdk.FindObject("Font", "ui_fonts.font_willowbody_18pt")

            # background
            util.draw_shader(
                params.Canvas,
                0,
                0,
                params.Canvas.SizeX,
                params.Canvas.SizeY,
                (0, 0, 0, 200),
                unrealsdk.FindObject("Texture2D", "EngineResources.WhiteSquareTexture"),
            )

            # text
            self.text_size = params.Canvas.StrLen("You Died")
            util.draw_text(
                params.Canvas,
                "You Died",
                (params.Canvas.SizeX / 2) - ((int(self.text_size[0]) * 2.5) / 2),
                (params.Canvas.SizeY / 2) - ((int(self.text_size[1]) * 2.5) / 2),
                2.5,
                2.5,
                (0, 0, 255, 255),
            )

            # restart prompt
            self.text_size = params.Canvas.StrLen("Press [" + str(ResetRunBind.Key) + "] To End Run")
            util.draw_text(
                params.Canvas,
                "Press [" + str(ResetRunBind.Key) + "] To End Run",
                (params.Canvas.SizeX / 2) - (int(self.text_size[0] / 2)),
                params.Canvas.SizeY * 0.95,
                1,
                1,
                (255, 255, 255, 200),
            )
            return True

        def died(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
            #unrealsdk.Log("Player Died Hook Ran")
            # unrealsdk.Log(f"SetInjuredDeadState: {_params.InjuredDeadStateVal}")
            if not self.isdead and int(params.InjuredDeadStateVal) != 0:
                pcon = unrealsdk.GetEngine().GamePlayers[0].Actor
                pcon.Pawn.Controller.Rotation = (49151, 23020, 0)
                pcon.Pawn.Location = (
                    util.get_player_location().X,
                    util.get_player_location().Y,
                    util.get_player_location().Z + float(250),
                )
                pcon.Unpossess()
                pcon.HideHUD()
                self.isdead = True
                self.isinffyl = False
            return True

        def blockpause(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, _params: unrealsdk.FStruct) -> bool:
            return not (self.draw_timer)

        def blockstatusmenu(
            _caller: unrealsdk.UObject,
            _function: unrealsdk.UFunction,
            _params: unrealsdk.FStruct,
        ) -> bool:
            return not self.draw_timer

        def tick(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, _params: unrealsdk.FStruct) -> bool:
            if not self.in_game:
                return True
            pc = unrealsdk.GetEngine().GamePlayers[0].Actor
            hud_movie: unrealsdk.UObject = pc.GetHUDMovie()
            if hud_movie is None:
                return True
            if not hud_movie.WPRI and GameState.travel_timer > 0:
                return True
            pc.ServerSetBadassSkillDisabled(True)
            loaded_map: str = unrealsdk.GetEngine().GetCurrentWorldInfo().GetStreamingPersistentMapName().lower()
            if (
                hud_movie.WPRI.Currency[7].CurrentAmount == 0
                and GameState.current_map.map_file == "G2 Leviathans Lair Starting Room 1.json"
                and unrealsdk.GetEngine().GetCurrentWorldInfo().GetStreamingPersistentMapName().lower() == "orchid_wormbelly_p"
            ):
                hud_movie.WPRI.Currency[0].CurrentAmount = 0
                hud_movie.WPRI.Currency[1].CurrentAmount = 0
                hud_movie.WPRI.Currency[7].CurrentAmount = 1
                self.spawn_start_loot()
                hud_movie.WPRI.GeneralSkillPoints = (
                    hud_movie.WPRI.Currency[7].CurrentAmount - pc.PlayerSkillTree.GetSkillPointsSpentInTree()
                )
                pc.PlayerSkillTree.UpgradeSkill(pc.PlayerSkillTree.GetActionSkill())

            hud_movie.WPRI.GeneralSkillPoints = (
                hud_movie.WPRI.Currency[7].CurrentAmount - pc.PlayerSkillTree.GetSkillPointsSpentInTree()
            )
            if GameState.current_map.map_file == "D1 Pete Raid Boss.json" or GameState.current_map.map_file == "H1 Ancient Dragons Raid Boss.json":
                if hud_movie.WPRI.Currency[1].CurrentAmount < 8:
                    hud_movie.WPRI.Currency[1].CurrentAmount = 8

            if loaded_map != GameState.current_map.package:
                util.travel_to_destination(GameState.current_map.travel_object_name)

            return True

        def startnewplaysession(
            _caller: unrealsdk.UObject,
            _function: unrealsdk.UFunction,
            _params: unrealsdk.FStruct,
        ) -> bool:
            # unrealsdk.Log("PostBeginPlay")
            self.in_game = True
            return True

        def kill(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, _params: unrealsdk.FStruct) -> bool:
            # unrealsdk.Log("Behavior_Killed: " + str(caller.BodyClass))
            return True

        def pawndied(caller: unrealsdk.UObject, _function: unrealsdk.UFunction, _params: unrealsdk.FStruct) -> bool:
            if "WillowPlayerPawn" in str(caller):
                return True
            aipawn = caller.GetAWillowAIPawn()
            #unrealsdk.Log("Died: " + str(aipawn.AIClass))

            if caller == self.boss_pawn:
                self.boss_pawn = None
                repinfo: unrealsdk.UObject = unrealsdk.GetEngine().GetCurrentWorldInfo().GRI
                repinfo.UpdateBossBarInfo()
                repinfo.InitBossBar(False, self.boss_pawn)
                self.boss_bar_active = False

            if str(aipawn.AIClass) in EXCLUDED_ENEMIES:
                return True  # skip if excluded

            # increment the kill challenge counter, but don't go over the goal
            if not GameState.current_map.kill_challenge_count + 1 > GameState.current_map.kill_challenge_goal:
                GameState.current_map.kill_challenge_count += 1
                mission_display.update_mission_display()
            if GameState.current_map.kill_challenge_count >= GameState.current_map.kill_challenge_goal:
                self.kill_challenge_complete = True

            if GameState.map_type in (MapType.MiniBoss, MapType.RedBarBoss, MapType.RaidBoss, MapType.FinalBoss):
                self.track_boss_kills_by_map(str(aipawn.AIClass))

            self.mission_tracker()
            return True

        def pawndamage(caller: unrealsdk.UObject, _function: unrealsdk.UFunction, _params: unrealsdk.FStruct) -> bool:
            # unrealsdk.Log(f"Caller: {str(caller.GetAWillowAIPawn().AIClass)}")
            if "WillowPlayerPawn" in str(caller) or not caller.GetAWillowAIPawn().AIClass:
                return True
            if "CharClass_Shootyface" in str(caller.GetAWillowAIPawn().AIClass):
                uFeed.ShowHUDMessage(
                    Title="HEY!",
                    Message="Dont do that to my mans Face McShooty cmon bro",
                    Duration=5,
                    MenuHint=0,
                )
                return False
            if self.boss_pawn is None and str(caller.GetAWillowAIPawn().AIClass) in (
                "AIClassDefinition gd_bluntcrack.Character.CharClass_BluntCrack",
                "AIClassDefinition GD_Flynt.Character.CharClass_Flynt",
                "AIClassDefinition GD_MrMercy.Character.CharClass_MrMercy",
                "AIClassDefinition GD_LoaderUltimateBadass.Character.CharClass_LoaderUltimateBadass",
                "AIClassDefinition GD_SpiderantScorch.Character.CharClass_SpiderantScorch",
            ):
                self.boss_pawn = caller
                repinfo: unrealsdk.UObject = unrealsdk.GetEngine().GetCurrentWorldInfo().GRI
                if repinfo:
                    repinfo.InitBossBar(True, self.boss_pawn)
                    self.boss_bar_active = True
            return True

        def forcelvl80enemies(
            caller: unrealsdk.UObject,
            _function: unrealsdk.UFunction,
            _params: unrealsdk.FStruct,
        ) -> bool:
            # exclude me
            if str(caller).split(".")[0] == "WillowPlayerPawn":
                return True

            unrealsdk.DoInjectedCallNext()
            caller.SetGameStage(80 + (GameState.level_offset * 3))
            return False

        def savequit(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, _params: unrealsdk.FStruct) -> bool:
            menu: uFeed.OptionBox = uFeed.OptionBox(
                Title="Save Quit:",
                Caption="Are you really sure u wanna do this?\nThis will end your current run.",
                PreventCanceling = True,
                Buttons=[
                    uFeed.OptionBoxButton(Name="No", Tip=""),
                    uFeed.OptionBoxButton(Name="Yes", Tip=""),
                ],
            )
            menu.OnPress = lambda button: {
                "No": self.dont_save_quit,
                "Yes": self.do_save_quit,
            }.get(button.Name, lambda _: None)()
            menu.Show()
            return False
        '''
            unrealsdk.GetEngine().GamePlayers[0].Actor.UnclaimedRewards = []
            self.isinffyl = False
            self.isdead = False
            self.in_game = False
            self.reset_mod(False, True, True)
            return True
        '''

        def spawn(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, _params: unrealsdk.FStruct) -> bool:
            # unrealsdk.Log(
            # "================================ WillowClientDisableLoadingMovie ================================",
            # )
            loaded_map: str = unrealsdk.GetEngine().GetCurrentWorldInfo().GetStreamingPersistentMapName().lower()
            # unrealsdk.Log("Got Current Game Map")
            if loaded_map == GameState.current_map.package:
                if GameState.current_map.map_file == "D1 Pete Raid Boss.json":
                    unrealsdk.FindObject("Behavior_SetUsabilityCost", "GD_IrisRaidBossData.InteractiveObjects.IrisRaidBoardPete:BehaviorProviderDefinition_0.Behavior_SetUsabilityCost_7").CostAmount = 0
                    unrealsdk.FindObject("Behavior_SetUsabilityCost", "GD_IrisRaidBossData.InteractiveObjects.IrisRaidBoardPete:BehaviorProviderDefinition_0.Behavior_SetUsabilityCost_8").CostAmount = 0
                    unrealsdk.FindObject("Behavior_SetUsabilityCost", "GD_IrisRaidBossData.InteractiveObjects.IrisRaidBoardPete:BehaviorProviderDefinition_0.Behavior_SetUsabilityCost_9").CostAmount = 0
                # unrealsdk.Log("Current Game Map == Current Mod Map")
                self.new_save_loaded = False
                map_file_path: Path = Path(__file__).parent.resolve() / "assets/Maps" / GameState.current_map.map_file
                # unrealsdk.Log(str(os.path.join(Path(__file__).parent.resolve(), "assets\\Maps", str(self.mapData[self.mapType][self.currentMap][10]))))
                if loaded_map == GameState.current_map.package:
                    if map_file_path.is_file():
                        with open(map_file_path) as mapfile:
                            maptoload = json.load(mapfile)
                            loadplease = maptoload.get(
                                loaded_map,
                                None,
                            )
                        # unrealsdk.Log("Loading Map")
                        placeablehelper.load_map(loadplease)
                        GameState.map_is_loaded = True
                        # unrealsdk.Log("Loaded Map")
                    else:
                        unrealsdk.Log(str(map_file_path) + " Doesnt Exist")

                # unrealsdk.Log("bTotalResetOnLevelLoad")
                for popdef in unrealsdk.FindAll("WillowPopulationDefinition"):
                    popdef.bTotalResetOnLevelLoad = True

                # unrealsdk.Log("Get Pcon")
                pcon = unrealsdk.GetEngine().GamePlayers[0].Actor
                # unrealsdk.Log("Set Mission Name")
                # pcon.ConsoleCommand("set GD_Z1_ShootMeInTheFace.M_ShootMeInTheFace MissionName Roguelands")
                # unrealsdk.Log("Set No Mission Selected")
                # unrealsdk.GetEngine().GetCurrentWorldInfo().GRI.MissionTracker.ActiveMission = unrealsdk.FindObject(
                # "MissionDefinition",
                # "GD_Z1_ShootMeInTheFace.M_ShootMeInTheFace",
                # )

                # unrealsdk.Log("Delay Spawn")
                threading.Thread(target=self.do_spawn_delayed).start()
                self.fill_ammo()

                pcon.bShowUndiscoveredMissions = False

                mission_display.MissionStuff.set_mission_name(
                    f"{MISSION_TYPE_READABLE[GameState.map_type]}Round {self.round_counter} / 13",
                )
                mission_display.update_mission_display()

                # unrealsdk.Log("Teleported to Start")

                # fix bloodshot stronghold loud ass audio (i stole this from bl2fix) (apparently they yoinked this from ucp?) (i have no idea who to credit for this im just gonna go with flare2v)
                # for soundvolume in unrealsdk.FindAll("WwiseSoundVolume")[:-1]:
                # unrealsdk.Log(str(soundvolume))
                # if "Dam_Audio" in str(soundvolume):
                # unrealsdk.Log("did thing")
                # soundvolume = None

                # unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("set PopulationOpportunityDen bIsWaitingForRespawn True")
                # unrealsdk.GetEngine().GamePlayers[0].Actor.ConsoleCommand("set PopulationOpportunityDen RespawnDelayStartTime -10000")

                # for animation in unrealsdk.FindAll("AnimSequence"):
                # if "Anim_1st_Person" not in str(animation) and "Engine.Default__AnimSequence" not in str(animation) and "Lootables" not in str(animation) and "Anim_Generic" not in str(animation) and "Flags" not in str(animation) and "Doors" not in str(animation) and "VendingMachine" not in str(animation) and "Dice" not in str(animation) and "FastTravel" not in str(animation) and "Crazy_Earl" not in str(animation):
                # unrealsdk.Log(str(animation))
                # animation.RateScale = 5

                if GameState.current_map.map_file == "G1 Hatreds Shadow Victory Room.json":
                    threading.Thread(target=map_scripts.g1_hatreds_shadow_victory_room.finish_cubes).start()

                if GameState.map_type == MapType.MiniGame:
                    threading.Thread(target=self.do_minigame_text).start()
                    if GameState.current_map.should_show_timer:
                        self.countdown_timer = GameState.current_map.kill_challenge_goal
                        threading.Thread(target=self.do_countdown).start()
                    if GameState.current_map.map_file == "E7 Beatdown Shifting Floors 1.json":
                        threading.Thread(
                            target=map_scripts.e7_beatdown_shifting_floors.move_floors_for_floors_minigame,
                        ).start()
                    if GameState.current_map.map_file == "E8 Forest Glitch Mini Game 1.json":
                        threading.Thread(target=map_scripts.e8_forest_glitch_mini_game.glitch_room).start()
            return True

        def on_chat_command(
            _caller: unrealsdk.UObject,
            _function: unrealsdk.UFunction,
            params: unrealsdk.FStruct,
        ) -> bool:
            splitstring = params.msg.split(" ")
            if str(params.PRI.PlayerName) == "PyrexBLJ" or str(params.PRI.PlayerName) == "JoltzDude139":
                # unrealsdk.Log(str(params.PRI.PlayerName))
                if splitstring[0].lower() != "rl":
                    return True

                cmd: str = splitstring[1].lower()

                unrealsdk.Log("rl Recieved")
                if cmd == "goto":
                    GameState.map_is_loaded = False
                    placeablehelper.unload_map()

                    for item in unrealsdk.FindAll("WillowPickup")[1:]:
                        item.Behavior_Destroy()

                    GameState.current_map.bosses_killed = 0
                    GameState.current_map.kill_challenge_count = 0

                    self.kill_challenge_complete = False
                    self.boss_challenge_complete = False
                    GameState.mission_complete = False
                    GameState.mission_complete_sound_played = False

                    GameState.map_type = MapType(int(splitstring[2]))
                    GameState.current_map = MAP_DATA[GameState.map_type][int(splitstring[3])]

                    self.draw_timer = False
                    GameState.travel_timer = 3
                    self.draw_minigame_text = 3

                    unrealsdk.GetEngine().GamePlayers[0].Actor.UnclaimedRewards = []
                    unrealsdk.GetEngine().GameViewport.bDisableWorldRendering = True
                    util.travel_to_destination(GameState.current_map.travel_object_name)
                elif cmd == "round":
                    self.round_counter = int(splitstring[2])
                elif cmd == "tier":
                    GameState.level_offset = int(splitstring[2]) - 1
                elif cmd == "unloadmap":
                    GameState.map_is_loaded = False
                    placeablehelper.unload_map()
                elif cmd == "loadmap":
                    loaded_map: str = unrealsdk.GetEngine().GetCurrentWorldInfo().GetStreamingPersistentMapName().lower()
                    map_file_path: Path = Path(__file__).parent.resolve() / "assets/Maps" / GameState.current_map.map_file
                    if loaded_map == GameState.current_map.package:
                        if map_file_path.is_file():
                            with open(map_file_path) as mapfile:
                                maptoload = json.load(mapfile)
                                loadplease = maptoload.get(
                                    loaded_map,
                                    None,
                                )
                            placeablehelper.load_map(loadplease)
                            GameState.map_is_loaded = True
                        else:
                            unrealsdk.Log(str(map_file_path) + " Doesnt Exist")
            return False

        def no(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, _params: unrealsdk.FStruct) -> bool:
            return False

        def sometimesno(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, _params: unrealsdk.FStruct) -> bool:
            uFeed.TrainingBox(
                Title="Use Level 30 Start Character",
                Message="Start a new character from the bottom of the save game list to play.\n\nFeel Free to delete saves from previous runs.",
                MinDuration=0,
                PausesGame=False,
                MenuHint=0,
                Priority=255,
            ).Show()
            return False

        def frontendhook(
            _caller: unrealsdk.UObject,
            _function: unrealsdk.UFunction,
            _params: unrealsdk.FStruct,
        ) -> bool:
            self.print_in_tick = False
            pc = unrealsdk.GetEngine().GamePlayers[0].Actor
            if pc.GetFrontendMovie() is None:
                return True
            if self.force_travel:
                self.force_travel = False
                unrealsdk.FindObject(
                    "BalanceModifierDefinition",
                    "GD_Playthrough3Tuning.Balance.BalanceMod_PT3",
                ).BalanceModifiers[0].EnemyDamageMultiplier = 0.3 + (GameState.level_offset / 10)
                pc.GetFrontendMovie().LaunchSaveGame(2)
            if self.themodisdone:
                unrealsdk.FindObject(
                    "BalanceModifierDefinition",
                    "GD_Playthrough3Tuning.Balance.BalanceMod_PT3",
                ).BalanceModifiers[0].EnemyDamageMultiplier = 0.3
                self.themodisdone = False
                # unrealsdk.GetEngine().GamePlayers[0].Actor.OnLoadSaveGame(False)
                # pc.GetFrontendMovie().OpenCharacterSelectFromList()
                # charselectmovie = pc.GetCharacterSelectMovie()
                # charselectmovie.LoadCharacterLobby.ConditionalLoadGame(charselectmovie.LoadCharacterLobby.MostRecentLoadInfo, charselectmovie.LoadCharacterLobby.SelectedDataIndex)
                # for menu in unrealsdk.FindAll("WillowGFxLobbyLoadCharacter")[1:]:
                # menu.ConditionalLoadGame(menu.MostRecentLoadInfo, menu.SelectedDataIndex)

            return True

        def frontendhook2(
            _caller: unrealsdk.UObject,
            _function: unrealsdk.UFunction,
            _params: unrealsdk.FStruct,
        ) -> bool:
            #unrealsdk.LogAllCalls(False)
            #unrealsdk.Log("FrontEndHook2 Ran")
            return True

        def soundplayed(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
            # unrealsdk.Log(f"SetInjuredState: {_params.InjuredStateVal}")
            injured_state_val: int = int(params.InjuredStateVal)

            self.isinffyl = injured_state_val != 0

            if self.last_injured_state == 0 and injured_state_val == 0:
                pcon = unrealsdk.GetEngine().GamePlayers[0].Actor
                pcon.Unpossess()
                pcon.HideHUD()
                self.isinffyl = False
                self.isdead = True

            self.last_injured_state = injured_state_val
            return True

        def loadsavegame(
            _caller: unrealsdk.UObject,
            _function: unrealsdk.UFunction,
            _params: unrealsdk.FStruct,
        ) -> bool:
            # unrealsdk.Log(f"Player Index: {_caller.PlayerIndex} Current Selection: {_caller.CurrentSelection}")
            unrealsdk.FindObject(
                "BalanceModifierDefinition",
                "GD_Playthrough3Tuning.Balance.BalanceMod_PT3",
            ).BalanceModifiers[0].EnemyDamageMultiplier = 0.3
            self.new_save_loaded = True
            return True

        def setpt3(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, _params: unrealsdk.FStruct) -> bool:
            unrealsdk.DoInjectedCallNext()
            _caller.SetCurrentPlaythrough(unrealsdk.GetEngine().GamePlayers[0].Actor, 2)
            return False

        def died2(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, _params: unrealsdk.FStruct) -> bool:
            # unrealsdk.Log("ShowRespawnDialog")
            pcon = unrealsdk.GetEngine().GamePlayers[0].Actor
            # pcon.Pawn.Controller.Rotation = (49151, 23020, 0)
            # pcon.Pawn.Location = (pcon.Pawn.Location.X, pcon.Pawn.Location.Y, pcon.Pawn.Location.Z + float(1000))
            pcon.Unpossess()
            pcon.HideHUD()
            self.isinffyl = False
            self.isdead = True
            return True

        def nocompassicons(
            _caller: unrealsdk.UObject,
            _function: unrealsdk.UFunction,
            _params: unrealsdk.FStruct,
        ) -> bool:
            # unrealsdk.Log(f"Object: {str(_caller.Name)} Icon: {str(_params.NewIcon)}")
            return False

        def gimmechallengename(
            _caller: unrealsdk.UObject,
            _function: unrealsdk.UFunction,
            params: unrealsdk.FStruct,
        ) -> bool:
            return not "Challenge Completed:" in str(params.MessageString)

        def nochallenges(
            _caller: unrealsdk.UObject,
            _function: unrealsdk.UFunction,
            _params: unrealsdk.FStruct,
        ) -> bool:
            # unrealsdk.Log("Closed a Menu")
            if GameState.mission_complete_sound_played:
                uFeed.ShowHUDMessage(
                    Title="Round Complete!",
                    Message=f"Press [{ClaimRewardBind.Key}] To Continue.",
                    Duration=30,
                    MenuHint=0,
                )
            return True

        def closestatusmenu(
            _caller: unrealsdk.UObject,
            _function: unrealsdk.UFunction,
            _params: unrealsdk.FStruct,
        ) -> bool:
            unrealsdk.Log("Close Status Menu Hook Ran")
            mission_display.update_mission_display()
            return True

        def closepausemenu(
            _caller: unrealsdk.UObject,
            _function: unrealsdk.UFunction,
            _params: unrealsdk.FStruct,
        ) -> bool:
            mission_display.update_mission_display()
            return True
        
        def hitloc(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, _params: unrealsdk.FStruct) -> bool:
            #unrealsdk.Log(f"WeaponFired Caller: {str(_caller)} StartTrace: {str(_params.StartTrace)} EndTrace: {str(_params.EndTrace)}")
            if GameState.current_map.map_file == "F1 Sanctuary (Gold Chest Room).json":
                map_scripts.f1_sanctuary_chest_room.check_button(_params.EndTrace)
            elif GameState.map_type == MapType.MiniBoss:
                map_scripts.miniboss.miniboss_shootable_objects(GameState.current_map, _params.EndTrace)
            elif GameState.map_type == MapType.RedBarBoss:
                map_scripts.redbarboss.open_gift_box(_params.EndTrace)
            elif GameState.map_type == MapType.StartRoom:
                map_scripts.starting_room.lel_gubs(GameState.current_map, _params.EndTrace)
            elif GameState.current_map.map_file == "E4 Bloodshot Secret Rooms 1.json":
                map_scripts.e4_bloodshot_secret_rooms.check_wall_hit(_params.EndTrace)
            elif GameState.current_map.map_file == "E9 Lair of Infinite Agony Puzzle Rooms 1.json":
                map_scripts.e9_lair_of_infinite_agony_puzzle_rooms.loia_puzzle(GameState.current_map, _params.EndTrace)
            if GameState.current_map.map_file == "A78 Unassuming Docks Mobbing 1.json":
                target = placeablehelper.TAGGED_OBJECTS.get("Target 1")
                if (target is not None
                    and (
                        util.distance(
                            _params.EndTrace,
                            placeablehelper.static_mesh.get_location(target[0].uobj),
                        )
                        < 150
                        and not GameState.current_map.custom_map_data[2]
                    )
                ):
                    GameState.current_map.custom_map_data[2] = True
                    # unrealsdk.Log("Hit Target")
                    threading.Thread(target=map_scripts.a78_unassuming_docks_mobbing.move_boat).start()
            return True
        
        def playermove(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, _params: unrealsdk.FStruct) -> bool:
            if _params.newAccel.X == 0 and _params.newAccel.Y == 0 and _params.newAccel.Z == 0:
                return True
            
            pc = unrealsdk.GetEngine().GamePlayers[0].Actor
            hud_movie: unrealsdk.UObject = pc.GetHUDMovie()
            pawn = pc.Pawn
            pawn_location = pawn.Location

            #pc.ServerSetBadassSkillDisabled(True)
            loaded_map: str = unrealsdk.GetEngine().GetCurrentWorldInfo().GetStreamingPersistentMapName().lower()

            if GameState.map_type == MapType.MiniGame:
                if not GameState.mission_complete:
                    if GameState.current_map.map_file == "E5 Crater Bar Glass Floor 1.json":
                        map_scripts.e5_crater_bar_glass_floor.glass_break_minigame(GameState.current_map)
                    elif GameState.current_map.map_file == "E9 Lair of Infinite Agony Puzzle Rooms 1.json":
                        map_scripts.e9_lair_of_infinite_agony_puzzle_rooms.loia_puzzle_player(GameState.current_map)
                    elif GameState.current_map.map_file == "E10 Digipeak Trivia Mini Game 1.json":
                        map_scripts.e10_digipeak_trivia_mini_game.trivia_questions(GameState.current_map)
                x, y, z = GameState.current_map.custom_map_data[0]
                self.distancetofinish = util.distance(pawn_location, (x, y, z))

                if self.distancetofinish <= 150.00:
                    self.boss_challenge_complete = True
                    # self.update_mission_display()
                    # self.missionComplete = True
                if (
                    (loaded_map == "interlude_p" and pawn_location.Z < -3255.166259765625)
                    or (loaded_map == "iris_dl2_p" and pawn_location.Z < -5242.3671875)
                    or (loaded_map == "iris_moxxi_p" and pawn_location.Z < 3282.876708984375)
                ):
                    pawn.Location = GameState.current_map.spawn_location
                    pawn.Controller.Rotation = GameState.current_map.spawn_rotation

            if (
                (GameState.map_type == MapType.Special and GameState.current_map.name == "Finish")
                and (
                    util.distance(
                        pawn_location,
                        (34699.6328125, 35569.55078125, 3550.85009765625),
                    )
                    < 150
                )
                and not self.themodisdone
            ):
                self.boss_challenge_complete = True
                # self.update_mission_display()
                # pc.ServerSetBadassSkillDisabled(False)
            
            if GameState.map_type == MapType.StartRoom:
                map_scripts.starting_room.check_for_tip()

                if (
                    util.distance(pawn_location, (6038.69873046875, -44883.6328125, -4841.07470703125)) < 250
                    and not GameState.current_map.custom_map_data[1]
                ):
                    GameState.current_map.custom_map_data[1] = True
                    if GameState.level_offset == 0:
                        uFeed.TrainingBox(
                            Title="Tannis note reads:",
                            Message="Hello friend! While I'm away, I could use your help. I've been experimenting with seraph crystals and been able to produce artificial power from them! I won't bore you with the science, but long story short, I was able to build a simulation that I'm calling the <font color='#ff0000'>Roguelands</font>. It simulates combat from our world, and it would be helpful to analyze your combat encounters for... science! Anyways, please step into the simulation when you are ready. Oh! Don’t die… Your neurons are linked to my machines. If you die in the simulation, you die in our world! That shouldn't be a big deal. Off with you! -Tannis",
                            MinDuration=0,
                            PausesGame=True,
                            MenuHint=0,
                            Priority=255,
                        ).Show()
                    elif GameState.level_offset == 1:
                        uFeed.TrainingBox(
                            Title="Tannis note reads:",
                            Message="I've acquired a significant amount of data from your combat encounters, but I feel as it isn't enough. Because of that, I've added more seraph crystal power to the simulation. Things will get tough from here, but I'm sure you can handle it. I'm off getting pizza, and no... you may not have any.\n\n-Tannis",
                            MinDuration=0,
                            PausesGame=True,
                            MenuHint=0,
                            Priority=255,
                        ).Show()
                    elif GameState.level_offset == 2:
                        uFeed.TrainingBox(
                            Title="Tannis note reads:",
                            Message="Good good! It seems that you are more useful than I thought. In order to get the last bit of data I need, I added even more seraph crystal power to the simulation. This will be your hardest challenge yet. Anyways, I need to go put my exotic snail collection in alphabetical order so I will be back later.\n\n-Tannis",
                            MinDuration=0,
                            PausesGame=True,
                            MenuHint=0,
                            Priority=255,
                        ).Show()
                if (
                    util.distance(util.get_player_location(), (5791.79736328125, -43377.20703125, -4518.513671875))
                    < 300
                ) and not self.isinffyl:
                    GameState.map_is_loaded = False
                    placeablehelper.unload_map()

                    for item in unrealsdk.FindAll("WillowPickup")[1:]:
                        item.Behavior_Destroy()

                    GameState.current_map.bosses_killed = 0
                    GameState.current_map.kill_challenge_count = 0
                    GameState.current_map.has_been_visited_in_current_rotation = True

                    self.kill_challenge_complete = False
                    self.boss_challenge_complete = False
                    GameState.mission_complete = False
                    GameState.mission_complete_sound_played = False

                    self.round_counter += 1

                    if self.round_counter % 13 == 0 and GameState.level_offset == 2:
                        # unrealsdk.Log("Picking Finale For Round " + str(self.round_counter))
                        GameState.map_type = MapType.Special
                        GameState.current_map = MAP_DATA[GameState.map_type][1]
                    elif self.round_counter % 13 == 0:
                        # unrealsdk.Log("Picking Mini Game For Round " + str(self.round_counter))
                        GameState.map_type = MapType.MiniGame
                        self.roll_new_map()
                    elif self.round_counter % 13 == 12 and GameState.level_offset == 2:
                        # unrealsdk.Log("Picking Final Boss For Round " + str(self.round_counter))
                        GameState.map_type = MapType.FinalBoss
                        GameState.current_map = MAP_DATA[GameState.map_type][0]
                    elif self.round_counter % 13 == 12:
                        # unrealsdk.Log("Picking Raid Boss For Round " + str(self.round_counter))
                        GameState.map_type = MapType.RaidBoss
                        self.roll_new_map()
                    elif self.round_counter % 13 == 11:
                        # unrealsdk.Log("Picking Gold Chest For Round " + str(self.round_counter))
                        GameState.map_type = MapType.Special
                        GameState.current_map = MAP_DATA[GameState.map_type][0]
                    elif self.round_counter % 13 in (5, 10):
                        # unrealsdk.Log("Picking Red Bar Boss For Round " + str(self.round_counter))
                        GameState.map_type = MapType.RedBarBoss
                        self.roll_new_map()
                    elif self.round_counter % 13 in (4, 9):
                        # unrealsdk.Log("Picking Mini Boss For Round " + str(self.round_counter))
                        GameState.map_type = MapType.MiniBoss
                        self.roll_new_map()
                    else:
                        # unrealsdk.Log("Picking Mobbing For Round " + str(self.round_counter))
                        GameState.map_type = MapType.Mobbing
                        self.roll_new_map()

                    self.draw_timer = False
                    GameState.travel_timer = 3
                    self.draw_minigame_text = 3
                    map_scripts.redbarboss.State.reset()
                    # unrealsdk.Log(
                    # "New Map: " + str(self.round_counter) + " : " + str(GameState.map_type) + " : " + str(GameState.current_map),
                    # )
                    pc.UnclaimedRewards = []
                    pc.ConsoleCommand("camera 1st")
                    util.travel_to_destination(GameState.current_map.travel_object_name)
            if GameState.current_map.map_file == "A20 Tundra Express Mobbing 3.json":
                if util.distance(util.get_player_location(), (-9708.37890625, 11290.0419921875, 791.4130859375)) < 25:
                    pawn.Location = (-7463.6767578125, 9188.490234375, -741.61474609375)
                    pc.ConsoleCommand("camera 3rd")
                if (
                    util.distance(
                        util.get_player_location(),
                        (-8517.263671875, 10214.6181640625, -724.6934814453125),
                    )
                    < 25
                ):
                    pawn.Location = (-7823.2607421875, 11024.740234375, 663.8499755859375)
                    pc.ConsoleCommand("camera 1st")



            # leak starts here
            if GameState.map_is_loaded:
                if GameState.map_type == MapType.Mobbing:
                    map_scripts.mobbing.check_plates()
                    map_scripts.mobbing.check_vault_symbols()

            #unrealsdk.Log(f"AdjustPlayerWalkingMoveAccel: {str(_params)}")
            if GameState.travel_timer > 0:
                self.mission_tracker()
            return True
        
        def wpriinit(_caller: unrealsdk.UObject, _function: unrealsdk.UFunction, _params: unrealsdk.FStruct) -> bool:
            unrealsdk.Log("WPRIInitialized")
            return True

        unrealsdk.RegisterHook(
            "WillowGame.WillowGameViewportClient.PostRender",
            "Postrender",
            render,
        )  # mem leak here but theres nothing more i can do about it
        unrealsdk.RegisterHook("WillowGame.WillowGameViewportClient.Tick", "ViewportTick", tick)
        unrealsdk.RegisterHook(
            "WillowGame.WillowPlayerPawn.SetInjuredDeadState",
            "Death",
            died,
        )  # WillowGame.WillowPlayerPawn.StartInjuredDeathSequence <- original, WillowGame.WillowPlayerPawn.GetInjuredDeadCameraValues <- works for all BUT downed into death barrier
        unrealsdk.RegisterHook("WillowGame.WillowPawn.Died", "PawnDied", pawndied)
        unrealsdk.RegisterHook("WillowGame.WillowPawn.TakeDamage", "PawnDamage", pawndamage)
        unrealsdk.RegisterHook("WillowGame.WillowPlayerController.ShowPauseMenu", "BlockPause", blockpause)
        unrealsdk.RegisterHook("WillowGame.WillowPlayerController.ShowStatusMenu", "BlockStatusMenu", blockstatusmenu)
        unrealsdk.RegisterHook("WillowGame.WillowPawn.SetGameStage", "EnemyLevel", forcelvl80enemies)
        unrealsdk.RegisterHook(
            "WillowGame.WillowPlayerController.StartNewPlaySession",
            "StartNewPlaySession",
            startnewplaysession,
        )
        unrealsdk.RegisterHook("WillowGame.PauseGFxMovie.PromptQuit_Ok", "SaveQuit", savequit)
        unrealsdk.RegisterHook(
            "WillowGame.WillowGameInfo.TeleportToFinalDestinationAfterLoad", # WillowGame.WillowGameInfo.TeleportToFinalDestinationAfterLoad
            "Spawn",
            spawn,
        )  # original spawn hook WillowGame.WillowPlayerController.WillowClientDisableLoadingMovie
        unrealsdk.RegisterHook("WillowGame.WillowGameReplicationInfo.SetCurrentPlaythrough", "PickPlaythrough", setpt3)
        unrealsdk.RegisterHook(
            "WillowGame.WillowPlayerController.CheckNotifyNewGoldenKeys",
            "AllMyHomiesHateGoldenKeyPopups",
            no,
        )
        unrealsdk.RegisterHook(
            "WillowGame.StatusMenuExGFxMovie.DisplayMarketingUnlockDialogIfNecessary",
            "NoMarketingPopups",
            no,
        )
        unrealsdk.RegisterHook("WillowGame.TextChatGFxMovie.AddChatMessage", "ChatCommands", on_chat_command)
        unrealsdk.RegisterHook("WillowGame.WillowPlayerPawn.SetInjuredState", "SetInjuredState", soundplayed)
        unrealsdk.RegisterHook("Engine.Actor.GetActorEyesViewPoint", "FrontEndLoaded", frontendhook)
        unrealsdk.RegisterHook("WillowGame.FrontendGFxMovie.LaunchNewGame", "NoNewGame", sometimesno)
        unrealsdk.RegisterHook("WillowGame.FrontendGFxMovie.LaunchSaveGame", "FrontEndLoaded2", sometimesno)
        unrealsdk.RegisterHook(
            "WillowGame.WillowGFxMenuHelperSaveGame.LoadSelectedCharacter",
            "LoadedNewSave",
            loadsavegame,
        )
        unrealsdk.RegisterHook("WillowGame.WillowHUD.ShowRespawnDialog", "ShowRespawnDialog", died2)
        unrealsdk.RegisterHook(
            "WillowGame.WillowInteractiveObject.SetCompassIcon",
            "RemoveCompassIcons",
            nocompassicons,
        )
        #unrealsdk.RegisterHook("WillowGame.WillowPlayerController.ClientCloseMenu", "CloseStatusMenu", closestatusmenu)
        unrealsdk.RegisterHook("WillowGame.WillowPlayerController.GFxPauseMenuClosed", "ClosePauseMenu", closepausemenu)
        unrealsdk.RegisterHook("WillowGame.WillowPlayerController.DisplaySkillPointsPrompt", "NoSkillPointReminder", no)
        unrealsdk.RegisterHook("WillowGame.WillowLightProjectileManager.AddProj", "AddProjectile", hitloc)
        unrealsdk.RegisterHook("Engine.PlayerController.AdjustPlayerWalkingMoveAccel", "PlayerMove", playermove)
        #unrealsdk.RegisterHook("Engine.PlayerReplicationInfo.PostBeginPlay", "WPRIInitialized", wpriinit)
        # unrealsdk.RegisterHook("WillowGame.WillowPlayerController.DisplayHUDMessage", "ChallengePopup2", gimmechallengename)
        # unrealsdk.RegisterHook("Engine.Canvas.DrawText", "DrawText", localizetext)
        # unrealsdk.RegisterHook("Engine.Actor.ReplaceText", "ReplaceText", replacetext)

        super().Enable()

    def Disable(self) -> None:
        uFeed.TrainingBox(
            Title="Persistent Changes",
            Message="Restart the game to fully remove all mod changes.",
            MinDuration=0,
            PausesGame=False,
            MenuHint=0,
            Priority=255,
        ).Show()
        Looties.Disable()
        unrealsdk.RemoveHook("WillowGame.WillowGameViewportClient.PostRender", "Postrender")
        unrealsdk.RemoveHook("WillowGame.WillowGameViewportClient.Tick", "ViewportTick")
        unrealsdk.RemoveHook("WillowGame.WillowPlayerPawn.SetInjuredDeadState", "Death")
        unrealsdk.RemoveHook("WillowGame.WillowPawn.Died", "PawnDied")
        unrealsdk.RemoveHook("WillowGame.WillowPlayerController.ShowPauseMenu", "BlockPause")
        unrealsdk.RemoveHook("WillowGame.WillowPlayerController.ShowStatusMenu", "BlockStatusMenu")
        unrealsdk.RemoveHook("WillowGame.WillowPawn.SetGameStage", "EnemyLevel")
        unrealsdk.RemoveHook("WillowGame.WillowPlayerController.StartNewPlaySession", "StartNewPlaySession")
        unrealsdk.RemoveHook("WillowGame.PauseGFxMovie.PromptQuit_Ok", "SaveQuit")
        unrealsdk.RemoveHook("WillowGame.WillowGameInfo.TeleportToFinalDestinationAfterLoad", "Spawn")
        unrealsdk.RemoveHook("WillowGame.WillowGameReplicationInfo.SetCurrentPlaythrough", "PickPlaythrough")
        unrealsdk.RemoveHook(
            "WillowGame.WillowPlayerController.CheckNotifyNewGoldenKeys",
            "AllMyHomiesHateGoldenKeyPopups",
        )
        unrealsdk.RemoveHook(
            "WillowGame.StatusMenuExGFxMovie.DisplayMarketingUnlockDialogIfNecessary",
            "NoMarketingPopups",
        )
        unrealsdk.RemoveHook("WillowGame.TextChatGFxMovie.AddChatMessage", "ChatCommands")
        unrealsdk.RemoveHook("WillowGame.WillowPlayerPawn.SetInjuredState", "SetInjuredState")
        unrealsdk.RemoveHook("Engine.Actor.GetActorEyesViewPoint", "FrontEndLoaded")
        unrealsdk.RemoveHook("WillowGame.FrontendGFxMovie.LaunchNewGame", "NoNewGame")
        unrealsdk.RemoveHook("WillowGame.FrontendGFxMovie.LaunchSaveGame", "FrontEndLoaded2")
        unrealsdk.RemoveHook("WillowGame.WillowGFxMenuHelperSaveGame.LoadSelectedCharacter", "LoadedNewSave")
        unrealsdk.RemoveHook("WillowGame.WillowHUD.ShowRespawnDialog", "ShowRespawnDialog")
        unrealsdk.RemoveHook("WillowGame.WillowInteractiveObject.SetCompassIcon", "RemoveCompassIcons")
        #unrealsdk.RemoveHook("WillowGame.WillowPlayerController.ClientCloseMenu", "CloseStatusMenu")
        unrealsdk.RemoveHook("WillowGame.WillowPlayerController.GFxPauseMenuClosed", "ClosePauseMenu")
        unrealsdk.RemoveHook("WillowGame.WillowPlayerController.DisplaySkillPointsPrompt", "NoSkillPointReminder")
        unrealsdk.RemoveHook("WillowGame.WillowLightProjectileManager.AddProj", "AddProjectile")
        unrealsdk.RemoveHook("Engine.PlayerController.AdjustPlayerWalkingMoveAccel", "PlayerMove")
        #unrealsdk.RemoveHook("Engine.PlayerReplicationInfo.PostBeginPlay", "WPRIInitialized")
        # unrealsdk.RemoveHook("WillowGame.WillowPlayerController.DisplayHUDMessage", "ChallengePopup2")
        # unrealsdk.RemoveHook("Core.Object.Localize", "LocalizeText")
        # unrealsdk.RemoveHook("Engine.Actor.ReplaceText", "ReplaceText")
        super().Disable()


instance = Main()

ModMenu.RegisterMod(instance)

# py unrealsdk.Log(str(unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn.Location))
# py unrealsdk.Log(str(unrealsdk.GetEngine().GamePlayers[0].Actor.Pawn.Controller.Rotation))
"""
funny meme pools/items

items
GD_Aster_Artifacts.A_Item_Unique.A_MysteryAmulet

pools
GD_Anemone_Plot_Mission060.ItemPool.IP_BeerBottle
GD_Iris_ItemPools.Achievements.ItemPool_MoxxiPicture
GD_Itempools.BuffDrinkPools.Pool_BuffDrinks_Toughness (turtle up, i dont think this does anything other than screen particles for way too long)
GD_LevelEchoChallenges.ItemPool.IP_LevelEchoChallenge (lost echo that plays nothing)
"""
