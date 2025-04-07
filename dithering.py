from PIL import Image
import numpy as np
from random import randint
from numba import njit

def save_image_from_array(image_array, filename, format='PNG'):
    """Saves a NumPy array as an image file.

    Args:
    image_array: The NumPy array representing the image.
    filename: The desired filename for the saved image (e.g., 'output.png').
    format: The desired image format (e.g., 'PNG', 'JPEG', 'TIFF'). 
    """
    try:
        img = Image.fromarray(image_array).convert('1')
        img.save(filename, format)
        print(f"Image saved successfully as {filename}")
    except Exception as e:
        print(f"Error saving image: {e}")

def load_gray_image_as_array(image_path):
    """Loads an image from the specified path and returns it as a NumPy array.

    Args:
    image_path: The path to the image file.

    Returns:
    A NumPy array representing the image.
    """
    img = Image.open(image_path)
    gray = img.convert('L')  # Convert to grayscale
    return np.array(gray)

def display_image_from_array(image_array):
    """Displays an image from a NumPy array.

    Args:
    image_array: The NumPy array representing the image.
    """
    img = Image.fromarray(image_array)
    img.show()


@njit
def iterative_dithering(image_array, hits, size_multiplier=1):
    N,M = image_array.shape

    # dithered = np.zeros_like(image_array)
    dithered = np.zeros((size_multiplier*N, size_multiplier*M), dtype='uint8')

    for times in range(hits):
        i = randint(0,size_multiplier*N-1)
        j = randint(0,size_multiplier*M-1)
        if image_array[int(i/size_multiplier)][int(j/size_multiplier)] > randint(0,255):
            dithered[i][j] = 255
    return dithered

@njit(parallel=True)
def sequencial_dithering(image_array, size_multiplier=1, samples=1, stretch_factor=1):
    N,M = image_array.shape

    #stretch
    image_array = ((image_array-127)*stretch_factor) + 127

    dithered = np.zeros((size_multiplier*N, size_multiplier*M), dtype='uint8')

    for i in range(size_multiplier*N-1):
        for j in range(size_multiplier*M-1):
            value = image_array[int(i/size_multiplier)][int(j/size_multiplier)]

            white=0
            black=0
            for s in range(samples):
                if value > randint(0,255):
                    white+=1
                else:
                    black+=1
            if white>=black:
                dithered[i][j] = 255
            else:
                dithered[i][j] = 0
    return dithered


#Cold start with tiny test image to compile
sequencial_dithering(np.array([[1,2,3],[1,2,3]], dtype='uint8'))


if __name__ == "__main__":
    # Example usage:
    image_array = load_gray_image_as_array('fasaia.png')
    # display_image_from_array(image_array)

    SIZE_MULTIPLIER = 1

    # bw = iterative_dithering(image_array, round(image_array.size*SIZE_MULTIPLIER**2), SIZE_MULTIPLIER)
    bw = sequencial_dithering(image_array, size_multiplier=SIZE_MULTIPLIER, samples=2, stretch_factor=2)

    display_image_from_array(bw)
    save_image_from_array(bw, 'dithered.png', 'PNG')