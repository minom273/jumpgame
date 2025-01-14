import pygame
import random

# 定数の定義
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLATFORM_SPAWN_INTERVAL = 120  # 足場の出現間隔
GROUND_HEIGHT = 100  # 地面の高さを設定
initial_platform_y = 200  # 最初の足場のY座標
platform_y_offset = 20  # 次の足場を20ピクセル下げるオフセット

# 足場生成関数の定義
def spawn_platform():
    global initial_platform_y
    new_y = initial_platform_y
    initial_platform_y += platform_y_offset
    x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
    return pygame.Rect(x, new_y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

# ゲームの初期化
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
running = True

# 足場の生成管理
platforms = []
spawn_timer = 0

# メインループ
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # フレームごとの更新
    spawn_timer += 1
    if spawn_timer >= PLATFORM_SPAWN_INTERVAL:
        platforms.append(spawn_platform())  # 新しい足場を生成
        spawn_timer = 0

    screen.fill((0, 0, 0))  # 背景を黒に

    # 足場を描画
    for platform in platforms:
        pygame.draw.rect(screen, (255, 255, 255), platform)  # 足場を白色で描画

    # 画面を更新
    pygame.display.flip()

# ゲーム終了処理
pygame.quit()