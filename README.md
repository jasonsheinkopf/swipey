# 🎮 Drift: A Minimalist Swipe-Physics Game

A meditative, physics-driven game where a lone sphere drifts through space. Use mouse swipes to impart momentum, collecting targets while exploring the depths of frictionless movement.

## Overview

**Design Philosophy:** Less is more. Every element is intentional. The game rewards mastery of subtle physics rather than reflexes.

## Features

- **Frictionless Physics**: Velocity persists indefinitely - every swipe matters
- **Screen Wrapping**: Seamless edge wrapping creates an infinite space
- **Procedural Audio**: All sounds generated at runtime using Web Audio
- **Twinkling Starfield**: Procedurally animated background
- **Configurable Swipe System**: Fine-tune your control with three parameters:
  - **Strength** (Q/A): Control impulse magnitude (1-10)
  - **Focus** (W/S): Which portion of swipe matters (1-10)
  - **Smoothness** (E/D): Direction averaging (1-10)

## Installation

```bash
git clone <repo>
cd swipey
pip install -r requirements.txt
```

## Running the Game

```bash
python src/main.py
```

## How to Play

1. **Move**: Click and drag (swipe) with your mouse to impart momentum to the white sphere
2. **Collect**: Touch the pulsing collectible to score points
3. **Adjust**: Use keyboard controls to fine-tune swipe parameters:
   - Q/A: Increase/decrease Strength
   - W/S: Increase/decrease Focus
   - E/D: Increase/decrease Smoothness
4. **Quit**: Press ESC or close the window

## Technical Details

- **Built with**: Python 3.8+, Pygame, NumPy
- **No external assets**: All visuals and audio are procedurally generated
- **Minimalist design**: Clean code, focused gameplay

## Requirements

- Python 3.8 or higher
- pygame >= 2.5.0
- numpy >= 1.24.0
