import libtcodpy as libtcod
from random import randint


from components.stairs import Stairs
from entity.entity import Entity
from game_messages import Message
from entity.creature_types import CreatureTypes
from entity.item_types import ItemTypes
from map_objects.rectangle import Rect
from map_objects.tile import Tile
from random_utils import from_dungeon_level, random_choice_from_dict, random_d2
from render_functions import RenderOrder

STAIRS_DOWN_CHARACTER = '>'

class GameMap:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.dungeon_level = dungeon_level

    def initialize_tiles(self):
        return [[Tile(True) for y in range(self.height)] for x in range(self.width)]

    # TODO: make most of these class fields, and avoid passing them around as params.
    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            new_room = GameMap.create_room(room_min_size, room_max_size, map_width, map_height)

            # run through the other rooms and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid

                self.unblock_room_tiles(new_room)
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # this is the first room, where the player starts
                    # TODO: stairs up would go here.
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 0 or 1)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.unblock_h_tunnel(prev_x, new_x, prev_y)
                        self.unblock_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.unblock_v_tunnel(prev_y, new_y, prev_x)
                        self.unblock_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities)

                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(
            new_x, new_y, STAIRS_DOWN_CHARACTER, libtcod.white, 'Stairs',
            render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

    @staticmethod
    def create_room(room_min_size, room_max_size, map_width, map_height):
        # random width and height
        w = randint(room_min_size, room_max_size)
        h = randint(room_min_size, room_max_size)
        # random position without going out of the boundaries of the map
        x = randint(0, map_width - w - 1)
        y = randint(0, map_height - h - 1)

        # "Rect" class makes rectangles easier to work with
        return Rect(x, y, w, h)

    def unblock_room_tiles(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def unblock_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def unblock_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    #
    # Placing monsters and items
    #

    def place_entities(self, room, entities):
        self.place_monsters(room, entities)
        self.place_items(room, entities)

    def current_chance(self, chance_by_level):
        # print("current_chance: {!s} {!s}".format(self.dungeon_level, chance_by_level))
        return from_dungeon_level(chance_by_level, self.dungeon_level)

    # Put monsters in a room.
    def place_monsters(self, room, entities):
        max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [4, 7], [5, 11]], self.dungeon_level)

        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)

        # TODO: move this into a data file.
        monster_chance_by_level = {
            CreatureTypes.RAT:          [[90, 1], [60, 2], [30, 3], [0, 5]],
            CreatureTypes.LARGE_RAT:    [[70, 1], [60, 2], [40, 4], [20, 6], [0, 8]],
            CreatureTypes.BOA_SNAKE:    [[20, 1], [0, 5]],
            CreatureTypes.GIANT_SPIDER: [[20, 3], [30, 5], [40, 8], [50, 12], [40, 16]],
            CreatureTypes.BROWN_BEAR:   [[15, 6], [20, 8], [30, 10], [50, 12]],

            CreatureTypes.GOBLIN:       [[90, 1], [60, 3], [50, 5], [30, 7], [20, 10], [0, 12]],
            CreatureTypes.ORC:          [[50, 2]],
            CreatureTypes.TROLL:        [[5, 4], [15, 6], [30, 8], [60, 13]],
            CreatureTypes.OGRE:         [[1, 9], [5, 11], [20, 14], [40, 16]]
        }

        current_monster_chances = { m: self.current_chance(chance_by_level)
            for m, chance_by_level in monster_chance_by_level.items() }

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # Check if an entity is already in that location
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(current_monster_chances)
                entities.append(CreatureTypes.make_creature_entity(x, y, monster_choice))

    # Put items in a room.
    def place_items(self, room, entities):
        max_items_per_room = from_dungeon_level([[1, 1], [2, 6]], self.dungeon_level)

        # Get a random number of items
        # TODO: pick a number of items for the entire level instead of per room.
        # using random_d2 to lower the number of items per room.
        number_of_items = random_d2(random_d2(randint(0, max_items_per_room)))

        # TODO: move this into a data file.
        item_chance_by_level = {
            ItemTypes.HEALING_POTION:   [[50, 1]],
            ItemTypes.SWORD:            [        [15, 2],          [25, 4]],
            ItemTypes.SHIELD:           [                 [20, 3],                    [25, 8]],
            ItemTypes.FIREBALL_SCROLL:  [                                    [20, 6]],
            ItemTypes.CONFUSION_SCROLL: [        [15, 2],                    [20, 6]],
            ItemTypes.LIGHTNING_SCROLL: [                          [10, 4],  [20, 6]]
        }
        current_item_chances = { m: self.current_chance(chance_by_level)
            for m, chance_by_level in item_chance_by_level.items() }

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # Check if an entity is already in that location
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(current_item_chances)
                entities.append(ItemTypes.make_item_entity(x, y, item_choice, self.dungeon_level))

    def is_blocked(self, x, y):
        return self.tiles[x][y].blocked

    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)

        return entities
