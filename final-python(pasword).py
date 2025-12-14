# -*- coding: utf-8 -*-
"""
Streamlit Password Strength Analyzer
"""

import streamlit as st
import random
import string
from datetime import datetime, timedelta

# --- دالة لتحليل قوة كلمة المرور ---
def password_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    score = 0
    if length >= 8:
        score += 1
    if has_upper:
        score += 1
    if has_lower:
        score += 1
    if has_digit:
        score += 1
    if has_special:
        score += 1

    if score <= 2:
        return "Weak"
    elif score == 3 or score == 4:
        return "Moderate"
    else:
        return "Strong"

# --- دالة لتوليد كلمة مرور عشوائية ---
def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

# --- واجهة Streamlit ---
st.title("🔒 Password Strength Analyzer")

# إدخال كلمة المرور
password_input = st.text_input("Enter your password:", type="password")

# زر للتحقق من القوة
if st.button("Check Strength"):
    if not password_input:
        st.warning("Please enter a password first!")
    else:
        strength = password_strength(password_input)
        st.success(f"Your password strength is: **{strength}**")

# زر لتوليد كلمة مرور عشوائية
st.subheader("Or generate a random password")
length = st.slider("Select password length", 8, 32, 12)

if st.button("Generate Password"):
    new_password = generate_random_password(length)
    st.info(f"Generated Password: `{new_password}`")
    strength = password_strength(new_password)
    st.success(f"Strength: **{strength}**")

# --- إضافة ميزة اقتراح تحسينات ---
st.subheader("Password Improvement Suggestions")
if password_input:
    suggestions = []
    if len(password_input) < 8:
        suggestions.append("Make it at least 8 characters long")
    if not any(c.isupper() for c in password_input):
        suggestions.append("Add uppercase letters")
    if not any(c.islower() for c in password_input):
        suggestions.append("Add lowercase letters")
    if not any(c.isdigit() for c in password_input):
        suggestions.append("Add numbers")
    if not any(c in string.punctuation for c in password_input):
        suggestions.append("Add special characters")
    
    if suggestions:
        st.write("Suggestions to improve your password:")
        for s in suggestions:
            st.write(f"- {s}")
    else:
        st.write("Your password is strong! ✅")


