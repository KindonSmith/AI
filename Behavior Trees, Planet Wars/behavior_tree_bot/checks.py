def if_enemy_fleet(state):
	return any(state.enemy_fleets())

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def have_largest_planet(state):
	strongest_ally = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
	strongest_enemy = max(state.enemy_planets(), key=lambda t: t.num_ships, default=None)
	if not strongest_ally or not strongest_enemy:
		return False
	cost = strongest_enemy.num_ships + (strongest_enemy.growth_rate * state.distance(strongest_enemy.ID, strongest_ally.ID))
	return strongest_ally.num_ships > cost