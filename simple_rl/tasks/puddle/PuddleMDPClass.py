'''
PuddleMDPClass.py: Contains the Puddle class from:

    Boyan, Justin A., and Andrew W. Moore. "Generalization in reinforcement learning:
    Safely approximating the value function." NIPS 1995.
'''

# Python imports.
import math
import numpy as np

# Other imports
from simple_rl.mdp.MDPClass import MDP
from simple_rl.tasks.grid_world.GridWorldMDPClass import GridWorldMDP
from simple_rl.tasks.grid_world.GridWorldStateClass import GridWorldState

class PuddleMDP(GridWorldMDP):
    ''' Class for a Puddle MDP '''

    def __init__(self, gamma=0.99, slip_prob=0.00, name="puddle", is_goal_terminal=True, rand_init=False):
        '''
        Args:
            height (int)
            width (int)
            init_loc (tuple: (int, int))
            goal_locs (list of tuples: [(int, int)...])
        '''
        self.delta = 0.01
        self.puddle_rects = [(0.1,0.8,0.5,0.7), (0.4, 0.7, 0.5, 0.4)]
        GridWorldMDP.__init__(self, width=1.0, height=1.0, init_loc=[0.25, 0.6], goal_locs=[[1.0, 1.0]], gamma=gamma, name=name, is_goal_terminal=is_goal_terminal, rand_init=rand_init)

    def _reward_func(self, state, action):
        if self._is_goal_state_action(state, action):
            return 1.0 - self.step_cost
        elif self._is_puddle_state_action(state, action):
            return -1.0
        else:
            return 0 - self.step_cost

    def _is_puddle_state_action(self, state, action):
        for puddle_rect in self.puddle_rects:
            x_1, y_1, x_2, y_2 = puddle_rect
            if state.x >= x_1 and state.x <= x_2 and \
                state.y <= y_1 and state.y >= y_2:
                return True

        return False


    def _is_goal_state_action(self, state, action):
        '''
        Args:
            state (State)
            action (str)

        Returns:
            (bool): True iff the state-action pair send the agent to the goal state.
        '''
        for g in self.goal_locs:
            if _euclidean_distance(state.x, state.y, g[0], g[1]) <= self.delta * 2 and self.is_goal_terminal:
                # Already at terminal.
                return False

        if action == "left" and self.is_loc_within_radius_to_goal(state.x - self.delta, state.y):
            return True
        elif action == "right" and self.is_loc_within_radius_to_goal(state.x + self.delta, state.y):
            return True
        elif action == "down" and self.is_loc_within_radius_to_goal(state.x, state.y - self.delta):
            return True
        elif action == "up" and self.is_loc_within_radius_to_goal(state.x, state.y + self.delta):
            return True
        else:
            return False

    def is_loc_within_radius_to_goal(self, state_x, state_y):
        for g in self.goal_locs:
            if _euclidean_distance(state_x, state_y, g[0], g[1]) <= self.delta * 2:
                return True
        return False

    def _transition_func(self, state, action):

        if state.is_terminal():
            return state

        to_move = self.delta + np.random.randn(1)[0] / 100.0

        if action == "up":
            next_state = GridWorldState(state.x, min(state.y + to_move, 1))
        elif action == "down":
            next_state = GridWorldState(state.x, max(state.y - to_move, 0))
        elif action == "right":
            next_state = GridWorldState(min(state.x + to_move, 1), state.y)
        elif action == "left":
            next_state = GridWorldState(max(state.x - to_move, 0), state.y)
        else:
            next_state = GridWorldState(state.x, state.y)

        if self._is_goal_state_action(state, action) and self.is_goal_terminal:
            next_state.set_terminal(True)

        return next_state


def _euclidean_distance(ax, ay, bx, by):
    return np.linalg.norm(np.array([ax, ay]) - np.array([bx, by]))
