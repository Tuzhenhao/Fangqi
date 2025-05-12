import random
import copy
import math


#This file is used for test Minimax algorithm versus MCTS algorithm


class game_test():
    def __init__(self):
        self.chessboard = None
        self.boardsize_x = 7  #chessboard row
        self.boardsize_y = 8  #chessboard row
        self.game = True      #Record game state. False for eliminate the game
        self.square_o = []    #Record for o square
        self.square_x = []    #Record for x square
        self.round = 1        #Record for round number
        self.flag = True      
        self.mode = None      #Game mode
        self.last_move = None  # 记录上一步的移动 [[from_x, from_y], [to_x, to_y]]
        self.move_history = []  # 记录最近的移动序列（用于检测循环）
        self.count_fill = 0
        self.count_remove = 0
        self.count_move = 0
    # make a chessboard 
    def create_chessboard(self):
        self.chessboard = [['.' for _ in range(self.boardsize_y)] for _ in range(self.boardsize_x)]

    # reset the game data
    def reset(self):
        self.chessboard = None
        self.boardsize_x = 7
        self.boardsize_y = 8
        self.game = True
        self.square_o = []
        self.square_x = []
        self.round = 1
        self.flag = True
        self.mode = None
        self.last_move = None 
        self.move_history = []
        self.count_fill = 0
        self.count_remove = 0
        self.count_move = 0
    def time_function(func, *args, **kwargs):
        import time
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        return result, end - start

    def track_winner(self):
        o_count = sum(row.count("o") for row in self.chessboard)
        x_count = sum(row.count("x") for row in self.chessboard)
        if o_count == 0:
            return "x"
        elif x_count == 0:
            return "o"
        # print chessboard
    def print_chessboard(self):
        #print index of column and row
        for i in range(len(self.chessboard)+1):
            if i == 0:
                print("  ", i+1,end="  ")
            else:
                print(i+1, end="  ")
        print("")

        #print value of chessboard
        for i in range(len(self.chessboard)):
                print(i+1, end="  ")
                print('  '.join(self.chessboard[i]))
        print("")

    #write game data in log.txt
    def write(self,x,y,Player,stage):
        if self.flag:
            self.flag = False
            with open("chessboard_log.txt", "w+") as f:  # 使用 "a" 模式追加写入
                if Player:
                    f.write(stage + "Round " + str(self.round) + " Player 1 move: " + str(x + 1) + ", " + str(y + 1) + "\n")
                else:
                    f.write(stage + "Round " + str(self.round) + " Player 2 move: " + str(x + 1) + ", " + str(y + 1) + "\n")
                for i in range(len(self.chessboard)+1):
                    if i == 0:
                        f.write("   " + str(i+1) + "  ")
                    else:
                        f.write(str(i+1) + "  ")
                f.write("\n")
                for i in range(len(self.chessboard)):
                    f.write(str(i+1) + "  ")
                    f.write('  '.join(self.chessboard[i]))
                    f.write("\n")
                f.write("\n")  # 添加空行分隔每次输出
        else:
            with open("chessboard_log.txt", "a+") as f:  # 使用 "a" 模式追加写入
                if Player:
                    f.write(stage + "Round " + str(self.round) + " Player 1 move: " + str(x + 1) + ", " + str(y + 1) + "\n")
                else:
                    f.write(stage + "Round " + str(self.round) + " Player 2 move: " + str(x + 1) + ", " + str(y + 1) + "\n")
                for i in range(len(self.chessboard)+1):
                    if i == 0:
                        f.write("   " + str(i+1) + "  ")
                    else:
                        f.write(str(i+1) + "  ")
                f.write("\n")
                for i in range(len(self.chessboard)):
                    f.write(str(i+1) + "  ")
                    f.write('  '.join(self.chessboard[i]))
                    f.write("\n")
                f.write("\n")  # 添加空行分隔每次输出

   #Winning condition in stage 3
    def win(self):
        win = False
        o = 0
        x = 0
        for i in self.chessboard:
            for j in i:
                if j == "o":
                    o += 1
                elif j == "x":
                    x += 1
        if o == 0 or x == 0:
            win = True
        return win

    #Instruction
    def instruction(self):
        print("-" * 100)
        print("Instructions:")
        print("(1)At the beginning of the game, you are asked to choose the game mode: Enter 1 for Player versus Bot, Enter 2 for Bot versus Bot.")
        print("")
        print("(2)Stage 1: You are required to take turns setting pieces. Try your best to form 2*2 squares!")
        print("")
        print("(3)Stage 2: You are required to remove one of your opponent's piece. ")
        print("         Then, according to your square amount, remove the same amount of your opponent's piece. ")
        print("         Remember: you can't remove the piece that is already in a square.")
        print("")
        print("(4)Stage 3: You can choose one of your piece and move it in up, down, left, right directions with no distance limit.")
        print("Once you form a square, you can immediately remove one of your opponent's piece.")
        print("")
        print("(5)User Input Requirement: You can type a two digit coordinate as choosing a piece or a position. For example: 54 means row 5, column 4.")
        print("")
        print("(6)Enter \"stop\" to quit the game. Enter \"instruction\" to call the instructions.")
        print("-" * 100)
    # User input        
    def player_input(self):
        validity = False
        count = 1
        while validity == False:
            if count == 1:
                x = input("Your Turn!(Enter \"stop\" to quit the game).Enter your move: ")
            else:
                x = input("Enter your move again: ")

            if x != "stop" and x!="instruction" and len(x) == 2 and 1 <= int(x[0]) <= self.boardsize_x and 1 <= int(x[1]) <= self.boardsize_y:
                print("Your move is: " + x[0] + "," + x[1])
                validity = True
            elif x != "stop" and x!= "instruction" and len(x) == 2 and ((int(x[0]) < 1 or int(x[0]) > self.boardsize_x) or (int(x[1]) < 1 or int(x[1]) > self.boardsize_y)):
                print("Input out of range. Please try another number from [" + "1," + str(self.boardsize_x) + "], and [" + "1," + str(self.boardsize_y) + "]")
                count += 1
            elif x != "stop" and x != "instruction" and len(x)!=2:
                print("Invalid input digit. Please try again.")
                count += 1
            elif x == "stop":
                validity = True
            elif x == "instruction":
                self.instruction()
            else:
                print("Detect invalid input. Please try again.")
        return x


    # check every square of o in the chessboard, return an amount
    def check_square_o(self):
        self.square_o = []
        square_amount = 0
        for i in range(self.boardsize_x - 1):
                for j in range(self.boardsize_y - 1):
                    count_o = 0
                    square = [[i,j],[i,j+1],[i+1,j],[i+1,j+1]]
                    for index in square:
                        if self.chessboard[index[0]][index[1]] == "x" or self.chessboard[index[0]][index[1]] == ".":
                            continue
                        else:
                            count_o += 1
                    if count_o == 4:
                        self.square_o.append(square)
                        square_amount += 1
        return square_amount
    
    # check every square of o in the chessboard, return an amount
    def check_square_x(self):
        self.square_x = []
        square_amount = 0
        for i in range(self.boardsize_x - 1):
                for j in range(self.boardsize_y - 1):
                    count_x = 0
                    square = [[i,j],[i,j+1],[i+1,j],[i+1,j+1]]
                    for index in square:
                        if self.chessboard[index[0]][index[1]] == "o" or self.chessboard[index[0]][index[1]] == ".":
                            continue
                        else:
                            count_x += 1
                    if count_x == 4:
                        self.square_x.append(square)
                        square_amount += 1
        return square_amount
    
    def set_mode(self, mode):
        self.mode = mode


####################################################################################################################################################################################################
#stage 1: Fill

    # Obtain the coordinates of all empty positions on the chessboard
    def get_empty_cells(self):
        empty_cell = []
        for i in range(self.boardsize_x):
            for j in range(self.boardsize_y):
                if self.chessboard[i][j] == ".":
                    empty_cell.append([i,j])
        return empty_cell
        
    # Check whether the current chessboard is full
    def full(self):
        full = True
        for i in range(self.boardsize_x):
            for j in range(self.boardsize_y):
                if self.chessboard[i][j] == ".":
                    full = False
        return full
    
    #Stage 1 evaluating mechanism
    def evaluate_fill(self,square):
        score = 0
        count_x = 0
        count_o = 0

        for i in square:
            if self.chessboard[i[0]][i[1]] == "x":
                count_x += 1
            if self.chessboard[i[0]][i[1]] == "o":
                count_o += 1

        #自己四个子的情况
        if count_x == 4:
            score += 300
        #自己三个子的情况
        elif count_x == 3 and count_o == 0:
            score += 150
        #自己两个子的情况
        elif count_x == 2 and count_o == 0:
            score += 50
        #自己一个子的情况
        elif count_x == 1 and count_o == 0:
            score += 10
        #对手四个子的情况
        elif count_o == 4:
            score -= 300
        #对手三个子的情况
        elif count_o == 3 and count_x == 0:
            score -= 150
        #对手两个子的情况
        elif count_o == 2 and count_x == 0:
            score -= 50
        #对手一个子的情况
        elif count_o == 1 and count_x == 0:
            score -= 10
        #各种组合
        elif count_o == 3 and count_x == 1:
            score += 100
        elif count_o == 1 and count_x == 3:
            score -= 100
        elif count_o == 2 and count_x == 2:
            score += 50
        elif count_o == 2 and count_x == 1:
            score -= 30
        elif count_o == 1 and count_x == 2:
            score += 30
        elif count_o == 1 and count_x == 1:
            score += 5



        return score

    # MiniMax algorithm
    def bot_input_fill_minimax(self,depth, alpha, beta, MaxPlayer):

        #出口：递归深度为0 或者棋盘已满。
        if depth == 0 or self.full:
            #计算分数
            score = 0
            for i in range(self.boardsize_x - 1):
                for j in range(self.boardsize_y - 1):
                    square = [[i,j],[i,j+1],[i+1,j],[i+1,j+1]]
                    score += self.evaluate_fill(square)
            eval = score
            return eval
        
        # 预测
        if MaxPlayer:
            maxEval = float('-inf')
            for i in self.get_empty_cells():

                #尝试当前运动
                self.chessboard[i[0]][i[1]] = "x"
                #递归找score
                score = self.bot_input_fill_minimax(depth - 1, alpha, beta, False)
                #复原
                self.chessboard[i[0]][i[1]] = "."

                maxEval = max(maxEval, score)
                alpha = max(alpha, score)
                if beta <= alpha:  # Alpha-Beta 剪枝
                    break
            return maxEval

        else:
            minEval = float('inf')
            for i in self.get_empty_cells():

                #尝试当前运动
                self.chessboard[i[0]][i[1]] = "o"
                #递归找score
                score = self.bot_input_fill_minimax(depth - 1, alpha, beta, True)
                #复原
                self.chessboard[i[0]][i[1]] = "."

                minEval = min(minEval, score)
                #beta = min(beta, score)
                #if beta <= alpha:  # Alpha-Beta 剪枝
                #    break
            return minEval
    
    # Call the Minimax algorithm
    def find_best_move(self, mode):
        if mode == False:  # 自己是 "x"（MaxPlayer）
            best_eval = float('-inf')
            best_moves = []  # 存储所有最优动作
            for i in self.get_empty_cells():
                self.chessboard[i[0]][i[1]] = "x"
                score = self.bot_input_fill_minimax(20, float('-inf'), float('inf'), False)
                self.chessboard[i[0]][i[1]] = "."
                if score > best_eval:
                    best_eval = score
                    best_moves = [i]  # 重置最优动作列表
                elif score == best_eval:
                    best_moves.append(i)  # 加入同等最优的动作
            return random.choice(best_moves)  # 随机选一个最优动作

        else:  # 自己是 "o"（MinPlayer）
            best_eval = float('inf')
            best_moves = []
            for i in self.get_empty_cells():
                self.chessboard[i[0]][i[1]] = "o"
                score = self.bot_input_fill_minimax(20, float('-inf'), float('inf'), True)
                self.chessboard[i[0]][i[1]] = "."
                if score < best_eval:
                    best_eval = score
                    best_moves = [i]
                elif score == best_eval:
                    best_moves.append(i)
            return random.choice(best_moves)
    
    def MCT_fill(self):
        class MCTSNode:
            def __init__(self, state, parent=None, move_made=None):
                self.state = copy.deepcopy(state)
                self.parent = parent
                self.children = []
                self.visits = 0
                self.score = 0
                self.untried_moves = self.get_empty_cells()
                self.last_move = move_made  # 记录这一步的移动
                self.current_player = self.determine_current_player()  # 明确当前玩家
    
            def determine_current_player(self):
                """精确判断当前应该下棋的玩家"""
                if self.parent is None:
                    # 根节点：根据游戏模式和回合数判断
                    if self.state.mode:  # Player vs Bot
                        return "o" if len(self.untried_moves) % 2 == 1 else "x"
                    else:  # Bot vs Bot
                        return "o" if (self.state.round + len(self.untried_moves)) % 2 == 1 else "x"
                else:
                    # 子节点：与父节点相反
                    return "x" if self.parent.current_player == "o" else "o"
    
            def get_empty_cells(self):
                return [[i, j] for i in range(self.state.boardsize_x)
                              for j in range(self.state.boardsize_y)
                              if self.state.chessboard[i][j] == "."]
    
            def select_child(self):
                best_score = -float('inf')
                best_child = None
                for child in self.children:
                    if child.visits == 0:
                        uct = float('inf')
                    else:
                        exploit = child.score / child.visits
                        explore = math.sqrt(2 * math.log(self.visits) / child.visits)
                        uct = exploit + 1.414 * explore
                    if uct > best_score:
                        best_score = uct
                        best_child = child
                return best_child
    
            def expand(self):
                move = self.untried_moves.pop()
                new_state = copy.deepcopy(self.state)
                new_state.chessboard[move[0]][move[1]] = self.current_player
                child = MCTSNode(new_state, self, move)
                self.children.append(child)
                return child
    
            def simulate(self):
                sim_state = copy.deepcopy(self.state)
                empty = sim_state.get_empty_cells()
                random.shuffle(empty)
                
                # 获取当前模拟的玩家角色
                is_x_turn = (self.current_player == "x")
                
                score = 0
                current_player = self.current_player
                
                for move in empty:
                    sim_state.chessboard[move[0]][move[1]] = current_player
                    current_player = "o" if current_player == "x" else "x"
                
                # 动态评估函数
                for i in range(sim_state.boardsize_x - 1):
                    for j in range(sim_state.boardsize_y - 1):
                        square = [[i,j],[i,j+1],[i+1,j],[i+1,j+1]]
                        counts = {
                            "x": sum(1 for cell in square if sim_state.chessboard[cell[0]][cell[1]] == "x"),
                            "o": sum(1 for cell in square if sim_state.chessboard[cell[0]][cell[1]] == "o")
                        }
                        
                        # 关键修改：根据当前玩家角色调整评分
                        if is_x_turn:  # 当前是x玩家
                            if counts["x"] == 4: score += 200
                            elif counts["x"] == 3: score += 50
                            elif counts["x"] == 2: score += 10
                            if counts["o"] == 4: score -= 300
                            elif counts["o"] == 3: score -= 80
                        else:  # 当前是o玩家
                            if counts["o"] == 4: score += 200
                            elif counts["o"] == 3: score += 50
                            elif counts["o"] == 2: score += 10
                            if counts["x"] == 4: score -= 300
                            elif counts["x"] == 3: score -= 80
                return score
    
            def backpropagate(self, result):
                self.visits += 1
                # 根据玩家类型调整得分方向
                if self.current_player == "x":
                    self.score += result  # x玩家希望最大化得分
                else:
                    self.score -= result  # o玩家希望最小化得分
                if self.parent:
                    self.parent.backpropagate(result)
    
        # MCTS主流程
        root = MCTSNode(self)
        for _ in range(1000):  # 迭代次数
            node = root
            # 选择
            while not node.untried_moves and node.children:
                node = node.select_child()
            # 扩展
            if node.untried_moves:
                node = node.expand()
            # 模拟
            result = node.simulate()
            # 回溯
            node.backpropagate(result)
    
        # 选择最佳移动
        if not root.children:
            empty = self.get_empty_cells()
            return random.choice(empty) if empty else None
        
        # 选择最高UCT值的节点
        best_child = max(root.children, 
                        key=lambda x: x.score/x.visits if x.visits > 0 else 0)
        return best_child.last_move

        # Stage 1: Fill
    def fill(self):
        if self.game == True:
        
            print("-" * 100)
            print("Stage 1: Fill. In this stage, You need to take turns alternately placing pieces till the board is full. Please try to form 2x2 squares with your pieces.")
            print("")
            self.print_chessboard()
            print("-" * 100)
            size = self.boardsize_x * self.boardsize_y

            if self.mode:
                while True:
                    if size == 0:
                        print("Stage 1: Fill is over.")
                        print("-" * 100)
                        break
                    
                    #Player's move
                    PlayerEnter = self.player_input()

                    if PlayerEnter == "stop":
                        print("Thanks for playing!")
                        self.game = False
                        break
                    
                    x1 = int(PlayerEnter[0]) - 1
                    y1 = int(PlayerEnter[1]) - 1   
                    if self.chessboard[x1][y1] == ".":
                        self.chessboard[x1][y1] = "o"
                        size -= 1
                        self.print_chessboard()

                        self.write(x1,y1,True,"Stage 1 Fill.")
                        self.count_fill += 1
                        self.round += 1
                    elif self.chessboard[x1][y1] == "o" or self.chessboard[x1][y1] == "x":
                        print("You can't place here, please choose another place!")
                        continue
                    
                    #bot input
                    best_move = self.find_best_move(False)
                    self.chessboard[best_move[0]][best_move[1]] = "x"
                    size -= 1
                    print("Player 2's move is: "+ str(best_move[0] + 1) + "," + str(best_move[1] + 1))
                    self.print_chessboard()
                    self.write(best_move[0],best_move[1],False,"Stage 1 Fill.")
                    self.count_fill += 1
                    self.round +=1
                    print("-" * 100)

            else:
                while True:
                    if size == 0:
                        print("Stage 1: Fill is over.")
                        print("-" * 100)
                        break
                    
                    # bot1 stage
                    best_move1 = self.find_best_move(True)
                    self.chessboard[best_move1[0]][best_move1[1]] = "o"
                    size -= 1
                    print("Player 1's move is: "+ str(best_move1[0] + 1) + "," + str(best_move1[1] + 1))
                    self.print_chessboard()
                    self.write(best_move1[0],best_move1[1],True,"Stage 1 Fill.")
                    self.round +=1
                    self.count_fill += 1
                    print("-" * 100)

                    #bot2 stage
                    best_move2 = self.MCT_fill()
                    self.chessboard[best_move2[0]][best_move2[1]] = "x"
                    size -= 1
                    print("Player 2's move is: "+ str(best_move2[0] + 1) + "," + str(best_move2[1] + 1))
                    self.print_chessboard()
                    self.write(best_move2[0],best_move2[1],False,"Stage 1 Fill.")
                    self.round += 1
                    self.count_fill += 1
                    print("-" * 100)

####################################################################################################################################################################################################
    
    #Bot Remove
    def bot_input_remove(self,mode):
        maxscore = float('-inf')
        best_remove = None
        score = 0

        for i in range(self.boardsize_x - 1):
            for j in range(self.boardsize_y - 1):

                count_x = 0
                count_o = 0
                square = [[i,j],[i,j+1],[i+1,j],[i+1,j+1]]

                for index in square:
                    if self.chessboard[index[0]][index[1]] == "x":
                        count_x += 1
                    elif self.chessboard[index[0]][index[1]] == "o":
                        count_o += 1
                
                if mode == False:
                    if count_o == 3 and count_x == 0:
                        score = 200
                    elif count_o == 1 and count_x == 3:
                        score = 150
                    elif count_o == 3 and count_x == 1:
                        score = 100
                    elif count_o == 2 and count_x == 2:
                        score = 80
                    elif count_o == 2 and count_x == 0:
                        score = 70
                    elif count_o == 1 and count_x == 2:
                        score = 40
                    elif count_o == 2 and count_x == 1:
                        score = 30
                    elif count_o == 1 and count_x == 1:
                        score = 10
                    elif count_o == 1 and count_x == 0:
                        score = 5
                else:
                    if count_x == 3 and count_o == 0:
                        score = 200
                    elif count_x == 1 and count_o == 3:
                        score = 150
                    elif count_x == 3 and count_o == 1:
                        score = 100
                    elif count_x == 2 and count_o == 2:
                        score = 80
                    elif count_x == 2 and count_o == 0:
                        score = 70
                    elif count_x == 1 and count_o == 2:
                        score = 40
                    elif count_x == 2 and count_o == 1:
                        score = 30
                    elif count_x == 1 and count_o == 1:
                        score = 10
                    elif count_x == 1 and count_o == 0:
                        score = 5
                if score > maxscore:
                    maxscore = score
                    best_remove = [i,j]

        square = [[best_remove[0],best_remove[1]],[best_remove[0] + 1,best_remove[1]],[best_remove[0],best_remove[1] + 1],[best_remove[0] + 1,best_remove[1] + 1]]
        valid_remove = []

        for i in square:
            if mode == False:
                if self.chessboard[i[0]][i[1]] == "o":
                    valid_remove.append(i)
            else:
                if self.chessboard[i[0]][i[1]] == "x":
                    valid_remove.append(i)
        
        if len(valid_remove) != 0:
            random_remove = random.randint(0, len(valid_remove) - 1)
            best_remove = valid_remove[random_remove]
            return best_remove
        else:
            return []
    
    #Player Remove
    def player_remove(self,player_move,call):
        while player_move != 0 and not self.win():
            self.print_chessboard()
            print("Please choose an \"x\" piece to remove.")
            remove = self.player_input()
            if remove == "stop":
                print("Thanks for playing!")
                print("-" * 100)
                break
            x1 = int(remove[0]) - 1
            y1 = int(remove[1]) - 1
            #检测remove的子是否已形成square（在不在self.square_x里）
            flag = True
            for i in self.square_x:
                if [x1,y1] in i:
                    flag = False
            if self.chessboard[x1][y1] == "x" and flag == True:
                self.chessboard[x1][y1] = "."
                self.print_chessboard()
                if call:
                    self.write(x1,y1,True,"Stage 2 Remove.")
                else:
                    self.write(x1,y1,True,"Stage 3 Move-Remove")
                player_move -= 1  
                self.round +=1
                self.count_remove += 1
            elif self.chessboard[x1][y1] == "o" or self.chessboard[x1][y1] == ".":
                print("You can't remove piece here. Please choose your oppenent's pieces")
                continue
            elif flag == False:
                print("This piece has formed square. Please try other one.")

    #Stage 2: Remove
    def remove(self):
        if self.game:
            print("-" * 100)
            print("")
            print("Stage 2: Remove. In this stage, You can remove one of your opponent's stones. Then, you count up the squares that you has formed and removes an equal number of your opponent's pieces, as long as those pieces are not part of a square.")
            print("")
            print("Now, choose your move to remove the opponent's pieces")
            self.check_square_o()
            self.check_square_x()

            if self.mode:
                # Player first remove
                self.player_remove(1,True)

                # Bot first remove
                if self.game:
                    best_move = self.bot_input_remove(False)
                    self.chessboard[best_move[0]][best_move[1]] = "."
                    print("The bot's remove is: " + str(best_move[0] + 1) + "," + str(best_move[1] + 1))
                    self.print_chessboard()
                    self.write(best_move[0],best_move[1],False,"Stage 2 Remove.")
                    self.round += 1
                    self.count_remove += 1

                #player stage
                player_move = len(self.square_o)
                while player_move != 0:
                    self.player_remove(1,True)
                    player_move -= 1

                #bot stage
                if self.game:
                    bot_move = len(self.square_x)
                    print("The bot can remove " + str(bot_move) + " of your pieces.")

                while bot_move != 0 and self.game:
                    best_move = self.bot_input_remove(False)
                    self.chessboard[best_move[0]][best_move[1]] = "."
                    print("The bot's remove is: " + str(best_move[0] + 1) + "," + str(best_move[1] + 1))
                    self.print_chessboard()
                    self.write(best_move[0],best_move[1],False,"Stage 2 Remove.")
                    bot_move -= 1
                    self.round += 1
                    self.count_remove += 1
            else:
                # Bot1 first remove
                best_move = self.bot_input_remove(True)
                self.chessboard[best_move[0]][best_move[1]] = "."
                print("Player 1's remove is: " + str(best_move[0] + 1) + "," + str(best_move[1] + 1))
                self.print_chessboard()
                self.write(best_move[0],best_move[1],True,"Stage 2 Remove.")
                self.round += 1
                self.count_remove += 1

                # Bot2 first remove
                best_move = self.bot_input_remove(False)
                self.chessboard[best_move[0]][best_move[1]] = "."
                print("Player 2's remove is: " + str(best_move[0] + 1) + "," + str(best_move[1] + 1))
                self.print_chessboard()
                self.write(best_move[0],best_move[1],False,"Stage 2 Remove.")
                self.round += 1
                self.count_remove += 1

                #bot1 stage
                bot_move = len(self.square_o)
                print("The bot can remove " + str(bot_move) + " of your pieces.")

                while bot_move != 0:
                    best_move = self.bot_input_remove(True)
                    self.chessboard[best_move[0]][best_move[1]] = "."
                    print("The bot's remove is: " + str(best_move[0] + 1) + "," + str(best_move[1] + 1))
                    self.print_chessboard()
                    self.write(best_move[0],best_move[1],True,"Stage 2 Remove.")
                    bot_move -= 1
                    self.round += 1
                    self.count_remove += 1

                #bot2 stage
                bot_move = len(self.square_x)
                print("The bot can remove " + str(bot_move) + " of your pieces.")

                while bot_move != 0:
                    best_move = self.bot_input_remove(False)
                    self.chessboard[best_move[0]][best_move[1]] = "."
                    print("The bot's remove is: " + str(best_move[0] + 1) + "," + str(best_move[1] + 1))
                    self.print_chessboard()
                    self.write(best_move[0],best_move[1],False,"Stage 2 Remove.")
                    bot_move -= 1
                    self.count_remove += 1
                    self.round += 1


####################################################################################################################################################################################################

#stage 3: move
    def evaluate_move(self):
        score = 0

        # === 新增：检测移动后能形成的新完整square数量 ===
        if hasattr(self, 'previous_squares'):
            # 获取移动后棋盘上所有完整square
            current_squares = []
            for i in range(self.boardsize_x - 1):
                for j in range(self.boardsize_y - 1):
                    sq = [[i,j],[i,j+1],[i+1,j],[i+1,j+1]]
                    first = self.chessboard[sq[0][0]][sq[0][1]]
                    if first != "." and all(self.chessboard[cell[0]][cell[1]] == first for cell in sq):
                        current_squares.append(sq)
            
            # 计算新形成的完整square数量
            new_x_squares = 0
            new_o_squares = 0
            for sq in current_squares:
                if sq not in self.previous_squares:
                    if self.chessboard[sq[0][0]][sq[0][1]] == "x":
                        new_x_squares += 1
                    else:
                        new_o_squares += 1
            
            # 根据新square数量加分
            score += new_x_squares * 400  # 每个新x完整square加300分
            score -= new_o_squares * 400  # 每个新o完整square减300分
        
        return score


    #Find the valid move of the chosen piece
    def move_valid_move(self,piece):
        axis_x = int(piece[0]) - 1
        axis_y = int(piece[1]) - 1
        valid_move = []
        #right side
        right = 1
        while True:
            if axis_y + right > self.boardsize_y - 1:
                break

            if self.chessboard[axis_x][axis_y + right] == ".":
                valid_move.append([axis_x,axis_y + right])
                right += 1

            elif self.chessboard[axis_x][axis_y + right] != ".":
                break
        
        #left side
        left = 1
        while True:
            if axis_y - left < 0:
                break

            if self.chessboard[axis_x][axis_y - left] == ".":
                valid_move.append([axis_x,axis_y - left])
                left += 1

            elif self.chessboard[axis_x][axis_y - left] != ".":
                break

        #up side
        up = 1
        while True:
            if axis_x - up < 0:
                break

            if self.chessboard[axis_x - up][axis_y] == ".":
                valid_move.append([axis_x - up,axis_y])
                up += 1

            elif self.chessboard[axis_x - up][axis_y] != ".":
                break

        #down side
        down = 1
        while True:
            if axis_x + down > self.boardsize_x - 1:
                break

            if self.chessboard[axis_x + down][axis_y] == ".":
                valid_move.append([axis_x + down,axis_y])
                down += 1

            elif self.chessboard[axis_x + down][axis_y] != ".":
                break

        return valid_move

    #Minimax for stage 2
    def bot_input_move_minimax(self,depth,alpha,beta, Maxplayer):
        if depth == 0 or self.win():
            score = 0
            score += self.evaluate_move()
            return score

        if Maxplayer:
            maxEval = float('-inf')

            for i in range(self.boardsize_x):
                for j in range(self.boardsize_y):
                    if self.chessboard[i][j] == "x":
                        for m in self.move_valid_move([i+1,j+1]):
                            #尝试当前运动
                            self.chessboard[m[0]][m[1]] = "x"
                            self.chessboard[i][j] = "."
                            #递归找score
                            score = self.bot_input_move_minimax(depth - 1,alpha, beta, False)
                            #复原
                            self.chessboard[m[0]][m[1]] = "."
                            self.chessboard[i][j] = "x"
                            maxEval = max(maxEval, score)

                            alpha = max(alpha, score)
                            if beta <= alpha:  # Alpha-Beta 剪枝
                                return maxEval
            return maxEval
        
        else:
            minEval = float('inf')

            for i in range(self.boardsize_x):
                for j in range(self.boardsize_y):
                    if self.chessboard[i][j] == "o":
                        for m in self.move_valid_move([i+1,j+1]):
                            #尝试当前运动
                            self.chessboard[m[0]][m[1]] = "o"
                            self.chessboard[i][j] = "."
                            #递归找score
                            score = self.bot_input_move_minimax(depth - 1,alpha,beta , True)
                            #复原
                            self.chessboard[m[0]][m[1]] = "."
                            self.chessboard[i][j] = "o"
                            minEval = min(minEval, score)
                            alpha = max(alpha, score)
                            if beta <= alpha:  # Alpha-Beta 剪枝
                                return minEval
            return minEval
        

    #Call the Minimax
    def find_best_move_move(self, mode):
        best_eval = float('-inf') if mode == False else float('inf')
        best_moves = []  # 存储所有最优动作
        best_pieces = []  # 存储所有最优棋子

        # 初始化移动历史（如果没有）
        if not hasattr(self, 'move_history'):
            self.move_history = []
        if not hasattr(self, 'piece_move_count'):
            self.piece_move_count = {}  # 记录每个棋子的连续移动次数

        # 检查是否有棋子连续移动了多次
        banned_pieces = []
        for piece, count in self.piece_move_count.items():
            if count >= 5:
                banned_pieces.append(piece)

        # 收集所有可能的移动
        for i in range(self.boardsize_x):
            for j in range(self.boardsize_y):
                current_piece = (i, j)
                # 如果这个棋子被禁止移动(因为已经连续移动多次)，跳过
                if current_piece in banned_pieces:
                    continue

                if self.chessboard[i][j] == ("x" if mode == False else "o"):
                    valid_moves = self.move_valid_move([i + 1, j + 1])
                    if not valid_moves:
                        continue

                    for m in valid_moves:
                        # 模拟移动
                        self.chessboard[m[0]][m[1]] = "x" if mode == False else "o"
                        self.chessboard[i][j] = "."
                        # 计算分数
                        score = self.bot_input_move_minimax(2, float('-inf'), float('inf'), not mode)
                        # 复原棋盘
                        self.chessboard[m[0]][m[1]] = "."
                        self.chessboard[i][j] = "x" if mode == False else "o"

                        # 更新最优解
                        if (mode == False and score > best_eval) or (mode == True and score < best_eval):
                            best_eval = score
                            best_moves = [m]
                            best_pieces = [[i, j]]
                        elif score == best_eval:
                            best_moves.append(m)
                            best_pieces.append([i, j])

        # 如果没有找到不重复的移动(可能是因为所有棋子都被禁止了)，则允许使用被禁止的棋子
        if not best_moves and banned_pieces:
            for i in range(self.boardsize_x):
                for j in range(self.boardsize_y):
                    if self.chessboard[i][j] == ("x" if mode == False else "o"):
                        valid_moves = self.move_valid_move([i + 1, j + 1])
                        if valid_moves:
                            best_moves = [valid_moves[0]]
                            best_pieces = [[i, j]]
                            break
                else:
                    continue
                break

        # 默认选择最优解（随机打破平局）
        if best_moves:
            idx = random.randint(0, len(best_moves) - 1)
            chosen_piece = tuple(best_pieces[idx])
            chosen_move = [best_pieces[idx], best_moves[idx]]

            # 更新棋子移动计数器
            if chosen_piece in self.piece_move_count:
                # 如果这个棋子是上次移动的棋子，增加计数器
                if len(self.move_history) > 0 and self.move_history[-1][0] == list(chosen_piece):
                    self.piece_move_count[chosen_piece] += 1
                else:
                    # 否则重置计数器
                    self.piece_move_count[chosen_piece] = 1
            else:
                self.piece_move_count[chosen_piece] = 1
        else:
            # 真的没有任何合法移动
            return None

        # 更新历史记录
        self.move_history.append(chosen_move)
        if len(self.move_history) > 10:
            self.move_history.pop(0)

        return chosen_move

    def move(self):
        if self.game:
            print("-" * 100)
            print("Stage 3: Move.")
            print("")

            def squares_equal(sq1, sq2):
                """比较两个square是否相同（基于内容而非引用）"""
                return set((x,y) for x,y in sq1) == set((x,y) for x,y in sq2)

            if self.mode:  # Player vs Bot 模式
                while not self.win() and self.game:
                    # 玩家回合
                    # 保存移动前的square状态（深拷贝）
                    old_squares_o = [sq.copy() for sq in self.square_o]

                    print("Please choose one of your pieces to move.")
                    player_piece = self.player_input()

                    if player_piece == "stop":
                        self.game = False
                        continue
                    
                    from_x, from_y = int(player_piece[0])-1, int(player_piece[1])-1

                    if self.chessboard[from_x][from_y] != "o":
                        print("Please choose your own piece.")
                        continue
                    
                    # 获取有效移动位置
                    valid_moves = self.move_valid_move(player_piece)
                    if not valid_moves:
                        print("This piece has no valid moves!")
                        continue
                    
                    print("Available moves:", ", ".join([f"{m[0]+1}{m[1]+1}" for m in valid_moves]))

                    # 玩家选择移动位置
                    while True:
                        print("Choose a position to move to:")
                        player_move = self.player_input()
                        to_x, to_y = int(player_move[0])-1, int(player_move[1])-1

                        if [to_x, to_y] in valid_moves:
                            break
                        print("Invalid move. Please choose from available moves.")

                    # 执行移动
                    self.chessboard[from_x][from_y] = "."
                    self.chessboard[to_x][to_y] = "o"
                    print(f"Player 1 moved from {from_x+1},{from_y+1} to {to_x+1},{to_y+1}")
                    self.count_move += 1
                    self.print_chessboard()
                    self.write(to_x, to_y, True, "Stage 3 Move.")
                    # 检测新形成的square
                    self.check_square_o()  # 必须立即更新square状态
                    new_squares = []
                    for new_sq in self.square_o:
                        is_new = True
                        for old_sq in old_squares_o:
                            if squares_equal(new_sq, old_sq):
                                is_new = False
                                break
                        if is_new:
                            new_squares.append(new_sq)

                    # 触发remove机制
                    if new_squares:
                        print(f"New squares formed at positions: {new_squares}")
                        print(f"You can remove {len(new_squares)} opponent pieces.")
                        self.player_remove(len(new_squares), False)

                    if self.win():
                        break

                    # Bot回合
                    old_squares_x = [sq.copy() for sq in self.square_x]
                    best_move = self.find_best_move_move(False)

                    if best_move:
                        (from_x, from_y), (to_x, to_y) = best_move
                        self.chessboard[from_x][from_y] = "."
                        self.chessboard[to_x][to_y] = "x"
                        print(f"Bot moved from {from_x+1},{from_y+1} to {to_x+1},{to_y+1}")
                        self.count_move += 1
                        self.print_chessboard()
                        self.write(to_x, to_y, False, "Stage 3 Move.")

                        # 检测Bot是否形成新square
                        self.check_square_x()
                        new_squares = []
                        for new_sq in self.square_x:
                            is_new = True
                            for old_sq in old_squares_x:
                                if squares_equal(new_sq, old_sq):
                                    is_new = False
                                    break
                            if is_new:
                                new_squares.append(new_sq)

                        # Bot执行remove
                        if new_squares:
                            print(f"Bot formed new squares at: {new_squares}")
                            print(f"Bot removes {len(new_squares)} of your pieces.")
                            for _ in range(len(new_squares)):
                                best_remove = self.bot_input_remove(False)
                                if best_remove:
                                    x, y = best_remove
                                    self.chessboard[x][y] = "."
                                    print(f"Bot removed at {x+1},{y+1}")
                                    self.count_remove += 1
                                    self.print_chessboard()
                                    self.write(x, y, False, "Stage 3 Move-Remove.")
                    else:
                        print("Bot has no valid moves. Skipping turn.")

            else:  # Bot vs Bot 模式
                while not self.win():
                    # Bot 1 (o) 回合
                    old_squares_o = [sq.copy() for sq in self.square_o]
                    best_move = self.find_best_move_move(True)

                    if best_move:
                        (from_x, from_y), (to_x, to_y) = best_move
                        self.chessboard[from_x][from_y] = "."
                        self.chessboard[to_x][to_y] = "o"
                        print(f"Bot 1 moved from {from_x+1},{from_y+1} to {to_x+1},{to_y+1}")
                        self.count_move += 1
                        self.print_chessboard()
                        self.write(to_x, to_y, True, "Stage 3 Move.")

                        # 检测新square
                        self.check_square_o()
                        new_squares = []
                        for new_sq in self.square_o:
                            is_new = True
                            for old_sq in old_squares_o:
                                if squares_equal(new_sq, old_sq):
                                    is_new = False
                                    break
                            if is_new:
                                new_squares.append(new_sq)

                        # Bot 1 执行remove
                        if new_squares:
                            print(f"Bot 1 formed new squares at: {new_squares}")
                            for _ in range(len(new_squares)):
                                best_remove = self.bot_input_remove(True)
                                if best_remove:
                                    x, y = best_remove
                                    self.chessboard[x][y] = "."
                                    print(f"Bot 1 removed at {x+1},{y+1}")
                                    self.count_remove += 1
                                    self.print_chessboard()
                                    self.write(x, y, True, "Stage 3 Move-Remove.")

                    if self.win():
                        break

                    # Bot 2 (x) 回合
                    old_squares_x = [sq.copy() for sq in self.square_x]
                    best_move = self.MCTS_move(False)

                    if best_move:
                        (from_x, from_y), (to_x, to_y) = best_move
                        self.chessboard[from_x][from_y] = "."
                        self.chessboard[to_x][to_y] = "x"
                        print(f"Bot 2 moved from {from_x+1},{from_y+1} to {to_x+1},{to_y+1}")
                        self.count_move += 1
                        self.print_chessboard()
                        self.write(to_x, to_y, False, "Stage 3 Move.")

                        # 检测新square
                        self.check_square_x()
                        new_squares = []
                        for new_sq in self.square_x:
                            is_new = True
                            for old_sq in old_squares_x:
                                if squares_equal(new_sq, old_sq):
                                    is_new = False
                                    break
                            if is_new:
                                new_squares.append(new_sq)

                        # Bot 2 执行remove
                        if new_squares:
                            print(f"Bot 2 formed new squares at: {new_squares}")
                            for _ in range(len(new_squares)):
                                best_remove = self.bot_input_remove(False)
                                if best_remove:
                                    x, y = best_remove
                                    self.chessboard[x][y] = "."
                                    print(f"Bot 2 removed at {x+1},{y+1}")
                                    self.count_remove += 1
                                    self.print_chessboard()
                                    self.write(x, y, False, "Stage 3 Move-Remove.")
                        
    

    # === Inserted MCTS for Stage 3 ===

    def MCTS_move(self, mode):
        import time

        class MCTSNode:
            def __init__(self, board, parent=None, move=None, player="x"):
                self.board = copy.deepcopy(board)
                self.parent = parent
                self.children = []
                self.visits = 0
                self.score = 0
                self.move = move
                self.player = player
                self.untried_moves = self.get_all_moves(player)

            def get_all_moves(self, player):
                moves = []
                for i in range(self.board.boardsize_x):
                    for j in range(self.board.boardsize_y):
                        if self.board.chessboard[i][j] == player:
                            valid = self.board.move_valid_move([i+1, j+1])
                            for to in valid:
                                moves.append([(i, j), to])
                return moves

            def select_child(self):
                best_score = float('-inf')
                best_child = None
                for child in self.children:
                    if child.visits == 0:
                        uct = float('inf')
                    else:
                        exploit = child.score / child.visits
                        explore = math.sqrt(math.log(self.visits) / child.visits)
                        uct = exploit + 1.41 * explore
                    if uct > best_score:
                        best_score = uct
                        best_child = child
                return best_child

            def expand(self):
                move = self.untried_moves.pop()
                new_board = copy.deepcopy(self.board)
                from_pos, to_pos = move
                new_board.chessboard[from_pos[0]][from_pos[1]] = "."
                new_board.chessboard[to_pos[0]][to_pos[1]] = self.player
                child = MCTSNode(new_board, self, move, "o" if self.player == "x" else "x")
                self.children.append(child)
                return child

            def simulate(self):
                sim_board = copy.deepcopy(self.board)
                player = self.player
                total_score = 0
                for _ in range(3):
                    moves = []
                    for i in range(sim_board.boardsize_x):
                        for j in range(sim_board.boardsize_y):
                            if sim_board.chessboard[i][j] == player:
                                valid = sim_board.move_valid_move([i+1, j+1])
                                for to in valid:
                                    moves.append([(i, j), to])
                    if not moves:
                        break
                    move = random.choice(moves)
                    from_pos, to_pos = move
                    sim_board.chessboard[from_pos[0]][from_pos[1]] = "."
                    sim_board.chessboard[to_pos[0]][to_pos[1]] = player
                    sim_board.check_square_x()
                    sim_board.check_square_o()
                    square_count = len(sim_board.square_x) if player == "x" else len(sim_board.square_o)
                    total_score += square_count * (1 if player == "x" else -1)
                    player = "o" if player == "x" else "x"
                return total_score

            def backpropagate(self, result):
                self.visits += 1
                self.score += result
                if self.parent:
                    self.parent.backpropagate(-result)

        root = MCTSNode(self, player="o" if mode else "x")
        end_time = time.time() + 1.5
        while time.time() < end_time:
            node = root
            while not node.untried_moves and node.children:
                node = node.select_child()
            if node.untried_moves:
                node = node.expand()
            result = node.simulate()
            node.backpropagate(result)

        best_child = max(root.children, key=lambda c: c.visits, default=None)
        return best_child.move if best_child else None


    def gamestart(self):
            print("")
            print("Game Start! Welcome to Fangqi world!")
            self.instruction()
            self.reset()
            self.create_chessboard()

            print("-" * 100)
            #游戏模式选择
            while True:
                x = input("Please Choose Your Game Mode.\nEnter \"1\" for Player versus Bot. Enter \"2\" for Bot versus Bot:")
                if x == "1":
                    self.set_mode(True)
                    break
                elif x == "2":
                    self.set_mode(False)
                    break
                elif x == "stop":
                    self.game = False
                else:
                    print("Invalid Input! Please try again.")

            self.fill()
            self.remove()
            self.move()
            print("Game over! Thank you for playing.")