# Civ Sim
After making this I've realized I should have used the term religion instead of civilization, please see the two terms as interchangeable.
This simulates a number of religions interacting in a world, and finds which traits belong to the civilization that
lasted the longest.

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

		Hate Growth

		Other Marry

		Other Leave Alone

## Initialization

The simulation starts with a map of sized NxN. I set N to 500.

In the beginning, the map is initialized with roughly 500 different people.
A random number between 2 and 502 is chosen, which represents the amount of starting civilizations.
Each civilization gets the same amount of people equal to

	num_people = ceil(500/num civs)

Each of the beginning civilizations is randomly initialized with all the traits listed above, each trait has a value between 0 and 1. The traits are all used for different parts of the simulation which will be explained below.

## Years

Each iteration within a simulation is called a year.
At The beginning of every year, all the people in the map are selected with a random order. This is the order in which every person will get to act. When acting, every person randomly selects one of the 8 neighboring spots and tries to move there. If a different person already inhabits the chosen spot, an interaction occurs, otherwise the move is successful.

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
The action is determined by multiplying a random number between 0 and 1 to each attribute and then choosing
the largest value. That is

	max(
    	    Same Kill * random(),
        Same Marry * random(),
        Same Leave Alone * random(),
    )

##### Marriage
If a person decides to try and marry their neighbor, they might still be unsuccessful. Seduction is calculated using the expression:

	seduction = Same Marry * random() + Same Marry * random()
 Marriage occurs if seduction is above 0.35.

 If a marriage does occur, a baby belonging to the same civilization is born and put into an empty spot next to one of the two people. If such a spot does not exist, the baby is not born.
##### Killing
If the person acting decides to kill their neighbor, the two will fight. A random loser is selected and removed from the map.
##### leave alone
Nothing happens



## Affinity
Interactions between people of two different civilizations are determined by the attributes of the two civilizations. These attributes can be changed by the affinity of two civilizations towards each other.

The attributes that are affected by affinities are

        Other Kill
        Other Marry
Every time two people meet, their attributes are calculated using

		Other Kill -= Affinity[civ1][civ2] * np.random.rand()
        Other Marry  += Affinity[civ1][civ2] * np.random.rand()
where Affinity[civ1][civ2] represents the affinity civilization 1 feels towards civilization 2.

The affinity of one civilization towards another is defaulted to 0, and then increased or decreased when some actions occur.

If two civilizations meet and leave each other alone, both start liking the other more (affinity goes up). The increase in affinity is proportional to the stat 'Peace Loving'

If two civilizations meet and fight, both start hating the other more (affinity goes down). The decrease in affinity is proportional to the stat 'Hate Growth'

Whenever a fight occurs between two civilizations, one civilization had to instigate the fight. All civilizations then change their affinity towards the instigating civilization. For any given civilization, CivA, CivAs affinity towards the instigating civilization goes down proportional to CivA's 'Peace Loving' stat, and up/down proportional to CivA's affinity towards the civilization that was attacked.
That is, if the instigating civilization attacked a civilization CivA disliked, the affinity can increase.
## Added Randomness
I will use this term a lot and so decided it deserved it's own section. Since attributes determine the general characteristics of a civilization, but all civilizations have variance within themselves, I decided not to use the attributes directly. Instead, I used the traits *with added randomness*.

What I mean by *with added randomness* is that the attribute is multiplied by a random number and then used.
That is, say I wanted to use CivA's 'Faith' attribute, I instead use

    Faith * random()
On average, I should be using 0.5 * Faith for all civilizations in all their interactions.
## Different Interactions
When two people from different civilizations interact, they can choose all the same actions as when two of the same civilization interact, and an added one: convert. The full list is

	Marry, Kill, Leave Alone, Convert

Which action a person takes is determined with the expression:

    max(
    	    Other Kill * random(),
        Other Marry * random(),
        Other Leave Alone * random(),
        Other Convert * random(),
    )
##### Convert
When a civilization, civ1, tries to convert another civilization civ2, 2/3rds of civ1's 'Other Convert' (with added randomness) must be greater than civ2's faith (with added randmoness).

If a conversion is unsuccessful, civ1 can try to do another action.

##### Kill

The winner of a fight is determined by the greater fight ability of the two civilizations (with added randomness)

Affinity is affected after a fight, as explained in the affinity section.

##### Marry
Seduction is calculated by adding the two 'Other Marry' attributes of civ1 and civ2 relative to each other

Faith is calculated using the faith attribute of both civs

If

	seduction * random() * random() > faith (with added randomness)

a marriage occurs.

Not ice that seduction is multiplied twice by a random average, meaning on average the expression will be

	seduction * 0.25 > faith * 0.5

If a marriage occurs, a baby is made and put into an empty neighboring spot if possible.
The baby's civilization is determined by the relative faiths of the two civs (with randomness). If the two civs are
within some threshhold of one another, a new civilization is born. Otherwise, the civilzation with the higher faith gets the baby.

The two parents are then converted to whatever faith the baby is.


## End
A simulation ends when one civilization makes up over 95% of the population.
When this happens, the traits of the winning civilization is recorded and the simulation is started anew.

The simulation is run as many times as wanted (I ran it 100 times) and the results for the average winning civilization
are stored in a csv marked winning_civs.csv
mine can be found in repo.