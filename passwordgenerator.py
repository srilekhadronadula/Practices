import random
import string

def generate_password(length):
    if length < 4:
        print("❌ Password length should be at least 4 characters.")
        return

    # Create a pool of characters
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    punctuation = string.punctuation
    
    # Ensure password complexity by including at least one of each character type
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(punctuation)
    ]
    
    # Fill the rest of the password with random choices from the full pool
    remaining_length = length - 4
    characters = lowercase + uppercase + digits + punctuation
    password += [random.choice(characters) for _ in range(remaining_length)]
    
    # Shuffle the password to ensure randomness
    random.shuffle(password)
    
    # Join the list into a string
    password = ''.join(password)

    print(f"✅ Generated Password: {password}")

# Get user input
try:
    length = int(input("Enter the desired password length: "))
    generate_password(length)
except ValueError:
    print("❌ Invalid input! Please enter a numeric value for the password length.")
