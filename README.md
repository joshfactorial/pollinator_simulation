# Pollinator simulator

# Title: 
Pollinator Monte Carlo (PMC) toolkit

## Creator:
Joshua Allen

# Monte Carlo Simulation Scenario & Purpose:
Originally developed to simulate a Monarch Butterfly attempting to migrate across a crop field in central Illinois, 
this project has been expanded to attempt to model any numbor of pollinators in agricultural areas attempting to survive
the harsh environments presented by the presence of humans. My goal is to be able to offer this as a toolkit for organic
and commercial farmers who want to find ways to optimize their fields to allow the crops and native habitat to coexist 
to the maximum extent possible. I recognize that modern farming has to maximize field usage, but also feel that as
citizens of planet Earth, we must be cognizant of our role here and strive for balance. I predict that it is possible to
strike that balance in a way that maintains the use of the land for human ends but still allows the survival of the
wildlife that existed before.

This simulation as originally constructed would simulate a field approximately 50 km long and monarch butterflies that 
would attempt to move north on their migration. The fields will simulate several one-acre plots with buffer zones both 
required by regulations and some variations to try to model different scenarios to see if we can find an optimal field 
configuration for monarchs. The ultimate goal is to both test the effectiveness of bare minimum agriculture rules and 
to see if there is an optimal arrangement that maximizes field production while still being good for the butterflies.

## Simulation's variables of uncertainty
First off, let me preface this by saying that a lot remains unknown about the habits of monarch butterflies, native
bees, and other pollinators. I've made my own assumptions about these to come up with what I felt were reasonable 
outcomes on calibration fields (e.g., I'd expect a field of all milkweed to have very high survival and successful 
migration rates for monarch butterflies). People using this toolkit should consider their own research and the
literature to determine the survival rates, eating rates, flight speeds, etc that are relevant to their animal of study.

I assume a degree of random movement for the pollinators, though I built-in goals as well (e.g., seek food, shelter, and 
northly migration), which of course isn't 100% accurate. Insects follow scent trails and air currents as they move in 
what can seem like arbitrary patterns, but since those parameters are subject to effectively random (i.e., highly 
nonlinear) motions, we can treat the pollinator movement as having a random component to its motion.

## Monarch simulation variables

The average farm size in Illinois is about 1.5 square km, according to the most recent data I could find. A monarch can
travel 50 km a day on average. Some have been tagged and found moving even farther than that. What is unknown, to me, 
is if that motion represents their linear movement (50 km from start to finish), or the actual distance it covers as it
zig zags from flower to flower and tree to tree. You can imagine a butterfly zig-zagging across a field covering several 
km of actual distance, but only traversing a few hundred meters as the crow flies.

I'll assume the researchers meant that it can get 50km from it's starting position, meaning thay they could potentially 
cross over 33-34 different farms in a single day. But the buffer zone regulations really only cover areas between crop 
fields and non-crop areas. And many farms in Illinois are adjacent. My model will attempt to cover ar area of 50km to 
try to simulate one day in the life of a monarch. I'll assume uniform 1.5 km fields with buffers in between to separate
farms, at least for my premade fields. Since the buffers are around 15 meters, this means each cell of my grid should
represent about 15 meters. So one day in the life of a monarch will require a grid size of around 3,333 units on the 
long edge. The fields, I think can be effectively modeled at a smaller width, since the monarch will be trying to move 
strictly north when it can I'll ignore towns, roads, and the other things that real life reflects in order to simplify 
the example.

I have set up several tests to see if I could find an optimal arrangement. There are some reasonable land layouts as 
they might actually exsist now to test if those are ideal for Monarchs. I'm currently attempting after some false 
starts to implement a semi-random arrangement algorithm that can take planned acres of fields and search for optimal
arrangements to maximize butterfly survival while maintaining the appropriate crop, buffer, and windbreak ratios. I made
a first stab at creating a randomization algorithm that would hold a ration of crops to food to shelter constant and
attempt to find a suitable pattern, but the patterns it found were very non-realistic. No farmer can afford to randomly 
seed trees and weeds throughout their fields, even if that would be optimal for wildlife, so that is something I must
continue to refine.

The butterfly's variables will be the exact position it enters the field. It will be along an edge, favoring the 
southern half of the area to maximize the simulation but chosen at random within those constraints. It begins with an 
arbitrary amount of food selected from a normal curve centered at 50, representing 50% full of food. 

Behaviorally, the Butterfly will seek food in the early morning, attempt to move north during the day, seek food again
in the early evening, and finally look for a place to shelter in the evening. Factors affecting its behavior will be its 
food level, which as it drops will increase the butterfly's desire to seek food. I plan to add a mating instinct and the
ability to seek other butterflies in the future as well. Different pollinators, of course, have different mating habits.
Social bees have designated times of year that they attempt to mate, and different conditions and nesting sites.

The current simulation runs for one day, modeling 4 am to 3:59 am the next day. It's easy to modify the start time and 
new pollinators could be introduced at various times about the day and begin engaging in the behavior appropriate to the
actual time. Because our clock time is arbitrary, the time variables are stored as attributes of the pollinators
themselves. They react using their own biological clocks and cues to the amount of sunlight and such.

I plan to introduce further elements of reality as time goes, such as environmental conditions, even simple ones like
rain. Pollinators generally seek shelter in rain, which can be a deadly mess for a small animal. 

Monarchs and other pollinators might seek to leave the area as they migrate, others will be strongly tied to an area 
not be allowed to simply wander off. This is an attribute of the animal that varies from species to species.

## Instructions on how to use the program:
A test field can be created by making a list of lists and converting it to a field using the field object, which usses
numpy arrays to store the data, and thus has all the attributes of numpy arrays and more. Anything that can be converted
to a numpy array can be converted to an Area, with the caveat that Areas must be 2 dimensional and can only contain 
integers in the set {1, 2, 3, 4}, where 1 = crop, 2 = food (milkweed and other flowers), 3 = shelter (trees). There are 
also several functions to create test fields. These are all prefaced "create_" etc. There is also a  built-in function 
in Field called random_field that can create a field given parameters of length, width, percent crop, percent food, and 
percent shelter, but see the notes above on the success and plans for this.

## All Sources Used:
Buffer zone source: [usda organic farming](https://www.ams.usda.gov/sites/default/files/media/6%20Buffer%20Zones%20FINAL%20RGK%20V2.pdf)
They give a buffer zone of 50 feet, which is right around 15 meters. So my unit of distance for a cell will be 15 meters


How far do monarchs travel in a day? They quote 25-30 miles. I rounded up
to 50 km to be my standard distance. [monarch lab FAQ](https://monarchlab.org/biology-and-research/ask-the-expert/faq)

The average farm size in Illinois in 2018 was 358 acres [average farm size](https://farmdocdaily.illinois.edu/2013/08/trends-illinois-farmland-parcel-size.html),
which translates to about 1.4 square kilometers, so I'll base it on 1.5 km to make it easier.

I welcome anyone who can point me to some sources for some of the simulation parameters
