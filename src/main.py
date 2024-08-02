from PIL import Image
from cryptography.fernet import Fernet
import numpy as np
import os

# local working directory
working_dir = os.path.dirname(os.path.abspath(__file__))


# generate encryption key
def generate_key():
    return Fernet.generate_key()


# encrypt data
def encrypt_data(key, data):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data


# decrypt data
def decrypt_data(key, encrypted_data):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)
    return decrypted_data.decode()


# embed data in image with least significant bits
def embed_data(data, account, output_image_name):
    image = Image.open(f"{working_dir}/raw image/{account}.png")

    if image.mode == 'P':
        image = image.convert('RGB')

    pixels = np.array(image)

    # Check the shape and dtype of the image array
    print(f"Image shape: {pixels.shape}, dtype: {pixels.dtype}, mode: {image.mode}")

    if pixels.dtype != np.uint8:
        raise TypeError(f"Expected image of type uint8, but got {pixels.dtype}")

    flat_pixels = pixels.flatten()

    # Debug: Initial pixel value statistics
    print(f"Initial pixel min: {flat_pixels.min()}, max: {flat_pixels.max()}")

    binary_data = ''.join(format(byte, '08b') for byte in data)
    print(f"Embedding data of length: {len(binary_data)}")

    for i in range(len(binary_data)):
        pixel_value = int(flat_pixels[i])  # Ensure pixel_value is an int
        try:
            binary_value = int(binary_data[i])
            if binary_value not in (0, 1):
                raise ValueError(f"Invalid binary value: {binary_value}")
            new_pixel_value = (pixel_value & ~1) | binary_value

            # Debug: Print pixel value changes
            if i < 10:  # Limit the number of debug prints
                print(
                    f"Index {i}: pixel_value={pixel_value}, binary_data[i]={binary_data[i]}, new_pixel_value={new_pixel_value}")

            if new_pixel_value < 0 or new_pixel_value > 255:
                raise ValueError(f"Invalid new pixel value: {new_pixel_value}")
            flat_pixels[i] = new_pixel_value
        except Exception as e:
            print(f"Error at index {i}: pixel_value={pixel_value}, binary_data[i]={binary_data[i]}")
            raise e

    stego_pixels = flat_pixels.reshape(pixels.shape)
    stego_image = Image.fromarray(stego_pixels.astype("uint8"), image.mode)

    # Ensure the directory exists
    output_dir = os.path.join(working_dir, "encrypted image")
    os.makedirs(output_dir, exist_ok=True)

    stego_image.save(os.path.join(output_dir, f"{output_image_name}.png"))


# extract data from image
def extract_data(output_image_name, data_length):
    image = Image.open(f"{working_dir}/encrypted image/{output_image_name}.png")
    pixels = np.array(image).flatten()
    binary_data = ''.join(str(pixels[i] & 1) for i in range(data_length * 8))
    byte_data = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]
    data = bytes([int(byte, 2) for byte in byte_data])
    return data


# example usage
key = generate_key()
passwords = input("Enter password:\n")
encrypted_password = encrypt_data(key, passwords)

# embed password into image
account = input("Enter the account application:\n")
output_image_name = f"{account}-epass"
embed_data(encrypted_password, account, output_image_name)

# extract and decrypt password
extracted_data = extract_data(output_image_name, len(encrypted_password))
decrypted_password = decrypt_data(key, extracted_data)

# print
print("Decrypted passwords: ", decrypted_password)
