import tkinter as tk
import random

# 游戏常量设置
CELL_SIZE = 40      # 每个方块的像素大小（从30扩大到40）
COLS = 10           # 游戏区列数
ROWS = 20           # 游戏区行数
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

# 定义7种方块的形状矩阵
SHAPES = [
    [[1, 5], [0, 5], [2, 5], [3, 5]], # I型
    [[1, 5], [0, 4], [0, 5], [1, 4]], # O型
    [[1, 5], [0, 4], [1, 4], [2, 5]], # S型
    [[1, 4], [0, 5], [1, 5], [2, 4]], # Z型
    [[1, 5], [0, 4], [1, 4], [2, 4]], # L型
    [[1, 4], [0, 4], [1, 5], [2, 5]], # J型
    [[1, 5], [0, 4], [0, 5], [0, 6]]  # T型
]

# 方块颜色
COLORS = ['#00FFFF', '#FFFF00', '#00FF00', '#FF0000', '#FFA500', '#0000FF', '#800080']

class Tetris:
    def __init__(self, root):
        self.root = root
        self.root.title("俄罗斯方块 - CodeGeeX")
        self.root.resizable(False, False)

        # 主框架
        self.frame = tk.Frame(self.root, bg='#2c3e50')
        self.frame.pack(padx=10, pady=10)

        # 游戏画布
        self.canvas = tk.Canvas(self.frame, width=WIDTH, height=HEIGHT, bg='#1a1a2e', highlightthickness=2, highlightbackground="#4a4a6a")
        self.canvas.pack(side=tk.LEFT)

        # 右侧信息面板
        self.info_frame = tk.Frame(self.frame, width=180, bg='#2c3e50')
        self.info_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(15, 0))
        
        # 分数和等级
        self.score_label = tk.Label(self.info_frame, text="分数: 0", font=("Arial", 16, "bold"), bg='#2c3e50', fg='white')
        self.score_label.pack(pady=(20, 10))
        
        self.level_label = tk.Label(self.info_frame, text="等级: 1", font=("Arial", 16, "bold"), bg='#2c3e50', fg='white')
        self.level_label.pack(pady=10)
        
        self.lines_label = tk.Label(self.info_frame, text="消除: 0 行", font=("Arial", 14), bg='#2c3e50', fg='#bdc3c7')
        self.lines_label.pack(pady=10)

        # 下一个方块预览
        self.preview_label = tk.Label(self.info_frame, text="下一个:", font=("Arial", 14), bg='#2c3e50', fg='white')
        self.preview_label.pack(pady=(30, 5))
        
        self.preview_canvas = tk.Canvas(self.info_frame, width=4*CELL_SIZE, height=4*CELL_SIZE, bg='#1a1a2e', highlightthickness=1, highlightbackground="#4a4a6a")
        self.preview_canvas.pack()

        # 重新开始按钮
        self.restart_btn = tk.Button(self.info_frame, text="重新开始", font=("Arial", 14), command=self.start_game, bg='#e74c3c', fg='white', relief=tk.FLAT)
        self.restart_btn.pack(pady=40, ipadx=10, ipady=5)

        # 绑定键盘事件
        self.root.bind("<KeyPress-Left>", self.move_left)
        self.root.bind("<KeyPress-Right>", self.move_right)
        self.root.bind("<KeyPress-Down>", self.move_down)
        self.root.bind("<KeyPress-Up>", self.rotate)
        self.root.bind("<space>", self.hard_drop)  # 新增：空格键一键到底

        self.start_game()

    def start_game(self):
        # 初始化游戏状态
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.speed = 800  # 初始速度变慢，800毫秒下落一次
        
        self.update_info()
        self.generate_next_piece()
        self.new_piece()
        
        if not self.game_over:
            self.draw_board()
            self.game_loop()

    def generate_next_piece(self):
        # 生成下一个方块的形状和颜色
        idx = random.randint(0, len(SHAPES) - 1)
        self.next_shape = [row[:] for row in SHAPES[idx]]
        self.next_color = COLORS[idx]
        self.draw_next_piece()

    def new_piece(self):
        # 将下一个方块变为当前方块
        self.current_shape = self.current_next_shape if hasattr(self, 'current_next_shape') else [row[:] for row in SHAPES[0]]
        self.current_color = self.current_next_color if hasattr(self, 'current_next_color') else COLORS[0]
        
        self.current_shape = [row[:] for row in self.next_shape]
        self.current_color = self.next_color
        
        # 生成新的下一个方块
        self.generate_next_piece()
        
        # 检查初始位置是否有效，无效则游戏结束
        if not self.valid_move(self.current_shape):
            self.game_over = True
            self.canvas.create_text(WIDTH/2, HEIGHT/2, text="GAME OVER", font=("Arial", 40, "bold"), fill="#e74c3c")

    def valid_move(self, shape):
        # 检查方块是否超出边界或与已有方块重叠
        for point in shape:
            x, y = point[1], point[0]
            if x < 0 or x >= COLS or y >= ROWS:
                return False
            if y >= 0 and self.board[y][x] != 0:
                return False
        return True

    def lock_piece(self):
        # 将当前方块固定到游戏板上
        for point in self.current_shape:
            x, y = point[1], point[0]
            if y >= 0:
                self.board[y][x] = self.current_color
        
        self.clear_lines()
        self.new_piece()

    def clear_lines(self):
        # 消除满行并计分
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines = ROWS - len(new_board)
        
        # 在顶部补上空行
        for _ in range(lines):
            new_board.insert(0, [0 for _ in range(COLS)])
            
        self.board = new_board
        
        if lines > 0:
            self.lines_cleared += lines
            # 消除行数越多，得分越高
            self.score += [0, 100, 300, 500, 800][lines]
            # 每消除10行升一级，速度加快
            self.level = self.lines_cleared // 10 + 1
            self.speed = max(100, 800 - (self.level - 1) * 80)  # 速度随等级提升，最快100ms
            self.update_info()

    def update_info(self):
        self.score_label.config(text=f"分数: {self.score}")
        self.level_label.config(text=f"等级: {self.level}")
        self.lines_label.config(text=f"消除: {self.lines_cleared} 行")

    def move_left(self, event=None):
        if not self.game_over:
            new_shape = [[p[0], p[1] - 1] for p in self.current_shape]
            if self.valid_move(new_shape):
                self.current_shape = new_shape

    def move_right(self, event=None):
        if not self.game_over:
            new_shape = [[p[0], p[1] + 1] for p in self.current_shape]
            if self.valid_move(new_shape):
                self.current_shape = new_shape

    def move_down(self, event=None):
        if not self.game_over:
            new_shape = [[p[0] + 1, p[1]] for p in self.current_shape]
            if self.valid_move(new_shape):
                self.current_shape = new_shape
                return True
            else:
                self.lock_piece()
                return False

    def hard_drop(self, event=None):
        # 空格键：直接落到底部
        if not self.game_over:
            while self.move_down():
                pass
            self.draw_board()

    def rotate(self, event=None):
        if not self.game_over:
            # 以第一个点为中心进行旋转
            pivot = self.current_shape[0]
            new_shape = []
            for point in self.current_shape:
                # 旋转公式
                new_x = point[0] - pivot[0] + pivot[1]
                new_y = pivot[0] - point[1] + pivot[0]
                new_shape.append([new_y, new_x])
                
            if self.valid_move(new_shape):
                self.current_shape = new_shape

    def draw_board(self):
        self.canvas.delete("all")
        
        # 绘制网格线（让空间感更强）
        for c in range(COLS + 1):
            self.canvas.create_line(c * CELL_SIZE, 0, c * CELL_SIZE, HEIGHT, fill='#2a2a4a', width=1)
        for r in range(ROWS + 1):
            self.canvas.create_line(0, r * CELL_SIZE, WIDTH, r * CELL_SIZE, fill='#2a2a4a', width=1)
        
        # 绘制已固定的方块
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] != 0:
                    self.draw_cell(self.canvas, c, r, self.board[r][c])
        
        # 绘制当前下落的方块
        if not self.game_over:
            for point in self.current_shape:
                x, y = point[1], point[0]
                if y >= 0:
                    self.draw_cell(self.canvas, x, y, self.current_color)

    def draw_next_piece(self):
        self.preview_canvas.delete("all")
        # 将预览方块居中绘制
        for point in self.next_shape:
            # 偏移量让方块在预览框居中
            x = point[1] - 3.5 
            y = point[0] - 0.5
            self.draw_cell(self.preview_canvas, x, y, self.next_color)

    def draw_cell(self, canvas, x, y, color):
        # 绘制单个方块，带有3D凸起效果
        x1 = x * CELL_SIZE
        y1 = y * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        # 底色
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')
        # 高光（左上）
        canvas.create_line(x1, y1, x2, y1, fill='white', width=2)
        canvas.create_line(x1, y1, x1, y2, fill='white', width=2)
        # 阴影（右下）
        canvas.create_line(x2, y1, x2, y2, fill='black', width=2)
        canvas.create_line(x1, y2, x2, y2, fill='black', width=2)

    def game_loop(self):
        if not self.game_over:
            self.move_down()
            self.draw_board()
            # 使用当前的speed控制下落速度
            self.root.after(self.speed, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    # 设置窗口背景色
    root.configure(bg='#2c3e50')
    game = Tetris(root)
    root.mainloop()
