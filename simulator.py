import world
import sys
import importlib
import copy

def simulate_agent(agent, worldstate, verbose_flag):
	percept = 'start'
	action_sequence = []
	percept_sequence = [percept]
	count = 0
	while percept != 'failed' and percept != 'succeeded':
		action = agent.choose_action(percept)
		if verbose_flag:
			print ("Percept:",percept,"| Action chosen:",action)
		percept = worldstate.perform_action(action)
		if percept == 'invalid_action':
			raise RuntimeError('Agent returned invalid action')
		if verbose_flag:
			worldstate.print_world()
		action_sequence.append(action)
		percept_sequence.append(percept)
		count += 1
		if count >= 500:
			print ("Agent hit max iters")
			break
	if verbose_flag:
		print ("Verbose output:")
		worldstate.print_details()
		worldstate.print_world()
		print ("Action sequence:", len(action_sequence), action_sequence)
		print ("Percept sequence:", len(percept_sequence), percept_sequence)
	print (percept)
	print ("Number of moves = ", len(action_sequence))
	print ("Water level at end = ", worldstate.water_level)
	print ("Power level at end = ", worldstate.power_level)
	print ("Left to water at end = ", worldstate.to_water)
	print ("Left to weed at end = ", worldstate.to_weed)

def run_test(worldstate, agent_type, agent_module, verbose_flag):
	agent = None
	if agent_type == 'simplereflex':
		agent = agent_module.simple_reflex_agent()
	else:
		print ("Invalid Agent Type Given")
		return
	simulate_agent(agent, worldstate, verbose_flag)
	return
	
if __name__ == '__main__':
	assert(len(sys.argv) > 3)
	agent_module = importlib.import_module(sys.argv[1])
	env_filename = sys.argv[2]
	agent_type = sys.argv[3]
	verbose_flag = False
	if len(sys.argv) > 4:
		if sys.argv[4] == 'v':
			verbose_flag = True
	worldstate = world.World(open(env_filename, 'r'))
	worldstate.print_details()
	worldstate.print_world()
	run_test(worldstate, agent_type, agent_module, verbose_flag)