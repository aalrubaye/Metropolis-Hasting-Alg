import Estimator
import numpy as np
import matplotlib.pyplot as plt

sum_of_means = 0
sum_of_acceptance_ratio = 0
number_of_iterations = 1
array_x = []


def f(x):
    return np.exp(-x**2)


def g(x):
    return np.exp(-x**4)


def h(x):
    return np.exp(-x**8)


# estimate the next x based on a walk length only
def next_point_estimator(x, walk_length):
    return np.random.normal(x, walk_length)


# estimate the next x based on involving the mean of the current distribution and a walk length
def next_point_estimator_mean_involved(x, walk_length, mean):
    x_next = np.random.normal(x, walk_length)
    if x_next < 0:
        x_next += mean
    else:
        x_next -= mean
    return x_next


def find_random_walk_length(n):
    a = []
    for i in range(0, n-1):
        a.append(np.random.uniform(low=0.01, high=100))
    return a


def find_walk_length(walk_type,n):
    switcher = {
        1: 1.,
        2: 0.01,
        3: 100,
        4: find_random_walk_length(n),
        5: 1.,
        6: 0.01,
        7: 100,
        8: find_random_walk_length(n)
    }
    return switcher.get(walk_type, "Invalid entry")


def main(walk_type):
    global sum_of_means, sum_of_acceptance_ratio, array_x

    # N is the number of iterations that is considered to produce the desired distribution
    N = 100000
    x = np.arange(N, dtype=np.float)

    x[0] = 0.2

    counter = 0
    sum = 0

    walk_length = find_walk_length(walk_type.value, N)

    for i in range(0, N-1):

        # finds the next x based on the walk type and the walk length
        if (walk_type == Estimator.WalkType.FWL_m) or (walk_type == Estimator.WalkType.SWL_m) or (walk_type == Estimator.WalkType.LWL_m):
            x_next = next_point_estimator_mean_involved(x[i], walk_length, sum/float(N))
        elif walk_type == Estimator.WalkType.RWL_m:
            x_next = next_point_estimator_mean_involved(x[i], walk_length[i], sum/float(N))
        elif walk_type == Estimator.WalkType.RWL:
            x_next = next_point_estimator(x[i], walk_length[i])
        else:
            x_next = next_point_estimator(x[i], walk_length)

        if np.random.random_sample() < min(1, f(x_next)/f(x[i])):
            x[i+1] = x_next
            counter = counter + 1
        else:
            x[i+1] = x[i]
        sum += x[i+1]

    array_x = x

    # sum_of_means += sum/float(N)
    sum_of_means += np.mean(x)
    sum_of_acceptance_ratio += counter/float(N)
    x = []


def generate_desired_ditribution(walk_type, plot_index):
    global sum_of_means, number_of_iterations, sum_of_acceptance_ratio

    for i in range(0, number_of_iterations):
        main(walk_type)

    print walk_type
    avg_mean = str(float(sum_of_means)/float(number_of_iterations))
    avg_acceptance_ratio = str(float(sum_of_acceptance_ratio)/float(number_of_iterations))
    print 'mean = ' + avg_mean
    print 'Acceptance Ratio= ' + avg_acceptance_ratio
    print ('-'*100)

    sum_of_means = 0
    sum_of_acceptance_ratio = 0

    plt.subplot(2, 1, plot_index)
    plt.hist(array_x, bins=50)
    plt.title(str(walk_type))


if __name__ == '__main__':

    plt.figure(figsize=(16,10))
    plt.subplots_adjust(wspace=0.4, hspace=0.3)

    generate_desired_ditribution(Estimator.WalkType.FWL,1)

    generate_desired_ditribution(Estimator.WalkType.SWL,2)

    generate_desired_ditribution(Estimator.WalkType.LWL,3)

    generate_desired_ditribution(Estimator.WalkType.RWL,4)

    generate_desired_ditribution(Estimator.WalkType.FWL_m,5)

    generate_desired_ditribution(Estimator.WalkType.SWL_m,6)

    generate_desired_ditribution(Estimator.WalkType.LWL_m,7)

    generate_desired_ditribution(Estimator.WalkType.RWL_m,8)

    plt.show()


