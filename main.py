import pygame

# Initialize game
pygame.init()

# Set display
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

def main():
    run = True

    # Game loop
    while run:
        for event in pygame.event.get():

            # Check for quit
            if event.type == pygame.QUIT:
                run = False
                break
    

    pygame.quit()

if __name__ == '__main__':
    main()