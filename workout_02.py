import streamlit as st
import pandas as pd

# Load the CSV file with the correct delimiter
df = pd.read_csv("TREINO_BASICO_PICS.csv", delimiter=";")

# Page configuration for a wide layout
st.set_page_config(page_title="FITNESS PLANNER", layout="wide")

# Inject custom CSS for the background image
st.markdown(
    f"""
    <style>
    /* Set the background image */
    .stApp {{
        background: url("https://t4.ftcdn.net/jpg/03/68/80/31/240_F_368803108_q1VVhfqt6wXTRUQ4FEc6Ucr41eNcEBSv.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    /* Customize text color for better visibility */
    h1, h2, h3, h4, h5, h6, p, div {{
        color: white;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Title Section
st.markdown("<h4 style='color:yellow;'>Bem vindo ao FITAPP</h4>", unsafe_allow_html=True)

# Sidebar for Slicer
st.sidebar.title("Selecione o exercício")
day_group = st.sidebar.selectbox("Selecione (DIA - GRUPO):", options=df['DIA - GRUPO'].unique())

# Title Section
st.markdown("Selecione ao lado o dia e treino desejado.")
st.markdown(f"<div style='font-size:22px;'>🏋️ {day_group}</div>", unsafe_allow_html=True)


# Filter the DataFrame based on the selected day group
filtered_df = df[df['DIA - GRUPO'] == day_group]

# Check if there are exercises to display
if not filtered_df.empty:
    # Loop through the filtered DataFrame
    for index, row in filtered_df.iterrows():
        # Create a 2-column layout
        col1, col2 = st.columns([1, 3])  # Adjust column widths as needed
        
        # Display the image in the first column
        with col1:
            st.image(row['IMAGE'], width=400)  # Adjust the size of the image

        # Display exercise details in the second column
        with col2:
            st.subheader(f"{row['EXERCICIO']}")
            st.markdown(f"🔢  {row['REPETIÇOES']}")
            st.markdown(f"📅  {row['DIA - GRUPO']}")
        
        # Add a horizontal line between exercises for better separation
        st.markdown("---")
else:
    st.warning("No exercises found for the selected day group. Please choose a different group.")

# Footer Section
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("Created by Donizetti da Silva")
