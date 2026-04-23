![](https://github.com/SagiriHimoto/SillyTileDisplay/blob/main/preview.gif?raw=true)
# Tile Display Program
![](https://img.shields.io/github/stars/SagiriHimoto/SillyTileDisplay.svg) ![](https://img.shields.io/github/forks/SagiriHimoto/SillyTileDisplay.svg) ![](https://img.shields.io/github/issues/SagiriHimoto/SillyTileDisplay.svg)

**For all your tileset previewing needs, provides an easy and flexible way to load any layout and draw a tileset for it!**
And it comes with prepackaged layout configurations for games such as "Mega Man Maker"!

------------

### Features

- Display that renders tiles as configured y the user;
- Full customization of every overlay, layout and program's design;
- Overlays on F1-3 keys;
- Simple navigation through tiles using arrows keys;
- Automatically reloades tilesets when you edit the file;
- Custom guides and keyboard functionallity;
- I even commented the code!!! (a bit);

------------

### Installation

To use this silly tool, you need!<br/><br/>**Watchdog:**<br/>
```cmd
pip install watchdog
```
**Pygame:**<br/>
```cmd
pip install pygame
```
(you also need "os" and "time", if you don't have those installed)<br/><br/>**to check if you have everything installed:**
```cmd
python setup.py
```
**OR just open `setup.bat`**

------------

### Run
**Have everything installed? Now you're ready to run! Just use:**
```cmd
python main.py
```
**OR just open `run.bat`**

------------
### How to use
> [!TIP]
> You can contact me or create an issue for help
#### Tileset File
By default, `main.py` prompts user to input a tileset file (e.g. "tstTileset" to use "tstTileset.png")<br/>This behaviour can be changed. Edit line 17: 
```py
TILESET_FILE = input(f"Tileset file name: ") + ".png"
```
and replace it with:
```py
TILESET_FILE = "tstTest.png"
``` 
this will load th file "tstTest.png", without prompting the user to input the file name, allowing for quick use. 
#### Config File 
By default, `main.py` automatically uses the file `config_mmm.json`, which is the file that replicates "Mega Man Maker" tiling system (tiles 50, 59 and 60 are not supported by "Mega Man Maker" engine). This file can be replaced with any other user-created json file, or with a prompt for input, if the user wants to constantly choose which file they want to use (recommended for installations with multiple json configs)<br/>Edit line 16:
```py
CONFIG_FILE = "config_mmm.json"
```
Replace "config_mmm" with any json file name. Or make this edit:
```py
CONFIG_FILE = input(f"Config file name: ") + ".json"
```
This edit will make it so that the script prompts the user every time, to provide the name of a config file they'd like to use.
#### Overlay File
This script provides users with the ability to overlay any picture over the tileset. This allows users to quickly reference information for editing or testing the tileset.  This script comes prepackaged with three overlays (for "Mega Man Maker" tilesets):

* overlay_a.png
  - Indicates tile numbers from config_mmm.json | **`F1`** 
* overlay_b.png
  - Indicates vertically and horizontally odd/even tiles with colored circles | **`F2`**
* overlay_c.png
  - Indicates "bridges", "pillars", "corners", and "walls" with silly small icons | **`F3`**


User can change overlays by editing these files, or by editing lines 18-20:
```py
OVERLAY_FILE_A = "overlay_a.png"
OVERLAY_FILE_B = "overlay_b.png"
OVERLAY_FILE_C = "overlay_c.png"
```
Any of these can be edited to:
```py
OVERLAY_FILE_A =  input(f"Overlay file \"A\" name: ") + ".png"
OVERLAY_FILE_B = input(f"Overlay file \"B\" name: ") + ".png"
OVERLAY_FILE_C = input(f"Overlay file \"C\" name: ") + ".png"
```
to prompt user for file names instead.
Future versions may add support for more overlays.

------------

This tool is made with love and care &hearts;
