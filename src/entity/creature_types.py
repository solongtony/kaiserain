from enum import Enum

import libtcodpy as libtcod

from components.ai import BasicMonster
from components.fighter import Fighter
from entity.entity import Entity
from render_functions import RenderOrder

class CreatureTypes(Enum):
    # Animals
    RAT = {
        'name': 'Rat',
        'character': 'r',
        'color': libtcod.dark_sepia,
        'stats': {'hp':1, 'defense':4, 'power':1, 'xp':1}
    }
    LARGE_RAT = {
        'name': 'Large Rat',
        'character': 'r',
        'color': libtcod.darkest_sepia,
        'stats': {'hp':5, 'defense':3, 'power':2, 'xp':5}
    }
    BOA = {
        'name': 'Boa Consrictor',
        'character': 's',
        'color': libtcod.desaturated_green,
        'stats': {'hp':6, 'defense':1, 'power':6, 'xp':12}
    }
    GIANT_SPIDER = {
        'name': 'Giant Spider',
        'character': 'S',
        'color': libtcod.dark_sepia,
        'stats': {'hp':8, 'defense':2, 'power':9, 'xp':15}
    }
    BROWN_BEAR = {
        'name': 'Brown Bear',
        'character': 'b',
        'color': libtcod.darkest_sepia,
        'stats': {'hp':25, 'defense':1, 'power':10, 'xp':48}
    }
    # Greenskins
    GOBLIN = {
        'name': 'Goblin',
        'character': 'g',
        'color': libtcod.desaturated_green,
        'stats': {'hp':8, 'defense':0, 'power':4, 'xp':18}
    }
    ORC = {
        'name': 'Orc',
        'character': 'o',
        'color': libtcod.desaturated_green,
        'stats': {'hp':14, 'defense':1, 'power':5, 'xp':35}
    }
    TROLL = {
        'name': 'Troll',
        'character': 'T',
        'color': libtcod.darkest_green,
        'stats': {'hp':30, 'defense':2, 'power':10, 'xp':80}
    }
    OGRE = {
        'name': 'Ogre',
        'character': 'O',
        'color': libtcod.darker_green,
        'stats': {'hp':45, 'defense':4, 'power':15, 'xp':120}
    }

    def make_creature_entity(x, y, creature_type):
        creature_value = creature_type.value
        fighter_component = Fighter(**creature_value['stats'])
        # TODO: also define ai in the CreatureType
        ai_component = BasicMonster()
        monster = Entity(x, y,
            creature_value['character'],
            creature_value['color'],
            creature_value['name'],
            blocks=True,
            render_order=RenderOrder.ACTOR,
            fighter=fighter_component,
            ai=ai_component)
        return monster
