# ino A

import random
from numpy.random import choice
from copy import deepcopy
import matplotlib.pyplot as plt # importing a plotting library

# This program contains these steps:
# Make Agent - creating an agent that has a vowel and a personality
# Make Population - creating a population of agents using the function in (1)
# Count - counting the proportion of agents with the same vowel in the population created by (2)
# Choose Pair - choosing two agents out of the population created in (2)
# Interact - implementing the interaxction between the two agents chosen in (4)
# Simulatoin
# Show results




def make_agent(vowel, personality):
    return [vowel, personality]


# Create a function that generates a population of N identical agents with given parameters
def make_population(N):
    
    population = []
    
    for i in range(N):
        
        v = random.randint(0,1)
        
        p = random.randint(0,1)
        
        agent = make_agent(vowels[v], personalities[p])
        
        population.append(agent)

    return population

# Create a function that calculates the proportion of agents with the variant 'a' in the population
def count(population):
    t = 0. # must be a float!     
    for agent in population:
        if agent[0] == 'a':
            t += 1            # The syntax =+ Adds 1 to t (or: t = t + 1)
    return t / len(population)


def choose_pair(population):
    i = random.randint(0, len(population) - 1) # phyton counts from 0, so pop(8) is an error
    j = random.randint(0, len(population) - 1)
    
    while i == j:
        j = random.randint(0, len(population) - 1) # make sure the same agent is not selected twice
        
    return population[i], population[j]


# Create a function that only updates agents using "pass" (which means do nothing in Python)

def interact(listener,producer): 
    
    if listener[0] == producer[0]:
        pass   # do nothing
    else:
        if listener[1]=='S':
            pass
        else:
            listener[0]=deepcopy(producer[0])

def simulate(n, k):
    
    population = make_population(n)
    
    # print("Initial Population:", population)
    
    proportion = [] # make an empty list to keep track of the porportions after every interaction
    
    for i in range(k):
        
        pair = choose_pair(population) # choose a pair from the population
        
        interact(pair[0],pair[1])  # make the chosen pair interact
        
        proportion.append(count(population)) # track the proportion of the vowels in the population during intrtaction
    
    return population, proportion

# Create a function that runs s simulations of a community of size N interacting randomly for K times    
def batch_simulate(n,k,s):
    batch_proportions=[]
    for i in range(s):
        new_population, proportion = simulate(n, k)
        batch_proportions.append(proportion)
    return batch_proportions


# Setting the parameters
vowels = ['a', 'i']
personalities = ['F', 'S'] # F= Flexible, S=Stubborn

# Simulate 500 interctions between 20 agents 
new_population, proportion = simulate(20, 500)
print("Final Population:", new_population)
plt.plot(proportion)

# and add some details to the plot
plt.title('Changes in the proportion of [a] over time')
plt.ylabel('Proportion [a] users')
plt.xlabel('Time [No. of interactions]')
plt.ylim(0,1)
plt.show()

plt.figure()
# Make 20 simulations of 5000 interctions between 200 agents 
results = batch_simulate(200,5000,20)
plt.ylim(0,1)

for i in results:
    plt.plot(i)
plt.show()