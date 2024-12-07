from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (state[0], state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        return len(self.children) == 0

# AI agent. Determine the next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3): 
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # (Hint) Useful functions: 
    # self.simulator.current_state, self.simulator.set_state, self.simulator.move

    # TODO: build a game tree from the current node up to the given depth
    def build_tree(self, node=None, depth=0):
        node = node or self.root
        self.simulator.set_state(*node.state)

        if depth == 0:
               return
        
        # adding child nodes to this node
        self.expand_node(node, depth)

        # Recursively build the tree for each child node
        for _, child_node in node.children:
            self.build_tree(child_node, depth - 1)

    def expand_node(self, node, depth):
        if node.player_type == MAX_PLAYER:
            self.expand_max_player_node(node, depth)
        else:
            self.expand_chance_player_node(node, depth)

    def expand_max_player_node(self, node, depth):
        for direction in MOVES:
            if self.simulator.move(direction):
                new_node = Node(self.simulator.current_state(), CHANCE_PLAYER)
                node.children.append((direction, new_node))
                self.simulator.undo()

    def expand_chance_player_node(self, node, depth):
        for tile in self.simulator.get_open_tiles():
            self.simulator.tile_matrix[tile[0]][tile[1]] = 2
            new_node = Node(self.simulator.current_state(), MAX_PLAYER)
            node.children.append((None, new_node))
            self.simulator.tile_matrix[tile[0]][tile[1]] = 0

    # TODO: expectimax calculation.
    # Return a (best direction, expectimax value) tuple if node is a MAX_PLAYER
    # Return a (None, expectimax value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node=None):
        if node is None:
            node = self.root

        if node.is_terminal():
            # Return the current score as the expectimax value for terminal nodes
            return None, node.state[1]  # state[1] is the score part of the state tuple
        
        best_direction = None
        if node.player_type == MAX_PLAYER:
            max_value = 0
            # Explore each child node resulting from a move
            for direction, child in node.children:
                _, child_value = self.expectimax(child)
                # Select the direction which maximizes the value
                if child_value > max_value:
                    max_value = child_value
                    best_direction = direction
            return best_direction, max_value

        elif node.player_type == CHANCE_PLAYER:
            total_value = 0
            num_children = len(node.children)
            # Average the expectimax values of all children
            for _, child in node.children:
                _, child_value = self.expectimax(child)
                total_value += child_value
            if num_children > 0:
                average_value = total_value / num_children
            else:
                average_value = 0
            return None, average_value


    # Return decision at the root
    def compute_decision(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        return random.randint(0, 3)