fx = { # fx from actor to target (includes buffs)

	# fire
	'BLAZE_ATTACK.FX':'blaze',
	'FIREBALL.FX':'blaze',
	'BLAZINGBOLT_ATTACK.FX':'blazing bolt',
	'/INFERNOBOLT.FX':'blazing bolt',
	'FLARES_ATTACK.FX':'flares',
	'FIREBLAST_ATTACK.FX':'fire blast',
	'INFERNO_ATTACK.FX':'inferno',

	# ice
	'BITTERFREEZERAY.FX':'bib', # misleading name
	'BITTERICEBOLT.FX':'bfr',
	'BITTERFREEZEBOLT.FX':'bfr',
	'ICEBLAST.FX':'ice blast',
	'FREEZERAY.FX':'freeze ray',

	# psi
	'WILLDOMINATION.FX':'will dom',
	'TELEKINETICBLAST.FX':'tk blast',
	'PSIONICLANCEBLASTQUICK.FX':'psi lance',
	'SUBDUEPSIONICBLAST.FX':'subdue',
	'PSIONICBLAST_SLOWCAST.FX':'mental blast',

	# BEAMRIFLE_DISINTEGRATE
	'BEAMRIFLE_DISINTEGRATE.FX':'disintegrate',
	'BEAMRIFLE_CHARGEDSHOT.FX':'p-ray/charged',
	'BEAMRIFLE_LANCERSHOT.FX':'lancer',
	'BEAMRIFLE_PIERCINGBEAM.FX':'piercing beam',

	# dark blast
	'MOONBEAM_QUICK.FX':'moonbeam',
	'MOONBEAMWITHSKULL_QUICK.FX':'moonbeam',
	'MOOMBEAM_ATTACK.FX':'moonbeam (slow)', # mooMbeam
	'DARKNESSCONTROL/LIFEDRAIN.FX':'life drain',

	'/PETRIFYINGGAZE.FX':'petrifying gaze',
	'DARKBLAST/SOULDRAIN.FX':'soul drain',

	# sonic
	'MASSIVESONICBLAST.FX':'shout',
	'HEADSONICSCREECH.FX':'screech',
	'SONICCONTROL/BLASTS/HEROSTANDARDBLAST2.FX':'scream',

	# sonic manip
	'SONICRESONANCE/SONICCAGE.FX':'echo chamber', # could be sonic resonance cage also? cross that bridge when we get to it
	'SONICRESONANCE/BUILDUP.FX':'sound booster',

	# emp
	'HEALINGHANDS.FX':'heal other',
	'ABSORBPAIN.FX':'absorb pain',
	# 'STRENGTHHANDS2.FX':,
	'EMPATHY/RADIATIONEMISSION.FX':'healing aura',
	'MINDWALL.FX':'clear mind',
	'ENDURANCE.FX':'adreneline boost',
	'FORTITUDE.FX':'fortitude',
	'EMPATHYCUREWOUNDS.FX':'regen aura',
	'ADRENALINEFLOW.FX':'recovery aura',
	'EMPATHY/RESURECTION.FX':'resurrect',

	# pain
	'SOOTH_ATTACK.FX':'soothe',
	'SHAREPAIN_ATTACK.FX':'share pain',
	'PAINBRINGER_ATTACK.FX':'painbringer',
	'WORLDOFPAIN_ATTACK.FX':'world of pain',
	'ENFORCEDMORALE_ATTACK.FX':'enforced morale',
	'/CONDUITOFPAIN_HIT.FX':'conduit of pain', # not reversed

	# psn
	'/POISONLIQUIDPROJECTILE.FX':'envenom',
	'/PALMPOISONLIQUIDPROJECTILE.FX':'weaken',
	'ALCALOIDEHEAL.FX':'alkaloid',
	'POISONCONEGASSES.FX':'neurotoxic breath',

	# cold
	'HEATLOSSBLAST.FX':'heat loss',

	# rad
	# this is actually the onhit animation as the activation animation EVERVATINGFIELDHANDS doesnt have target info for some reason
	'ENERVATINGFIELDCONTINUING.FX': 'enervating field',

	# ill
	'ILLUSDECOY.FX':'phantom army',
	'ILLUSTERROR.FX':'spectral terror',
	'/ILLUSDECIEVE.FX':'confuse',
	'ILLUSIONCONTROL/ILLUSBLIND.FX':'blind', # attack and target? need to match up w/ MOV MOUTH

	# grav
	'/GCDISTORTION.FX':'gravity distortion',
	'/GCCRUSH_SINGULARITY.FX':'crush',
	'GCLIFT.FX':'lift',
	'/GCDIMENSIONSHIFT.FX':'dimension shift', # toggle on
	'GRAVITYCONTROL/SUBTRACTIVE/GCDISTORTIONFIELD.FX':'singularity', # could be distortion field also? but banned so doesn't matter

	# plant
	'THORNS/BUILDUP_ATTACK.FX':'toxins',
	'PLANTCONTROLHIT.FX':'strangler', # shared with plant control
	'ENTANGLEPLANTSEEDTHROW.FX':'entangle', # shared with plant control
	# 'STRANGLERROOTS.FX': 'strangler', # doesn't spawn on every strangler

	# elec
	'REJUVENATINGCIRCUITATK.FX':'rejuvenating circuit',
	'EMPOWERINGCIRCUITATK.FX':'empowering circuit',
	'INSULATINGCIRCUITATK.FX':'insulating circuit',
	'AMPUPATTACK.FX':'amp up',
	'/ENERGIZINGCIRCUITATK.FX':'energizing circuit',
	'SHOCKTHERAPY/WITCHESLIGHTNINGBOLTMEGA.FX':'shock',
	'ELECTRICITYCONTROL/WITCHESLIGHTNINGBOLTMEGA':'shocking bolt',
	'/GALVANICSENTINELSUMMON.FX':'galvanic sentinel',
	# 'ENERGYSINKCASTATTACK.FX':'shock', # galvanic shock

	#nature
	'CORROSIVESAP.FX':'corrosive enzyme',
	'WILDBASTION.FX':'wild bastion', # share with plant
	'OVERGROWTH.FX':'overgrowth',
	'WILD_GROWTH.FX':'wild growth',
	'/REGROWTH2.FX':'regrowth',

	# therm
	'THERMALRADIATION/PROTECTHOLDS.FX':'thaw',
	'THERMALRADIATION/BUFFDAMAGE.FX':'forge',
	'THERMALRADIATION/PBAOE.FX':'warmth',
	'THERMALRADIATION/HEAL/FIREHEALSELFWITHHANDS.FX':'cauterize',
	'THERMALRADIATION/FIREHEALSELFWITHHANDS.FX':'cauterize',
	'THERMALRADIATION/MELTARMORCAST.FX':'melt armor',
	# no direct heat exhaustion fx?


	# trick arrow
	'/ARROW_NET.FX':'entangling arrow',
	'/ARROW_STICKY.FX':'glue arrow',
	'/ARROW_ACID.FX':'acid arrow',

	# warshade
	'NICTUSQUICKBLAST.FX':'shadow blast',
	'KHELDIAN_WARSHADE/XRAYBEAM/XRAYBEAM.FX':'ebon eye',
	'KHELDIAN_WARSHADE/ANIMATEFOE/ANIMATEFOE.FX':'dark extraction',
	'KHELDIAN_WARSHADE/MELEELIFEDRAIN/MELEELIFEDRAIN.FX':'essence drain',

	# pb
	'PEACEHEALSELFHANDS.FX':'glowing touch',
	'/PEACEHEALSELF.FX':'reform essence',
	'ENERGYDRONES/PEACEDRONEHANDS3.FX':'photon seekers',
	'KHELDIAN_PEACEBRINGER/DAMAGEBUIDUP/DAMAGEBUIDUP.FX':'inner light',
	'PEACEQUICKBLAST/PEACEAOEBLAST.FX':'luminous blast',
	'PEACEBRINGER/XRAYBEAM/XRAYBEAM.FX':'glinting eye',
	'/HEAVYPEACEPUNCH.FX':'incandescent strike',

	# epics
	'/COMMAND2.FX':'dominate',
	'SCHOOLOFSHARKS_HIT.FX':'ssj', # not sure about this one
	'V_MAKO_SPIRITSHARK_CIRCLE_HIT':'ssj',
	'SHOCKINGBOLT_ATTACK.FX':'shocking bolt',
	# 'SPIRTSHARKJAWS_CONDITIONAL.FX': 'ssj',
	'/HIBERNATE.FX':'hibernate',
	'/HIBERNATE_CONTINUING.FX':'hibernate',
	'/SOOT.FX':'char',
	'/BUILDUPPOWERBOOST.FX':'power boost',
	'GHOSTWIDOW/SOULSTORM.FX':'soul storm',
	'GHOSTWIDOW/DARKSOULBLAST.FX':'dark blast',
	'MU_HANDLIGHTNINGFX/REDMU_CAGEBOLTS.FX':'electric shackles',
	'CALTROPSTHROW.FX':'caltrops',

	# pools
	'JAUNT_ATTACK.FX':'jaunt',
	'SPIRITWARD.FX':'spirit ward',
	'FLIGHT/NONCOMBATFLIGHT':'mystic/flight',
	'MYSTICFLIGHT.FX':'mystic/flight',
	'/INVISPHASE_FASTCAST.FX':'phase shift',
	'PHASESHIFT_ATTACK.FX':'phase shift',
	'MEDICINE/MAID.FX':'aid other', # or aid other
	'AIDOTHER_ATTACK.FX':'aid other', # or aid other
	'/TELEPORT_ATTACK.FX':'translocation', # MOV A_\TRANSLOCATION
	'AIRSUPERIORITY_ATTACK.FX':'air superiority', # 

	# misc powerset
	'BUILDUP_ATTACK.FX':'build up',
	'FOSSILIZEHANDS.FX':'fossilize',
	'/STALAGMITESTOMP.FX':'stalagmites',

	'CLAWS/CLAWSTWIRL.FX':'focus',

	'/SHIVER.FX':'shiver',
	'/CHILLBLAINSHANDS.FX':'chilblain',

	'HAUNT_ATTACK.FX':'haunt',

	'/THUNDEROUSBLAST.FX':'thunderous blast',
	'ZAPP_QUICK.FX':'zapp',
	'LIGHTNINGBOLT.FX':'lightning bolt',
	'CHARGEDBOLTS.FX':'charged bolt',

	'/KININERTIALREDUCTIONS.FX':'ir',
	'/KINSIPHONSPEED.FX':'siphon speed',
	'/KINTRANSFERENCE.FX':'transference',

	'ENERVATINGFIELDCONTINUING.FX':'enervating field',
	'ACCELERATEMETABOLISM.FX':'accelerate metabolism',

	'/EXECUTIONERSSHOT_ATTACK.FX':'executioner shot',
	'/PIERCINGROUNDS_ATTACK.FX':'piercing rounds',
	'SUPPRESSIVEFIRE_ATTACK.FX':'suppressive fire',

	'RADIATIONCONTROL/XRAYBEAM.FX':'x-ray beam',
	'COSMICBLAST.FX':'cosmic burst',
	'PROTONBLAST_QUICK.FX':'proton blast',

	'BIOARMOR/ABLATIVE_CARAPACE.FX':'ablative carapace',
	'PSIONICMELEE/PSIBUFF.FX':'concentration',
	'ENERGYAURA/SUBTRACTIVE/BUILDUPENDURENCE.FX':'energize',
	'ENERGYAURA/SUBTRACTIVE/OVERLOAD.FX':'overload',
	'/ARMORMELTDOWN.FX':'meltdown',
	'/MOMENTOFGLORY.FX':'moment of glory',
	
	'/THUGS_UPGRADE_TOSS_2.FX':'thugs upgrade',
	'PARAMILITARY/PARAMILITARY_BOOSTEQUIP.FX':'merc upgrade',
	'NECROMACY/MINIONBOOSTHIGH.FX':'necro upgrade',
	'PLAYER_MERCENARIES_GUNFIRE_SHOTGUN.FX':'thugs slug',
	
	'/WATERJET.FX':'water jet',
	'WATERJET_FAST.FX':'water jet',
	'/DEHYDRATE.FX':'dehydrate',
	
	'POWERPUSH.FX':'power push',
	#'/SMOKEHIT.FX':'smoke',
	'MEGA.FX':'power burst',
	# 'CUSTOMANIM_MEGA.FX':'power burst', 
	'SNIPERBLAST_QUICK.FX':'sniper blast', 
	'ENERGYBLAST.FX':'energy blast', 
	'CHRONOLOGICALSELECTION_ATTACK.FX':'chronos', 

	'MARTIALARTS/FOCUSCHI.FX':'upshot/focus', # or tac arrow?
	
	# melee
	'ASSASINSPSIBLADE.FX':'assassin\'s strike', 
	'BRAWLING/ASSASSINSSTRIKE_ATTACK.FX':'assassin\'s strike', 
	'PSIBLADEGREAT.FX':'greater psi blade', 
	'STRENGTHSTREAKSKO.FX':'ko blow', # epic ko blow?
	'BRAWLING/BUILDUP_ACTIVATION.FX':'combat readiness',
	'RAWLING/CRUSHINGUPPERCUT_ATTACK.FX':'crushing uppercut',
	'SPINES/IMPALE_ATTACK.FX':'impale',
	'SPINES/THROWSPINES_ATTACK.FX':'throw spines',
	'TOTALFOCUSFAST_ATTACK.FX':'total focus',

	'/FORCEBOLT.FX':'force bolt',
	'TIMECRAWL_ATTACK.FX':'time crawl',
	'TEMPORALMENDING_ATTACK.FX':'temporal mending',


	'BOOSTRANGE_ATTACK.FX':'boost range', 
	'AIM.FX':'aim',
	'FOLLOWUPHIT4.FX':'build up', #'fiery embrace',
	'/TIDALFORCES.FX':'aim', #water
	'AIM_ACTIVATION.FX':'aim',

	# misc generic
	'ALIGNMENT_JUSTICE.FX':'call to justice',
	# 'WEAPONS/LASER_PISTOL_1.FX':'crey pistol', # using MOV count
	# '/STOLLEN_IMOBILIZER_PISTOL.FX':'crey pistol', #  'stollen'
	# 'GEASTHEKINDONESCONTINUING.FX':'geas', # can pop multiple FX continuing
	'/ALIGNMENT_FRENZY.FX':'frenzy', # or other insp?
	'/BRAWL_ATTACK.FX':'brawl',
	'FORCEOFWILL/WEAKENRESOLVE.FX':'weaken resolve',
	'SUPERSPEED/BURNOUT.FX':'burnout',

	# insps
	'/STAMINA.FX':'green',
	'/WILLPOWER.FX':'red',
	'/INTELLIGENCE.FX':'blue',
	'/STRENGTH.FX':'purple/orange',
	'/AGILITY.FX':'yellow/agility', # shares with tac arrow agility

	# temp
	'WEBGRENADETHROW.FX':'web nade',
	'/SKYRAIDERJETS.FX':'raptor pack', # num toggle ons - not time
}


resdebuff = 'DEBUFFDAMRESCONTINUING.FX'

phases = [
	'phase shift',
	'hibernate',
]
teleports = [
	'jaunt',
	'translocation',
]

evade = []
evade.extend(teleports)
evade.extend(phases)



healhit = { # not in use yet
	# emp
	'EMPATHY/HEALINGDRAINBALL.FX':'absorb pain',
	'/HEALING.FX':'heal other', # or aid other

	# elec
	'/INSULATINGCIRCUITHIT.FX':'insulating circuit',
	'/REJUVENATINGCIRCUITHIT.FX':'rejuvenating circuit',

	# pools
	'SPIRITWARD_HIT.FX':'spirit ward',
}


pmov = { # prepend with 'A_' for flying version
	'DRAW_PISTOL':'crey pistol', # aka Nullifier now
	'DRAW_SABER':'crey pistol', # aka Nullifier now
	'DRAW_WEAPONBACK':'crey pistol', # defunct now with new Nullifier
	'WALL':'ssj',
	'MOUTH':'blind',
	#'PLAYER_HITDEATH' # death anim
}


# primary attacks for determining spike instances (i.e. ignore jaunts off flares or snipe only or w/e)
primaryattacks = [
	'envenom',
	#'corrosive enzyme',
	'enervating field',
	'dominate',
	'disintegrate',
	'blaze',
	'bib',
	'lancer',
	'char',
	'p-ray/charged',
	'will dom',
]


# reduced weighting on these attacks
weightedattacks = {
	'disintegrate':-0.5,
	'char':-0.5,
	'p-ray/charged':-0.5,
}

jauntoffoneattacks= [
	'enervating field',
	'blaze',
	'bib',
]

powerdelay = {
	'strangler':0.67,
	'ssj':0.83,
	'enervating field':1.50,
	'dehydrate':0.53,
}

hittiming = { # :[delay,speed]
	# blast
	'blaze':[16/30,90],
	'blazing bolt':[22/30,450],
	'fire blast':[16/30,90],
	'bib':[17/30,84],
	'bfr':[69/30,90],
	'freeze ray':[17/30,90],
	'strangler':[16/30,1000000],
	'p-ray/charged':[29/30,60],
	'lancer':[23/30,1000000],
	'disintegrate':[29/30,1000000],
	'psi lance':[40/30,105],
	'will dom':[50/30,51],
	'tk blast':[15/30,120],
	'dehydrate':[16/30,1000000],
	'water jet':[11/30,1000000],
	

	# debuffs
	'envenom':[25/30,66],
	'enervating field':[45/30,1000000],
	'corrosive enzyme':[19/30,90],

	# epics
	'dominate':[20/30,1000000],
	'ssj':[21/30,1000000],
	'char':[23/30,51],
	'shocking bolt':[28/30,1000000],

	# heals
	'heal other':[22/30,1000000],
	'absorb pain':[37/30,1000000],
	'soothe':[22/30,1000000],
	'share pain':[37/30,1000000],
	'rejuvenating circuit':[23/30,1000000],
	'insulating circuit':[22/30,1000000],
	'aid other':[40/30,1000000],
	'alkaloid':[34/30,66],
	'cauterize':[22/30,1000000],
	'glowing touch':[25/30,1000000],

	# pools/misc
	'green':[15/30,1000000],
	'hibernate':[1/30,1000000],
	'phase shift':[16/30,1000000],
	'jaunt':[2/30,1000000],
}

hitexclude = [
	'envenom',
	'corrosive enzyme',
	'enervating field',
]
healhitexclude = [
	'insulating circuit',
	'alkaloid',
]


repeatpowers = [ # powers that do multiples of an FX on use
	'enervating field',
]

utility = [	# for filtering out not atk offense powers
	'shock',
	'entangling arrow',
	'time crawl',
	'temporal mending',
	'weaken',
	'siphon speed',
	'transference',
	# 'force bolt',
	# 'web nade',
	'glue arrow',
	'confuse',
	'smoke',
	'shiver',
	'thunderous blast',
	'heat loss',
	'singularity',
	'phantasm',
	'crey pistol',
]

utilitycount = [	# for filtering out not atk offense powers
	'adreneline boost',
	'fortitude',
	'clear mind',
	'recovery aura',
	'regeneration aura',
	'resurrect',
	
	'conduit of pain',
	'painbringer',
	'enforced morale',
	'world of pain',

	'siphon speed',
	'speed boost',
	'transference',
	'ir',

	'entangling arrow',
	'glue arrow',
	'acid arrow',
	
	'overgrowth',
	'wild growth',
	'wild bastion',
	'regrowth',

	'weaken',
	'neurotoxic breath',

	'galvanic sentinel',
	'shock',
	'energizing circuit',
	'empowering circuit',
	'amp up',

	'photon seekers',
	'phantom army',
	'spectral terror',
	'dimension shift',
	'smoke',
	'shiver',

	'confuse',
	'thunderous blast',
	'heat loss',

	'web nade',
]


rez = [
'resurrect',
]


# generic FX by the actor - usage determined by target's FX
preverse = [
	# buffs
	'ENDURANCE.FX',
	'MINDWALL.FX',
	'FORTITUDE.FX',
	'THERMALRADIATION/PROTECTHOLDS.FX',
	'THERMALRADIATION/BUFFDAMAGE.FX',
	'ALCALOIDEHEAL.FX',

	#attacks - note this means misses for these powers don't get counted
	'/PLANTCONTROLHIT.FX',
	'SCHOOLOFSHARKS_HIT.FX',
	'/V_MAKO_SPIRITSHARK_CIRCLE_HIT',
	'/DEHYDRATE.FX',
	'ENERVATINGFIELDCONTINUING.FX',
	'WILDBASTION_HIT.FX',
	#'/SMOKEHIT.FX',
]


buffs = [
	'HEALINGHANDS.FX', # 0.93 delay
	'ABSORBPAIN.FX', # 1.47 delay
	'STRENGTHHANDS2.FX',
	'ENDURANCE.FX',
	'MINDWALL.FX',
	'FORTITUDE.FX',
	'REJUVENATINGCIRCUITATK.FX',
	'EMPOWERINGCIRCUITATK.FX',
	'INSULATINGCIRCUITATK.FX',
	'AMPUPATTACK.FX',
	'PAINBRINGER_ATTACK.FX',
	'WILD_GROWTH_HIT.FX',
	'WILDBASTION_HIT.FX',
	'KINSPEEDBOOSTHIT.FX',
	'THERMALRADIATION/PROTECTHOLDS.FX',
	'THERMALRADIATION/BUFFDAMAGE.FX',
	'PEACEHEALSELFHANDS.FX',
]

gatherbuffs = [
	'WILDBASTION_HIT.FX',
	'KINSPEEDBOOSTHIT.FX',
	'KININERTIALREDUCTIONSCONTINUING.FX',
]

heals = [
	'heal other',
	'absorb pain',
	'soothe',
	'share pain',
	'aid other',
	'rejuvenating circuit',
	'insulating circuit',
	'glowing touch',
	'cauterize',
	'spirit ward',
	'alkaloid',
]

absorbs = [
	# 'insulating circuit', # need to rewrite for duration
	'spirit ward'
]

cmpowers = [
	'clear mind',
	'enforced morale',
	'thaw',
	'clarity',
	'antidote',
	'id',
]


filterextras = [
	'crey pistol',
	'raptor pack',
	'mystic/flight',
	'green',
	'red',
	'blue',
	'purple/orange',
	'yellow',
	# 'clear mind',
	'healing aura',
	'power boost',
]

npc = [
	'NPC',
	'EntTypeFile',
]

ignorecostume = [ # npc costumes used by players throwing off player detection
	'FRK_45',
	'Kheldian_Peacebringer_Light_Form',
	'V_Coralax_Player_Boss',
]

# filter out non-player entities - issues if player name = one of these
# probably a better way to do this
name_filter  = [
	'Mu Guardian',
	'Phantasm',
	'Decoy Phantasm',
	'Decoy',
	'Singularity',
	'Coralax Blue Hybrid',
	'Dr',
	'Poison Trap',
	'Animated Stone',
	'Victory Rush',
	'Bruiser',
	'Blind',
	'Galvanic Sentinel',
	'Voltaic Geyser',
	'Voltaic Sentinel',
	'Power Disruptor',
	'Protected Area',
	'Rain of Fire',
	'Water Spout',
	'Fortunata Mistress',
	'Superior Vigilant Assault',
	'Superior Scourging Blast',
	'Superior Defenders Bastion',
	'German Shepherd',
	'Ice Storm',
	'Energy Font',
	'Spectral Terror',
	'Coralax Red Hybrid',
	'Faraday Cage',
	'Architect Entertainment Instructor',
	'Architect Contact',
	'Spirit Panther',
	'Ticket Vendor',
	'Architect Entertainment Greeter',
	'Howler Wolf',
	'Alpha Howler Wolf',
	'Dire Wolf',
	'Lioness',
	'Burst of Speed',
]

otherfx = { # like toggles and stuff for determining powersets
	'THORNS_ACTIVATION.FX':'thorns',
	'/REACTIONTIME.FX':'reaction time',
	'ENERVATINGFIELDHAND.FX':'ef toggle on',
	'WILDFORTRESS.FX':'wild fortress',
	# 'AGILITY.FX':'agility',
}

powersets = {
	'bib':'ice',
	'blaze':'fire',
	'blazing bolt':'fire',
	'lancer':'beam',
	'disintegrate':'beam',
	'p-ray/charged':'beam',
	'will dom':'psi',
	'psi lance':'psi',
	'soul drain':'dark blast',
	'water jet':'water',
	'tidal forces':'water',
	'thunderous blast':'elec blast',
	'shout':'sonic blast',
	'screech':'sonic blast',
	'lightning bolt':'elec blast',
	'executioner shot':'dual pistol',
	'suppressive fire':'dual pistol',
	'water jet':'water',
	'tidal forces':'water',
	'power push':'energy blast',
	'power burst':'energy blast',
	
	'heal other':'emp',
	'absorb pain':'emp',
	'soothe':'pain',
	'share pain':'pain',
	'insulating circuit':'elec aff',
	'amp up':'elec aff',
	'shock':'elec aff',
	'forge':'therm',
	'cauterize':'therm',
	
	'envenom':'poison',
	'weaken':'poison',
	'corrosive enzyme':'nature',
	'overgrowth':'nature',
	'wild growth':'nature',
	'force bolt':'bubble',
	
	'thorns':'plant',
	'toxins':'plant',
	'wild fortress':'plant',
	'upshot/focus':'tac',
	'reaction time':'martial',
	'boost range':'energy manip',
	'chronos':'temporal',
	'echo chamber':'sonic manip',

	'cosmic burst':'rad blast',

	'ir':'kin',
	'siphon speed':'kin',
	'accelerate metabolism':'rad',
	'ef toggle on':'rad',
	'time crawl':'time',
	'temporal mending':'time',
	'entangling arrow':'trick',
	'heat loss':'cold',

	'phantom army':'ill',
	'phantasm':'ill',
	'dimension shift':'grav',
	'singularity':'grav',
	'lift':'grav',
	'fossilize':'earth',
	'chilblain':'ice ctrl',
	'shiver':'ice ctrl',
	'smoke':'fire ctrl',
	'haunt':'dark ctrl',

	'thugs upgrade':'thugs',
	'thugs slug':'thugs',
	'merc upgrade':'merc',
	'necro upgrade':'necro',


	'luminous blast':'peacebringer',
	'incandescent strike':'peacebringer',
	'shadow blast':'warshade',
	'ebon eye':'warshade',

	#melee
	'greater psi blade':'psi melee',
	'crushing uppercut':'street justice',
	'total focus':'energy melee', # maybe an issue with the power pool total focus
	'impale':'spines',
	'focus':'claws',

	# armor
	'ablative carapace':'bio',
	'energize':'energy aura',
	'overload':'energy aura',
	'meltdown':'rad armor',
	'moment of glory':'regen',
}

primarysupport = [
	'emp',
	'pain',
	'elec aff',
	'therm',
]
primaryoffence = [ 
	'poison',
	'fire',
	'ice',
	'beam',
	'psi',
	'water',
	'energy blast',
	'dual pistol',
	'sonic blast',
	'elec blast',
	'rad blast',
	'water',
	'thugs',
	'merc',
	'necro',
	'claws',
	'psi melee',
	'energy melee',
	'street justice',
	'spines',
]



at_blastsets = [
	'ice',
	'fire',
	'beam',
	'water',
	'dark',
	'rad blast',
	'energy blast',
	'psi',
	'dual pistol',
	'sonic blast',
	'elec blast',
]

at_mezsets = [
	'ice ctrl',
	'fire ctrl',
	'dark ctrl',
	'grav',
	'ill',
	'mind',
	'earth',
]

at_mm = [
	'thugs',
	'merc',
	'necro',
]

at_blastsecondaries = [
	'tac',
	'plant',
	'martial',
	'energy manip',
	'sonic manip',
	'temporal',
]

at_meleesets = [
	'claws',
	'psi melee',
	'energy melee',
	'street justice',
	'spines',
]

at_defsets = [
	'kin',
	'rad',
	'time',
	'trick',
	'cold',
	'elec aff',
	'emp',
	'therm',
	'pain',
	'poison',
	'nature',
	'bubble',
]
