class Sprite:
    def __init__(self, x, y, szer, wys, vx, vy):
        self.x = x
        self.y = y
        self.szer = szer
        self.wys = wys
        self.vx = vx
        self.vy = vy
    def odbijX(self):
        self.vx = -self.vx

    def odbijY(self):
        self.vy = -self.vy

    def przesun(self):
        self.x += self.vx
        self.y += self.vy

    def kolizjaKrawedz(self, rozmiar):
        if self.x < 0 or self.y < 0 or \
                (self.x + self.szer) > rozmiar[0] or \
                (self.y + self.wys) > rozmiar[1]:
            return True
        else:
            return False

    def kolizjaZ(self, obiekt):
        A = [self.x, self.x + self.szer, self.y, self.y + self.wys]
        B = [obiekt.x, obiekt.x + obiekt.szer, obiekt.y, obiekt.y + obiekt.wys]

        kolizjaX = 0
        kolizjaY = 0

        if A[0] > B[0] and A[0] < B[1]:
            kolizjaX += 1
        if A[1] > B[0] and A[1] < B[1]:
            kolizjaX += 1
        if A[2] > B[2] and A[2] < B[3]:
            kolizjaY += 1
        if A[3] > B[2] and A[3] < B[3]:
            kolizjaY += 1

        if kolizjaX >= 1 and kolizjaY >= 1:
            return True
        else:
            return False
