import numpy as np
class civs():
    def __init__(self, N):
        self.N = N
        self._num_attributes = 9
        self._same_attributes = 3
        self._other_attributes = 7
        self._same_marry = 0
        self._same_kill = 1
        self._same_leave_alone = 2
        self._other_convert = 3
        self._other_kill = 4
        self._other_marry = 5
        self.other_leave_alone = 6
        self._faith = 7
        self._fight_ability = 8
        self.num_civs = 1
        self._attributes = np.zeros((self._num_attributes,N))
    def stats(self):
        stats = {}
        for i in range(self.num_civs):
            stats[i] = {}
            stats[i]['Same Marry'] = self._attributes[self._same_marry][i]
            stats[i]['Same Kill'] = self._attributes[self._same_kill][i]
            stats[i]['Same Leave Alone'] = self._attributes[self._same_leave_alone][i]
            stats[i]['Other Convert'] = self._attributes[self._other_convert][i]
            stats[i]['Other Kill'] = self._attributes[self._other_kill][i]
            stats[i]['Other Marry'] = self._attributes[self._other_marry][i]
            stats[i]['Other Leave Alone'] = self._attributes[self.other_leave_alone][i]
            stats[i]['Faith'] = self._attributes[self._faith][i]
            stats[i]['Fight Ability'] = self._attributes[self._fight_ability][i]
        return stats

    def init_rand_civs(self, num_civs = 5):
        on_civ = self.num_civs
        for i in range(num_civs):
            for j in range(self._num_attributes):
                self._attributes[j][on_civ] = np.random.rand()
                if j == self._fight_ability:
                    self._attributes[j][on_civ] = np.random.rand() * 0.3 + 0.4
            on_civ+=1
        self.num_civs = on_civ

    def _empty_spot(self,world, c1,c2):
        empty = self._empty_neighbors(world,c1[0],c1[1])
        if len(empty) != 0:
            i = np.random.randint(len(empty))
            return (empty[0][i], empty[1][i])
        empty = self._empty_neighbors(world,c2[0],c2[1])
        if len(empty) != 0:
            i = np.random.randint(len(empty))
            return (empty[0][i], empty[1][i])
        return None

    def _empty_neighbors(self,world,x,y):
        search_area = world[x-1:x+2,y-1:y+2]
        return np.where(search_area == 0)

    def interact(self, world, c1, c2):
        if world[c1[0]][c1[1]] == world[c2[0]][c2[1]]:
            self._same_interact(world, c1, c2)
        else:
            self.other_interact(world, c1,c2)

    def _same_marry_them_up(self,civ):
        seduction = 0
        seduction += self._attributes[self._same_marry][civ] * np.random.rand()
        seduction += self._attributes[self._same_marry][civ] * np.random.rand()
        return seduction >= 0.35
    def _same_interact(self,world, c1, c2):
        civ = world[c1[0]][c1[1]]
        action = np.argmax(self._attributes[civ][:self._same_attributes])
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
            self._attributes[i][self.num_civs] = self._attributes[civ1][i] * weight + self._attributes[civ2][i] * (1 - weight)
        self.num_civs += 1
        return self.num_civs - 1

    def _fight(self, civ1, civ2):
        a1 = self._attributes[self._fight_ability][civ1] * np.random.rand()
        a2 = self._attributes[self._fight_ability][civ2] * np.random.rand()
        return a1 > a2

    def _convert(self, civ1, civ2):
        convert = self._attributes[civ1][self._other_convert] * np.random.rand()
        faith = self._attributes[civ2][self._faith] * np.random.random()
        return convert > faith

    def _marry(self, civ1, civ2):
        seduction1 = self._attributes[self._other_marry][civ1] * np.random.rand()
        faith = self._attributes[self._faith][civ2] * np.random.rand()
        return seduction1 > faith

    def other_interact(self, world, c1, c2):
        civ1 = world[c1[0]][c1[1]]
        civ2 = world[c2[0]][c2[1]]
        attributes = self._attributes[:][civ1]
        action = np.argmax(self._attributes[civ1][self._same_attributes:self._other_attributes]) + self._same_attributes
        if action == self._other_convert:
            if self._convert(civ1, civ2):
                world[c2[0]][c2[1]] = civ1
            else:
                # if failed to convert, can do something else.
                action = np.argmax(self._attributes[civ1][self._same_attributes+1:self._other_attributes])
        if action == self._other_kill:
            won_fight = self._fight(civ1,civ2)
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
            baby_civ = self._baby_civ(civ1,civ2)
            world[empty_spot[0]][empty_spot[1]] = baby_civ
        elif action == self.other_leave_alone:
            pass
        else:
            print "Should have picked an other action"