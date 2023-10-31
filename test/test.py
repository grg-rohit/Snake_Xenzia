import pygame
import random

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initial game speed
INITIAL_SPEED = 10

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.score = 0
        self.speed = INITIAL_SPEED  # Initial speed

    def move(self, food):
        new_head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])

        # Check for collision with food
        if new_head == food:
            self.body.insert(0, new_head)
            self.score += 1
            if self.score % 5 == 0:
                self.speed += 1  # Increase speed every 5 points
            return True
        else:
            self.body.insert(0, new_head)
            self.body.pop()
            return False

    def change_direction(self, new_direction):
        # Disallow reversing direction
        if (new_direction[0], new_direction[1]) != (-self.direction[0], -self.direction[1]):
            self.direction = new_direction

class Food:
    def __init__(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.snake = Snake()
        self.food = Food()
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.paused = False
        self.menu_active = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction(RIGHT)
                elif event.key == pygame.K_ESCAPE:
                    if not self.menu_active:
                        self.show_menu()
                    else:
                        self.menu_active = False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused  # Toggle pause when 'P' is pressed

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, BLACK, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, BLACK, (0, y), (SCREEN_WIDTH, y))

    def draw_snake(self):
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def draw_food(self):
        pygame.draw.rect(self.screen, RED, (self.food.position[0] * GRID_SIZE, self.food.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def draw_score(self):
        font = pygame.font.Font(None, 18)
        text = font.render("Score: " + str(self.snake.score), True, WHITE)
        self.screen.blit(text, (10, 10))

    def check_collision(self):
        if self.snake.body[0] in self.snake.body[1:]:
            return True
        if (
            self.snake.body[0][0] < 0
            or self.snake.body[0][0] >= GRID_WIDTH
            or self.snake.body[0][1] < 0
            or self.snake.body[0][1] >= GRID_HEIGHT
        ):
            return True
        return False

    def show_game_over(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 48)
        text = font.render("Game Over", True, WHITE)
        score_text = font.render("Score: " + str(self.snake.score), True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 20))
        pygame.display.update()
        pygame.time.wait(2000)  # Wait for 2 seconds before exiting
        self.game_over = True

    def run(self):
        while not self.game_over:
            if not self.paused and not self.menu_active:
                self.handle_events()
                self.game_over = self.check_collision()
                if not self.game_over:
                    food_eaten = self.snake.move(self.food.position)
                    if food_eaten:
                        self.food.randomize_position()

            self.screen.fill((0, 0, 0))
            self.draw_grid()
            self.draw_food()
            self.draw_snake()
            self.draw_score()
            pygame.display.update()
            self.clock.tick(self.snake.speed)  # Adjust the game speed

        self.show_game_over()

    def show_menu(self):
        self.menu_active = True
        while self.menu_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.fill((0, 0, 0))
            pygame.draw.rect(self.screen, WHITE, (50, 100, 300, 200))
            font = pygame.font.Font(None, 36)

            # Check if the mouse is hovering over the buttons
            mouse = pygame.mouse.get_pos()
            resume_hover = 180 + 100 > mouse[0] > 180 and 120 + 50 > mouse[1] > 120
            exit_hover = 180 + 100 > mouse[0] > 180 and 170 + 50 > mouse[1] > 170

            # Increase the font size on hover
            resume_font_size = 38 if resume_hover else 36
            exit_font_size = 38 if exit_hover else 36

            resume_text = pygame.font.Font(None, resume_font_size).render("Resume", True, (0, 0, 0))
            exit_text = pygame.font.Font(None, exit_font_size).render("Exit", True, (0, 0, 0))

            self.screen.blit(resume_text, (180, 120))
            self.screen.blit(exit_text, (180, 170))

            click = pygame.mouse.get_pressed()

            if resume_hover:
                if click[0] == 1:
                    self.menu_active = False

            if exit_hover:
                if click[0] == 1:
                    pygame.quit()
                    quit()

            pygame.display.update()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
    pygame.quit()
