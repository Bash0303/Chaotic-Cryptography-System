import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hashlib
import binascii
import time
import os

# Set page configuration
st.set_page_config(
    page_title="Chaotic Cryptography System",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3D58;
        text-align: center;
        padding: 1rem;
    }
    .math-formula {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: monospace;
        font-size: 1.2rem;
        text-align: center;
    }
    .result-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
    .encrypted-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        font-family: monospace;
        font-size: 0.9rem;
        word-break: break-all;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #28a745;
        text-align: center;
        animation: pulse 0.5s ease-in-out;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    .celebration {
        font-size: 1.5rem;
        font-weight: bold;
        color: #28a745;
        text-align: center;
        padding: 1rem;
        animation: glow 1s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from { text-shadow: 0 0 5px #28a745; }
        to { text-shadow: 0 0 20px #28a745; }
    }
</style>
""", unsafe_allow_html=True)

def chaotic_map_int(x, y, a, b, precision=10000):
    """
    Chaotic map using integer arithmetic to avoid floating point issues
    x, y are integers in range [0, precision]
    F(x, y) = b * [a * (x - y) * (1 - a * (x - y))]
    """
    x_f = x / precision
    y_f = y / precision
    diff = x_f - y_f
    inner = a * diff
    inner = max(-2, min(2, inner))
    logistic = inner * (1 - inner)
    result = b * logistic
    result_int = int((result + 1) / 2 * precision)
    result_int = max(0, min(precision, result_int))
    return result_int

def bytes_to_int_list(byte_data):
    """Convert bytes to list of integers (0-255)"""
    return list(byte_data)

def int_list_to_bytes(int_list):
    """Convert list of integers back to bytes"""
    return bytes([max(0, min(255, int(x))) for x in int_list])

def encrypt_bytes(plain_bytes, key, a, b):
    """Encrypt bytes using chaotic map with integer arithmetic"""
    if not plain_bytes:
        return b""
    
    key_hash = hashlib.sha256(key.encode()).hexdigest()
    x0 = int(key_hash[:8], 16) % 10000
    y0 = int(key_hash[8:16], 16) % 10000
    
    plain_ints = bytes_to_int_list(plain_bytes)
    x, y = x0, y0
    
    for _ in range(100):
        x = chaotic_map_int(x, y, a, b)
        y = chaotic_map_int(y, x, a, b)
    
    encrypted_ints = []
    for p in plain_ints:
        x = chaotic_map_int(x, y, a, b)
        y = chaotic_map_int(y, x, a, b)
        chaotic_val = x % 256
        encrypted_val = p ^ chaotic_val
        encrypted_ints.append(encrypted_val)
    
    return int_list_to_bytes(encrypted_ints)

def decrypt_bytes(encrypted_bytes, key, a, b):
    """Decrypt bytes using chaotic map with integer arithmetic"""
    if not encrypted_bytes:
        return b""
    
    key_hash = hashlib.sha256(key.encode()).hexdigest()
    x0 = int(key_hash[:8], 16) % 10000
    y0 = int(key_hash[8:16], 16) % 10000
    
    encrypted_ints = bytes_to_int_list(encrypted_bytes)
    x, y = x0, y0
    
    for _ in range(100):
        x = chaotic_map_int(x, y, a, b)
        y = chaotic_map_int(y, x, a, b)
    
    decrypted_ints = []
    for e in encrypted_ints:
        x = chaotic_map_int(x, y, a, b)
        y = chaotic_map_int(y, x, a, b)
        chaotic_val = x % 256
        decrypted_val = e ^ chaotic_val
        decrypted_ints.append(decrypted_val)
    
    return int_list_to_bytes(decrypted_ints)

def encrypt_text(plaintext, key, a, b):
    """Encrypt text and return hex representation"""
    try:
        plain_bytes = plaintext.encode('utf-8')
        encrypted_bytes = encrypt_bytes(plain_bytes, key, a, b)
        hex_string = binascii.hexlify(encrypted_bytes).decode('ascii')
        return hex_string
    except Exception as e:
        st.error(f"Encryption failed: {e}")
        return ""

def decrypt_text(hex_string, key, a, b):
    """Decrypt from hex representation back to text"""
    try:
        encrypted_bytes = binascii.unhexlify(hex_string)
        decrypted_bytes = decrypt_bytes(encrypted_bytes, key, a, b)
        decrypted_text = decrypted_bytes.decode('utf-8', errors='replace')
        return decrypted_text
    except Exception as e:
        return f"Decryption error: {str(e)}"

def analyze_chaotic_properties(a, b, iterations=1000):
    """Analyze chaotic properties of the map"""
    x, y = 5000, 3000
    values = []
    
    for i in range(iterations):
        x = chaotic_map_int(x, y, a, b)
        y = chaotic_map_int(y, x, a, b)
        values.append(x / 10000)
    
    values_array = np.array(values)
    x_mean = np.mean(values_array)
    x_std = np.std(values_array)
    
    hist, _ = np.histogram(values_array, bins=50)
    hist = hist[hist > 0]
    probs = hist / len(values_array)
    entropy = -np.sum(probs * np.log2(probs + 1e-10))
    
    return values, x_mean, x_std, entropy

def plot_bifurcation_diagram(a_min, a_max, b, steps=100):
    """Generate bifurcation diagram"""
    a_values = np.linspace(a_min, a_max, steps)
    x_values = []
    a_list = []
    
    for a in a_values:
        x, y = 5000, 3000
        for _ in range(200):
            x = chaotic_map_int(x, y, a, b)
            y = chaotic_map_int(y, x, a, b)
        for _ in range(100):
            x = chaotic_map_int(x, y, a, b)
            y = chaotic_map_int(y, x, a, b)
            x_values.append(x / 10000)
            a_list.append(a)
    
    return a_list, x_values

def show_celebration():
    """Show celebration effects"""
    celebration_placeholder = st.empty()
    
    celebration_html = '''
    <div class="celebration">
        ⭐✨🎉 PERFECT DECRYPTION! 🎉✨⭐<br>
        🔐 MESSAGE SUCCESSFULLY RECOVERED! 🔐<br>
        🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟
    </div>
    '''
    celebration_placeholder.markdown(celebration_html, unsafe_allow_html=True)
    st.balloons()
    st.snow()
    time.sleep(3)
    celebration_placeholder.empty()

def main():
    # Header
    st.markdown('<h1 class="main-header">🔐 Chaotic Cryptography System</h1>', 
                unsafe_allow_html=True)
    
    st.markdown('### Advanced Encryption Using Chaotic Maps')
    st.markdown('This system implements the chaotic map function:')
    st.markdown('<div class="math-formula">F(x, y) = b x [a x (x - y) x (1 - a x (x - y))]</div>', 
                unsafe_allow_html=True)
    st.markdown('Where:')
    st.markdown('- **x, y in [0, 1]** (input values)')
    st.markdown('- **a in [0, infinity)** (bifurcation parameter)')
    st.markdown('- **b in [0, infinity)** (scaling parameter)')
    
    # Sidebar for parameters
    st.sidebar.header("⚙️ Encryption Parameters")
    
    a_param = st.sidebar.slider(
        "Parameter a (bifurcation)",
        min_value=0.0,
        max_value=5.0,
        value=3.7,
        step=0.05,
        help="Values > 3.57 produce chaotic behavior"
    )
    
    b_param = st.sidebar.slider(
        "Parameter b (scaling)",
        min_value=0.0,
        max_value=2.0,
        value=0.9,
        step=0.05,
        help="Scaling factor"
    )
    
    # Key input
    st.sidebar.header("🔑 Encryption Key")
    encryption_key = st.sidebar.text_input(
        "Enter your secret key",
        type="password",
        value="my_secret_key_2026",
        help="Must use the SAME key for encryption and decryption"
    )
    
    # Analysis section
    st.sidebar.header("📊 System Analysis")
    if st.sidebar.button("Analyze Chaotic Properties"):
        with st.sidebar:
            st.info("Analyzing chaotic behavior...")
            values, x_mean, x_std, entropy = analyze_chaotic_properties(a_param, b_param, 500)
            
            st.metric("Mean Value", f"{x_mean:.4f}")
            st.metric("Standard Deviation", f"{x_std:.4f}")
            st.metric("Shannon Entropy (bits)", f"{entropy:.2f}")
            
            if entropy > 3.5:
                st.success("✅ System shows good chaotic behavior")
            else:
                st.warning("⚠️ System may not be fully chaotic")
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Encryption")
        input_text = st.text_area(
            "Enter text to encrypt:",
            height=150,
            value="Hello World",
            key="input_text"
        )
        
        if st.button("🔒 Encrypt Text", type="primary", use_container_width=True):
            if input_text:
                with st.spinner("Encrypting..."):
                    hex_encrypted = encrypt_text(input_text, encryption_key, a_param, b_param)
                    
                    if hex_encrypted:
                        st.session_state.encrypted_hex = hex_encrypted
                        st.session_state.original_text = input_text
                        
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.success("✅ Encryption Complete!")
                        
                        st.markdown('<div class="encrypted-box">', unsafe_allow_html=True)
                        st.markdown("**📋 Encrypted Text (HEX format - copy this exactly):**")
                        st.code(hex_encrypted, language="text")
                        st.caption("✅ This HEX string is safe to copy and will work for decryption")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error("❌ Encryption failed. Please try again.")
            else:
                st.warning("⚠️ Please enter text to encrypt.")
    
    with col2:
        st.subheader("🔓 Decryption")
        
        default_hex = st.session_state.get('encrypted_hex', '')
        encrypted_input = st.text_area(
            "Enter HEX encrypted text to decrypt:",
            height=150,
            value=default_hex,
            placeholder="Paste the HEX encrypted text here...",
            help="Paste the exact HEX string from encryption"
        )
        
        if st.button("🔓 Decrypt Text", type="primary", use_container_width=True):
            if encrypted_input:
                with st.spinner("Decrypting..."):
                    decrypted_text = decrypt_text(encrypted_input, encryption_key, a_param, b_param)
                    
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.success("✅ Decryption Complete!")
                    st.text_area("Decrypted Output:", decrypted_text, height=100, key="decrypted_output")
                    
                    if 'original_text' in st.session_state and st.session_state.original_text:
                        if decrypted_text == st.session_state.original_text:
                            show_celebration()
                            
                            st.markdown("""
                            <div class="success-box">
                                <h2>🎉 PERFECT DECRYPTION! 🎉</h2>
                                <h3>✨ Decrypted text matches the original message! ✨</h3>
                                <p>🔐 The chaotic cryptography system is working perfectly! 🔐</p>
                                <p>⭐ ⭐ ⭐ ⭐ ⭐</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error("❌ VERIFICATION FAILED")
                            st.warning("Make sure you're using the EXACT SAME:")
                            st.info(f"🔑 Secret key: '{encryption_key}'")
                            st.info(f"📊 Parameter a: {a_param}")
                            st.info(f"📈 Parameter b: {b_param}")
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("⚠️ Please enter encrypted text to decrypt.")
    
    # Visualization Section
    st.subheader("📈 Chaotic Map Visualization")
    
    tab1, tab2, tab3 = st.tabs(["📉 Time Series", "🌀 Phase Space", "📊 Bifurcation Diagram"])
    
    with tab1:
        st.markdown("### Time Series Analysis")
        iterations = st.slider("Number of iterations", 50, 500, 200, key="ts_iter")
        
        if st.button("Generate Time Series", key="ts_btn"):
            values, _, _, entropy = analyze_chaotic_properties(a_param, b_param, iterations + 100)
            values = values[100:100 + iterations]
            
            fig = make_subplots(rows=2, cols=1, 
                               subplot_titles=("Chaotic Time Series", "Distribution Histogram"))
            
            fig.add_trace(go.Scatter(y=values, mode='lines', name='Chaotic Signal', 
                                    line=dict(color='blue', width=1)), row=1, col=1)
            
            fig.add_trace(go.Histogram(x=values, nbinsx=30, name='Distribution', 
                                      marker_color='green'), row=2, col=1)
            
            fig.update_layout(height=600, title_text=f"Chaotic System Analysis (Entropy: {entropy:.2f} bits)")
            fig.update_xaxes(title_text="Time Step", row=1, col=1)
            fig.update_yaxes(title_text="Value", row=1, col=1)
            fig.update_xaxes(title_text="Value", row=2, col=1)
            fig.update_yaxes(title_text="Frequency", row=2, col=1)
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.info(f"📊 Statistics: Mean = {np.mean(values):.4f}, Std = {np.std(values):.4f}, Entropy = {entropy:.2f} bits")
    
    with tab2:
        st.markdown("### Phase Space Plot")
        points = st.slider("Number of points", 100, 2000, 500, key="ps_points")
        
        if st.button("Generate Phase Space", key="ps_btn"):
            values, _, _, _ = analyze_chaotic_properties(a_param, b_param, points + 100)
            values = values[100:100 + points]
            
            x_phase = values[:-1]
            y_phase = values[1:]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x_phase, y=y_phase, mode='markers', 
                                    marker=dict(size=2, color='red', opacity=0.6),
                                    name='Phase Space'))
            
            fig.update_layout(title="Phase Space Plot (Attractor)",
                             xaxis_title="X(t)",
                             yaxis_title="X(t+1)",
                             height=500)
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.info("🌀 The phase space plot shows the system's attractor. A filled, complex pattern indicates chaos.")
    
    with tab3:
        st.markdown("### Bifurcation Diagram")
        col1, col2 = st.columns(2)
        with col1:
            a_min = st.slider("a minimum", 2.0, 3.9, 3.5, 0.05, key="bd_min")
        with col2:
            a_max = st.slider("a maximum", a_min + 0.1, 5.0, 4.0, 0.05, key="bd_max")
        
        if st.button("Generate Bifurcation Diagram", key="bd_btn"):
            with st.spinner("Generating bifurcation diagram (this may take a moment)..."):
                a_list, x_values = plot_bifurcation_diagram(a_min, a_max, b_param, steps=100)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=a_list, y=x_values, mode='markers', 
                                        marker=dict(size=1, color='blue', opacity=0.5),
                                        name='Bifurcation'))
                
                fig.update_layout(title="Bifurcation Diagram",
                                 xaxis_title="Parameter a",
                                 yaxis_title="X Values",
                                 height=500)
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("**Understanding the Bifurcation Diagram:**")
                st.markdown("- **a < 3.57**: Periodic behavior (few vertical lines)")
                st.markdown("- **a > 3.57**: Chaotic behavior (filled regions)")
                st.markdown("- The transition shows the 'route to chaos'")
    
    # Documentation for Supervisor
    with st.expander("📚 Documentation for Supervisor"):
        st.markdown("### System Overview")
        st.markdown("This cryptographic system uses a chaotic map to generate a pseudorandom keystream for XOR encryption.")
        
        st.markdown("### Mathematical Foundation")
        st.markdown("**The Chaotic Map:**")
        st.code("F(x, y) = b x [a x (x - y) x (1 - a x (x - y))]", language="text")
        
        st.markdown("### Deployment Information")
        st.markdown("This application is deployed on Render and accessible via web browser.")
        st.markdown("- **Platform**: Render.com")
        st.markdown("- **Framework**: Streamlit")
        st.markdown("- **Python Version**: 3.9")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; padding: 1rem;'>
    🎓 PhD Research Project - Chaotic Cryptography for Text Encryption<br>
    📐 Mathematical Foundation: F(x, y) = b x [a x (x - y) x (1 - a x (x - y))]<br>
    ⭐ Recommended Parameters: a = 3.7, b = 0.9 (chaotic regime)
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()