# in seconds
targetwindow = 2   # time window for min attacks to count a spike
evadewindow = 2*targetwindow   # time window for min attacks to count a spike
earlyevadecount = 3
earlyevadetime = 2
cleanspiketime = 0.8 # time window for a spike to be considered clean
cleanspikecount = 3 # number on target to be clean
targethealwindow = 2.8 # depends on the type of offense (blaze lead requires lower than beam)
targetmaxtime = 6 # MIN spike time
targetcooldown = 3.5 # max spike time
targetminattacks = 2   # minimum atks on target to count as attack
targetminattackers = 2 # minimum ppl on target to count as attack
predictspiketime = 10 # time before someone gets spiked where they can receive an absorb and have it count as a heal, e.g. spirit warding someone you expect to be the next target
matchtime = 600
t_bundle_step = 60
phasedelay = 0.5
paintedtimer = 16 # ~how long after a debuff indicator it's still valid, not sure when the second pops up?
extras_start = 5