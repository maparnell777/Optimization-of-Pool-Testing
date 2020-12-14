# A stab at the pool testing method
# Question: Given an initial (positive) pool (sized 2 - 50), how best to test all members within two days?

import matplotlib.pyplot as plt
import math
import random


#REQUIRES n to be even
def find_expected_2(n, num_infected):
    expected_sum = 0
    for iteration in range(300):
        # print("iteration")
        #Initialize list to false
        people = [False for i in range(n)]
        #Set values of infected people randomly to True
        for i in range(num_infected):
            # print(i)
            rand = random.randrange(n)
            # print(rand)
            # print(people)
            while (people[rand]):
                # print(rand)
                # print(people)
                rand = random.randrange(n)
            people[rand] = True
        # Pair up adjacent values
        num_infect_groups = 0
        for j in range(0,n,2):
            if (people[j] or people[j+1]):
                num_infect_groups += 1
        expected_sum += num_infect_groups
    return expected_sum/300
#REQUIRES n to be a multiple of 3
def find_expected_3(n, num_infected):
    expected_sum = 0
    for iteration in range(300):
        # print("iteration")
        #Initialize list to false
        people = [False for i in range(n)]
        #Set values of infected people randomly to True
        for i in range(num_infected):
            # print(i)
            rand = random.randrange(n)
            # print(rand)
            # print(people)
            while (people[rand]):
                # print(rand)
                # print(people)
                rand = random.randrange(n)
            people[rand] = True
        # Pair up adjacent values
        num_infect_groups = 0
        for j in range(0,n,3):
            if (people[j] or people[j+1] or people[j+2]):
                num_infect_groups += 1
        expected_sum += num_infect_groups
    return expected_sum/300
#REQUIRES n to be a multiple of 4
def find_expected_4(n, num_infected):
    expected_sum = 0
    for iteration in range(300):
        # print("iteration")
        #Initialize list to false
        people = [False for i in range(n)]
        #Set values of infected people randomly to True
        for i in range(num_infected):
            # print(i)
            rand = random.randrange(n)
            # print(rand)
            # print(people)
            while (people[rand]):
                # print(rand)
                # print(people)
                rand = random.randrange(n)
            people[rand] = True
        # Pair up adjacent values
        num_infect_groups = 0
        for j in range(0,n,4):
            if (people[j] or people[j+1] or people[j+2] or people[j+3]):
                num_infect_groups += 1
        expected_sum += num_infect_groups
    return expected_sum/300

pool_sizes_2 = range(4, 51, 2) #4-50
scatterx_2 = []
scattery_2 = []
avg_test_ratio_2 = [] #Will eventually line up with 2-50
for n in pool_sizes_2:
    #testing_ratios = []
    ratio_sum = 0
    '''
    for num_infected in range(1, n//2 + 1):
        #Initial Method
        # total_test = n // 2
        # #Can redo this part if we ever model over 50% positive
        # if num_infected <= n/2:
        #     total_test += (num_infected * 2)
        # else:
        #     total_test += n
        # ratio_sum += total_test / n  # tests/n, which gives testing ratio

        #Potential probability model
        #Find expected value of tests used
        #Find a list of possible number of positive groups (distribution)
        #distribution = range(math.ceil(num_infected/2), num_infected+1)
        #Using this list, find a corresponding probability for each distribution
        #Using both lists, find expected value by summing the products of each corresponding index

        total_test = n // 2
        # Average expected value
        expected_pos_groups = find_expected_2(n, num_infected)
        total_test += expected_pos_groups * 2
        ratio_sum += total_test / n  # tests/n, which gives testing ratio
        #Add to scatter plot points
        scatterx_2.append(n)
        scattery_2.append(total_test / n)
    '''
    scatterx_2.append(n)
    #Calculate testing ratio for one infected
    total_test = n // 2 + 2
    scattery_2.append(total_test/n)
	#Find average testing ratio, add to list
    avg_test_ratio_2.append(ratio_sum/len(range(1, n//2 + 1)))

pool_sizes_3 = range(6, 51, 6) #4-50
avg_test_ratio_3 = [] #Will eventually line up with 2-50
scatterx_3 = []
scattery_3 = []
for n in pool_sizes_3:
    #testing_ratios = []
    ratio_sum = 0
    '''
    for num_infected in range(1, n//2 + 1):
        total_test = n // 3
        # Average expected value
        expected_pos_groups = find_expected_3(n, num_infected)
        total_test += expected_pos_groups * 3
        ratio_sum += total_test / n  # tests/n, which gives testing ratio
        # Add to scatter plot points
        scatterx_3.append(n)
        scattery_3.append(total_test / n)
    '''
    scatterx_3.append(n)
    #Calculate testing ratio for one infected
    total_test = n // 3 + 3
    scattery_3.append(total_test/n)
	#Find average testing ratio, add to list
    avg_test_ratio_3.append(ratio_sum/len(range(1, n//2 + 1)))

pool_sizes_4 = range(8, 51, 4) #4-50
avg_test_ratio_4 = [] #Will eventually line up with 2-50
scatterx_4 = []
scattery_4 = []
for n in pool_sizes_4:
    ratio_sum = 0
    '''
    for num_infected in range(1, n//2 + 1):
        total_test = n // 4
        # Average expected value
        expected_pos_groups = find_expected_4(n, num_infected)
        total_test += expected_pos_groups * 4
        ratio_sum += total_test / n  # tests/n, which gives testing ratio
        # Add to scatter plot points
        scatterx_4.append(n)
        scattery_4.append(total_test / n)
    '''
    scatterx_4.append(n)
    #Calculate testing ratio for one infected
    total_test = n // 4 + 4
    scattery_4.append(total_test/n)
	#Find average testing ratio, add to list
    avg_test_ratio_4.append(ratio_sum/len(range(1, n//2 + 1)))

#Initialize list of points - list of lists
points = []
UPPER = 9
#Run through a loop of n_prime sizes
for n_prime in range(2, UPPER + 1):
    pool_sizes = range(n_prime*2, 51, n_prime)
    scatterx = []
    scattery = []
    for n in pool_sizes: #Scaling along the x axis
        #assuming only 1 infected
        scatterx.append(n) #x val
        # Calculate testing ratio for one infected
        total_test = (n // n_prime) + n_prime
        scattery.append(total_test / n)
    points.append([scatterx, scattery])

# # Plotting:
# # Plot the average testing ratios in a line (connected scatter plot)
# # n vs testing ratios
# plt.plot(pool_sizes_2, avg_test_ratio_2)
# plt.plot(pool_sizes_3, avg_test_ratio_3)
# plt.plot(pool_sizes_4, avg_test_ratio_4)
# plt.show()
#
# # Plot the scatter
# plt.scatter(scatterx_2, scattery_2)
# plt.scatter(scatterx_3, scattery_3)
# plt.scatter(scatterx_4, scattery_4)
# plt.show()

#Plot each set of points in points
for n_prime in range(UPPER-1):
    plt.plot(points[n_prime][0], points[n_prime][1], label=n_prime+2)
plt.xlabel("Pool Size (n, # people in pool)")
plt.ylabel("Average Testing Ratio, Tests Used Per Pool Size (%)")
plt.legend(loc="upper right")
plt.show()