import pygame
import random


class FallingObject:
    def __init__(self, x, y, size, speed, object_type):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.object_type = object_type

        if self.object_type == "water":
            self.image = pygame.image.load(
                "assets/water.png"
            ).convert_alpha()

            self.image = pygame.transform.scale(
                self.image,
                (50, 50)
            )

        elif self.object_type == "food":
            self.image = pygame.image.load(
                "assets/food.png"
            ).convert_alpha()

            self.image = pygame.transform.scale(
                self.image,
                (60, 60)
            )


        elif self.object_type == "first_aid":
            self.image = pygame.image.load(
                "assets/first_aid.png"
            ).convert_alpha()

            self.image = pygame.transform.scale(
                self.image,
                (70, 70)
            )

        elif self.object_type == "emergency":
            self.image = pygame.image.load(
                "assets/emergency.png"
            ).convert_alpha()

            self.image = pygame.transform.scale(
                self.image,
                (60, 60)
            )
        elif self.object_type == "debris":
            self.image = pygame.image.load(
                "assets/debris.png"
            ).convert_alpha()

            self.image = pygame.transform.scale(
                self.image,
                (60, 60)
            )

        elif self.object_type == "fire":
            self.image = pygame.image.load(
                "assets/fire.png"
            ).convert_alpha()

            self.image = pygame.transform.scale(
                self.image,
                (60, 60)
            )



    def update(self):
        self.y += self.speed

    def draw(self, screen):

        if self.object_type == "water":
            screen.blit(
                self.image,
                (self.x, self.y)
            )
            return

        elif self.object_type == "food":
            screen.blit(
                self.image,
                (self.x, self.y)
            )
            return


        elif self.object_type == "first_aid":
            screen.blit(
                self.image,
                (self.x, self.y)
            )
            return


        elif self.object_type == "emergency":
            screen.blit(
                self.image,
                (self.x, self.y)
            )
            return

        elif self.object_type == "debris":
            screen.blit(
                self.image,
                (self.x, self.y)
            )
            return


        elif self.object_type == "fire":
            screen.blit(
                self.image,
                (self.x, self.y)
            )
            return

        pygame.draw.rect(
            screen,
            color,
            (self.x, self.y, self.size, self.size)
        )

    def get_rect(self):
        hitbox_size = 30

        hitbox_x = self.x + (self.size - hitbox_size) // 2
        hitbox_y = self.y + (self.size - hitbox_size) // 2

        return pygame.Rect(
            hitbox_x,
            hitbox_y,
            hitbox_size,
            hitbox_size
        )

    def is_off_screen(self, screen_height):
        return self.y > screen_height

    def get_score(self):
        scores = {
            "water": 5,
            "food": 5,
            "first_aid": 10,
            "emergency": 15,
            "debris": 0
        }

        return scores[self.object_type]

    def is_hazard(self):
        return self.object_type in ["debris", "fire"]


def create_random_object(screen_width, level):
    if level == 1:
        object_types = [
            "water",
            "food",
            "first_aid",
            "emergency",
            "debris"
        ]

    elif level == 2:
        object_types = [
            "water",
            "food",
            "first_aid",
            "emergency",
            "debris",
            "fire"
        ]

    else:
        object_types = [
            "water",
            "food",
            "first_aid",
            "emergency",
            "debris",
            "fire",
            "fire"
        ]

    object_type = random.choice(object_types)

    size = 40

    margin = 30

    x = random.randint(
        margin,
        screen_width - size - margin
    )

    # Speed depends on level
    if level == 1:
        speed = random.randint(3, 4)

    elif level == 2:
        speed = random.randint(4, 6)

    else:
        speed = random.randint(6, 8)

    return FallingObject(
        x,
        -size,
        size,
        speed,
        object_type
    )