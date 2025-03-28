# ino A
"""
    1. defining some classes for
        1.1. PMT social theory
        1.2. SCT social theory
        1.3. agents
        1.4. water resource (API)
        1.5. quality
    2. Test Scenarios
        3.1. define scenarios
        3.2. test scenario
"""

import random
import draw as draw

# 1. defining a class for usres
# 1.1. PMT social theory

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

# 1.2. SCT social theory
class SCTSocialParameters:
        performanceAccomplishment = 0.0
        emotionalArousal = 0.0
        VicariousLearning = 0.0
        socialPersuation = 0.0
        # results:
        approachAndAvoidance = 0.0
        performance = 0.0
        persistence = 0.0
        

class Crop:
    Type = 1
    Yield = random.uniform(0.3, 0.5)
    sellPrice = 200
    cultivationCost = 100
    waterDemand = 100
    def __init__(self):
        self.Type = 1
        self.Yield = random.uniform(0.3, 0.5)
        self.sellPrice = 200
        self.cultivationCost = 100
    @staticmethod
    def create():
        obj = Crop()
        return obj


# 1.3. Agents
class Agent:
    agentType = 1  # 1: proactive, 2: interactive, 3: bounded rational, 4: preceptive
    typeOfUsing = 1 # 1: agricultural, 2: industrial, 3: municipal
    farmlandCoordinates = [(100, 100), (200, 100), (200, 200), (100, 200)]
    area = -1
    shape = draw.Shape()
    pmtSubSocialParameters = PMTSubSocialParameters()
    lastCrop = Crop()
    newCrop = Crop()
    def __init__(self, agentType = None, typeOfUsing = None, farmlandCoordinates = None):
        if agentType != None:
            self.agentType = agentType
        if typeOfUsing != None:
            self.typeOfUsing = typeOfUsing
        if farmlandCoordinates != None:
            self.shape.coordinates = farmlandCoordinates
    
    @staticmethod
    def create():
        obj = Agent()
        return obj
    # def socialFactor (self):
    #     return(round(random.uniform((self.agentType-1)*0.25, self.agentType*0.25), 2))
    def ProbabilityOfLegalCompliance(self, method="PMT"): # a nubmer between 0 and 1 
        if (method == "PMT"):
            pmtSocialParameters = PMTSocialParameters()
            pmtSocialParameters.calculateParameters(self.pmtSubSocialParameters)
            return(pmtSocialParameters.pmtSocialFactor)
        else:
            return(0)

    def premittedCrops(self, scenario, crops):
        premittedWaterUsage =  scenario.groundWaterPumpingLimit
        premitArray = [False] * len(crops)
        for i in range(len(crops)): # all of crop types
            if (crops[i].waterDemand <= premittedWaterUsage):
                premitArray[i] = True
        return premitArray

             
    def ChooseNewCrop(self, probabilityOfLegalCompliance, scenario, annualInterestYear, crops):
        newCropIndex = 0
        premittedCrop = [True]*len(crops)
        status = random.choices(["lawAbiding", "lawBreaker"], weights=[probabilityOfLegalCompliance, (1-probabilityOfLegalCompliance)])[0]
        if status == "lawAbiding":
            premittedCrop = premittedCrops(scenario, crops)
        # last crop nb:
        lastCost = (self.lastCrop.waterDemand + self.lastCrop.cultivationCost) * (1/self.lastCrop.Yield)
        lastIncome = self.lastCrop.sellPrice
        lastNb = lastIncome - lastCost
        maxDiff = 0
        for i in range(len(crops)): # all of crop types
            if (premittedCrop[i]):
                cost =  (crops[i].waterDemand + crops[i].cultivationCost) * (1/crops[i].Yield)
                income = crops[i].sellPrice
                nb = income - cost
                if (maxDiff < (nb-lastNb)):
                    newCropIndex = i
                    maxDiff = nb - lastNb
        
        self.lastCrop = self.newCrop
        self.newCrop = crops[newCropIndex]


            

    def decision(self, scenario, annualInterestYear, crops):
        # calculate social factor
        probabilityOfLegalCompliance = ProbabilityOfLegalCompliance("PMT")
        # adding economic factor
        self.ChooseNewCrop(probabilityOfLegalCompliance, scenario, annualInterestYear, crops)

# 1.3.1. agents functions
def drawAllFarmlands(agents):
    shapes = [draw.Shape.create() for _ in range(len(agents))]
    for i in range(len(agents)):
        shapes[i].coordinates = agents[i].shape.coordinates
        if (agents[i].newCrop.Type == 0):
            agents[i].shape.color = (0, 0, 255)
        elif (agents[i].newCrop.Type == 1):
            agents[i].shape.color = (255, 0, 0)
        elif (agents[i].newCrop.Type == 2):
            agents[i].shape.color = (0, 255, 0)
        elif (agents[i].newCrop.Type == 3):
            agents[i].shape.color = (0, 255, 255)
        elif (agents[i].newCrop.Type == 4):
            agents[i].shape.color = (255, 255, 0)
        else:
            agents[i].shape.color = (255, 0, 255)
        shapes[i].color = agents[i].shape.color
    draw.draw_agents(shapes)
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
        agent = Agent(agentType, typeOfUsing,[(100, 100), (200, 100), (200, 200), (100, 200)])
        agents.append(agent)

    return agents



# 1.4. water resource (API)
# 1.4.1. Define the water resource
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
    groundWaterPumpingLimit = 100 # usage per area

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


if __name__ == "__main__":
    scenario1 = Scenario()
    agents = makeAPopulation(10)
    #shape = draw.Shape("1", [(100, 100), (200, 100), (200, 200), (100, 200)])
    #shape.draw_closed_shape(color=(255, 0, 0))

    # Agent 1
    #agent1 = Agent(1, 1, [(100, 100), (200, 100), (200, 200), (100, 200)])
    #agent1.shape.draw_closed_shape()

    crops = [Crop.create() for _ in range(6)]
    for i in range(6):
        crops[i].Type = i
        crops[i].Yield = random.uniform(0.3, 0.5)
        crops[i].sellPrice = random.randint(100, 300)
        crops[i].cultivationCost = crops[i].sellPrice*0.6
        crops[i].waterDemand = random.randint(50, 250) # per area

    # agents array
    agents = [Agent.create() for _ in range(25)]
    bSquare = 100
    xStart = 0
    yStart = 0
    offset = 10
    farmNo = 0
    for farmNo in range(len(agents)):
        agents[farmNo].agentType = 1
        agents[farmNo].typeOfUsing = 1
        x1 = (farmNo%5)*(bSquare + offset)
        y1 = round(farmNo//5)*(bSquare + offset)
        x2 = x1 + bSquare
        y2 = y1 + bSquare
        agents[farmNo].shape = draw.Shape()
        agents[farmNo].shape.coordinates = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
        agents[farmNo].shape.color = (255, 0, 0)
        agents[farmNo].shape.calculateArea()
        agents[farmNo].newCrop = Crop()
        cropType = random.randint(0, 5)
        agents[farmNo].newCrop = crops[cropType]
        agents[farmNo].lastCrop = agents[farmNo].newCrop
    
    annualInterestYear = 0.6

    #draw.test()
    drawAllFarmlands(agents)

    print(123)