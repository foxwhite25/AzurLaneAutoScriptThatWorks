from campaign.event_20240521_cn.campaign_base import CurrentFleetGrid
from module.base.utils import location2node
from module.campaign.campaign_base import CampaignBase
from module.logger import logger
from module.map.map_base import CampaignMap
from .d1 import Config as ConfigBase

MAP = CampaignMap('D3')
MAP.shape = 'K9'
MAP.camera_data = ['D3', 'D6', 'H3', 'H6']
MAP.camera_data_spawn_point = ['D7']
MAP.map_data = """
    ++ ++ -- ++ ++ ++ ++ -- ++ ME --
    ++ ++ ME ++ ++ ++ ++ -- ME -- --
    ME -- -- ++ ++ ++ ++ -- -- -- ME
    -- -- Me ++ ++ ++ ++ -- ++ ++ --
    ME -- ++ ++ ++ ++ ++ -- Me ++ --
    ++ -- ++ -- MS MB MS -- -- Me --
    -- -- Me -- -- MS -- -- -- -- ME
    -- ME -- ME -- __ -- ME -- ME --
    -- ++ ++ ++ SP -- SP ++ ++ ++ --
"""
MAP.weight_data = """
    90 90 90 50 50 50 50 50 50 50 50
    50 50 90 50 50 50 50 50 50 50 50
    90 90 90 50 50 50 50 50 50 50 50
    90 90 90 50 50 50 50 50 50 50 50
    90 90 90 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50 50 50
    50 50 50 50 50 10 50 50 50 50 50
    50 50 50 50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50 50 50 50
"""
MAP.spawn_data = [
    {'battle': 0, 'enemy': 2, 'siren': 2},
    {'battle': 1, 'enemy': 1},
    {'battle': 2, 'enemy': 2, 'siren': 1},
    {'battle': 3, 'enemy': 1},
    {'battle': 4, 'enemy': 2},
    {'battle': 5, 'enemy': 1},
    {'battle': 6, 'boss': 1},
]
A1, B1, C1, D1, E1, F1, G1, H1, I1, J1, K1, \
A2, B2, C2, D2, E2, F2, G2, H2, I2, J2, K2, \
A3, B3, C3, D3, E3, F3, G3, H3, I3, J3, K3, \
A4, B4, C4, D4, E4, F4, G4, H4, I4, J4, K4, \
A5, B5, C5, D5, E5, F5, G5, H5, I5, J5, K5, \
A6, B6, C6, D6, E6, F6, G6, H6, I6, J6, K6, \
A7, B7, C7, D7, E7, F7, G7, H7, I7, J7, K7, \
A8, B8, C8, D8, E8, F8, G8, H8, I8, J8, K8, \
A9, B9, C9, D9, E9, F9, G9, H9, I9, J9, K9, \
    = MAP.flatten()


class Config(ConfigBase):
    # ===== Start of generated config =====
    MAP_SIREN_TEMPLATE = ['huiguangzhihe']
    MOVABLE_ENEMY_TURN = (2,)
    MAP_HAS_SIREN = True
    MAP_HAS_MOVABLE_ENEMY = True
    MAP_HAS_MAP_STORY = True
    MAP_HAS_FLEET_STEP = True
    MAP_HAS_AMBUSH = False
    MAP_HAS_MYSTERY = False
    # ===== End of generated config =====

    INTERNAL_LINES_FIND_PEAKS_PARAMETERS = {
        'height': (80, 255 - 17),
        'width': (0.9, 10),
        'prominence': 10,
        'distance': 35,
    }
    EDGE_LINES_FIND_PEAKS_PARAMETERS = {
        'height': (255 - 17, 255),
        'prominence': 10,
        'distance': 50,
        'wlen': 1000
    }
    HOMO_EDGE_COLOR_RANGE = (0, 17)
    HOMO_EDGE_HOUGHLINES_THRESHOLD = 210
    MAP_SWIPE_MULTIPLY = (1.016, 1.036)
    MAP_SWIPE_MULTIPLY_MINITOUCH = (0.983, 1.001)
    MAP_SWIPE_MULTIPLY_MAATOUCH = (0.954, 0.972)


class Campaign(CampaignBase):
    grid_class = CurrentFleetGrid
    MAP = MAP
    ENEMY_FILTER = '1L > 1M > 1E > 1C > 2L > 2M > 2E > 2C > 3L > 3M > 3E > 3C'

    def in_sight(self, location, sight=None):
        logger.info('In sight: %s' % location2node(location))
        x, y = location
        if x >= 7 and y <= 4:
            x = 7
            location = (x, y)
            logger.info('In sight: %s' % location2node(location))
            return super().focus_to(location)
        if x <= 4 and y <= 4:
            x = 3
            location = (x, y)
            logger.info('In sight: %s' % location2node(location))
            return super().focus_to(location)

        return super().in_sight(location, sight=sight)

    def battle_0(self):
        if self.clear_siren():
            return True
        if self.clear_filter_enemy(self.ENEMY_FILTER, preserve=1):
            return True

        return self.battle_default()

    def battle_5(self):
        if self.clear_siren():
            return True
        if self.clear_filter_enemy(self.ENEMY_FILTER, preserve=0):
            return True

        return self.battle_default()

    def battle_6(self):
        return self.fleet_boss.clear_boss()
