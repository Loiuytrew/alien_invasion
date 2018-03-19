class Settings:
    """存储外星人入侵的所有设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""

        self.screen_width = 1280
        self.screen_height = 960
        self.bg_color = (230, 230, 230)
        self.bg_color2 = (5, 30, 125)

        # 飞船的设置
        self.ship_speed_factor = 2.5
        self.ship_slow_speed_factor = 1
        self.ship_limit = 3

        # 子弹设置
        self.bullet_speed_factor = 4.5
        self.bullet_width = 8
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)

        # 外星人设置
        self.alien_speed_factor = 1
        self.alien_drop_speed = 10
        self.fleet_direction = 1

        # 以什么样的速度加快游戏节奏
        self.speedup_scale1 = 1.1
        self.speedup_scale2 = 1.05
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行变化的设置"""
        self.ship_speed_factor = 2.5
        self.ship_slow_speed_factor = 1
        self.bullet_speed_factor = 4.5
        self.alien_speed_factor = 1
        self.fleet_direction = 1

        self.alien_points = 100

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale2
        self.ship_slow_speed_factor *= self.speedup_scale2
        self.bullet_speed_factor *= self.speedup_scale2
        self.alien_speed_factor *= self.speedup_scale1

        self.alien_points = int(self.alien_points * self.score_scale)
