import pygame, os ,sys
import game
import recorder

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
move = ['down', 'left', 'right', 'up']

def main():
  pygame.init()
  os.environ['SDL_VIDEO_CENTERED'] = '1'
  pygame.display.set_caption('Slide Puzzle')
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
  fpsclock = pygame.time.Clock()
  program = game.SlidePuzzle((4, 3), 160, 5)
  detect = recorder.Recorder()

  while True:
    dt = fpsclock.tick() / 1000
    screen.blit(program.background, (0, 0))
    program.draw(screen)
    pygame.display.flip()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      program.events(event)
    detect.listen()
    program.update(dt)

if __name__ == '__main__':
  main()
