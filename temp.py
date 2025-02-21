# ino A
"""
    1. defining a class for usres
        1.1. attributes
        1.2. agents functions
        1.3. rules
    2. defining a class for water resources
    3. Test Scenarios
        3.1. define scenarios
        3.2. test scenario
"""

import random


# 1. defining a class for usres
# 1.1. agents class
class Agent:
    agentType = "normalUsage"  # lowUsage, normalUsage, highUsage
    typeOfUsing = "industrial" # agricultural, industrial, municipal
    def __init__(self, agentType, typeOfUsing, condition):
        self.agentType = agentType
        self.typeOfUsing = typeOfUsing

# 1.2. agents functions


# def updateAgents (agent):
#     """
#     Updates the agent's status based on its condition.
#     Parameters:
#     agent (Agent): The agent with all its attributes.
#     Returns:
#     Agent: The agent, potentially with a new type.
#     """
#     if agent.agentType == "lowUsage" and agent.condition != "conservation":
#         agent.agentType = "normalUsage"
#     if agent.agentType == "normal" and agent.condition == "intensive":
#         agent.agentType = "highUsage"
#     if agent.agentType == "normal" and agent.condition == "conservation":
#         agent.agentType = "lowUsage"
#     if agent.agentType == "highUsage" and agent.condition != "intensive":
#         agent.agentType = "normalUsage"
#         return agent

def makeAPopulation(n):
    """
    Generates a specified number of agents with random attributes.
    Parameters:
    n (int): The number of agents to create.
    Returns:
    list: A list of agents, each with random attributes.
    """
    agentTypes = ["lowUsage", "normalUsage", "highUsage"]
    typesOfUsing = ["agricultural", "industrial", "municipal"]

    agents = []
    for _ in range(n):
        agentType = random.choice(agentTypes)
        typeOfUsing = random.choice(typesOfUsing)
        agent = Agent(agentType, typeOfUsing)
        agents.append(agent)

    return agents


# 3. Scenarios
# 3.1. define scenario
class Scenario:
    def __init__(self, name, effectOnLowUsage, effectOnNormalUsage, effectOnHighUsage):
        self.name = name
        self.effectOnLowUsage = effectOnLowUsage
        self.effectOnNormalUsage = effectOnNormalUsage
        self.effectOnHighUsage = effectOnHighUsage

# 3.1. test scenario
# 3.1.1. implementing scenario on the environment and agents
def applyScenarioToAgent(scenario,agent):
    """
    Updates the agent's status based on its condition.
    Parameters:
    agent (Agent): The agent with all its attributes.
    Returns:
    Agent: The agent, potentially with a new type.
    """

    if agent.agentType == "lowUsage" and agent.condition != "conservation":
        agent.agentType = "normalUsage"

    if agent.agentType == "normal" and agent.condition == "intensive":
        agent.agentType = "highUsage"
    if agent.agentType == "normal" and agent.condition == "conservation":
        agent.agentType = "lowUsage"

    if agent.agentType == "highUsage" and agent.condition != "intensive":
        agent.agentType = "normalUsage"

        return agent

# 3.1.1. Scenario 1
# This scenario changes 50% of normal municipal users to low usage.
# Additionally, if the environment prioritizes conservation, 25% of high usage
# municipal users will shift to normal usage.
scenario1 = Scenario("encouragement", 1, 1, 0.5)

agents = makeAPopulation(10)

