# Kindon Smith and Riley Honbo
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 10
explore_faction = 2.

def traverse_nodes(node, state, identity, board):
    """ Traverses the tree until the end criterion are met.
    next_node.child_nodes[n] = ("hello")

    Args:
        node:       A tree node from which the search is traversing.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    list_of_actions = board.legal_actions(state)
    current_node = node

    while not board.is_ended(state):
        current_player = board.current_player(state)
        if current_node.untried_actions:
            return expand_leaf(current_node,state,board)
        else:
            score = 0
            for _,child in current_node.child_nodes.items():
                score_check = ucb1(current_node, child, current_player, identity)
                if score_check >= score:
                    step_node = child
                    score = score_check
            current_node = step_node
            state = board.next_state(state,current_node.parent_action)

    return current_node



def expand_leaf(node, state, board):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        state:  The state of the game.

    Returns:    The added child node.

    """

    random_options = choice(node.untried_actions)
    legal_actions = board.legal_actions(board.next_state(state, random_options))
    child_node = MCTSNode(node,random_options,legal_actions)
    node.child_nodes[random_options] = child_node
    node.untried_actions.remove(random_options)
    return child_node


def rollout(state, board, node):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        state:  The state of the game. (Initial, root state)
        node :  the given leaf node that we want to simulate on

    """

    traceback = []
    bot_player = board.current_player(state)

    while node.parent != None:
        traceback.append(node.parent_action)
        node = node.parent

    while traceback:
        step = traceback.pop()
        state = board.next_state(state, step)

    #Now we look at the legal moves from here,
    legal_moves = board.legal_actions(state)
    #and play out the game with random moves
    while not board.is_ended(state):
        random_move = choice(legal_moves)


        state = board.next_state(state, random_move)
        legal_moves = board.legal_actions(state)

    #we then use the the recorded player id to see if we won
    final_score = board.points_values(state)
    if final_score[bot_player] == 1:
        won = True
    else:
        won = False

    return won


def backpropagate(node, won, board):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    while True:
        node.visits += 1
        if won is True:
            node.wins += 1
        if node.parent is None:
            break
        else:
            node = node.parent


def ucb1(parent, child, player, bot_identity):

    if child.visits == 0:
        exploit = 0
        explore = inf
    else:
        exploit = child.wins/child.visits
        explore = explore_faction*sqrt(log(parent.visits)/child.visits)

    # It will give an accurate ratio taking into consideration enemy moves
    if player != bot_identity:
        exploit = 1 - exploit
    return exploit+explore


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    alt = 0
    move_list = []
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        return_node = traverse_nodes(node, state, identity_of_bot, board)
        won = rollout(state, board, return_node)
        backpropagate(return_node, won, board)

    for move, child in root_node.child_nodes.items():
        check = child.wins/child.visits
        if check >= alt:
            final_decision = move
            alt = check

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    return final_decision
