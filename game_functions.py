import sys
import pygame
from bullet import Bullet
from alien import Alien
from random import randint
from time import sleep


def check_keydown_events(event, ai_settings, screen, stats, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_z:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_LSHIFT:
        speedslow = ai_settings.ship_slow_speed_factor
        ai_settings.ship_slow_speed_factor = ai_settings.ship_speed_factor
        ai_settings.ship_speed_factor = speedslow
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def check_keyup_events(event, ai_settings, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
    elif event.key == pygame.K_z:
        ship.fire = False
    elif event.key == pygame.K_LSHIFT:
        speedslow = ai_settings.ship_slow_speed_factor
        ai_settings.ship_slow_speed_factor = ai_settings.ship_speed_factor
        ai_settings.ship_speed_factor = speedslow


def check_events(ai_settings, screen, stats, play_button, sb, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ai_settings, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, sb, ship, aliens,
                      bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, play_button, sb, ship, aliens,
                      bullets, mouse_x, mouse_y):
    """在玩家单击play按钮时开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True
        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_bg(ai_settings, screen, sb, play_button):
    screen.fill(ai_settings.bg_color2)
    play_button.draw_button()
    sb.show_score()
    pygame.display.flip()


def update_screen(ai_settings, screen, sb, ship, aliens, bullets):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 让每次循环重绘屏幕为设定的背景色
    screen.fill(ai_settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    screen.fill(ai_settings.bg_color2, (0, 0, 280, 960))
    screen.fill(ai_settings.bg_color2, (1000, 0, 1280, 960))
    sb.show_score()

    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹的位置，并删除已消失的子弹"""
    # 更新子弹的位置
    bullets.update()

    # 删除屏幕外的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 检查是否有子弹击中了外星人，若击中，则删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    # 若外星人全灭，删除现有的子弹并生成一组新的外星人，并加快游戏节奏
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)


def fire_bullet(ai_settings, screen, ship, bullets):
    """发射一颗子弹"""
    new_bullet = Bullet(ai_settings, screen, ship)
    bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少外星人"""
    available_space_x = ai_settings.screen_width - 560 - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = ai_settings.screen_height - 2.5 * alien_height - ship_height
    number_rows = int(available_space_y / (2 * alien_height)) - 3
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其放在当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 250 + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = 0.5 * alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建第一个外星人
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            random_number = randint(1, 10)
            if random_number >= 3:
                create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.alien_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 1:
        # 将剩余飞船生命-1
        stats.ships_left -= 1

        # 更新得分记录
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)

    else:
        with open('highscore.txt', 'w') as hs:
            hs.write(str(stats.high_score))
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship,  aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, sb, ship,  aliens, bullets)
            break


def update_aliens(ai_settings, stats, screen, sb, ship,  aliens, bullets):
    """检查是否有外星人位于屏幕边缘，更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    # 检测是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, stats, screen, sb, ship,  aliens, bullets)


def check_high_score(stats, sb):
    """检查是否诞生了新的最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()