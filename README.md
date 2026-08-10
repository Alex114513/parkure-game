# **Parkour game**

## Overview

This is a basic parkour game based on python and pygame.

## Features

- Side-scrolling platform movement
- Jumping and ground detection
- Main menu and scene transitions
- New save and load save support
- Pause menu

## Controls

- A and D for moving left and right
- W for jumping
- Esc for pausing
- 0 key for editing mode (only when `debug_mode = True` in const.py)
- L and R for rotating platform (in edit mode)
- Left-arrow,Right-arrow,Up-arrow and Down-arrow for resizing platform(in edit mode)

## How to run

1. Install Python 3.10 or newer.
2. Install pygame and blinker by running `pip install pygame blinker`
3. Run the game by `python main.py`(before,please use`cd`to cd into the project file(Parkour game) )



## Project Structure

* [main.py](<vscode-file://vscode-app/c:/Users/ALEXXXXXXXXXXXXXXXXX/AppData/Local/Programs/Microsoft%20VS%20Code/df53daabb1/resources/app/out/vs/code/electron-browser/workbench/workbench.html>) - Program entry point
* [scenes](<vscode-file://vscode-app/c:/Users/ALEXXXXXXXXXXXXXXXXX/AppData/Local/Programs/Microsoft%20VS%20Code/df53daabb1/resources/app/out/vs/code/electron-browser/workbench/workbench.html>) - Game scenes such as title, gameplay, save menu, and pause menu
* [sprites](<vscode-file://vscode-app/c:/Users/ALEXXXXXXXXXXXXXXXXX/AppData/Local/Programs/Microsoft%20VS%20Code/df53daabb1/resources/app/out/vs/code/electron-browser/workbench/workbench.html>) - Player, platforms, and other game objects
* [configs](<vscode-file://vscode-app/c:/Users/ALEXXXXXXXXXXXXXXXXX/AppData/Local/Programs/Microsoft%20VS%20Code/df53daabb1/resources/app/out/vs/code/electron-browser/workbench/workbench.html>) - JSON configuration files
* [saves](<vscode-file://vscode-app/c:/Users/ALEXXXXXXXXXXXXXXXXX/AppData/Local/Programs/Microsoft%20VS%20Code/df53daabb1/resources/app/out/vs/code/electron-browser/workbench/workbench.html>) - Player save data
* [tests](<vscode-file://vscode-app/c:/Users/ALEXXXXXXXXXXXXXXXXX/AppData/Local/Programs/Microsoft%20VS%20Code/df53daabb1/resources/app/out/vs/code/electron-browser/workbench/workbench.html>) - Automated tests

## Current Status

This project is still in active development.A lot if features(like NPCs,levels and enimies etc.) are not implemented yet.
