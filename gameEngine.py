import pygame, math
pygame.init()

class Sprite(pygame.sprite.Sprite):
    # constructor
    def __init__(self, scene):
        pygame.sprite.Sprite.__init__(self)
        self.scene = scene
        self.screen = scene.screen

        # variables
        self.xPos = 50
        self.yPos = 200
        self.dx = 0
        self.speed = 0
        self.angle = 0
        self.center = (100, 100)
        self.isJump = False
        self.yGravity = 1
        self.jumpHeight = 10
        self.yVel = self.jumpHeight

        # set image to car.gif
        self.imageMaster = pygame.image.load("car.gif")
        self.imageMaster = self.imageMaster.convert()
        self.image = self.imageMaster
        self.rect = self.image.get_rect()
    
    def update(self):
        self.center = self.rect.center
        self.checkEvents()
        self.calcVector()
        self.calcPosition()
        self.checkBounds()
        self.jump()
        self.rect.center = (self.xPos, self.yPos)
    
    def checkEvents(self):
        keys = pygame.key.get_pressed()
        # press left key to slow down
        if keys[pygame.K_LEFT]:
            self.speedup(-.5)
        # press right key to speed up
        if keys[pygame.K_RIGHT]:
            self.speedup(.5)
        # press space key to jump (holding it makes you jump faster)
        if keys[pygame.K_SPACE]:
            self.isJump = True
            self.jump()

    def calcVector(self):
        theta = self.angle / 180.0 * math.pi
        self.dx = math.cos(theta) * self.speed
        #dy does not change
    
    # calculates new position of sprite - adds dx to xPos to change it
    def calcPosition(self):
        self.xPos += self.dx
    
    # check boundaries - assume that it only stops the sprite if it attempts to go out of bounds
    def checkBounds(self):
        widthScreen = self.screen.get_width()
        if self.xPos > widthScreen:
            self.xPos = 0
        if self.xPos < 0:
            self.xPos = widthScreen
    
    def setSpeed(self, speed):
        self.speed = speed
    
    def speedup(self, number):
        self.speed += number
        # slow down
        if self.speed < -10:
            self.speed = -10
        # speed up
        if self.speed > 10:
            self.speed = 10
    
    def jump(self):
        if self.isJump:
            self.yPos -= self.yVel
            self.yVel -= self.yGravity
            if self.yVel < -self.jumpHeight:
                self.isJump = False
                self.yVel = self.jumpHeight

    


# in the Scene class, we identify:
# - size of screen
# - group of sprites
# - framerate (30)
class Scene(object):
    # constructor - inits screen, background, and sprite(s)
    def __init__(self):
        pygame.init()
        self.framerate = 30
        self.screen = pygame.display.set_mode((640, 480))
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill((0, 0, 0))
        pygame.display.set_caption("car game")

        # set up sprite group:
        self.sprite = Sprite(self)
        self.sprites = [self.sprite]
        self.groups = []

    def start(self):
        self.theSprites = pygame.sprite.OrderedUpdates(self.sprites)
        self.groups.append(self.theSprites)
        
        self.screen.blit(self.background, (0, 0))
        self.clock = pygame.time.Clock()
        self.keepGoing = True
        while self.keepGoing:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.keepGoing = False
                self.doEvents(event)
        
            self.update()
            for group in self.groups:
                group.clear(self.screen, self.background)
                group.update()
                group.draw(self.screen)
        
            pygame.display.flip()

    def end(self):
        self.keepGoing = False
    
    def doEvents(self, event):
        pass

    def update(self):
        pass


def main():
    game = Scene()
    game.background.fill((0, 0, 0))
    car = Sprite(game)
    car.setSpeed(0)
    game.sprites = [car]
    game.start()

if __name__ == "__main__":
    main()
