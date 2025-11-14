import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# High-quality deception dataset
training_data = [
    ("nmap -A 192.168.1.1", "scan"),
    ("masscan 0.0.0.0/0", "scan"),
    ("port scanning detected 445", "scan"),

    ("hydra -l admin -P passwords.txt ssh://192.168.1.10", "brute"),
    ("failed password for root", "brute"),
    ("multiple authentication failures", "brute"),

    ("msfconsole exploit/linux/samba/usermap_script", "exploit"),
    ("buffer overflow attempt", "exploit"),
    ("malicious payload delivery", "exploit"),

    ("attacker probing file shares", "lateral"),
    ("remote command execution attempt", "lateral"),
    ("pivoting to internal network", "lateral"),

    ("dnsenum domain.com", "recon"),
    ("whois lookup", "recon"),
    ("subdomain enumeration", "recon"),
]

texts = [t[0] for t in training_data]
labels = [t[1] for t in training_data]

print("[*] Training deception classifier...")

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

model = LogisticRegression()
model.fit(X, labels)

joblib.dump(model, "model/model.pkl")
joblib.dump(vectorizer, "model/vector.pkl")

print("[+] Training complete. Model saved.")

