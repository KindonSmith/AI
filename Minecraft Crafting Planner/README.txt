Kindon Smith
Philip Stanley

Our search approach differed in that we don't technically have a queue,
we just have a list of actions we can take and we choose the best one
from there, rather than sorting them and putting them into a queue.

Our heuristic essentially incentivizes options that increase
the variety of our state and deincentivizes multiple of the same object.
It's not a great heuristic for building one of an item, but it does
ok for building single ones.

Our search isn't a* or dijkstras, its a much simpler MST beacuse we thought
that might be better for exploring a variety of options at will rather than
having a set queue every time you check an action.