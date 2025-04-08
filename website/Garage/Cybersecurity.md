This is a hands-on learning roadmap for Cybersecurity.

### Level 0: Foundations of IT security

**Goal:** Understand the fundamentals of information security and the modern threat landscape.

### Topics

- What is cybersecurity?
- Security goals: confidentiality, integrity, availability (CIA)
- Introduction to digital threats and risks

### Mini-projects

- Simulate a phishing attack scenario (via mock emails)
- Create a visual map of the CIA triad applied to a company
- Make a “top 10 cybersecurity terms” flashcard deck

---

### Level 1: Threats and protection techniques

**Goal:** Learn to recognize cyber threats and explore basic protection strategies.

### Topics

- Types of threats (malware, phishing, ransomware)
- Social engineering
- Antivirus and firewall basics

### Mini-projects

- Simulate threat detection with ClamAV or Windows Defender
- Create a “security awareness” presentation for non-tech users
- Design a personal cybersecurity checklist

---

### Level 2: Local systems security

**Goal:** Understand how to secure personal or organizational local systems.

### Topics

- OS and software vulnerabilities
- System hardening practices (Windows/Linux)
- Access control and authentication

### Mini-projects

- Harden a virtual Linux machine (disable services, enable UFW, set SSH config)
- Create a user role and permission matrix
- Write a script to monitor file changes in a folder

---

### Level 3: Securing data transmission

**Goal:** Protect information in transit using encryption and secure protocols.

### Topics

- Symmetric vs asymmetric encryption
- HTTPS, TLS/SSL, VPNs
- Email security (S/MIME, PGP)

### Mini-projects

- Use `openssl` to encrypt and decrypt a file
- Set up a simple HTTPS server using a self-signed cert
- Send a signed/encrypted email via Thunderbird + GPG

---

### Level 4: Threat environment & risk identification

**Goal:** Analyze the environment in which cyber threats operate and how to identify them.

### Topics

- Cyber threat landscape (APT, zero-day, DDoS, IoT threats)
- Risk management frameworks (ISO/IEC 27005 basics)
- Threat modeling (STRIDE)

### Mini-projects

- Map STRIDE threats for a web app
- Create a threat matrix and risk chart
- Simulate a DDoS detection with network tools (e.g., Wireshark)

---

### Level 5: Secure programming & algorithmic defense

**Goal:** Understand how insecure code leads to vulnerabilities and learn how to prevent them.

### Topics

- Secure coding practices (input validation, SQL injection)
- OWASP Top 10 vulnerabilities
- Static analysis tools

### Mini-projects

- Vulnerable web app analysis (e.g., DVWA or Juice Shop)
- Fix a set of insecure code examples
- Write a Python login script with secure password hashing

---

### Level 6: Cybersecurity system design

**Goal:** Design an organizational cybersecurity system or security policy.

### Topics

- Layers of defense
- Policy creation (access, backup, incident response)
- Security operations center (SOC) basics

### Mini-projects

- Draft a simple company-wide security policy
- Create a layered defense diagram for a small office
- Document an incident response plan template

---

### Level 7: Integrated Security Systems & Tools

**Goal:** Learn how different security tools work together in real infrastructure.

### Topics

- IDS/IPS (e.g. Snort, Suricata)
- Firewalls (pfSense, iptables)
- Log management (SIEM overview)

### Mini-projects

- Simulate intrusion detection with Snort
- Build a log monitoring dashboard (e.g., ELK stack basics)
- Combine UFW, fail2ban, and logs into a simple security setup
