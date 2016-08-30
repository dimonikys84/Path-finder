#logo = io.imread('http://deti-online.com/img/raskraska-spanchbob.jpg', as_grey=True)
import random
import skimage as sk
from skimage import io
from skimage.morphology import skeletonize
from skimage.morphology import medial_axis
import numpy as np
import matplotlib.pyplot as plt
from path_finder import find_paths

test_arr = [[False,False,False,False,False],
           [False,False,True ,False,False],
           [False,False,True ,False,False],
           [True ,True ,True ,True ,True ],
           [True ,False,False,False,False],
           [False,False,False,False,False]]

image = io.imread('http://etc.usf.edu/clipart/49500/49593/49593_napol_emp_md.gif', as_grey=True)
prep_image = ~sk.img_as_bool(image)
prep_image = sk.img_as_float(prep_image)


# perform skeletonization
skel, distance = medial_axis(prep_image, return_distance=True)
print(distance[100])


skeleton = skeletonize(prep_image)
print(len(skeleton),len(skeleton[0]))
lines = find_paths(skeleton)


drawed_img = np.zeros((len(skeleton),len(skeleton[0])), dtype=np.uint8)
for line in lines:
    color = random.randrange(200,2000)
    for point in line:
        drawed_img[point[1],point[0]] = color


# display results
fig, (ax0, ax2,ax3) = plt.subplots(nrows=1, ncols=3, figsize=(8, 4.5),
                               sharex=True, sharey=True,
                               subplot_kw={'adjustable': 'box-forced'})

ax0.imshow(image, cmap=plt.cm.gray)
ax0.axis('off')
ax0.set_title('Original', fontsize=20)

ax2.imshow(skeleton, cmap=plt.cm.gray)
ax2.axis('off')
ax2.set_title('skeleton', fontsize=20)

ax3.imshow(drawed_img, cmap=plt.cm.spectral)
ax3.axis('off')
ax3.set_title('Routes (' + str(len(lines)) +')', fontsize=20)

fig.tight_layout()


plt.show()