from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Efficient function to generate RSA key pair for one user
generate_rsa_key_pair = lambda: (
    rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    ),
    rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    ).public_key()
)

# Efficient generation of key pairs for 100 users
patient_keys = {f'patient_{i}': generate_rsa_key_pair() for i in range(1, 101)}

# Efficient function to retrieve keys by user ID
get_patient_keys = lambda patient_id: patient_keys.get(patient_id, (None, None))

# Optional: If you want to serialize and save keys to files
def save_key_to_file(key, filename, is_private=False):
    pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ) if is_private else key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(filename, 'wb') as f:
        f.write(pem)
#print all dict        
#print(patient_keys)

# Example usage: Get keys for a specific user (public/private)
patient_id = 'patient_5' 
private_key, public_key = get_patient_keys(patient_id)

if private_key and public_key:
    # Private Key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')
    print(f"Private Key for {patient_id}:\n{private_pem}")
    
    # Public Key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
    print(f"Public Key for {patient_id}:\n{public_pem}")


# print all patients and thair keys
#for patient_id, (private_key, public_key) in patient_keys.items():
   # print(f"patient ID: {patient_id}")
   # print(f"  Private Key: {private_key.__class__.__name__}")
   # print(f"  Public Key: {public_key.__class__.__name__}")

