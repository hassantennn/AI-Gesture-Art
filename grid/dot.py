import pygame

BASE_RADIUS = 1
FADE_SPEED = 3
MAX_ALPHA = 200

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BASE_RADIUS
        self.alpha = 0
        self.color = (100, 255, 255)
        self.active = False

    def update(self, hand_pos, react_radius, active_color):
        dx = self.x - hand_pos[0]
        dy = self.y - hand_pos[1]
        dist_sq = dx * dx + dy * dy

        if dist_sq < react_radius * react_radius:
            self.active = True
            self.alpha = MAX_ALPHA
            self.color = active_color
            self.radius = BASE_RADIUS + 1.5
        else:
            self.alpha = max(0, self.alpha - FADE_SPEED)
            self.radius = BASE_RADIUS
            self.active = False

    def draw(self, surface):
        if self.alpha <= 0:
            return

        glow_radius = int(self.radius * 4)
        glow_surf = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
        glow_color = (*self.color[:3], int(self.alpha * 0.15))
        pygame.draw.circle(glow_surf, glow_color, (glow_radius, glow_radius), glow_radius)

        dot_surf = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
        dot_color = (*self.color[:3], int(self.alpha))
        pygame.draw.circle(dot_surf, dot_color, (int(self.radius * 2), int(self.radius * 2)), int(self.radius))

        surface.blit(glow_surf, (self.x - glow_radius, self.y - glow_radius))
        surface.blit(dot_surf, (self.x - self.radius * 2, self.y - self.radius * 2))
