# libraries
from classes import *
from gpiozero import Button

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

window_width = 700
window_height = 700
size = (window_width, window_height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Galaxy')
background = pygame.image.load('/home/raspbian/Desktop/galaxy/photos/space.png')

END = False

clock = pygame.time.Clock()

laser_sound = pygame.mixer.Sound("/home/raspbian/Desktop/galaxy/sound/laser.wav")
menu = True
choice = 1
choice_return = 1

menuWindow = pygame.Surface((500, 180))
menuFont = pygame.font.SysFont('Calibri', 25, True, False)

option1 = menuFont.render("Start game", True, BLACK)
option2 = menuFont.render("Exit", True, BLACK)
option3 = menuFont.render("Restart", True, BLACK)

guiFont = pygame.font.SysFont('Calibri', 15, True, False)

player = Player()
player.x = 330
player.y = 550

bullets = []

enemies = []
counter = 0
global_counter = 0
acceleration = 0
points = 0
life = 20


def displayBar():
    pygame.draw.rect(screen, (100, 100, 100), [0, 0, window_width, 30])
    pointsText = guiFont.render('Points: ' + str(points), True, BLACK)
    screen.blit(pointsText, [25, 5])


def displayLife():
    pygame.draw.rect(screen, (255, 0, 0), [0, 30, window_width * (life / 20), 30])
    lifePoints = guiFont.render(str(life) + '/20', True, WHITE)
    screen.blit(lifePoints, [window_width / 2 - 15, 35])


def displayScore():
    lost = menuFont.render('GAME OVER', True, RED)
    screen.blit(lost, [30, 35])
    score = menuFont.render('Number of points scored: ' + str(points), True, RED)
    screen.blit(score, [30, 65])


GAME = True
GAME_STATE = 0  # [0, 1 or 2]
music = pygame.mixer.Sound('/home/raspbian/Desktop/galaxy/sound/g-m.mp3')  # Provide the path to your sound file
music.play(-1)

buttons = {
    "up": Button(27),
    "down": Button(5),
    "left": Button(17),
    "right": Button(22),
    "start": Button(6),
    #"select": Button(13),
    #"x": Button(26),
    #"y": Button(19),
    #"b": Button(3),
    "a": Button(18)
}

mapping = {
    "left": pygame.K_a,
    "right": pygame.K_d,
    "up": pygame.K_w,
    "down": pygame.K_s,
    "start": pygame.K_m,
    "a": pygame.K_SPACE
}

def ppress(p):
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=mapping[p]))

def prelease(p):
    pygame.event.post(pygame.event.Event(pygame.KEYUP, key=mapping[p]))

for p in buttons:
    buttons[p].when_pressed = lambda p=p: ppress(p)
    buttons[p].when_released = lambda p=p: prelease(p)

while GAME:
    if GAME_STATE == 0:
        menu = True
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
                    GAME = False
                    continue
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        choice = 1
                    elif event.key == pygame.K_s:
                        choice = 2
                    elif event.key == pygame.K_SPACE:
                        if choice == 1:
                            menu = False
                            END = False
                            GAME_STATE = 1
                            player.x = 330
                            player.y = 550
                            try:
                                del bullets[:]
                                del enemies[:]
                            except IndexError:
                                print("Cannot delete elements")

                            counter = 0
                            global_counter = 0
                            acceleration = 0
                            points = 0
                            life = 20
                        if choice == 2:
                            menu = False
                            GAME = False
                            continue
            screen.fill(BLACK)
            screen.blit(background, (0, 0))
            menuWindow.fill((100, 100, 100))
            if choice == 1:
                pygame.draw.rect(menuWindow, RED, [40, 50, 300, 30])
            if choice == 2:
                pygame.draw.rect(menuWindow, RED, [40, 95, 300, 30])
            menuWindow.blit(option1, [50, 50])
            menuWindow.blit(option2, [50, 100])
            screen.blit(menuWindow, [100, 100])
            pygame.display.flip()
            clock.tick(10)
    elif GAME_STATE == 1:
        END = False
        while not END:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    END = True
                    GAME = False
                    continue
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        player.vx = -10
                    elif event.key == pygame.K_d:
                        player.vx = 10
                    elif event.key == pygame.K_m:
                        END = True
                        GAME_STATE = 2
                        continue
                    elif event.key == pygame.K_SPACE:
                        laser_sound.play()
                        bullet = Bullet()
                        bullet.x = player.x + player.width / 2 - bullet.width / 2
                        bullet.y = player.y
                        bullet.vy = -15
                        bullets.append(bullet)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a and player.vx == -10:
                        player.vx = 0
                    elif event.key == pygame.K_d and player.vx == 10:
                        player.vx = 0

            if player.edgeCollision(size):
                if player.x < 0:
                    player.x = 0
                else:
                    player.x = window_width - player.width
            player.move()

            for bullet in bullets:
                bullet.move()
                shipNumber = 0
                for ship in enemies:
                    if bullet.objectCollision(ship):
                        points += 1
                        del enemies[shipNumber]
                        try:
                            del bullets[0]
                        except IndexError:
                            print("Index out of range")
                    shipNumber += 1
                if bullet.edgeCollision(size):
                    try:
                        del bullets[0]
                    except IndexError:
                        print("Index out of range")

            counter += 1
            global_counter += 1
            print(global_counter)
            if counter == 60:
                counter = 0 + acceleration
                new = Enemies()
                new.y = -new.height
                new.x = random.randrange(0, window_width - new.width)
                new.vy = 3
                enemies.append(new)
            if global_counter > 400:
                acceleration += 1
                global_counter = 0
            if acceleration == 45:
                acceleration = 20

            removed_index = -1
            for index, i in enumerate(enemies):
                if i.y > 700:
                    life -= 1
                    removed_index = index

            if removed_index >= 0:
                try:
                    del enemies[removed_index]
                except IndexError:
                    print("Index out of range")

            if life <= 0:
                END = True
                GAME_STATE = 2
                continue

            for ship in enemies:
                ship.move()

            screen.fill(BLACK)
            screen.blit(background, (0, 0))
            player.draw(screen)

            for bullet in bullets:
                bullet.draw(screen)

            for ship in enemies:
                ship.draw(screen)

            displayBar()
            displayLife()

            pygame.display.flip()

            clock.tick(60)
    elif GAME_STATE == 2:
        return_menu = True
        while return_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return_menu = False
                    GAME = False
                    continue
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        choice_return = 1
                    elif event.key == pygame.K_s:
                        choice_return = 2
                    elif event.key == pygame.K_SPACE:
                        if choice_return == 1:
                            return_menu = False
                            GAME_STATE = 0
                            continue
                        if choice_return == 2:
                            return_menu = False
                            GAME = False
                            continue

            screen.fill(BLACK)
            screen.blit(background, (0, 0))
            menuWindow.fill((100, 100, 100))
            if choice_return == 1:
                pygame.draw.rect(menuWindow, RED, [40, 50, 400, 30])
            if choice_return == 2:
                pygame.draw.rect(menuWindow, RED, [40, 95, 400, 30])  # for two options instead of 50, 95
            displayScore()
            menuWindow.blit(option3, [50, 50])
            menuWindow.blit(option2, [50, 100])
            screen.blit(menuWindow, [100, 100])
            pygame.display.flip()
            clock.tick(10)

pygame.quit()
