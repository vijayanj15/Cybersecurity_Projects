# Advanced Network Vulnerability Scanner

This project is a powerful, multi-threaded network vulnerability scanner written in Python. It's designed to automate the initial phases of a penetration test by discovering live hosts, identifying open ports and running services, and cross-referencing those services with known vulnerabilities from the National Vulnerability Database (NVD).

## ✨ Features

The scanner operates in three distinct phases:

* **1. Host Discovery:**
    * Accepts a target network in CIDR notation (e.g., `10.0.2.0/24`).
    * Uses ARP requests with Scapy to quickly and reliably discover live hosts on the local network.
    * Reports the total number of active hosts found.

* **2. Port Scanning & Service Detection:**
    * Performs a fast, multi-threaded TCP port scan on each discovered host.
    * Attempts to grab the service banner from each open port to identify running software and its version (e.g., `vsFTPd 2.3.4`, `SSH-2.0-OpenSSH_4.7p1`).

* **3. Vulnerability Analysis:**
    * Parses product and version information from the collected banners.
    * Connects to the NVD via the `nvdlib` library to search for publicly disclosed CVEs (Common Vulnerabilities and Exposures) related to the detected service version.
    * Reports potential vulnerabilities found, including the CVE ID and a short description.

## 🚀 Sample Output

Here is a screenshot of the scanner in action, discovering hosts, finding open ports, and identifying potential CVEs.

*(**Action:** Upload your screenshot `nr_3.png` to the `assets` folder and rename it to `recon-output.png` for this image to appear)*
`![Scanner Output](assets/recon-output.png)`

## 🛠️ Technologies Used

* **Python**
* **Scapy:** For crafting and sending ARP packets during host discovery.
* **nvdlib:** A Python library for accessing the National Vulnerability Database API.
* **Threading & Queue:** For efficient, high-speed port scanning.

## ⚙️ Installation & Setup

Follow these steps to set up and run the project locally.

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd Cybersecurity_Projects/Network\ Reconnaissance/
    ```

2.  **Create and activate a Python virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    *(On Windows, use `venv\Scripts\activate`)*

3.  **Create a `requirements.txt` file** with the following content:
    ```
    scapy
    nvdlib
    ```

4.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Add Your NVD API Key:**
    * This scanner requires an NVD API key to look up CVEs. You can get a free key from the [NVD API Request Page](https://nvd.nist.gov/developers/request-an-api-key).
    * Open the `scanner.py` file and paste your key into the `NVD_API_KEY` variable inside the `find_cves` function.

## 💻 Usage

Run the script from the command line, providing a target IP address or a network range in CIDR notation. You may need to use `sudo` because Scapy's ARP scan requires root privileges to craft packets.

**Example Command**:
```bash
sudo python3 scanner.py 10.0.2.0/24
