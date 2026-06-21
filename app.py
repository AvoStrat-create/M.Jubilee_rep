
import streamlit as st
import random

st.title("BB84 Quantum Cryptography Simulator")

n = st.slider("Number of Qubits", 10, 100, 20)

if st.button("Run Simulation"):

    alice_bits = [random.randint(0, 1) for _ in range(n)]
    alice_bases = [random.choice(['+', 'x']) for _ in range(n)]

    bob_bases = [random.choice(['+', 'x']) for _ in range(n)]

    bob_results = []

    for i in range(n):
        if alice_bases[i] == bob_bases[i]:
            bob_results.append(alice_bits[i])
        else:
            bob_results.append(random.randint(0, 1))

    matching_positions = []

    for i in range(n):
        if alice_bases[i] == bob_bases[i]:
            matching_positions.append(i)

    shared_key = [bob_results[i] for i in matching_positions]

    st.subheader("Results")

    st.write("Alice Bits:", alice_bits)
    st.write("Alice Bases:", alice_bases)
    st.write("Bob Bases:", bob_bases)
    st.write("Matching Positions:", matching_positions)
    st.write("Shared Secret Key:", shared_key)
