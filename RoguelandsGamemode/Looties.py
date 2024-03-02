from __future__ import annotations

from unrealsdk import GetEngine, Log #type: ignore
from unrealsdk import ConstructObject, FindObject, KeepAlive #type: ignore
from unrealsdk import DoInjectedCallNext, RemoveHook, RunHook #type: ignore
from unrealsdk import FStruct, UFunction, UObject, UPackage #type: ignore

from random import getrandbits

from typing import Any, Callable, Dict, Generator, Iterable, List, Optional, Tuple, Union


NamePrefix: str = "Loot"

Rarity: int = 8
"""
How rarely enemies should roll as loot variants. A value of 0 means every (eligible) enemy spawns as
a loot variant, 1 means 1/2 of enemies will, 2 means 1/4 will, etcetera. The default is 8, or 1/256.
"""

Skill: UObject
"""The SkillDefinition object activated for each loot enemy after they spawn."""

LootBehavior: UObject
"""The Behavior_SpawnLootAroundPoint object which spawns loot on each loot enemies' death."""

AIRollBlacklist: List[Optional[str]] = [
    None,
    "CharClass_Bloodwing", # Bloodwing
    "CharClass_BunkerBoss", # Bunker
    "CharacterClass_Orchid_BossWorm", # Leviathan
    "CharClass_DragonHeart_Raid", # Fake healthbar for Ancient Dragons
    "CharClass_GoliathBossProxy", # Fake healthbar for Happy Couple
]
"""
AIClassDefinition names whose pawns should not roll as Giants. This is in addition to the
existing restrictions against all "badass" enemies.
"""

_ai_bequeath_whitelist: Tuple[str, ...] = (
    "CharClass_InfectedPodTendril", # Infected Pods
    "CharClass_Pumpkinhead", # Pumpkin Kingpin
    "CharClass_Skeleton_Fire", # Flaming Skeleton
    "CharClass_Skeleton_King", # Skeleton King
    # Varkids
    "CharClass_Anemone_BugMorph_Basic",
    "CharClass_BugMoprhUltimate",
    "CharClass_BugMorph",
    "CharClass_BugMorph_Adult",
    "CharClass_Bugmorph_Badass",
    "CharClass_Bugmorph_SuperBadass",
    "CharClass_Nast_BugMorph_BadassBloodhound",
    "CharClass_Nast_BugMorphTreasure",
    "CharClass_Nasturtium_BugMorph_Acid",
    "CharClass_Nasturtium_BugMorph_Badass",
    "CharClass_Nasturtium_BugMorph_Bloodhound",
    "CharClass_Nasturtium_BugMorph_Fire_Holiday",
    "CharClass_Nasturtium_BugMorph_Miami",
    "CharClass_Nasturtium_BugMorph_Rasta",
    "CharClass_Nasturtium_BugMorph_Shock",
    "CharClass_Nasturtium_BugMorph_Tropical",
)
"""AIClassDefinition names whose pawns should pass on Gigantism to their child pawns."""

_ai_loot_blacklist: Tuple[str, ...] = (
    "CharClass_Assassin_Hologram", # Zer0's hologram
    "CharClass_Aster_Roland_Turret", # Roland's turret
    "CharClass_DeathTrap", # Deathtrap
    "CharClass_RakkVolcanic", # Volcanic Rakk
    "CharClass_RolandDeployableTurret", # Roland's turret
    "CharClass_Scorpio", # Axton's Turret
    "CharClass_Skeleton_King", # Skeleton Kings (these drop loot via their head pawns)
    "CharClass_TargetDummy", # Target dummy
    "CharClass_TargetDummy_Shield", # Target dummy
    "CharClass_TargetDummy_Target", # Target dummy
    "CharClass_TargetDummyBot", # Target dummy
)
"""AIClassDefinition names whose pawns should not drop loot on death."""

_ai_badass_overrides: Dict[Optional[str], bool] = {
    "CharacterClass_Anemone_SandWormBoss_1": True, # Haderax
    "CharacterClass_Anemone_SandWormQueen": True, # Sandworm Queen
    "CharacterClass_Orchid_SandWormQueen": True, # Sand Worms Queens
    "CharClass_Anemone_Cassius": True, # Cassius
    "CharClass_Anemone_Hector": True, # Hector
    "CharClass_Anemone_Infected_Golem_Badass": True, # Infected Badass Golem
    "CharClass_Anemone_Lt_Angvar": True, # Angvar
    "CharClass_Anemone_Lt_Bolson": True, # Bolson
    "CharClass_Anemone_Lt_Hoffman": True, # Hoffman
    "CharClass_Anemone_Lt_Tetra": True, # Tetra
    "CharClass_Anemone_UranusBOT": True, # Uranus
    "CharClass_Aster_GenericNPC": False, # Flamerock Citizen
    "CharClass_BlingLoader": True, # BLING Loader
    "CharClass_Boll": True, # Boll
    "CharClass_BugMorph_Bee_Badass": True, # Badass Stabber Jabber
    "CharClass_CommunityMember": False, # Flamerock Citizen?
    "CharClass_Dragon": True, # Ancient Dragons
    "CharClass_FlyntSon": True, # Sparky Flynt
    "CharClass_GateGuard": False, # Davlin
    "CharClass_Golem_SwordInStone": True, # Unmotivated Golem
    "CharClass_Iris_BikeRiderMarauderBadass": True, # Badass Biker
    "CharClass_Iris_MotorMamaBike": True, # Motor Mama's Bike
    "CharClass_Iris_Raid_PyroPete": True, # Raid Pete
    "CharClass_Juggernaut": True, # Juggernauts
    "CharClass_Orchid_Deserter_Cook": True, # Terry
    "CharClass_Orchid_Deserter_Deckhand": True, # Deckhand
    "CharClass_Orchid_LittleSis": True, # Lil' Sis
    "CharClass_Orchid_RaidShaman": True, # Master Gee
    "CharClass_RakkBadass": True, # Badass Rakks
    "CharClass_Sage_AcquiredTaste_Creature": True, # Bulstoss
    "CharClass_Sage_Ep3_Creature": True, # Thermitage
    "CharClass_Sage_Raid_Beast": True, # Vorac
    "CharClass_Sage_Raid_BeastMaster": True, # Chief Ngwatu
    "CharClass_Sage_Rhino": True, # Der monwahtever
    "CharClass_Sage_RhinoBasass": True, # Borok Badasses
    "CharClass_Sage_ScaylionQueen": True, # Queen Scaylions
    "CharClass_SarcasticSlab": True, # Sarcastic Slab
    "CharClass_Skeleton_Immortal": False, # Immortal Skeleton
    "CharClass_Spiderpants": True, # Spiderpants
    "CharClass_SpiderTank_Baricade": False, # BAR-TNK
    "CharClass_Tentacle_Slappy": False, # Old Slappy TentacleZ`
    "CharClass_Thresher_Raid": True, # Terramorphus
    "CharClass_TundraPatrol": True, # Will
    "CharClass_Darkness": True, # The Darkness
    "CharClass_Mimic": True, # Mimic
}
""" """

_friendship_definition: Tuple[Any, ...]

_willow_item: UObject
_friendship_skill: UObject

def _activate_skill(caller: UObject, function: UFunction, params: FStruct):
    pc = GetEngine().GamePlayers[0].Actor
    return params.Definition != _friendship_skill or params.SkillInstigator != pc



"""
Enemy and NPC spawns in Borderlands 2 are implemented with transient WillowAIPawn objects. The base
concept of Reign Of Giants is to intercept WillowAIPawn objects, perform an RNG roll for their
Gigantism, then perform modifications to ones which roll Gigantism and track them throughout their
life cycle.

One difficulty in working with transient WillowAIPawns is that, once we have taken an interest in
one (i.e. once we have selected it to be a Giant), we have no way with the SDK to guarantee we will
be made aware of its destruction. Any attempt to access a destroyed instance will result in garbage
data or a crash. This means we cannot create lists in Python which track WillowAIPawn objects, and
also we cannot easily associate our own Python data with individual pawns.

Instead, we can store our data in Unreal Engine objects attached to the WillowAIPawns. For iterating
WillowAIPawns in order to find ones we are interested in, conveniently the game maintains a linked
list of each extant pawn.
"""
class aipawn:
    """A wrapper for WillowAIPawns that provides functionality relevant to our usage of them."""

    __slots__ = "uobject"
    uobject: UObject

    def __init__(self, uobject: UObject):
        self.uobject = uobject


    @classmethod
    def all(cls) -> Generator[aipawn, None, None]:
        """Yield an object for every WillowAIPawn (and subclass) that has an AIClass."""

        # All pawns currently spawned on the map form a linked list with one another, the start of
        # which is accessible from the current world info object.
        pawn = GetEngine().GetCurrentWorldInfo().PawnList
        while pawn is not None:
            # If the pawn has an AIClass, we can be sure it is a WillowAIPawn that is of use to us.
            if pawn.AIClass is not None:
                yield cls(pawn)
            # Continue to the next item in the linked list, if any.
            pawn = pawn.NextPawn


    @property
    def ai_class(self) -> Optional[str]:
        """
        The name of the pawn's AIClassDefinition, if it has one. This can be used to identify what
        type of enemy (or NPC) this pawn represents.
        """
        ai_class = self.uobject.AIClass
        return None if ai_class is None else ai_class.Name


    @property
    def grade_index(self) -> int:
        """
        The grade index of the pawn's balance definition state. This is used to apply modifiers to
        the pawn's balance, however it appears to always be set to -1 (no modifiers) to WillowAIPawn
        objects. The grade index is useful as it is replicated to client instances of the pawn.
        """
        return self.uobject.BalanceDefinitionState.GradeIndex

    @grade_index.setter
    def grade_index(self, grade_index: int) -> None:
        self.uobject.BalanceDefinitionState.GradeIndex = grade_index


    @property
    def balance(self) -> Optional[UObject]:
        """
        The pawn's BalanceDefinition. This contains additional information about the pawn, like
        its name, and whether it is a badass.
        """
        return self.uobject.BalanceDefinitionState.BalanceDefinition


    @property
    def is_badass(self) -> bool:
        """Whether we deem the pawn to be a badass."""

        # If the pawn has a balance, default to its value; otherwise, default to false. Use the
        # default if we don't have a specific override for the pawn's AI class.
        is_champion = False if self.balance is None else self.balance.Champion
        return _ai_badass_overrides.get(self.ai_class, is_champion)


    def encode_ID(self, ID: int) -> None:
        """
        Encode the provided grade index and ID number into a single int. This assumes a grade index
        between -32,767 and 32,768, and an ID between 0 and 65,536.
        """

        # Add 32,767 to the grade index to yield a non-negative integer that is still less than 65,536,
        # thus ensuring it's not using over 16 bits. Shift the ID 16 bits to the right, and OR it in.
        self.grade_index = (self.grade_index + 32767) ^ (ID << 16)


    @property
    def vanilla_grade_index(self) -> int:
        """Return the original grade index that was encoded into the provided grade index value."""

        # Remove any bits from all but the leftmost 16, thus deleting the encoded ID. Subtract the
        # 32,767 that was originally added in, yielding the original grade index.
        return (self.grade_index & 0xFFFF) - 32767


    @property
    def ID(self) -> int:
        """Return the ID number that was encoded into the provided grade index value."""

        # Shift the provided grade index 16 bits to the left, deleting the encoded grade index, and
        # returning the ID as it was originally provided.
        return (self.grade_index >> 16)


    @property
    def is_giant(self):
        """Whether the pawn has been selected for Gigantism."""
        record = self.uobject.DebugPawnMarkerInst
        return record is not None and record.Name == "RoguelandsLootEnemies"
    

    def initialize_giant(self) -> None:
        """Configure our custom storage object on a WillowAIPawn that was selected for Gigantism."""

        # The DebugPawnMarkerInst property on WillowAIPawns takes a UObject, and is not utilized
        # anywhere in the vanilla game. Since it's not utilized in vanilla, We may set it to an
        # object of our own creation, and use that to store data relevant to the Giant.
        self.uobject.DebugPawnMarkerInst = ConstructObject("KnowledgeRecord", self.uobject, "RoguelandsLootEnemies")
        self.should_drop_loot = True


    def roll_gigantism(self, force: bool = False) -> bool:
        """
        Roll whether the given pawn should be a Giant. If so, apply the server-only modifications to
        it, followed by the server/client modifications, returning the resulting Giant object.
        """

        # If the pawn is already selected as a Giant, return it.
        if self.is_giant:
            return True

        # If the pawn's AI class is in our blacklist, don't roll gigantism for it.
        if self.uobject.MyWillowMind is None or self.ai_class in AIRollBlacklist:
            return False
        
        # If we were told to force a giant for this pawn, do so.
        if force:
            self.initialize_giant()
            return True

        # If the pawn is a badass, it is not eligible to roll for gigantism.
        if self.is_badass:
            return False

        # Unless we are in cheat mode or were told to force a giant, We roll 8 bits (1 in 256) to
        # determine whether the pawn will be a giant or not.
        if Rarity == 0 or getrandbits(Rarity) == 0:
            self.initialize_giant()
            return True

        return False


    def gigantize(self):
        """Growwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"""
        player_pawn = GetEngine().GamePlayers[0].Actor.Pawn
        for _ in range(4):
            relic = _willow_item.CreateItemFromDef(_friendship_definition, player_pawn, 1)
            self.uobject.EquipItem(relic)

        self.uobject.MyWillowMind.Behavior_ActivateSkill(_friendship_skill)
        self.uobject.MyWillowMind.Behavior_ActivateSkill(Skill)


    @property
    def vanilla_name_list_index(self) -> int:
        """
        The original name list index for the Giant's pawn before we modified it. We use it when we
        need to temporarily revert the pawn's vanilla name list index to regenerate its name.
        """
        return self.uobject.DebugPawnMarkerInst.FlagIndex if self.is_giant else self.uobject.NameListIndex
    
    @vanilla_name_list_index.setter
    def vanilla_name_list_index(self, index: int) -> None:
        if self.is_giant:
            self.uobject.DebugPawnMarkerInst.FlagIndex = index


    @property
    def should_drop_loot(self) -> bool:
        """
        Whether the Giant should drop loot on death. This is set to `True` on client gigantism, but
        will be toggled off if the Giant has spawned a child pawn.
        """
        return self.is_giant and bool(self.uobject.DebugPawnMarkerInst.Active)
    
    @should_drop_loot.setter
    def should_drop_loot(self, should: bool) -> None:
        if self.is_giant:
            self.uobject.DebugPawnMarkerInst.Active = should


    def giant_name(self) -> str:
        """Generate the Giant-ized name based on the current vanilla name."""

        # If this pawn's balance has not yet been applied, skip it.
        if self.balance is None:
            return ""

        # The following is a port of GetTargetName.
        name = None

        if -1 < self.vanilla_name_list_index < _vanilla_name_list_length:
            name = list(_name_list.Names)[self.vanilla_name_list_index]

        # If the pawn is set to display it's parent's name, do so without giant-izing it.
        elif self.uobject.DisplayParentInfo() and self.uobject.GetParent() is not None:
            return self.uobject.GetParent().GetTargetName()

        else:
            if self.uobject.TransformType != 0:
                name = self.uobject.GetTransformedName()
            else:
                name = self.balance.GetDisplayNameAtGrade(-1)

            if name is None and self.uobject.AIClass is not None:
                name = self.uobject.AIClass.DefaultDisplayName

        if name is None:
            return ""

        # Before we potentially format this name for a pet presentation, prefix it.
        name = f"{NamePrefix} {name}"

        if self.uobject.PlayerMasterPRI is not None:
            masterName = self.uobject.PlayerMasterPRI.GetHumanReadableName()
            if len(masterName) > 0:
                name = self.uobject.MasteredDisplayName.replace("%s", masterName).replace("%n", name)

        return name


    def bequeath_gigantism(self, child: UObject):
        """
        If this pawn is of an AI class which undergoes "transformation" by spawning a child pawn,
        then dying, ensure the child pawn inherits its Gigantism, and that this pawn won't drop loot
        when it "dies."
        """
        if self.is_giant and self.ai_class in _ai_bequeath_whitelist:
            self.should_drop_loot = False
            type(self)(child).roll_gigantism(force=True)


    def drop_loot(self) -> None:
        """
        Drop loot, assuming the pawn is marked to do so, and its AI class is not in our list of ones
        whose pawns should not.
        """
        if self.should_drop_loot and self.ai_class not in _ai_loot_blacklist:
            # Invoke our loot spawning behavior with our UObject as the context.
            LootBehavior.ApplyBehaviorToContext(self.uobject, (), None, None, None, ())


"""
A significant aspect of Reign Of Giants is the adjusting of individual WillowAIPawns to include
"Giant" in the name displayed to the player. To determine what name is displayed, the game invokes
GetTargetName on its WillowAIPawn. This function accepts an `out` parameter through which it passes
the final name. The SDK cannot alter `out` parameters, so instead we must hijack the mechanisms
accessed in GetTargetName.

GetTargetName checks a series of conditionals to determine the pawn's name, so we must use the first
one to ensure our altered name is chosen. Each WillowAIPawn has a NameListIndex property, an integer
that refers to an entry in the current GameReplicationInfo's NameListDefinition. We can add strings
to this list, and individually set pawn's NameListIndex to point to those new strings.
"""
_name_list: UObject
"""A persistent NameListDefinition to which we copy vanilla fixup names, then append our custom
giant names. This will be assigned as the GameReplicationInfo's NameListDef in every map."""

_vanilla_name_list_length: int
"""The original length of the GameReplicationInfo's NameListDefinition for the current map."""

_vanilla_name_list_names: str
"""
The items of the vanilla name list for the current map, in a format suitable for insertion into a
set console command.
"""

_level_address: int = 0
""" """


"""
In co-op play, WillowAIPawns are represented on clients as their own WillowAIPawn instances, that
have various attributes replicated from the host's instance. In Reign Of Giants, we need clients'
instances to be Gigantized when they are Gigantized on the server.

Unfortunately there is no apparent way of easily identifying which WillowAIPawn instances on clients
correspond to ones on host. We solve this by generating an ID number for each pawn, and encoding it
into a property which the game replicates between host and client instances.
"""
_giant_IDs: List[int] = []
"""The IDs for pawns that the server has reported as Giants, in order of their NameListIndex."""


_package: Optional[UPackage]
"""A custom UPackage used to maintain a persistent namespace for our custom UObjects."""


"""
The SDK has difficulties with certain things; namely, strings allocated by the SDK currently cause a
crash when deallocated by Unreal Engine. Also, it rejects tuples being assigned to FStructs if we
attempt to pass None when the field expects a UObject. Both of these issues can be worked around by
using a `set` console command to apply these "problematic" values to properties.
"""
def _set_command(obj: UObject, property: str, value: Union[str, Iterable[str]]) -> None:
    """Perform a console command to set the given object's property to the specified value(s)."""

    if isinstance(value, str):
        command = f"set {UObject.PathName(obj)} {property} {value}"
    else:
        command = f"set {UObject.PathName(obj)} {property} ({','.join(value)})"

    GetEngine().GamePlayers[0].Actor.ConsoleCommand(command, False)


def _array_string(string: str) -> str:
    """
    Return the string with its quotes escaped, enclosed in quotes, followed by a comma. This format
    is suitable for concatenation into an array as the value for a `set` console command.
    """
    string = string.replace('"', '\\"')
    return f"\"{string}\","


def _defer_to_tick(name: str, callable: Callable[[], Optional[bool]]) -> None:
    """Schedule a routine to be invoked each game tick until it returns True."""

    # Create a wrapper to call the routine that is suitable to be passed to RunHook.
    def tick(caller: UObject, function: UFunction, params: FStruct) -> bool:
        # Invoke the routine. If it returns False, unregister its tick hook.
        if not callable():
            RemoveHook("WillowGame.WillowGameViewportClient.Tick", "RoguelandsLootEnemies." + name)
        return True

    # Hook the wrapper.
    RunHook("WillowGame.WillowGameViewportClient.Tick", "RoguelandsLootEnemies." + name, tick)


def _prepare_lists() -> Optional[bool]:
    """
    If it has not yet been done in the current map, prepare the name list variables and set of
    WillowAIPawn subclasses.
    """
    global _level_address

    # Get the current world info, and the address of the current level object.
    world_info = GetEngine().GetCurrentWorldInfo()
    current_level_address = world_info.CommittedPersistentLevel.GetAddress()

    # If we are missing either a game replication or player replication object, we are a client in a
    # new game session, and must defer a request for the current Giants state until we have both.
    if world_info.GRI is None or GetEngine().GamePlayers[0].Actor.PlayerReplicationInfo is None:
        _level_address = current_level_address
        return None

    # If the address of the current level object matches our existing record, we're still in the
    # same level, and do not need to perform setup.
    if _level_address == current_level_address:
        return None
    # With a new level, update our record of its address.
    _level_address = current_level_address

    # Initialize our records of the vanilla name list's length and items.
    global _vanilla_name_list_length, _vanilla_name_list_names
    _vanilla_name_list_length = 0
    _vanilla_name_list_names = ""

    # If the vanilla name list does in fact exist in this map, populate our records with its values.
    if world_info.GRI.NameListDef is not None and world_info.GRI.NameListDef.Names is not None:
        for name in world_info.GRI.NameListDef.Names:
            _vanilla_name_list_length += 1
            _vanilla_name_list_names += _array_string(name)

    # Assign our name list to the GRIs, and schedule an update for the name list's contents.
    world_info.GRI.NameListDef = _name_list
    _defer_to_tick("UpdatePawns", _update_pawns)

    return None


def _update_pawns() -> Optional[bool]:
    """
    Update our name list to contain the contents of the vanilla one, as well as the current name of
    each Giant. This should be scheduled to be run on a game tick, so as to consolidate multiple
    requests for updates that may occur in quick succession.
    """

    # Iterate over every current WillowAIPawn object. Record the ID for each pawn that has one, each
    # pawn that does not yet have an ID, and each pawn that is a Giant.
    IDs = set()
    IDless_pawns = []
    giant_pawns = []

    for pawn in aipawn.all():
        ID = pawn.ID
        if ID > 0:
            IDs.add(ID)
        else:
            IDless_pawns.append(pawn)

        if pawn.is_giant:
            giant_pawns.append(pawn)

    # Starting with 1, find IDs that are not currently in use, assigning them to the pawns that did
    # not yet have an ID.
    new_ID = 1
    for IDless_pawn in IDless_pawns:
        while new_ID in IDs:
            new_ID += 1
        IDless_pawn.encode_ID(new_ID)
        new_ID += 1

    # Initialize our list of Giants' IDs, and begin the "array" of new names with the vanilla ones.
    global _giant_IDs
    _giant_IDs = []
    name_list_names = _vanilla_name_list_names

    # For each Giant pawn that was found, add its ID to the list of Giants' IDs, add its name to the
    # names "array," and set its NameListIndex to the index it will be found in the list.
    for giant_index, giant_pawn in enumerate(giant_pawns):
        _giant_IDs.append(giant_pawn.ID)
        name_list_names += _array_string(giant_pawn.giant_name())
        giant_pawn.uobject.NameListIndex = _vanilla_name_list_length + giant_index

    # Apple the new names to the name list, and send the new list of Giants' IDs to clients.
    _set_command(_name_list, "Names", f"({name_list_names})")

    return None


def _gigantize_pawns() -> Optional[bool]:
    """
    From the current list of Giants' IDs, find each Giant pawn, Gigantize them, and update the names
    list with their Gigantized names, in order.
    """

    # Get the current game replication info. If it has not yet been created, tick until it has.
    GRI = GetEngine().GetCurrentWorldInfo().GRI
    if GRI is None:
        return True

    # Create a list of empty strings as long as the number of Giants.
    giant_names = [""] * len(_giant_IDs)

    # For each current pawn, attempt to locate the index of its ID in the list of Giants' IDs.
    for pawn in aipawn.all():
        try:
            giant_index = _giant_IDs.index(pawn.ID)
        # If the pawn's ID is not in the in the list of Giant IDs, skip it.
        except ValueError:
            continue

        # If we encounter a Giant that is not yet had its, balance definition applied, stop here and
        # try again on the next tick.
        if pawn.balance is None:
            return True

        pawn.gigantize()

        # Generate the Giant's name and place it in the names list at the Giant's index.
        giant_names[giant_index] = pawn.giant_name()
        # The Giant's name's index in the names list will be its index relative to the end of
        # the vanilla ones.
        pawn.uobject.NameListIndex = _vanilla_name_list_length + giant_index

    # Start the new names list with the vanilla ones, then append each Giant's name in order.
    name_list_names = _vanilla_name_list_names
    for name in giant_names:
        name_list_names += _array_string(name)

    # Make sure our name list is applied to the world info, and apply our names to it.
    GRI.NameListDef = _name_list
    _set_command(_name_list, "Names", f"({name_list_names})")

    return None


def _aipawn_post_begin_play(caller: UObject, function: UFunction, params: FStruct) -> bool:
    """
    Every single WillowAIPawn, even ones without balances, have this method called after being
    spawned.
    """
    _prepare_lists()

    # Temporarily remove our hook for this method before invoking injecting its call now.
    RemoveHook("WillowGame.WillowAIPawn.PostBeginPlay", "RoguelandsLootEnemies")
    DoInjectedCallNext()
    caller.PostBeginPlay()
    RunHook("WillowGame.WillowAIPawn.PostBeginPlay", "RoguelandsLootEnemies", _aipawn_post_begin_play)

    # If a bogus name list index was applied to the pawn, sanitize it now to prevent it from kicking
    # in with the names we add to the name list.
    if caller.NameListIndex >= _vanilla_name_list_length:
        caller.NameListIndex = -1
    return False


def _setup_balanced_population(caller: UObject, function: UFunction, params: FStruct) -> bool:
    """
    All pawn entities that we are concerned with are passed through a routine that applies a number
    of properties to them, such as their balance definition and spawn point.
    """

    # The new pawn and its "spawn point" object are passed as parameters.
    pawn = params.SpawnedPawn
    spawn = params.SpawnLocationContextObject
    if pawn is None or spawn is None:
        return True

    # If the spawn point has a WillowAIPawn as its Owner, then that is the parent pawn of the new,
    # pawn, so tell it to bequeath its Gigantism to the new pawn, if applicable.
    if spawn.Owner is not None and spawn.Owner.AIClass is not None:
        aipawn(spawn.Owner).bequeath_gigantism(pawn)

    return True


def _apply_balance_customizations(caller: UObject, function: UFunction, params: FStruct) -> bool:
    """
    All WillowAIPawns that we are interested in will be configured with a balance definition. Once
    it has been assigned to them, this method is called to apply its contents to the pawn's
    properties involving its target name, whether it's a badass, and other things. This must take
    place after any initializations of the pawn for its AI class.
    """
    _prepare_lists()

    if caller.AIClass is None:
        return True

    pawn = aipawn(caller)

    # If we are not a client, Roll Gigantism for the pawn (if it had not already inherited it from
    # its parent in SetupBalancedPopulationActor).
    is_giant = pawn.roll_gigantism()

    # Get the pawn's ID from its grade index. If it has one, revert its grade index to the vanilla
    # value before proceeding. If it doesn't, schedule a pawn update to assign it one.
    ID = pawn.ID
    if ID > 0:
        pawn.grade_index = pawn.vanilla_grade_index

    # Temporarily remove this hook before invoking the original method.
    RemoveHook("Engine.Pawn.ApplyBalanceDefinitionCustomizations", "RoguelandsLootEnemies")
    DoInjectedCallNext()
    caller.ApplyBalanceDefinitionCustomizations()
    RunHook("Engine.Pawn.ApplyBalanceDefinitionCustomizations", "RoguelandsLootEnemies", _apply_balance_customizations)

    # If the pawn had an ID, re-encode it now.
    if ID > 0:
        pawn.encode_ID(ID)

    # Ensure the resulting name list index applied to the pawn isn't bogus, to prevent it from
    # kicking in with the names we added to the names list.
    if caller.NameListIndex >= _vanilla_name_list_length:
        caller.NameListIndex = -1

    # If we did roll a giant, update its balance-dependent properties, then update the name list.
    if is_giant:
        pawn.vanilla_name_list_index = caller.NameListIndex
        pawn.gigantize()
        _defer_to_tick("UpdatePawns", _update_pawns)

    return False


def _replicated_event(caller: UObject, function: UFunction, params: FStruct) -> bool:
    """
    WillowAIPawns that exist on the server are only guaranteed to exist on the client when the
    client is engaged with them. When they do, the server periodically sends replicated events about
    them to indicate things like the values of properties having been updated.
    """

    # If we are being notified of this pawn's balance definition state, this instance has just been
    # freshly replicated to this client, so we should check whether it needs to be gigantized.
    if params.VarName == "BalanceDefinitionState" and aipawn(caller).ID in _giant_IDs:
        _defer_to_tick("GigantizePawns", _gigantize_pawns)

    return True


def _ai_level_up(caller: UObject, function: UFunction, params: FStruct) -> bool:
    """
    When an AI undergoes a transformation that involves it leveling up, this method is called on
    both server and client.
    """

    DoInjectedCallNext()
    caller.AILevelUp()

    # If this pawn is already a Giant, update its name.
    pawn = aipawn(caller)
    if pawn.is_giant:
        _defer_to_tick("UpdatePawns", _update_pawns)

    # If we are not a client player, give the pawn a new roll at being a Giant.
    elif pawn.roll_gigantism():
        pawn.vanilla_name_list_index = caller.NameListIndex
        pawn.gigantize()
        _defer_to_tick("UpdatePawns", _update_pawns)

    return False


def _behavior_transform(caller: UObject, function: UFunction, params: FStruct) -> bool:
    """
    Various WillowAIPawns are able to undergo "transformation" (e.g. Varkids, Goliaths). When this
    occurs, a Behavior_Transform object is invoked with the pawn as the context object, and that
    pawn's TransformType is simply updated with that of the behavior object.
    """

    # When one of our giants has a transform invoked on them, we update their name.
    pawn = aipawn(params.ContextObject)
    if pawn.is_giant:
        params.ContextObject.TransformType = caller.Transform
        _defer_to_tick("UpdatePawns", _update_pawns)

    return True


def _died(caller: UObject, function: UFunction, params: FStruct) -> bool:
    """All WillowAIPawns die someday. Circle of WillowAILife."""

    aipawn(caller).drop_loot()
    return True


def Enable() -> None:
    """Create our custom package and its subobjects."""
    global _friendship_definition, _willow_item, _friendship_skill
    global _package, _name_list, LootBehavior, Skill

    _friendship_definition = (
        # ItemDefinition
        FindObject("ArtifactDefinition", "GD_Aster_Artifacts.A_Item_Unique.Artifact_MysteryAmulet"),
        # BalanceDefinition
        FindObject("InventoryBalanceDefinition", "GD_Aster_Artifacts.A_Item_Unique.A_MysteryAmulet"),
        # ManufacturerDefinition
        FindObject("ManufacturerDefinition", "GD_Manufacturers.Artifacts.Artifact_TypeA"),
        # ManufacturerGradeIndex
        1,
        # AlphaItemPartDefinition
        FindObject("ArtifactPartDefinition", "GD_Artifacts.Enable1st.EnableFirst_Effect1"),
        # BetaItemPartDefinition
        None,
        # GammaItemPartDefinition
        None,
        # DeltaItemPartDefinition
        None,
        # EpsilonItemPartDefinition
        None,
        # ZetaItemPartDefinition
        None,
        # EtaItemPartDefinition
        FindObject("ArtifactPartDefinition", "GD_Aster_Artifacts.Body.Body_MysteryAmulet"),
        # ThetaItemPartDefinition
        FindObject("ArtifactPartDefinition", "GD_Aster_Artifacts.Upgrade.Upgrade_Amulet_Grade2"),
        # MaterialItemPartDefinition
        None,
        # PrefixItemNamePartDefinition
        None,
        # TitleItemNamePartDefinition
        None,
        # GameStage
        1,
        # UniqueId
        0
    )

    _willow_item = FindObject("WillowItem", "WillowGame.Default__WillowItem")
    _friendship_skill = FindObject("SkillDefinition", "GD_Aster_Artifacts.Misc.Skill_Friendship")

    def construct_object(uclass: str, outer: Optional[UObject], name: str) -> UObject:
        path = name if outer is None else f"{UObject.PathName(outer)}.{name}"
        uobject = FindObject(uclass, path)
        if uobject is None:
            uobject = ConstructObject(uclass, outer, name)
            KeepAlive(uobject)
        return uobject

    _package = construct_object("Package", None, "RoguelandsLootEnemies")
    _name_list = construct_object("NameListDefinition", _package, "NameList")
    LootBehavior = construct_object("Behavior_SpawnLootAroundPoint", _package, "LootBehavior")
    Skill = construct_object("SkillDefinition", _package, "Skill")

    def _construct_item_pool(name: str, items: Iterable[Tuple[str, Union[str, float]]]) -> UObject:
        """
        Constructs an ItemPoolDefinition with the given object paths and weights. Weights can be
        either a float representing Probability's BaseValueConstant, or a string representing
        the object path to its InitializationDefinition.
        """
        item_pool = ConstructObject("ItemPoolDefinition", LootBehavior, name)

        balanced_items = []

        for pool, weight in items:
            if type(weight) is float:
                probability = f"(BaseValueConstant={weight},BaseValueScaleConstant=1)"
            elif type(weight) is str:
                probability = f"(InitializationDefinition={weight},BaseValueScaleConstant=1)"

            balanced_item = f"(ItmPoolDefinition={pool},Probability={probability},bDropOnDeath=True)"
            balanced_items.append(balanced_item)

        _set_command(item_pool, "BalancedItems", balanced_items)

        return item_pool

    # Create a legendary weapon loot pool that mimics the vanilla legendary pool, except with no
    # pearl drops (these will come from the Tubby pearl pool).
    _legendary_pool = _construct_item_pool("LegendaryWeaponPool", (
        ( "GD_Itempools.WeaponPools.Pool_Weapons_Pistols_06_Legendary",       100.0 ),
        ( "GD_Itempools.WeaponPools.Pool_Weapons_AssaultRifles_06_Legendary",  80.0 ),
        ( "GD_Itempools.WeaponPools.Pool_Weapons_SMG_06_Legendary",            80.0 ),
        ( "GD_Itempools.WeaponPools.Pool_Weapons_Shotguns_06_Legendary",       80.0 ),
        ( "GD_Itempools.WeaponPools.Pool_Weapons_SniperRifles_06_Legendary",   55.0 ),
        ( "GD_Itempools.WeaponPools.Pool_Weapons_Launchers_06_Legendary",      20.0 ),
    ))

    # Create a legendary shield loot pool identical to the vanilla one, except with the omission
    # of the roid shield pool, since it only drops non-unique Bandit shields.
    _shield_pool = _construct_item_pool("LegendaryShieldPool", (
        ( "GD_Itempools.ShieldPools.Pool_Shields_Standard_06_Legendary",         1.0 ),
        ( "GD_Itempools.ShieldPools.Pool_Shields_NovaShields_All_06_Legendary",  1.0 ),
        ( "GD_Itempools.ShieldPools.Pool_Shields_SpikeShields_All_06_Legendary", 1.0 ),
        ( "GD_Itempools.ShieldPools.Pool_Shields_Juggernaut_06_Legendary",       1.0 ),
        ( "GD_Itempools.ShieldPools.Pool_Shields_Booster_06_Legendary",          1.0 ),
        ( "GD_Itempools.ShieldPools.Pool_Shields_Absorption_06_Legendary",       1.0 ),
        ( "GD_Itempools.ShieldPools.Pool_Shields_Impact_06_Legendary",           1.0 ),
        ( "GD_Itempools.ShieldPools.Pool_Shields_Chimera_06_Legendary",          1.0 ),
    ))

    # THe name of the initialization definition object which is used to scale Tubby pearl drop
    # weight based on item level. This maxes out at 0.2 at level 80.
    pearl_weight = "GD_Lobelia_Itempools.Weighting.Weight_Lobelia_Pearlescent_Tubbies"

    # Create the standard item pool from which each Giant's item drop will be selected.
    _item_pool = _construct_item_pool("ItemPool", (
        # ( "GD_Lobelia_Itempools.WeaponPools.Pool_Lobelia_Pearlescent_Weapons_All", pearl_weight ),
        # The weights of the pools that aren't the Tubby loot pool should add up to 0.2, such
        # that the odds of a Pearl max out at 50% at level 80.
        ( UObject.PathName(_legendary_pool),                              0.080 ),
        ( UObject.PathName(_shield_pool),                                 0.030 ),
        ( "GD_Itempools.GrenadeModPools.Pool_GrenadeMods_06_Legendary",   0.030 ),
        # The Tubby class mod pool should be 3x the weight of the main game class mod pool, such
        # that every legendary class mod has an equal chance of dropping.
        ( "GD_Lobelia_Itempools.ClassModPools.Pool_ClassMod_Lobelia_All", 0.045 ),
        ( "GD_Itempools.ClassModPools.Pool_ClassMod_06_Legendary",        0.015 ),
    ))

    # Retrieve the green items loot pool to serve as the base for our PreLegendaryPool object.
    uncommon_pool = FindObject("ItemPoolDefinition", "GD_Itempools.EnemyDropPools.Pool_GunsAndGear_02_Uncommon")

    # Set our loot behavior to spawn one instance of the main item pool, or five instances of
    # the pre-legendary loot pool.
    _set_command(LootBehavior, "ItemPools", (
        UObject.PathName(_item_pool),
        "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar",
        "GD_Itempools.AmmoAndResourcePools.Pool_Eridium_Bar",
    ))

    _set_command(Skill, "SkillEffectDefinitions", (
        "(AttributeToModify=D_Attributes.DamageTypeModifers.NormalImpactDamageModifier,           EffectTarget=TARGET_Self,BaseModifierValue=(BaseValueConstant=-1.000000))",
        "(AttributeToModify=D_Attributes.DamageTypeModifers.ExplosiveImpactDamageModifier,        EffectTarget=TARGET_Self,BaseModifierValue=(BaseValueConstant=-1.000000))",
        "(AttributeToModify=D_Attributes.DamageTypeModifers.AmpImpactDamageModifier,              EffectTarget=TARGET_Self,BaseModifierValue=(BaseValueConstant=-1.000000))",
        "(AttributeToModify=D_Attributes.DamageTypeModifers.CorrosiveImpactDamageModifier,        EffectTarget=TARGET_Self,BaseModifierValue=(BaseValueConstant=-1.000000))",
        "(AttributeToModify=D_Attributes.DamageTypeModifers.CorrosiveStatusEffectDamageModifier,  EffectTarget=TARGET_Self,BaseModifierValue=(BaseValueConstant=-1.000000))",
        "(AttributeToModify=D_Attributes.DamageTypeModifers.IncendiaryImpactDamageModifier,       EffectTarget=TARGET_Self,BaseModifierValue=(BaseValueConstant=-1.000000))",
        "(AttributeToModify=D_Attributes.DamageTypeModifers.IncendiaryStatusEffectDamageModifier, EffectTarget=TARGET_Self,BaseModifierValue=(BaseValueConstant=-1.000000))",
        "(AttributeToModify=D_Attributes.DamageTypeModifers.ShockImpactDamageModifier,            EffectTarget=TARGET_Self,BaseModifierValue=(BaseValueConstant=-1.000000))",
        "(AttributeToModify=D_Attributes.DamageTypeModifers.ShockStatusEffectDamageModifier,      EffectTarget=TARGET_Self,BaseModifierValue=(BaseValueConstant=-1.000000))",
    ))

    # Register our hooks.
    RunHook( "WillowGame.WillowAIPawn.PostBeginPlay",                                   "RoguelandsLootEnemies", _aipawn_post_begin_play       )
    RunHook( "WillowGame.PopulationFactoryBalancedAIPawn.SetupBalancedPopulationActor", "RoguelandsLootEnemies", _setup_balanced_population    )
    RunHook( "Engine.Pawn.ApplyBalanceDefinitionCustomizations",                        "RoguelandsLootEnemies", _apply_balance_customizations )
    RunHook( "WillowGame.WillowAIPawn.ReplicatedEvent",                                 "RoguelandsLootEnemies", _replicated_event             )
    RunHook( "WillowGame.WillowAIPawn.AILevelUp",                                       "RoguelandsLootEnemies", _ai_level_up                  )
    RunHook( "WillowGame.Behavior_Transform.ApplyBehaviorToContext",                    "RoguelandsLootEnemies", _behavior_transform           )
    RunHook( "WillowGame.WillowAIPawn.Died",                                            "RoguelandsLootEnemies", _died                         )
    RunHook( "WillowGame.SkillEffectManager.ActivateSkill",                             "RoguelandsLootEnemies", _activate_skill)

def Disable() -> None:
    def release_object(uclass: str, path: str) -> None:
        uobject = FindObject(uclass, path)
        if uobject is not None:
            uobject.ObjectFlags.A &= ~0x4000

    release_object("NameListDefinition", "RoguelandsLootEnemies.NameList")
    release_object("Behavior_SpawnLootAroundPoint", "RoguelandsLootEnemies.LootBehavior")
    release_object("Package", "RoguelandsLootEnemies")

    # Perform the garbage collection console command to force destruction of the objects.
    GetEngine().GamePlayers[0].Actor.ConsoleCommand("obj garbage", False)

    RemoveHook( "WillowGame.WillowAIPawn.PostBeginPlay",                                   "RoguelandsLootEnemies" )
    RemoveHook( "WillowGame.PopulationFactoryBalancedAIPawn.SetupBalancedPopulationActor", "RoguelandsLootEnemies" )
    RemoveHook( "Engine.Pawn.ApplyBalanceDefinitionCustomizations",                        "RoguelandsLootEnemies" )
    RemoveHook( "WillowGame.WillowAIPawn.ReplicatedEvent",                                 "RoguelandsLootEnemies" )
    RemoveHook( "WillowGame.WillowAIPawn.AILevelUp",                                       "RoguelandsLootEnemies" )
    RemoveHook( "WillowGame.Behavior_Transform.ApplyBehaviorToContext",                    "RoguelandsLootEnemies" )
    RemoveHook( "WillowGame.WillowAIPawn.Died",                                            "RoguelandsLootEnemies" )
    RemoveHook( "WillowGame.WillowGameViewportClient.Tick", "RoguelandsLootEnemies.RequestGiants"  )
    RemoveHook( "WillowGame.WillowGameViewportClient.Tick", "RoguelandsLootEnemies.UpdatePawns"    )
    RemoveHook( "WillowGame.WillowGameViewportClient.Tick", "RoguelandsLootEnemies.GigantizePawns" )
    RemoveHook( "WillowGame.SkillEffectManager.ActivateSkill", "RoguelandsLootEnemies")