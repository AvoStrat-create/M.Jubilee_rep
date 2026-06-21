import streamlit as st
import random
import pandas as pd

st.set_page_config(
    page_title="BB84 Quantum Cryptography Dashboard",
    layout="wide"
)

st.title("BB84 Quantum Cryptography Analytics Dashboard")

st.markdown("""
This dashboard simulates the BB84 Quantum Key Distribution protocol and
demonstrates how eavesdropping can be detected using quantum principles.
""")

# Sidebar Controls
st.sidebar.header("Simulation Controls")

n = st.sidebar.slider(
    "Number of Qubits",
    min_value=10,
    max_value=500,
    value=100
)

eve_enabled = st.sidebar.checkbox(
    "Enable Eve (Attacker)"
)

run_simulation = st.sidebar.button(
    "Run Simulation"
)

if run_simulation:

    # Alice generates random bits and bases
    alice_bits = [random.randint(0, 1) for _ in range(n)]
    alice_bases = [random.choice(['+', 'x']) for _ in range(n)]

    # Bob chooses random bases
    bob_bases = [random.choice(['+', 'x']) for _ in range(n)]

    bob_results = []

    # Eve OFF
    if not eve_enabled:

        for i in range(n):

            if alice_bases[i] == bob_bases[i]:
                bob_results.append(alice_bits[i])

            else:
                bob_results.append(random.randint(0, 1))

    # Eve ON
    else:

        eve_bases = [random.choice(['+', 'x']) for _ in range(n)]

        eve_results = []

        for i in range(n):

            if alice_bases[i] == eve_bases[i]:
                eve_results.append(alice_bits[i])

            else:
                eve_results.append(random.randint(0, 1))

        for i in range(n):

            if eve_bases[i] == bob_bases[i]:
                bob_results.append(eve_results[i])

            else:
                bob_results.append(random.randint(0, 1))

    # Matching positions
    matching_positions = []

    for i in range(n):

        if alice_bases[i] == bob_bases[i]:
            matching_positions.append(i)

    # Shared key
    shared_key = [bob_results[i] for i in matching_positions]

    # Error calculation
    errors = 0

    for i in matching_positions:

        if alice_bits[i] != bob_results[i]:
            errors += 1

    if len(matching_positions) > 0:
        error_rate = (errors / len(matching_positions)) * 100
    else:
        error_rate = 0

    # Dashboard Metrics
    st.subheader("Key Metrics")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Qubits Sent", n)
    col2.metric("Matching Bases", len(matching_positions))
    col3.metric("Shared Key Length", len(shared_key))
    col4.metric("Errors", errors)
    col5.metric("Error Rate (%)", round(error_rate, 2))

    # Security Status
    st.subheader("🛡 Security Assessment")

    if eve_enabled:

        if error_rate > 10:
            st.error("Possible Eavesdropping Detected")

        elif error_rate > 0:
            st.warning("Some Errors Detected")

        else:
            st.success("No Eavesdropping Detected")

    else:
        st.success("Communication Secure")

    # Analytics Chart
    st.subheader("Basis Matching Analytics")

    chart_data = pd.DataFrame({
        "Category": [
            "Matching Bases",
            "Non-Matching Bases"
        ],
        "Count": [
            len(matching_positions),
            n - len(matching_positions)
        ]
    })

    st.bar_chart(
        chart_data.set_index("Category")
    )

    # Data Table
    st.subheader("Transmission Data")

    data = pd.DataFrame({
        "Alice Bit": alice_bits,
        "Alice Basis": alice_bases,
        "Bob Basis": bob_bases,
        "Bob Result": bob_results
    })

    st.dataframe(data)

    # Shared Key
    st.subheader("Shared Secret Key")

    st.code(
        "".join(str(bit) for bit in shared_key),
        language="text"
    )
