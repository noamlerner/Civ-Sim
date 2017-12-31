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
        civ = np.random.randint(1,num_civs)
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
    civ.affinity_decay()

def world_stats(world,i, c):
    stats_dict = {}
    size = len(np.where(world != 0)[0])
    print "Civilizations for year: " + str(i)
    print "-------------------------"
    civs = c.stats()
    stats_dict['civs'] = {}
    for j in range(1,c.num_civs):
        population = len(np.where(world == j)[0])
        if population == 0:
            continue
        stats_dict[j] = float(population) / size
        if float(population) / size > 0.1:
            stats_dict['civs'][j] = civs[j]
            print "\tCivilization " + str(j)
            for k in civs[j].keys():
                print "\t\t" + k + ":\t" + str(civs[j][k])
            print "\t\tPopulation: " + str(population)
            print "\t\tRelaitve Population: " + str(stats_dict[j])
    print "Averages for year: " + str(i)
    print "-------------------------"
    average_stats = {}
    civkeys = civs.keys()
    if len(civkeys) == 0:
        print "They Dont Killed Themselves"
        return
    print "Number of Civs: " + str(len(civkeys))
    for k in civs[civkeys[0]].keys():
        av = 0
        for j in stats_dict.keys():
            if j == 'civs': continue
            av += civs[j][k] * stats_dict[j]
        print "\tAverage " + k + ": " + str(av)
        average_stats[k] = av
    stats_dict['averages'] = average_stats
    return stats_dict

def simulate():
    N = 1000
    c = civs(N)
    c.init_rand_civs(10)
    world = create_world(N)
    rand_populate_world(world,c.num_civs,100,0.25)
    for i in range(1000000):
        print "Year " + str(i)
        move_world(world,c)
        if i % 100 == 0:
            stats = world_stats(world,i,c)
            for i in range(c.num_civs):
                if i in stats and stats[i] > 0.95:
                    print "Civ " + str(i) + " won this one"
                    stats['civs'] = stats['civs'][i]
                    return stats
    stats = world_stats(world,10000,c)
    return stats

def n_simulate(N):
    stats = []
    for i in range(N):
        stats.append(simulate())
    print " Done "
    print '----------------\n----------------\n----------------\n----------------'
    print stats

n_simulate(1)



