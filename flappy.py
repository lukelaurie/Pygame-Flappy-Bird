import pygame, os, random
pygame.font.init()

# Width, height and creating the window, and global vars
WHITE = (255, 255, 255)
YELLOW = (190, 190, 50)
WIDTH, HEIGHT = 600, 900
BIRD_WIDTH, BIRD_HEIGHT = 50, 50
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
GRAVITY = 5
VELOCITY_Y = 10
jump = False
new_pipe = True
new_pipe_other = True
x_location = 700
x_location_again = 1100
start = False
total = 0
total_points = 0
#Sets the title
pygame.display.set_caption("Flappy Bird")

#Gets the background Image
BACKGROUND = pygame.image.load(os.path.join('images', 'background.png'))
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))
FLOOR = pygame.image.load(os.path.join('images', 'ground.png'))
FLOOR_IMAGE = pygame.transform.scale(FLOOR, (WIDTH, 130))
FLOOR_RECT = pygame.Rect(0, 770, WIDTH, 130)
# Gets the bird images
bird_down = pygame.image.load(os.path.join('images', 'bird_wing_down.png'))
bird_up = pygame.image.load(os.path.join('images', 'bird_wing_up.png'))
# makes the images bigger
bird_wing_down = pygame.transform.scale(bird_down, (BIRD_WIDTH, BIRD_HEIGHT))
bird_wing_up = pygame.transform.scale(bird_up, (BIRD_WIDTH, BIRD_HEIGHT))
# pipe images
PIPE_BODY = pygame.image.load(os.path.join('images', 'pipe_body.png'))
PIPE_END_IMAGE = pygame.image.load(os.path.join('images', 'pipe_end.png'))
# starting image
STARTING = pygame.image.load(os.path.join('images', 'message.png'))
STARTING_IMAGE = pygame.transform.scale(STARTING, (368, 534))
# game over image
GAME_OVER = pygame.image.load(os.path.join('images', 'gameover.png'))
GAME_OVER_IMAGE = pygame.transform.scale(GAME_OVER, (384, 84))
# creates the restart image
RESTART_OVER = pygame.image.load(os.path.join('images', 'restart.png'))
# creates the score text
SCORE_FONT = pygame.font.SysFont('Sledge', 90)
ENDING_FONT = pygame.font.SysFont('Arial', 70)

def starting_screen():
    '''
    Creates the starting screen
    '''
    global start
    while start == False:
        WIN.blit(STARTING_IMAGE, ((WIDTH/2)-170, 150))
        pygame.display.update()
        #checks if button is pressed
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                start = True
            if event.type == pygame.QUIT:
                start = True
                pygame.quit()

def draw_window(bird, bird_type):
    '''
    This correctly displays all of the objects on the screen.
    bird: Location of bird image
    '''
    global x_location, x_location_again
    global new_pipe, new_pipe_other
    # sets the background image
    WIN.blit(BACKGROUND_IMAGE, (0,0))
    WIN.blit(FLOOR_IMAGE, (0, 770))
    starting_screen()
    #bird images
    WIN.blit(bird_type, (bird.x, bird.y))
    if x_location <= -80:
        x_location = 700
        new_pipe = True
    if x_location_again <= -80:
        x_location_again = 700
        new_pipe_other = True
    draw_pipe()
    draw_pipe_again()
    # displays the current score text
    current_text = SCORE_FONT.render(str(total_points), 1, WHITE)
    WIN.blit(current_text, (WIDTH/2-20, 20))
    pygame.display.update()

def draw_pipe():
    '''
    Draws the pipes at random y coordinates
    '''
    #sets needed global variables
    global new_pipe, pipe_height, x_location
    global top_pipe_rect, bottom_pipe_rect, winner_rect
    # gets random index for the pipe
    if new_pipe is True:
        pipe_height = random.randint(50, 510)
        new_pipe = False
    # Sets rectangles of pipes
    top_pipe_rect = pygame.Rect(x_location,0, 80, pipe_height)
    bottom_pipe_rect = pygame.Rect(x_location, 770 - (520 - pipe_height), 80, 520 - pipe_height)
    # gets the point adding rectangle
    winner_rect = pygame.Rect(x_location + 40, pipe_height, 1, 230)

    # Sets pipes to their correct positions
    top_pipe_image = pygame.transform.scale(PIPE_BODY, (80, pipe_height))
    bottom_pipe_image = pygame.transform.rotate(pygame.transform.scale(PIPE_BODY, (80, 520 - pipe_height)), 180)
    WIN.blit(top_pipe_image, (top_pipe_rect.x, 0))
    WIN.blit(bottom_pipe_image, (bottom_pipe_rect.x, 770 - (520 - pipe_height)))
    WIN.blit(PIPE_END_IMAGE, (top_pipe_rect.x, pipe_height))
    WIN.blit(PIPE_END_IMAGE, (bottom_pipe_rect.x, 770 - (520 - pipe_height+ 32)))
    x_location -= 4

def draw_pipe_again():
    '''
    Draws the pipes at random y coordinates
    '''
    #sets needed global variables
    global new_pipe_other, new_pipe_height, x_location_again
    global other_top_pipe_rect, other_bottom_pipe_rect, other_winner_rect
    # gets random index for the pipe
    if new_pipe_other is True:
        new_pipe_height = random.randint(50, 510)
        new_pipe_other = False

    other_top_pipe_rect = pygame.Rect(x_location_again,0, 80, new_pipe_height)
    other_bottom_pipe_rect = pygame.Rect(x_location_again, 770 - (520 - new_pipe_height), 80, 520 - new_pipe_height)
    other_winner_rect = pygame.Rect(x_location_again + 40, new_pipe_height, 1, 230)

    # Sets pipes to their correct positions
    top_pipe_image = pygame.transform.scale(PIPE_BODY, (80, new_pipe_height))
    bottom_pipe_image = pygame.transform.rotate(pygame.transform.scale(PIPE_BODY, (80, 520 - new_pipe_height)), 180)
    WIN.blit(top_pipe_image, (x_location_again, 0))
    WIN.blit(bottom_pipe_image, (x_location_again, 770 - (520 - new_pipe_height)))
    WIN.blit(PIPE_END_IMAGE, (x_location_again, new_pipe_height))
    WIN.blit(PIPE_END_IMAGE, (x_location_again, 770 - (520 - new_pipe_height+ 32)))
    x_location_again -= 4

def bird_collide(top_pipe, bottom_pipe, other_top_pipe, other_bottom_pipe, bird):
    '''
    Checks if the bird collides with anything and determines that the player lost if they did.
    top pipe: top pipe rectangle
    bottom pipe: bottom pipe rectangle
    bird: the bird rectangle
    '''
    global total_points, total
    # checks if bird collides with the floor or the pipes
    if bird.colliderect(FLOOR_RECT):
        game_ending()
    elif bird.colliderect(top_pipe):
        game_ending()
    elif bird.colliderect(bottom_pipe):
        game_ending()
    elif bird.colliderect(other_top_pipe):
        game_ending()
    elif bird.colliderect(other_bottom_pipe):
        game_ending()
    elif bird.colliderect(winner_rect) or bird.colliderect(other_winner_rect):
        total += 1
        if total % 13 == 1:
            total_points += 1

def game_ending():
    '''
    displays the game over screen with the correct scoring.
    '''
    global total_points, total, VELOCITY_Y, jump, new_pipe_other, new_pipe, start, \
        x_location_again, x_location
    clock = pygame.time.Clock()
    #creates the rectangle
    restart_rect = pygame.Rect(WIDTH / 2 - 66, 570, 132, 45)
    while True:
        # displays all the ending images
        clock.tick(FPS)
        WIN.blit(BACKGROUND_IMAGE, (0, 0))
        WIN.blit(FLOOR_IMAGE, (0, 770))
        WIN.blit(GAME_OVER_IMAGE, ((WIDTH / 2) - 192, 150))
        #ending text
        ending_text = SCORE_FONT.render("SCORE", 1, YELLOW)
        WIN.blit(ending_text, (WIDTH / 2 - 110, 250))
        best_text = SCORE_FONT.render("BEST", 1, YELLOW)
        WIN.blit(best_text, (WIDTH / 2 - 80, 400))
        # score text
        ending_score_text = SCORE_FONT.render(str(total_points), 1, WHITE)
        if int(total_points) >= 10:
            WIN.blit(ending_score_text, (WIDTH / 2 - 40, 320))
        else:
            WIN.blit(ending_score_text, (WIDTH / 2 - 20, 320))
        record_text = SCORE_FONT.render(str(current_record()), 1, WHITE)
        # gets x location for record
        if int(current_record()) >= 10:
            WIN.blit(record_text, (WIDTH / 2 - 40, 470))
        else:
            WIN.blit(record_text, (WIDTH / 2 - 20, 470))
        # displays restart button
        WIN.blit(RESTART_OVER, (WIDTH / 2 - 66, 570))
        pygame.display.update()
        for event in pygame.event.get():
            # checks if the user quit
            if event.type == pygame.QUIT:
                pygame.quit()
            # checks to see if restart rectangle is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                # Checks if user point collides with the rectangle
                if restart_rect.collidepoint(mouse_position):
                    total_points = 0
                    total = 0
                    VELOCITY_Y = 10
                    jump = False
                    new_pipe = True
                    new_pipe_other = True
                    x_location = 700
                    x_location_again = 1100
                    start = False
                    main()


def current_record():
    '''
    This finds out the current record
    '''
    # opens flappy_record text file and checks if the score was a record.
    flappy_record = open("flappy_bird.txt", "r")
    point_record = flappy_record.readline()
    if point_record == "":
        point_record = 0
    if total_points > int(point_record):
        flappy_record.close()
        point_record = total_points
        flappy_record = open("flappy_bird.txt", "w")
        flappy_record.writelines(str(point_record))
        flappy_record.close()
    return point_record

def main():
    # Creates boxes representing the birds
    bird_location = pygame.Rect(200, 450- BIRD_HEIGHT, BIRD_WIDTH, BIRD_HEIGHT)
    #gets fps and runs loop
    clock = pygame.time.Clock()
    run = True
    i = 0
    # creates needed jumping variables
    jump = False
    total = 0
    global VELOCITY_Y
    while run:
        clock.tick(FPS)
        # gets each event
        for event in pygame.event.get():
            # checks if the user quit
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and jump is False:
                    jump = True
                    total = 0

        if jump is True:
            bird_location.y -= VELOCITY_Y
            if total > 20:
                jump = False
                VELOCITY_Y = 10
            total += 1

        i += .03 -int(i)
        #draws the bird at an angle
        angle = total
        if jump == False:
            angle = - total
        if i >= 0.5:
        # animates the bird
            draw_window(bird_location, pygame.transform.rotate(bird_wing_up, angle * 2))
            #causes the bird to be falling
        else:
            draw_window(bird_location, pygame.transform.rotate(bird_wing_down, angle * 2))
        bird_location.y += GRAVITY
        # checks for bird collision
        bird_collide(top_pipe_rect, bottom_pipe_rect, other_top_pipe_rect, other_bottom_pipe_rect, bird_location)

main()
