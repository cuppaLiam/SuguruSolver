# SuguruSolver
This project was made as the practical prototype to represent the algorithm constructed for my VCE Algorithmics class. Although it was not required, it turned into a project that took up many months, versions, optimising further than I initially believed it could be, and to some extent work can still be done on it. 

As far as I know, the algorithm is as close to perfected as it can be (some small changes could make a difference but I am not sure of any of them currently), excluding problems that come with python of course.

There are a bunch of small updates that are needed in this repo like a better READ ME for example, and adding in validation, instructions, a better explanation and hopefully some future resolution..

..I hope to return to this project when I have the chance, and finally resolve the time complexity analysis for this, as no definite answer has been resolved.

## (Attempt at) An Explanation
Suguru (the game), also known as Tectonics, is a board game on an **l** x **w** (generally) grid, where solid lines define area boundaries which must be filled with 1 to **n** where **n** is the amount cells inside that area. Additionally, the same digit cannot occupy two adjacent cells (including diagonally). Finally, a valid suguru game must only have one solution; a small but fundamental rule that allows for such an optimised solving method.
With this set of rules, any suguru game can be solved with the created algorithm.
![Suguru game](https://images.squarespace-cdn.com/content/v1/52711462e4b0932c24aa05ae/1563529211468-I4XWA7AC3AZVQ93GMU0M/image-asset.png?format=2500w)Example suguru game shown above (source:https://www.knightfeatures.com/logic-puzzles/suguru)

One key takeaway from this algorithm is that it is **not backtracking**, instead, a more optimised decision based algorithm slowly but surely solves the game.
To put simply, the algorithm attempts to solve one cell at a time, looping through the board, taking advantage of the rules of the game to deduce information.

In the future, a more detailed explanation will hopefully be put here!
