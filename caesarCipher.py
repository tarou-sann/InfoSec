def encrypt(plaintext, key, show_steps=False):
    try:
        shift = int(key)
    except ValueError:
        raise ValueError("Caesar cipher key must be an integer")
    
    ciphertext = ""
    steps = ""
    
    if show_steps:
        steps += "CAESAR CIPHER ENCRYPTION STEPS:\n"
        steps += f"Using shift value: {shift}\n\n"
        steps += "Character | ASCII | Shifted | Mod 26 | New Char\n"
        steps += "-" * 50 + "\n"
    
    for char in plaintext:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            # Convert to 0-25 range, shift, and mod 26 to wrap around
            shifted = (ord(char) - ascii_offset + shift) % 26
            # Convert back to ASCII and then to character
            encrypted_char = chr(shifted + ascii_offset)
            
            if show_steps:
                steps += f"{char} | {ord(char)} | {ord(char) - ascii_offset} + {shift} = {ord(char) - ascii_offset + shift} | {shifted} | {encrypted_char}\n"
            
            ciphertext += encrypted_char
        else:
            # Keep non-alphabetic characters unchanged
            ciphertext += char
            if show_steps:
                steps += f"{char} | (non-alphabetic, kept as is)\n"
    
    return ciphertext, steps

def decrypt(ciphertext, key, show_steps=False):
    try:
        shift = int(key)
    except ValueError:
        raise ValueError("Caesar cipher key must be an integer")
    
    # To decrypt, we use the negative of the shift value
    return encrypt(ciphertext, -shift, show_steps)