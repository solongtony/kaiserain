from random import randint


def from_dungeon_level(table, dungeon_level):
    for (value, level) in reversed(table):
        if dungeon_level >= level:
            return value

    return 0


def random_choice_index(chances):
    random_chance = randint(1, sum(chances))

    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w

        if random_chance <= running_sum:
            return choice
        choice += 1


def random_choice_from_dict(choice_dict):
    choices = list(choice_dict.keys())
    chances = list(choice_dict.values())

    return choices[random_choice_index(chances)]

# Sum the rolls `count` number 2 sided dice (coin flips),
# but instead of 1 or 2 the values are 0 or 1.
def random_d2(count):
    sum = 0
    for i in range(count):
        sum += randint(0, 1)
    return sum
