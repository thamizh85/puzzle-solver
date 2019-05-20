## Signpost


### Objective
I am interested to emulate how Kasparove plays Chess rather than how Deep Blue does. There are tons of solvers out there which implement deep and wide searches which are not humanly possible. Whereas we solve by a process of elimination and building a shallow guesswork tree (limited by our brain's working memory capacity). This solver aims to replicate that process.

### Strategy
 1. From each cell, prepare a mini graph with next available moves
 2. A Path graph is part of the final solution since we need to visit all
 3. The whole puzzle is solved once the graph attached to every cell is a Path graph.

## TODO
1. Currently the solver can only solve simple puzzles which can be solved by elimination and without guesswork. Technically speaking, populating all available moves for a given cells is a guess work but that is where we (draw the line)[https://www.gmpuzzles.com/blog/2013/03/ask-dr-sudoku-12-the-line-must-be-drawn-here/].
2. Get rid of the frankenstein data representation models and eliminate convoluted if conditions.
3. Isolate the more generic parts of the code to a generic solver which can be applied to all puzzles of the same class. 
4. If point 1 is not tenable, introduce a thin BFS attempt to pull the model out of a non-deterministic trench.