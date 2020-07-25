atk = { # fx from actor to target (includes buffs)

	# fire
	'BLAZE_ATTACK.FX':'blaze',
	'FIREBALL.FX':'blaze',
	'BLAZINGBOLT_ATTACK.FX':'blazing bolt',
	'/INFERNOBOLT.FX':'blazing bolt',

	# ice
	'BITTERFREEZERAY.FX':'bib',
	'BITTERICEBOLT.FX':'bfr',
	'BITTERFREEZEBOLT.FX':'bfr',
	'ICEBLAST.FX':'ice blast',
	'FREEZERAY.FX':'freeze ray',

	# BEAMRIFLE_DISINTEGRATE
	'BEAMRIFLE_DISINTEGRATE.FX':'disintegrate',
	'BEAMRIFLE_CHARGEDSHOT.FX':'penetrating ray/charged shot',
	'BEAMRIFLE_LANCERSHOT.FX':'lancer',

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

	# pain
	# 'SOOTH_ATTACK.FX':'soothe',
	# 'SHAREPAIN_ATTACK.FX':'share pain',
	'SOOTH_ATTACK.FX':'heal other', # same thing
	'SHAREPAIN_ATTACK.FX':'absorb pain',

	# psn
	'/POISONLIQUIDPROJECTILE.FX':'envenom',
	'/PALMPOISONLIQUIDPROJECTILE.FX':'weaken',


	# ill
	'ILLUSDECOY.FX':'phantom army',
	'ILLUSIONCONTROL/ILLUSBLIND.FX':'blind', # attack and target? need to match up w/ MOV MOUTH

	# plant
	'THORNS/BUILDUP_ATTACK.FX':'toxins',
	'THORNS/BUILDUP_ATTACK.FX':'build up',
	'PLANTCONTROL/PLANTCONTROLHIT.FX':'strangler',

	# elec
	'REJUVENATINGCIRCUITATK.FX':'rejuvenating circuit',
	'EMPOWERINGCIRCUITATK.FX':'empowering circuit',
	'INSULATINGCIRCUITATK.FX':'insulating circuit',
	'AMPUPATTACK.FX':'amp up',
	'WITCHESLIGHTNINGBOLTMEGA.FX':'shock',#?
	'ENERGYSINKCASTATTACK.FX':'shock',

	#nature
	'CORROSIVESAP.FX':'corrosive enzyme',

	# epics
	'/COMMAND2.FX':'dominate',
	'/SCHOOLOFSHARKS_HIT.FX':'ssj',
	'V_MAKO_SPIRITSHARK_CIRCLE_HIT':'ssj',
	'/HIBERNATE.FX':'hibernate',
	'/HIBERNATE_CONTINUING.FX':'hibernate',
	'FIRECONTROL/SOOT.FX':'char',
	# '/EMBERSHITSOOTANDCINDERS.FX':'char', # hit?

	# pools
	'JAUNT_ATTACK.FX':'jaunt',
	'SPIRITWARD.FX':'spirit ward',
	'FLIGHT/NONCOMBATFLIGHT':'mystic/flight',
	'MYSTICFLIGHT.FX':'mystic/flight',
	'/INVISPHASE_FASTCAST.FX':'phase shift',
	'PHASESHIFT_ATTACK.FX':'phase shift',
	'MEDICINE/MAID.FX':'aid other',

	# misc powerset
	'FOSSILIZEHANDS.FX':'fossilize',
	'AIM.FX':'aim',
	'FOLLOWUPHIT4.FX':'build up', #'fiery embrace',
	'AIM_ACTIVATION.FX':'aim',
	'/THUNDEROUSBLAST.FX':'thunderous blast',


	# misc generic
	'ALIGNMENT_JUSTICE.FX':'call to justice',
	# 'WEAPONS/LASER_PISTOL_1.FX':'crey pistol', # using MOV count
	'GEASTHEKINDONESCONTINUING.FX':'geas',
	'/STAMINA.FX':'respite', # or other insp?


	# temp
	'WEBGRENADETHROW.FX':'web nade',
	'/SKYRAIDERJETS.FX':'raptor pack', # num toggle ons - not time
}


hit = { # fx on target from actor (includes buffs)


# nature
'CORROSIVESAP_HIT.FX':'corrosive enzyme',

# fire
'BLAZE_HIT.FX':'blaze',
'FIREBALLHITNO_RING.FX':'blaze',
'BLAZINGBOLT_HIT.FX':'blazing bolt',

# ice
'ICEBOLTHIT.FX':'bfr',

# plant
'PLANTCONTROLHIT.FX':'strangler',

# poison
'POISONHITQUICK.FX':'envenom', # or weaken

# elec
'INSULATINGCIRCUITHIT.FX':'insulating circuit',
'DNASIPHON_HIT.FX':'shock', #?

# epics
'MINDCONTROLHIT.FX':'dominate',
'CINDERSHIT.FX':'char',
'EMBERSHITSOOTANDCINDERS.FX':'char',
'SCHOOLOFSHARKS_HIT.FX':'ssj',
'V_MAKO_SPIRITSHARK_CIRCLE_HIT.FX':'ssj',

# pools
'SPIRITWARD_HIT.FX':'spirit ward',
}



pmov = { # prepend with 'A_' for flying version 
'DRAW_PISTOL':'crey pistol',
'WALL':'ssj',
'MOUTH':'blind',
#'PLAYER_HITDEATH' # death anim
}




# generic FX by the actor - usage determined by target's FX
preverse = [
# buffs
'ENDURANCE.FX',
'MINDWALL.FX',
'FORTITUDE.FX',

#attacks - note this means misses for these powers don't get counted
'PLANTCONTROL/PLANTCONTROLHIT.FX',
'/SCHOOLOFSHARKS_HIT.FX',
'V_MAKO_SPIRITSHARK_CIRCLE_HIT',
]

buffs = [
'HEALINGHANDS.FX',
'ABSORBPAIN.FX',
'STRENGTHHANDS2.FX',
'ENDURANCE.FX',
'MINDWALL.FX',
'FORTITUDE.FX',
'REJUVENATINGCIRCUITATK.FX',
'EMPOWERINGCIRCUITATK.FX',
'INSULATINGCIRCUITATK.FX',
'AMPUPATTACK.FX',
]

# common attacks - unused for anything atm
atks = [
'BLAZE_ATTACK.FX',
'FIREBALL.FX',
'BLAZINGBOLT_ATTACK.FX',
'/INFERNOBOLT.FX',
'BITTERFREEZERAY.FX',
'BITTERICEBOLT.FX',
'BITTERFREEZEBOLT.FX',
'ICEBLAST.FX',
'FREEZERAY.FX',
'BEAMRIFLE_DISINTEGRATE.FX',
'BEAMRIFLE_CHARGEDSHOT.FX',
'BEAMRIFLE_LANCERSHOT.FX',
'/COMMAND2.FX',
]


npc = [
'NPC',
'EntTypeFile',
]

# filter out non-player entities - issues if player name = one of these
# probably a better way to do this
name_filter  = [
'Mu Guardian',
'Phantasm',
'Decoy Phantasm',
'Decoy',
'Coralax Blue Hybrid',
'Dr',
'Poison Trap',
'Animated Stone',
'Superior Vigilant Assault',
'Blind',
'Galvanic Sentinel',
'Voltaic Geyser',
'Voltaic Sentinel',
'Water Spout',
'Fortunata Mistress',
'Superior Scourging Blast',
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
]