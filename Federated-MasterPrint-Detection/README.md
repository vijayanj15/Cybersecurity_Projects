\# Federated Learning for Network-Wide MasterPrint Attack Detection



!\[Project Status](https://img.shields.io/badge/Status-Completed-success)

!\[Python](https://img.shields.io/badge/Python-3.x-blue)

!\[TensorFlow](https://img.shields.io/badge/Framework-TensorFlow-orange)



\## 📌 Overview

This project implements a \*\*privacy-preserving biometric defense system\*\* designed to detect "MasterPrint" presentation attacks on mobile devices. 



Unlike traditional centralized systems that store sensitive biometric data on servers (vulnerable to breaches like BioStar 2), this solution utilizes \*\*Federated Learning (FedAvg)\*\*. This architecture allows a network of devices to collaboratively train a \*\*MobileNetV2\*\* intrusion detection model without any raw user data ever leaving the local device.



\## 🛡️ The Problem: MasterPrint Vulnerability

Mobile fingerprint sensors typically capture partial fingerprints due to size constraints. Research (Roy et al., 2017) has shown that \*\*"MasterPrints"\*\*—synthetic partial prints with common ridge features—can exploit this entropy loss to fortuitously match up to \*\*65% of users\*\*.



\## 💡 The Solution: Federated Entropy Defense

We propose a dual-layer defense:

1\.  \*\*AI-Based Detection:\*\* A custom MobileNetV2 model trained to distinguish between high-entropy genuine prints and low-entropy MasterPrint attacks based on textural artifacts.

2\.  \*\*Privacy-Preserved Training:\*\* A Federated Learning simulation ($N=5$ clients) where only model gradients are shared, eliminating the risk of centralized data theft.



\## 📂 Project Structure

```text

├── data/                   # Dataset directory (FVC2004 + Synthetic)

├── results/                # Performance graphs and evidence logs

├── config.py               # Configuration parameters (Img size, Rounds, Clients)

├── model\_builder.py        # MobileNetV2 architecture definition

├── generate\_masterprints.py# Novel algorithm for synthetic attack generation

├── main\_federated.py       # Core simulation: Server aggregation \& Client training

├── demo.py                 # Live CLI demonstration script

├── requirements.txt        # Project dependencies

└── README.md               # Project documentation

