import numpy as np
from PIL import Image


def rc4(key, data):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0
    result = bytearray()
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        result.append(byte ^ S[(S[i] + S[j]) % 256])

    return result


def encrypt_image(original_image_path, encryption_key):
    original_image = Image.open(original_image_path).convert('L')  # Convert to grayscale
    pixels = np.array(original_image)

    encrypted_pixels = []
    for row in pixels:
        encrypted_row = []
        for pixel in row:
            encrypted_pixel = rc4(encryption_key, [int(pixel)])
            encrypted_row.append(np.uint8(encrypted_pixel[0]))
        encrypted_pixels.append(encrypted_row)

    encrypted_image = Image.fromarray(np.array(encrypted_pixels, dtype=np.uint8))
    encrypted_image.save("encrypted_image.png")
    return "encrypted_image.png"


def embed_data(encrypted_image_path, data_hiding_key, additional_data):
    encrypted_image = Image.open(encrypted_image_path)
    pixels = np.array(encrypted_image)

    data_bits = [int(bit) for bit in '{:08b}'.format(int(additional_data))]
    block_size = 8  # Assuming 8 bits of data in each block

    for i in range(0, len(pixels), block_size):
        block = pixels[i:i + block_size]
        set_a = np.random.choice([0, 1], size=block.shape, p=[0.5, 0.5])

        for j in range(block.shape[0]):
            for k in range(block.shape[1]):
                if data_bits[j] == 0:
                    block[j][k] = np.bitwise_xor(block[j][k], set_a[j][k] & 0b111)  # Flip 3 LSB
                else:
                    block[j][k] = np.bitwise_xor(block[j][k], (~set_a[j][k] & 0b111))  # Flip 3 LSB

    embedded_image = Image.fromarray(np.array(pixels, dtype=np.uint8))
    embedded_image.save("embedded_image.png")
    return "embedded_image.png"


def decrypt_image(embedded_image_path, encryption_key):
    embedded_image = Image.open(embedded_image_path)
    pixels = np.array(embedded_image)

    decrypted_pixels = []
    for row in pixels:
        decrypted_row = []
        for pixel in row:
            decrypted_pixel = rc4(encryption_key, [int(pixel)])
            decrypted_row.append(np.uint8(decrypted_pixel[0]))
        decrypted_pixels.append(decrypted_row)

    decrypted_image = Image.fromarray(np.array(decrypted_pixels, dtype=np.uint8))
    decrypted_image.save("decrypted_image.png")
    return "decrypted_image.png"


# Example usage
encryption_key = b'\x08\xfa\x06\xc6\xdd\xbd\xa4\x80'
original_image_path = '/Users/dominic/Downloads/grayscale_image.png'
additional_data = '12345678'

# Encrypt the original image
encrypted_image_path = encrypt_image(original_image_path, encryption_key)

# Embed data into the encrypted image
embedded_image_path = embed_data(encrypted_image_path, encryption_key, additional_data)

# Decrypt the embedded image
decrypted_image_path = decrypt_image(embedded_image_path, encryption_key)
print(f"Decrypted image saved as: {decrypted_image_path}")