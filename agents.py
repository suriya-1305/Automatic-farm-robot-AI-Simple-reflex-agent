import world
from numpy.random import randint

class simple_reflex_agent:
	def __init__(self):
		return		
	def choose_action(self, percept):
		if percept in ('start', 'move_succeeded'):
			return 'sense_water'
		if percept == 'needs_watering':
			return 'water'
		if percept in ('does_not_need_watering', 'watering_succeeded'):
			return 'sense_weed'
		if percept == 'needs_weeding':
			return 'weed'
		if percept in ('weeding_succeeded', 'does_not_need_weeding', 'hit_barrier'):
			return 'move'

