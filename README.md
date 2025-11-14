<h1 align="center">
  <img src="https://raw.githubusercontent.com/blacklatch-cybersecurity/assets/main/ai-threat-deception/logo.png" width="120"/><br>
  AI Threat Deception Engine
</h1>

<p align="center">
  <b>Advanced Deception Intelligence • Real-time Intent Detection • MITRE Mapping • Honeypot Analysis</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Framework-Flask-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge">
</p>

---

## 🚀 Overview  
AI Threat Deception Engine is an intelligent system that:
- Detects attacker **intent** (Recon, Exploit, Persistence)
- Normalizes malicious text using LLM signals  
- Maps detected intent to **MITRE ATT&CK**
- Displays results in a live deception dashboard
- Integrates with honeypot events (SSH fake server)

This project is built for SOC teams, DFIR units, and deception engineers.

---

## 🧠 Core Features

### ✔️ 1. Real-time threat intent classification  
### ✔️ 2. Live deception dashboard  
### ✔️ 3. MITRE ATT&CK automatic mapping  
### ✔️ 4. Timeline of attacker actions  
### ✔️ 5. Honeypot event integration  
### ✔️ 6. JSON API for automation  
### ✔️ 7. Full local inference (No cloud needed)

---

## 📸 Screenshots

### **Deception Dashboard**
![Dashboard](https://raw.githubusercontent.com/blacklatch-cybersecurity/assets/main/ai-threat-deception/dashboard.png)

### **MITRE Mapping Heatmap**
![MITRE](https://raw.githubusercontent.com/blacklatch-cybersecurity/assets/main/ai-threat-deception/mitre.png)

---

## 🏗️ Installation
git clone https://github.com/blacklatch-cybersecurity/ai-threat-deception.git
cd ai-threat-deception
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./run.sh

Dashboard runs at:
http://127.0.0.1:9900


---

## 🔌 API Usage

### **Analyze text**
POST /api/analyze
{
"text": "nmap -sV -p 22 server"
}

### **Response**
{
"intent": "Reconnaissance",
"mitre": "TA0043",
"risk": "Medium",
"explanation": "The actor is scanning ports for service discovery."
}


---

## 🗺 MITRE ATT&CK Mapping

| Intent | MITRE Technique | Example |
|-------|-----------------|---------|
| Recon | TA0043 | nmap, enum, scan |
| Exploit | TA0002 | exploit-db, sqlmap |
| Credential Theft | TA0006 | hydra, brute-force |
| Persistence | TA0003 | backdoor, implant |

---

## 🪤 Honeypot Integration
SSH fake honeypot logs attacker commands and sends them to classifier.

To run honeypot:
python3 honeypot/ssh_fake.py


---

## 🐳 Docker Deployment
docker build -t deception-ai .
docker run -p 9900:9900 deception-ai


---

## 🔐 Maintained by  
**Blacklatch Cybersecurity Defense**
Founder & CEO – Blacklatch Cyber Defense
Offensive + Defensive Cyber Engineering
