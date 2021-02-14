from enum import Enum

import libtcodpy as libtcod

from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.item import Item
from entity.entity import Entity
from game_messages import Message
from item_functions import cast_confuse, cast_fireball, cast_lightning, heal
from random_utils import random_d2
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
        'color': libtcod.dark_blue,
        'item': None,
        # 'equipable': Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
        'equipable': {
            'slot': EquipmentSlots.MAIN_HAND,
            'defense_bonus': 0,
            'power_bonus': 3
        }
    }
    SHIELD = {
        'name': 'Shield',
        'character': '[',
        'color': libtcod.darker_orange,
        'item': None,
        #'equipable': Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1)
        'equipable': {
            'slot': EquipmentSlots.OFF_HAND,
            'defense_bonus': 1,
            'power_bonus': 0
        }
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

    def make_item_entity(x, y, item_type, dungeon_level):
        item_value = item_type.value

        # Equipment can be more powerful the deeper you go.
        bonus = random_d2(dungeon_level // 4)

        # Possibly add name modifier, e.g. "Sword +2"
        name = item_value['name']

        equip_values = item_value['equipable']
        if equip_values:
            if bonus > 0:
                name += " +" + str(bonus)
            # Assign bonus to either non-zero stat.
            defense_bonus = 0 if equip_values['defense_bonus'] == 0 else equip_values['defense_bonus'] + bonus
            power_bonus = 0 if equip_values['power_bonus'] == 0 else equip_values['power_bonus'] + bonus

            equipable_component = Equippable(equip_values['slot'], defense_bonus = defense_bonus, power_bonus = power_bonus)
        else:
            equipable_component = None

        item = Entity(
            x, y,
            item_value['character'],
            item_value['color'],
            name,
            render_order=RenderOrder.ITEM,
            item=item_value['item'],
            equippable=equipable_component)
        return item
