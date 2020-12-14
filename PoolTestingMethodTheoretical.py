import random
import math
import matplotlib.pyplot as plt

def find_expected_n(pop, num_infected, n):
    '''
    Stochastic simulation to find the number of infected groups given a population size,
    a number of infected people, and the group size given that the entire population is
    being divided into groups of the given size.
    :param pop: Population size
    :param num_infected: Number of people infected people within the population
    :param n: Pool size; split the entire population into groups of this size
    :return: The expected number of pools (of size n) which should test positive (may not be a whole number
    since it is the average of several stochastic simulations)
    '''
    expected_sum = 0
    iterations = 100
    for iteration in range(iterations):
        #Initialize list to false
        people = [False for i in range(pop)]
        #Set values of infected people randomly to True
        for i in range(num_infected):
            rand = random.randrange(pop)
            while (people[rand]):
                rand = random.randrange(pop)
            people[rand] = True
        # Identify num of infected groups
        num_infect_groups = 0
        for j in range(0,pop,n):
            infected = False
            for k in range(j, j+n):
                if k < pop:
                    if people[k]:
                        infected = True
            if infected:
                num_infect_groups += 1
        expected_sum += num_infect_groups
    return expected_sum/iterations

def find_expected_n_float(pop, num_infected, n):
    '''
    Stochastic simulation to find the number of infected groups given a population size,
    a number of infected people, and the group size given that the entire population is
    being divided into groups of the given size. Same as previous method, but it is capable
    of taking in a float as the number of infected people, so it takes longer to run.
    :param pop: Population size
    :param num_infected: Number of people infected people within the population
    :param n: Pool size; split the entire population into groups of this size
    :return: The expected number of pools (of size n) which should test positive (may not be a whole number
    since it is the average of several stochastic simulations)
    '''
    expected_sum = 0
    iterations = 100
    percent_infected = num_infected/pop
    for iteration in range(iterations):
        #Initialize list to false arbitrarily
        people = [False for i in range(pop)]
        #Evaluate each person - let them be infected with a probabilty that matched the percent infected
        for i in range(len(people)):
            rand = random.uniform(0,1)
            if rand <= percent_infected:
                people[i] = True
        # Identify num of infected groups
        num_infect_groups = 0
        for j in range(0,pop,n):
            infected = False
            for k in range(j, j+n):
                if k < pop:
                    if people[k]:
                        infected = True
            if infected:
                num_infect_groups += 1
        expected_sum += num_infect_groups
    return expected_sum/iterations

# Population
people = 1000
p_vals = []
cost_vals = []
n_vals = []
n_prime_vals = []
master = {}
for num_infected in range(1, (people//4)+ 1):
    p_vals.append((num_infected/people)*100) #percentage people infected
    # Stochastically check each pool size to find the best pool size
    bestn = 1
    bestn_cost = people
    bestn_prime_outer = 1
    for n in range(1, 51):
        # Find the number of pools expected to return positive (based on n size and number of people infected)
        num_infected_pools = find_expected_n(people, num_infected, n)
        #Calculate on average how many infected people in each pool
        '''
        num_infected_in_group = round(num_infected/num_infected_pools) #some weird float
        #Make sure it isn't 0
        if num_infected_in_group == 0:
            num_infected_in_group = 1
        '''
        num_infected_in_group = num_infected / num_infected_pools
        #At this point, we will consider one uniform group (n) with a uniform num infected people (num_infected_in_group)

        #Find range of possible n_prime values capped at 8 (what's reasonable)
        n_prime_max = 8
        if n_prime_max > n:
            n_prime_max = n
        #Initialize best cost for subgroup to be n_prime is 1, test each individual
        bestn_prime = 1
        bestn_prime_cost = people
        for n_prime in range(2, n_prime_max+1):
            # Determine stochastically how many tests it will take to
            # Test each individual, given a definite num_infected_in_group, n_prime, and n

            #First, find the expected number of subpools that are infected
            num_infected_subpools = find_expected_n_float(n, num_infected_in_group, n_prime)

            #Now we know how many infected pools we have, how many infected subpools we have assuming
            #each pool acts the same, and n_prime. Calculate total number of testing cost for everyone
            test_cost = math.ceil(people/n) #First level pooling
            test_cost +=  num_infected_pools * math.ceil(n/n_prime)#Second level pooling
            test_cost += num_infected_subpools * n_prime * num_infected_pools #Third level pooling
            if test_cost < bestn_prime_cost:
                bestn_prime_cost = test_cost
                bestn_prime = n_prime
        if bestn_prime_cost < bestn_cost:
            bestn_cost = bestn_prime_cost
            bestn = n
            bestn_prime_outer = bestn_prime
    cost_vals.append(bestn_cost)
    n_vals.append(bestn)
    n_prime_vals.append(bestn_prime_outer)
    master[num_infected] = ["Cost", bestn_cost, "N", bestn, "N Prime", bestn_prime_outer]

print(master)
#Normal pool testing
pool_size = 10
old_cost_vals = [] #Old meaning using the old method - single level pooling with static pool size
for num_infected in range(1, (people//4) + 1):
    # p_vals.append(num_infected/people) #percentage people infected
    num_infected_pools = find_expected_n(people, num_infected, pool_size)
    total_cost = math.ceil(people/pool_size)
    total_cost += num_infected_pools*pool_size
    old_cost_vals.append(total_cost)

#Plot the scatter
# p_vals = [1,2,3]
# n_prime_vals = [1,2,3]
# n_vals = [1,2,3]
# cost_vals = [1,2,3]
plt.scatter(p_vals, n_vals, label = "Best N")
plt.xlabel("Percent Infected (%)")
plt.ylabel("Best N Value (Pool Size)")
plt.legend(loc="upper right")
plt.show()

plt.scatter(p_vals, n_prime_vals, label = "Best N Prime")
plt.xlabel("Percent Infected (%)")
plt.ylabel("Best N Prime Value (Subpool Size)")
plt.legend(loc="upper right")
plt.show()

plt.scatter(p_vals, cost_vals, label = "Testing Cost with Subpools")
plt.xlabel("Percent Infected (%)")
plt.ylabel("Testing Cost for Population of 1000 (# Tests)")
plt.legend(loc="upper right")
plt.show()

# Comparing testing cost of single level static pooling and double level dynamic pooling
plt.scatter(p_vals, cost_vals, label = "Testing Cost with Subpools/Dynamic N Values")
plt.scatter(p_vals, old_cost_vals, label = "Testing Cost without Subpools/Static N Values")
plt.scatter(p_vals, cost_vals, label = "")
plt.xlabel("Percent Infected (%)")
plt.ylabel("Testing Cost for Population of 1000 (# Tests)")
plt.legend(loc="upper right")
plt.show()

#Calculating/plotting this difference between old and new testing methods
difference = []
for i in range(len(p_vals)):
    difference.append(old_cost_vals[i] - cost_vals[i])

plt.scatter(p_vals, difference, label = "Cost Savings With New Method")
plt.xlabel("Percent Infected (%)")
plt.ylabel("Cost Saving for Population of 1000 (# Tests)")
plt.legend(loc="upper right")
plt.show()