# About

This is a Roquelike game in Python3, starting from the code and ideas from some online tutorials.
The source code originated from http://rogueliketutorials.com/ which in turn came from this original tutorial in Python 2.x http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python%2Blibtcod

To start the game, run `python3 engine.py` or `python engine.py` depending on the name of Python 3 on your system.

# Controls

Movement with arrow keys or number pad keys.

Actions:

Main Menu:        Esc
Pickup (**G**et): g
**I**nventory:    i
**D**rop:         d
use stairs:       Enter
**C**haracter info: c

# Change list

* Randomized combat
Added random element to combat.  This avoids leveling up to where lesser creatures have no chance to hurt you.  The method of randomness is to "flip a coin" i.e. roll a two sided die for each point.  So for a power of 5, roll 5d2.  The sum will be 0-5.  This makes the range of values correspond nicely (directly) to the stated values.
By making defense randomized as well, it will avoids the situation where some creatures cannot ever damage you.  On average, the values from the random function will be 1/2 the value of the stat.  I could compensate by doubling the stats in each creature type.

* Data driven creature definitions
* Data driven item definitions
* Numpad key handling

# Bugs

* Monster movement
Monsters stop moving when there is not a continuous path to the PC, even if they
could get closer than they are.  See "Monster Movement" TODO.

TODO: Is this still a problem?

* Direction key
If I hold a direction key down, character continues to move in that direction
after releasing the key. This can be fatal, if you run into a wall and monsters
keep attacking you. This was specifically mentioned as being addressed in the
original tutorial, need to look that up.

# Roadmap

## Code cleanup

Menus, menu key handling, and menu result handler should all be together in code.

Data definitions for monsters and items should be actual data files, like JSON,
instead of data dictionaries in code.

Better handling for dynamic parts of items and monsters, e.g. item bonuses and monster difficulty.

### Engine

There's way too much inline code in the game engine.  Pull things out into methods.

Implement callbacks/handlers where they make sense instead of using state tracking for everything.

## Features

* More monster types.

* Messaging
show message when path is blocked ("Ouch! ran into the <thing>")
show message / blank line _something_ between turns when fighting

* Unit tests
Needed

* Skills, abilities, classes, etc.

* Arena / Map editor
Ability to create specific scenarios, for testing and fun

* Equipment
1) Organize items by type and number
  * reading a list of 8 of the same potion mixed in with random scrolls is annoying
2) Limit carrying by weight

* Auto walk
ability to walk in one direction until path ends, a monster comes into sight, damage is taken, etc.

* Movement code
Movement code needs to be separated out from the base entity.  Not all entities
move, so that's not the right place for it.

* Monster movement
1) Add a fall-back move calculator for when A* pathing is blocked.
2) Allow monsters to move when not in sight.
   Possibly only if they have seen the player then move to player's last known position.

* Monsters drop loot
Possible loot in monster bodies.

* Healing
Slowly heal over time, possibly faster when resting.

* Hunger
Slowly get hungry.  Don't want it to be a really hard part of the game like in some.

* Dialog
Interaction other than fighting.  I'm imagining SIMs like menus of ways to interact.

* Data-driven components
Items, NPCs, places defined in data.
Spells are more closely tied to code, b/c of the diverse possible affects.

* Up ladders.  Need to save the level state so you can come back to it.

# Possible game additions

## Surface world

* Towns, roads, terrain, etc.

## Civilization Simulation

* NPC traders, artisans, producers and consumers.
* Market forces.
* Law enforcement, military.
* Different cultures.

## Additional Possible Combat Improvements

Here are some ways I've thought of to make combat more advanced.  They have varying levels of complexity, difficulty to implement, and visibility to the player.

* Implement Dodge vs Block
Have a stat for _avoiding_ damage (agility), separate from a stat for _absorbing_ damage (armor).  Corresponding changes to attack would be likelihood of hitting (agility + skill) vs damage from hit (strength and skill).

* Implement wounds vs hitpoints
Track wounds, e.g. light, moderate, severe instead of hitpoints.

* Damage affects you
Damage decreases your strength, agility, speed, etc.

* Body parts
Track which body part was damaged and by how much.  Those woulds can then have very specific affects; arms affect attacking and blocking, legs affect dodge and speed.  Body affects strength and stamina, head affects intelligence, wisdom, observation (hard to model in game).

### Detailed technique based fighting

Choose a specific technique (availability based on skills and equipped items)
* Thrust, jab, slash, chop, swing (requires initiative, the faster the better to avoid enemy blocking, parrying, or dodging)
* Parry & repost (give up initiative, only affective if enemy attacks, most effective if the type of attack is anticipated, if affective then offensive attack successful)
* Block (give up initiative, only affective if enemy attacks, possibly cause rebound/recoil)
* Redirect - switch places with enemy? off balance?
* Grab / lock - physically control part of the enemy.
* Offbalance - put enemy in off balanced state instead of causing damage.
* Throw / sweep / trip - make enemy fall

These things would require a lot more state to be useful.  Some of the things to track would be initiative, balance, speed, readiness.

This is basically a mini game in itself, like JRPG fights.

An "on the ground" state would be interesting, giving someone standing above an advantage.

Would help to have a detailed combat data area, showing your character's perception (varyingly accurate) of the state of all targets in combat range.  You would only need a local map, maybe FOV, not an entire level map visible when fighting.

Take into account ranged combat - actually much simpler than melee fighting.  Shots towards engaged combatants might strike a target different than the one intended.
