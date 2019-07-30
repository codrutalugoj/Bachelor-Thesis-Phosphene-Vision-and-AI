import PIL
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

cur_dir = os.path.dirname(os.path.abspath(__file__))

class Phosphene(object):
    def __init__(self, resolution, minimum, maximum):
        self.f = np.zeros((resolution[0], resolution[1]))

        x = np.linspace(minimum[0], maximum[0], resolution[0])
        y = np.linspace(minimum[1], maximum[1], resolution[1])

        self.x, self.y = np.meshgrid(x, y)

    def Get(self):
        phosphene_grid = PIL.Image.fromarray((255 * self.f / self.f.max()).astype('uint8'))
        return phosphene_grid

    def Set(self, A, sx, sy, x0, y0):
        self.f += np.transpose(A * np.exp(-((self.x - x0) ** 2 / (2 * sx ** 2) + (self.y - y0) ** 2 / (2 * sy ** 2))))

def phosphene_wrapper(image_properties,phosphene_matrix):
    image_properties[0] = [int(image_properties[0][0]), int(image_properties[0][1])]
    phosphene     = Phosphene(image_properties[0], image_properties[1], image_properties[2])
    for row in phosphene_matrix:
        if row[0] != 0:
          phosphene.Set(*row)

    return phosphene.Get()

# Define image properties
# x,y = resolution, extreme values 
def image_Properties(x,y):  
  image_properties = np.zeros((3,2),dtype=int)
  image_properties[0] = (2*y,2*x)
  image_properties[1] = (-y,-x)
  image_properties[2] = (y,x)
  return image_properties

# Create phosphene parameters
# size = average size of phosphene, so mean standard deviation of gaussian
# std = variation in size of phosphenes, standard deviation of the standard deviation
# extreme_dimension = the size of the image in terms of distance to the middle in each dimension

def phosphene_Matrix(numberx, numbery, size, std, image_properties):
  #round off number of phosphenes so it's a square
  number_phosphenes=int(numberx*numbery)
  
  parameters= np.zeros((number_phosphenes,5))
  #amplitude
  parameters[:,0]=1
  #decide on positions of phosphenes
  edge=image_properties[0][1]/(2*numberx)
  ys=np.linspace(image_properties[1][0]+edge, image_properties[2][0]-edge, numbery)
  xs=np.linspace(image_properties[1][1]+edge, image_properties[2][1]-edge, numberx)
  grid=np.meshgrid(xs,ys)
  y= np.reshape(grid[0],(1,number_phosphenes))
  x= np.reshape(grid[1],(1,number_phosphenes))
  parameters[:,3]=x
  parameters[:,4]=y
  #decide on size of each phosphene
  for row in parameters:
    periphery = np.sqrt(row[3]**2+row[4]**2)/(image_properties[0][0])+0.5
    row[1]= np.random.normal(size*np.sqrt(periphery), std*periphery)
    row[2]= np.random.normal(row[1],std)
  
  return parameters

from PIL import Image


# Generating grid
image_properties=image_Properties(80,50)
phosphene_matrix=phosphene_Matrix(40,25,2.5,0.3,image_properties)
grid = phosphene_wrapper(image_properties,phosphene_matrix)
print(grid.size)


matrixtxt = "phosphene_matrix_presentation.txt"
gridtxt = "grid_presentation.txt"
imagepropertiestxt = "image_properties_presentation.txt"
np.savetxt(matrixtxt,phosphene_matrix.astype(float),fmt='%i %1.5f %1.5f %i %i')
np.savetxt(gridtxt,np.array(grid).astype(int),fmt=' '.join(['%i']*160))
np.savetxt(imagepropertiestxt,np.array(image_properties).astype(int),fmt = '%i %i')


phosphene_matrix = np.loadtxt("/home/coco/thesisExperiment/phosphene_matrix_presentation.txt")
grid = np.loadtxt("/home/coco/thesisExperiment/grid_presentation.txt",dtype = 'int')
image_properties= np.loadtxt("/home/coco/thesisExperiment/image_properties_presentation.txt",dtype='int')

imgplot = plt.imshow(grid)
plt.imsave("/home/coco/thesisExperiment/grid_presentation.png",grid,cmap='gray')


def to_phosphene(image):
        #savepath = "/home/coco/thesisExperiment/phosphenized/"
        phosphene_matrix = np.loadtxt("/home/coco/thesisExperiment/phosphene_matrix.txt")
        grid = np.loadtxt("/home/coco/thesisExperiment/grid.txt",dtype = 'int')
        image_properties= np.loadtxt("/home/coco/thesisExperiment/image_properties.txt",dtype='int')


        #im2x = im2x.crop((0,0,945,945))
        im2x = np.array(image)
        #im2x = image.resize((40,25))
        im2x = (im2x > 100).astype(np.int_)
        #print((im2x > 100).astype(np.int_))
        outcomeimage = np.zeros((40,40))
        for i in range(40):
                for j in range(40):
                        count = 0
                        temp = im2x[i*15:i*15+15,j*15:j*15+15]
                        count = np.sum(temp)
                        if count > 1:
                                outcomeimage[i,j] = 1
        #outcomeimage = image.convert('L')
        indexes = np.linspace(-78,78,num=40)
        #Draw phosphenes that are activated
        imagephosphenes = np.zeros((1600,5))
        #print(imagephosphenes.shape)
        for row in range(1600):
                x = int(np.where(indexes == phosphene_matrix[row][3])[0])
                #print(x)
                y = int(np.where(indexes == phosphene_matrix[row][4])[0])
                if outcomeimage[x,y] != 0:
                        imagephosphenes[row,:]=phosphene_matrix[row,:]
        phosphene_image = phosphene_wrapper(image_properties,imagephosphenes)
        #print(type(phosphene_image))
        phosphene_image = phosphene_image.crop((0,0,phosphene_image.size[0], phosphene_image.size[1]-60))
        #print(image.size, phosphene_image.size)
        #phosphene_image = phosphene_image.crop((0,0,phosphene_image.size[0], image.size[1]))
        #print(phosphene_image.size)
        #phosphene_image.save(savepath + "phosphene.png")
        #np.savetxt(savepath + 'binary.txt',np.array(outcomeimage).astype(int),fmt=' '.join(['%i']*40))
        return phosphene_image


