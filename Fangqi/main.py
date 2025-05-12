#from initialize import game
from test_mcts_full import game
import time  # 导入时间模块

if __name__ == "__main__": 
    #game = game()
    #count_fill = 0
    #count_remove = 0
    #count_move = 0
    #start_time = time.time()  # 记录开始时间戳
    #game.gamestart()
    #count_fill += game.count_fill
    #count_remove += game.count_remove
    #count_move += game.count_move
#
    #
    #end_time = time.time()  # 记录结束时间戳
    #total_time = end_time - start_time  # 计算总耗时（秒
#
    #with open("chessboard_log.txt", "a+") as f:
    #    f.write("Count Fill "+ str(count_fill) + " times\n")
    #    f.write("Count Remove " + str(count_remove) + " times\n")
    #    f.write("Count Move "+ str(count_move) + " times \n")
    #    f.write("Total execution time: " + str(round(total_time, 2)) + " seconds\n")


    #Test
    total_fill = 0
    total_remove = 0
    total_move = 0
    total_time = 0
    x_win_count = 0
    o_win_count = 0
    for i in range(100):
        g = game()
        g.reset()
        g.create_chessboard()
        g.set_mode(False)  # Bot vs Bot 模式
        start = time.time()
        g.fill()
        g.remove()
        g.move()
        end = time.time()
        total_fill += g.count_fill
        total_remove += g.count_remove
        total_move += g.count_move
        total_time += (end - start)
        winner = g.track_winner()
        if winner == "x":
            x_win_count += 1
        elif winner == "o":
            o_win_count += 1
    with open("chessboard_log.txt", "a+") as f:
        f.write("=== 100 Game Simulation Summary ===\n")
        f.write(f"Total Count Fill: {total_fill} times\n")
        f.write(f"Total Count Remove: {total_remove} times\n")
        f.write(f"Total Count Move: {total_move} times\n")
        f.write(f"Total execution time: {round(total_time, 2)} seconds\n")
        f.write(f"Average time per game: {round(total_time / 500, 2)} seconds\n")
        f.write(f"Player x wins: {x_win_count}\n")
        f.write(f"Player o wins: {o_win_count}\n")