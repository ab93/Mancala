__author__ = 'avik'

import sys
import util

inf = 1000
answerStates = []
values = []
MAX_PLAYER = 1
MIN_PLAYER = 2

class GameState:

    def __init__(self,A,B):
        self.N = len(A) - 1
        self.P2_Stones = A
        self.P1_Stones = B
        self.P1_Mancala = self.P1_Stones[-1]
        self.P2_Mancala = self.P2_Stones[0]
        self.evalScore = None
        self.node = 'root'

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
        print "P2 Stones:",self.P2_Stones[1:]
        print "P1 Stones:",self.P1_Stones[:-1]
        print "P2 Mancala:",self.getP2_Mancala()
        print "P1 Mancala:",self.getP1_Mancala()
        print "Eval score:",self.getEvalScore()
        print "Node:",self.getNode()

    def setEvalScore(self):
        if MAX_PLAYER == 1:
            self.evalScore = self.getP1_Mancala() - self.getP2_Mancala()
        else:
            self.evalScore = self.getP2_Mancala() - self.getP1_Mancala()

    def getEvalScore(self):
        return self.evalScore

    def setNode(self,node):
        self.node = node

    def getNode(self):
        return self.node

    ## add gameover condition

def printTraverseLog_alpha_beta(node,depth,value,isNextMove,alpha,beta):
    global inf

    with open('traverse_log_new_alpha_beta.txt','a+') as f:
        if value == inf:
            value = 'Infinity'
        elif value == -inf:
            value = '-Infinity'

        if alpha == inf:
            alpha = 'Infinity'
        elif alpha == -inf:
            alpha = '-Infinity'

        if beta == -inf:
            beta = '-Infinity'
        elif beta == inf:
            beta = 'Infinity'

        print alpha,beta
        #raw_input()
        print "node,depth,value,isNextMove,alpha,beta:",node + ',' + str(depth) + ',' + str(value) + ',' + str(isNextMove) + ',' + str(alpha) + ',' + str(beta) + '\n'
        f.write(node + ',' + str(depth) + ',' + str(value) + ',' + str(alpha) + ',' + str(beta) + '\n')

def printTraverseLog(node,depth,value,isNextMove):
    with open('traverse_log_new.txt','a+') as f:
        if value == inf:
            value = 'Infinity'
        elif value == -inf:
            value = '-Infinity'
        print "node,depth,value,isNextMove:",node + ',' + str(depth) + ',' + str(value) + ',' + str(isNextMove) + '\n'
        f.write(node + ',' + str(depth) + ',' + str(value) + '\n')


def AlphaBeta(State,player,cutoff_depth):

    global MAX_PLAYER,MIN_PLAYER

    def maxValue(State,depth,cutoff_depth,isNextMove,alpha,beta):

        if depth == cutoff_depth:
            State.setEvalScore()
            printTraverseLog_alpha_beta(State.getNode(),depth,State.getEvalScore(),isNextMove,alpha,beta)
            return State.getEvalScore()

        v = -inf
        index = 0
        legalSuccessors,nextMoves = GetLegalSuccessors(State,MAX_PLAYER)
        for action in legalSuccessors:
            printTraverseLog_alpha_beta(State.getNode(),depth,v,isNextMove,alpha,beta)
            v = max(v, minValue(action,depth + 1,cutoff_depth,nextMoves[index],alpha,beta))
            index += 1

            if v >= beta:
                return v
            alpha = max(alpha,v)

        printTraverseLog_alpha_beta(State.getNode(),depth,v,isNextMove,alpha,beta)

        return v


    def minValue(State,depth,cutoff_depth,isNextMove,alpha,beta):

        if depth == cutoff_depth:
            State.setEvalScore()
            printTraverseLog_alpha_beta(State.getNode(),depth,State.getEvalScore(),isNextMove,alpha,beta)
            return State.getEvalScore()

        v = inf
        index = 0
        legalSuccessors,nextMoves = GetLegalSuccessors(State,MIN_PLAYER)
        for action in legalSuccessors:
            printTraverseLog_alpha_beta(State.getNode(),depth,v,isNextMove,alpha,beta)
            v = min(v, maxValue(action,depth + 1,cutoff_depth,nextMoves[index],alpha,beta))
            index += 1

            if v <= alpha:
                return v
            beta = min(beta,v)

        printTraverseLog_alpha_beta(State.getNode(),depth,v,isNextMove,alpha,beta)

        return v

    legalSuccessors,nextMoves = GetLegalSuccessors(State,MAX_PLAYER)
    bestSuccessor = None
    score = -inf
    bestScore = score
    index = 0
    alpha = -inf
    beta = inf

    for action in legalSuccessors:
        prevscore = score
        printTraverseLog_alpha_beta(State.getNode(),0,score,False,alpha,beta)
        score = max(score,minValue(action,1,cutoff_depth,nextMoves[index],alpha,beta))
        index += 1
        if score > prevscore:
            bestSuccessor = action
            bestScore = score

    print "\nChosen Action:"
    printTraverseLog_alpha_beta(State.getNode(),0,bestScore,False,alpha,beta)

    bestSuccessor.display()


def Minimax(State,player,cutoff_depth):

    global MAX_PLAYER,MIN_PLAYER

    def maxValue(State,depth,cutoff_depth,isNextMove):
        print "\nEnter maxValue..depth:",depth
        if depth == cutoff_depth:
            State.setEvalScore()

            if isNextMove == False:
                printTraverseLog(State.getNode(),depth,State.getEvalScore(),isNextMove)
                return State.getEvalScore()

        index = 0
        if isNextMove == False:
            v = -inf
            #legalSuccessors,nextMoves = GetLegalSuccessors(State,1)
            legalSuccessors,nextMoves = GetLegalSuccessors(State,MAX_PLAYER)
            for action in legalSuccessors:
                printTraverseLog(State.getNode(),depth,v,isNextMove)
                v = max(v, minValue(action,depth + 1,cutoff_depth,nextMoves[index]))
                index += 1
        else:
            v = inf
            if depth == cutoff_depth:
                v = State.getEvalScore()
            legalSuccessors,nextMoves = GetLegalSuccessors(State,MIN_PLAYER)
            for action in legalSuccessors:
                printTraverseLog(State.getNode(),depth,v,isNextMove)
                v = min(v, maxValue(action,depth,cutoff_depth,nextMoves[index]))
                index += 1

        printTraverseLog(State.getNode(),depth,v,isNextMove)
        if depth == 1:
            answerStates.append(State)
            values.append(v)
        print "max_v,depth:",v,depth
        return v


    def minValue(State,depth,cutoff_depth,isNextMove):
        print "\nEnter minValue..depth:",depth
        if depth == cutoff_depth:
            State.setEvalScore()

            if isNextMove == False:
                printTraverseLog(State.getNode(),depth,State.getEvalScore(),isNextMove)
                return State.getEvalScore()

        index= 0

        if isNextMove == False:
            v = inf
            legalSuccessors,nextMoves = GetLegalSuccessors(State,MIN_PLAYER)
            for action in legalSuccessors:
                printTraverseLog(State.getNode(),depth,v,isNextMove)
                v = min(v, maxValue(action,depth + 1,cutoff_depth,nextMoves[index]))
                index += 1
        else:
            v = -inf
            if depth == cutoff_depth:
                v = State.getEvalScore()
            legalSuccessors,nextMoves = GetLegalSuccessors(State,MAX_PLAYER)
            for action in legalSuccessors:
                printTraverseLog(State.getNode(),depth,v,isNextMove)
                v = max(v, minValue(action,depth,cutoff_depth,nextMoves[index]))
                index += 1

        print "min_v,depth:",v,depth
        printTraverseLog(State.getNode(),depth,v,isNextMove)
        if depth == 1:
            answerStates.append(State)
            values.append(v)
        return v

    legalSuccessors,nextMoves = GetLegalSuccessors(State,MAX_PLAYER)
    bestSuccessor = None
    score = -inf
    bestScore = score
    index = 0

    for action in legalSuccessors:
        prevscore = score
        printTraverseLog(State.getNode(),0,score,False)
        score = max(score,minValue(action,1,cutoff_depth,nextMoves[index]))
        index += 1
        if score > prevscore:
            bestSuccessor = action
            bestScore = score

    print "\nChosen Action:"
    printTraverseLog(State.getNode(),0,bestScore,False)

    bestSuccessor.display()
    #answerStates.append(State)

    i = 0
    for state in answerStates:
        print '\n'
        state.display()
        print values[i]
        i += 1

    print "Bestscore:",bestScore

    i=0
    temp = []
    for state in answerStates:
        print values[i]
        if values[i] == bestScore and state != bestSuccessor :
            temp.append(state)
        i += 1

    if len(temp) == 0:
        finalNextState = bestSuccessor

    print "\ntemp states:"
    MAX_EVAL = -inf
    for state in temp:
        if state.getEvalScore() > MAX_EVAL:
            MAX_EVAL = state.getEvalScore()
            finalNextState = state
        state.display()

    print "\nFinal Next State:"
    finalNextState.display()



def Greedy(State,player):

    actions,nextMoves = GetLegalSuccessors(State,player)
    nextMoves_rev = list(reversed(nextMoves))

    if player == 1:
        maxi = -inf
        i = -1
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
        #i = len(actions)
        i = -1
        #for action in list(reversed(actions)):
        for action in actions:
            i += 1
            if action.getEvalScore() < mini:
                mini = action.getEvalScore()
                newState = action
                index = i

        print "\nchosen index:",index
        print "Chosen state:"

        newState.display()

        if nextMoves[index] == True:
            print "\nHas an extra turn"
            Greedy(newState,player)



def CalculateEvalScore(P2_Mancala,P1_Mancala):
    return P1_Mancala - P2_Mancala


def GetLegalSuccessors(state,player):

    possibleStates = []
    nextMove = []
    nodes = []

    P1_Stones = state.getP1_Stones()
    P1_Mancala = state.getP1_Mancala()
    P2_Stones = state.getP2_Stones()
    P2_Mancala = state.getP2_Mancala()

    print P2_Stones,P1_Stones

    if player == 1:    #only for player 1
        pitSize = state.getPitSize()

        for pitIndex in range(pitSize):

            #print "\npitIndex:",pitIndex
            isNextMove = False
            pits = P1_Stones + list(reversed(P2_Stones[1:]))

            #print "pits:",pits

            if pits[pitIndex] == 0:
                continue
            else:
                nodes.append('B'+str(pitIndex+2))
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

                        #print "pits now:",pits

                    else:
                        if i > len(pits)-1:
                            i = 0
                            continue
                        else:
                            pits[i] += 1
                            i += 1
                            val -= 1

                        #print "pits now:",pits
                #print "i,pitsize:",i-1,pitSize
                if i - 1 == pitSize:
                    isNextMove = True

            P1_Stones_new = pits[:pitSize+1]
            P2_Stones_new = [P2_Mancala] + list(reversed(pits[pitSize+1:]))
            newState = GameState(P2_Stones_new,P1_Stones_new)
            possibleStates.append(newState)
            nextMove.append(isNextMove)
            #print "pits:",pits

        print nextMove,nodes
        i = 0
        for x in possibleStates:
            print "\nPossible States:"
            x.setEvalScore()
            x.setNode(nodes[i])
            x.display()
            i += 1

        return possibleStates,nextMove

    else:  #if player 2
        pitSize = state.getPitSize()

        for pitIndex in range(pitSize):
            #print "\npitIndex:",pitIndex
            isNextMove = False
            pits = list(reversed(P2_Stones)) + P1_Stones[:-1]

            #print "pits initially:",pits

            if pits[pitIndex] == 0:
                continue
            else:
                #nodes.append('A'+str(pitIndex + 2))
                nodes.append('A'+str(pitSize - pitIndex + 1))
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
                        #print "pits now:",pits
                    else:
                        #print pits,i
                        if i > len(pits)-1:
                            i = 0
                            continue
                        else:
                            pits[i] += 1
                            i += 1
                            val -= 1
                        #print "pits now:",pits

                #print "i,pitsize:",i-1,pitSize
                if i - 1 == pitSize:
                    isNextMove = True

            P1_Stones_new = pits[pitSize+1:] + [P1_Mancala]
            P2_Stones_new = list(reversed(pits[:pitSize+1]))
            newState = GameState(P2_Stones_new,P1_Stones_new)
            possibleStates.append(newState)
            nextMove.append(isNextMove)

            #print "pits:",pits

        print "\n",list(reversed(nextMove)),list(reversed(nodes))
        i = len(possibleStates) - 1
        for x in list(reversed(possibleStates)):
            print "\nPossible States:"
            x.setEvalScore()
            x.setNode(nodes[i])
            x.display()
            i -= 1

        return list(reversed(possibleStates)),list(reversed(nextMove))



def ParseInputFile():

    global MAX_PLAYER,MIN_PLAYER
    with open(sys.argv[1]) as inputFile:

        task = inputFile.readline().strip()
        print "task:",task

        line = inputFile.next()
        player_id = line.strip()
        print "player_id:",player_id

        if player_id == '1':
            MAX_PLAYER = 1
        else:
            MAX_PLAYER = 2
            MIN_PLAYER = 1

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

        return A,B,cutoff

def main():
    A,B,cutoffDepth = ParseInputFile()

    global MAX_PLAYER,MIN_PLAYER

    Start = GameState(A,B)
    #GetLegalSuccessors(Start,1)
    #Greedy(Start,2)
    printTraverseLog('Node','Depth','Value','')
    #printTraverseLog_alpha_beta('Node','Depth','Value','','Alpha','Beta')
    #Minimax(Start,2,3)    ####problem with >3

    Minimax(Start,MAX_PLAYER,2)
    #AlphaBeta(Start,MAX_PLAYER,2)

if __name__ == '__main__':
    main()



