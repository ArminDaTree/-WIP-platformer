import pygame


class Champi(pygame.sprite.Sprite):

    def __init__(self,x, y):
        super().__init__()

        self.position = [x, y]

        self.sprite_sheet = pygame.image.load('sprites/champi.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.images = {
            'down': self.get_image(0, 0),
            'left': self.get_image(0, 32),
            'right': self.get_image(0, 64),
            'up': self.get_image(0, 96)
        }
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image
