I learned quite a bit on this assignment, and I enjoyed most of it(not the debugging part). Sadly, I
had to work on this alone due to my partner forcing rescheduling and then not being available.

I had a very simple method that I implemented in the beginning, and it beat all 5 bots with ease. Sadly,
I encountered a bug with it that made my code unusable, and I was forced to restart. Since then I have 
been able to beat 3 out of 5 of the bots, and I feel proud that I was able to do that.

My primary thought process was to counteract the enemy fleets in flight, if possible. I flip-flopped
on deciding to counter offensive fleets or colonizing fleets, and I decided on neutral planets only. I counteract enemy fleets if I can get to the neutral planet by the same turn, and add 1 to my fleet size.
I also adjusted the attacking behaviour to only operate if my largest planet was larger than the enemy largest planet, accounting for distance and growth rate, and then to attack the fastest growing enemy planet. My spread
also targest the fastest growing neutral planets.

I learned that checks are just as important as behaviours in behaviour trees. Without a good check, a behaviour
can be useless or make the AI worse. Several times I had checks that I just put in without too much thought, and it caused my program to suffer. I sat there scratching my head on why the behaviour didn't work properly, only to realize it was because my behaviour was executed at an unintended or poor time.

The opposite of this is pretty obvious, as it happens more often. You might know exactly when you want to
have a behaviour operate, but incorrectly execute. This happened to me quite a bit, as I am new to python
so I didn't know how to check if an objects property matched the property of some other object in a list.

All in all, behaviour trees are cool. I enjoyed this assignment thoroughly, even though I was unable to finish 
it. At one point, my bot was beating both defensive and spread bots, but not easybot, and I got a kick out of 
that. 3/5 is good for me, especially considering I did this solo.