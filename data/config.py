# in seconds
targetwindow = 2   # time window for min attacks to count a spike
cleanspiketime = 0.8 # time window for a spike to be considered clean
cleanspikecount = 3 # number on target to be clean
targethealwindow = 2.8 # depends on the type of offense (blaze lead requires lower than beam)
targetcooldown = 8 # max spike time
targetminattacks = 2   # minimum atks on target to count as attack
targetminattackers = 2 # minimum ppl on target to count as attack
predictspiketime = 8 # time before someone gets spiked where they can receive an absorb and have it count as a heal, e.g. spirit warding someone you expect to be the next target
matchtime = 600 # 2 sec buff