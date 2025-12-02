from collections import defaultdict
import heapq
import itertools


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
		if CONSTS is None:
			self.CONSTANTS = CONST(missionaries, cannibals, 2, 100)
		else:
			self.CONSTANTS = CONSTS

		if moves is None:
			self.moves = self.genPossibleMoves()
		else:
			self.moves = moves

	def key(self):
		return (self.missionaries, self.cannibals, self.dir)
		
	def genPossibleMoves(self):
		moves = []
		for m in range(self.CONSTANTS.CAP_BOAT + 1):
			for c in range(self.CONSTANTS.CAP_BOAT + 1):
				if 0 < m < c:
					continue
				if 1 <= m + c <= self.CONSTANTS.CAP_BOAT:
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
		new_dir = Direction.NEW_TO_OLD if self.dir == Direction.OLD_TO_NEW else Direction.OLD_TO_NEW
		
		newState = State(
			self.missionaries + sgn * m,
			self.cannibals + sgn * c,
			new_dir,
			self.missionariesPassed - sgn * m,
			self.cannibalsPassed - sgn * c,
			self.level + 1,
			self.CONSTANTS
		)
		
		if newState.isValid():
			newState.action = f" take {m} missionaries and {c} cannibals {direction}."
			listChild.append(newState)

	def ida_successors(self):
		children = []
		if self.isGoalState() or not self.isValid():
			return children

		for m, c in self.moves:
			if self.dir == Direction.OLD_TO_NEW:
				new_m = self.missionaries - m
				new_c = self.cannibals - c
				new_m_passed = self.missionariesPassed + m
				new_c_passed = self.cannibalsPassed + c
				direction = "from the original shore to the new shore"
			else:
				new_m = self.missionaries + m
				new_c = self.cannibals + c
				new_m_passed = self.missionariesPassed - m
				new_c_passed = self.cannibalsPassed - c
				direction = "back from the new shore to the original shore"

			new_dir = Direction.NEW_TO_OLD if self.dir == Direction.OLD_TO_NEW else Direction.OLD_TO_NEW
			new_node = State(
				new_m,
				new_c,
				new_dir,
				new_m_passed,
				new_c_passed,
				self.level + 1,
				self.CONSTANTS,
				None
			)

			if new_node.isValid():
				new_node.action = f" take {m} missionaries and {c} cannibals {direction}."
				children.append(new_node)

		return children


	def isValid(self):
		# obvious
		if self.missionaries < 0 or self.cannibals < 0 or self.missionaries > self.CONSTANTS.MAX_M or self.cannibals > self.CONSTANTS.MAX_C or (
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

#TERMINAL_STATE = State(-1, -1, Direction.NEW_TO_OLD, -1, -1, 0, None)
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
		visited = {(cm.missionaries, cm.cannibals, cm.dir): True}
		cm.level = 0

		queue = [cm]
		while queue:
			self.expandedBFS += 1

			u = queue.pop(0)

			if u.isGoalState():
				queue.clear()
				return True, self.expandedBFS

			# Stops searching after a certain node limit 
			if self.expandedBFS > u.CONSTANTS.MAX_NODES:
				print("EXCEEDED NODE LIMIT of %d" % u.CONSTANTS.MAX_NODES)
				queue.clear()
				return False, self.expandedBFS

			for v in reversed(u.successors()):
				if (v.missionaries, v.cannibals, v.dir) not in visited.keys():
					v.level = u.level + 1
					queue.append(v)
					visited[(v.missionaries, v.cannibals, v.dir)] = True

		return False, self.expandedBFS

	def DFS(self, cm):
		self.expandedDFS = 0
		visited = {(cm.missionaries, cm.cannibals, cm.dir): True}

		stack = [cm]
		while stack:
			u = stack.pop()
			self.expandedDFS += 1

			if u.isGoalState():
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
					stack.append(v)
		return False, self.expandedDFS
	
	def DIJKSTRA(self, cm):
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
					heapq.heappush(pq, (new_cost, v))

		return False, self.expandedDIJ

	def heuristic(self, cm):
		remaining = cm.missionaries + cm.cannibals
		cap = cm.CONSTANTS.CAP_BOAT
		return (remaining + cap - 1) // cap

	def ASTAR(self, cm):
		self.expandedASTAR = 0
		g = {cm.key(): 0}
		visited = set() 

		counter = itertools.count()
		pq = [(self.heuristic(cm), next(counter), cm)]

		while pq:
			f_u, _, u = heapq.heappop(pq)

			if u.key() in visited:
				continue
			visited.add(u.key())

			self.expandedASTAR += 1

			if u.isGoalState():
				return True, self.expandedASTAR

			for v in u.successors():
				tentative_g = g[u.key()] + 1
				k = v.key()

				if k not in g or tentative_g < g[k]:
					g[k] = tentative_g
					f_v = tentative_g + self.heuristic(v)
					heapq.heappush(pq, (f_v, next(counter), v))

		return False, self.expandedASTAR



	def IDASTAR(self, start):
		self.expandedIDASTAR = 0

		def heuristic(n):
			remaining = n.missionaries + n.cannibals
			cap = n.CONSTANTS.CAP_BOAT
			return (remaining + cap - 1) // cap

		limit = heuristic(start)

		path = [start]
		path_keys = {start.key()}

		def dfs_limited(node, g, limit):
			self.expandedIDASTAR += 1

			f = g + heuristic(node)
			if f > limit:
				return f

			if node.isGoalState():
				return True

			min_overlimit = float("inf")

			for succ in node.ida_successors():
				if succ.key() in path_keys:
					continue

				path.append(succ)
				path_keys.add(succ.key())

				result = dfs_limited(succ, g + 1, limit)

				path.pop()
				path_keys.remove(succ.key())

				if result is True:
					return True

				if isinstance(result, (int, float)) and result < min_overlimit:
					min_overlimit = result

			return min_overlimit

		while True:
			result = dfs_limited(start, 0, limit)

			if result is True:
				return True, self.expandedIDASTAR

			if result == float("inf"):
				return False, self.expandedIDASTAR
			limit = result
