from enum import Enum

import libtcodpy as libtcod

from components.ai import BasicMonster
from components.fighter import Fighter
from entity.entity import Entity
from render_functions import RenderOrder

class CreatureTypes(Enum):
    # Greenskins
    ORC = {
        'name': 'Orc',
        'character': 'o',
        'color': libtcod.desaturated_green,
        'stats': {'hp':20, 'defense':0, 'power':4, 'xp':35}
    }
    TROLL = {
        'name': 'Troll',
        'character': 'T',
        'color': libtcod.darker_green,
        'stats': {'hp':30, 'defense':2, 'power':8, 'xp':100}
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
