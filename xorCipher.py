def encrypt(plaintext, key, show_steps=False):
    # Convert key to bytes if it's a string
    if isinstance(key, str):
        key = key.encode()
    else:
        # Try to convert to string and then bytes
        key = str(key).encode()
    
    # Convert plaintext to bytes if it's a string
    if isinstance(plaintext, str):
        plaintext = plaintext.encode()
    
    ciphertext_bytes = bytearray()
    steps = ""
    
    if show_steps:
        steps += "XOR CIPHER ENCRYPTION STEPS:\n\n"
        steps += "Byte by byte encryption:\n"
        steps += "Plaintext | Key | XOR Result | ASCII\n"
        steps += "-" * 50 + "\n"
    
    for i, byte in enumerate(plaintext):
        key_byte = key[i % len(key)]
        encrypted_byte = byte ^ key_byte
        ciphertext_bytes.append(encrypted_byte)
        
        if show_steps:
            # Show the operations in binary and decimal
            steps += f"{chr(byte) if 32 <= byte <= 126 else '?'} ({byte}) | "
            steps += f"{chr(key_byte) if 32 <= key_byte <= 126 else '?'} ({key_byte}) | "
            steps += f"{byte} XOR {key_byte} = {encrypted_byte} | "
            steps += f"{chr(encrypted_byte) if 32 <= encrypted_byte <= 126 else '?'}\n"
    
    # Return as hex string for easier display/storage
    ciphertext = ''.join(f'{b:02x}' for b in ciphertext_bytes)
    
    if show_steps:
        steps += f"\nFinal ciphertext (hex): {ciphertext}\n"
    
    return ciphertext, steps

def decrypt(ciphertext, key, show_steps=False):
    # Convert key to bytes if it's a string
    if isinstance(key, str):
        key = key.encode()
    else:
        # Try to convert to string and then bytes
        key = str(key).encode()
    
    # Convert hex ciphertext to bytes
    try:
        ciphertext_bytes = bytes.fromhex(ciphertext)
    except ValueError:
        # If not hex, try treating as regular text
        ciphertext_bytes = ciphertext.encode() if isinstance(ciphertext, str) else ciphertext
    
    plaintext_bytes = bytearray()
    steps = ""
    
    if show_steps:
        steps += "XOR CIPHER DECRYPTION STEPS:\n\n"
        steps += "Byte by byte decryption:\n"
        steps += "Ciphertext | Key | XOR Result | ASCII\n"
        steps += "-" * 50 + "\n"
    
    for i, byte in enumerate(ciphertext_bytes):
        key_byte = key[i % len(key)]
        decrypted_byte = byte ^ key_byte
        plaintext_bytes.append(decrypted_byte)
        
        if show_steps:
            # Show the operations in binary and decimal
            steps += f"{byte} | "
            steps += f"{chr(key_byte) if 32 <= key_byte <= 126 else '?'} ({key_byte}) | "
            steps += f"{byte} XOR {key_byte} = {decrypted_byte} | "
            steps += f"{chr(decrypted_byte) if 32 <= decrypted_byte <= 126 else '?'}\n"
    
    # Convert back to string
    try:
        plaintext = plaintext_bytes.decode('utf-8')
    except UnicodeDecodeError:
        # If can't decode as UTF-8, return as hex
        plaintext = ''.join(f'{b:02x}' for b in plaintext_bytes)
        if show_steps:
            steps += "\nWarning: Could not decode result as UTF-8, returning hex representation.\n"
    
    return plaintext, steps