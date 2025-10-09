# 🔐 Automated Password Security Assessor

This project is a comprehensive tool built in Python to assess the strength of passwords based on multiple security criteria. It features an interactive web interface built with Streamlit and a command-line version for quick assessments.

The assessor provides a final score, a strength rating, and actionable feedback to help users create more secure passwords.

## ✨ Features

The tool evaluates passwords against four key security metrics:

* **Length Analysis:** Scores the password based on its total number of characters, rewarding longer passwords.
* **Character Variety:** Checks for the presence of lowercase letters, uppercase letters, numbers, and special characters.
* **Common Password Check:** Compares the password against a list of the most common and easily guessable passwords.
* **Data Breach Check:** Securely checks the password against the 'Have I Been Pwned' Pwned Passwords API to see if it has been exposed in a known data breach.

## 🚀 Web Application UI

The project includes an easy-to-use web interface powered by Streamlit.

*(**Pro Tip:** Upload the screenshot `ps_2.png` to an `assets` folder and rename it to `password-assessor-ui.png` to make this image appear)*
`![Web UI Screenshot](assets/password-assessor-ui.png)`

## 🛠️ Technologies Used

* **Python**
* **Streamlit:** For the interactive web application.
* **Requests:** For making API calls to the 'Have I Been Pwned' service.
* **Click:** For creating the command-line interface.

## ⚙️ Installation & Usage

Follow these steps to set up and run the project locally.

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <your-project-folder>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *(On Windows, use `venv\Scripts\activate`)*

3.  **Install the required dependencies:**
    (The `requirements.txt` file is visible in your project directory).
    ```bash
    pip install -r requirements.txt
    ```

### Running the Web Application

To launch the Streamlit web interface, run the following command:
```bash
streamlit run app.py

Bash :
python assessor.py "Your-Password-Here"
