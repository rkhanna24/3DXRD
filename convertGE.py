import readGE
import writeImage
import writeGE

folder = '/media/Argonne Backup/FFfine/'
bgName = folder + 'Ti7Test_00017.ge2'
fileHead = 'Ti7_PreHRM_PreLoad__005'
output = 'ring'

#folder = '/home/tempuser/Rohan/'
#bgName = ''
#fileHead = 'ring'
#output = 'ringb'

minID = 53 # ID of first binary
maxID = 70 # ID of last binary

#minID = 0
#maxID = 0

pBar = True

im = readGE.readGE( directory = folder, 
                       filePrefix = fileHead, 
                       bgFile = bgName,
                       lowerID = minID, 
                       upperID = maxID, 
                       bar = pBar)

writeImage.toImage( image_data = im, 
                       outputim = output,
                       bar = pBar)

writeGE.writeGE( image_data = im,
				 directory = folder,
				 filePrefix = fileHead,
				 outputbin = output,
				 lowerID = minID)