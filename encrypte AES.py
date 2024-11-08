import pandas as pd
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import hashlib

# Load the dataset
dataset = pd.read_csv('new dataset1.csv')

# Extract relevant columns from the dataset
columns_to_encrypt = dataset[['Heart Rate (BPM)', 'Blood Pressure (mmHg)', 'SpO2 (%)', 'Blood Glucose (mg/dL)']]

# Convert the data into a single string to be used as input for encryption
data_to_encrypt = columns_to_encrypt.to_string(index=False)

# Create a hash from a combination of patient ID and Date-Time as IV (ensuring 16 bytes)
unique_id = dataset['Patient ID'].iloc[0] + dataset['Date-Time'].iloc[0]
iv = hashlib.sha256(unique_id.encode('utf-8')).digest()[:16]

# Generate a 256-bit AES key (32 bytes)
key = get_random_bytes(32)

# AES encryption function
def aes_encrypt(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(data.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return ciphertext

# AES decryption function
def aes_decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_data.decode('utf-8')

# Encrypt the extracted data
encrypted_data = aes_encrypt(data_to_encrypt, key, iv)

# Output the encrypted data (for example, save it to a file or display it)
print("Encrypted data (first 100 bytes):", encrypted_data[:100])

# Decrypt the data (for verification)
decrypted_data = aes_decrypt(encrypted_data, key, iv)
print("Decrypted data:", decrypted_data)
