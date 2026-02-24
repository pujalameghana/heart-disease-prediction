# auth_config.py
import bcrypt

passwords = ["admin123", "doctor123", "panel123"]

print("Copy these hashed passwords into app_ui.py:")
for i, p in enumerate(passwords):
    hashed = bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()
    print(f"Password {i+1}: {hashed}")