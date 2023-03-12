import pygame
pygame.init()

WIDTH, HEIGHT = 700,500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

refresh_rate = 240

WHITE =(255,255,255)
BLACK = (0,0,0)

WINNING_LIMIT = 10

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7 

SCORE_FONT = pygame.font.SysFont("comicsans", 50)

KEYSTATE = None

class Ball:
    COLOR = WHITE
    MAX_VEL = 5
    """saving attributes to the ball"""
    def __init__(self, x, y, radius):
        self.x =self.origin_x= x
        self.y =self.origin_y= y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.origin_x
        self.y = self.origin_y
        self.y_vel = 0
        self.x_vel *= -1

class Paddle: 
    COLOR = WHITE
    PADDLE_VELOCITY = 1
    """saving attributes related to the paddles"""
    def __init__(self, x, y, width, height): #initilizing variables
        self.x = self.origin_x = x
        self.y = self.origin_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.PADDLE_VELOCITY
        else:
            self.y += self.PADDLE_VELOCITY

    def reset(self):
        self.x = self.origin_x
        self.y = self.origin_y
        KEYSTATE = False


def draw(win, ball,left_player, right_player, paddles=[], ): #construct the pygame window
    win.fill(BLACK) #fill the window with white

    left_score_text = SCORE_FONT.render(f"{left_player}",1,WHITE)
    right_score_text = SCORE_FONT.render(f"{right_player}",1,WHITE)
    win.blit(left_score_text, (WIDTH//4- left_score_text.get_width()//2,20))
    win.blit(right_score_text, (WIDTH*(3/4)- right_score_text.get_width()//2,20))
    
    for paddle in paddles: #drawing multiple paddles
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 -5, i, 10, HEIGHT//20))
    
    ball.draw(win)

    pygame.display.update() #updating the window

def handle_paddle_movement(input_keys, left_paddle, right_paddle): 
    """Handles the paddle movement"""
    
    if input_keys[pygame.K_w] and left_paddle.y != 0:
        left_paddle.move(up=True)
    if input_keys[pygame.K_s] and left_paddle.y != HEIGHT-PADDLE_HEIGHT:
        left_paddle.move(up=False)
    if input_keys[pygame.K_UP] and right_paddle.y != 0:
        right_paddle.move(up=True)
    if input_keys[pygame.K_DOWN] and right_paddle.y != HEIGHT-PADDLE_HEIGHT:
        right_paddle.move(up=False)
    if input_keys[pygame.K_r]:
        left_paddle.y = HEIGHT//2 - PADDLE_HEIGHT//2
        right_paddle.y = HEIGHT//2 - PADDLE_HEIGHT//2

def handle_collisions(left_paddle, right_paddle, ball):

    if ball.x == WIDTH-10-PADDLE_WIDTH and ball.y >= right_paddle.y and ball.y <= right_paddle.y+PADDLE_HEIGHT:
        ball.x_vel = -1*(ball.x_vel)
        ball.y_vel = 0.05*((right_paddle.y+ PADDLE_HEIGHT//2)-ball.y )
        
    if ball.x == 10+PADDLE_WIDTH and ball.y >= left_paddle.y and  ball.y <= left_paddle.y+PADDLE_HEIGHT:
        ball.x_vel = -1*ball.x_vel
        ball.y_vel = 0.05*(left_paddle.y+PADDLE_HEIGHT//2-ball.y )
    if ball.y - BALL_RADIUS <= 0 :
        ball.y_vel *= -1
        
    if ball.y + BALL_RADIUS >= HEIGHT:
        ball.y_vel *= -1
        
    

    
def main():

    WINNER = None

    run = True #boolean variable assigned to see the state of the loop
    clock = pygame.time.Clock() 

    #positioning the paddles
    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH-10-PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    #positioning the ball
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)
    #scoring
    left_player = 0
    right_player = 0
    while run:
        KEYSTATE = True
        clock.tick(refresh_rate)
        draw(WIN,ball,left_player, right_player, [right_paddle,left_paddle]) #drawing the window @ 60 hz
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        if KEYSTATE :
            input_keys = pygame.key.get_pressed()

        handle_paddle_movement(input_keys, left_paddle, right_paddle)

        ball.move()
        handle_collisions(left_paddle, right_paddle, ball)
        
        if ball.x == 0:
            right_player += 1
            ball.reset()
             
        if ball.x == WIDTH:
            left_player += 1
            ball.reset()

        if left_player == WINNING_LIMIT:
            WINNER = True

        if right_player == WINNING_LIMIT:
            WINNER = True

        if WINNER:
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
    pygame.quit()

if __name__ == '__main__':
    main()
