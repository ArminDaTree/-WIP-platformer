# Import statements are to enable the code to use the functions from the library
import pygame
import sys
import os
import pytmx
from pytmx.util_pygame import load_pygame

# initialize pygame & window
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
SCREENWIDTH = 500
SCREENHEIGHT = 500
SCREENSIZE = [SCREENWIDTH, SCREENHEIGHT]
SCREEN = pygame.display.set_mode(SCREENSIZE)

# caption for the game
pygame.display.set_caption("My first game in pygame")

# map
tiled_map = load_pygame('./map/map.tmx', pixelalpha=True)
tilewidth = tiled_map.tilewidth
tileheight = tiled_map.tileheight

collision = tiled_map.get_layer_by_name("objects")

p_spritesheet = pygame.image.load("sprites/player.png")


image = pygame.Surface([32, 32])
image.blit(p_spritesheet, (0, 0), (0, 0, 32, 32))
image.set_colorkey([0,0,0])
player = image
CAMERA = tiled_map.get_object_by_name("player")

for layer in tiled_map.layers:
    if isinstance(layer, pytmx.TiledTileLayer):
        for x, y, tile in layer.tiles():
            if (tile):
                SCREEN.blit(tile, [(x*tilewidth) - CAMERA.x +(SCREENWIDTH/2) , (y*tileheight) - CAMERA.y + (SCREENHEIGHT/2)])

    elif isinstance(layer, pytmx.TiledObjectGroup):
        for object in layer:
            if (object.type=='player'):
                SCREEN.blit(player, [object.x - CAMERA.x +(SCREENWIDTH/2), object.y - CAMERA.y + (SCREENHEIGHT/2)])

    pygame.display.update()
# game loop
while True:

    for events in pygame.event.get():  # get all pygame events
        if events.type == pygame.QUIT:  # if event is quit then shutdown window and program
            pygame.quit()
            sys.exit()
