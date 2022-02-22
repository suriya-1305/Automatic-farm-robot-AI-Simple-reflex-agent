import copy
from collections import deque
class GridSquare:
	def __init__(self, spec_string):
		chars = ['x','F','T']
		assert(len(spec_string)==2 and spec_string[0] in chars and spec_string[1] in chars)
		self.barrier = False
		self.needs_watering = False
		self.needs_weeding = False
		if spec_string == 'xx':
			self.barrier = True
		else:
			if spec_string[0] == 'T':
				self.needs_watering = True
			if spec_string[1] == 'T':
				self.needs_weeding = True
class World:
	def __init__(self, fileobject):
		lines = fileobject.readlines()
		assert(len(lines) >= 1)
		dimension_info = lines[0].split()
		assert(len(dimension_info) == 2)
		agent_info = lines[1].split()
		assert(len(agent_info) == 10)
		gridlines = lines[2:]

		self.nrows = int(dimension_info[0])
		self.ncols = int(dimension_info[1])

		self.agent_row = int(agent_info[0])
		self.agent_col = int(agent_info[1])
		assert(self.agent_row < self.nrows and self.agent_col < self.ncols)
		self.agent_facing = str(agent_info[2])
		assert(self.agent_facing in ['north', 'south', 'east', 'west'])
		self.water_level = int(agent_info[3])
		self.watering_amount = int(agent_info[4])
		self.power_level = int(agent_info[5])
		self.watering_power = int(agent_info[6])
		self.weeding_power = int(agent_info[7])
		self.moving_power = int(agent_info[8])
		self.sensing_power = int(agent_info[9])
		self.grid = []
		self.to_water = 0
		self.to_weed = 0
		for line in gridlines:
			gridrow = []
			for square in line.split():
				gs = GridSquare(square)
				if gs.needs_watering:
					self.to_water += 1
				if gs.needs_weeding:
					self.to_weed += 1
				gridrow.append(gs)
			assert(len(gridrow) == self.ncols)
			self.grid.append(gridrow)
		assert(len(self.grid) == self.nrows)
		assert(self.grid[self.agent_row][self.agent_col].barrier == False)

	def print_details(self):
		print ("nrows =", self.nrows, "ncols =", self.ncols)
		print ("water level =", self.water_level, "power level =", self.power_level)
		print ("amount per watering =", self.watering_amount)
		print ("power required for...")
		print ("...watering =", self.watering_power)
		print ("...weeding =", self.weeding_power)
		print ("...moving =", self.moving_power)
		print ("...sensing =", self.sensing_power)
		print ("places left to weed =", self.to_weed)
		print ("places left to water =", self.to_water)

	def print_world(self):
		print ("agentpos = (", self.agent_row, ", ", self.agent_col, ") facing", self.agent_facing)
		gridstr = "  "
		for j in range(self.ncols):
			gridstr += str(j) + "  "
		gridstr += '\n'
		for i, row in enumerate(self.grid):
			gridstr += str(i) + ' '
			for square in row:
				if square.barrier:
					gridstr += "xx "
				else:
					ch1 = 'F'
					ch2 = 'F'
					if square.needs_watering:
						ch1 = 'T'
					if square.needs_weeding:
						ch2 = 'T'
					gridstr += ch1+ch2+' '
			gridstr += '\n'
		print (gridstr)

	def water(self):
		if self.water_level < self.watering_amount or self.power_level < self.watering_power:
			if self.power_level < self.watering_power:
				self.power_level = 0
			if self.water_level < self.watering_amount:
				self.water_level = 0
			return 'watering_failed' 
		if self.grid[self.agent_row][self.agent_col].needs_watering:
			self.grid[self.agent_row][self.agent_col].needs_watering = False
			self.to_water -= 1
		self.water_level -= self.watering_amount
		self.power_level -= self.watering_power
		return 'watering_succeeded'

	def weed(self):
		if self.power_level < self.weeding_power:
			self.power_level = 0
			return 'weeding_failed'
		if self.grid[self.agent_row][self.agent_col].needs_weeding:
			self.grid[self.agent_row][self.agent_col].needs_weeding = False
			self.to_weed -= 1
		self.power_level -= self.weeding_power
		return 'weeding_succeeded'
	
	def move(self, direction=None):
		if self.power_level < self.moving_power:
			self.power_level = 0
			return 'move_failed'

		hit_barrier = False
		if direction is not None:
			self.agent_facing = direction

		if self.agent_facing == 'north':
			self.agent_row -= 1
			if self.agent_row < 0 or self.grid[self.agent_row][self.agent_col].barrier:
				self.agent_row += 1
				self.agent_facing = 'east'
				hit_barrier = True
		elif self.agent_facing == 'south':
			self.agent_row += 1
			if self.agent_row >= self.nrows or self.grid[self.agent_row][self.agent_col].barrier:
				self.agent_row -= 1
				self.agent_facing = 'west'
				hit_barrier = True
		elif self.agent_facing == 'east':
			self.agent_col += 1
			if self.agent_col >= self.ncols or self.grid[self.agent_row][self.agent_col].barrier:
				self.agent_col -= 1
				self.agent_facing = 'south'
				hit_barrier = True
		elif self.agent_facing == 'west':
			self.agent_col -= 1
			if self.agent_col < 0 or self.grid[self.agent_row][self.agent_col].barrier:
				self.agent_col += 1
				self.agent_facing = 'north'
				hit_barrier = True
		self.power_level -= self.moving_power
		if hit_barrier:
			return 'hit_barrier'
		else:
			return 'move_succeeded'
		
	def sense_water(self):
		if self.power_level < self.sensing_power:
			self.power_level = 0
			return 'water_sensing_failed'
		self.power_level -= self.sensing_power
		square = self.grid[self.agent_row][self.agent_col]
		if square.needs_watering:
			return 'needs_watering'
		else:
			return 'does_not_need_watering'
	
	def sense_weed(self):
		if self.power_level < self.sensing_power:
			self.power_level = 0
			return 'weed_sensing_failed' 
		self.power_level -= self.sensing_power
		square = self.grid[self.agent_row][self.agent_col]
		if square.needs_weeding:
			return 'needs_weeding'
		else:
			return 'does_not_need_weeding'

	def succeeded(self):
		return (self.to_weed == 0 and self.to_water == 0)

	def failed(self):
		return ((self.power_level == 0 and (self.to_weed > 0 or self.to_water > 0)) or
				(self.water_level == 0 and self.to_water > 0))
	
	def perform_action(self, action):
		result = 'invalid_action'
		if action == 'sense_weed':
			result = self.sense_weed()
		elif action == 'sense_water':
			result = self.sense_water()
		elif action == 'move':
			result = self.move()
		elif action == 'move_north':
			result = self.move('north')
		elif action == 'move_south':
			result = self.move('south')
		elif action == 'move_east':
			result = self.move('east')
		elif action == 'move_west':
			result = self.move('west')	
		elif action == 'water':
			result = self.water()
		elif action == 'weed':
			result = self.weed()

		if self.failed():
			result = 'failed'
		if self.succeeded():
			result = 'succeeded'

		return result

class SearchSquare:
	def __init__(self, valid, visited):
		self.valid = valid
		self.visited = visited

class search_grid:
	def __init__(self, world):
		self.search_grid = []
		self.count = 0
		self.nrows = world.nrows
		self.ncols = world.ncols
		for row in world.grid:
			search_row = []
			for square in row:
				search_row.append(SearchSquare(not square.barrier, False))
				if not square.barrier:
					self.count += 1
			self.search_grid.append(search_row)
		self.search_grid[world.agent_row][world.agent_col].visited = True
		self.count -= 1
		self.row = world.agent_row
		self.col = world.agent_col

	def perform_action(self, action):
		if action == 'move_north':
			if self.row == 0 \
				or not self.search_grid[self.row-1][self.col].valid:
				return False, False
			else:
				self.row -= 1
		elif action == 'move_east':
			if self.col == self.ncols-1 \
				or not self.search_grid[self.row][self.col+1].valid:
				return False, False
			else:
				self.col += 1
		elif action == 'move_south':
			if self.row == self.nrows-1 \
				or not self.search_grid[self.row+1][self.col].valid:
				return False, False
			else:
				self.row += 1
		elif action == 'move_west':
			if self.col == 0 \
				or not self.search_grid[self.row][self.col-1].valid:
				return False, False
			else:
				self.col -= 1
		visited_before = self.search_grid[self.row][self.col].visited
		if not visited_before:
			self.search_grid[self.row][self.col].visited = True
			self.count -= 1
		return True, visited_before
	
	def all_visited(self):
		return self.count == 0

class node:
	actionlist = ['move_north', 'move_east', 'move_south', 'move_west']

	def __init__(self, grid, parent, action, pathcost):
		self.grid = grid 
		self.parent = parent
		self.action = action
		self.pathcost = pathcost

	def expand(self):
		successors = []
		allvisited = True
		for a in node.actionlist:
			nextstate = copy.deepcopy(self.grid)
			result, visited_before = nextstate.perform_action(a)
			if result: 
				allvisited = (allvisited and visited_before)
				successors.append((node(nextstate, self, a, self.pathcost+1), visited_before))
		if allvisited:
			return [t[0] for t in successors]
		else:
		 	return [t[0] for t in successors if not t[1]]

	def isgoal(self):
		return self.grid.all_visited()

def get_action_sequence(nd):
	reversed_actions = []
	while nd is not None:
		if nd.parent is not None:
			reversed_actions.append(nd.action)
		nd = nd.parent
	return reversed_actions[::-1]
def BFS(worldstate):
	grid = search_grid(worldstate)
	rootnode = node(grid, None, None, 0)
	bfsqueue = deque()
	bfsqueue.append(rootnode)
	count = 0
	while len(bfsqueue) > 0:
		nextnode = bfsqueue.popleft()
		if nextnode.isgoal():
			return get_action_sequence(nextnode), True
		successors = nextnode.expand()
		for n in successors:
			bfsqueue.append(n)
		if count%1000 == 0:
		 	print ("BFS Iter", count, ", search depth", nextnode.pathcost)
		if count >= 10000:
			print ("BFS Iteration limit exceeded, returning empty list")
			return [], False
		count += 1
	return [], False

