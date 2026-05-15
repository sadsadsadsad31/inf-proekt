import random
import os
from typing import List, Tuple, Optional

class ConsoleMaze:
    
    def __init__(self, width: int = 21, height: int = 21):
        # Размеры должны быть нечётными для корректной генерации
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        self.maze = None
        self.player_pos = None
        self.start = None
        self.end = None
        self.steps = 0
        
    def generate(self):
        self.maze = [[1 for _ in range(self.width)] for _ in range(self.height)]
        
        # Начинаем с (1, 1)
        start_x, start_y = 1, 1
        self.maze[start_y][start_x] = 0
        
        stack = [(start_x, start_y)]
        
        while stack:
            x, y = stack[-1]
            
            neighbors = []
            for dx, dy in [(0, -2), (0, 2), (-2, 0), (2, 0)]:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.width - 1 and 0 < ny < self.height - 1:
                    if self.maze[ny][nx] == 1:
                        neighbors.append((nx, ny, dx // 2, dy // 2))
            
            if neighbors:
                nx, ny, wall_dx, wall_dy = random.choice(neighbors)
                self.maze[y + wall_dy][x + wall_dx] = 0
                self.maze[ny][nx] = 0
                stack.append((nx, ny))
            else:
                stack.pop()
        
        # вход и выход
        self.start = (1, 0)
        self.end = (self.width - 2, self.height - 1)
        self.maze[0][1] = 0  # Вход
        self.maze[self.height - 1][self.width - 2] = 0  # Выход
        
        self.player_pos = list(self.start)
        self.steps = 0
        
        return self.maze
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def draw(self):
        result = []
        result.append("=" * (self.width + 4))
        result.append("Используйте WASD для движения. Q - выход")
        result.append("=" * (self.width + 4))
        
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                if (x, y) == tuple(self.player_pos):
                    line += "🧙"  # Игрок
                elif (x, y) == self.end:
                    line += "🚪"  # Выход
                elif (x, y) == self.start:
                    line += "🚪"  # Вход
                elif self.maze[y][x] == 1:
                    line += "██"  # Стена
                else:
                    line += "  "  # Проход
            result.append(line)
        
        result.append("-" * (self.width + 4))
        result.append(f"Шагов сделано: {self.steps}")
        
        dx = self.end[0] - self.player_pos[0]
        dy = self.end[1] - self.player_pos[1]
        if dx > 0:
            result.append("💡 Выход → справа")
        elif dx < 0:
            result.append("💡 Выход ← слева")
        elif dy > 0:
            result.append("💡 Выход ↓ снизу")
        elif dy < 0:
            result.append("💡 Выход ↑ сверху")
        
        print("\n".join(result))
    
    def move(self, dx: int, dy: int):
        """перемещение"""
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        
        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            if self.maze[new_y][new_x] == 0:
                self.player_pos = [new_x, new_y]
                self.steps += 1
                return True
            else:
                print("\n🔇 Стена! Нельзя пройти.")
                input("Нажмите Enter...")
                return False
        return False
    
    def check_win(self) -> bool:
        if tuple(self.player_pos) == self.end:
            self.clear_screen()
            print("=" * 50)
            print("🎉🎉🎉 ПОБЕДА! 🎉🎉🎉")
            print(f"Вы вышли из лабиринта за {self.steps} шагов!")
            print("=" * 50)
            return True
        return False
    
    def run(self):
        """главный игр. цикл"""
        self.generate()
        
        print("Генерация лабиринта...")
        input("Нажмите Enter для начала игры...")
        
        running = True
        while running:
            self.clear_screen()
            self.draw()
            
            if self.check_win():
                break
            
            key = input("\nВаш ход (W/A/S/D или Q): ").strip().lower()
            
            if key == 'q':
                print("Выход из игры. До встречи!")
                running = False
            elif key == 'w':
                self.move(0, -1)
            elif key == 's':
                self.move(0, 1)
            elif key == 'a':
                self.move(-1, 0)
            elif key == 'd':
                self.move(1, 0)
            else:
                print("Неизвестная команда! Используйте W/A/S/D или Q")
                input("Нажмите Enter...")


class AutoSolverMaze:
    
    def __init__(self, width: int = 51, height: int = 51):
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        self.maze = None
        
    def generate(self):
        self.maze = [[1 for _ in range(self.width)] for _ in range(self.height)]
        
        start_x, start_y = 1, 1
        self.maze[start_y][start_x] = 0
        stack = [(start_x, start_y)]
        
        while stack:
            x, y = stack[-1]
            neighbors = []
            for dx, dy in [(0, -2), (0, 2), (-2, 0), (2, 0)]:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.width - 1 and 0 < ny < self.height - 1:
                    if self.maze[ny][nx] == 1:
                        neighbors.append((nx, ny, dx // 2, dy // 2))
            
            if neighbors:
                nx, ny, wall_dx, wall_dy = random.choice(neighbors)
                self.maze[y + wall_dy][x + wall_dx] = 0
                self.maze[ny][nx] = 0
                stack.append((nx, ny))
            else:
                stack.pop()
        
        self.maze[0][1] = 0
        self.maze[self.height - 1][self.width - 2] = 0
        
        return self.maze
    
    def solve_astar(self):
        start = (1, 0)
        end = (self.width - 2, self.height - 1)
        
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        def get_neighbors(pos):
            x, y = pos
            neighbors = []
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.maze[ny][nx] == 0:
                        neighbors.append((nx, ny))
            return neighbors
        
        import heapq
        open_set = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, end)}
        open_set_hash = {start}
        
        while open_set:
            current = heapq.heappop(open_set)[1]
            open_set_hash.remove(current)
            
            if current == end:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path
            
            for neighbor in get_neighbors(current):
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, end)
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)
        return None
    
    def draw_text_maze(self, path=None):
        result = []
        result.append("+" + "-" * self.width + "+")
        
        for y in range(self.height):
            line = "|"
            for x in range(self.width):
                if path and (x, y) in path:
                    line += "●"
                elif (x, y) == (1, 0):
                    line += "▶"
                elif (x, y) == (self.width - 2, self.height - 1):
                    line += "◀"
                elif self.maze[y][x] == 1:
                    line += "#"
                else:
                    line += " "
            line += "|"
            result.append(line)
        
        result.append("+" + "-" * self.width + "+")
        return "\n".join(result)
    
    def run_auto(self):
        print("Генерация лабиринта...")
        self.generate()
        
        print("Поиск пути алгоритмом A*...")
        path = self.solve_astar()
        
        if path:
            print(f"\n✅ Путь найден! Длина: {len(path)} шагов\n")
            print(self.draw_text_maze(path))
            print(f"\n📊 Статистика: Лабиринт {self.width}x{self.height}, длина пути {len(path)}")
        else:
            print("❌ Путь не найден!")


def main():
    print("=" * 60)
    print("ЛАБИРИНТ - Выберите режим")
    print("=" * 60)
    print("1. Интерактивный режим (играть самому, управление WASD)")
    print("2. Автоматический режим (программа найдёт путь сама)")
    print("=" * 60)
    
    choice = input("Ваш выбор (1 или 2): ").strip()
    
    if choice == "1":
        print("\nЗапуск интерактивного режима...")
        print("Размер лабиринта: 21x21 (можно изменить в коде)")
        game = ConsoleMaze(width=21, height=21)
        game.run()
    elif choice == "2":
        print("\nЗапуск автоматического режима...")
        print("Размер лабиринта: 31x31")
        solver = AutoSolverMaze(width=31, height=31)
        solver.run_auto()
    else:
        print("Неверный выбор!")

if __name__ == "__main__":
    main()