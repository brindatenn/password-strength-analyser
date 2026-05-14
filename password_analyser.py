import hashlib
import requests
import re


HIBP_API_URL = "https://api.pwnedpasswords.com/range/"


def analyse_password_strength(password: str) -> dict:
    score = 0
    feedback = []

    length = len(password)

    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_symbol = bool(re.search(r"[^A-Za-z0-9]", password))

    if length >= 12:
        score += 2
    elif length >= 8:
        score += 1
    else:
        feedback.append("Use at least 12 characters.")

    if has_lower:
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    if has_upper:
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    if has_digit:
        score += 1
    else:
        feedback.append("Add numbers.")

    if has_symbol:
        score += 1
    else:
        feedback.append("Add symbols such as !, %, $, @, or #.")

    common_patterns = ["password", "admin", "qwerty", "1234", "letmein", "welcome"]

    if any(pattern in password.lower() for pattern in common_patterns):
        score -= 2
        feedback.append("Avoid common words or patterns such as 'password', 'admin', or '1234'.")

    if len(set(password)) <= 4:
        score -= 1
        feedback.append("Avoid repeating the same characters too often.")

    if score <= 2:
        rating = "Weak"
    elif score <= 4:
        rating = "Moderate"
    else:
        rating = "Strong"

    return {
        "score": max(score, 0),
        "rating": rating,
        "feedback": feedback
    }


def sha1_hash_password(password: str) -> str:
    return hashlib.sha1(password.encode("utf-8")).hexdigest().upper()


def check_password_breach(password: str) -> int:
    sha1_password = sha1_hash_password(password)

    prefix = sha1_password[:5]
    suffix = sha1_password[5:]

    response = requests.get(HIBP_API_URL + prefix, timeout=10)

    if response.status_code != 200:
        raise RuntimeError("Could not contact HaveIBeenPwned API.")

    hashes = response.text.splitlines()

    for line in hashes:
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return int(count)

    return 0


def main():
    print("=" * 60)
    print("Password Strength Analyser and Breach Detector")
    print("=" * 60)

    password = input("Enter password to analyse: ")

    if not password:
        print("No password entered.")
        return

    print("\nAnalysing password strength...")
    strength_result = analyse_password_strength(password)

    print(f"\nStrength Rating: {strength_result['rating']}")
    print(f"Score: {strength_result['score']}/6")

    if strength_result["feedback"]:
        print("\nSuggestions:")
        for item in strength_result["feedback"]:
            print(f"- {item}")
    else:
        print("\nGood password structure.")

    print("\nChecking breach database securely...")

    try:
        breach_count = check_password_breach(password)

        if breach_count > 0:
            print(f"\nWarning: This password has appeared in {breach_count:,} known data breaches.")
            print("You should not use this password.")
        else:
            print("\nGood news: This password was not found in the known breach database.")

    except RuntimeError as error:
        print(f"\nError: {error}")
    except requests.RequestException:
        print("\nNetwork error: Could not connect to the breach-checking service.")

    print("\nSecurity note: Your full password was never sent to the API.")
    print("Only the first 5 characters of its SHA-1 hash were sent.")


if __name__ == "__main__":
    main()