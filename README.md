# BYTEHAVEN — The Lost Containers

> A 2D side-scrolling platformer shooter built with Python and Pygame.

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.6-green?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?logo=windows)
![License](https://img.shields.io/badge/License-Academic-orange)

---

## Overview

**Bytehaven** is a cyberpunk-themed 2D platformer where the player controls **Prometheus**, a rogue cyborg on a mission to recover corrupted data containers scattered across two hostile zones.

Navigate handcrafted platforms, eliminate or dodge two enemy archetypes, collect all three data containers per stage, and reach the exit — all while managing HP and avoiding enemy fire.

---

## Gameplay

| Action | Key |
|---|---|
| Move Left / Right | `A` / `D` |
| Jump | `W` or `Space` |
| Shoot | `Left Ctrl` |
| Return to Menu | `Esc` |

### Objective
1. Collect all **3 data containers** hidden across the level
2. Reach the **EXIT** portal — unlocked after all containers are collected
3. Complete both levels to win and submit your score to the **Top 10 leaderboard**

### Enemies
| Type | Behavior | HP | Score |
|---|---|---|---|
| **Biker** | Patrols platform, deals contact damage | 80 | 100 pts |
| **Punk** | Patrols and fires projectiles | 60 | 125 pts |

### Lose Condition
HP reaches zero — a death animation plays and the run ends.

---

## Features

- **2 handcrafted levels** with unique platform layouts and enemy placements
- **Parallax scrolling background** with 3 depth layers
- **Animated sprites** — idle, run, jump, attack, hurt and death states
- **Sound effects** — jump, shoot, hurt, enemy death, container collect
- **Background music** per screen (menu, level 1, level 2, victory)
- **Persistent leaderboard** — Top 10 scores saved to local SQLite database
- **Score screen** with name entry (up to 4 characters) after each run
- **Camera system** that follows the player across a 3200 px world
- **Corrupted zone** — instant death if the player falls below the ground

---

## Architecture & Design Patterns

This project demonstrates software design patterns applied to game development:

| Pattern | Class | Role |
|---|---|---|
| **Factory** | `EntityFactory` | Centralises creation of Player, Enemies, Shots and Containers |
| **Mediator** | `EntityMediator` | Decouples collision logic between all entity types |
| **Proxy** | `DBProxy` | Wraps SQLite access behind a clean interface |
| **Abstract Class** | `Entity` | Defines the contract (`update` / `draw`) for all game entities |

---

## Project Structure

```
Bytehaven/
├── main.py                  # Entry point
├── setup.py                 # cx_Freeze build config
├── asset/
│   ├── audio/               # Music (.mp3) and sound effects (.wav)
│   └── sprites/             # Sprite sheets and background layers
└── code/
    ├── Const.py             # Global constants
    ├── Paths.py             # Frozen-aware base path helper (dev + exe)
    ├── Entity.py            # Abstract base class for all entities
    ├── Player.py            # Player logic, physics and animation
    ├── Enemy.py             # Enemy AI — patrol and shoot behaviours
    ├── Shot.py              # Projectile movement and collision
    ├── Container.py         # Collectable data container
    ├── Background.py        # Parallax background renderer
    ├── EntityFactory.py     # Factory pattern
    ├── EntityMediator.py    # Mediator pattern — all collision logic
    ├── DBProxy.py           # Proxy pattern — SQLite leaderboard
    ├── SoundFX.py           # Sound effect manager
    ├── Level.py             # Level data, camera and game loop
    ├── Menu.py              # Main menu screen
    ├── Score.py             # Score entry and leaderboard screen
    └── Game.py              # State machine (Menu → Level → Score)
```

---

## Running from Source

**Requirements:** Python 3.12+ and Pygame 2.6+

```bash
# Install dependencies
pip install pygame

# Run the game
python main.py
```

---

## Building the Windows Executable

```bash
pip install cx_Freeze
python setup.py build
```

The compiled game is output to `build/exe.win-amd64-3.xx/`.  
Run `Bytehaven.exe` — no Python installation required.

---

## Tech Stack

| Tool | Version |
|---|---|
| Python | 3.13 |
| Pygame | 2.6.1 |
| SQLite3 | stdlib |
| cx_Freeze | 8.6.4 |

---

## Asset Credits

- **Character & enemy sprites** — [Free 3 Cyberpunk Sprites Pixel Art](https://ansimuz.itch.io/cyberpunk-street-maincharacter) by Ansimuz
- **Gun animations** — [Free Guns for Cyberpunk Characters](https://ansimuz.itch.io/guns-pack) by Ansimuz
- **Background layers & tiles** — Generated with Claude AI (800×450 px and 32×32 px PNG)
- **Audio** — Royalty-free SFX and music from [OpenGameArt.org](https://opengameart.org)

---

## Academic Context

Developed as the practical assignment (*Atividade Prática*) for the course  
**Linguagem de Programação Aplicada** — UNINTER, 2026.

**Requirements met:**
- [x] Playable 2D demo
- [x] Player-controlled character with challenge
- [x] Win and lose conditions
- [x] Main menu with controls listed
- [x] Executable delivery (`.exe` + assets in `.zip`)
- [x] Software design patterns — Factory, Mediator, Proxy, ABC
