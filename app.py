import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="BB84 Quantum Dashboard")

st.title("BB84 Quantum Cryptography Dashboard")

n = st.slider("Number of Qubits", 10, 500, 100)

if st.button("Run Simulation"):

    alice_bits = [random.randint(0,1) for _ in range(n)]
    alice_bases = [random.choice(['+','x']) for _ in range(n)]

    bob_bases = [random.choice(['+','x']) for _ in range(n)]

    bob_results = []

    for i in range(n):
        if alice_bases[i] == bob_bases[i]:
            bob_results.append(alice_bits[i])
        else:
            bob_results.append(random.randint(0,1))

    matching_positions = []

    for i in range(n):
        if alice_bases[i] == bob_bases[i]:
            matching_positions.append(i)

    shared_key = [bob_results[i] for i in matching_positions]

    errors = 0

    for i in matching_positions:
        if alice_bits[i] != bob_results[i]:
            errors += 1

    error_rate = 0

    if len(matching_positions) > 0:
        error_rate = (errors / len(matching_positions)) * 100
            st.subheader("Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Qubits Sent", n)
    col2.metric("Matching Bases", len(matching_positions))
    col3.metric("Key Length", len(shared_key))
    col4.metric("Errors", errors)    st.subheader("Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Qubits Sent", n)
    col2.metric("Matching Bases", len(matching_positions))
    col3.metric("Key Length", len(shared_key))
    col4.metric("Errors", errors)
        st.subheader("Security Assessment")

    if errors > 0:
        st.error(" Eavesdropping Detected")
    else:
        st.success(" Communication Secure")
            data = pd.DataFrame({
        "Alice Bit": alice_bits,
        "Alice Basis": alice_bases,
        "Bob Basis": bob_bases,
        "Bob Result": bob_results
    })

    st.subheader("Transmission Data")
    st.dataframe(data)
    st.subheader("Simulation Analytics")

    chart_data = pd.DataFrame({
        "Category": ["Matching", "Non-Matching"],
        "Count": [
            len(matching_positions),
            n - len(matching_positions)
        ]
    })

    st.bar_chart(
        chart_data.set_index("Category")
    )
    st.metric(
        "Error Rate (%)",
        round(error_rate, 2)
    )

