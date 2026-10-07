import pygame


class Player:
    def __init__(self, x, y):
        self.width = 160
        self.height = 110

        self.x = x
        self.y = y

        self.speed = 6

        self.lives = 3
        self.score = 0
        self.image = pygame.image.load(
            "assets/player.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (self.width, self.height)
        )

    def move(self, screen_width):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        # Prevent player from leaving the screen
        if self.x < 0:
            self.x = 0

        if self.x + self.width > screen_width:
            self.x = screen_width - self.width

    def draw(self, screen):
        screen.blit(
            self.image,
            (self.x, self.y)
        )

    def get_rect(self):
        hitbox_width = 60
        hitbox_height = 45

        hitbox_x = self.x + (self.width - hitbox_width) // 2
        hitbox_y = self.y + (self.height - hitbox_height) // 2

        return pygame.Rect(
            hitbox_x,
            hitbox_y,
            hitbox_width,
            hitbox_height
        )