# python-chess-game

An attempt at programming a chess game. Object-oriented programming is not used. Python's dictionary data structure was greatly helpful in organizing the state of the chess board. Debugging was very helpful in testing - using both the built-in debugger of VSCode, as well as the basic print function. Manipulation of lists was vital for keeping track of possible movement locations on the board. Writing separate functions for movement of pieces, board manipulation, and gamestate manipulation was very useful for organization. Printing the graphical version of the board uses basic printing and formatting, but is pretty neat. And finally, being able to collaborate with my programmer brother Russell was very informative, and very helpful for learning. Thank you as well to Tristan, my other brother, and his spouse, Elliot, for their suggestions, support, and help. 

While the program started out simply enough, the eventual additions of functions such as check and checkmate greatly increase the complexity. Check, for example, has to make a list of all valid movements that could capture a king, and it has to take into account that a movement cannot be made if it places your own king in check. 

Many improvements could be made to this program. First, the actual chess notation is backwards! The program takes space inputs of "1a", for example. But proper notation should be "a1"! Traditional chess notation could certainly be followed more closely. More broadly, there are vast amounts of research to be done on the game of chess itself - but that research is outside the scope and goals of this project. 

Special rules, such as castling and pawn promotion, have not been implemented. There are also several functions and variables that are written separately for black and white pieces. With perhaps a few exceptions (ex. white vs. black pawns), these functions and variables would probably best be combined. This could be done by using a bool to describe color. Variable scope could probably be cleaned up as well. Debugging also became more difficult the longer the program got - which, of course, could be mitigated several ways. Even without using object-oriented programming, some functions could be combined, and some functions could also be relegated to their own .py files. And finally, of course there are some missing features as of this writing, like an AI, a save-state, or better exit and undo functions.
