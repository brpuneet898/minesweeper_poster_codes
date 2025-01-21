import random
import time
import csv
import numpy as np
from datetime import datetime
from collections import deque
class Minesweeper:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.grid_size = self.get_grid_size()
        self.num_mines = self.get_num_mines()
        self.grid = self.generate_grid()
        self.visited = set()
        self.is_game_over = False
        self.is_game_won = False

    def get_grid_size(self):
        if self.difficulty == 'easy':
            return 10
        elif self.difficulty == 'medium':
            return 15
        else:
            return 20
    def get_num_mines(self):
        if self.difficulty == 'easy':
            return int(self.grid_size * self.grid_size * 0.1)  
        elif self.difficulty == 'medium':
            return int(self.grid_size * self.grid_size * 0.15)  
        else:
            return int(self.grid_size * self.grid_size * 0.2)  
    def generate_grid(self):
        grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        mines = random.sample(range(self.grid_size * self.grid_size), self.num_mines)
        for mine in mines:
            row, col = divmod(mine, self.grid_size)
            grid[row][col] = -1
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if grid[row][col] == -1:
                    continue
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if 0 <= row + dr < self.grid_size and 0 <= col + dc < self.grid_size:
                            if grid[row + dr][col + dc] == -1:
                                count += 1
                grid[row][col] = count
        return grid
    def make_move(self, row, col):
        if self.grid[row][col] == -1:
            self.is_game_over = True
            self.is_game_won = False
        else:
            self.visited.add((row, col))
            if self.grid[row][col] == 0:
                self.flood_fill(row, col)

    def flood_fill(self, row, col):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        stack = deque([(row, col)])
        while stack:
            r, c = stack.pop()
            if (r, c) in self.visited:
                continue
            self.visited.add((r, c))
            if self.grid[r][c] == 0:
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size and (nr, nc) not in self.visited:
                        stack.append((nr, nc))
    def check_win(self):
        return len(self.visited) == (self.grid_size * self.grid_size - self.num_mines)
    def reset_game(self):
        self.visited.clear()
        self.is_game_over = False
        self.is_game_won = False
        self.grid = self.generate_grid()

class HumanLikeAgent:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.game = Minesweeper(difficulty)
    def play_game(self):
        moves = 0
        start_time = time.time()
        while not self.game.is_game_over:
            unvisited_cells = [(r, c) for r in range(self.game.grid_size)
                               for c in range(self.game.grid_size) if (r, c) not in self.game.visited]
            if unvisited_cells:
                row, col = random.choice(unvisited_cells)
                self.game.make_move(row, col)
                moves += 1
            if self.game.check_win():
                self.game.is_game_over = True
                self.game.is_game_won = True
        end_time = time.time()
        total_time = end_time - start_time
        return total_time, moves

def simulate_games():
    results = []
    agent_id = 1
    difficulties = ['easy', 'medium', 'hard']
    for difficulty in difficulties:
        for _ in range(333333):
            agent = HumanLikeAgent(difficulty)
            time_taken, score = agent.play_game()
            result = 1 if agent.game.is_game_won else 0
            results.append([agent_id, difficulty, round(time_taken, 2), score, result])
            agent_id += 1
            agent.game.reset_game()
    with open('/content/human_game_results.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "difficulty", "time", "score", "result"])
        writer.writerows(results)

simulate_games()
print("Simulation complete. The results have been saved in 'human_game_results.csv'.")