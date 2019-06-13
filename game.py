import pygame, os, random
import os.path as path
from recorder import Recorder

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720

class SlidePuzzle:
  speed = 500
  prev = None
  menu = True
  move = 0
  won = False
  background = pygame.transform.scale(
      pygame.image.load('/home/zizoz/Documents/Xử lý tiếng nói/slide_voice/resources/back_ground.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
  pics = []
  def __init__(self, gs, ts, ms):
    self.gs, self.ts, self.ms = gs, ts, ms
    self.tile_len = gs[0]*gs[1]-1
    self.tiles = [(x, y) for y in range(gs[1]) for x in range(gs[0])]
    self.position = [n + 1 for n in range(gs[0] * gs[1])]

    self.tilespos = [(x * (ts + ms) + ms, y * (ts + ms) + ms) for y in range(gs[1]) for x in range(gs[0])]  # actual pos on screen
    self.tilesPOS = {(x, y): (x * (ts + ms) + ms, y*(ts + ms) + ms) for y in range(gs[1]) for x in range(gs[0])} # the place they slide to

    font = pygame.font.Font(None, 120)

    for r, d, f in os.walk('/home/zizoz/Documents/Xử lý tiếng nói/slide_voice/resources/game_img'):
      for file in f:
        if '.jpg' in file:
          self.pics.append(os.path.join(r, file))
    # print(self.pics)
    #set game picture
    self.rect = pygame.Rect(0, 0, gs[0] * (ts + ms) + ms, gs[1] * (ts + ms) + ms)
    self.oripic = pygame.image.load(random.choice(self.pics))
    self.pic = pygame.transform.scale(self.oripic, self.rect.size)
    self.images = []
    for i in range(self.tile_len):
      x, y = self.tilespos[i]
      image = self.pic.subsurface(x, y, ts, ts)
      number = font.render(str(i + 1), 2, (0, 0, 0))
      w, h = number.get_size()
      image.blit(number, ((ts-w)/2, (ts-h)/2))
      self.images += [image]
  def getBlank(self): return self.tiles[-1]
  def setBlank(self, pos): self.tiles[-1] = pos
  opentile = property(getBlank, setBlank)
  def adjacent(self):
    x, y = self.opentile
    return (x-1, y), (x, y-1), (x+1, y), (x, y+1)

  def random(self):
    adj = self.adjacent()
    adj = [pos for pos in adj if self.in_grid(pos) and pos != self.prev]
    tile = random.choice(adj)
    if tile != self.prev:
      self.switch(tile, True)

  def switch(self, tile, random):
    n = self.tiles.index(tile)
    self.tiles[n], self.opentile, self.prev = self.opentile, self.tiles[n], self.opentile
    if not random:
      self.move += 1
      self.check_win_condition()

  def in_grid(self, tile):
    return tile[0] >= 0 and tile[0] < self.gs[0] and tile[1] >= 0 and tile[1] < self.gs[1]

  def update(self, dt):
    s = self.speed*dt
    for i in range(self.tile_len):
      x, y = self.tilespos[i]  # current pos
      X, Y = self.tilesPOS[self.tiles[i]]  # target pos
      dx, dy = X - x, Y - y
      x = X if abs(dx) < s else x+s if dx > 0 else x-s
      y = Y if abs(dy) < s else y+s if dy > 0 else y-s
      self.tilespos[i] = x, y

  def draw(self, screen):
    if self.won == False:
      # draw menu
      if self.menu:
        title = pygame.image.load(path.join('', "/home/zizoz/Documents/Xử lý tiếng nói/slide_voice/resources/title.png")).convert_alpha()
        rect = title.get_rect()
        width, height = rect.width, rect.height
        screen.blit(title, (SCREEN_WIDTH / 2 - width / 2, SCREEN_HEIGHT / 2 - height / 2 - 50))
        title = pygame.image.load(path.join('', "/home/zizoz/Documents/Xử lý tiếng nói/slide_voice/resources/instruction_1.png")).convert_alpha()
        rect = title.get_rect()
        width, height = rect.width, rect.height
        screen.blit(title, (SCREEN_WIDTH / 2 - width /2, SCREEN_HEIGHT / 2 - height / 2 + 100))
        title = pygame.image.load(path.join('', "/home/zizoz/Documents/Xử lý tiếng nói/slide_voice/resources/instruction_2.png")).convert_alpha()
        rect = title.get_rect()
        width, height = rect.width, rect.height
        screen.blit(title, (SCREEN_WIDTH / 2 - width /2, SCREEN_HEIGHT / 2 - height / 2 + 200))
      else:  # draw game
        width = self.gs[0] * (self.ts + self.ms)
        height = self.gs[1] * (self.ts + self.ms)
        for i in range(self.tile_len):
          x, y = self.tilespos[i]
          screen.blit(self.images[i], (x + SCREEN_WIDTH/2 - width/2 - 150,y + SCREEN_HEIGHT / 2 - height / 2 - 50))
        #draw move
        FONT = pygame.font.SysFont("comicsansms", 50)
        text = FONT.render("Moves: {}".format(self.move), True, (255, 0, 0))
        screen.blit(text, (SCREEN_WIDTH / 2 - width / 2 - 150, SCREEN_HEIGHT / 2 + height / 2 + 20))
    else:
      # draw win
      screen.blit(pygame.transform.scale(self.oripic, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))
      FONT = pygame.font.SysFont("comicsansms", 50)
      score = FONT.render("Final score: {}".format(self.move), True, (255, 0, 0))
      screen.blit(score, (0,0))

  def events(self, event):
    if event.type == pygame.KEYDOWN:
      for key, dx, dy in ((pygame.K_w, 0, -1), (pygame.K_s, 0, 1), (pygame.K_a, -1, 0), (pygame.K_d, 1, 0)):
        if event.key == key:
          x, y = self.opentile
          tile = x + dx, y + dy
          if self.in_grid(tile):
            self.switch(tile, False)
      # if event.key == pygame.K_SPACE:
      #   action = predict()
      #   print(action, 0)
      #   for move, dx, dy in (('up', 0, -1), ('down', 0, 1), ('left', -1, 0), ('right', 1, 0)):
      #     if action == move:
      #       x, y = self.opentile
      #       tile = x + dx, y + dy
      #       print(tile)
      #       if self.in_grid(tile):
      #         self.switch(tile, False)
      if event.key == pygame.K_RETURN:
        if self.won == False:
          self.menu = False
          if (self.move == 0):
            for i in range(1):
              self.random()
        else:
          self.won = False
          self.menu = True
          self.move = 0
    elif event.type == pygame.USEREVENT:
      for move, dx, dy in (('up', 0, -1), ('down', 0, 1), ('left', -1, 0), ('right', 1, 0)):
            if event.action == move:
              x, y = self.opentile
              tile = x + dx, y + dy
              print(tile)
              if self.in_grid(tile):
                self.switch(tile, False)
  def check_win_condition(self):
    answer = [(x, y) for y in range(self.gs[1]) for x in range(self.gs[0])]
    if self.tiles == answer:
      print("Won")
      self.won = True
