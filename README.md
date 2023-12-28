Finished Development: 10/04/2021

Important Note: Makes sure you run this using Python3.9 because it crashes in 3.12 if you are trying
to run older versions of the game

# Summary
This was my third iteration on an endless platformer. My first two I abandoned after only working on them for around
6 hours. This was my first "large-scale" project. Part of this code made its way into my game engine that I build from
scratch. My senior year of high school I would make another version of this code that worked a lot better. It had original
pixel art! I started working on this project with my cousin. He, however, quit pretty early in the project and
had minimal contributions (less than 1% of code base).

# Monumental Commits
### Generation of enemies and platforms: 02/01/2021
commit d0e5d53715a2e645761a2bc7cee73b76727c3995

This was the last commit I made before I stopped working on the project for over four months. It was still a working 
game, but was quite buggy. Platform generation worked, collisions worked mostly, and jumping was still pretty glitchy. 
The overall feel of the game was quite good at this point though and it feels very nostalgic to look at - not very polished, 
but still was fun

### Last Commit Before Moving To Velocities: 06/29/2021
commit 2e4247bd8a15378d1a90126685ee65ea057b1381

This was the last commit I made before switching to using velocities and deltaTime. At the time I had something called a
ConsistencyKeeper that figured out the ratio between the average running time when the game values were fine tuned and the
average running time now. Then it would use the ratio to find what those values should be. I reasoned that different machines
run at different speeds and the more code I added, the slower the code would get. Thankfully, I eventually switched to 
velocities and deltaTime

### Switched to Velocity and deltaTime: 07/26/2021
commit dc0284763dfa06263df935ce13ed19f69e15cefb

Changed the code to using velocities for objects and deltaTime (like Unity and most game engines). The velocity would 
be multiplied by the deltaTime to find the distance. A very important change!

### Last Commit Before Changing Textures: 08/16/2021
commit caed3bf0cc56988b5fe0016920c91afd5d910ee0

This was the last commit I made before changing the textures. The game at this point felt pretty good and most of the 
game mechanics from this point forward stayed relatively the same.

### Changed the Textures: 08/17/2021
commit cec31b55a922d987eb8933093e75643a1ad9098e

Changed the look of the game completely. It looks much better after this modification! There is also a funny bug where you
can stick to the ceiling infinitely by holding up while on the ceiling (jump into ceiling and keep the up arrow held in)

### Changed the textures and made it more fun: 09/28/2021
commit d3e058e0e15c4e5698cc772faa43be67856e667d

Changed textures, fixed some bugs, overall more fun


### Last Commit I made before Nov. 2023 Revisions: 10/04/2021
commit ea56332b7cf0f62543c949f8449789a6a9f79244

Movement playground to test the slowing down and other code

# Bug Fixes 12/27/2023
- Fixed some deceleration and collision code (minor, but important changes)
- Reinstated the endless platformer code (uncommented code and deleted quick test code)
- Made the file structure prettier
