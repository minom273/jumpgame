import pygame
import random

# 初期化
pygame.init()

# 定数
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 30
FPS = 60
PLATFORM_SPAWN_INTERVAL = 120  # 足場の出現間隔（フレーム数）

# 色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# スクリーンの設定
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jumping Game")

# キャラクターのクラス
class Player:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT - GROUND_HEIGHT - 35, 30, 30)  # 最初の位置を下に設定
        self.velocity_y = 0
        self.on_ground = True
        self.jump_power = 0
        self.gravity = 1

    def jump(self):
        if self.on_ground:
            self.velocity_y = -self.jump_power
            self.on_ground = False
            self.jump_power = 0  # ジャンプパワーをリセット

    def update(self):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        if self.rect.y >= SCREEN_HEIGHT - GROUND_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.rect.height
            self.on_ground = True
            self.velocity_y = 0

# 足場のクラス
class Platform:
    def __init__(self, y_position):
        self.rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - 80), y_position, 80, 10)

    def update(self):
        self.rect.y += 1  # 足場がゆっくりと下に移動（スクロール速度を減少）

        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = -10  # 再生成
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)

# メインゲーム関数
def main():
    clock = pygame.time.Clock()
    player = Player()
    
    platforms = []  # 初期の足場を生成
    spawn_timer = 0

    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # シフトキーが押されている間、ジャンプパワーを蓄積
        if keys[pygame.K_LSHIFT]:
            player.jump_power += 0.5  # パワーを少しずつ増加、最大パワーを制限する
            if player.jump_power > 15:  # 上限を指定
                player.jump_power = 15

        # シフトキーが離れた場合にジャンプを実行
        if not keys[pygame.K_LSHIFT] and player.on_ground:
            player.jump()

        # マウスの動きに応じて、プレイヤーの位置を調整
        mouse_x, _ = pygame.mouse.get_pos()
        if player.on_ground:
            player.rect.x = mouse_x - player.rect.width // 2  # プレイヤーをマウスに追従させる

        player.update()

        # 足場の出現を管理
        spawn_timer += 1
        if spawn_timer >= PLATFORM_SPAWN_INTERVAL:
            platforms.append(Platform(random.randint(0, SCREEN_WIDTH - 80)))
            spawn_timer = 0

        # 足場を更新
        for platform in platforms:
            platform.update()
            if platform.rect.colliderect(player.rect) and player.velocity_y > 0:
                player.on_ground = True
                player.rect.bottom = platform.rect.top
                player.velocity_y = 0

        # `player.rect.y`が画面外に出たらゲームオーバー
        if player.rect.y > SCREEN_HEIGHT:
            game_over = True

        # 描画
        screen.fill(BLACK)
        # 地面を描画
        pygame.draw.rect