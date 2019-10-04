import sys
sys.path.insert(0, '../')
from planet_wars import issue_order

def evacuate_this_planet(state):
    dist = 10000
    for fleet in state.enemy_fleets():
        for planet in state.my_planets():
            if fleet.destination_planet == planet.ID:
                if fleet.num_ships > planet.num_ships+fleet.turns_remaining*planet.growth_rate:
                    for nearby_planet in state.my_planets():
                        if state.distance(planet.ID, nearby_planet.ID) < dist:
                            closest_planet = nearby_planet
                            dist = state.distance(planet.ID, nearby_planet.ID)
                    issue_order(state, planet.ID, nearby_planet.ID, planet.num_ships)





    return False


def preemptive_strike(state):
    launch_planet = None

    for fleet in state.enemy_fleets():
        if any(neutral.ID == fleet.destination_planet for neutral in state.neutral_planets()):
            for planet in state.my_planets():
                if state.distance(planet.ID, fleet.destination_planet) == fleet.turns_remaining:
                    if planet.num_ships > fleet.num_ships:
                        launch_planet = planet
                        cost = fleet.num_ships+1
                        target_planet = fleet.destination_planet
        '''elif any(friendly.ID == fleet.destination_planet for friendly in state.my_planets()):
            for planet in state.my_planets():
                if planet.ID != fleet.destination_planet:
                    if state.distance(planet.ID, fleet.destination_planet) == fleet.turns_remaining:
                        if planet.num_ships > fleet.num_ships:
                            launch_planet = planet
                            cost = fleet.num_ships+1 
                            target_planet = fleet.destination_planet '''
    if not launch_planet:
        return False
    else:
        issue_order(state, launch_planet.ID, fleet.destination_planet, cost)
    return False

def attack_strongest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    alt = 0

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)
    target_planet = None

    # (3) Find the weakest enemy planet.
    for enemy_planet in state.enemy_planets():
        if enemy_planet.growth_rate > alt:
            target_planet = enemy_planet
            cost = enemy_planet.num_ships
            alt = enemy_planet.growth_rate
    #strongest_enemy_planet = max(state.enemy_planets(), key=lambda t: t.num_ships, default=None)
    if not strongest_planet or not target_planet:
        return False

    '''for planet in state.my_planets():
        if planet.num_ships > strongest_enemy_planet.growth_rate*state.distance(strongest_planet.ID, strongest_enemy_planet.ID)+strongest_enemy_planet.num_ships:
            issue_order(state, planet.ID, strongest_enemy_planet.ID, 1+strongest_enemy_planet.growth_rate*state.distance(strongest_planet.ID, strongest_enemy_planet.ID)+strongest_enemy_planet.num_ships)            
            break
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.'''
    return issue_order(state, strongest_planet.ID, target_planet.ID, 1+target_planet.growth_rate*state.distance(strongest_planet.ID, target_planet.ID)+target_planet.num_ships)


def spread_to_highest_growing_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    alt = 0
    distance = 10000
    launch_planet = None

    for neutral_planet in state.neutral_planets():
        if neutral_planet.growth_rate > alt:
            target_planet = neutral_planet
            cost = neutral_planet.num_ships
            alt = neutral_planet.growth_rate

    for planet in state.my_planets():
        if planet.num_ships > target_planet.num_ships:
            if state.distance(planet.ID, target_planet.ID) < distance:
                launch_planet = planet
                distance = state.distance(planet.ID, target_planet.ID)
                #cost = cost + distance*target_planet.growth_rate

    if not launch_planet:
        return False
    else:
        for fleet in state.my_fleets():
            if fleet.destination_planet == target_planet.ID:
                return False
            else:
                issue_order(state, planet.ID, target_planet.ID, cost+1)

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
