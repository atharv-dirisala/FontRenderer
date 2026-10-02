import pygame
from tokenizer import *

pygame.init()
screen = pygame.display.set_mode((1400, 685))
pygame.display.set_caption("Mangol Mir Font Renderer")

# Preloads the petals of images.
images = {}

def preLoad():
    petals = ['a', 'ā', 'i', 'u', 'e', 'o', 'gā', 'gi', 'k', 'l', 'm', 'f', 's', 'y', 'h', 'r', 'sh', 'w', 'v', 'mb', 'ng', 'n', 'nk', 'b', 'ky', 'ksh', 'nm', 'z', 'j']
    for petal in petals:
        images[petal] = pygame.image.load("petals/" + petal + ".png").convert_alpha()

preLoad()

# Function to render a petal to get its bounding box.
def renderPetal(petal, angle):
    image = images[petal]

    match petal:
        case 'h' | 'r' | 'sh':
            xOff = 5
        case 'w' | 'v' | 'mb':
            xOff = -5
        case 'ng' | 'n' | 'nk':
            xOff = 13
        case 'b' | 'ky' | 'ksh':
            xOff = -13
        case _:
            xOff = 0

    rotate = pygame.Vector2(xOff, -image.get_size()[1] / 2 - 15).rotate(angle)

    rotateImage = pygame.transform.rotozoom(image, -angle, 1.0)

    newPosition = rotateImage.get_rect(center = rotate)

    bounds = rotateImage.get_bounding_rect()
    left = newPosition.left + bounds.left
    right = newPosition.left + bounds.right

    return (rotateImage, newPosition, left, right)

# Draws a petal on the screen.
def drawPetal(background, image, position, offset):
    position = position.move(offset)
    background.blit(image, position)

# The angular values of how petals look.
def bounds(petal):
    match petal:
        case 'k' | 'l' | 'm':
            return (-22, 22)
        case 'f' | 's' | 'y':
            return (-22, 22)
        case 'h' | 'r' | 'sh':
            return (-22, 22)
        case 'w' | 'v' | 'mb':
            return (-22, 22)
        case 'ng' | 'n' | 'nk':
            return(-22, 38)
        case 'b' | 'ky' | 'ksh':
            return (-38, 22)
        case 'nm' | 'z' | 'j':
            return (-38, 38)
        case 'a' | 'ā' | 'gā':
            return (-22, 22)
        case 'i' | 'u' | 'gi':
            return (-12, 12)
        case 'e' | 'o':
            return (-26, 26)

# Renders all of the petals on a flower to get its bounding box.
def renderPetals(petals):
    angles = [0]
    
    highBound, lowBound = bounds(petals[0])
    highBound += 360
    for i in range(1, len(petals) - 1):
        bound = bounds(petals[i])
        span = bound[1] - bound[0]
        angles.append(lowBound - bound[0])
        lowBound += span

    if len(petals) > 3:
        bound = bounds(petals[-1])
        span = bound[1] - bound[0]
        angles.append(((lowBound - bound[0]) + (highBound - bound[1])) / 2)
    elif len(petals) > 1:
        bound = bounds(petals[-1])
        span = bound[1] - bound[0]
        angles.append(180)
    
    boundLeft = float('inf')
    boundRight = float('-inf')
    images = []
    for i in range(len(petals)):
        petal = renderPetal(petals[i], angles[i])
        images.append((petal[0], petal[1]))
        boundLeft = min(boundLeft, petal[2])
        boundRight = max(boundRight, petal[3])

    return (images, boundLeft, boundRight)

# Renders the full word with all the flowers, and again, gets the bounding box.
def renderFlowers(petals):
    flowers = [[petals[0]]]

    highBound, lowBound = bounds(petals[0])
    highBound += 360

    for i in range(1, len(petals)):
        bound = bounds(petals[i])
        span = bound[1] - bound[0]
        if lowBound + span > highBound:
            flowers.append([petals[i]])
            highBound, lowBound = bound
            highBound += 360
        else:
            flowers[-1].append(petals[i])
            lowBound += span
    
    allImages = []
    lowers = []
    highers = []
    for flower in flowers:
        images, lowBound, highBound = renderPetals(flower)
        allImages.append(images)
        lowers.append(lowBound)
        highers.append(highBound)

    return (allImages, lowers, highers)

# Draws out a full word.
def drawWord(background, flowers, lowers, highers, position):
    prevRight = 0
    totalOffset = 0
    for flower in range(len(flowers)):
        offset = prevRight - lowers[flower]
        totalOffset += offset
        pygame.draw.circle(background, (0, 0, 0), (position[0] + totalOffset, position[1]), 20, 10)
        for petal in flowers[flower]:
            drawPetal(background, petal[0], petal[1], (position[0] + totalOffset, position[1]))
        prevRight = highers[flower]

# Draws out the full line.
def drawSentence(background, words, xLeft, xRight, yPos):
    x, y = xLeft, yPos
    prevRight = 0
    for word in words:
        flowers, lowers, highers = renderFlowers(word)
        offset = prevRight - lowers[0]
        totalOffset = sum(highers) - sum(lowers)
        if x + totalOffset > xRight:
            x = xLeft
            y += 300
        drawWord(background, flowers, lowers, highers, (x, y))
        x += totalOffset
        x += 50
        prevRight = highers[-1]
    return y

# Inputs texts.
def getInput(fileName):
    with open(fileName, 'r', encoding='utf-8') as file:
        mangolMir = []
        english = []
        while True:
            mangol = file.readline()
            if not mangol:
                break
            if not mangol.strip():
                continue
            eigo = file.readline()
            mangolMir.append(mangol.strip())
            english.append(eigo.strip())
    return english, mangolMir

# Saves all of the images into a folder.
def saveImages(fileName):
    english, mangolMir = getInput(fileName)
    font = pygame.font.Font(None, 50)

    for i in range(len(english)):
        eigo = english[i]
        mangol = mangolMir[i]
        screen.fill((255, 255, 255))

        englishText = font.render(eigo, True, (0, 0, 0))
        mangolText = font.render(mangol, True, (0, 0, 0))
        tokenized = fullProcesser(mangol)
        screen.blit(englishText, (0, 0))
        screen.blit(mangolText, (0, 50))
        y = drawSentence(screen, tokenized, 0, 1400, 250)

        crop = pygame.Rect(0, 0, 1400, y + 135)
        crop = screen.subsurface(crop)
        pygame.image.save(crop, "pictures/" + str(i) + ".png")

        from PIL import Image, ImageOps
        ImageOps.expand(Image.open("pictures/" + str(i) + ".png"), border=20, fill="white").save("pictures/" + str(i) + ".png")
