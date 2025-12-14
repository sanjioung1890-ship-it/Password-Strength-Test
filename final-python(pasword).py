# -*- coding: utf-8 -*-
"""
Streamlit Version - Password Strength Tool
Author: Raghad
"""

import random
import string
from datetime import datetime, timedelta
import streamlit as st


# ---------------- Password Analyzer ----------------
class passCheck:
    def __init__(self, password):
        self.password = password

    def check(self):
        types = 0
        if any(c.islower() for c in self.password):
            types += 1
        if any(c.isupper() for c in self.password):
            types += 1
        if any(c.isdigit() for c in self.password):
            types += 1
        if any(c in string.punctuation for c in self.password):
            types += 1
        return types

    def length2(self):
        types = self.check()
        if len(self.password) <= 8 or types < 2:
            return "weak"
        elif 8 < len(self.password) < 10 and types >= 2:
            return "good"
        elif 10 <= len(self.password) < 14 and types >= 3:
            return "powerful"
        elif 12 <= len(self.password) < 16 and types == 4:
            return "very_powerful"
        else:
            return "too_long"


# ---------------- Suggest Stronger Password ----------------
class randoms_sugg:
    def suggest(self, password, suggestion):
        if suggestion == "weak":
            add = ''.join(random.choices(
                string.ascii_letters + string.digits + string.punctuation, k=6))
        elif suggestion == "good":
            k = random.randint(4, 8)
            add = ''.join(random.choices(
                string.ascii_uppercase + string.punctuation, k=k))
        elif suggestion == "powerful":
            target_length = random.randint(12, 16)
            to_add = max(0, target_length - len(password))
            k = random.randint(to_add, to_add + 4)
            add = ''.join(random.choices(
                string.ascii_letters + string.digits + string.punctuation, k=k))
        else:
            add = ""

        middle = len(password) // 2
        return password[:middle] + add + password[middle:]


# ---------------- Update Reminder ----------------
class update_reminder:
    def suggest_date(self):
        today = datetime.today()
        return (today + timedelta(weeks=2)).strftime('%Y-%m-%d')


# ================= Streamlit UI =================
st.set_page_config(page_title="Password Strength Tool", page_icon="🔐")

st.title("🔐 Password Strength Tool")
st.caption("By Raghad")

show_pass = st.checkbox("Show password")

password = st.text_input(
    "Enter your password",
    type="default" if show_pass else "password"
)

if st.button("Analyze Password"):
    if not password:
        st.error("Please enter a password.")
    else:
        checker = passCheck(password)
        strength = checker.length2()

        st.subheader("Password Strength")
        st.write(f"**{strength.replace('_', ' ').capitalize()}**")

        if strength in ["powerful", "very_powerful", "too_long"]:
            st.success("✅ Your password passed the strength test")

        # Suggestion
        if strength not in ["very_powerful", "too_long"]:
            suggester = randoms_sugg()
            suggested = suggester.suggest(password, strength)

            st.subheader("Suggested Password")
            st.code(suggested)

            st.download_button(
                "Copy Suggested Password",
                suggested,
                file_name="password.txt"
            )
        else:
            st.info("Your password is strong enough!")

        # Update reminder
        updater = update_reminder()
        st.subheader("Update Reminder")
        st.write(f"🔄 Update due date: **{updater.suggest_date()}**")

        if strength in ["powerful", "very_powerful", "too_long"]:
            st.divider()
            st.success("🎉 THIS IS THE END OF MY PROJECT")




