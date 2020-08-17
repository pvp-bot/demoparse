# not in use yet
class Target:
	def __init__(self, start, target, team):
		self.firstatk = start # match time of first attack
		self.firsthit = 0
		self.firstheal = 0
		self.endspike = 0
		self.targettime = 0 #total time being targeted

		self.target = target # player being targeted
		self.team = team # team being targeted
		self.death = 0 # 1 if dead
		
		self.attacks = 0 # how many attacks thrown
		self.attackers = [] # list of attackers
		self.heals = 0 # number of heals/absorbs received
		self.healers = [] # list of support casting on target
		self.greens = 0 # list of support casting on target
		
		self.phasetime = 0 # time into spike when phase hit
		self.atksbeforephase = 0 # number of atks cast before phase/hiber animated

		self.jaunttime = 0 # time into spike when jaunt hit
		self.atksbeforejaunt = 0 # number of atks cast before jaunt animated

