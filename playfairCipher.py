def prepare_key(key):
    # Convert key to uppercase and remove non-alphabetic characters
    key = ''.join(filter(str.isalpha, key.upper()))
    
    # Replace J with I
    key = key.replace('J', 'I')
    
    # Create the key matrix (5x5 grid)
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # No J
    # Add key characters first (without duplicates)
    matrix_chars = ""
    for char in key:
        if char not in matrix_chars:
            matrix_chars += char
    
    # Add remaining alphabet characters
    for char in alphabet:
        if char not in matrix_chars:
            matrix_chars += char
    
    # Create 5x5 matrix
    matrix = []
    for i in range(0, 25, 5):
        matrix.append(list(matrix_chars[i:i+5]))
    
    return matrix

def find_position(matrix, char):
    # Replace J with I for lookups
    if char == 'J':
        char = 'I'
    
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    
    return -1, -1  # Should never reach here with valid input

def prepare_text(text):
    # Convert to uppercase and remove non-alphabetic characters
    text = ''.join(filter(str.isalpha, text.upper()))
    
    # Replace J with I
    text = text.replace('J', 'I')
    
    # Split into digraphs and handle repeated letters
    digraphs = []
    i = 0
    while i < len(text):
        if i + 1 < len(text):
            if text[i] == text[i + 1]:
                digraphs.append(text[i] + 'X')
                i += 1
            else:
                digraphs.append(text[i] + text[i + 1])
                i += 2
        else:
            # Handle odd-length text by adding X
            digraphs.append(text[i] + 'X')
            i += 1
    
    return digraphs

def encrypt(plaintext, key, show_steps=False):
    matrix = prepare_key(key)
    digraphs = prepare_text(plaintext)
    ciphertext = ""
    steps = ""
    
    if show_steps:
        steps += "PLAYFAIR CIPHER ENCRYPTION STEPS:\n\n"
        steps += "Key Matrix:\n"
        for row in matrix:
            steps += f"| {' | '.join(row)} |\n"
        steps += "\nSplit plaintext into digraphs:\n"
        steps += " ".join(digraphs) + "\n\n"
        steps += "Encryption of each digraph:\n"
    
    for digraph in digraphs:
        row1, col1 = find_position(matrix, digraph[0])
        row2, col2 = find_position(matrix, digraph[1])
        
        # Same row
        if row1 == row2:
            new_char1 = matrix[row1][(col1 + 1) % 5]
            new_char2 = matrix[row2][(col2 + 1) % 5]
            rule = "Same row - shift right"
        # Same column
        elif col1 == col2:
            new_char1 = matrix[(row1 + 1) % 5][col1]
            new_char2 = matrix[(row2 + 1) % 5][col2]
            rule = "Same column - shift down"
        # Rectangle
        else:
            new_char1 = matrix[row1][col2]
            new_char2 = matrix[row2][col1]
            rule = "Rectangle - swap columns"
        
        if show_steps:
            steps += f"Digraph: {digraph}\n"
            steps += f"  {digraph[0]} at position ({row1},{col1})\n"
            steps += f"  {digraph[1]} at position ({row2},{col2})\n"
            steps += f"  Rule: {rule}\n"
            steps += f"  Encrypted: {new_char1}{new_char2}\n\n"
        
        ciphertext += new_char1 + new_char2
    
    return ciphertext, steps

def decrypt(ciphertext, key, show_steps=False):
    matrix = prepare_key(key)
    # Split ciphertext into digraphs (no need to handle repeated letters for decryption)
    digraphs = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]
    plaintext = ""
    steps = ""
    
    if show_steps:
        steps += "PLAYFAIR CIPHER DECRYPTION STEPS:\n\n"
        steps += "Key Matrix:\n"
        for row in matrix:
            steps += f"| {' | '.join(row)} |\n"
        steps += "\nSplit ciphertext into digraphs:\n"
        steps += " ".join(digraphs) + "\n\n"
        steps += "Decryption of each digraph:\n"
    
    for digraph in digraphs:
        row1, col1 = find_position(matrix, digraph[0])
        row2, col2 = find_position(matrix, digraph[1])
        
        # Same row
        if row1 == row2:
            new_char1 = matrix[row1][(col1 - 1) % 5]
            new_char2 = matrix[row2][(col2 - 1) % 5]
            rule = "Same row - shift left"
        # Same column
        elif col1 == col2:
            new_char1 = matrix[(row1 - 1) % 5][col1]
            new_char2 = matrix[(row2 - 1) % 5][col2]
            rule = "Same column - shift up"
        # Rectangle
        else:
            new_char1 = matrix[row1][col2]
            new_char2 = matrix[row2][col1]
            rule = "Rectangle - swap columns"
        
        if show_steps:
            steps += f"Digraph: {digraph}\n"
            steps += f"  {digraph[0]} at position ({row1},{col1})\n"
            steps += f"  {digraph[1]} at position ({row2},{col2})\n"
            steps += f"  Rule: {rule}\n"
            steps += f"  Decrypted: {new_char1}{new_char2}\n\n"
        
        plaintext += new_char1 + new_char2
    
    # Create a cleaned version without X's that were added during encryption
    cleaned_plaintext = remove_padding_x(plaintext)
    
    # Return both versions
    if show_steps:
        steps += f"\nDecrypted text: {plaintext}\n"
        steps += f"Decrypted text (without the X's): {cleaned_plaintext}\n"
    
    return plaintext, steps, cleaned_plaintext

def remove_padding_x(text):
    """Remove X's that were likely added as padding during encryption."""
    # Remove trailing X if present (for odd-length input)
    if len(text) > 0 and text[-1] == 'X':
        text = text[:-1]
    
    # Remove X's between repeated characters
    cleaned = ""
    i = 0
    while i < len(text):
        cleaned += text[i]
        
        # Check if we have X between identical letters
        if (i + 2 < len(text) and 
            text[i+1] == 'X' and 
            text[i] == text[i+2]):
            i += 2
        else:
            i += 1
            
    return cleaned