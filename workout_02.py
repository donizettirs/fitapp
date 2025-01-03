import streamlit as st
import pandas as pd
import time

# Load the CSV file with the correct delimiter
df = pd.read_csv("TREINO_BASICO_PICS.csv", delimiter=";")

# Page configuration for a wide layout
st.set_page_config(page_title="FITNESS PLANNER", layout="wide")

# Inject custom CSS for the background image, hide header and footer
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
    /* Hide the Streamlit header */
    header {{
        visibility: hidden;
    }}
    /* Hide the footer */
    footer {{
        visibility: hidden;
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

# Sidebar Inputs for Timer
st.sidebar.title("Configuração do Timer")
rounds = st.sidebar.number_input("Número de séries:", min_value=1, value=3, step=1)
interval = st.sidebar.number_input("Intervalo entre séries (em segundos):", min_value=10, value=30, step=5)

# Title Section
st.markdown("Selecione ao lado o dia e treino desejado.")
st.markdown(f"<div style='font-size:22px;'>🏋️ {day_group}</div>", unsafe_allow_html=True)

# Filter the DataFrame based on the selected day group
filtered_df = df[df['DIA - GRUPO'] == day_group]

# Check if there are exercises to display
if not filtered_df.empty:
    for index, row in filtered_df.iterrows():
        # Create a 2-column layout
        col1, col2 = st.columns([1, 3])  # Adjust column widths as needed
        
        # Display the image in the first column
        with col1:
            st.image(row['IMAGE'], width=400)  # Adjust the size of the image

        # Display exercise details in the second column
        with col2:
            st.subheader(f"{row['EXERCICIO']}")
            st.markdown(f"🔢 &nbsp;  {row['REPETIÇOES']}")
            st.markdown(f"📅 &nbsp; {row['DIA - GRUPO']}")

            # Timer Logic using session_state for round tracking
            if f"round_{index}_{row['EXERCICIO']}" not in st.session_state:
                st.session_state[f"round_{index}_{row['EXERCICIO']}"] = 0  # Initialize round state

            current_round = st.session_state[f"round_{index}_{row['EXERCICIO']}"]

            # Display exercise timer button
            if st.button(f"Iniciar intervalo {row['EXERCICIO']}", key=f"start_button_{index}_{row['EXERCICIO']}"):
                st.write(f"Iniciando {row['EXERCICIO']}...")

                # Timer Logic for current round
                for current_round in range(current_round + 1, rounds + 1):
                    st.session_state[f"round_{index}_{row['EXERCICIO']}"] = current_round
                    st.write(f"Série {current_round} de {rounds}")

                    # Display countdown in a single line
                    timer_display = st.empty()  # Placeholder for countdown display
                    progress_bar = st.progress(0)

                    for seconds_left in range(interval, 0, -1):
                        mins, secs = divmod(seconds_left, 60)
                        timer_display.text(f"Tempo restante: {mins:02d}:{secs:02d}")
                        progress_bar.progress((interval - seconds_left) / interval)
                        time.sleep(1)  # Delay for 1 second

                    timer_display.text("Intervalo concluído!")
                    progress_bar.progress(1.0)
                    st.success(f"Série {current_round} concluída!")

                    # Pause before the next round
                    if current_round < rounds:
                        st.write("Aguarde para iniciar a próxima série.")
                        st.session_state[f"round_{index}_{row['EXERCICIO']}"] = current_round

                        # Pause logic until user is ready for the next round
                        while st.session_state.get(f"round_{index}_{row['EXERCICIO']}") == current_round:
                            time.sleep(0.1)  # Prevent high CPU usage
                        
                st.balloons()

        # Add a horizontal line between exercises for better separation
        st.markdown("---")
else:
    st.warning("No exercises found for the selected day group. Please choose a different group.")

# Footer Section
st.caption("Created by Donizetti da Silva")
