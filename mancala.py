__author__ = 'avik'

import sys
import util

inf = 1000

class GameState:

    def __init__(self,A,B):
        self.N = len(A) - 1
        self.P2_Stones = A
        self.P1_Stones = B
        self.P1_Mancala = self.P1_Stones[-1]
        self.P2_Mancala = self.P2_Stones[0]
        self.evalScore = None

    def getP1_Stones(self):
        return self.P1_Stones

    def getP1_Mancala(self):
        return self.P1_Mancala

    def getP2_Stones(self):
        return self.P2_Stones

    def getP2_Mancala(self):
        return self.P2_Mancala

    def getPitSize(self):
        return self.N

    def display(self):
        print "pit size:",self.getPitSize()
        print "P2 Stones:",self.getP2_Stones()
        print "P1 Stones:",self.getP1_Stones()
        print "P2 Mancala:",self.getP2_Mancala()
        print "P1 Mancala:",self.getP1_Mancala()
        print "Eval score:",self.getEvalScore()

    def setEvalScore(self):
        self.evalScore = self.getP1_Mancala() - self.getP2_Mancala()

    def getEvalScore(self):
        return self.evalScore

#def NextTurn():


def Greedy(State,player):

    actions,nextMoves = GetLegalActions(State,player)
    i = -1

    if player == 1:
        maxi = -inf

        for action in actions:
            i += 1
            if action.getEvalScore() > maxi:
                maxi = action.getEvalScore()
                newState = action
                index = i

        print "\nchosen index:",index
        print "Chosen state:"

        newState.display()

        if nextMoves[index] == True:
            Greedy(newState,player)

    else:
        mini = inf

        for action in actions:
            if action.getEvalScore() < mini:
                mini = action.getEvalScore()
                newState = action

        print "\nChosen state:"

        newState.display()



def CalculateEvalScore(P2_Mancala,P1_Mancala):
    return P1_Mancala - P2_Mancala


def GetLegalActions(state,player):

    possibleStates = []
    nextMove = []

    P1_Stones = state.getP1_Stones()
    P1_Mancala = state.getP1_Mancala()
    P2_Stones = state.getP2_Stones()
    P2_Mancala = state.getP2_Mancala()

    print P2_Stones,P1_Stones

    if player == 1:    #only for player 1
        pitSize = state.getPitSize()


        for pitIndex in range(pitSize):

            print "\npitIndex:",pitIndex
            isNextMove = False
            pits = P1_Stones + list(reversed(P2_Stones[1:]))

            #print "pits:",pits

            if pits[pitIndex] == 0:
                continue
            else:
                val = pits[pitIndex]
                #print val
                pits[pitIndex] = 0
                i = pitIndex + 1

                while val > 0:
                    if i < pitSize and pits[i] == 0 and val == 1:
                        pits[pitSize] += pits[-1-i]
                        pits[-1-i] = 0
                        pits[pitSize] += 1
                        i += 1
                        val -= 1

                        print "pits now:",pits

                    else:
                        pits[i] += 1
                        i += 1
                        val -= 1

                        print "pits now:",pits

                print "i,pitsize:",i-1,pitSize
                if i - 1 == pitSize:
                    isNextMove = True

            P1_Stones_new = pits[:pitSize+1]
            P2_Stones_new = [P2_Mancala] + list(reversed(pits[pitSize+1:]))
            #P2_Stones_new = [P2_Mancala] + pits[pitSize+1:]
            newState = GameState(P2_Stones_new,P1_Stones_new)
            possibleStates.append(newState)
            nextMove.append(isNextMove)

            print "pits:",pits

    print "\n",nextMove
    for x in possibleStates:
        print "\nPossible States:"
        x.setEvalScore()
        x.display()

    return possibleStates,nextMove




def ParseInputFile():

    with open(sys.argv[1]) as inputFile:

        task = inputFile.readline().strip()
        print "task:",task

        line = inputFile.next()
        player_id = line.strip()
        print "player_id:",player_id

        line = inputFile.next()
        cutoff = line.strip()
        print "cutoff:",cutoff

        line = inputFile.next()
        p2_states = line.strip().split()
        #print p2_states
        A = p2_states

        line = inputFile.next()
        p1_states = line.strip().split()
        #print p1_states
        B = p1_states

        line = inputFile.next()
        p2_mancala = line.strip()
        #print p2_mancala
        A.insert(0,p2_mancala)

        line = inputFile.next()
        p1_mancala = line.strip()
        #print p1_mancala
        B.append(p1_mancala)

        A = map(int,A)
        B = map(int,B)

        return A,B

def main():
    A,B = ParseInputFile()
    Start = GameState(A,B)
    #GetLegalActions(Start,1)
    Greedy(Start,1)

if __name__ == '__main__':
    main()



