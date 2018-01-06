#Civ Sim
I've realized this is better described by the term religion.
This simulates a number of religions interacting in a world, and finds which traits belong to the civilization that
lasted the longest. (Religion and civilization should be seen as interchangeable from this point on)/

Traits included are:

		Faith

		Same Kill

		Other Affinity Decay

		Same Marry

        Peace Loving

		Fight Ability

		Same Leave Alone

		Other Kill

		Other Convert

		Other Hate Growth

		Other Marry

		Other Leave Alone

## Initialization

The simulation starts with a map of sized NxN. I set N to 500.

In the beginning, the map is initialized with roughly 50 different civilizations and 3 people from each civ.
The people are randomly distributed along the map.
Each of the beginning civilizations is randomly initialized with all the traits listed, each trait has a value between 0 and 1.

## Years

Each iteration within a simulation is called a year.
At The beginning of every year, all the people in the map are selected with a random order. This is the order in which every
person will get to act.
When acting, every person randomly selects one of the 8 neighboring spots and tries to move there. If a person already inhabits
the chosen spot, an interaction occurs, otherwise the move is successful.

Interactions are determined primarily by whether or not the two people are of the same civilization. Then by the attributes
of the civilizations.

## Interactions

### Same interactions

When two people belong to the same civilization, they choose one of the following actions:

  	 Marry, Kill, Leave Alone

The action taken is largely affected by the attributes

    Same Kill
    Same Marry
    Same Leave Alone
The action is determined by adding a random number between 0 and 1 to each attribute and then choosing
the largest value. That is

	max(
    	Same Kill + random(),
        Same Marry + random(),
        Same Leave Alone + random(),
    )

##### Marriage
If a person decides to try and marry their neighbor, they might still be unsuccessful. Seduction is calculated using the expression:

	seduction = Same Marry * random() + Same Marry * random()
 Marriage occurs if seduction is above 0.35.

 If a marriage does occur, a baby belonging to the same civilization is born and put into an empty spot next to one of the two people. If such a spot does not exist, the baby is not born.
##### Killing
If the action chosen is two kill, one of the two people is chosen at random and taken off the map.
##### leave alone
Nothing happens



## Affinity
Interactions are determined by the attributes of the two civilizations. These attributes can be changed by the affinity of two
civilizations towards each other.

The affinity of one civilization towards another is defaulted to 0, and then increased or decreased when some actions occur.

Actions that decrease the affinity of civ1 to civ2 are:

    Fight between two people in civ1 and civ2
    Marriage between civ1 and civ2, result being a baby that does not belong to civ1

These amount changes are affected by a randomization of 'Other Hate Growth'

Whenever a person from one civ attacks a person from another, all other civilizations affinities changes towards that civ.
The change is a randomization of the sum of 20% of a civilizations affinity towards the attacked civilization, and 50% of
the civilizations Peace Loving stat.

Every year the affinity is decayed by multiplying the current affinity with 'Other Affinity Decay'

Affinity is increased by an amount equal to a randomized Peace Loving stat whenever a peaceful interaction occurs between two people
of the same civilization (Leave Alone).

Affinity affects Other Marry and Other Kill.

	    Other Kill -= Affinity[civ1][civ2] * np.random.rand()
        Other Marry  += Affinity[civ1][civ2] * np.random.rand()
Keep in mind that a positive affinity means love, negative is hate.

## Different Interactions
When two people from different civilizations interact, they can choose all the same actions as when two of the same civilization interact, and an added one.

	Marry, Kill, Leave Alone, Convert

Which action a person takes is determined with the expression:

    max(
    	Other Kill + random(),
        Other Marry + random(),
        Other Leave Alone + random(),
        Other Convert + random(),
    )
##### Convert
when civ1 tries to convert civ2, two values are calculated. Convert and faith.

	    convert = Civ1 Other Convert * random()
        faith = Civ2 Faith * random()
 the conversion is successful if convert > faith.

 If a conversion is unsuccessful, civ1 can try to do another action.


##### Kill

The winner of a fight is determined by the greater fight ability of the two civs (with added randomness)

##### Marry
Seduction is calculated by adding the two Other Marry attributes of civ1 and civ2 relative to each other

Faith is calculated using the faith attribute of both civs

If seduction> faith, a marriage occurs.

If a marriage occurs, a baby is made and put into an empty neighboring spot if possible.
The baby's civilization is determined by the relative faiths of the two civs (with randomness). If the two civs are
within 0.1 faith of one another, a new civilization is born. Otherwise, the civilzation with the higher faith gets the baby.

The two parents are then converted to whatever faith the baby is.


## End
A simulation ends when one civilization makes up over 95% of the population.
When this happens, the traits of the winning civilization is recorded and the simulation is started anew.

The simulation is run as many times as wanted (I ran it 1000 times) and the results for the average winning civilization are printed out:
Average Attributes
Normalized Average Attributes

My results were:







Full CSVs can be found in the file system