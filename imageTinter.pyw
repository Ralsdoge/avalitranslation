from PIL import Image, ImageColor
Images = [] #Tinted Images
CreatedLookup = [] #Lookup table
def hex_to_rgba(value): #Get a RGBA value from a hex code
    return ImageColor.getcolor(value, "RGBA") 
def tint_image(image, color): #tints a given alpha matte to a different color
    baseImage = image.convert('RGBA') #convert image type to rgba
    r, g, b, alpha = baseImage.split() #split into channels
    coloredImage = Image.new('RGBA', baseImage.size, color) # Make an image that is the color we want with correct size
    coloredImage.putalpha(alpha) #Replace the alpha of the image we made with the baseImage's alpha channel. 
    return coloredImage #return img
def preformTint(path, color): #image = path to image as string, color = #fffff (hex code)
    image = Image.open(path)
    name = image.filename
    expt = name + ":" + color
    for i in range(len(CreatedLookup)): #search if it's already created
        if CreatedLookup[i] == expt:
            print('Tinted Image already exists.')
            return Images[i] #give image
    rgbtint = hex_to_rgba(color) #grab rgb value
    #print("rgbtint:",rgbtint)
    tinted = tint_image(image,rgbtint) #Tinting process
    print('New image tinted as:',expt)
    Images.append(tinted) #Save Images here
    CreatedLookup.append(expt) #Save name and tint color here
    return tinted #give image
# Example usage:
'''
tinted_image = preformTint("Images/sidebar/Settings.png", '#ff0000')
print(Images)
Images[0].show()'''
#Images[0].save("Images/sidebar/SettingsTintTest.png",format="PNG")