import numpy as np
import tkinter
import customtkinter
import networkx as nx
from networkx.algorithms import bipartite
from networkx.drawing.layout import bipartite_layout
import matplotlib.pyplot as plt

class Player:
    def __init__(self,number,budget):
        self.number = number
        self.budget = budget
        self.acceptance = [] # This value determines the player which proposed the current contract (None if the player is not in a contract right now)
        self.payoff = 0

    def findMax(self,A,B): # This finds the transfer profile which the current player likes the most
        values = []

        if len(self.budget) == 0:
            return None

        for i in range(0,len(self.budget)): # This iterates through all the players on the other side
            values.append(self.utility(self.budget[i],A,B))

        if np.max(np.array(values)) == 0:
            return None
        return self.budget[np.argmax(values)]
     
    def competition(self,profile,A,B):
        # This method represents some proposer proposing a transfer contract to this player

        if self.utility(profile,A,B) > self.payoff:
            return True
        return False
    
    def utility(self,contract,A,B): # This function takes a transfer contract and returns the preference value from it
        
        if self.number < n:
            return A[contract[0]][contract[1]%n] - contract[2] + contract[3]
        else:
            return B[contract[0]][contract[1]%n] + contract[2] - contract[3]


def createPlayers(A,B):
    players = []
    
    for i in range(0,n):
        transfers = []
        for j in range(0,n):
            for t in range(0,int(B[i][j])):
                transfers.append([i,j+n,0,t])
        players.append(Player(i,transfers))

    for i in range(0,n):
        transfers = []
        for j in range(0,n):
            for t in range(0,int(A[j][i])):
                transfers.append([j,i+n,t,0])
        players.append(Player(i+n,transfers))

    return players

def stabilityChecker(matching,payoffM,payoffW,A,B,epsilon):
    outsideOptions = []

    for i in range(0,len(A)):
        values = []

        for j in range(0,len(A)):
            if j != matching[i]%len(A):
                values.append(A[i][j] + B[i][j] - payoffW[j] - epsilon)

        outsideOptions.append(max(values))

    for i in range(0,len(A)):

        if payoffM[i] < outsideOptions[i]:
            print("This matching is not " + str(epsilon) + "-externally stable")
            return

    print("This matching is " + str(epsilon) + "-externally stable")

def runAlgorithm(A,B,phi,epsilon):
    global n
    n = len(A)
    players = []
    flag = False
    players = createPlayers(A,B)
    currentMatching = [None]*len(players)
   
    while flag != True:
        flag = True
        ordering = phi.copy()

        while len(ordering) != 0:
            currentPlayer = ordering[0]
            ordering.pop(0)
            proposal = players[currentPlayer].findMax(A,B)

            if proposal != None:
                if currentMatching[currentPlayer] != proposal:

                    flag = False
                    contractTarget = proposal[1] if currentPlayer < n else proposal[0]
                    players[contractTarget].acceptance.append(currentPlayer)
                    players[contractTarget].budget.append(proposal)

                    if players[contractTarget].competition(proposal,A,B):
                        currentContract = currentMatching[currentPlayer]

                        if currentContract != None: # This occurs when a player is matched to the current player but the current player accepts another contract
                            currentPartner = currentContract[1] if currentPlayer < n else currentContract[0]

                            if currentContract in players[currentPartner].budget:
                                players[currentPartner].budget.remove(currentContract)

                            currentMatching[currentPartner] = None
                            players[currentPartner].payoff = 0

                            if currentPlayer in players[currentPartner].acceptance:
                                ordering = [currentPartner] + ordering
                        
                        previousContract = currentMatching[contractTarget]

                        if previousContract != None:
                            
                            previousPartner = previousContract[0] if currentPlayer < n else previousContract[1]

                            if previousContract in players[previousPartner].budget:
                                players[previousPartner].budget.remove(previousContract)

                            currentMatching[previousPartner] = None
                            players[previousPartner].payoff = 0

                            if contractTarget in players[previousPartner].acceptance:
                                ordering = [previousPartner] + ordering

                        
                        currentMatching[currentPlayer] = proposal
                        currentMatching[contractTarget] = proposal
                        players[currentPlayer].payoff = players[currentPlayer].utility(proposal,A,B)
                        players[contractTarget].payoff = players[contractTarget].utility(proposal,A,B)

                    else:
                        players[currentPlayer].budget.remove(proposal)

    f = []
    g = []
    solution = []

    for i in range(0,len(players)):
        if i<n:
            f.append(players[i].payoff)
            solution.append(currentMatching[i][1]) if currentMatching[i] != None else solution.append(None)
        else:
            g.append(players[i].payoff)
            solution.append(currentMatching[i][0]) if currentMatching[i] != None else solution.append(None)
    print("A = " + str(A))
    print("B = " + str(B))
    print("Phi = " + str(phi))
    print("Here is the list of transfer profiles in the form [Mi,Wj,xi,yj]: \n" + str(currentMatching))
    print("payoffM = " + str(f))
    print("payoffW = " + str(g))
    stabilityChecker(solution,f,g,A,B,epsilon)
    return solution

class GUI:
    def __init__(self):
        self.A = None
        self.B = None
        self.phi = None
        self.epsilon = None
        self.solution = None
        self.errorLabel = None
        self.manualInputButton = None
        self.textFileInputButton = None
        self.AInput = None
        self.ALabel = None
        self.ASubmit= None
        self.BInput = None
        self.BLabel = None
        self.BSubmit= None
        self.phiInput = None 
        self.phiLabel = None
        self.phiEpsilonSubmit = None
        self.epsilonInput = None
        self.epsilonLabel = None
        self.fileInput = None
        self.fileLabel = None
     


def error():
    # NOTE: This function will have to keep being edited as I add more GUI elements
    GUIElements.errorLabel = customtkinter.CTkLabel(master=root,text="An error has occured, check input formatting")
    GUIElements.errorLabel.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
    GUIElements.errorLabel.configure(font=fontTemplate)
    GUIElements.AInput.place_forget() if GUIElements.AInput != None else None
    GUIElements.ALabel.place_forget() if GUIElements.ALabel != None else None
    GUIElements.ASubmit.place_forget() if GUIElements.ASubmit != None else None
    GUIElements.BInput.place_forget() if GUIElements.BInput != None else None
    GUIElements.BLabel.place_forget() if GUIElements.BLabel != None else None
    GUIElements.BSubmit.place_forget() if GUIElements.BSubmit != None else None
    GUIElements.phiInput.place_forget() if GUIElements.phiInput != None else None
    GUIElements.epsilonInput.place_forget() if GUIElements.epsilonInput != None else None
    GUIElements.epsilonLabel.place_forget() if GUIElements.epsilonLabel != None else None
    GUIElements.phiLabel.place_forget() if GUIElements.phiLabel != None else None
    GUIElements.phiEpsilonSubmit.place_forget() if GUIElements.phiEpsilonSubmit != None else None
    GUIElements.fileInput.place_forget() if GUIElements.fileInput != None else None
    GUIElements.fileLabel.place_forget() if GUIElements.fileLabel != None else None

    mainMenu()

def textParser(inputString,type):
    output = []
    row = []
    currentVal = ""

    for i in range(0,len(inputString)):

        if i == len(inputString) - 1:
            currentVal += inputString[i]

        if inputString[i] == "\n" or i == len(inputString) - 1:
            row.append(float(currentVal)) if type else row.append(int(currentVal))
            output.append(row)
            row = []
            currentVal = ""

        elif inputString[i] == " ":
            row.append(float(currentVal)) if type else row.append(int(currentVal))
            currentVal = ""

        else:
            currentVal += inputString[i]

    n = len(output[0])
    
    if type == False:
        if n == 0:
            raise Exception
        else:
            return output[0]
 
    if len(output) != n:
        
        raise Exception

    for i in output:
        if len(i) != n:
            raise Exception
    
    return output

def preprocessFile(inputString):
    output = []
    currentVal = ""

    for i in range(0,len(inputString)):

        if i == len(inputString) - 1:
            output.append(inputString[i])

        if inputString[i] == "\n":
            output.append(currentVal)
            currentVal = ""
        else:
            currentVal += inputString[i]

    return output

def AInput():
    GUIElements.manualInputButton.place_forget()
    GUIElements.textFileInputButton.place_forget()
    GUIElements.errorLabel.place_forget() if GUIElements.errorLabel != None else None
    GUIElements.AInput = tkinter.Text(master=root,height=10,width=20,bg="#343638",fg="#fff")
    GUIElements.AInput.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
    GUIElements.ALabel = customtkinter.CTkLabel(master=root,text="Enter the payoff matrix for set M")
    GUIElements.ALabel.place(relx=0.5, rely=0.63, anchor=tkinter.CENTER)
    GUIElements.ALabel.configure(font=fontTemplate)
    GUIElements.AInput.configure(font=fontTemplate,highlightthickness=2,highlightbackground="black")
    GUIElements.ASubmit= customtkinter.CTkButton(master=root,width=200,height=100,text="Submit",command=BInput,font=fontTemplate)
    GUIElements.ASubmit.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
         
def BInput():
    try:
        GUIElements.A = textParser(list(GUIElements.AInput.get("1.0",'end-1c')),True)
    except:
        error()
        return

    GUIElements.AInput.place_forget()
    GUIElements.ALabel.place_forget()
    GUIElements.ASubmit.place_forget()
    GUIElements.BInput = tkinter.Text(master=root,height=10,width=20,bg="#343638",fg="#fff")
    GUIElements.BInput.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
    GUIElements.BLabel = customtkinter.CTkLabel(master=root,text="Enter the payoff matrix for set W")
    GUIElements.BLabel.place(relx=0.5, rely=0.63, anchor=tkinter.CENTER)
    GUIElements.BLabel.configure(font=fontTemplate)
    GUIElements.BInput.configure(font=fontTemplate,highlightthickness=2,highlightbackground="black")
    GUIElements.BSubmit = customtkinter.CTkButton(master=root,width=200,height=100,text="Submit",command=phiEpsilonInput,font=fontTemplate)
    GUIElements.BSubmit.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

def phiEpsilonInput():
    try:
        GUIElements.B = textParser(list(GUIElements.BInput.get("1.0",'end-1c')),True)

        if len(GUIElements.A) != len(GUIElements.B):
            raise Exception
    except:
        error()
        return

    GUIElements.BInput.place_forget()
    GUIElements.BLabel.place_forget()
    GUIElements.BSubmit.place_forget()
    GUIElements.phiInput = customtkinter.CTkEntry(master=root,width=400,height=100)
    GUIElements.phiInput.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
    GUIElements.phiInput.configure(font=fontTemplate,justify=tkinter.CENTER)
    GUIElements.phiLabel = customtkinter.CTkLabel(master=root,text="Enter the ordering of proposers phi")
    GUIElements.phiLabel.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
    GUIElements.phiLabel.configure(font=fontTemplate)
    
    GUIElements.epsilonInput = customtkinter.CTkEntry(master=root,width=100,height=100)
    GUIElements.epsilonInput.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    GUIElements.epsilonInput.configure(font=fontTemplate,justify=tkinter.CENTER)
    GUIElements.epsilonLabel = customtkinter.CTkLabel(master=root,text="Enter the approximation epsilon")
    GUIElements.epsilonLabel.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
    GUIElements.epsilonLabel.configure(font=fontTemplate)
    GUIElements.phiEpsilonSubmit = customtkinter.CTkButton(master=root,width=200,height=100,text="Submit",command=finaliseInputs,font=fontTemplate)
    GUIElements.phiEpsilonSubmit.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
    

def processFile():
    GUIElements.fileInput.place_forget()
    GUIElements.fileLabel.place_forget()
    GUIElements.fileSubmit.place_forget()

    try:
        file = open(GUIElements.fileInput.get())
        input = list(file.readlines())
        
        file.close()

    except:
        error()
        return

    data = preprocessFile(input)
    GUIElements.A = textParser(data[0],True)
    GUIElements.B = textParser(data[1],True)
    GUIElements.phi = textParser(data[2],False)
    GUIElements.epsilon = float(data[3])
    GUIElements.solution = computeSolution()
    
def computeSolution():
   
    solution = runAlgorithm(GUIElements.A,GUIElements.B,GUIElements.phi,GUIElements.epsilon)
    graph = nx.Graph()
    M = []
    W = []
    edges = []
    
    for i in range(0,len(GUIElements.A)):
        M.append("M" + str(i + 1))
        W.append("W" + str(i + 1))

    for i in range(0,len(GUIElements.A)):
        edges.append((M[i],W[solution[i]%len(GUIElements.A)]))

    print(edges)

    graph.add_nodes_from(M,bipartite=0)
    graph.add_nodes_from(W,bipartite=1)
    graph.add_edges_from(edges)
    pos = bipartite_layout(graph,M)
    nx.draw(graph,pos,with_labels=1)
    plt.show()
    mainMenu()
    

def finaliseInputs():
    GUIElements.phiLabel.place_forget()
    GUIElements.phiInput.place_forget()
    GUIElements.epsilonInput.place_forget()
    GUIElements.epsilonLabel.place_forget()
    GUIElements.phiEpsilonSubmit.place_forget()
    try:
        GUIElements.phi = textParser(GUIElements.phiInput.get(),False)

        if max(GUIElements.phi) != len(GUIElements.A)*2 - 1:
            raise Exception 

        GUIElements.epsilon = float(GUIElements.epsilonInput.get())
    except:
        error()
        return
    computeSolution()

def textFileInput():
    GUIElements.manualInputButton.place_forget()
    GUIElements.textFileInputButton.place_forget()
    GUIElements.errorLabel.place_forget() if GUIElements.errorLabel != None else None
    GUIElements.fileInput = customtkinter.CTkEntry(master=root,width=400,height=100)
    GUIElements.fileInput.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
    GUIElements.fileInput.configure(font=fontTemplate)
    GUIElements.fileLabel = customtkinter.CTkLabel(master=root,text="Enter the chosen file's name")
    GUIElements.fileLabel.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    GUIElements.fileLabel.configure(font=fontTemplate)
    GUIElements.fileSubmit = customtkinter.CTkButton(master=root,width=200,height=100,text="Submit",command=processFile,font=fontTemplate)
    GUIElements.fileSubmit.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

def mainMenu():
    GUIElements.manualInputButton = customtkinter.CTkButton(master=root, text="Manual input",command=AInput,font=fontTemplate,width=400,height=200)
    GUIElements.manualInputButton.place(relx=0.3, rely=0.5, anchor=tkinter.CENTER)
    GUIElements.textFileInputButton = customtkinter.CTkButton(master=root, text="Text file input",command=textFileInput,font=fontTemplate,width=400,height=200)
    GUIElements.textFileInputButton.place(relx=0.7, rely=0.5, anchor=tkinter.CENTER)

if __name__ == "__main__":
    #REMEMBER TO SEARCH THROUGH ALL THE NOTES I'VE LEFT IN THE COMMENTS
    global GUIElements
    global fontTemplate
    fontTemplate = ("Calibri", 30)
    GUIElements = GUI()
    root = customtkinter.CTk()
    root.resizable(False,False)
    mainMenu()
    
    root.geometry("1200x1200")
    root.mainloop()
