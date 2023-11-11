import pygame

# Initialize game
pygame.init()

# Set display
# Variables
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

class Paddle:

    COLOR = WHITE

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))


# Draw window function
def draw(win, paddles):
    # Background
    win.fill(BLACK)

    # Paddles
    for paddle in paddles:
        paddle.draw(win)

    pygame.display.update()


# Main function
def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    # Game loop
    while run:

        # Run 60 frames per a second
        clock.tick(FPS)

        # Draw window
        draw(WIN, [left_paddle, right_paddle])

        for event in pygame.event.get():

            # Check for quit
            if event.type == pygame.QUIT:
                run = False
                break
    

    pygame.quit()

if __name__ == '__main__':
    main()