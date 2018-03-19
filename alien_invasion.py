import pygame

from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
import game_functions as gf


def run_game():
    # 初始化游戏并创建一个屏幕screen
    pygame.init()  # 该语句初始化背景设置,让pygame能够正确工作
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建按钮
    play_button = Button(ai_settings, screen, "Play")
    # 创建一个用于存储游戏统计信息的实例，并创建计分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    # 创建一个用于存储子弹的编组
    bullets = Group()
    # 创建一个用于存储外星人的编组
    aliens = Group()
    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 游戏的主循环
    while True:

        gf.check_events(ai_settings, screen, stats, play_button, sb, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)

        if stats.game_active:
            gf.update_screen(ai_settings, screen, sb, ship, aliens, bullets)
        else:
            gf.update_bg(ai_settings, screen, sb, play_button)


run_game()