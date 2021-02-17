class minmax:
	class SearchError(Exception):
		pass
	
	def __init__(self, turn):
		self.turn = turn
	
	def players_choice(self, player, items):
		self.choice_stack.append([])
		for choice in items:
			# [choice, result, result is set, search failed in this branch, choice list]
			self.choice_stack[-1].append([choice, None, False, False, None])
			yield choice
		else:
			selected_choice = None
			selected_result = None
			selected_choice_list = None
			for choice_info in self.choice_stack[-1]:
				if not choice_info[3]:
					if not choice_info[2]:
						raise SearchError(f"search imcompleted for choice \"#{choice_info[0]}\"")
					
					result = choice_info[1]
					if selected_choice_list == None or (player == 0 and result > selected_result or player == 1 and result < selected_result):
						selected_choice = choice
						selected_result = result
						selected_choice_list = choice_info[4]
			
			self.choice_stack.pop()
			if selected_choice_list != None:
				self._set_result(selected_result, ((player, selected_choice),) + selected_choice_list)
			else:
				self.set_failed()
	
	def set_result(self, result):
		self._set_result(result, ())
		
	def _set_result(self, result, choice_list):
		choice_info = self.choice_stack[-1][-1]
		if choice_info[2] or choice_info[3]:
			raise SearchError(f"result for choice \"#{choice_info[0]}\" has been already set")
		
		choice_info[1] = result
		choice_info[2] = True
		choice_info[4] = choice_list
	
	def set_failed(self):
		choice_info = self.choice_stack[-1][-1]
		if choice_info[2] or choice_info[3]:
			raise SearchError(f"result for choice \"#{choice_info[0]}\" has been already set")
		
		choice_info[3] = True
	
	def next_turn(self, *state):
		self.turn(self, *state)
	
	def simulate(self, *state):
		self.choice_stack = [[[None, None, False, False, None]]]
		self.next_turn(*state)
		return (self.choice_stack[0][0][1], self.choice_stack[0][0][4])
