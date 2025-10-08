# Salted Hash Cracker

This is a command-line tool written in Python to crack SHA256 hashes that have been salted. The project was developed to practice and demonstrate skills in Python scripting, cryptographic principles, and file handling for cybersecurity applications.

The script performs a dictionary attack against a list of salted SHA256 hashes, using a provided wordlist and salt value.

## Features
* **Algorithm:** Specifically targets the SHA256 hashing algorithm.
* **Salting Support:** Handles salted hashes where the salt is prepended to the password (`salt + password`) before hashing.
* **Dictionary Attack:** Reads from a user-provided wordlist to find matching passwords.
* **Efficient:** Clearly outputs the found passwords, the salt used, and the corresponding hash.

## How to Use

### Prerequisites
* Python 3

### Installation & Setup
1.  Clone the main repository and navigate into this project's directory:
    ```bash
    git clone [https://github.com/vijayanj15/Cybersecurity_Projects.git](https://github.com/vijayanj15/Cybersecurity_Projects.git)
    cd Cybersecurity_Projects/Hash_Cracker/
    ```

2.  Prepare your files:
    * A file containing the hashes you want to crack (e.g., `hashes.txt`).
    * A wordlist file containing potential passwords (e.g., `wordlist.txt`).

### Running the Script
Use the following command format to run the cracker:
```bash
python3 hash_cracker.py <path_to_hashes_file> <path_to_wordlist_file> --salt '<your_salt_value>'
