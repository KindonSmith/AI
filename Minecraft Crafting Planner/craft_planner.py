import json
from collections import namedtuple, defaultdict, OrderedDict
from timeit import default_timer as time
from math import inf

Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])


class State(OrderedDict):
    """ This class is a thin wrapper around an OrderedDict, which is simply a dictionary which keeps the order in
        which elements are added (for consistent key-value pair comparisons). Here, we have provided functionality
        for hashing, should you need to use a state as a key in another dictionary, e.g. distance[state] = 5. By
        default, dictionaries are not hashable. Additionally, when the state is converted to a string, it removes
        all items with quantity 0.

        Use of this state representation is optional, should you prefer another.
    """

    def __key(self):
        return tuple(self.items())

    def __hash__(self):
        return hash(self.__key())

    def __lt__(self, other):
        return self.__key() < other.__key()

    def copy(self):
        new_state = State()
        new_state.update(self)
        return new_state

    def __str__(self):
        return str(dict(item for item in self.items() if item[1] > 0))

def in_inventory(item, state):
    # return TRUE if the item is in the current inventory
    # return FALSE otherwise
    if item in state and state[item] > 0:
        return True
    else:
        return False


def make_checker(rule):
    # Implement a function that returns a function to determine whether a STATE MEETS a
    # rule's REQUIREMENTS. This code runs once, when the rules are constructed before
    # the search is attempted.

    # establish consumables and requirements
    if 'Consumes' in rule:
        con = rule['Consumes']
    else:
        con = None
        
    if 'Requires' in rule:
        req = rule['Requires']
    else:
        req = None

    def check(state):
        # This code is called by graph(state) and runs millions of times.
        # Tip: Do something with rule['Consumes'] and rule['Requires'].
        C = con
        R = req
        #print("print requirements ", R)
        check_passed = False
        #print("IN CHECK", C, R)
        # test: HAVE REQUIREMENTS
        if R:
            for i, b in R.items():
                # in my inventory?
                if i in state.keys() and state[i] <= 0:
                    #print("no reqs")
                    return check_passed
        # test: HAVE NEEDED RESOURCES
        if C:
            for i, a in C.items():
                # have enough?
                if a > state[i]:
                    #print("not enough of item")
                    return check_passed
        # tests passed: RETURN TRUE
        check_passed = True
        return check_passed

    return check


def make_effector(rule):
    # Implement a function that returns a function which TRANSITIONS from state to
    # new_state given the rule. This code runs once, when the rules are constructed
    # before the search is attempted.

    if 'Consumes' in rule:
        con = rule['Consumes']
    else:
        con = None

    pro = rule['Produces']

    def effect(state):
        # This code is called by graph(state) and runs millions of times
        # Tip: Do something with rule['Produces'] and rule['Consumes'].
        next_state = state.copy()
        C = con
        P = pro

        # if it is consuming:
        #   remove those from the new state
        if C:
            for item, amt in C.items():
                next_state[item] -= amt
        # if it is producing:
        #   add them to the state
        for item, amt in P.items():
            next_state[item] += amt
            
        return next_state

    return effect


def make_goal_checker(goal):
    # Implement a function that returns a function which checks if the state has
    # MET THE GOAL criteria. This code runs once, before the search is attempted.

    def is_goal(state):
        #print("in is goal: ", state)
        has = state
        # This code is used in the search process and may be called millions of times.
        for item, amt in goal.items():
            if item in has:
                if has[item] < amt:
                    return False
            else:
                return False
        return True

    return is_goal


def graph(state):
    # Iterates through all recipes/rules, checking which are valid in the given state.
    # If a rule is valid, it returns the rule's name, the resulting state after application
    # to the given state, and the cost for the rule.
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)

"""
def heuristic(state, time, json):
    # Implement your heuristic here!
    retval = time
    needed = []
    # look thru what is needed for the goal
    for item, amnt in json['Goal'].items():
        # look thru requiements
        if 'Requires' in json['Recipes'][item]:
            
            for req, boo in json['Recipes'][*]['Requires'].items():
                # if we dont already have it
                if !state[req]:
                    needed.append(req)
        # look thru consumptions
    
    return retval
"""
def heuristic(future_state, time, json, current_state):
    # Implement your heuristic here!
    retval = 0
    c_var = [(items, amnt) for items, amnt in current_state.items() if amnt > 0]
    f_var = [(items, amnt) for items, amnt in future_state.items() if amnt > 0]

    if not c_var or not f_var:
        return 100

    # MORE VARIETY OF ITEMS
    # better value = more variety
    # future variety > current_variety
    if len(c_var) < len(f_var):
        retval -= (len(f_var))
    # LESS OF SAME ITEM
    else:
        # most of item
        f_most = (max(f_var, key=lambda i: i[1]))
        c_most = (max(c_var, key=lambda i: i[1]))
        #print(f_most, c_most)
        if f_most[1] > c_most[1]:
            retval += c_most[1]
        
    return retval


def search(graph, state, is_goal, limit, heuristic, full_list):

    start_time = time()
    path = [(state, None)]
    path_found = False
    explored = []
    best_state = state.copy()
    # Implement your search here! Use your heuristic here!
    # When you find a path to the goal return a list of tuples [(state, action)]
    # representing the path. Each element (tuple) of the list represents a state
    # in the path and the action that took you to this state
    while time() - start_time < limit:
        # parse first obj in graph connections (yield)
        if path_found:
            break
        obj = graph(best_state)
        best_name = ""
        best_cost = inf
        current_state = best_state
        # item creates good path? A*
        # this will update our current state
        for n, e, c in obj:
            #print(n, e, c)
            # goal state found?
            #break if no e
            if not e:
                break
            # calc goal or best cost
            current_cost = heuristic(e, c, full_list, current_state)
            if is_goal(e):
                best_name = n
                best_state = e
                path_found = True
                #print("CURRENT PATH: ", path)
                break
            elif current_cost < best_cost:
                best_name = n
                best_cost = current_cost
                best_state = e
        #print("CURRENT STATE: ", state)
        path.append((best_state, best_name))  
        #print("CURRENT PATH UPDATED: ", current_cost)

    """
        Create List of items that produce my current NEED
        list = [act for act,results in [Recipes] if any([Recipes][Produces] == NEED)]
        for action, requirement in ???:
    """
    if not path_found:
        # Failed to find a path
        print(time() - start_time, 'seconds.')
        print("Failed to find a path from", state, 'within time limit.')
        print(best_state)
        return None
    else:
        print(time() - start_time, 'seconds to FIND goal.')
        return path

if __name__ == '__main__':
    with open('crafting.json') as f:
        Crafting = json.load(f)

    # # List of items that can be in your inventory:
    #print('All items:', Crafting['Items'])
    #
    # # List of items in your initial inventory with amounts:
    print('Initial inventory:', Crafting['Initial'])
    #
    # # List of items needed to be in your inventory at the end of the plan:
    print('Goal:',Crafting['Goal'])
    #
    # # Dict of crafting recipes (each is a dict):
    #print('Example recipe:','craft stone_pickaxe at bench ->',Crafting['Recipes']['craft stone_pickaxe at bench'])

    # Build rules
    all_recipes = []
    for name, rule in Crafting['Recipes'].items():
        checker = make_checker(rule)
        effector = make_effector(rule)
        recipe = Recipe(name, checker, effector, rule['Time'])
        all_recipes.append(recipe)

    print("All recipes made.... ")#, all_recipes)

    # Create a function which checks for the goal
    is_goal = make_goal_checker(Crafting['Goal'])

    # Initialize first state from initial inventory
    state = State({key: 0 for key in Crafting['Items']})
    state.update(Crafting['Initial'])

    print("STARTING STATE: ", state)

    #print("GRAPH:???  ", graph(state))

    # Search for a solution
    resulting_plan = search(graph, state, is_goal, 30, heuristic, Crafting)

    if resulting_plan:
        # Print resulting plan
        print("PATH FOUND: ")
        #for state, action in resulting_plan:
        #    print('\t', action, " -> ", state)
        print(resulting_plan[-1])
