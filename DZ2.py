import pygame
import sys
pygame.init()
WIDTH, HEIGHT = 626, 351
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pervaia IGRA")
clock = pygame.time.Clock()
FPS = 120
background_img = pygame.image.load("D:\PyCharm\DZ\pygame_game\cosmos.png")
WHITE = (240, 240, 240)
RED = (220, 40, 40)
BLUE = (60, 120, 240)
BLACK = (10, 10, 10)
class Player:
    def __init__(self):
        self.pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
        self.radius = 25
        self.color = RED
        self.target = None
        self.speed = 300
        self.dragging = False
        self.drag_offset = pygame.Vector2(0, 0)
        self.projectile = None
    def update(self, dt):
        if self.dragging:
            mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
            self.pos = mouse_pos - self.drag_offset
            self.pos.x = max(self.radius, min(WIDTH - self.radius, self.pos.x))
            self.pos.y = max(self.radius, min(HEIGHT - self.radius, self.pos.y))
            self.target = None
            return
        if self.target is not None:
            direction = self.target - self.pos
            distance = direction.length()
            if distance < 5:
                self.target = None
            else:
                move_dist = self.speed * dt
                if move_dist >= distance:
                    self.pos = self.target.copy()
                    self.target = None
                else:
                    self.pos += direction.normalize() * move_dist
        if self.projectile:
            self.projectile.update(dt)
            if self.projectile.is_dead(WIDTH, HEIGHT):
                self.projectile = None
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
        pygame.draw.circle(surface, BLACK, (int(self.pos.x), int(self.pos.y)), self.radius, 2)
        if self.projectile:
            self.projectile.draw(surface)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.Vector2(event.pos)
            if event.button == 1:
                if (mouse_pos - self.pos).length() <= self.radius:
                    self.dragging = True
                    self.drag_offset = mouse_pos - self.pos
                else:
                    self.target = mouse_pos
                    self.dragging = False
            elif event.button == 3:
                if self.projectile is None:
                    self.projectile = Projectile(self.pos.x, self.pos.y, event.pos[0], event.pos[1])
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
class Projectile:
    def __init__(self, start_x, start_y, target_x, target_y):
        self.pos = pygame.Vector2(start_x, start_y)
        self.target = pygame.Vector2(target_x, target_y)
        self.speed = 600
        self.radius = 8
        self.color = (220, 60, 60)
        direction = self.target - self.pos
        dist = direction.length()
        if dist > 0:
            self.vel = direction.normalize() * self.speed
        else:
            self.vel = pygame.Vector2(0, 0)
    def update(self, dt):
        self.pos += self.vel * dt
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
    def is_dead(self, screen_w, screen_h):
        if (self.target - self.pos).length() < 10:
            return True
        if not (0 <= self.pos.x <= screen_w and 0 <= self.pos.y <= screen_h):
            return True
        return False
player = Player()
running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        player.handle_event(event)
    player.update(dt)
    screen.blit(background_img, (0, 0))
    player.draw(screen)
    pygame.display.flip()
pygame.quit()
sys.exit()