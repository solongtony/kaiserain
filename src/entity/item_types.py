from enum import Enum

import libtcodpy as libtcod

from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.item import Item
from entity.entity import Entity
from game_messages import Message
from item_functions import cast_confuse, cast_fireball, cast_lightning, heal
from render_functions import RenderOrder

class ItemTypes(Enum):
    # Potions
    HEALING_POTION = {
        'name': 'Healing Potion',
        'character': '!',
        'color': libtcod.violet,
        'item': Item(use_function=heal, amount=40),
        'equipable': None
    }
    # Equipment
    SWORD = {
        'name': 'Sword',
        'character': '/',
        'color': libtcod.sky,
        'item': None,
        'equipable': Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
    }
    SHIELD = {
        'name': 'Shield',
        'character': '[',
        'color': libtcod.darker_orange,
        'item': None,
        'equipable': Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1)
    }
    # Scrolls
    FIREBALL_SCROLL = {
        'name': 'Fireball Scroll',
        'character': '#',
        'color': libtcod.red,
        'item': Item(
            use_function=cast_fireball, targeting=True,
            targeting_message=Message(
                'Left-click a target tile for the fireball, or right-click to cancel.',
                libtcod.light_cyan),
            damage=25, radius=3),
        'equipable': None
    }
    CONFUSION_SCROLL = {
        'name': 'Confusion Scroll',
        'character': '#',
        'color': libtcod.light_pink,
        'item': Item(
            use_function=cast_confuse, targeting=True,
            targeting_message=Message(
                'Left-click an enemy to confuse it, or right-click to cancel.',
                libtcod.light_cyan)),
        'equipable': None
    }
    LIGHTNING_SCROLL = {
        'name': 'Lightning Scroll',
        'character': '#',
        'color': libtcod.yellow,
        'item': Item(use_function=cast_lightning, damage=40, maximum_range=5),
        'equipable': None
    }

    def make_item_entity(x, y, item_type):
        item_value = item_type.value
        item_component = item_value['item']
        equipable_component = item_value['equipable']
        item = Entity(
            x, y, item_value['character'], item_value['color'],
            item_value['name'], render_order=RenderOrder.ITEM,
            item=item_component, equippable=equipable_component)
        return item
