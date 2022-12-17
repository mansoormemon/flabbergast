# Types of Screens

1. Home

   - Play
   - Settings
     - Name
     - Sprite
   - Exit

2. Story

3. Game

4. Win

5. End Screen

# Levels

- 1
- 2
- 3
- 4
- Final

# Strategies

- Game opens at the Home / Main Menu screen.
- Once the game is started, the levels will progress until the game ends.
- The game can not be resetted until it ends.
- If (for any reason) the game halts mid-game, the level will restart but the levels completed prior to that will be saved.
- When a level is completed, a cut scene (story) shows up and after it ends, the player moves on to the next level.
- Cut scene will be part of the next level.
- Game auto saves progress when a level is completed.
- The cycle is propagates as follows:
    1. Cut Scene (Level n)
    2. Game
    3. if death, go to step 2.
    4. if halt, go to step 1.
    5. level n complete
    6. save game at level n
    7. Cut Scene (Level n + 1)
