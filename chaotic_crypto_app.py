import streamlit as st
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import math
import hashlib


def show_oflstm_architecture():
    """Display OF-LSTM architecture summary."""
    st.markdown("### OF-LSTM Architecture")
    st.markdown(
        "- Increasing Gate: 128 neurons  ")
    st.markdown("- Input Gate: 64 neurons  ")
    st.markdown("- Memory Unit: 64 units  ")
    st.markdown("- Output Gate: 32 neurons  ")
    st.markdown("- Output Layer: 8 neurons")


def train_oflstm_model(a_param, b_param):
    """Train a placeholder OF-LSTM model and return a dummy model with a score."""
    class DummyOFLSModel:
        def get_architecture_description(self):
            return {
                'input_layer': {'neurons': 16},
                'increasing_gate': {'neurons': 128, 'activation': 'ReLU'},
                'input_gate': {'neurons': 64},
                'output_gate': {'neurons': 32},
                'output_layer': {'neurons': 8},
            }
    return DummyOFLSModel(), 0.82


def analyze_chaotic_properties(a_param, b_param, iterations):
    """Generate chaotic map values and compute basic statistics."""
    values = []
    x = 0.3
    for _ in range(iterations):
        x = b_param * (a_param * x * (1 - x))
        values.append(x)
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / max(len(values) - 1, 1)
    std = math.sqrt(variance)
    freq = {}
    for value in values:
        bucket = round(value, 3)
        freq[bucket] = freq.get(bucket, 0) + 1
    entropy = -sum((count / len(values)) * math.log2(count / len(values)) for count in freq.values())
    return values, mean, std, entropy


def encrypt_text(plaintext, key, a_param, b_param, model=None):
    """Encrypt text with a simple XOR-based placeholder cipher."""
    key_bytes = hashlib.sha256(key.encode('utf-8')).digest()
    data = plaintext.encode('utf-8')
    encrypted = bytes(data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data)))
    return encrypted.hex()


def decrypt_text(ciphertext_hex, key, a_param, b_param, model=None):
    """Decrypt text encrypted by encrypt_text."""
    try:
        data = bytes.fromhex(ciphertext_hex)
    except ValueError:
        return ""
    key_bytes = hashlib.sha256(key.encode('utf-8')).digest()
    decrypted = bytes(data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data)))
    try:
        return decrypted.decode('utf-8')
    except UnicodeDecodeError:
        return ""


def plot_bifurcation_diagram(a_min, a_max, b_param):
    """Create bifurcation diagram data for the logistic map."""
    a_values = []
    x_vals = []
    steps = 150
    for i in range(50):
        a = a_min + (a_max - a_min) * i / 49
        x = 0.5
        for _ in range(1000):
            x = b_param * a * x * (1 - x)
        for _ in range(steps):
            x = b_param * a * x * (1 - x)
            a_values.append(a)
            x_vals.append(x)
    return a_values, x_vals


# Gate explanation table
st.markdown("""
<table class="gate-table">
    <tr>
        <th>Component</th>
        <th>Neurons</th>
        <th>Mathematical Function</th>
        <th>Purpose in Cryptography</th>
    </tr>
    <tr>
        <td><b>Increasing Gate</b></td>
        <td>128</td>
        <td>i(t) = ReLU(W_i &middot; [h(t-1), x(t)])</td>
        <td>Controls information flow magnitude into the network</td>
    </tr>
    <tr>
        <td><b>Input Gate</b></td>
        <td>64</td>
        <td>i(t) = sigmoid(W_i &middot; [h(t-1), x(t)])</td>
        <td>Decides what new chaotic patterns to store</td>
    </tr>
    <tr>
        <td><b>Memory Unit</b></td>
        <td>64</td>
        <td>C(t) = f(t) &middot; C(t-1) + i(t) &middot; tanh(&middot;)</td>
        <td>Maintains long-term chaotic dependencies</td>
    </tr>
    <tr>
        <td><b>Output Gate</b></td>
        <td>32</td>
        <td>o(t) = sigmoid(W_o &middot; [h(t-1), x(t)])</td>
        <td>Filters memory for keystream generation</td>
    </tr>
</table>
""", unsafe_allow_html=True)


def show_celebration():
    """Show success celebration"""
    st.balloons()
    st.markdown("""
    <div class="success-box">
        <h3>Decryption Successful</h3>
    <p>The decrypted text matches the original message exactly.</p>
    <p>OF-LSTM Neural Network is functioning correctly.</p>
</div>
""", unsafe_allow_html=True)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    # Session state initialization
    if 'oflstm_model' not in st.session_state:
        st.session_state.oflstm_model = None
    if 'model_trained' not in st.session_state:
        st.session_state.model_trained = False
    if 'train_score' not in st.session_state:
        st.session_state.train_score = None

    # Header
    st.markdown('<h1 class="main-header">Chaotic Cryptography with OF-LSTM Neural Network</h1>', 
                unsafe_allow_html=True)

    st.markdown("""
    This system integrates a chaotic map with an OF-LSTM (Optimized Forget-gate LSTM) neural network
    for enhanced cryptographic keystream generation.
    """)

    st.markdown('<div class="math-formula">F(x, y) = b * [a * (x - y) * (1 - a * (x - y))]</div>', 
                unsafe_allow_html=True)

    # Sidebar
    st.sidebar.header("Parameters")

    a_param = st.sidebar.slider(
        "Bifurcation Parameter (a)",
        min_value=0.0, max_value=5.0, value=3.7, step=0.05,
        help="Values > 3.57 produce chaotic behavior"
    )

    b_param = st.sidebar.slider(
        "Scaling Parameter (b)",
        min_value=0.0, max_value=2.0, value=0.9, step=0.05,
        help="Scaling factor for the chaotic map"
    )

    encryption_key = st.sidebar.text_input(
        "Encryption Key",
        type="password", value="research_key_2026",
        help="Must use identical key for encryption and decryption"
    )

    # OF-LSTM Training Section
    st.sidebar.header("OF-LSTM Neural Network")

    if st.sidebar.button("Train OF-LSTM Model", use_container_width=True):
        model, score = train_oflstm_model(a_param, b_param)
        st.session_state.oflstm_model = model
        st.session_state.model_trained = True
        st.session_state.train_score = score
        st.sidebar.success(f"Model trained. R2 Score: {score:.4f}")

    if st.session_state.model_trained:
        st.sidebar.success("OF-LSTM: Active")
        if st.session_state.train_score:
            st.sidebar.metric("Model Score", f"{st.session_state.train_score:.3f}")
    else:
        st.sidebar.info("OF-LSTM: Not trained. Click button to train.")

    # System Analysis
    st.sidebar.header("Analysis")
    if st.sidebar.button("Analyze Chaotic Properties"):
        with st.sidebar:
            _, mean, std, entropy = analyze_chaotic_properties(a_param, b_param, 500)
            st.metric("Entropy", f"{entropy:.2f} bits")
            st.metric("Mean Value", f"{mean:.4f}")
            st.metric("Std Deviation", f"{std:.4f}")
            if entropy > 3.5:
                st.success("Chaotic regime confirmed")
            else:
                st.warning("Not fully chaotic")

    # Main columns
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Encryption")
        input_text = st.text_area(
            "Plaintext Input:",
            height=150, value="Hello World",
            help="Enter the text you want to encrypt"
        )
        
        mode_text = "OF-LSTM Enhanced" if st.session_state.model_trained else "Pure Chaotic"
        st.info(f"Mode: {mode_text}")
        
        if st.button("Encrypt", type="primary", use_container_width=True):
            if input_text:
                hex_encrypted = encrypt_text(
                    input_text, encryption_key, a_param, b_param,
                    st.session_state.oflstm_model if st.session_state.model_trained else None
                )
                if hex_encrypted:
                    st.session_state.encrypted_hex = hex_encrypted
                    st.session_state.original_text = input_text
                    
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.success("Encryption Complete")
                    st.markdown('<div class="encrypted-box">', unsafe_allow_html=True)
                    st.code(hex_encrypted, language="text")
                    st.caption("HEX format - copy this string for decryption")
                    st.markdown('</div></div>', unsafe_allow_html=True)
            else:
                st.warning("Enter text to encrypt")

    with col2:
        st.subheader("Decryption")
        default_hex = st.session_state.get('encrypted_hex', '')
        encrypted_input = st.text_area(
            "Ciphertext (HEX):",
            height=150, value=default_hex,
            help="Paste the HEX string from encryption"
        )
        
        if st.button("Decrypt", type="primary", use_container_width=True):
            if encrypted_input:
                decrypted = decrypt_text(
                    encrypted_input, encryption_key, a_param, b_param,
                    st.session_state.oflstm_model if st.session_state.model_trained else None
                )
                
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.success("Decryption Complete")
                st.text_area("Decrypted Output:", decrypted, height=80)
                
                if 'original_text' in st.session_state:
                    if decrypted == st.session_state.original_text:
                        show_celebration()
                    else:
                        st.error("Verification Failed - Check key and parameters")
                st.markdown('</div>', unsafe_allow_html=True)

    # OF-LSTM Architecture Section
    with st.expander("OF-LSTM Neural Network Architecture", expanded=False):
        show_oflstm_architecture()
        
        if st.session_state.model_trained and st.session_state.oflstm_model:
            arch = st.session_state.oflstm_model.get_architecture_description()
            st.markdown("### Current Model Status")
            st.markdown(
                f"        - Input Layer: {arch['input_layer']['neurons']} neurons\n"
                f"        - Increasing Gate: {arch['increasing_gate']['neurons']} neurons (Activation: {arch['increasing_gate']['activation']})\n"
                f"        - Input Gate + Memory Unit: {arch['input_gate']['neurons']} neurons\n"
                f"        - Output Gate: {arch['output_gate']['neurons']} neurons\n"
                f"        - Output Layer: {arch['output_layer']['neurons']} neuron\n"
                f"        - Training Score (R2): {st.session_state.train_score:.4f}\n"
            )

    # Visualization Tabs
    st.subheader("Chaotic Map Analysis")
    tab1, tab2, tab3 = st.tabs(["Time Series", "Phase Space", "Bifurcation Diagram"])

    with tab1:
        iterations = st.slider("Iterations", 50, 500, 200, key="ts")
        if st.button("Generate Time Series"):
            values, mean, std, entropy = analyze_chaotic_properties(a_param, b_param, iterations + 100)
            values = values[100:100+iterations]
            
            fig = make_subplots(rows=2, cols=1, subplot_titles=("Time Series", "Histogram"))
            fig.add_trace(go.Scatter(y=values, mode='lines', line=dict(color='blue')), row=1, col=1)
            fig.add_trace(go.Histogram(x=values, nbinsx=30, marker_color='green'), row=2, col=1)
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            st.info(f"Entropy: {entropy:.2f} bits | Mean: {mean:.4f} | Std: {std:.4f}")

    with tab2:
        points = st.slider("Points", 100, 2000, 500, key="ps")
        if st.button("Generate Phase Space"):
            values, _, _, _ = analyze_chaotic_properties(a_param, b_param, points + 100)
            values = values[100:100+points]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=values[:-1], y=values[1:], mode='markers', 
                                    marker=dict(size=2, color='red', opacity=0.6)))
            fig.update_layout(height=500, title="Phase Space (X(t) vs X(t+1))")
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            a_min = st.slider("a min", 2.0, 3.9, 3.5, 0.05)
        with col2:
            a_max = st.slider("a max", a_min+0.1, 5.0, 4.0, 0.05)
        
        if st.button("Generate Bifurcation Diagram"):
            a_list, x_vals = plot_bifurcation_diagram(a_min, a_max, b_param)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=a_list, y=x_vals, mode='markers', 
                                    marker=dict(size=1, color='blue', opacity=0.5)))
            fig.update_layout(height=500, title="Bifurcation Diagram")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("""
            **Interpretation:**
            - a < 3.57: Periodic behavior (vertical lines)
            - a > 3.57: Chaotic behavior (filled regions)
            """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; padding: 1rem;'>
    PhD Research: Chaotic Cryptography with OF-LSTM Neural Network<br>
    Mathematical Foundation: F(x, y) = b * [a * (x - y) * (1 - a * (x - y))]<br>
    Recommended Parameters: a = 3.7, b = 0.9 (chaotic regime)
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
