from collections import defaultdict
import heapq

MAX_M = 30
MAX_C = 30
CAP_BOAT = 20
CNST = None

class Direction:
	OLD_TO_NEW = 1
	NEW_TO_OLD = 0


class CONST:
	def __init__(self, MAX_M, MAX_C, CAP_BOAT, MAX_NODES):
		self.MAX_M = MAX_M
		self.MAX_C = MAX_C
		self.CAP_BOAT = CAP_BOAT
		self.MAX_NODES = MAX_NODES

# TERMINAL_STATE = State(-1, -1, Direction.NEW_TO_OLD, -1, -1, 0)
# INITIAL_STATE = None
# #	State(MAX_M, MAX_C, Direction.OLD_TO_NEW, 0, 0,0)




class State(object):

	def __init__(self, missionaries, cannibals, dir, missionariesPassed, cannibalsPassed, level, CONSTS, moves = None):
		self.missionaries = missionaries
		self.cannibals = cannibals
		self.dir = dir
		self.action = ""
		self.level = level
		self.missionariesPassed = missionariesPassed
		self.cannibalsPassed = cannibalsPassed
		self.CONSTANTS = CONSTS

		global MAX_M
		global MAX_C
		global CAP_BOAT
		global CNST

		if not CONSTS is None:
			CNST = CONSTS

			MAX_M = CONSTS.MAX_M
			MAX_C = CONSTS.MAX_C
			CAP_BOAT = CONSTS.CAP_BOAT

		if moves is None:
			self.moves = self.genPossibleMoves()
		else:
			self.moves = moves

	def key(self):
		return (self.missionaries, self.cannibals, self.dir)
		
	def genPossibleMoves(self):
		moves = []
		for m in range(CAP_BOAT + 1):
			for c in range(CAP_BOAT + 1):
				if 0 < m < c:
					continue
				if 1 <= m + c <= CAP_BOAT:
					moves.append((m, c))
		return moves

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
	def __lt__(self, other):
		return (self.missionaries, self.cannibals, self.dir) < (other.missionaries, other.cannibals, other.dir)

TERMINAL_STATE = State(-1, -1, Direction.NEW_TO_OLD, -1, -1, 0, CNST)
# INITIAL_STATE = State(MAX_M, MAX_C, Direction.OLD_TO_NEW, 0, 0, 0, CNST)



class Graph:

	def __init__(self):

		self.bfs_parent = {}
		self.dfs_parent = {}
		self.dij_parent = {}
		self.astar_parent = {}
		self.idastar_parent = {}

		self.expandedBFS = 0
		self.expandedDFS = 0
		self.expandedDIJ = 0
		self.expandedASTAR = 0
		self.expandedIDASTAR = 0

	def BFS(self, cm):
		self.expandedBFS = 0
		self.bfs_parent[cm] = None
		visited = {(cm.missionaries, cm.cannibals, cm.dir): True}
		cm.level = 0

		queue = [cm]
		while queue:
			self.expandedBFS += 1

			u = queue.pop(0)

			if u.isGoalState():
				queue.clear()
				self.bfs_parent[TERMINAL_STATE] = u
				return True, self.expandedBFS

			# Stops searching after a certain node limit 
			if self.expandedBFS > u.CONSTANTS.MAX_NODES:
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

	def DFS(self, cm):
		self.expandedDFS = 0
		self.dfs_parent[cm] = None
		visited = {(cm.missionaries, cm.cannibals, cm.dir): True}

		stack = [cm]
		while stack:
			u = stack.pop()
			self.expandedDFS += 1

			if u.isGoalState():
				self.dfs_parent[TERMINAL_STATE] = u
				stack.clear()
				return True, self.expandedDFS

			# Stops searching after a certain node limit 
			if self.expandedDFS > u.CONSTANTS.MAX_NODES:
				print("EXCEEDED NODE LIMIT of %d" % u.CONSTANTS.MAX_NODES)
				stack.clear()
				return False, self.expandedDFS

			for v in u.successors():
				if (v.missionaries, v.cannibals, v.dir) not in visited.keys():
					visited[(v.missionaries, v.cannibals, v.dir)] = True
					self.dfs_parent[v] = u
					stack.append(v)
		return False, self.expandedDFS
	
	def DIJKSTRA(self, cm):
		self.dij_parent = {cm: None}
		dist = {cm.key(): 0}
		pq = [(0, cm)]

		while pq:
			cost_u, u = heapq.heappop(pq)
			self.expandedDIJ += 1

			if u.isGoalState():
				return True, self.expandedDIJ
			for v in u.successors():
				new_cost = cost_u + 1	
				k = v.key()

				if k not in dist or new_cost < dist[k]:
					dist[k] = new_cost
					self.dij_parent[v] = u
					heapq.heappush(pq, (new_cost, v))

		return False, self.expandedDIJ

	def heuristic(self, cm):
		remaining = cm.missionaries + cm.cannibals
		cap = cm.CONSTANTS.CAP_BOAT
		return (remaining + cap - 1) // cap

	def ASTAR(self, cm):
		self.astar_parent = {cm: None}
		self.expandedASTAR = 0
		g = {cm.key(): 0}

		pq = [(self.heuristic(cm), cm)]

		while pq:
			f_u, u = heapq.heappop(pq)
			self.expandedASTAR += 1

			if u.isGoalState():
				return True, self.expandedASTAR

			for v in u.successors():
				tentative_g = g[u.key()] + 1
				k = v.key()

				if k not in g or tentative_g < g[k]:
					g[k] = tentative_g
					f_v = tentative_g + self.heuristic(v)
					self.astar_parent[v] = u
					heapq.heappush(pq, (f_v, v))

		return False, self.expandedASTAR


	def IDASTAR(self, start):

		self.idastar_parent = {start: None}
		self.expandedIDASTAR = 0
		limit = self.heuristic(start)

		def dfs_limited(node, g, limit):
			self.expandedIDASTAR += 1

			f = g + self.heuristic(node)
			if f > limit:
				return f 

			if node.isGoalState():
				return True 

			min_overlimit = float("inf")

			for succ in node.successors():
				if succ not in self.idastar_parent:
					self.idastar_parent[succ] = node
					result = dfs_limited(succ, g + 1, limit)

					if result is True:
						return True

					if isinstance(result, (int, float)) and result < min_overlimit:
						min_overlimit = result

					del self.idastar_parent[succ]

			return min_overlimit

		while True:
			result = dfs_limited(start, 0, limit)

			if result is True:
				return True, self.expandedIDASTAR

			if result == float("inf"):
				return False, self.expandedIDASTAR

			limit = result

