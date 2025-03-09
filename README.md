[![Code style: black](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/psf/black)
<p align="center">
Bullet hell OCR A-level project using pygame.  
</p>

## Assets
Font used - [edit-undo](https://www.dafont.com/edit-undo.font)  
Sprite editor - [aseprite](https://www.aseprite.org/)  
### Music
Main menu - [HOYO-MiX - Oneiros of Borehole Planet | Honkai Star Rail](https://www.youtube.com/watch?v=yQ-rcBeFKVw)  
Stage 1 - [Chris Christodoulou - Moisture Deficit | Risk of Rain (2013)](https://www.youtube.com/watch?v=RbzA6lX84xM)  
### Links
[Trello board](https://trello.com/b/xCHQx3Uu/shmup-trello)  
## Version changelog
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
- fixed audio bugs and made new audio class for handling future audio better [#30]
- optimised stage transition logic by removing redundant code [#31]
### v0.0.3 prototype
- #### file structure rework - top level file loads in rest of the modules. All modules rewritten and optimised Lazy loading implemented.
- screen now works with any 16:9 resolution. All graphics are scaled appropriately [#32]
- event manager implemented that tracks all user input [#33]
- event handler reworked to use event manager and optimised [#34]
- event handler can manage button combinations including overlapping button combinations (e.g. A and SHIFT + A being different) [#35]
- screen can toggle fullscreen with F11 [#36]
- screen can toggle borderless with SHIFT + F11 [#37]
- assets loaded in using a class that searches a directory for files instead of one by one [#38]
- some assets now use lazy loading: asset loading class creates dict of file paths instead of loading file directly [#39]
- spritesheet loading class reworked into a function that returns a list containing the subsurfaces [#40]
- button class improved and optimised. A class for text labels on buttons and a class for image labels on buttons [#41]
- button image class can now use the button image label as the entire button using pixel perfect collision [#42]
- main menu design reworked. Main title at the top of the screen and splash art and main menu buttons below [#43]
- introduced state manager for managing traversing states from a centralised location [#44]
- improved quit event handling by centralising it in the state manager [#45]
- added ability to switch between splash arts using arrow keys [#46]
- implemented widget manager for managing ui elements like buttons or text on the screen [#47]
- centralised screen variable to avoid having to call pygame.display.get_surface() [#48]
- reworked some global variables to use frozen dataclasses to group data [#49]
- reworked honestly garbage collision manager. Now uses rect collisions [#50]
