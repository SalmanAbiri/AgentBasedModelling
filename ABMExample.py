from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class WaterUserAgent(Agent):
    """An agent representing a water user."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.water_usage = self.random.randint(1, 10)  # Random water usage
        self.cooperation_level = self.random.uniform(0, 1)  # Cooperation level

    def step(self):
        # Adjust water usage based on cooperation level
        if self.cooperation_level > 0.5:
            self.water_usage = max(1, self.water_usage - 1)  # Use less water
        else:
            self.water_usage = min(10, self.water_usage + 1)  # Use more water
        
        # Update cooperation level based on neighbors
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
        if neighbors:
            avg_cooperation = sum([neighbor.cooperation_level for neighbor in neighbors]) / len(neighbors)
            self.cooperation_level = (self.cooperation_level + avg_cooperation) / 2

class WaterResourceModel(Model):
    """A model simulating shared water resource management."""
    def __init__(self, width, height, num_agents):
        self.num_agents = num_agents
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)

        # Create agents
        for i in range(self.num_agents):
            agent = WaterUserAgent(i, self)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

        # Data collector
        self.datacollector = DataCollector(
            agent_reporters={"WaterUsage": "water_usage", "CooperationLevel": "cooperation_level"}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

# Run the model
if __name__ == "__main__":
    model = WaterResourceModel(width=10, height=10, num_agents=50)
    for i in range(100):  # Run for 100 steps
        model.step()

    # Collect data
    agent_data = model.datacollector.get_agent_vars_dataframe()
    print(agent_data.head())
