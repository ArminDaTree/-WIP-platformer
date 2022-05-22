import pygame
import pytmx
import pyscroll
from player import Player
from enemy import Champi

FPS = 144
timestep = 1/FPS

class Game:
    def __init__(self):
        # create window
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("DaTreeRPG")

        # load map
        tmx_data = pytmx.util_pygame.load_pygame("map/map.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # generate player
        self.player_sp = tmx_data.get_object_by_name("player_spawnpoint") #spawnpoint
        self.player = Player(self.player_sp.x, self.player_sp.y)

        #generate champi
        self.champi_sp = tmx_data.get_object_by_name("champi_spawnpoint") #spawnpoint
        self.champi = Champi(self.champi_sp.x, self.champi_sp.y)

        # collisions rect
        self.walls = []
        self.platforms = []
        self.holes = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "platform":
                self.platforms.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            elif obj.type == "hole":
                self.holes.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # draw groups layers
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=4)
        self.group.add(self.champi)
        self.group.add(self.player)

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.player.move_left()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
        elif pressed[pygame.K_SPACE] and self.player.can_jump < self.player.max_jump:
            self.player.velocity[1] = self.player.velocity[1] - 0.025
            self.player.can_jump += 1

    def update(self):
        self.group.update()
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()
                self.player.velocity[1] = self.player.velocity[1]+1*timestep
            elif sprite.feet.collidelist(self.platforms) > -1:
                self.player.velocity[1] = 0
                self.player.can_jump = 0
            elif sprite.feet.collidelist(self.holes) > -1:
                self.player.position = [self.player_sp.x, self.player_sp.y]
            else:
                print("ok")
                self.player.velocity[1] = self.player.velocity[1]+1*timestep
                self.player.position[1] = self.player.position[1]+self.player.velocity[1]


    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            time = clock.tick(FPS)
            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        pygame.quit()