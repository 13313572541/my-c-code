import curses
import random

def main(stdscr):
    # 初始化设置
    curses.curs_set(0)      # 隐藏光标
    stdscr.nodelay(1)       # 非阻塞输入
    stdscr.timeout(150)     # 刷新间隔(毫秒)，数值越大蛇越慢，150比较适中
    
    # 获取屏幕尺寸
    sh, sw = stdscr.getmaxyx()
    
    # 初始化蛇的位置（屏幕中间）
    snake_y = sh // 2
    snake_x = sw // 4
    snake = [
        [snake_y, snake_x],
        [snake_y, snake_x - 1],
        [snake_y, snake_x - 2]
    ]
    
    # 初始化食物（同时存在3个食物）
    FOOD_COUNT = 3
    foods = []
    def create_food():
        """生成一个不在蛇身上也不在其他食物位置的新食物"""
        while True:
            new_food = [random.randint(1, sh - 2), random.randint(1, sw - 2)]
            if new_food not in snake and new_food not in foods:
                return new_food

    for _ in range(FOOD_COUNT):
        foods.append(create_food())
        
    # 初始化敌人（2个活动的敌人）
    ENEMY_COUNT = 2
    enemies = []
    def create_enemy():
        """生成一个不在蛇身上、食物位置上的新敌人"""
        while True:
            new_enemy = [random.randint(1, sh - 2), random.randint(1, sw - 2)]
            if new_enemy not in snake and new_enemy not in foods and new_enemy not in enemies:
                return new_enemy

    for _ in range(ENEMY_COUNT):
        enemies.append(create_enemy())
    
    # 初始方向向右
    key = curses.KEY_RIGHT
    score = 0
    
    # 定义四个方向
    directions = [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]
    
    while True:
        # 绘制分数
        stdscr.addstr(0, 2, f" Score: {score} | Enemies: {ENEMY_COUNT} ")
        
        # 绘制食物
        for f in foods:
            stdscr.addch(f[0], f[1], '*')
            
        # 绘制敌人
        for e in enemies:
            stdscr.addch(e[0], e[1], 'X')
        
        # 获取下一个按键
        next_key = stdscr.getch()
        
        # 如果按下 q 键，退出游戏
        if next_key == ord('q'):
            break
            
        # 更新方向（防止180度反向掉头）
        if next_key in directions:
            if key == curses.KEY_DOWN and next_key == curses.KEY_UP: pass
            elif key == curses.KEY_UP and next_key == curses.KEY_DOWN: pass
            elif key == curses.KEY_LEFT and next_key == curses.KEY_RIGHT: pass
            elif key == curses.KEY_RIGHT and next_key == curses.KEY_LEFT: pass
            else:
                key = next_key
                
        # 计算蛇头的新位置
        new_head = [snake[0][0], snake[0][1]]
        
        if key == curses.KEY_DOWN:
            new_head[0] += 1
        elif key == curses.KEY_UP:
            new_head[0] -= 1
        elif key == curses.KEY_LEFT:
            new_head[1] -= 1
        elif key == curses.KEY_RIGHT:
            new_head[1] += 1
            
        # 判断游戏结束条件：撞墙或撞自己或撞敌人
        if (new_head[0] in [0, sh - 1] or 
            new_head[1] in [0, sw - 1] or 
            new_head in snake or 
            new_head in enemies):
            
            msg = f"Game Over! Your score is {score}. Press 'q' to quit."
            stdscr.addstr(sh // 2, (sw - len(msg)) // 2, msg)
            stdscr.refresh()
            stdscr.nodelay(0)
            while stdscr.getch() != ord('q'):
                pass
            break
            
        # 插入新的蛇头
        snake.insert(0, new_head)
        
        # 判断是否吃到食物
        if new_head in foods:
            score += 1
            # 移除被吃掉的食物
            foods.remove(new_head)
            # 补充一个新的食物
            foods.append(create_food())
        else:
            # 没吃到食物，蛇尾前进（删除最后一节并擦除画面）
            tail = snake.pop()
            stdscr.addch(tail[0], tail[1], ' ')
            
        # 绘制蛇头
        try:
            stdscr.addch(snake[0][0], snake[0][1], '#')
        except curses.error:
            pass

        # --- 敌人移动逻辑 ---
        for i in range(len(enemies)):
            old_enemy = enemies[i]
            # 擦除旧敌人
            stdscr.addch(old_enemy[0], old_enemy[1], ' ')
            
            # 随机选择一个方向移动
            move_dir = random.choice(directions)
            new_enemy_pos = [old_enemy[0], old_enemy[1]]
            
            if move_dir == curses.KEY_DOWN:
                new_enemy_pos[0] += 1
            elif move_dir == curses.KEY_UP:
                new_enemy_pos[0] -= 1
            elif move_dir == curses.KEY_LEFT:
                new_enemy_pos[1] -= 1
            elif move_dir == curses.KEY_RIGHT:
                new_enemy_pos[1] += 1
                
            # 边界检查：如果敌人撞墙，就原地不动
            if 0 < new_enemy_pos[0] < sh - 1 and 0 < new_enemy_pos[1] < sw - 1:
                # 确保敌人不会走到其他敌人或食物的位置上（可选逻辑，让画面更干净）
                if new_enemy_pos not in enemies and new_enemy_pos not in foods:
                    enemies[i] = new_enemy_pos

            # 检查敌人移动后是否直接撞上了蛇头（防止敌人主动撞你导致你没反应过来）
            if enemies[i] == snake[0]:
                msg = f"Game Over! An enemy caught you! Score: {score}. Press 'q' to quit."
                stdscr.addstr(sh // 2, (sw - len(msg)) // 2, msg)
                stdscr.refresh()
                stdscr.nodelay(0)
                while stdscr.getch() != ord('q'):
                    pass
                return

if __name__ == "__main__":
    curses.wrapper(main)
