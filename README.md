# Stable-Matching-games-calculator
## Overview
This is a python based application which is designed to find a stable matching for a bipartite matching problem similar to that of the stable marriage problem introduced by Gale and Shapley except payoffs are determined by matched players transferring utility between each other and both sides of the matching are allowed to propose transfer contracts.

The application will allow the user to input a matching game problem and output a solution which will include the stable allocation, the transfer profiles which have been chosen by the algorithm, a confirmation of being stable within an epsilon approximate range and a visual representation of the stable solution as a bipartite graph.
## Required Modules 
In order to run the application, the following python modules must be installed:
- customtkinter
- networkx
- matplotlib
- numpy
## Input Formatting
### Manual Input
If the manual input option is chosen for inputting an instance of a matching game, the utility matrices for both sides of the matching will have to be inputted along with the order of transfer proposals to take place and the epsilon approximate value which the solution will be tested against.

All matrix inputs in both the manual and text file inputs follow this input scheme:

![Matrix input](https://user-images.githubusercontent.com/55467605/217369613-ff9cb3a7-3a3c-4ed4-a224-eeb2c65a3c35.jpg)

In the shown formatting spaces represents a seperation between elements and a newline represents seperated rows. It should also be noted that all matrix inputs must be square (i.e. have dimensions NxN) otherwise the input will not be accepted. 
