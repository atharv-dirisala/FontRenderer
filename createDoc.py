from petalRenderer import *
import shutil
from pathlib import Path
from PIL import Image

def clearFolder():
    folder = Path('pictures')
    shutil.rmtree(folder)
    folder.mkdir(parents=True, exist_ok=True)

def makeDocument(fileName):
    clearFolder()
    saveImages(fileName)
    fileNum = sum(1 for x in Path('/Users/atharvdirisala/Documents/programs/Python/fontRenderer/pictures').iterdir() if x.is_file())
    head = Image.open('pictures/0.png').convert("RGB")
    remainder = [Image.open("pictures/" + str(i) + ".png") for i in range(1, fileNum)]
    head.save("document.pdf", save_all=True, append_images=remainder)

def song():
    songName = input("Choose a song from the songs folder (without txt): ")
    try:
        print("Attempting to render font...")
        makeDocument("songs/" + songName + ".txt")
        print("Rendering font...")
        print("COMPLETE: Song made! Check the document created.")
    except:
        print("ERROR: Song does not exist.")

song()
