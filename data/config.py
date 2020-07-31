# in seconds
targetwindow = 4   # time window for min attacks to count a spike
cleanspike = 0.5 # time window for a spike to be considered clean
targetcooldown = 8 # time after spike started to ignore new attacks as a spike
targetminattacks = 3   # minimum atks on target to count as attack
targetminattackers = 2 # minimum ppl on target to count as attack
predictspiketime = 10 # time before someone gets spiked where they can receive an absorb and have it count as a heal, e.g. spirit warding someone you expect to be the next target
# getting good numbers comparing to vods with these values
