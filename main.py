import pygame

# Initialize game
pygame.init()

# Set display
# Variables
WIDTH, HEIGHT = 700, 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

FPS = 60

WHITE = (255,255,255)
BLACK = (0,0,0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100

BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 10

class Paddle:

    COLOR = WHITE
    VELOCITY = 7

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    
    MAX_VELOCITY = 3
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VELOCITY
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


# Draw window function, takes in window and list of paddles, called in main function
def draw(win, paddles, ball, left_score, right_score):
    # Background
    win.fill(BLACK)

    # Score
    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

    # Paddles
    for paddle in paddles:
        paddle.draw(win)

    # Middle dotted line
    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))

    # Ball
    ball.draw(win)

    pygame.display.update()


# Handle ball collision for ceiling/floor and paddle
def handle_collision(ball, left_paddle, right_paddle):
    # Floor
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    # Ceiling
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    # Left Paddle
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VELOCITY
                y_vel = difference_in_y /reduction_factor
                ball.y_vel = -1 * y_vel

    # Right Paddle
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VELOCITY
                y_vel = difference_in_y /reduction_factor
                ball.y_vel = -1 * y_vel


# Takes in paddles and uses key strokes to move them, called in main function
def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_i] and right_paddle.y - right_paddle.VELOCITY >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_k] and right_paddle.y + right_paddle.VELOCITY + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)


# Main function
def main():
    run = True
    clock = pygame.time.Clock()

    # Initialize Variables
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)
    left_score = 0
    right_score = 0


    # Game loop
    while run:

        # Run 60 frames per a second
        clock.tick(FPS)

        if ball.x < 0:
            right_score += 1
            left_paddle.reset()
            right_paddle.reset()
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            left_paddle.reset()
            right_paddle.reset()
            ball.reset()

        # Draw window
        draw(WINDOW, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():

            # Check for quit
            if event.type == pygame.QUIT:
                run = False
                break
            
        # Get keys pressed for paddle movement
        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        # Move ball
        ball.move()

        # Handle collisions
        handle_collision(ball, left_paddle, right_paddle)

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"

        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"
        
        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WINDOW.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()


if __name__ == '__main__':
    main()