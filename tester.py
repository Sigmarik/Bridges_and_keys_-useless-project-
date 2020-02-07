import pygame

pygame.init()
MaxKey = 0

font = pygame.font.Font(None, 30)

def dist(a, b = [0, 0]):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def is_in(a, b):
    for el in a:
        if el not in b:
            return False
    return True

class island:
    pos = [0, 0]
    connections = []
    key_sets = []
    color = [0, 0, 0]
    def __init__(self, pos, cons = [], color = [255, 0, 0]):
        self.pos = pos
        self.connections = cons.copy()
        self.color = color
    def connect(self, isl, key):
        self.connections.append([isl, key])
        #print(self.connections)
    def check_set(self):
        KeySet = self.key_sets
        for i in range(len(KeySet))[::-1]:
            for j in range(len(KeySet)):
                if i != j and is_in(KeySet[j], KeySet[i]):
                    KeySet.pop(i)
                    break
    def draw(self, scr):
        pygame.draw.circle(scr, self.color, self.pos, 6)
        for con in self.connections:
            pygame.draw.line(scr, [0, 0, 255], self.pos, con[0].pos, 2)
            scr.blit(font.render(str(con[1]), 0, [255, 0, 0]), [(self.pos[0] + con[0].pos[0]) // 2, (self.pos[1] + con[0].pos[1]) // 2])
        for i, line in enumerate(self.key_sets):
            scr.blit(font.render(str(line), 0, [0, 0, 0]), [self.pos[0], self.pos[1] + i * 24])
def get_keys(arr, ind = 0, preds = []):
    if ind == 1:
        return
    preds.append(arr[ind])
    cons = arr[ind].connections
    ks = arr[ind].key_sets
    for con in cons:
        for IS in arr:
            IS.check_set()
            IS.draw(scr)
        pygame.display.update()
        if con[0] not in preds:
            #print('step')
            res = sorted([list(set(x + [con[1]])) for x in ks])
            arr[arr.index(con[0])].key_sets = sorted(con[0].key_sets.copy() + res)
            get_keys(arr, ind=arr.index(con[0]), preds=preds.copy())

KG = True

islands = ([island([350, 50], color = [0, 255, 0]), island([350, 650], color = [0, 255, 0])])[::-1]
islands[0].key_sets = [[]]
MIN = 0
key = 0

scr = pygame.display.set_mode([700, 700])

while KG:
    scr.fill([255, 255, 255])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            KG = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                islands.append(island(list(pygame.mouse.get_pos())))
            if event.button == 1:
                if len(islands) > 0:
                    MPos = list(pygame.mouse.get_pos())
                    for IS in islands:
                        if MIN == 0 or dist(MPos, MIN.pos) > dist(MPos, IS.pos):
                            MIN = IS
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if len(islands) > 0:
                    MPos = list(pygame.mouse.get_pos())
                    MN = island([-10 ** 9, -10 ** 9])
                    for IS in islands:
                        if (MN == 0 or dist(MPos, MN.pos) > dist(MPos, IS.pos)):
                            MN = IS
                    if MN != MIN:
                        MIN.connect(MN, key)
                        MN.connect(MIN, key)
                    MIN = 0
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_q]:
                key = int(input('Введите код соединения --> '))
            if event.key in [pygame.K_SPACE]:
                for IS in islands:
                    IS.key_sets = []
                islands[0].key_sets = [[]]
                #print(islands)
                result = get_keys(islands)
                #islands = result
                for IS in islands:
                    IS.check_set()
    for IS in islands:
        IS.draw(scr)
    if MIN != 0:
        pygame.draw.line(scr, [0, 0, 255], pygame.mouse.get_pos(), MIN.pos, 1)
    pygame.display.update()
pygame.quit()
