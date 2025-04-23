import numpy as np
import skimage as sk
from matplotlib import pyplot as plt
import heapq

image1 = sk.io.imread('3.Aufgabe/lena.jpg')
image2 = sk.io.imread('3.Aufgabe/pepper.jpg')
image3 = sk.io.imread('3.Aufgabe/tree.png')


def mexican_hat_5x5():
    return np.array([
        [ 0,  0, -1,  0,  0],
        [ 0, -1, -2, -1,  0],
        [-1, -2, 16, -2, -1],
        [ 0, -1, -2, -1,  0],
        [ 0,  0, -1,  0,  0]
    ])


def convert_to_gs(image):
    res = np.dot(image[..., :3] , [0.2989, 0.5870, 0.1140])
    res = res.astype(np.uint8)
    return np.stack((res,)*3, axis =-1)

# TODO: noch Falten, aka andersrum drueber laufen lassen
def image_filter(in_image, filter, off, edge):

    height, width = in_image.shape
    filter_height,filter_width = filter.shape
    surplus_y = filter_height-1
    surplus_x = filter_width-1
    count = 0
    for i in filter:
        for j in i:
            count += j

    if edge == 'min':
        padded = np.zeros((height+surplus_y, width+surplus_x))
    elif edge == 'max':
        padded = np.full((height+surplus_y, width+surplus_x),fill_value=255)
    elif edge == 'continue':
        padded = np.zeros((height+surplus_y, width+surplus_x))

    if not edge == 'none':
        for y in range(height):
            for x in range(width):
                padded[y + int(surplus_y/2), x + int(surplus_x/2)] = in_image[y, x]

    if edge == 'continue':
        for x in range(width):
            for i in range(int(surplus_x/2)):
                padded[i, x+int(surplus_x/2)] = in_image[0, x]
                padded[height + int(surplus_x/2) + i, x + int(surplus_x/2)] = in_image[height-1, x]

        for y in range(height):
            for i in range(int(surplus_y/2)):
                padded[y+int(surplus_y/2), i] = in_image[y, 0]
                padded[y+int(surplus_y/2), width + int(surplus_x/2) + i] = in_image[y, width-1]

        for i in range(int(surplus_y/2)):
            for j in range(int(surplus_x/2)):
                padded[i, j] = in_image[0,0]
                padded[i, width + int(surplus_x/2) + j] = in_image[0, width-1]
                padded[height + int(surplus_y/2) +i, j] = in_image[height-1, 0]
                padded[height + int(surplus_y/2) + i, width + int(surplus_x/2) + j] = in_image[height-1, width-1]

    if not edge == 'none':
        in_image = padded
        height, width = in_image.shape


    out_image = np.zeros_like(in_image)


    for y in range(height-(2*off)):
        for x in range(width-(2*off)):
            sum = 0
            for u in range(filter_height):
                for v in range(filter_width):
                    adjusted_u = -(filter_height - 1)*0.5 + u
                    adjusted_v = -(filter_width - 1)*0.5 + v
                    yi = y + off
                    xi = x + off
                    sum += in_image[yi - int(adjusted_u), xi - int(adjusted_v)] * filter[u,v]
            if count != 0:
                out_image[y + off, x + off] = sum / float(count)
            else:
                out_image[y + off, x + off] = sum


    if off > 0:
        return out_image[off:-off, off:-off]
    else:
        return out_image


def heapsort(values):
    h = []
    for value in values:
        heapq.heappush(h, value)
    return [heapq.heappop(h) for i in range(len(h))]  

def median_filter(in_image, filtersize, offset):
    out_image = np.zeros_like(in_image)
    height, width = in_image.shape

    for y in range(height - (2*offset)):
        for x in range(width - (2*offset)):
            filterwindow = []
            for i in range(filtersize):
                for j in range(filtersize):
                    adjusted_i = -(filtersize-1)/2+i
                    adjusted_j = -(filtersize-1)/2+j
                    filterwindow.append(in_image[y+int(adjusted_i)+offset, x+int(adjusted_j)+offset])

            filterwindow = heapsort(filterwindow)
            out_image[y + offset , x + offset] = filterwindow[len(filterwindow)//2]

    return out_image

gs_im1 = convert_to_gs(image1)
gs = gs_im1[:,:,2]

fm = np.ones((5,5))

fm[1,1] = 3
mh = mexican_hat_5x5()
test = image_filter(gs, fm, 2, 'min')

test2 = median_filter(image2, 3, 1)
test3 = median_filter(image3, 5, 2)
#sk.io.imshow(gs)
#sk.io.show()

#sk.io.imshow(test, cmap='gray')
#sk.io.show()

sk.io.imshow(test2)
sk.io.show()

sk.io.imshow(test3)
sk.io.show()
