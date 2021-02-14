import libtcodpy as libtcod

import math

from components.item import Item

from render_functions import RenderOrder


class Entity:
    # A generic object to represent players, enemies, items, etc.
    def __init__(
            self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE,
            fighter=None, ai=None, item=None, inventory=None, stairs=None,
            level=None, equipment=None, equippable=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        # Components
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.stairs = stairs
        self.level = level
        self.equipment = equipment
        self.equippable = equippable

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

        if self.stairs:
            self.stairs.owner = self

        if self.level:
            self.level.owner = self

        if self.equipment:
            self.equipment.owner = self

        if self.equippable:
            self.equippable.owner = self

            if not self.item:
                item = Item()
                self.item = item
                self.item.owner = self

    # TODO: Move the movement logic.
    # 1) Movement stuff does not need to be in the base Entity class.
    #    Entities like stairs and items do not move.
    # 2) Many of these functions require `game_map` and `entities` as arguments,
    #    make a class representing both e.g. dungeon_level.
    # Logic related to moving an entity itself can go in a new component e.g. `mobile`
    # The `mobile` component can use info methods on the `dungeon_level` object.


    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    # A simple direct line approach.  Used as a backup if no A* path is found.
    def move_towards(self, target_x, target_y, game_map, entities):
        # Cannot use `distance` functions, need normalized distance from dx, dy, and distance.
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance == 0:
            # Avoid division by 0, for example if character died or
            # there is an entity that can occupy the same space as the character.
            distance = 1
            # Don't go anywhere.
            dx = 0
            dy = 0

        # Normalized dx, dy to -1, 0, or 1
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if self.is_coordinate_open(dx, dy, game_map, entities):
            self.move(dx, dy)

    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def distance_to(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        return self.distance(dx, dy)

    # BUG: Monsters stop moving when there is not a continuous path to the PC,
    # even if they could get closer than they are.
    def move_astar(self, target, entities, game_map):
        # Create a FOV map that has the dimensions of the map
        fov = libtcod.map_new(game_map.width, game_map.height)

        # Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                           not game_map.tiles[x1][y1].blocked)

        # Scan all the objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway

        # Update: this causes monsters to stop approaching when they could get closer than they are.
        # The fallback `move_towards` function below does not handle this well, because the simple linear path can be
        # blocked by a wall.
        # Instead, ignore entities for the purpose of pathing, and let the `move` function prevent moving into a
        # blocked space.  This still isn't optimal, b/c the the next step of the A* path could be blocked by an entity,
        # but another closer space could be available.  Could check each surounding space to see if any unblocked space
        # is closer than the current one...
        # for entity in entities:
        #     if entity.blocks and entity != self and entity != target:
        #         # Set the tile as a wall so it must be navigated around
        #         libtcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        my_path = libtcod.path_new_using_map(fov, 1.414213562)

        # Compute the path between self's coordinates and the target's coordinates
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths
        # (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map if
        # there's an alternative path really far away
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            # Keep the old move function as a backup so that if there are no paths (for example another monster blocks
            # a corridor) it will still try to move towards the player (closer to the corridor opening).
            self.move_towards(target.x, target.y, game_map, entities)

            # Delete the path to free memory
        libtcod.path_delete(my_path)


def is_coordinate_open(self, x, y, game_map, entities):
    return (not game_map.is_blocked(x, y)
            and not get_blocking_entities_at_location(entities, x, y))


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
