# Simulation representing the usage of the created testing method in a
# Every certain number of results, the expected p value is updated
import random
import math
import matplotlib.pyplot as plt

#Change these to change the simulation
# p_estimate = 0.05
# p_actual = 0.08
population = 1000
n_max = 50
static_pool_size = 10 #Static pool size for comparison against optimized method
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

def find_best_pool_size(people, p_estimate):
    num_infected = round(p_estimate*people)
    bestn = 1
    bestn_cost = people
    bestn_prime_outer = 1
    for n in range(1, n_max+1):
        # Find the number of pools expected to return positive (based on n size and number of people infected)
        num_infected_pools = find_expected_n(people, num_infected, n)
        # Calculate on average how many infected people in each pool
        '''
        num_infected_in_group = round(num_infected/num_infected_pools) #some weird float
        #Make sure it isn't 0
        if num_infected_in_group == 0:
            num_infected_in_group = 1
        '''
        num_infected_in_group = num_infected / num_infected_pools #float
        # At this point, we will consider one uniform group (n) with a uniform num infected people (num_infected_in_group)

        # Find range of possible n_prime values capped at 8 (what's reasonable)
        n_prime_max = 8
        if n_prime_max > n:
            n_prime_max = n
        # Initialize best cost for subgroup to be n_prime is 1, test each individual
        bestn_prime = 1
        bestn_prime_cost = people
        for n_prime in range(2, n_prime_max + 1):
            # Determine stochastically how many tests it will take to
            # Test each individual, given a definite num_infected_in_group, n_prime, and n

            # First, find the expected number of subpools that are infected
            num_infected_subpools = find_expected_n_float(n, num_infected_in_group, n_prime)

            # Now we know how many infected pools we have, how many infected subpools we have assuming
            # each pool acts the same, and n_prime. Calculate total number of testing cost for everyone
            test_cost = math.ceil(people / n)  # First level pooling
            test_cost += num_infected_pools * math.ceil(n / n_prime)  # Second level pooling
            test_cost += num_infected_subpools * n_prime * num_infected_pools  # Third level pooling
            if test_cost < bestn_prime_cost:
                bestn_prime_cost = test_cost
                bestn_prime = n_prime
        if bestn_prime_cost < bestn_cost:
            bestn_cost = bestn_prime_cost
            bestn = n
            bestn_prime_outer = bestn_prime
    return bestn, bestn_prime_outer

#To use this script outside of a simulation environment, a user could use the "find_best_pool_size" function to figure out the
# best testing plan
# - They would just need to input the number of tests they have available that day/the number of tests from
#   that day that they need to process, as well as an estimate of the percentage of people infected at the time
# The function gives them "ideal" values to use for n and nprime

# Simulation creates a batch (based on population size) of fictional people who are positive or not based on p_actual
# It then runs two scenarios - one using the optimized method, and another using the standard traditional method
# It returns the cost from each of these methods

#Note: after each "batch", the p estimate can be updated as needed if desired

def simulate(population, p_estimate, p_actual):
    '''
    Creates one simulation run based on p actual, applies optimized (using best n and n prime predicted stochastically)
    and traditional method on one concrete fictional group
    :param population: batch size of tests
    :param p_estimate: estimated percent of population infected (in decimal form)
    :param p_actual: actual percent of population infected (in decimal form)
    :return: cost to test each member using optimized method, cost to test each member using traditional method
    '''
    #CREATE SIMULATION
    # Start evaluation of the optimized model on a random population - start by creating the fictional population
    #Create each individual 'actual' person
    people_list = [False for i in range(population)]
    num_infected = round(p_actual*population)
    # Infect the exact number of people to satisfy p_actual; place them randomly
    for i in range(num_infected):
        rand = random.randrange(population)
        while (people_list[rand]):
            rand = random.randrange(population)
        people_list[rand] = True

    #DECIDE PARAMETERS FOR OPTIMIZED METHOD
    #Decide which n, n prime values are ideal based on p_estimate
    n, nprime = find_best_pool_size(population, p_estimate)
    # print(n, nprime)
    #APPLY OPTIMIZED METHOD
    # Identify num of infected groups, store each of the infected groups, start to accumulate total cost
    total_cost = 0
    infected_groups_list = []
    #Skip through the population one group at a time
    for j in range(0,population,n):
        total_cost += 1
        current_group = []
        infected = False
        #Check each member in the group
        for k in range(j, j+n): # k = one person's index
            if k < population: #This check is necessary for the last group in the population - it might be out of indexing range
                current_group.append(people_list[k])
                if people_list[k]:
                    infected = True
        #Every group which is infected is added to the list of infected pools
        if infected:
            infected_groups_list.append(current_group)
    # print(len(infected_groups_list))

    #Now we have our completed list of infected groups
    #Conduct subpooling, find total cost depending on which subpools test positive
    #Check groups one at a time
    for group in infected_groups_list:
        #Skip through the list using nprime as the new pooling size
        for j in range(0,len(group), nprime):
            total_cost += 1 #Accounting one test for each subpool, positive or negative
            current_group = []
            infected = False
            # Check each group member of the subpool ( k = one person's index)
            for k in range(j, j + nprime):
                if k < len(group): #Make sure it is within range
                    current_group.append(group[k])
                    if group[k]:
                        infected = True
            if infected:
                #Account for final level testing of those in positive groups
                total_cost += len(current_group)

    #APPLY TRADITIONAL METHOD
    #To compare, find the cost to do traditional pooling methods for this SPECIFIC example
    # Identify num of infected groups, store each of the infected groups
    total_cost_old = 0
    num_infected_groups = 0
    #Skip through the population one group at a time - group size is defined statically
    for j in range(0,population,static_pool_size):
        total_cost_old += 1 #Account one test for each pool, positive or negative
        current_group = []
        infected = False
        #Check each group member
        for k in range(j, j+static_pool_size):
            if k < population:
                current_group.append(people_list[k])
                if people_list[k]:
                    infected = True
        if infected:
            #Add the cost of testing each member of a positive pool
            total_cost_old += len(current_group)
            num_infected_groups +=1
    # print(num_infected_groups)
    return total_cost, total_cost_old


# GRAPHING
# #First, we will run the simulation on varying p levels (where p actual = p estimate) to show general savings
# pvals1 = [.1, .2, .3, .4, .5, .6, .7, .8, .9, 1] # p value, in % format (better for graphing)
# pvals1_new = []
# pvals1_old = []
# for percent in pvals1:
#     percent = percent/100 #putting p values into decimal format for the simulate function
#     #Average over 3 runs
#     new_sum = 0
#     old_sum = 0
#     for i in range(3):
#         new, old = simulate(population, percent, percent) #p estimate = p actual
#         new_sum += new
#         old_sum += old
#     new_avg = new_sum/3
#     old_avg = old_sum/3
#     #Store the (averaged) costs for the new (optimized) and old (traditional) methods at corresponding indices to the
#     #associated p value (in pvals1)
#     pvals1_new.append(new_avg)
#     pvals1_old.append(old_avg)
#
# pvals2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] #in %
# pvals2_new = []
# pvals2_old = []
# for percent in pvals2:
#     percent = percent/100 #putting p values into decimal format for the simulate function
#     #Average over 3 runs
#     new_sum = 0
#     old_sum = 0
#     for i in range(3):
#         new, old = simulate(population, percent, percent) #p estimate = p actual
#         new_sum += new
#         old_sum += old
#     new_avg = new_sum/3
#     old_avg = old_sum/3
#     #Store the (averaged) costs for the new (optimized) and old (traditional) methods at corresponding indices to the
#     #associated p value (in pvals1)
#     pvals2_new.append(new_avg)
#     pvals2_old.append(old_avg)
#
# plt.scatter(pvals1, pvals1_new, label = "Optimized Approach")
# plt.scatter(pvals1, pvals1_old, label = "Traditional Approach")
# plt.xlabel("Percent Infected (%)")
# plt.ylabel("Testing Cost for Population of 1000 (# Tests)")
# plt.legend(loc="upper right")
# plt.show()
#
# plt.scatter(pvals2, pvals2_new, label = "Optimized Approach")
# plt.scatter(pvals2, pvals2_old, label = "Traditional Approach")
# plt.xlabel("Percent Infected (%)")
# plt.ylabel("Testing Cost for Population of 1000 (# Tests)")
# plt.legend(loc="upper right")
# plt.show()

#
# # #Then, to show that the optimized method is flexible, we will show the cost savings still occurs when running the
# # simulation on varying levels of discrepancy between the p_estimate and the p_actual
# # We decided to fix p_actual at .3% and 3% while varying p_estimate greatly
# pvals3 = [.1, .2, .3, .4, .5, .6, .7, .8, .9, 1] # p value, in % format (better for graphing)
# pvals3_new = []
# pvals3_old = []
# for percent in pvals3:
#     percent = percent/100 #putting p values into decimal format for the simulate function
#     #Average over 3 runs
#     new_sum = 0
#     old_sum = 0
#     for i in range(3):
#         new, old = simulate(population, percent, 0.003) #p estimate != p actual (usually)
#         new_sum += new
#         old_sum += old
#     new_avg = new_sum/3
#     old_avg = old_sum/3
#     #Store the (averaged) costs for the new (optimized) and old (traditional) methods at corresponding indices to the
#     #associated p value (in pvals1)
#     pvals3_new.append(new_avg)
#     pvals3_old.append(old_avg)
#
# pvals4 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] #in %
# pvals4_new = []
# pvals4_old = []
# for percent in pvals4:
#     percent = percent/100 #putting p values into decimal format for the simulate function
#     #Average over 3 runs
#     new_sum = 0
#     old_sum = 0
#     for i in range(3):
#         new, old = simulate(population, percent, 0.03) #p estimate != p actual (usually)
#         new_sum += new
#         old_sum += old
#     new_avg = new_sum/3
#     old_avg = old_sum/3
#     #Store the (averaged) costs for the new (optimized) and old (traditional) methods at corresponding indices to the
#     #associated p value (in pvals1)
#     pvals4_new.append(new_avg)
#     pvals4_old.append(old_avg)
#
# plt.scatter(pvals3, pvals3_new, label = "Optimized Approach")
# plt.scatter(pvals3, pvals3_old, label = "Traditional Approach")
# plt.xlabel("Estimated Percent Infected (%)")
# plt.ylabel("Testing Cost for Population of 1000 (# Tests)")
# plt.legend(loc="upper right")
# plt.show()
#
# plt.scatter(pvals4, pvals4_new, label = "Optimized Approach")
# plt.scatter(pvals4, pvals4_old, label = "Traditional Approach")
# plt.xlabel("Estimated Percent Infected (%)")
# plt.ylabel("Testing Cost for Population of 1000 (# Tests)")
# plt.legend(loc="upper right")
# plt.show()
