

## TODO list

* Pull number pad key handling from original tutorial
In part 11, the original tutorial added number pad key support, with diagonals and 5 for wait.  This version of the tutorial uses the awful "hjkl" direction keys and even worse "yubn" diagonals. And "z" for wait. 'Cause that makes sense.

* Randomize combat
I want to add a random element to combat.  This will avoid leveling up to where lesser creatures have no chance to hurt you.  My idea for randomness is to "flip a coin" i.e. roll a two sided die for each point.  So for a power of 5, roll 5d2.  The sum will be 0-5.  This makes the range of values correspond nicely (directly) to the stated values.
By making defense randomized as well, it will avoid where some creatures cannot ever damage you.  On average, the values from the random function will be 1/2 the value of the stat.  I could compensate by doubling the stats in each creature type.

* Dialog
Interaction other than fighting.  I'm imagining SIMs like menus of ways to interact.

* Data-driven components
Items, monsters, NPCs, places defined in data.
Spells are more closely tied to code, b/c of the diverse possible affects.

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
