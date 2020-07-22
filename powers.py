pdict = {

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
'SOOTH_ATTACK.FX':'heal other',
'SHAREPAIN_ATTACK.FX':'absorb pain',

# psn
'/POISONLIQUIDPROJECTILE.FX':'envenom',
'/PALMPOISONLIQUIDPROJECTILE.FX':'weaken',


# ill
'ILLUSDECOY.FX':'phantom army',
'ILLUSIONCONTROL/ILLUSBLIND.FX':'blind', # attack and target?

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
'MENTALPOWERS/COMMAND2.FX':'dominate',
'MINDCONTROL/COMMAND2.FX':'dominate',
'SPIRTSHARKJAWS_CONDITIONAL.FX':'ssj',
'/SCHOOLOFSHARKS_HIT.FX':'ssj',
'V_MAKO_SPIRITSHARK_CIRCLE_HIT':'ssj',
'/HIBERNATE.FX':'hibernate',
'/HIBERNATE_CONTINUING.FX':'hibernate',
'FIRECONTROL/SOOT.FX':'char',
'/EMBERSHITSOOTANDCINDERS.FX':'char', #??

# pools
'JAUNT_ATTACK.FX':'jaunt',
'SPIRITWARD.FX':'spirit ward',
'FLIGHT/NONCOMBATFLIGHT':'mystic/flight',
'MYSTICFLIGHT.FX':'mystic/flight',
'/INVISPHASE_FASTCAST.FX':'phase shift',
'PHASESHIFT_ATTACK.FX':'phase shift',
'MEDICINE/MAID.FX':'aid other',

# misc
'ALIGNMENT_JUSTICE.FX':'call to justice',
'AIM.FX':'aim',
# 'FOLLOWUPHIT4.FX':'fiery embrace',
'FOLLOWUPHIT4.FX':'build up',
'AIM_ACTIVATION.FX':'aim',
'FOSSILIZEHANDS.FX':'fossilize',
'WEAPONS/LASER_PISTOL_1.FX':'crey pistol',
'/THUNDEROUSBLAST.FX':'thunderous blast',
'/STAMINA.FX':'respite', # or other insp?
'GEASTHEKINDONESCONTINUING.FX':'geas',


# temp
'WEBGRENADETHROW.FX':'web nade',
'/SKYRAIDERJETS.FX':'raptor pack', # num toggle ons - not time

}




pmov = { # prepend with 'A_' for flighing version 
'DRAW_PISTOL':'crey pistol',
'WALL':'ssj',
'MOUTH':'blind',
]






preverse = [
# buffs
'ENDURANCE.FX',
'MINDWALL.FX',
'FORTITUDE.FX',

#attacks
'PLANTCONTROL/PLANTCONTROLHIT.FX',
'SPIRTSHARKJAWS_CONDITIONAL.FX',
'/SCHOOLOFSHARKS_HIT.FX',
'V_MAKO_SPIRITSHARK_CIRCLE_HIT',
'/EMBERSHITSOOTANDCINDERS.FX',
]

pemp = [
'HEALINGHANDS.FX',
'ABSORBPAIN.FX',
'STRENGTHHANDS2.FX',
]

pattack = [ # discern between atk and receive w/ same indicator
'ILLUSIONCONTROL/ILLUSBLIND.FX', # attack and target?'
]

# filter out non-player entities - issues if player name = one of these
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
]