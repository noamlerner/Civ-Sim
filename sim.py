import numpy as np
import matplotlib.pyplot as plt
from civ import civs

def create_world(N):
    return np.zeros((N,N)).astype(np.int64)

def rand_populate_world(world, num_civs, baby_per_civ, restrict_to):
    N = len(world)
    middle = int(N/2)
    min_ = int(middle - N * restrict_to /2)
    choose = int(N * restrict_to)
    on_civ = 1
    civ_baby_counter = 0
    while on_civ <= num_civs:
        x = np.random.randint(choose) + min_
        y = np.random.randint(choose) + min_
        world[x][y] = on_civ
        civ_baby_counter += 1
        if civ_baby_counter >= baby_per_civ:
            on_civ+=1
            civ_baby_counter = 0

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
    total_pop  = 0
    num_civs = 0
    for j in range(1,c.num_civs):
        population = len(np.where(world == j)[0])
        total_pop += population
        if population == 0:
            continue
        num_civs +=1
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
    print "Number of Civs: " + str(num_civs)
    for k in civs[civkeys[0]].keys():
        av = 0
        for j in stats_dict.keys():
            if j == 'civs': continue
            av += civs[j][k] * stats_dict[j]
        print "\tAverage " + k + ": " + str(av)
        average_stats[k] = av
    stats_dict['averages'] = average_stats
    stats_dict['total_population'] = total_pop
    print "Total Population: " + str(total_pop)
    return stats_dict

def simulate():
    N = 500
    c = civs(N)
    num_civs = int(np.random.random() * 500) + 2
    c.init_rand_civs(num_civs)
    world = create_world(N)
    rand_populate_world(world,c.num_civs, int(np.ceil(500.0/num_civs)),0.5)
    for i in range(1000000):
        move_world(world,c)
        print "Year " + str(i)
        if i % 50 == 0:
            stats = world_stats(world,i,c)
            if stats['total_population'] < 5 or i > 10000:
                print "This world was a failure, restarting..."
                return None
            for j in range(c.num_civs):
                if j in stats and stats[j] > 0.95:
                    print "Civ " + str(j) + " won this one"
                    stats['civs'][j]['year'] = i
                    return stats['civs'][j]
    stats = world_stats(world,10000,c)
    return stats

def n_simulate(N):
    civ_stats = []
    for i in range(N):
        print "Simulation " + str(i) + "\n---------------\n---------------\n---------------"
        s = simulate()
        if s is not None:
            civ_stats.append(s)
    keys = civ_stats[0].keys()
    organized_data = np.zeros((len(keys),len(civ_stats)))

    av_f = open("./winning_civs.csv",'w')
    key_line = "id,"
    for k in keys:
        key_line+= k + ','
    av_f.write(key_line+'\n')

    for i in range(len(civ_stats)):
        k_i = 0
        av_f.write(str(i) + ',')
        for k in keys:
            organized_data[k_i][i] = civ_stats[i][k]
            av_f.write(str(organized_data[k_i][i]) + ',')
            k_i += 1
        av_f.write("\n")
    av_f.close()
    print " Done "
    print '----------------\n----------------\n----------------\n----------------'

n_simulate(100)



