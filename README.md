# python-chess-game
A chess game programmed in python, by me, Kevin. 

Special thanks to Russell, Tristan, and Elliot (the first two of whom are my brothers)! They have been immensely helpful in all sorts of aspects of coding.

![image](https://user-images.githubusercontent.com/64618290/88246685-116c9480-cc50-11ea-97c6-68a0bd02c1de.png)
These chess programs demonstrate the importance of object-oriented programming and design. Chess 1.0 uses procedural programming in a single file.  See the associated readme in the chess-py-1.0 file for more details.

![image](https://user-images.githubusercontent.com/64618290/88463694-6df6cc00-ce69-11ea-8540-c19525a978a2.png)
Chess 2.0 uses objects and classes in multiple files. See the associated readme in the chess-py-2.0 file for details.



The chess 2.0 program builds upon the design of version 1.0. However, many improvements were made - many functions were streamlined and shortened. Where possible, constants were substituted for numbers to improve code readability. Functions for different objects were encapsulated in their own classes - making the code base much easier to work with and debug. For example, different piece types inherit functionality and properties from a parent Piece class, which improves the ease of working with them. The str operator for the Board class was overloaded so that print(board) now works, since the board is returned as a string (rather than having a function print the board to the terminal, line by line). Where possible, consideration to minimizing CPU cycles was given. 

Improvements are still to be made. The biggest goal is getting the Python code running in a browser - which involves programming a graphical interface, among other things. I am confident that it can be done and am working towards that goal. Other improvements are still forthcoming - for example, undo functions and castling are not yet implemented. 

Overall, some major objectives have been met. These include practicing object-oriented programming in Python, practicing collaboration through GitHub, and of course, having some fun doing a personal coding project!
