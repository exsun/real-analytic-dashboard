import streamlit as st
import pandas as pd

def epley_1rm(weight, reps):
    """
    Calculate 1RM using the Epley formula.
    1RM = W * (1 + 0.0333 * R)
    """
    return weight * (1 + 0.0333 * reps)

def brzycki_1rm(weight, reps):
    """
    Calculate 1RM using the Brzycki formula.
    1RM = W / (1.0278 - 0.0278 * R)
    """
    denominator = 1.0278 - 0.0278 * reps
    if denominator <= 0:
        return 0  # Avoid division by zero or negative
    return weight / denominator

# A reference list of (Reps, Percentage) pairs down to ~35%.
rep_percentage_data = [
    (1,   100),
    (2,    95),
    (3,    93),
    (4,    90),
    (5,    87),
    (6,    85),
    (7,    83),
    (8,    80),
    (9,    77),
    (10,   75),
    (11,   70),  # Typically 11–12 ~70%
    (12,   70),
    (13,   65),  # Typically 13–15 ~65%
    (14,   65),
    (15,   65),
    (16,   60),  # Typically 16–20 ~60%
    (17,   60),
    (18,   60),
    (19,   60),
    (20,   60),
    (25,   50),  # Broad range for higher reps ~50–55%
    (30,   40),
    (35,   35),
]

# -----------------
# Streamlit App
# -----------------

st.title("One-Rep Max Calculator & Percentage Breakdown")

st.write("""
This tool calculates your estimated 1RM using either the Epley or Brzycki formula,
and provides a reference table showing how much weight corresponds to each rep range
(roughly 35% to 100% of 1RM).
""")

# Get user inputs
weight = st.number_input("Weight lifted (kg)", min_value=0.0, value=80.0)
reps = st.number_input("Number of reps performed", min_value=1, value=8)

formula = st.selectbox(
    "Select formula for 1RM calculation:",
    ("Epley", "Brzycki")
)

# Calculate 1RM
if formula == "Epley":
    estimated_1rm = epley_1rm(weight, reps)
else:
    estimated_1rm = brzycki_1rm(weight, reps)

st.subheader("Estimated 1RM")
st.write(f"**{estimated_1rm:.2f} kg**")

# Build the DataFrame for the rep ranges and percentages
df_data = []
for rep_count, perc in rep_percentage_data:
    weight_at_perc = (perc / 100.0) * estimated_1rm
    df_data.append({
        "% of 1RM": f"{perc}%",
        "Weight (kg)": f"{weight_at_perc:.2f}",
        "Reps": rep_count
    })

df = pd.DataFrame(df_data)

st.subheader("Approximate Rep-to-Weight Breakdown")
st.dataframe(df,hide_index=True)

st.write("""
**How to use this table**:  
- Each row shows a *rough* rep count and the corresponding percentage of your 1RM.  
- The "Weight (kg)" column approximates how much you might lift if you aim for that rep range.
""")