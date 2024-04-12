![](https://github.com/r5nnn/shmup/blob/main/assets/textures/icon/logo.png)  
Bullet hell (shoot em up) esque A-level project using pygame.  
## Assets
Font used - [edit-undo](https://www.dafont.com/edit-undo.font)  
Sprite editor - [aseprite](https://www.aseprite.org/)  
### Music
Main menu - [HOYO-MiX - Oneiros of Borehole Planet | Honkai Star Rail](https://www.youtube.com/watch?v=yQ-rcBeFKVw)  
Stage 1 - [Chris Christodoulou - Moisture Deficit | Risk of Rain (2013)](https://www.youtube.com/watch?v=RbzA6lX84xM)  
### Links
[Trello board](https://trello.com/b/xCHQx3Uu/shmup-trello)  
## version changelog
### v0.0.1 prototype
- #### created menu concept, and a prototype of player movement and shooting aswell as a test dummy enemy.
- created color palette [#1]
- created character sprite [#2]
- created title screen [#3]
- added pause screen [#4]
- added keybinds screen [#5]
- added character movement [#6]
- added menu music [#7]
- updated background [#8]
- added sfx for buttons [#9]
- added character slow down when modifier key held down [#10]
- updated character sprite when moving [#11]
- created bullets [#12]
- created enemies [#13]
- added collision detection with bullets and hitbox [#14]
- added health to enemies [#15]
### v0.0.2 prototype
- #### workflow rework - screens are loaded/unloaded using a state stack. All modules reworked and rewritten. Event handling now uses observer pattern.
- added deltatime for compatibility when not at fps cap [#16]
- added method for placing relative to top left or center [#17]
- added text wrapping [#18]
- created new title images for screens [#19]
- images now scale to the pygame window instead of being scaled up in the file itself [#20]
- added more placing methods for buttons and images [#21]
- created spritesheet class [#22]
- player images now stored in spritesheet and json file [#23]
- can now refer to the coordinates of wrapped text [#24]
- added documentation according to the google style guide for python [#25]
- type hints are now more accurate for all modules and classes [#26]
- created event manager class using observer pattern for event handling [#27]
- updated button clicking logic [#28]
- player movement and sprites now update based on latest key pressed [#29]
