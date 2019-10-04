Kindon Smith
Brandon Samudio

PA6, Mario Level Generation.

We will not be participating in the competition.

Individual_Grid:    
For fitness, we only modified the weighted values of the given metrics to
incentivize path and emptiness over everything except solvability. Most of our
level changes aren't proactive, they are reactive, so we focused on mutate the
most.

Breaking it down, we generate one completely new, random parent, and one
parent wins in a fitness tournament. The generate children method favors
the tournament parent 80% of the time, so we focus on the best possible level,
but still have some randomness to increase the variety of levels.

Our mutate function has access to a dictionary we made with weighted options based
on what we think makes a good level, and randomly assigns those. It then corrects itself
and removes things below a certain height, provides floor to
a % of the level, has a higher chance of removing things that are placed
lower in the level, and puts caps on uncapped pipes.

Also our program no longer infintely loops. It stops after generation 49.

Individual_DE:
We attempted to make changes to DE but it did not actually improve the functionality
of Individual DE.

First, we changed the fitness function to evaluate fitness off a few metrics,
hopefully making a more interesting level.We had used the same values we used for 
individual_grid

The mutate function in DE appears to pick a random structure or block type, then
decides whether or not to build that thing in a specific location depending on
the probability of the 'choice' variable. This is a much nicer method than a random
distribution of blocks and we think it's really interesting.

Our idea of improving this mutate fuction was to actually add to the elif
of enemy type, because it seems that the previous version skipped over it.
We try to copy the propeties of block and modify for enemy.
We also added a loop of 5 for mutate. However all these changes
still resulted in two objects in the map only.