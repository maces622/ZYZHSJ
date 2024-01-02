from logging import root
import numpy as np
from PIL import Image
import os

from PIL import Image
import numpy as np

# RC4 encryption algorithm
class RC4:
    def __init__(self, key=None):
        self.state = list(range(256))  # Initialize state array
        self.x = self.y = 0  # Set indices to 0

        # Key-scheduling algorithm (KSA)
        if key:
            self.init_ksa(key)

    def init_ksa(self, key):
        j = 0
        for i in range(256):
            j = (j + self.state[i] + key[i % len(key)]) % 256
            self.state[i], self.state[j] = self.state[j], self.state[i]

    def encrypt(self, data):
        return bytes([b ^ self.prga() for b in data])

    def prga(self):  # Pseudo-random generation algorithm (PRGA)
        self.x = (self.x + 1) % 256
        self.y = (self.y + self.state[self.x]) % 256
        self.state[self.x], self.state[self.y] = self.state[self.y], self.state[self.x]
        return self.state[(self.state[self.x] + self.state[self.y]) % 256]

# Function to encrypt an image using RC4
def encrypt_image(img_path, key):
    # Load the image and convert it to grayscale
    img=Image.open(img_path)
    img_data = np.array(img)
    # Flatten the image array and convert to bytes
    flat_img_data = img_data.flatten()
    byte_data = bytes(flat_img_data)

    # Initialize RC4 with the provided key
    rc4 = RC4(key)

    # Encrypt the data
    encrypted_data = rc4.encrypt(byte_data)

    # Convert the encrypted data back to the original image dimensions
    encrypted_img_data = np.frombuffer(encrypted_data, dtype=np.uint8).reshape(img_data.shape)

    # Create an encrypted image from the data
    encrypted_img = Image.fromarray(encrypted_img_data)
    return encrypted_img

# Path to the input image (replace with the path to your image)

root_path=os.path.abspath(os.path.join(os.getcwd(), ".."))
pic_path=os.path.join(root_path,"picture")
original_image_path = pic_path+"\\7_dec.png"
key = b'secret_key'  # Update this key

# Encrypt the image
# input_img = Image.open(original_image_path).convert('L')
# input_img.save("7_ori.png")
encrypted_image = encrypt_image(original_image_path, key)

# Display the original and encrypted images

# original_image.show(title="Original Image")
encrypted_image.show(title="Encrypted Image")
encrypted_image.save("7_enc.png")