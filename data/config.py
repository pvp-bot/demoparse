# in seconds
targetwindow = 2   # time window for min attacks to count a spike
earlyevadecount = 3
earlyevadetime = 2
targethealwindow = 2	 # depends on the type of offense (blaze lead requires lower than beam)
targethealwindowdmg = 1	 # depends on the type of offense (blaze lead requires lower than beam)
targethealatks = 3	 # depends on the type of offense (blaze lead requires lower than beam)
targetmaxtime = 4 # MIN spike time to look for attacks
targetcooldown = 4 # end time of spike to check new attacks
targetminattacks = 2   # minimum atks on target to count as attack
targetminattackers = 2 # minimum ppl on target to count as attack
predictspiketime = 12 # time before someone gets spiked where they can receive an absorb and have it count as a heal, e.g. spirit warding someone you expect to be the next target
matchtime = 600 # time in seconds (10 min)
t_bundle_step = 30
phasedelay = 0.63 # delay after activation when unaffecting (max delay for phase, using same value hibe for this)
phasemax = 4 # window after phase where heals on target don't count
paintedtimer = 16 # ~how long after a (psn) debuff indicator it's still valid, not sure when the second pops up?
extras_start = 4
repeat_reset = 4 # how long to ignore duplicate of repeating power (i.e. enervating field)
posdelay = 1 # how long in s to delay position coords for distance calcs (due to server lag)

map_aliases = {
	'Arena_OutbreakRuin_01.txt':'outbreak',
	'Arena_Founders_01.txt':'liberty town',
	'Arena_Praetoria_01.txt':'last bastion', # aka ruined eden
	'Arena_Industrial_01.txt':'factory',
	'Arena_Industrial_02.txt':'industrial (new)',
	'Arena_Outdoor_01.txt':'council earth',
	'Arena_Outdoor_02.txt':'luna square',
}