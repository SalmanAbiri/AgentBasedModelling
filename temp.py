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

class PMTSubSocialParameters:
    welfare = random.random() # variable
    groundwaterStatus = random.random() # variable
    trustInAuthorities = random.random()
    agriculturalExperience = random.random()
    education = random.random()
    importanceAndUnderstandingOfConsequencesOfSubsidence = random.random()
    Age = random.random()
    dependenceOnAgriculturalLivelihoods = random.random()

class PMTSocialParameters:
        attitude = 0.0
        subjectiveNorm = 0.0
        preceivedBehavioralControl = 0.0
        pmtSocialFactor = 0.0
        def calculateParameters(self, pmtSubSocialParams):
            for i in range(len(pmtSubSocialParams)):
                sumAttitude = sumAttitude + (pmtSubSocialParams[i].welfare + 
                                             pmtSubSocialParams[i].trustInAuthorities + 
                                             pmtSubSocialParams[i].agriculturalExperience)/3
                sumSubjectiveNorm = sumSubjectiveNorm + (pmtSubSocialParams[i].education + 
                                                        pmtSubSocialParams[i].importanceAndUnderstandingOfConsequencesOfSubsidence + 
                                                        pmtSubSocialParams[i].groundwaterStatus)/3
                sumPreceivedBehavioralControl = sumPreceivedBehavioralControl + (pmtSubSocialParams[i].age
                                                                                 + pmtSubSocialParams[i].education
                                                                                 + pmtSubSocialParams[i].agriculturalExperience
                                                                                 + pmtSubSocialParams[i].dependenceOnAgriculturalLivelihoods)/4
            self.attitude = sumAttitude/len(pmtSubSocialParams)
            self.subjectiveNorm = sumSubjectiveNorm/len(pmtSubSocialParams)
            self.preceivedBehavioralControl = sumPreceivedBehavioralControl/len(pmtSubSocialParams)
            self.pmtSocialFactor = (self.attitude + self.subjectiveNorm + self.preceivedBehavioralControl) / 3

class SCTSocialParameters:
        performanceAccomplishment = 0.0
        emotionalArousal = 0.0
        VicariousLearning = 0.0
        socialPersuation = 0.0
        # results:
        approachAndAvoidance = 0.0
        performance = 0.0
        persistence = 0.0
        
        

class Agent:
    agentType = 1  # 1: proactive, 2: interactive, 3: bounded rational, 4: preceptive
    typeOfUsing = 1 # 1: agricultural, 2: industrial, 3: municipal
    def __init__(self, agentType, typeOfUsing):
        self.agentType = agentType
        self.typeOfUsing = typeOfUsing
    
    def socialFactor (self):
        return(round(random.uniform((self.agentType-1)*0.25, self.agentType*0.25), 2))

    def decision(self):
        # calculate social factor
        socialFac = self.socialFactor()
        # calculate economic factor
        # calculate final decision
        print(12.)

# 1.2. agents functions

def makeAPopulation(n):
    """
    Generates a specified number of agents with random attributes.
    Parameters:
    n (int): The number of agents to create.
    Returns:
    list: A list of agents, each with random attributes.
    """
    agentTypes = [ 1, 2, 3, 4]
    typesOfUsing = [1, 2, 3]

    agents = []
    for _ in range(n):
        agentType = random.randint(1, 4)
        typeOfUsing = random.randint(1, 3)
        agent = Agent(agentType, typeOfUsing)
        agents.append(agent)

    return agents



# 3. Environment
# 3.1. Define the environment
class Environment:
    def __init__(self, name, groundWaterHeight=100, groundWaterArea=100, numberOfWells=10,\
        socialCondition="Overexploited"):
        self.name = name
        self.groundWaterHeight = groundWaterHeight # meter
        self.groundWaterArea = groundWaterArea     # squared kilo meter
        self.numberOfWells = numberOfWells
        self.wellsCoordinates = []                 # id, x, y
        self.socialCondition = socialCondition     # Overexploited, Sustainable, Conserved
        self.effectOnType1 = None
        self.effectOnType2 = None
        self.effectOnType3 = None
        self.effectOnType4 = None

    def set_well_coordinates(self, coordinates):
        """Sets coordinates for all wells."""
        self.wellsCoordinates = coordinates

    def add_well(self, well_id, x, y):
        """Add a single well's coordinates."""
        self.wellsCoordinates.append({"id": well_id, "x": x, "y": y})

    def set_effects(self, effectOnType1, effectOnType2, effectOnType3, effectOnType4):
        """Set the effects of groundwater usage on different user types."""
        self.effectOnType1 = effectOnType1
        self.effectOnType2 = effectOnType2
        self.effectOnType3 = effectOnType3
        self.effectOnType4 = effectOnType4

    def update_social_condition(self, new_condition):
        """Update the social condition based on usage patterns."""
        self.socialCondition = new_condition

    def display_environment(self):
        """Display information about the environment."""
        print(f"Environment: {self.name}")
        print(f"Groundwater Height: {self.groundWaterHeight} meters")
        print(f"Groundwater Area: {self.groundWaterArea} square kilometers")
        print(f"Number of Wells: {self.numberOfWells}")
        print(f"Social Condition: {self.socialCondition}")
        print(f"Wells Coordinates: {self.wellsCoordinates}")
        print(f"Effect on Type1: {self.effectOnType1}")
        print(f"Effect on Type2: {self.effectOnType2}")
        print(f"Effect on Type3: {self.effectOnType3}")
        print(f"Effect on Type4: {self.effectOnType4}")

    def __str__(self):
        return (f"Environment {self.name}: {self.socialCondition} - {self.groundWaterHeight}\
            meters groundwater, "
                f"{self.numberOfWells} wells.")

# 4. Scenarios
# 4.1. define scenario
class Scenario:
    def __init__(self, name, effectOnType1, effectOnType2, effectOnType3, effectOnType4):
        self.name = name
        self.effectOnType1 = effectOnType1
        self.effectOnType2 = effectOnType2
        self.effectOnType3 = effectOnType3
        self.effectOnType4 = effectOnType4

# 4.2. test scenario
# 4.2.1. implementing scenario on the environment and agents
def applyScenarioToAgent(scenario,agent, environment):
    """
    Updates the agent's status based on its condition.
    Parameters:
    agent (Agent): The agent with all its attributes.
    Returns:
    Agent: The agent, potentially with a new type.
    """
    # check environmental status
    socialCondition = calculateSocialCondition(agents)
    scenario.effectOnType1 = max(min(scenario.effectOnType1+socialCondition, 1),-1)
    scenario.effectOnType2 = max(min(scenario.effectOnType2+socialCondition, 1),-1)
    scenario.type3 = max(min(scenario.type3+socialCondition, 1),-1)

    if agent.agentType == 1 and scenario.effectOnType1 == +1:
        agent.agentType = 2

    if agent.agentType == 2 and scenario.effectOnType2 == -1:
        agent.agentType = 1
    if agent.agentType == 2 and scenario.effectOnType2 == +1:
        agent.agentType = 3

    if agent.agentType == 3 and scenario.type3 == -1:
        agent.agentType = 2

    return agent

def calculateSocialCondition(agents):
    summation = 0
    for agent in agents:
        if agent.agentType == 1:
            summation = summation-1
        if agent.agentType == 2:
            summation = summation+1
    average = summation/len(agents)
    rounded_average = round(average)  # Round to nearest whole number
    return rounded_average

scenario1 = Scenario("encouragement", 1, 1, 0.5, 1)

agents = makeAPopulation(10)
print(123)