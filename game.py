import pygame, sys, random
# tạo hàm trò chơi
def draw_floor():
    screen.blit(floor, (floor_x_pos,650))
    screen.blit(floor, (floor_x_pos+432,650))
def create_pipe():
    random_pipe_pos = random.choice(pipe_hei)
    bottom_pipe = pipe_sur.get_rect(midtop = (500,random_pipe_pos))
    top_pipe = pipe_sur.get_rect(midtop = (500,random_pipe_pos-650))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
    for pipe in pipes :
        pipe.centerx -= 5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_sur, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_sur,False,True)
            screen.blit(flip_pipe, pipe)
def check_col(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
            return False
    return True 
def rotate_bird(bird1):
    new_bird =pygame.transform.rotozoom(bird1,bird_move*3,1)
    return new_bird
def bird_an():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect  
def score_dis(game_state):
    if game_state == 'main game':
        score_sur = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_sur.get_rect(center = (216,100))
        screen.blit(score_sur,score_rect)
    if game_state == 'game over':
        score_sur = game_font.render(f'High Score: {(int(high_score))}',True,(255,255,255))
        score_rect = score_sur.get_rect(center = (216,610))
        screen.blit(score_sur,score_rect)

        high_score_sur = game_font.render(f'Score: {(int(score))}',True,(255,255,255))
        high_score_rect = high_score_sur.get_rect(center = (216,500))
        screen.blit(high_score_sur,high_score_rect)
def up_sco(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen = pygame.display.set_mode((432,768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)
# tạo biến trò chơi
gravity = 0.25
bird_move = 0
game_ac = True
score = 0
high_score = 0
# phông
bg = pygame.image.load('assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)
# sàn
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
# chim
bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down,bird_mid,bird_up]
bird_index = 0
bird = bird_list[bird_index] 
# bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100,384))
# timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap,200)
# ống
pipe_sur = pygame.image.load('assets/pipe-green.png').convert()
pipe_sur = pygame.transform.scale2x(pipe_sur)
pipe_list = []
# tạo timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_hei = [150,250,350]
# bg end
game_over_sur = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_sur.get_rect(center= (216,384))
# sound
flap_sound = pygame.mixer.Sound('sound/5_Flappy_Bird_sound_sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/5_Flappy_Bird_sound_sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/5_Flappy_Bird_sound_sfx_point.wav')
score_sound_countdown = 100
# vòng lặp
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_ac:
                bird_move = 0
                bird_move = -11
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_ac == False:
                game_ac = True
                pipe_list.clear()
                bird_rect.center = (100,384)
                bird_move = 0
                score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index= 0
            bird, bird_rect = bird_an()

    screen.blit(bg, (0,0))
    if game_ac:
        # chim
        bird_move += gravity
        ro_bird = rotate_bird(bird)
        bird_rect.centery += bird_move
        screen.blit(ro_bird, bird_rect)
        game_ac = check_col(pipe_list)
        # ống
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_dis('main game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_sur,game_over_rect)
        high_score = up_sco(score,high_score)
        score_dis('game over')
    # sàn
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120)