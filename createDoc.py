from petalRenderer import *
import shutil
import os
from pathlib import Path
from PIL import Image

# Clear the folder of snapshots/
def clearFolder():
    folder = Path('pictures')
    shutil.rmtree(folder)
    folder.mkdir(parents=True, exist_ok=True)

# Takes the font rendering and puts it into a document.
def makeDocument(fileName):
    clearFolder()
    saveImages(fileName)
    fileNum = sum(1 for x in Path('/Users/atharvdirisala/Documents/programs/Python/fontRenderer/pictures').iterdir() if x.is_file())
    head = Image.open('pictures/0.png').convert("RGB")
    remainder = [Image.open("pictures/" + str(i) + ".png") for i in range(1, fileNum)]
    head.save("document.pdf", save_all=True, append_images=remainder)

# Asks input from the user for the song.
def song():
    songName = input("Choose a song from the songs folder (without txt): ")
    try:
        if not os.path.exists('pictures'):
            os.makedirs('pictures')
        print("Attempting to render font...")
        makeDocument("songs/" + songName + ".txt")
        print("Rendering font...")
        print("COMPLETE: Song made! Check the document created.")
    except:
        print("ERROR: Song does not exist.")

song()
