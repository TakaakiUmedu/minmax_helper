# minmax_helper
Helper class to implement min-max algorithm in Python

# How to use
- prepare `turn(gamme, *state)` function that advances the game
	- `turn()` function will be called with arguments represents the game object and the state
	- in `turn()` function, the following rule must be kept
		- in each of the following parts,
			- each iteration of loop `for choice in game.players_choice(player, choises):`
			- any part out of such loops
		- one of the following must be called just at once
			- `game.player_choice()` funciton, called like `for choice in game.players_choice(player, choises):`
				- `player` argument must be `0` or `1` and indicates which player among player 0 and player 1 will make the choice
				- `choices` argument indicates possible choices as list or anyother iterable object
			- `game.set_result(result)` function with the final result value, when a game sequence is finished
				- player 0 tryes to maximize the result, while player 1 minimize it
			- `game.set_failed()` function, when a game sequence reached some kinds of an error state with that game cannot be continued
				- the searching branch will be ignored
- make `mm = minmax(turn)` to make a simulator
- call `mm.simulate(*start state)` to solve
	- `mm.simulate()` function will returns the result as `(maximized result, choice list)`
	- `maximized result` is the maximum value for player 0 and the minimized value for player 1 that set by `game.set_result()`
	- `choice list` is a list (tuple) of `choice`s to get the result, where `choice` is a tuple like `(who selects, which choice)`

# Examples
## [AtCoder Regular Contest 112 / C - DFS Game](https://atcoder.jp/contests/arc112/tasks/arc112_c)
```
import sys

from minmax import minmax

def turn(game, player, cur, points, coins):
#	cur, points, coins = state
	if coins[cur]:
		coins = list(coins)
		coins[cur] = False
		if player == 0:
			game.next_turn(1 - player, cur, (points[0] + 1, points[1]), coins)
		else:
			game.next_turn(1 - player, cur, (points[0], points[1] + 1), coins)
	else:
		choices = []
		for v in children[cur]:
			if coins[v]:
				choices.append(v)
		if len(choices) > 0:
			for v in game.players_choice(player, choices):
				game.next_turn(1 - player, v, points, coins)
		else:
			if parent[cur] != None:
				game.next_turn(1 - player, parent[cur], points, coins)
			else:
				game.set_result(points[0] - points[1])

N = int(input())

children = [[] for _ in range(N)]
parent = [None] * N

for i, p in zip(range(1, N), map(int, input().split())):
	p -= 1
	parent[i] = p
	children[p].append(i)

g = minmax(turn)
result =  g.simulate(0, 0, (0, 0), [True] * N)

print(result, file = sys.stderr)
print((N + result[0]) // 2)
```

## [AtCoder Grand Contest 002 / E - Candy Piles](https://atcoder.jp/contests/agc002/tasks/agc002_e)

```
import sys
import minmax

from minmax import minmax

def turn(game, player, state):
	for v in game.players_choice(player, range(2)):
		if v == 0:
			if len(state) == 1:
				if player == 0:
					game.set_result(-1)
				else:
					game.set_result(1)
			else:
				game.next_turn(1 - player, state[::-2])
		else:
			new_state = []
			for n in state:
				if n > 1:
					new_state.append(n - 1)
			if len(new_state) == 0:
				if player == 0:
					game.set_result(-1)
				else:
					game.set_result(1)
			else:
				game.next_turn(1 - player, new_state)

N = int(input())

state = list(map(int, input().split()))
state.sort()
state.reverse()

mm = minmax(turn)
result, choices = mm.simulate(0, state)
print(choices, file = sys.stderr)

if result == 1:
	print("First")
else:
	print("Second")

```

