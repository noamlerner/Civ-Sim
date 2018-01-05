import numpy as np
class civs():
    def __init__(self, N):
        self.N = N
        self._num_attributes = 11
        self._same_attributes = 3
        self._other_attributes = 7
        self._same_marry = 0
        self._same_kill = 1
        self._same_leave_alone = 2
        self._other_convert = 3
        self._other_kill = 4
        self._other_marry = 5
        self._other_leave_alone = 6
        self._faith = 7
        self._other_hate_growth = 8
        self._other_affinity_decay = 9
        self._fight_ability = 10
        self.num_civs = 1
        self._attributes = np.zeros((N*N,self._num_attributes))
        self._affinities = np.zeros((N*N, N*N))

    def stats(self):
        stats = {}
        for i in range(self.num_civs):
            stats[i] = {}
            stats[i]['Same Marry'] = self._attributes[i][self._same_marry]
            stats[i]['Same Kill'] = self._attributes[i][self._same_kill]
            stats[i]['Same Leave Alone'] = self._attributes[i][self._same_leave_alone]
            stats[i]['Other Convert'] = self._attributes[i][self._other_convert]
            stats[i]['Other Kill'] = self._attributes[i][self._other_kill]
            stats[i]['Other Marry'] = self._attributes[i][self._other_marry]
            stats[i]['Other Leave Alone'] = self._attributes[i][self._other_leave_alone]
            stats[i]['Other Hate Growth'] = self._attributes[i][self._other_hate_growth]
            stats[i]['Other Affinity Decay'] = self._attributes[i][self._other_affinity_decay]
            stats[i]['Faith'] = self._attributes[i][self._faith]
            stats[i]['Fight Ability'] = self._attributes[i][self._fight_ability]
        return stats

    def still_alive(self,alive):
        attributes = np.zeros((self.N*self.N,self._num_attributes))
        on_civ = 0
        for i in alive:
            attributes[on_civ] = self._attributes[i]
            on_civ +=1
        self._attributes = attributes
        self.num_civs = on_civ
    def init_rand_civs(self, num_civs = 5):
        on_civ = self.num_civs
        for i in range(num_civs):
            for j in range(self._num_attributes):
                self._attributes[on_civ][j] = np.random.rand()
            on_civ+=1
        self.num_civs = on_civ

    def _empty_spot(self,world, c1,c2):
        empty_neighbor = self._empty_neighbor(world,c1[0],c1[1])
        if empty_neighbor != None:
            return empty_neighbor
        return self._empty_neighbor(world,c2[0],c2[1])

    def _empty_neighbor(self,world,x,y):
        search_area = world[x-1:x+2,y-1:y+2]
        basex = x-1
        basey = y-1
        w = np.where(search_area == 0)
        if len(w[0]) == 0:
            return None
        i = np.random.randint(len(w[0]))
        return (basex + w[0][i], basey + w[1][i])

    def interact(self, world, c1, c2):
        if world[c1[0]][c1[1]] == world[c2[0]][c2[1]]:
            self._same_interact(world, c1, c2)
        else:
            self.other_interact(world, c1,c2)

    def _same_marry_them_up(self,civ):
        seduction = 0
        seduction += self._attributes[civ][self._same_marry] * np.random.rand()
        seduction += self._attributes[civ][self._same_marry] * np.random.rand()
        return seduction >= 0.35

    def _same_interact(self,world, c1, c2):
        civ = world[c1[0]][c1[1]]
        action = self._take_action(self._attributes[civ][:self._same_attributes])
        if action == self._same_marry:
            if not self._same_marry_them_up(civ):
                return
            empty_spot = self._empty_spot(world,c1,c2)
            if empty_spot == None:
                return
            world[empty_spot[0]][empty_spot[1]] = civ
        elif action == self._same_kill:
            killed = np.random.randint(2)
            cs = [c1,c2]
            world[cs[killed][0],cs[killed][1]] = 0
        elif action == self._same_leave_alone:
            pass
        else:
            print "Should have picked a same action"

    def _baby_civ(self, civ1, civ2):
        for i in range(self._num_attributes):
            weight = np.random.rand()
            self._attributes[self.num_civs][i] = self._attributes[civ1][i] * weight + self._attributes[civ2][i] * (1 - weight) + np.random.rand()
        self.num_civs += 1
        return self.num_civs - 1

    def _fight(self, civ1, civ2):
        a1 = self._get_other_attributes(civ1,civ2)
        a2 = self._get_other_attributes(civ2,civ1)
        f1 = a1[self._fight_ability] * np.random.rand()
        f2 = a2[self._fight_ability] * np.random.rand()
        return f1 > f2

    def _convert(self, civ1, civ2):
        convert = self._attributes[civ1][self._other_convert] * np.random.rand()
        faith = self._attributes[civ2][self._faith] * np.random.random()
        return convert > faith

    def _marry(self, civ1, civ2):
        a1 = self._get_other_attributes(civ1,civ2)
        a2 = self._get_other_attributes(civ2,civ1)
        seduction1 = a1[self._other_marry] * np.random.rand() * np.random.rand()
        faith1 = a1[self._faith] * np.random.rand()
        seduction2 = a2[self._other_marry] * np.random.rand() * np.random.rand()
        faith2 = a2[self._faith] * np.random.rand()
        seduction = seduction1 + seduction2
        faith = faith1 + faith2
        return faith < seduction

    def _take_action(self, attributes):
        a = []
        for i in attributes:
            a.append(i * np.random.rand())
        return np.argmax(a)
    def _affinity_growth(self, civ1, civ2):
        self._affinities[civ1][civ2] -= self._attributes[civ1][self._other_hate_growth]

    def affinity_decay(self):
        for i in range(self.num_civs):
            self._affinities[i] *= self._attributes[i][self._other_affinity_decay]

    def _decide_baby_civ(self, civ1, civ2):
        baby_civ1 = self._attributes[civ1][self._faith] * np.random.rand()
        baby_civ2 = self._attributes[civ2][self._faith] * np.random.rand()
        if abs(baby_civ1 - baby_civ2) < 0.3:
            return self._baby_civ(civ1,civ2)
        else:
            if baby_civ1 > baby_civ2: return civ1
            else: return civ2

    def _get_other_attributes(self, civ1, civ2):
        attributes = np.copy(self._attributes[civ1])
        attributes[self._other_kill] -= self._affinities[civ1][civ2] * np.random.rand()
        attributes[self._other_marry] += self._affinities[civ1][civ2] * np.random.rand()
        return attributes


    def other_interact(self, world, c1, c2):
        civ1 = world[c1[0]][c1[1]]
        civ2 = world[c2[0]][c2[1]]
        attributes = self._get_other_attributes(civ1,civ2)
        action = self._take_action(attributes[self._same_attributes:self._other_attributes]) + self._same_attributes
        if action == self._other_convert:
            if self._convert(civ1, civ2):
                world[c2[0]][c2[1]] = civ1
                return
            else:
                # if failed to convert, can do something else.
                action = self._take_action(
                    self._attributes[civ1][self._same_attributes+1:self._other_attributes]) + self._same_attributes + 1
        if action == self._other_kill:
            won_fight = self._fight(civ1,civ2)
            self._affinity_growth(civ2, civ1)
            self._affinity_growth(civ1, civ2)
            if won_fight:
                world[c2[0]][c2[1]] = 0
            else:
                world[c1[0]][c1[1]] = 0
        elif action == self._other_marry:
            if not self._marry(civ1,civ2):
                return
            empty_spot = self._empty_spot(world,c1,c2)
            if empty_spot == None:
                return
            baby_civ = self._decide_baby_civ(civ1,civ2)
            if baby_civ != civ1:
                self._affinity_growth(civ1, civ2)
            if baby_civ != civ2:
                self._affinity_growth(civ2, civ1)
            world[empty_spot[0]][empty_spot[1]] = baby_civ
        elif action == self._other_leave_alone:
            pass
        else:
            print "Should have picked an other action"