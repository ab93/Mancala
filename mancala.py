__author__ = 'avik'

import sys

inf = 1000
answerStates = []
values = []
MAX_PLAYER = 1
MIN_PLAYER = 2
MAX_VAL = -inf
ChosenState = None

class GameState:

    def __init__(self,A,B):
        self.N = len(A) - 1
        self.P2_Stones = A
        self.P1_Stones = B
        self.P1_Mancala = self.P1_Stones[-1]
        self.P2_Mancala = self.P2_Stones[0]
        self.evalScore = None
        self.node = 'root'
        self.gameOver = False

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
        print "isGameOver:",self.isGameOver()

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

    def setGameOver(self):
        self.gameOver = True

    def isGameOver(self):
        return self.gameOver

    ## add gameover condition

def printTraverseLog_alpha_beta(node,depth,value,isNextMove,alpha,beta):
    global inf

    with open('traverse_log.txt','a+') as f:
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

        print "node,depth,value,isNextMove,alpha,beta:",node + ',' + str(depth) + ',' + str(value) + ',' + str(isNextMove) + ',' + str(alpha) + ',' + str(beta) + '\n'
        f.write(node + ',' + str(depth) + ',' + str(value) + ',' + str(alpha) + ',' + str(beta) + '\n')


def printTraverseLog(node,depth,value,isNextMove):
    with open('traverse_log.txt','a+') as f:
        if value == inf:
            value = 'Infinity'
        elif value == -inf:
            value = '-Infinity'
        print "node,depth,value,isNextMove:",node + ',' + str(depth) + ',' + str(value) + ',' + str(isNextMove) + '\n'
        f.write(node + ',' + str(depth) + ',' + str(value) + '\n')


def printNextState(nextState):
    with open('next_state.txt','w') as f:
        P2_Stones = nextState.getP2_Stones()
        P1_Stones = nextState.getP1_Stones()

        line = ''
        for i in range(1,nextState.getPitSize() + 1):
            line += str(P2_Stones[i]) + ' '
        f.write(line.strip() + '\n')

        line = ''
        for i in range(nextState.getPitSize()):
            line += str(P1_Stones[i]) + ' '
        f.write(line.strip() + '\n')

        f.write(str(nextState.getP2_Mancala()) + '\n' + str(nextState.getP1_Mancala()))


def AlphaBeta(State,player,cutoff_depth):

    global MAX_PLAYER,MIN_PLAYER,MAX_VAL,ChosenState

    def maxValue(State,depth,cutoff_depth,isNextMove,alpha,beta):

        global MAX_VAL,ChosenState

        if ((depth == cutoff_depth and isNextMove == False) or (State.gameOver == True)):
            State.setEvalScore()
            printTraverseLog_alpha_beta(State.getNode(),depth,State.getEvalScore(),isNextMove,alpha,beta)

            if depth == 1:
                if State.getEvalScore() > MAX_VAL:
                    ChosenState = State
                    MAX_VAL = State.getEvalScore()
                answerStates.append(State)
                values.append(State.getEvalScore())

            return State.getEvalScore()

        #raw_input()

        index = 0
        if isNextMove == False:
            v = -inf
            legalSuccessors,nextMoves = GetLegalSuccessors(State,MAX_PLAYER)

            for action in legalSuccessors:
                printTraverseLog_alpha_beta(State.getNode(),depth,v,isNextMove,alpha,beta)
                v = max(v, minValue(action,depth + 1,cutoff_depth,nextMoves[index],alpha,beta))
                index += 1

                #print "now....Node,depth,v:",State.getNode(),depth,v
                #raw_input()

                if v >= beta:
                    printTraverseLog_alpha_beta(State.getNode(),depth,v,isNextMove,alpha,beta)
                    return v
                alpha = max(alpha,v)

        else:
            v = inf
            legalSuccessors,nextMoves = GetLegalSuccessors(State,MIN_PLAYER)

            for action in legalSuccessors:
                printTraverseLog_alpha_beta(State.getNode(),depth,v,isNextMove,alpha,beta)
                v = min(v, maxValue(action,depth,cutoff_depth,nextMoves[index],alpha,beta))
                index += 1

                if v <= alpha:
                    printTraverseLog_alpha_beta(State.getNode(),depth,v,isNextMove,alpha,beta)
                    return v
                beta = min(beta,v)

        printTraverseLog_alpha_beta(State.getNode(),depth,v,isNextMove,alpha,beta)

        if depth == 1:
            if v > MAX_VAL:
                ChosenState = State
                MAX_VAL = v
            answerStates.append(State)
            values.append(v)

        return v


    def minValue(State,depth,cutoff_depth,isNextMove,alpha,beta):

        global MAX_VAL,ChosenState

        if ((depth == cutoff_depth and isNextMove == False) or (State.gameOver == True)):
            State.setEvalScore()
            printTraverseLog_alpha_beta(State.getNode(),depth,State.getEvalScore(),isNextMove,alpha,beta)

            if depth == 1:
                if State.getEvalScore() > MAX_VAL:
                    ChosenState = State
                    MAX_VAL = State.getEvalScore()
                answerStates.append(State)
                values.append(State.getEvalScore())

            return State.getEvalScore()

        index = 0

        if isNextMove == False:
            v = inf
            legalSuccessors,nextMoves = GetLegalSuccessors(State,MIN_PLAYER)
            for action in legalSuccessors:
                printTraverseLog_alpha_beta(State.getNode(),depth,v,isNextMove,alpha,beta)
                v = min(v, maxValue(action,depth + 1,cutoff_depth,nextMoves[index],alpha,beta))
                index += 1

                if v <= alpha:
                    printTraverseLog_alpha_beta(State.getNode(),depth,v,isNextMove,alpha,beta)
                    return v
                beta = min(beta,v)

        else:
            v = -inf
            legalSuccessors,nextMoves = GetLegalSuccessors(State,MAX_PLAYER)
            for action in legalSuccessors:
                printTraverseLog_alpha_beta(State.getNode(),depth,v,isNextMove,alpha,beta)
                v = max(v, minValue(action,depth,cutoff_depth,nextMoves[index],alpha,beta))
                index += 1

                if v >= beta:
                    printTraverseLog_alpha_beta(State.getNode(),depth,v,isNextMove,alpha,beta)
                    return v
                alpha = max(alpha,v)

        printTraverseLog_alpha_beta(State.getNode(),depth,v,isNextMove,alpha,beta)

        if depth == 1:
            if v > MAX_VAL:
                ChosenState = State
                MAX_VAL = v
            answerStates.append(State)
            values.append(v)

        return v

    f= open('traverse_log.txt','w')
    f.close()

    printTraverseLog_alpha_beta('Node','Depth','Value','','Alpha','Beta')
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

        alpha = max(alpha,score)

        if score > prevscore:
            bestSuccessor = action
            bestScore = score

    printTraverseLog_alpha_beta(State.getNode(),0,bestScore,False,alpha,beta)

    print "\nChosen Action:"
    bestSuccessor.display()

    #i = 0
    #for state in answerStates:
    #    print '\n'
    #    state.display()
    #    print values[i]
    #    i += 1

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

    else:
        print "\ntemp states:"
        MAX_EVAL = -inf
        for state in temp:
            if state.getEvalScore() > MAX_EVAL:
                MAX_EVAL = state.getEvalScore()
                finalNextState = state
            state.display()

    print "\nFinal Next State:"
    finalNextState.display()

    print "\nChosenState:",ChosenState.display()

    printNextState(finalNextState)


def Minimax(State,player,cutoff_depth):

    global MAX_PLAYER,MIN_PLAYER,MAX_VAL,ChosenState

    def maxValue(State,depth,cutoff_depth,isNextMove):

        global MAX_VAL,ChosenState

        if ((depth == cutoff_depth and isNextMove == False) or (State.gameOver == True)):
            State.setEvalScore()
            printTraverseLog(State.getNode(),depth,State.getEvalScore(),isNextMove)

            if depth == 1:
                if State.getEvalScore() > MAX_VAL:
                    ChosenState = State
                    MAX_VAL = State.getEvalScore()
                answerStates.append(State)
                values.append(State.getEvalScore())

            return State.getEvalScore()

            #if isNextMove == False:
                #printTraverseLog(State.getNode(),depth,State.getEvalScore(),isNextMove)
                #return State.getEvalScore()

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
            #if depth == cutoff_depth:
            #    v = State.getEvalScore()
            legalSuccessors,nextMoves = GetLegalSuccessors(State,MIN_PLAYER)
            for action in legalSuccessors:
                printTraverseLog(State.getNode(),depth,v,isNextMove)
                v = min(v, maxValue(action,depth,cutoff_depth,nextMoves[index]))
                index += 1

        printTraverseLog(State.getNode(),depth,v,isNextMove)
        if depth == 1:
            if v > MAX_VAL:
                ChosenState = State
                MAX_VAL = v
            answerStates.append(State)
            values.append(v)
        print "max_v,depth:",v,depth
        return v


    def minValue(State,depth,cutoff_depth,isNextMove):

        global MAX_VAL,ChosenState
        #State.display()
        #print (State.gameOver)
        #raw_input()

        if ((depth == cutoff_depth and isNextMove == False) or (State.gameOver == True)) :
            State.setEvalScore()
            printTraverseLog(State.getNode(),depth,State.getEvalScore(),isNextMove)
            #raw_input()

            if depth == 1:
                if State.getEvalScore() > MAX_VAL:
                    ChosenState = State
                    MAX_VAL = State.getEvalScore()
                answerStates.append(State)
                values.append(State.getEvalScore())

            return State.getEvalScore()

        index= 0

        #raw_input("wrong place")

        if isNextMove == False:
            v = inf
            legalSuccessors,nextMoves = GetLegalSuccessors(State,MIN_PLAYER)
            for action in legalSuccessors:
                printTraverseLog(State.getNode(),depth,v,isNextMove)
                v = min(v, maxValue(action,depth + 1,cutoff_depth,nextMoves[index]))
                index += 1
        else:
            v = -inf
            #if depth == cutoff_depth:
            #    v = State.getEvalScore()
            legalSuccessors,nextMoves = GetLegalSuccessors(State,MAX_PLAYER)
            for action in legalSuccessors:
                printTraverseLog(State.getNode(),depth,v,isNextMove)
                v = max(v, minValue(action,depth,cutoff_depth,nextMoves[index]))
                index += 1

        print "min_v,depth:",v,depth
        printTraverseLog(State.getNode(),depth,v,isNextMove)
        if depth == 1:
            if v > MAX_VAL:
                ChosenState = State
                MAX_VAL = v
                print MAX_VAL
                ChosenState.display()
                #raw_input()
            answerStates.append(State)
            values.append(v)
        return v

    f= open('traverse_log.txt','w')
    f.close()

    printTraverseLog('Node','Depth','Value','')
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

    print "\ndepth 1 states:"
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

    print '\nChosenState:',ChosenState.display()

    printNextState(ChosenState)



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


def CheckGameEnd(P1_Stones,P2_Stones,pitSize):

    P1_Stones_copy = P1_Stones
    P2_Stones_copy = P2_Stones

    all_zeros = True    #Check for P1 empty
    for i in range(pitSize):
        if P1_Stones_copy[i] != 0:
            all_zeros = False
            break

    if all_zeros == True:   #Make P2 pits to 0 and transfer to its mancala
        print "P1 Empty"
        value = 0
        for i in range(1,pitSize+1):
            value += P2_Stones_copy[i]
            P2_Stones[i] = 0
        P2_Stones[0] += value

        return P1_Stones,P2_Stones,True

    all_zeros = True    #Check for P2 empty
    for i in range(1,pitSize+1):
        if P2_Stones_copy[i] != 0:
            all_zeros = False
            break

    if all_zeros == True:    #Make P1 pits to 0 and transfer to its mancala
        print
        value = 0
        for i in range(pitSize):
            value += P1_Stones_copy[i]
            P1_Stones[i] = 0
        P1_Stones[pitSize] += value

        return P1_Stones,P2_Stones,True

    return P1_Stones,P2_Stones,False




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

            isNextMove = False
            pits = P1_Stones + list(reversed(P2_Stones[1:]))

            if pits[pitIndex] == 0:
                continue
            else:
                nodes.append('B'+str(pitIndex+2))
                val = pits[pitIndex]
                pits[pitIndex] = 0
                i = pitIndex + 1

                while val > 0:
                    if i < pitSize and pits[i] == 0 and val == 1:   #capture condition
                        pits[pitSize] += pits[-1-i]
                        pits[-1-i] = 0
                        pits[pitSize] += 1
                        i += 1
                        val -= 1

                    else:
                        if i > len(pits)-1:
                            i = 0
                            continue
                        else:
                            pits[i] += 1
                            i += 1
                            val -= 1

                if i - 1 == pitSize:
                    isNextMove = True

            P1_Stones_new = pits[:pitSize+1]
            P2_Stones_new = [P2_Mancala] + list(reversed(pits[pitSize+1:]))

            #print P1_Stones_new,P2_Stones_new
            #raw_input("before:")

            P1_Stones_new,P2_Stones_new,isGameEnd = CheckGameEnd(P1_Stones_new,P2_Stones_new,pitSize)

            #print P1_Stones_new,P2_Stones_new
            #raw_input("after:")

            newState = GameState(P2_Stones_new,P1_Stones_new)

            if isGameEnd == True:
                newState.setGameOver()
                isNextMove = False
                print "End move:"
                newState.display()
                #raw_input()

            possibleStates.append(newState)
            nextMove.append(isNextMove)

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

            P1_Stones_new,P2_Stones_new,isGameEnd = CheckGameEnd(P1_Stones_new,P2_Stones_new,pitSize)

            newState = GameState(P2_Stones_new,P1_Stones_new)

            if isGameEnd == True:
                newState.setGameOver()
                isNextMove = False
                print "End move:"
                newState.display()
                #raw_input()

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

        #raw_input()

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

        return A,B,int(cutoff),int(task)

def main():
    A,B,cutoffDepth,task = ParseInputFile()

    global MAX_PLAYER,MIN_PLAYER

    Start = GameState(A,B)
    #printTraverseLog_alpha_beta('Node','Depth','Value','','Alpha','Beta')
    #Minimax(Start,2,3)    ####problem with >3

    if task == 1:
        Minimax(Start,MAX_PLAYER,1)
    elif task == 2:
        Minimax(Start,MAX_PLAYER,cutoffDepth)
    else:
        AlphaBeta(Start,MAX_PLAYER,cutoffDepth)

    #Minimax(Start,MAX_PLAYER,3)
    #AlphaBeta(Start,MAX_PLAYER,2)

if __name__ == '__main__':
    main()



