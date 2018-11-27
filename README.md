# Developing AI Agent to play a simplified version of Magic The Gathering

The objective of this repository is to research some AI and deep learning techniques to 
train an agent to play a game. The main focus is to personally learn this technology.

A game engine will be developed along side the agent, adding features to make the 
game more complex, and observe the agent behaviour on different scenarios.

## test_game.py

This script is used to start a Magic game.

Usage:

Optional arguments:
 - **--game_type** Path to the game configurations file (.json). 
    Defaults to 'config/game_normal.json'.
- **--deck_1** Deck file for player 1 (.txt). 
    Defaults to 'config/deck_basic.txt'.
- **--deck_2** Deck file for player 2 (.txt). 
    Defaults to 'config/deck_basic.txt'.

Basic usage:

````bash
python test_game.py
````