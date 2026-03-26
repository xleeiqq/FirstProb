import pygame
import sys
pygame.init()
WIDTH, HEIGHT = 626, 351
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pervaia IGRA")
clock = pygame.time.Clock()
FPS = 120
background_img = pygame.image.load("D:\PyCharm\DZ\pygame_game\cosmos.png")
RED = (220, 40, 40)
BLACK = (10, 10, 10)
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
class Projectile:
    def __init__(self, start_x, start_y, target_x, target_y):
        self.pos = pygame.Vector2(start_x, start_y)
        self.speed = 600
        self.radius = 8
        self.color = (255, 100, 100)
        direction = pygame.Vector2(target_x, target_y) - self.pos
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
        if not (0 <= self.pos.x <= screen_w and 0 <= self.pos.y <= screen_h):
            return True
        return False
class Player:
    def __init__(self):
        self.pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
        self.radius = 25
        self.color = RED
        self.speed = 300
        self.target = None
        self.dragging = False
        self.drag_offset = pygame.Vector2(0, 0)
        self.projectile = None
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
player = Player()
running = True
'''while running:
    screen.blit(background_img, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(f"Нажата кнопка: {event.button}")
            print(f"Позиция: {event.pos}")
        if event.type == pygame.MOUSEBUTTONUP:
            print(f"Отпущена кнопка: {event.button}")
            print(f"Позиция: {event.pos}")
    pygame.draw.circle(screen, "red", player_pos, 25)
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        if player_pos.y >= 30 * dt: player_pos.y -= 30 * dt
    if key[pygame.K_s]:
        if player_pos.y <= screen.get_height() - 30 * dt: player_pos.y += 30 * dt
    if key[pygame.K_a]:
        if player_pos.x >= 30 * dt: player_pos.x -= 30 * dt
    if key[pygame.K_d]:
        if player_pos.x <= screen.get_width() - 30 * dt: player_pos.x += 30 * dt
    pygame.display.flip()
    dt = clock.tick(FPS) / 1000'''
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
