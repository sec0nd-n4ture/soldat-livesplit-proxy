# Runmode LiveSplit
![livesplitdemo](https://user-images.githubusercontent.com/38664511/144734428-7d7fbf47-03f7-4045-a7cc-a206149c51b5.png)

# How to use:
    Download Python3 and optionally install PySocks (Not required).
    Download RunmodeLiveSplit.py and proxycfg.ini, make sure they are in the same folder.
    Execute RunmodeLiveSplit.py and join localhost:23666 in Soldat.


# Configuration:
    All fields of proxycfg.ini can be edited and are applied in real time.
    Interface can be moved around by changing anchorXY value in proxycfg.ini.
    Colors can be changed and are hexadecimal colors.
    Server is hardcoded in RunmodeLiveSplit.py as 217.182.78.135:23080 (Midgard Runmode).
    
https://user-images.githubusercontent.com/38664511/144734661-67ac29d7-6198-4ab9-8f87-b64859c74452.mp4

# TODO:
    Make interface scaling dynamic.
    Implement a db to save and load best checkpoint times.
    Add support for maps with laps.
    
    Find a way to:
        detect a completed run
        resolve map name dynamically
        find out checkpoint count
