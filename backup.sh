#!/bin/sh

BACKUP_DIR=saved_games

# Loop until there is not a save file for that number.
i=0
while true
do
  i=$(expr $i + 1)
  if [ ! -f "$BACKUP_DIR/$i" ]
  then
    cp savegame.dat "$BACKUP_DIR/$i"
    break
  fi
done
