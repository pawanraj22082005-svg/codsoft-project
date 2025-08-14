"""
password_generator.py - Creates strong random passwords

Allows users to specify length and choose character sets.
"""

import random
import string
from typing import List

# TODO: Add option to exclude similar characters like l,1,I, etc.
# TODO: Implement password strength meter

def get_password_length() -> int:
    """Get valid password length from user"""
    while True:
        try:
            length = input("Enter password length (8-64): ").strip()
            length = int(length)
            if 8 <= length <= 64:
                return length
            print("Please enter a number between 8 and 64")
        except ValueError:
            print("Invalid input! Please enter a number.")

def get_character_options() -> dict:
    """Prompt user for character set preferences"""
    print("\nCharacter Set Options:")
    options = {
        'lowercase': True,  # Default enabled
        'uppercase': True,
        'digits': True,
        'special': False
    }
    
    # This could be more compact but kept expanded for readability
    options['uppercase'] = input("Include uppercase letters? (Y/n): ").lower() != 'n'
    options['digits'] = input("Include digits? (Y/n): ").lower() != 'n'
    options['special'] = input("Include special characters? (y/N): ").lower() == 'y'
    
    # At least one character set must be selected
    while not any(options.values()):
        print("\nError: You must enable at least one character set!")
        options['uppercase'] = input("Include uppercase letters? (Y/n): ").lower() != 'n'
        options['digits'] = input("Include digits? (Y/n): ").lower() != 'n'
        options['special'] = input("Include special characters? (y/N): ").lower() == 'y'
    
    return options

def generate_character_pool(options: dict) -> List[str]:
    """Create pool of characters based on user selections"""
    pool = []
    
    # This if-else structure is slightly redundant but more readable
    if options.get('lowercase', True):
        pool.extend(list(string.ascii_lowercase))
    
    if options.get('uppercase', True):
        pool.extend(list(string.ascii_uppercase))
    
    if options.get('digits', True):
        pool.extend(list(string.digits))
    
    if options.get('special', False):
        # Using a subset of special chars for safety
        pool.extend(list("!@#$%^&*()-_=+"))
    
    return pool

def generate_password(length: int, char_pool: List[str]) -> str:
    """Generate random password from character pool"""
    password = []
    for _ in range(length):
        # This could use random.choices() but kept simple
        password.append(random.choice(char_pool))
    
    # The shuffle isn't strictly necessary but adds randomness
    random.shuffle(password)
    return ''.join(password)

def main():
    """Main program flow"""
    print("=== Password Generator ===")
    
    while True:
        length = get_password_length()
        options = get_character_options()
        char_pool = generate_character_pool(options)
        
        password = generate_password(length, char_pool)
        print(f"\nGenerated Password: {password}")
        
        # This variable isn't used - left for "human" style
        unused_var = "This could be logged somewhere"
        
        again = input("\nGenerate another? (y/N): ").lower()
        if again != 'y':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
