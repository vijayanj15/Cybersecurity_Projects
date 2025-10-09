# assessor.py

import re
import hashlib
import requests
import click

# Load the set of common passwords from the file into memory for fast lookups.
# Using a 'set' is much more efficient for checking existence than a 'list'.
try:
    with open('common_passwords.txt', 'r') as f:
        COMMON_PASSWORDS = set(line.strip() for line in f)
except FileNotFoundError:
    print("Error: 'common_passwords.txt' not found. Please download it and place it in the same directory.")
    COMMON_PASSWORDS = set()

def check_length(password):
    """Scores the password based on its length."""
    length = len(password)
    if length < 8:
        return 0, "Password is too short (less than 8 characters)."
    elif 8 <= length <= 11:
        return 20, "Password length is okay (8-11 characters)."
    elif 12 <= length <= 15:
        return 40, "Password length is good (12-15 characters)."
    else:
        return 60, "Password length is excellent (16+ characters)."

def check_character_variety(password):
    """Scores the password based on the variety of characters used."""
    score = 0
    feedback = []
    
    if re.search(r'[a-z]', password):
        score += 10
    else:
        feedback.append("Add lowercase letters (a-z).")
        
    if re.search(r'[A-Z]', password):
        score += 10
    else:
        feedback.append("Add uppercase letters (A-Z).")
        
    if re.search(r'\d', password):
        score += 10
    else:
        feedback.append("Add numbers (0-9).")
        
    if re.search(r'[^a-zA-Z\d]', password): # Checks for non-alphanumeric characters
        score += 10
    else:
        feedback.append("Add special characters (e.g., !@#$%).")
        
    return score, " ".join(feedback)

def check_commonality(password):
    """Penalizes the password if it's in the common passwords list."""
    if password.lower() in COMMON_PASSWORDS:
        return -50, "This is a very common password and is extremely insecure."
    return 0, ""

def check_pwned_api(password):
    """
    Checks if the password has been exposed in a data breach using the
    'Have I Been Pwned' Pwned Passwords API with k-Anonymity.
    """
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_password[:5], sha1_password[5:]
    url = f'https://api.pwnedpasswords.com/range/{prefix}'
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return 0, f"API Error: Could not check if password was pwned (Status: {response.status_code})."
            
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return -100, f"DANGER: This password has appeared in a data breach {count} times! Do not use it."
                
        return 0, "Good news! This password was not found in any known data breaches."
    except requests.RequestException:
        return 0, "API Error: Could not connect to the 'Have I Been Pwned' service."

@click.command()
@click.argument('password', type=str)
def assess_password_strength(password):
    """An automated password security assessor that checks length, character variety,
    commonality, and exposure in data breaches."""
    
    total_score = 0
    feedback_items = []

    # Run all checks
    checks = [
        check_length,
        check_character_variety,
        check_commonality,
        check_pwned_api
    ]

    for check_func in checks:
        score, feedback = check_func(password)
        total_score += score
        if feedback:
            feedback_items.append(f"• {feedback}")

    # Determine final strength rating
    if total_score < 0:
        rating = "Very Weak"
    elif 0 <= total_score < 40:
        rating = "Weak"
    elif 40 <= total_score < 80:
        rating = "Medium"
    elif 80 <= total_score < 100:
        rating = "Strong"
    else:
        rating = "Very Strong"

    # Print the final report to the console
    click.echo("\n--- Password Security Assessment ---")
    click.echo(f"Final Score: {max(0, total_score)}/100")
    click.echo(f"Strength Rating: {rating}")
    click.echo("\nRecommendations:")
    if not feedback_items:
        click.echo("• Excellent password! Keep it safe.")
    else:
        for item in feedback_items:
            click.echo(item)
    click.echo("------------------------------------")


if __name__ == '__main__':
    assess_password_strength()

