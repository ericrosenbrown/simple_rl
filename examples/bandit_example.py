#!/usr/bin/env python

# Python imports.
import sys

# Other imports.
import srl_example_setup
from simple_rl.agents import LinUCBAgent, QLearnerAgent, RandomAgent
from simple_rl.tasks import BanditMDP
from simple_rl.run_experiments import run_agents_on_mdp

def main(open_plot=True):
    # Setup MDP, Agents.
    mdp = BanditMDP()

    lin_agent = LinUCBAgent(actions=mdp.get_actions())
    ql_agent = QLearnerAgent(actions=mdp.get_actions())
    rand_agent = RandomAgent(actions=mdp.get_actions())

    # Run experiment and make plot.
    run_agents_on_mdp([ql_agent, lin_agent, rand_agent], mdp, instances=25, episodes=1, steps=10000, open_plot=open_plot)

if __name__ == "__main__":
    main(open_plot=not(sys.argv[-1] == "no_plot"))
