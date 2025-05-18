def encrypt(plaintext, key, show_steps=False):
    if not key.isalpha():
        raise ValueError("Vigenère cipher key must contain only letters")
    
    key = key.upper()
    ciphertext = ""
    steps = ""
    
    if show_steps:
        steps += "VIGENÈRE CIPHER ENCRYPTION STEPS:\n\n"
        steps += "Character by character encryption:\n"
        steps += "Plaintext | Key | Calculation | Ciphertext\n"
        steps += "-" * 50 + "\n"
    
    key_pos = 0
    for char in plaintext:
        if char.isalpha():
            # Get corresponding key character
            key_char = key[key_pos % len(key)]
            key_pos += 1
            
            # Convert to 0-25 range
            p = ord(char.upper()) - ord('A')
            k = ord(key_char.upper()) - ord('A')
            
            # Encrypt and convert back to letter
            c = (p + k) % 26
            
            # Preserve original case
            if char.isupper():
                encrypted_char = chr(c + ord('A'))
            else:
                encrypted_char = chr(c + ord('A')).lower()
            
            if show_steps:
                steps += f"{char} | {key_char} | ({p} + {k}) % 26 = {c} | {encrypted_char}\n"
            
            ciphertext += encrypted_char
        else:
            # Keep non-alphabetic characters unchanged
            ciphertext += char
            if show_steps:
                steps += f"{char} | (non-alphabetic, kept as is)\n"
    
    return ciphertext, steps

def decrypt(ciphertext, key, show_steps=False):
    if not key.isalpha():
        raise ValueError("Vigenère cipher key must contain only letters")
    
    key = key.upper()
    plaintext = ""
    steps = ""
    
    if show_steps:
        steps += "VIGENÈRE CIPHER DECRYPTION STEPS:\n\n"
        steps += "Character by character decryption:\n"
        steps += "Ciphertext | Key | Calculation | Plaintext\n"
        steps += "-" * 50 + "\n"
    
    key_pos = 0
    for char in ciphertext:
        if char.isalpha():
            # Get corresponding key character
            key_char = key[key_pos % len(key)]
            key_pos += 1
            
            # Convert to 0-25 range
            c = ord(char.upper()) - ord('A')
            k = ord(key_char.upper()) - ord('A')
            
            # Decrypt and convert back to letter
            p = (c - k) % 26
            
            # Preserve original case
            if char.isupper():
                decrypted_char = chr(p + ord('A'))
            else:
                decrypted_char = chr(p + ord('A')).lower()
            
            if show_steps:
                steps += f"{char} | {key_char} | ({c} - {k}) % 26 = {p} | {decrypted_char}\n"
            
            plaintext += decrypted_char
        else:
            # Keep non-alphabetic characters unchanged
            plaintext += char
            if show_steps:
                steps += f"{char} | (non-alphabetic, kept as is)\n"
    
    return plaintext, steps