# in seconds
targetwindow = 2   # time window for min attacks to count a spike
evadewindow = 2*targetwindow   # time window for min attacks to count a spike
earlyevadecount = 3
earlyevadetime = 2
cleanspiketime = 0.8 # time window for a spike to be considered clean
cleanspikecount = 3 # number on target to be clean
targethealwindow = 2.5	 # depends on the type of offense (blaze lead requires lower than beam)
targethealatks = 3	 # depends on the type of offense (blaze lead requires lower than beam)
targetmaxtime = 4 # MIN spike time to look for attacks
targetcooldown = 4.5 # end time of spike to check new attacks
targetminattacks = 2   # minimum atks on target to count as attack
targetminattackers = 2 # minimum ppl on target to count as attack
predictspiketime = 10 # time before someone gets spiked where they can receive an absorb and have it count as a heal, e.g. spirit warding someone you expect to be the next target
matchtime = 600
t_bundle_step = 60
phasedelay = 0.4 # delay after activation when unaffecting (estimate, same value for hibe and phase)
phasemax = 4 #
paintedtimer = 16 # ~how long after a debuff indicator it's still valid, not sure when the second pops up?
extras_start = 5

map_aliases = {
	'Arena_OutbreakRuin_01.txt':'outbreak',
	'Arena_Founders_01.txt':'liberty',
	'Arena_Praetoria_01.txt':'last bastion', #aka ruined eden
	'Arena_Industrial_01.txt':'factory',
	'Arena_Industrial_02.txt':'industrial',
	'Arena_Outdoor_01.txt':'council earth',
	'Arena_Outdoor_02.txt':'luna square',
}