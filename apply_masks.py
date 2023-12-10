import numpy as np
import tensorflow as tf
import os

def main():
    try:
        os.mkdir("__pycache__/A/")
        os.mkdir("__pycache__/B/")
    except:
        pass

    # List all files in the directory
    files = os.listdir("__pycache__/data")

    # Iterate through each file
    for file_name in files:
        if file_name.endswith(".jpg"):
            continue
        
        file_path = os.path.join("__pycache__", "data", file_name)
        
        # Check if it's a file (not a directory)
        unmasked_path = os.path.join("__pycache__", "A", file_name)
        masked_path = os.path.join("__pycache__", "B", file_name)
        if os.path.isfile(file_path) and not os.path.isfile(masked_path):
            with open(file_path, 'r+b') as maskfile, open(file_path.replace("png", "jpg"), 'r+b') as imagefile, open(unmasked_path, 'wb') as unmasked, open(masked_path, 'wb') as masked:
                mask = maskfile.read()
                image = imagefile.read()
                unmasked.write(image)
                image = apply_mask(image, mask)
                masked.write(image)

def apply_mask(image: bytes, mask: bytes):
    # Converts image into a W×H array of pixels (which are 3-tuples of RGB)
    img = tf.image.decode_image(image, channels=3)
    img = tf.cast(img, tf.float32)
    img = normalize(img)
    
    msk = tf.image.decode_image(mask, channels=3)
    msk = tf.cast(msk, tf.float32)
    msk = msk.numpy()
    
    # Replace image pixel-by-pixel
    # Ideally this would be one image, but API requires it be two.
    white_pixel_indices = []
    height = len(img)
    width = len(img[0])
    
    for j in range(0, height):
        for i in range(0, width):
            # If any color in mask pixel wasn't transparent or black, then blank that part of the real image
            # Basically just merging the mask onto the image.
            if msk[j][i][0] != 0:
                white_pixel_indices.append([j, i])
    
    # Par docs, this is equivalent to:
    # for idx in white_pixel_indices:
    #     img[idx[0]][idx[1]] = [1,1,1]
    # But more efficient on the CPU.
    indices = tf.constant(white_pixel_indices)
    updates = tf.ones([len(white_pixel_indices), 3])

    img = tf.tensor_scatter_nd_update(tensor=img, indices=indices, updates=updates)
    
    return model_tensor_to_png(img)

# Converts an array of pixels from values of 0...255 to -1...1
# Used for pix2pix model
def normalize(tensor_image):
    return (tensor_image / 127.5) - 1

# Undoes normalization
def denormalize(tensor_image):
    return tf.cast((tensor_image + 1) * 127.5, dtype=tf.uint8)

# Converts a [[[r,g,b]]] Tensor where rgb are -1...1 to a PNG image
def model_tensor_to_png(tensor_image):
    return tf.image.encode_png(denormalize(tensor_image)).numpy()

main()
