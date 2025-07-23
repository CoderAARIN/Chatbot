import pyttsx3
import regex as re
import random
import json
import os
import wikipedia
import datetime
import webbrowser


# ✅ Load existing user data from file
def load_user_data():
    if os.path.exists('user_data.json'):
        with open('user_data.json', 'r') as file:
            return json.load(file)
    return {}

# ✅ Save user data to file
def save_user_data(data):
    with open('user_data.json', 'w') as file:
        json.dump(data, file)

# ✅ Delete user data for re-login
def delete_user_data():
    if os.path.exists('user_data.json'):
        os.remove('user_data.json')


# ✅ Start with two options: Re-login or Continue
print("👋 Welcome to Jarvis!")
if os.path.exists('user_data.json'):
    choice = input("👉 Do you want to:\n1. Re-login\n2. Continue\n\nEnter your choice (1/2): ").strip()

    if choice == '1':
        delete_user_data()
        print("\n✅ Previous user data deleted. Please log in again.\n")
    elif choice == '2':
        # ✅ Load existing user data and continue
        user_data = load_user_data()
        if user_data:
            entered_name = input("\nEnter your full name to continue: ").strip()

            # ✅ Match with full name instead of first name
            if entered_name.lower() == user_data.get('full_name', '').lower():
                print(f"✅ Welcome back, {user_data.get('first_name')}!")
                engine = pyttsx3.init()
                engine.say(f"Hi {user_data.get('first_name')}! How can I help you today?")
                engine.runAndWait()
                exit()
            else:
                print("❌ User not recognized. Please log in again.")
    else:
        print("❌ Invalid choice. Restarting...")
        exit()

# ✅ If no existing data or re-login chosen → Start fresh login
print("\nHi user, welcome to the world of AI!")
print("Before you start using Jarvis, you must create an account.")

full_name = input("Enter your full name: ").strip()
email = input("Enter your email address: ").strip()
while not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
    print("❌ Invalid email address. Try again.")
    email = input("Enter your email address: ").strip()

phone = input("Enter your phone number: ").strip()
while not re.match(r"^\d{10}$", phone):
    print("❌ Invalid phone number. Must be 10 digits.")
    phone = input("Enter your phone number: ").strip()

print("\n✅ Create a password")
print("👉 Must have:\n - At least 8 characters\n - Uppercase and lowercase letters\n - A number\n - A special character (@, #, $, etc.)")

# ✅ Password Strength Checker
def check_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return "Password must contain at least one number."
    if not re.search(r"[@#$%^&*!]", password):
        return "Password must contain at least one special character (@, #, $, etc.)."
    return "Password is strong!"

password = input("Enter your password: ").strip()
result = check_password(password)
while result != "Password is strong!":
    print(f"❌ {result}")
    password = input("Enter your password: ").strip()
    result = check_password(password)

print("✅ Password accepted!")

# ✅ Generate OTP
code = str(random.randint(100000, 999999))
print(f"\nYour 6-digit code is: {code}")

otp = input("Enter the given code: ").strip()
while otp != code:
    print("❌ Incorrect code. Try again.")
    otp = input("Enter the given code: ").strip()

print("✅ Thanks for logging in with us!")


# ✅ Save user data after successful login
user_data = {
    'first_name': full_name.split()[0],
    'full_name': full_name,
    'email': email,
    'phone': phone,
    'password': password
}
save_user_data(user_data)



print("Thanks for joinning with us")

# ✅ Greeting after successful login


