# app.py

import streamlit as st
# Import all the functions from your original script
from assessor import check_length, check_character_variety, check_commonality, check_pwned_api

def main():
    st.title("🔐 Automated Password Security Assessor")
    st.write("Enter a password to assess its strength and see if it has been exposed in a data breach.")

    # Get user input from a text box
    password = st.text_input("Enter your password:", type="password")

    if password:
        total_score = 0
        feedback_items = []
        
        # --- Reuse your existing logic ---
        checks = [check_length, check_character_variety, check_commonality, check_pwned_api]
        for check_func in checks:
            score, feedback = check_func(password)
            total_score += score
            if feedback:
                # Format feedback for display
                if "DANGER" in feedback or "very common" in feedback:
                    st.error(f"• {feedback}")
                elif "API Error" in feedback:
                    st.warning(f"• {feedback}")
                else:
                    feedback_items.append(feedback)

        # --- Display the results visually ---
        if total_score < 0:
            rating = "Very Weak 👎"
            st.progress(10)
        elif 0 <= total_score < 40:
            rating = "Weak 😟"
            st.progress(30)
        elif 40 <= total_score < 80:
            rating = "Medium 🤔"
            st.progress(60)
        elif 80 <= total_score < 100:
            rating = "Strong 👍"
            st.progress(90)
        else:
            rating = "Very Strong! 💪"
            st.progress(100)
        
        st.subheader(f"Strength Rating: {rating}")

        st.subheader("Recommendations:")
        for item in feedback_items:
            st.info(f"• {item}")

if __name__ == '__main__':
    main()


