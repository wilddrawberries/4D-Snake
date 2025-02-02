


import pygame
import random
from collections import deque

# Constants
SCREEN_SIZE = 800

thenumber=20
GRID_SIZE = thenumber
CELL_SIZE = thenumber
MAX_Z = thenumber
MAX_W = thenumber
FPS = 10  ##SPEED OF THE GAME

# Directions mapping
DIRECTION_MAP = {
    pygame.K_UP: (0, -1, 0, 0),
    pygame.K_DOWN: (0, 1, 0, 0),
    pygame.K_LEFT: (-1, 0, 0, 0),
    pygame.K_RIGHT: (1, 0, 0, 0),
    pygame.K_w: (0, 0, 1, 0),
    pygame.K_s: (0, 0, -1, 0),
    pygame.K_a: (0, 0, 0, 1),
    pygame.K_d: (0, 0, 0, -1),
}

def greedy_move(snake):
    directions = [
        (1, 0, 0, 0), (-1, 0, 0, 0), (0, 1, 0, 0), (0, -1, 0, 0),
        (0, 0, 1, 0), (0, 0, -1, 0), (0, 0, 0, 1), (0, 0, 0, -1)
    ]
    
    best_move = None
    best_distance = float('inf')
    head = snake.body[0]

    for d in directions:
        new_pos = tuple(map(sum, zip(head, d)))
        if snake.is_within_bounds(new_pos) and new_pos not in snake.body:
            distance = heuristic(new_pos, snake.food)  # Use heuristic from A*
            if distance < best_distance: 
                best_distance = distance
                best_move = d

    return best_move if best_move else random.choice(directions)  # Fallback

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("4D Snake Game")
clock = pygame.time.Clock()
import heapq  # Needed for priority queue

def heuristic(a, b):
    """ Manhattan distance heuristic function """
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2]) + abs(a[3] - b[3])

def astar_move(snake):
    directions = [
        (1, 0, 0, 0), (-1, 0, 0, 0), (0, 1, 0, 0), (0, -1, 0, 0),
        (0, 0, 1, 0), (0, 0, -1, 0), (0, 0, 0, 1), (0, 0, 0, -1)
    ]
    
    start = snake.body[0]
    goal = snake.food
    visited = set()
    priority_queue = [(0, start, [])]  # (cost, position, path)

    while priority_queue:
        cost, current, path = heapq.heappop(priority_queue)

        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            return path[0] if path else None  # Return first move

        for d in directions:
            neighbor = tuple(map(sum, zip(current, d)))
            if neighbor not in visited and snake.is_within_bounds(neighbor) and neighbor not in snake.body:
                new_cost = cost + 1
                heapq.heappush(priority_queue, (new_cost + heuristic(neighbor, goal), neighbor, path + [d]))

    return random.choice(directions)  # Fallback random move

# Colors
def gradient_color(z, w, is_food=False):
    """
    Adjusts color based on depth (z) and dimension shift (w).
    - Snake becomes redder as `w` increases.
    - Food becomes greener as `w` increases.
    """
    intensity = max(0, min(1, (MAX_Z - z + 1) / MAX_Z))  # Clamps between 0 and 1
    w_factor = max(0, min(1, w / MAX_W))  # Clamps W between 0 and 1
    
    if 0: #is_food:
        return (
            int(50 * (1 - w_factor)),  # Less red as W increases
            int(255 * (1 - w_factor)),  # More green as W increases
            int(50 * (1 - w_factor))   # Keep some blue
        )
    
    return (
        int(255 * w_factor),   # More red as W increases
        int(200 * (1 - w_factor)),  # Less green as W increases
        int(100 * (1 - w_factor))   # Less blue as W increases
    )

import math  # Ensure this is at the top of your script

def draw_polygon(surface, x, y, size, color, sides):
    points = []
    angle_step = 360 / sides
    for i in range(sides):
        angle = math.radians(i * angle_step)  # Use math.radians here
        px = x + size * math.cos(angle)
        py = y + size * math.sin(angle)
        points.append((px, py))
    pygame.draw.polygon(surface, color, points)


# Snake Class
class Snake4D:
    def __init__(self):
        self.body = [(0, 0, 0, 0)]  # Starting position (x, y, z, w)
        self.direction = (1, 0, 0, 0)  # Initial direction
        self.alive = True
        self.food = self.generate_food()

    def move(self):
        if not self.alive:
            return
        head = self.body[0]
        new_head = tuple(map(sum, zip(head, self.direction)))

        if new_head in self.body or not self.is_within_bounds(new_head):
            self.alive = False  # Snake collided with itself or boundary
        else:
            self.body.insert(0, new_head)
            if new_head == self.food:
                self.food = self.generate_food()
            else:
                self.body.pop()

    def generate_food(self):
        while True:
            food = (
                random.randint(-GRID_SIZE+2, GRID_SIZE - 2),
                random.randint(-GRID_SIZE+2, GRID_SIZE - 2),
                random.randint(0, MAX_Z),
                random.randint(0, MAX_W)
            )
            if food not in self.body:
                return food

    def is_within_bounds(self, pos):
        x, y, z, w = pos
        return (
            -GRID_SIZE <= x < GRID_SIZE and
            -GRID_SIZE <= y < GRID_SIZE and
            0 <= z <= MAX_Z and
            0 <= w <= MAX_W
        )

    def change_direction(self, new_direction):
        if self.alive:
            self.direction = new_direction

# BFS AI
def bfs_move(snake):
    directions = [
        (1, 0, 0, 0), (-1, 0, 0, 0), (0, 1, 0, 0), (0, -1, 0, 0),
        (0, 0, 1, 0), (0, 0, -1, 0), (0, 0, 0, 1), (0, 0, 0, -1)
    ]
    random.shuffle(directions)
    start = snake.body[0]
    food = snake.food
    visited = set(snake.body)
    queue = deque([(start, [])])  # (current position, path)

    while queue:
        current, path = queue.popleft()

        if current == food:
            return path[0] if path else None  # First step towards the food

        for d in directions:
            neighbor = tuple(map(sum, zip(current, d)))
            if neighbor not in visited and snake.is_within_bounds(neighbor):
                visited.add(neighbor)
                queue.append((neighbor, path + [d]))

    return random.choice(directions)  # Random fallback move if no path

# Draw the snake
def draw_snake(snake):
    screen.fill((0, 0, 0))  # Clear screen
    
    # Draw border
    border_color = (0, 200, 0)  # Same green as the snake
    border_thickness = 5
    pygame.draw.rect(
        screen,
        border_color,
        (
            SCREEN_SIZE // 2 - GRID_SIZE * CELL_SIZE,
            SCREEN_SIZE // 2 - GRID_SIZE * CELL_SIZE,
            GRID_SIZE * 2 * CELL_SIZE,
            GRID_SIZE * 2 * CELL_SIZE
        ),
        border_thickness
    )
    
    # Initialize font
    font = pygame.font.Font(None, 28)  # Default font, size 28
    text_color = (255, 255, 255)  # White for contrast

    for (x, y, z, w) in snake.body:
        draw_segment(x, y, z, w)

    # Draw food
    draw_segment(*snake.food, is_food=True)

    # Display coordinates in the top-left corner
    coord_text = font.render(f"Head: ({snake.body[0][0]}, {snake.body[0][1]}, {snake.body[0][2]}, {snake.body[0][3]})", True, text_color)
    screen.blit(coord_text, (10, 10))  # Position in top-left corner
    coord_text = font.render(f"Food: ({snake.food[0]}, {snake.food[1]}, {snake.food[2]}, {snake.food[3]})", True, text_color)
    screen.blit(coord_text, (10, 40))  # Position in top-left corner

    pygame.display.flip()




def draw_segment(x, y, z, w, is_food=False):
    size = CELL_SIZE * ((MAX_Z - z + 1) / MAX_Z)  # Adjust size based on Z
    color = gradient_color(z, w, is_food)
    sides = max(3, MAX_W - w + 3)  # W determines polygon sides

    screen_x = SCREEN_SIZE // 2 + x * CELL_SIZE
    screen_y = SCREEN_SIZE // 2 + y * CELL_SIZE

    draw_polygon(screen, screen_x, screen_y, size, color, sides)

# Game Loop
snake = Snake4D()
running = True

while running and snake.alive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key in DIRECTION_MAP:
            snake.change_direction(DIRECTION_MAP[event.key])

    snake.move()
    draw_snake(snake)

    clock.tick(FPS)

pygame.quit()
