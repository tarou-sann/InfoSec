def encrypt(plaintext, key, show_steps=False):
    try:
        rails = int(key)
        if rails <= 1:
            raise ValueError("Number of rails must be greater than 1")
    except ValueError:
        raise ValueError("Rail Fence cipher key must be an integer greater than 1")
    
    # Handle case where rails is greater than text length
    if rails > len(plaintext):
        rails = len(plaintext)
    
    # Create the fence pattern
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1
    
    steps = ""
    if show_steps:
        steps += "RAIL FENCE CIPHER ENCRYPTION STEPS:\n\n"
        steps += f"Using {rails} rails\n\n"
        steps += "Building the fence pattern:\n"
    
    # Build the rail fence pattern
    for char in plaintext:
        fence[rail].append(char)
        
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
            
        rail += direction
    
    # Visualization for steps
    if show_steps:
        # Create a matrix to visualize the fence
        matrix = [[' ' for _ in range(len(plaintext))] for _ in range(rails)]
        rail = 0
        direction = 1
        
        for i in range(len(plaintext)):
            matrix[rail][i] = plaintext[i]
            
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
                
            rail += direction
        
        # Print the matrix
        for row in matrix:
            steps += ''.join(row) + '\n'
        
        steps += "\nReading the rails to form ciphertext:\n"
    
    # Read off the fence to get the ciphertext
    ciphertext = ""
    for rail_chars in fence:
        rail_text = ''.join(rail_chars)
        ciphertext += rail_text
        
        if show_steps:
            steps += f"Rail: {rail_text}\n"
    
    return ciphertext, steps

def decrypt(ciphertext, key, show_steps=False):
    try:
        rails = int(key)
        if rails <= 1:
            raise ValueError("Number of rails must be greater than 1")
    except ValueError:
        raise ValueError("Rail Fence cipher key must be an integer greater than 1")
    
    # Handle case where rails is greater than text length
    if rails > len(ciphertext):
        rails = len(ciphertext)
    
    # Create empty fence
    fence = [[] for _ in range(rails)]
    
    # Calculate lengths for each rail
    lengths = [0] * rails
    rail = 0
    direction = 1
    
    for _ in range(len(ciphertext)):
        lengths[rail] += 1
        
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
            
        rail += direction
    
    steps = ""
    if show_steps:
        steps += "RAIL FENCE CIPHER DECRYPTION STEPS:\n\n"
        steps += f"Using {rails} rails\n\n"
        steps += "Calculating characters per rail:\n"
        for i, length in enumerate(lengths):
            steps += f"Rail {i}: {length} characters\n"
        steps += "\nFilling rails with ciphertext:\n"
    
    # Fill the fence with characters from ciphertext
    index = 0
    for rail in range(rails):
        fence[rail] = list(ciphertext[index:index + lengths[rail]])
        if show_steps:
            steps += f"Rail {rail}: {''.join(fence[rail])}\n"
        index += lengths[rail]
    
    if show_steps:
        steps += "\nReading zigzag pattern to recover plaintext:\n"
    
    # Read off in zigzag pattern
    plaintext = ""
    rail = 0
    direction = 1
    rail_indices = [0] * rails
    
    for _ in range(len(ciphertext)):
        plaintext += fence[rail][rail_indices[rail]]
        rail_indices[rail] += 1
        
        if rail == 0:
            direction = 1
        elif rail == rails - 1:
            direction = -1
            
        rail += direction
    
    if show_steps:
        # Create a matrix to visualize the decryption
        matrix = [[' ' for _ in range(len(ciphertext))] for _ in range(rails)]
        rail_indices = [0] * rails
        rail = 0
        direction = 1
        
        for i in range(len(ciphertext)):
            matrix[rail][i] = fence[rail][rail_indices[rail]]
            rail_indices[rail] += 1
            
            if rail == 0:
                direction = 1
            elif rail == rails - 1:
                direction = -1
                
            rail += direction
        
        # Print the matrix
        for row in matrix:
            steps += ''.join(row) + '\n'
    
    return plaintext, steps