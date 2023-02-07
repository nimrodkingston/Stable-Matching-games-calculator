# Stable-Matching-games-calculator
## Overview
This is a python based application which is designed to find a stable matching for a bipartite matching problem similar to that of the stable marriage problem introduced by Gale and Shapley except payoffs are determined by matched players transferring utility between each other and both sides of the matching are allowed to propose transfer contracts.

The application will allow the user to input a matching game problem and output a solution which will include the stable allocation, the transfer profiles which have been chosen by the algorithm, a confirmation of being stable within an ε-approximate range and a visual representation of the stable solution as a bipartite graph.
## Required Modules 
In order to run the application, the following python modules must be installed:
- customtkinter
- networkx
- matplotlib
- numpy
## Input Formatting
### Manual Input
If the manual input option is chosen for inputting an instance of a matching game, the utility matrices for both sides of the matching will have to be inputted along with the order of transfer proposals to take place and the ε-approximate value which the solution will be tested against.

All matrix inputs in both the manual and text file inputs follow this input scheme:

![Matrix input](https://user-images.githubusercontent.com/55467605/217370041-06397d20-4c17-4648-9d19-0d3b4c1dc936.jpg)

In the shown formatting spaces represents a seperation between elements and a newline represents seperated rows. It should also be noted that all matrix inputs must be square (i.e. have dimensions NxN) otherwise the input will not be accepted. 

The inputs for the ordering of transfer proposals Φ and the approixmation value ε is shown:

![value input](https://user-images.githubusercontent.com/55467605/217378957-0289dce7-f8f0-4c4b-952a-5e4365efb76f.jpg)

The ordering Φ is in the form of a list of indexes where the values 0 to (N/2)-1 represents players in the set M and values in the range (N/2)-1 to N-1 represents players in the set W. The values can be in any order and can even be repeated as long as there is at least one of each value in the range 0 to N-1 in Φ.

The value ε for the approximation test can take any float value the user chooses.
### Text file input
Pre-made text files which are placed in the same folder as the source code can also be used for inputs in case the same/similar results are needed often. The text file name given to the application should be in the format [filename].txt and the text file itself should be formatted accordingly:

![text file format](https://user-images.githubusercontent.com/55467605/217384884-6bb227f1-12bb-4999-87f0-a62b23ca5024.jpg)
