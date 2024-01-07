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
    def get_key(self):
        return self.state
# Function to encrypt an image using RC4
def encrypt_image(img_path, key):
    # Load the image and convert it to grayscale
    # img=Image.open(img_path)
    img_data = np.array(img_path)
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


root_path=os.path.abspath(os.path.join(os.getcwd(), ".."))
pic_path=os.path.join(root_path,"gray_pic")
enc_path=os.path.join(root_path,"enc_pic")
files=os.listdir(pic_path)
key = b'115'  # Update this key

for file in files:
    original_image_path=os.path.join(pic_path,file)
    # print(file_name)
    img=Image.open(original_image_path)
    enc_img=encrypt_image(img,key)
    enc_img.save(os.path.join(enc_path,file))


# encrypted_image = encrypt_image(original_image_path, key)
# encrypted_image.show(title="Encrypted Image")