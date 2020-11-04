from PIL import Image, ImageDraw
import numpy as np
import random

# Convirt RGB value to Hue, Saturation, Luminosity
def rgb_to_hsl(rgbColor):
    var_R = rgbColor[0] / 255
    var_G = rgbColor[1] / 255
    var_B = rgbColor[2] / 255

    minVal = min(var_R, var_G, var_B)
    maxVal = max(var_R, var_G, var_B)
    del_Max = maxVal - minVal

    lum = (maxVal + minVal) / 2

    if del_Max == 0:
        hue = 0
        sat = 0
    else:
        if lum < 0.5:
            sat = del_Max / (maxVal + minVal)
        else:
            sat = del_Max / (2 - maxVal - minVal)
        
        del_R = (((maxVal - var_R) / 6) + (del_Max / 2)) / del_Max
        del_G = (((maxVal - var_G) / 6) + (del_Max / 2)) / del_Max
        del_B = (((maxVal - var_B) / 6) + (del_Max / 2)) / del_Max

        if var_R == maxVal:
            hue = del_B - del_G
        elif var_G == maxVal:
            hue = (1/3) + del_R - del_B
        elif var_B == maxVal:
            hue = (2/3) + del_G - del_R

        if hue < 0:
            hue += 1
        if hue > 1:
            hue -= 1
    return hue, sat, lum

# Calculate Hue value to RGB
def hue_to_rgb(v1, v2, vH):
    if vH < 0:
        vH += 1
    if vH > 1:
        vH -= 1
    if (6 * vH) < 1:
        return (v1 + (v2 -v1) * 6 * vH)
    if (2 * vH) < 1:
        return (v2)
    if (3 * vH) < 2:
        return (v1 + (v2 - v1) * ((2/3) - vH) * 6 )
    return (v1)

# Convirt Hue, Saturation, Luminosity to RGB value
def hsl_to_rgb(hslColor):
    hue = hslColor[0]
    sat = hslColor[1]
    lum = hslColor[2]

    if sat == 0:
        red = lum * 255
        green = lum * 255
        blue = lum * 255
    else:
        if lum < 0.5:
            var_2 = lum * (1 + sat)
        else:
            var_2 = (lum + sat) - (sat * lum)
    
    var_1 = 2 * lum - var_2

    red = 255 * hue_to_rgb(var_1, var_2, hue + (1/3))
    green = 255 * hue_to_rgb(var_1, var_2, hue)
    blue = 255 * hue_to_rgb(var_1, var_2, hue - (1/3))
    # return(var_1, var_2, hue)
    return(abs(int(red)),abs(int(green)),abs(int(blue)))

# Pick a random rgb value
def randColor():
    color = tuple(np.random.choice(range(256), size=3))
    return color

# Reverse a binary number
def reverseBin(bnum):
    newBnum = ''
    for num in bnum:
        if num == '1':
            newBnum += '0'
        else:
            newBnum += '1'
    return str(newBnum)

# Create the complimentary color of input
def newColor(color):
    newColor = []
    for num in color:
        bnum = f'{num:08b}'

        bnum = reverseBin(bnum)

        bnum = int(bnum, 2)

        newColor.append(bnum)
    newColor = tuple(newColor)
    return newColor

def adjustLuminosity(hslColor, cRange):
    hue = hslColor[0]
    sat = hslColor[1]
    lum = hslColor[2]

    amount1 = cRange

    if lum < .9:
        lum += amount1
    else:
        lum -= amount1

    return (hue, sat, lum)

def adjustLumSat(hslColor, cRange):
    hue = hslColor[0]
    sat = hslColor[1]
    lum = hslColor[2]

    amount1 = random.uniform(*cRange)
    amount2 = random.uniform(*cRange)

    if sat < .5 and  lum < .5:
        sat += amount1
        lum += amount2
    else:
        sat -= amount1
        lum -= amount2

    return (hue, sat, lum)

def sortLowestLum(colors):
    hslColors = []
    outputColors = []
    for color in colors:
        hslColors.append(rgb_to_hsl(color))

    hslColors.sort(key = lambda x: x[2])

    for color in hslColors:
        outputColors.append(hsl_to_rgb(color))

    return outputColors

def monolumColorScheme():
    color1 = randColor()
    color2 = hsl_to_rgb(adjustLuminosity(rgb_to_hsl(color1), .10))
    color3 = hsl_to_rgb(adjustLuminosity(rgb_to_hsl(color2), .10))
    color4 = hsl_to_rgb(adjustLuminosity(rgb_to_hsl(color3), .10))
    color5 = hsl_to_rgb(adjustLuminosity(rgb_to_hsl(color4), .10))

    rgbColors = [color1, color2, color3, color4, color5]

    colors = sortLowestLum(rgbColors)

    colors = colors[::-1]

    color1 = colors[0]
    color2 = colors[1]
    color3 = colors[2]
    color4 = colors[3]
    color5 = colors[4]

    print(rgb_to_hsl(color1)[2],rgb_to_hsl(color2)[2],rgb_to_hsl(color3)[2],rgb_to_hsl(color4)[2],rgb_to_hsl(color5)[2])
    print(color1, color2, color3, color4, color5)
    return color1, color2, color3, color4, color5

def complimentaryColor(colors):
    outPut = []
    compColors = []
    for color in colors:
        print(color)
        compColors.append(newColor(color))
    return compColors[::-1]

def monochromeColorScheme():
    color1 = randColor()
    color2 = hsl_to_rgb(adjustLumSat(rgb_to_hsl(color1), (.05, .25)))
    color3 = hsl_to_rgb(adjustLumSat(rgb_to_hsl(color1), (.15, .35)))
    color4 = hsl_to_rgb(adjustLumSat(rgb_to_hsl(color1), (.25, .45)))
    color5 = hsl_to_rgb(adjustLumSat(rgb_to_hsl(color1), (.35, .55)))

    print(color1, color2, color3, color4, color5)
    return color1, color2, color3, color4, color5

def complimentaryColorScheme():
    cRange = (.05,.25)
    color1 = randColor()
    color2 = hsl_to_rgb(adjustLumSat(rgb_to_hsl(color1), cRange))
    color3 = hsl_to_rgb(adjustLumSat(rgb_to_hsl(color2), cRange))
    color4 = newColor(color1)
    color5 = hsl_to_rgb(adjustLumSat(rgb_to_hsl(color4), cRange))

    print(color1, color2, color3, color4, color5)
    return color1, color2, color3, color4, color5

def printColors(color1, color2, color3, color4, color5):
    # Random Color
    img1 = Image.new('RGB', (1000, 1000), color=color1)
    img2 = Image.new('RGB', (1000, 1000), color=color2)
    img3 = Image.new('RGB', (1000, 1000), color=color3)
    img4 = Image.new('RGB', (1000, 1000), color=color4)
    img5 = Image.new('RGB', (1000, 1000), color=color5)

    img1.show()
    img2.show()
    img3.show()
    img4.show()
    img5.show()

def rgb_to_hex(colors):
    hexColors = []
    hexColor = '#{:02x}{:02x}{:02x}'.format(*colors)
    hexColors.append(hexColor)
    return hexColors