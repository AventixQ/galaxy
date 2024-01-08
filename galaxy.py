# biblioteki
import pygame
import random
from sprite import *

pygame.init()

CZARNY = (0, 0, 0)
BIALY = (255, 255, 255)
ZIELONY = (0, 255, 0)
CZERWONY = (255, 0, 0)
NIEBIESKI = (0, 0, 255)

szerokoscOkna = 700
wysokoscOkna = 500
rozmiar = (szerokoscOkna, wysokoscOkna)
ekran = pygame.display.set_mode(rozmiar)
pygame.display.set_caption('Galaxy')
tlo = pygame.image.load('photos/kosmos.png')

KONIEC = False

zegar = pygame.time.Clock()


class Gracz(Sprite):
    def __init__(self):
        super().__init__(0, 0, 0, 0, 0, 0)
        self.kostium = pygame.image.load("photos/playerShip1_blue.png")
        self.szer = self.kostium.get_width()
        self.wys = self.kostium.get_height()

    def rysuj(self):
        ekran.blit(self.kostium, [self.x, self.y])


class Pocisk(Sprite):
    def __init__(self):
        super().__init__(0, 0, 0, 0, 0, 0)
        self.kostium = pygame.image.load("photos/laserGreen10.png")
        self.szer = self.kostium.get_width()
        self.wys = self.kostium.get_height()

    def rysuj(self):
        ekran.blit(self.kostium, [self.x, self.y])


class Przeciwnicy(Sprite):
    def __init__(self):
        super().__init__(0, 0, 0, 0, 0, 0)
        self.kostium = pygame.image.load("photos/enemyGreen1.png")
        self.szer = self.kostium.get_width()
        self.wys = self.kostium.get_height()

    def rysuj(self):
        ekran.blit(self.kostium, [self.x, self.y])


gracz = Gracz()
gracz.x = 330
gracz.y = 350

pociski = []

przeciwnicy = []
licznik = 0
globalny_licznik = 0
przyspieszenie = 0

dzwiek_laser = pygame.mixer.Sound("sound/laser.wav")
menu = True
wybór = 1
wybór_powrot = 1

oknoMenu = pygame.Surface((500, 180))
fontMenu = pygame.font.SysFont('Calibri', 25, True, False)

opcja1 = fontMenu.render("Rozpocznij grę", True, CZARNY)
opcja2 = fontMenu.render("Wyjdź", True, CZARNY)
opcja3 = fontMenu.render("Przejdź do menu głównego", True, CZARNY)

fontGUI = pygame.font.SysFont('Calibri', 15, True, False)

punkty = 0
zycie = 20


def wyswietlPasek():
    pygame.draw.rect(ekran, (100, 100, 100), [0, 0, szerokoscOkna, 30])
    punktyText = fontGUI.render('Punkty: ' + str(punkty), True, CZARNY)
    ekran.blit(punktyText, [25, 5])


def wystwietlZycie():
    pygame.draw.rect(ekran, (255, 0, 0), [0, 30, szerokoscOkna*(zycie/20), 30])
    punktyZycie = fontGUI.render(str(zycie) + '/20', True, BIALY)
    ekran.blit(punktyZycie, [szerokoscOkna / 2 - 15, 35])


def wyswietlWynik():
    przegrana = fontMenu.render('GAME OVER', True, CZERWONY)
    ekran.blit(przegrana, [30, 35])
    wynik = fontMenu.render('Liczba zdobytych punktów: ' + str(punkty), True, CZERWONY)
    ekran.blit(wynik, [30, 65])

GRA = True
STAN_GRY = 0 #[0, 1 lub 2]
muzyka = pygame.mixer.Sound('sound/g-m.mp3')  # Podaj ścieżkę do swojego pliku dźwiękowego
muzyka.play(-1)
while GRA:
    if STAN_GRY == 0:
        menu = True
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu = False
                    GRA = False
                    continue
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        wybór = 1
                    elif event.key == pygame.K_s:
                        wybór = 2
                    elif event.key == pygame.K_SPACE:
                        if wybór == 1:
                            menu = False
                            KONIEC = False
                            STAN_GRY = 1
                        if wybór == 2:
                            menu = False
                            GRA = False
                            continue
            ekran.fill(CZARNY)
            ekran.blit(tlo, (0, 0))
            oknoMenu.fill((100, 100, 100))
            if wybór == 1:
                pygame.draw.rect(oknoMenu, CZERWONY, [40, 50, 300, 30])
            if wybór == 2:
                pygame.draw.rect(oknoMenu, CZERWONY, [40, 95, 300, 30])
            oknoMenu.blit(opcja1, [50, 50])
            oknoMenu.blit(opcja2, [50, 100])
            ekran.blit(oknoMenu, [100, 100])
            pygame.display.flip()
            zegar.tick(10)
    elif STAN_GRY == 1:
        zycie = 2
        przepuszczeni = 0
        KONIEC = False
        while not KONIEC:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    KONIEC = True
                    GRA = False
                    continue
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        gracz.vx = -10
                    elif event.key == pygame.K_d:
                        gracz.vx = 10

                    elif event.key == pygame.K_w:
                        dzwiek_laser.play()
                        pocisk = Pocisk()
                        pocisk.x = gracz.x + gracz.szer / 2 - pocisk.szer / 2
                        pocisk.y = gracz.y
                        pocisk.vy = -15
                        pociski.append(pocisk)


                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_a and gracz.vx == -10:
                        gracz.vx = 0
                    elif event.key == pygame.K_d and gracz.vx == 10:
                        gracz.vx = 0

            if gracz.kolizjaKrawedz(rozmiar):
                if gracz.x < 0:
                    gracz.x = 0
                else:
                    gracz.x = szerokoscOkna - gracz.szer
            gracz.przesun()

            for pocisk in pociski:
                pocisk.przesun()
                nrStatku = 0
                for statek in przeciwnicy:
                    if pocisk.kolizjaZ(statek):
                        punkty += 1
                        #print(punkty)
                        del przeciwnicy[nrStatku]
                        try:
                            del pociski[0]
                        except Exception: print("Index out of range")
                    nrStatku += 1
                if pocisk.kolizjaKrawedz(rozmiar):
                    del pociski[0]

            licznik += 1
            globalny_licznik += 1
            print((globalny_licznik))
            if licznik == 60:
                licznik = 0 + przyspieszenie
                nowy = Przeciwnicy()
                nowy.y = -nowy.wys
                nowy.x = random.randrange(0, szerokoscOkna - nowy.szer)
                nowy.vy = 3
                przeciwnicy.append(nowy)
            if globalny_licznik > 600:
                przyspieszenie += 1
                globalny_licznik = 0
            if przyspieszenie == 60: przyspieszenie == 30
            zycie = 20
            przepuszczeni = 0
            for i in przeciwnicy:
                if i.y > 500: przepuszczeni += 1
            zycie = zycie - przepuszczeni

            if zycie <= 0:
                KONIEC = True
                STAN_GRY = 2
                continue

            for statek in przeciwnicy:
                statek.przesun()

            ekran.fill(CZARNY)
            ekran.blit(tlo, (0, 0))
            wyswietlPasek()
            wystwietlZycie()
            gracz.rysuj()

            for pocisk in pociski:
                pocisk.rysuj()

            for statek in przeciwnicy:
                statek.rysuj()

            pygame.display.flip()

            zegar.tick(60)
    elif STAN_GRY == 2:
        menu_powrotu = True
        while menu_powrotu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_powrotu = False
                    GRA = False
                    continue
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        wybór_powrot = 1
                    elif event.key == pygame.K_s:
                        wybór_powrot = 2
                    elif event.key == pygame.K_SPACE:
                        #if wybór_powrot == 1:
                            #menu_powrotu = False
                            #STAN_GRY = 0
                            #continue
                        if wybór_powrot == 2:
                            menu_powrotu = False
                            GRA = False
                            continue

            ekran.fill(CZARNY)
            ekran.blit(tlo, (0, 0))
            oknoMenu.fill((100, 100, 100))
            #if wybór_powrot == 1:
            #    pygame.draw.rect(oknoMenu, CZERWONY, [40, 50, 300, 30])
            if wybór_powrot == 2:
                pygame.draw.rect(oknoMenu, CZERWONY, [40, 50, 300, 30]) #przy dwóch opcjach zamiast 50, 95
            wyswietlWynik()
            #oknoMenu.blit(opcja3, [50, 50])
            oknoMenu.blit(opcja2, [50, 50])
            ekran.blit(oknoMenu, [100, 100])
            pygame.display.flip()
            zegar.tick(10)

pygame.quit()
