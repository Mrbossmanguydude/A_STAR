import pygame
import math

ROWS = 20
COLS = 20
WIDTH = 500
HEIGHT = 500
CELL_SIZE = WIDTH // COLS
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A*")
pygame.display.set_icon(pygame.image.load("images\\Old stuff\\Astar_icon.png"))
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = col * CELL_SIZE
        self.y = row * CELL_SIZE
        self.color = WHITE
        self.neighbors = []
        self.g_score = float("inf")
        self.h_score = float("inf")
        self.f_score = float("inf")
        self.came_from = None

    def get_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        if pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE).collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.color = GREEN
            elif pygame.mouse.get_pressed()[1]:
                self.color = BLACK
            elif pygame.mouse.get_pressed()[2]:
                self.color = BLUE

    def update_neighbors(self):
        global grid
        if self.row > 0:
            above = grid[self.row - 1][self.col]
            if above.color != BLACK:
                self.neighbors.append(above)
        if self.row < ROWS - 1:
            below = grid[self.row + 1][self.col]
            if below.color != BLACK:
                self.neighbors.append(below)
        if self.col > 0:
            left = grid[self.row][self.col - 1]
            if left.color != BLACK:
                self.neighbors.append(left)
        if self.col < COLS - 1:
            right = grid[self.row][self.col + 1]
            if right.color != BLACK:
                self.neighbors.append(right)
    
def heuristic_euclidean(node1, node2):
    return math.sqrt((node1.row - node2.row)**2 + (node1.col - node2.col)**2)

def draw_grid(screen, rows, width):
    gap = width // rows 
    for i in range(rows):
        pygame.draw.line(screen, (128, 128, 128), (0, i* gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(screen, (128, 128, 128), (j * gap, 0), (j * gap, width))

def reconstruct_path(end_node):
    path = []
    current_node = end_node
    while current_node.came_from is not None:
        path.append(current_node)
        current_node = current_node.came_from
    path.append(current_node)
    return path

def a_star(start_node, end_node):
    open_nodes = []
    open_nodes.append(start_node)

    start_node.g_score = 0
    start_node.h_score = heuristic_euclidean(start_node, end_node)
    start_node.f_score = start_node.g_score + start_node.h_score

    while len(open_nodes) > 0:
        open_nodes.sort(key=lambda node: node.f_score)
        current_node = open_nodes.pop(0)
        if current_node == end_node:
            return reconstruct_path(end_node)

        current_node.update_neighbors()
        for neighbor in current_node.neighbors:
            if neighbor.color == BLACK:
                pass
            temp_gscore = current_node.g_score + 1
            if temp_gscore < neighbor.g_score:
                # Check if the node beneath the current one is an obstacle
                # if neighbor.row < ROWS - 1 and grid[neighbor.row + 1][neighbor.col].color == BLACK:
                neighbor.came_from = current_node
                neighbor.g_score = temp_gscore
                neighbor.h_score = heuristic_euclidean(neighbor, end_node)
                neighbor.f_score = neighbor.g_score + neighbor.h_score
                if neighbor not in open_nodes:
                    open_nodes.append(neighbor)
    return None

grid = [[Node(row, col) for col in range(COLS)] for row in range(ROWS)]

running = True

point_a = None
point_b = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and point_a is not None and point_b is not None:
                result = a_star(point_a, point_b)

                if result is not None:
                    for node in result[1:-1]:
                        node.color = YELLOW
                else:
                    print("No path found")

    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, grid[row][col].color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    draw_grid(screen, ROWS, WIDTH)

    for i in grid:
        for j in i:
            if j.color == GREEN and point_a != j:
                if point_a != None:
                    point_a.color = WHITE
                point_a = j
            elif j.color == BLUE and point_b != j:
                if point_b != None:
                    point_b.color = WHITE
                point_b = j

            j.get_clicked()
    pygame.display.update()

pygame.quit()