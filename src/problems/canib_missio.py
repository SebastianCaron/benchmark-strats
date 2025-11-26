from collections import defaultdict
import time


MAX_M = 30
MAX_C = 30
CAP_BOAT = 20
CNST = None

class Direction:
	OLD_TO_NEW = 1
	NEW_TO_OLD = 0


class CONST:
	def __init__(self, MAX_M, MAX_C, CAP_BOAT, MAX_TIME_S, MAX_NODES):
		self.MAX_M = MAX_M
		self.MAX_C = MAX_C
		self.CAP_BOAT = CAP_BOAT

		self.MAX_TIME = MAX_TIME_S
		self.MAX_NODES = MAX_NODES

# TERMINAL_STATE = State(-1, -1, Direction.NEW_TO_OLD, -1, -1, 0)
# INITIAL_STATE = None
# #	State(MAX_M, MAX_C, Direction.OLD_TO_NEW, 0, 0,0)




class State(object):

	def __init__(self, missionaries, cannibals, dir, missionariesPassed, cannibalsPassed, level, CONSTS,moves):
		self.missionaries = missionaries
		self.cannibals = cannibals
		self.dir = dir
		self.action = ""
		self.level = level
		self.missionariesPassed = missionariesPassed
		self.cannibalsPassed = cannibalsPassed
		self.CONSTANTS = CONSTS

		self.moves = moves

		global MAX_M
		global MAX_C
		global CAP_BOAT
		global CNST

		if not CONSTS is None:
			CNST = CONSTS

			MAX_M = CONSTS.MAX_M
			MAX_C = CONSTS.MAX_C
			CAP_BOAT = CONSTS.CAP_BOAT

	# pass True to count forward
	def successors(self):
		listChild = []
		if not self.isValid() or self.isGoalState():
			return listChild
		if self.dir == Direction.OLD_TO_NEW:
			sgn = -1
			direction = "from the original shore to the new shore"
		else:
			sgn = 1
			direction = "back from the new shore to the original shore"
		for i in self.moves:
			(m, c) = i
			self.addValidSuccessors(listChild, m, c, sgn, direction)
		return listChild

	def addValidSuccessors(self, listChild, m, c, sgn, direction):
		newState = State(self.missionaries + sgn * m, self.cannibals + sgn * c, self.dir + sgn * 1,
							self.missionariesPassed - sgn * m, self.cannibalsPassed - sgn * c, self.level + 1,
							self.CONSTANTS,self.moves)
		if newState.isValid():
			newState.action = " take %d missionaries and %d cannibals %s." % (m, c, direction)
			listChild.append(newState)

	def isValid(self):
		# obvious
		if self.missionaries < 0 or self.cannibals < 0 or self.missionaries > MAX_M or self.cannibals > MAX_C or (
				self.dir != 0 and self.dir != 1):
			return False

		# then check whether missionaries outnumbered by cannibals in any shore
		if (self.cannibals > self.missionaries > 0) or (
				self.cannibalsPassed > self.missionariesPassed > 0):  # more cannibals then missionaries on original shore
			return False

		return True

	def isGoalState(self):
		return self.cannibals == 0 and self.missionaries == 0 and self.dir == Direction.NEW_TO_OLD

	def __repr__(self):
		return "\n%s\n\n< @Depth:%d State (%d, %d, %d, %d, %d) >" % (
			self.action, self.level, self.missionaries, self.cannibals, self.dir, self.missionariesPassed,
			self.cannibalsPassed)

	def __eq__(self, other):
		return self.missionaries == other.missionaries and self.cannibals == other.cannibals and self.dir == other.dir

	def __hash__(self):
		return hash((self.missionaries, self.cannibals, self.dir))

	def __ne__(self, other):
		return not (self == other)


TERMINAL_STATE = State(-1, -1, Direction.NEW_TO_OLD, -1, -1, 0, CNST,None)
# INITIAL_STATE = State(MAX_M, MAX_C, Direction.OLD_TO_NEW, 0, 0, 0, CNST)



class Graph:

	def __init__(self):

		self.bfs_parent = {}
		self.dfs_parent = {}

		self.expandedBFS = 0
		self.expandedDFS = 0

	def BFS(self, s):
		self.expandedBFS = 0
		self.bfs_parent[s] = None
		visited = {(s.missionaries, s.cannibals, s.dir): True}
		s.level = 0

		start_time = time.time()
		queue = [s]
		while queue:
			self.expandedBFS += 1

			u = queue.pop(0)

			if u.isGoalState():
				queue.clear()
				self.bfs_parent[TERMINAL_STATE] = u
				return True, self.expandedBFS

			# Stops searching after a certain time/node limit 
			t = time.time() - start_time
			if t > u.CONSTANTS.MAX_TIME or self.expandedBFS > u.CONSTANTS.MAX_NODES:
				if t > u.CONSTANTS.MAX_TIME:
					print("%.2fs EXCEEDED TIME LIMIT of %.2fs" % (t, u.CONSTANTS.MAX_TIME))
				else:
					print("EXCEEDED NODE LIMIT of %d" % u.CONSTANTS.MAX_NODES)
				queue.clear()
				return False, self.expandedBFS

			for v in reversed(u.successors()):
				if (v.missionaries, v.cannibals, v.dir) not in visited.keys():
					self.bfs_parent[v] = u
					v.level = u.level + 1
					queue.append(v)
					visited[(v.missionaries, v.cannibals, v.dir)] = True

		return False, self.expandedBFS

	def DFS(self, s):
		self.expandedDFS = 0
		self.dfs_parent[s] = None
		visited = {(s.missionaries, s.cannibals, s.dir): True}

		start_time = time.time()
		stack = [s]
		while stack:
			u = stack.pop()
			self.expandedDFS += 1

			if u.isGoalState():
				self.dfs_parent[TERMINAL_STATE] = u
				stack.clear()
				return True, self.expandedDFS

			t = time.time() - start_time
			# Stops searching after a certain time/node limit 
			if t > u.CONSTANTS.MAX_TIME or self.expandedDFS > u.CONSTANTS.MAX_NODES:
				if t > u.CONSTANTS.MAX_TIME:
					print("%.2fs EXCEEDED TIME LIMIT of %.2fs" % (t, u.CONSTANTS.MAX_TIME))
				else:
					print("EXCEEDED NODE LIMIT of %d" % u.CONSTANTS.MAX_NODES)
				stack.clear()
				return False, self.expandedDFS

			for v in u.successors():
				if (v.missionaries, v.cannibals, v.dir) not in visited.keys():
					visited[(v.missionaries, v.cannibals, v.dir)] = True
					self.dfs_parent[v] = u
					stack.append(v)
		return False, self.expandedDFS
