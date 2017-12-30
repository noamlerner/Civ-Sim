import numpy as np
import matplotlib.pyplot as plt
from civ import civs

def create_world(N):
    return np.zeros((N,N)).astype(np.int64)

def rand_populate_world(world, num_civs, num_babies, restrict_to):
    N = len(world)
    middle = int(N/2)
    min_ = int(middle - N * restrict_to /2)
    choose = int(N * restrict_to)
    for i in range(num_babies):
        x = np.random.randint(choose) + min_
        y = np.random.randint(choose) + min_
        civ = np.random.randint(num_civs)
        world[x][y] = civ

def interact(world,x,y,interact_with,c):
    c.interact(world,(x,y),interact_with)

def coords(N, x,y,direction):
    if direction == 0: return (x,y)
    if direction == 1:
        if x == 0: return (x,y)
        return (x-1,y)
    if direction == 2:
        if y == 0 : return (x,y)
        return (x,y-1)
    if direction == 3:
        if x == N -1: return (x,y)
        return (x+1,y)
    if direction == 4:
        if y == N -1: return (x,y)
        return(x,y+1)


def move(world,x,y, move_to):
    if x == move_to[0] and y == move_to[1]:
        return True
    if world[move_to[0]][move_to[1]] == 0:
        world[move_to[0]][move_to[1]] = world[x][y]
        world[x][y] = 0
        return True
    return False

def move_world(world,civ):
    N = len(world)
    civs = np.where(world != 0)
    squares = range(len(civs[0]))
    np.random.shuffle(squares)
    for c in squares:
        x = civs[0][c]
        y = civs[1][c]
        direction = np.random.randint(5)
        move_to = coords(N,x,y,direction)
        succesful_move = move(world,x,y,move_to)
        if not succesful_move:
            interact(world,x,y,move_to,civ)
def world_stats(world, i, stats_dict, c):
    size = len(np.where(world != 0)[0])
    print "Civilizations for year: " + str(i)
    print "-------------------------"
    stats_dict['civs'] = c.stats()
    stats_dict[i] = {}
    for j in range(1,c.num_civs):
        population = len(np.where(world == j)[0])
        if population == 0:
            continue
        stats_dict[i][j] = population / size
        print "\tCivilization " + str(j)
        print "\t" + str(stats_dict['civs'][j])
        print "\tPopulation: " + str(population)
        print "\tRelaitve Population: " + str(population/size)
    print "Averages for year: " + str(i)
    print "-------------------------"
    average_stats = {}
    for k in stats_dict['civs'][1].keys():
        sum = 0
        num = 0
        for j in stats_dict[i].keys():
            sum += stats_dict['civs'][j][k]
            num += 1
        av = sum / num
        print "\tAverage " + k + ": " + str(av)
        average_stats[k] = av
    stats_dict['averages'] = average_stats

def simulate():
    N = 1000
    c = civs(N)
    c.init_rand_civs(10)
    world = create_world(N)
    stats = {}
    rand_populate_world(world,c.num_civs,100,0.25)
    for i in range(10000):
        move_world(world,c)
        if i % 500 == 0:
            world_stats(world,i, stats,c)
    world_stats(world,10000, stats,c)
    return stats

simulate()