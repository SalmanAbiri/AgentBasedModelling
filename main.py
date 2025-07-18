# ino A
"""
    1. defining some classes for
        1.1. PMT social theory
        1.2. SCT social theory
        1.3. agents
        1.4. water resource (API)
        1.5. water quality
    2. Test Scenarios
        3.1. define scenarios
        3.2. test scenario
"""


import random
import draw as draw
import pandas as pd


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
    def __init__(self, Type=1, Yield=None, sellPrice=200, cultivationCost=100, waterDemand=100):
        self.Type = Type
        self.Yield = Yield if Yield is not None else random.uniform(0.3, 0.5)
        self.sellPrice = sellPrice
        self.cultivationCost = cultivationCost
        self.waterDemand = waterDemand

    @staticmethod
    def create_from_dict(data):
        return Crop(
            Type=data.get('Type', 1),
            Yield=data.get('Yield', None),
            sellPrice=data.get('sellPrice', 200),
            cultivationCost=data.get('cultivationCost', 100),
            waterDemand=data.get('waterDemand', 100)
        )


# 1.3. Agents
class Agent:
    def __init__(self, agentType=1, typeOfUsing=1, farmlandCoordinates=None, area=-1,
                 lastCrop=1, newCrop=1):
        self.agentType = agentType
        self.typeOfUsing = typeOfUsing
        self.farmlandCoordinates = farmlandCoordinates or [(100, 100), (200, 100), (200, 200), (100, 200)]
        self.area = area
        self.shape = draw.Shape()
        self.shape.coordinates = self.farmlandCoordinates
        self.pmtSubSocialParameters = PMTSubSocialParameters()
        self.lastCrop = lastCrop
        self.newCrop = newCrop

    @staticmethod
    def create_from_dict(data):
        # Safely evaluate farmlandCoordinates if stored as a string
        coords = eval(data.get("farmlandCoordinates")) if "farmlandCoordinates" in data else None
        return Agent(
            agentType=data.get("agentType", 1),
            typeOfUsing=data.get("typeOfUsing", 1),
            farmlandCoordinates=coords,
            area=data.get("area", -1),
            lastCrop=data.get("lastCrop", 1),
            newCrop=data.get("newCrop", 1)
        )

    def ProbabilityOfLegalCompliance(self, method="PMT"):
        if method == "PMT":
            pmtSocialParameters = PMTSocialParameters()
            pmtSocialParameters.calculateParameters(self.pmtSubSocialParameters)
            return pmtSocialParameters.pmtSocialFactor
        else:
            return 0

    def permittedCrops(self, scenario, crops):
        permittedWaterUsage = scenario.groundWaterPumpingLimit
        return [crop.waterDemand <= permittedWaterUsage for crop in crops]

    def ChooseNewCrop(self, probabilityOfLegalCompliance, scenario, annualInterestYear, crops):
        status = random.choices(
            ["lawAbiding", "lawBreaker"],
            weights=[probabilityOfLegalCompliance, 1 - probabilityOfLegalCompliance]
        )[0]

        permittedCrop = [True] * len(crops)
        if status == "lawAbiding":
            permittedCrop = self.permittedCrops(scenario, crops)

        # Compare net benefits
        lastCost = (self.lastCrop.waterDemand + self.lastCrop.cultivationCost) * (1 / self.lastCrop.Yield)
        lastIncome = self.lastCrop.sellPrice
        lastNb = lastIncome - lastCost

        maxDiff = float('-inf')
        newCropIndex = 0
        for i, crop in enumerate(crops):
            if permittedCrop[i]:
                cost = (crop.waterDemand + crop.cultivationCost) * (1 / crop.Yield)
                income = crop.sellPrice
                nb = income - cost
                if nb - lastNb > maxDiff:
                    newCropIndex = i
                    maxDiff = nb - lastNb

        self.lastCrop = self.newCrop
        self.newCrop = crops[newCropIndex]

    def decision(self, scenario, annualInterestYear, crops):
        compliance = self.ProbabilityOfLegalCompliance("PMT")
        self.ChooseNewCrop(compliance, scenario, annualInterestYear, crops)

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

    # Read the Excel file
    data = pd.read_excel("inputs.xlsx", sheet_name=["crops", "agents"])

    # Create Crop objects
    crop_df = data["crops"]
    crops = [Crop.create_from_dict(row._asdict()) for row in crop_df.itertuples(index=False)]

    # Example: print all crops
    for crop in crops:
        print(vars(crop))

    # Agent objects
    agent_df = data["agents"]
    agents = [Agent.create_from_dict(row._asdict()) for row in agent_df.itertuples(index=False)]


    bSquare = 100
    xStart = 0
    yStart = 0
    offset = 10
    farmNo = 0
    for farmNo in range(len(agents)):
        # agents[farmNo].agentType = 1
        # agents[farmNo].typeOfUsing = 1
        # x1 = (farmNo%5)*(bSquare + offset)
        # y1 = round(farmNo//5)*(bSquare + offset)
        # x2 = x1 + bSquare
        # y2 = y1 + bSquare
        # agents[farmNo].shape.coordinates = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
        # agents[farmNo].newCrop = Crop()
        # cropType = random.randint(0, 5)
        # agents[farmNo].newCrop = crops[cropType]
        # agents[farmNo].lastCrop = agents[farmNo].newCrop
        agents[farmNo].shape = draw.Shape()
        agents[farmNo].shape.color = (255, 0, 0)
        agents[farmNo].shape.calculateArea()
    
    annualInterestYear = 0.6

    #draw.test()
    drawAllFarmlands(agents)

    print(123)