# Password Strength Analyser and Breach Detector
A Python command-line security tool that analyses password strength and checks whether a password has appeared in known data breaches using the HaveIBeenPwned Pwned Passwords API.
The tool combines local password strength analysis with privacy-preserving breach detection using SHA-1 hashing and k-anonymity.

## Features
- Analyses password strength based on:
  - Password length
  - Uppercase letters
  - Lowercase letters
  - Numbers
  - Symbols
  - Common weak patterns
- Gives a strength rating: Weak, Moderate, or Strong
- Provides improvement suggestions for weak passwords
- Checks whether a password appears in known breach datasets
- Uses SHA-1 hashing before breach checking
- Sends only the first 5 characters of the SHA-1 hash to the HaveIBeenPwned API
- Compares the remaining hash suffix locally
- Does not send the full plaintext password to any external service

## Why This Project Matters
Weak and reused passwords are a major security risk. Many passwords that appear strong may already have been exposed in previous data breaches.
This tool helps users assess two things:
1. Whether a password is structurally strong.
2. Whether the password has appeared in known breach databases.
A password can be long and complex but still unsafe if it has already been leaked. For that reason, breach detection is an important part of practical password security.

## How It Works
The project performs two main checks.
### 1. Local Password Strength Analysis
The password is first analysed locally. The tool checks whether the password contains:
- A suitable length
- Lowercase letters
- Uppercase letters
- Numbers
- Symbols
- Common weak words or patterns
Based on these checks, the tool gives the password a score and a rating.
Example feedback may include:
```text
Use at least 12 characters.
Add uppercase letters.
Add symbols such as !, %, $, @, or #.
Avoid common words or patterns such as 'password', 'admin', or '1234'.
```

### 2. Breach Detection Using HaveIBeenPwned
The tool then checks whether the password appears in the HaveIBeenPwned Pwned Passwords database.
The full password is never sent to the API.
Instead, the tool follows this process:
1. The password is converted into a SHA-1 hash locally.
2. The SHA-1 hash is split into two parts:
    - The first 5 characters
    - The remaining hash suffix
3. Only the first 5 characters are sent to the HaveIBeenPwned API.
4. The API returns a list of hash suffixes that match that prefix.
5. The tool compares the remaining suffix locally.
6. If a match is found, the password has appeared in known breaches.

For example:
```text
Password: password123
SHA-1 hash: CBFDAC6008F9CAB4083784CBD1874F76618D2A97

Prefix sent to API: CBFDA
Suffix kept locally: C6008F9CAB4083784CBD1874F76618D2A97
```
This method is known as k-anonymity. It allows the tool to check a password against breach data without exposing the full password or full hash to the API.
HaveIBeenPwned’s Pwned Passwords API is designed around this range-search model, where the request uses the first 5 characters of a SHA-1 hash and the returned results contain matching hash suffixes and breach counts.

## Technologies Used
- Python
- Requests
- Regular expressions
- SHA-1 hashing
- HaveIBeenPwned Pwned Passwords API
- Command-line interface

## Installation
Clone the repository:
```bash
git clone https://github.com/brindatenn/password-strength-analyser.git
cd password-strength-analyser
```
Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
### Windows PowerShell
Run:
```powershell
python password_analyser.py
```
### Git Bash on Windows
If running the script in Git Bash, use:
```bash
winpty python password_analyser.py
```
This is required on some Windows Git Bash setups because interactive Python input may not work properly with the normal command.

If this works for you:
```bash
python password_analyser.py
```
then ```text winpty ``` is not needed. However, if the program displays the input prompt but does not continue after typing a password, use the ```text winpty ``` command.

## Example Output
```text
============================================================
Password Strength Analyser and Breach Detector
============================================================
Enter password to analyse: password123

Analysing password strength...

Strength Rating: Weak
Score: 1/6

Suggestions:
- Add uppercase letters.
- Add symbols such as !, %, $, @, or #.
- Avoid common words or patterns such as 'password', 'admin', or '1234'.

Checking breach database securely...

Warning: This password has appeared in 2,254,650 known data breaches.
You should not use this password.

Security note: Your full password was never sent to the API.
Only the first 5 characters of its SHA-1 hash were sent.
```

## Project Structure
```text
password-strength-analyser/
│
├── password_analyser.py
├── requirements.txt
├── README.md
└── .gitignore
```
## Security Notes
This tool is designed for educational and defensive security purposes.
Although the tool avoids sending the full password to the API, users should avoid testing real passwords they actively use. Use sample or test passwords when demonstrating the project.
The breach-checking process is privacy-preserving because:
- The plaintext password is never sent.
- The full SHA-1 hash is never sent.
- Only the first 5 characters of the SHA-1 hash are sent.
- The final comparison is performed locally.

## Limitations
This tool uses rule-based password strength scoring. It can identify common weaknesses, but it does not replace a full enterprise-grade password policy system.
The breach detection depends on the HaveIBeenPwned database. If a password has not appeared in that dataset, the tool will report that it was not found, but this does not guarantee that the password has never been compromised elsewhere.

## Future Improvements
Possible improvements include:
- Adding command-line arguments with ```text argparse ```
- Adding JSON output for automation
- Adding unit tests
- Adding a password generator
- Adding offline breach-checking support
- Creating a Streamlit dashboard version
- Improving the scoring model using entropy estimation

## Disclaimer
This project is for educational and defensive security purposes only. Do not use it to collect, store, or test other people’s passwords.

## Author 
brindatenn
