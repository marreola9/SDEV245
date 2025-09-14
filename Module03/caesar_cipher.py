
FIRST_CHAR_CODE = ord("A")
LAST_CHAR_CODE = ord("Z")
CHAR_RANGE = LAST_CHAR_CODE - FIRST_CHAR_CODE + 1


def caesar_shift(message, shift):
    

# REsult placeholder.
    result = ""

# Go through each of the letters in the message.
    for char in message.upper():
        if char .isalpha():
    
    # Convert character to the ACII code.
            char_code = ord(char)
            new_char_code = char_code + shift
        
            if new_char_code > LAST_CHAR_CODE:
                new_char_code -= CHAR_RANGE
                
            if new_char_code < FIRST_CHAR_CODE:
                new_char_code += CHAR_RANGE 
            
            new_char = chr(new_char_code)
            result += new_char
        else:
            result += char
     
    return result
    
user_message = input("Mesage to Encrypt: ")
user_shift_key = int(input("Shift Key (integer): "))


# Encrypt
encrypted = caesar_shift(user_message, user_shift_key)
print(f"Encrypted: {encrypted}")

# Decrypt (just use negative shift)
decrypted = caesar_shift(encrypted, -user_shift_key)
print(f"Decrypted: {decrypted}")

# caesar_shift(user_message, user_shift_key)