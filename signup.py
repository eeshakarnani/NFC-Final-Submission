import streamlit as st
from streamlit_option_menu import option_menu

# Simulate the signup function
def signup():
    # CSS for styling
    st.markdown("""
    <style>
    /* Hide Streamlit Style */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

   /* Page Background Changed to White */

[data-testid="stAppViewContainer"] {
    background-color: #444CF755;  /* White background */
    opacity: 1;  /* Full opacity */
    background-image: /*repeating-radial-gradient(circle at 0 0, transparent 0, #000080 10px),*/ repeating-linear-gradient(#ADD8E6, #ADD8E6);}




    /* Signup Page Styles */
    .signup-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh; /* Full height for centering */
    }

    .signup-title {
        font-size: 2em;
        color: #ffffff; /* White text for contrast */
        margin-bottom: 20px;
    }

    input[type="text"], input[type="email"], input[type="password"] {
        width: 300px; /* Fixed width for input fields */
        padding: 10px;
        margin-bottom: 15px;
        border: 1px solid #ffffff; /* White border */
        border-radius: 5px;
        background-color: rgba(255, 255, 255, 0.1); /* Slightly transparent background */
        color: #ffffff; /* White text color */
    }

    /* Eye Icon Positioning */
    .password-container {
        position: relative; /* Positioning context for absolute elements */
        width: 300px; /* Match input field width */
    }

    .password-input {
        width: 100%; /* Full width */
        padding-right: 30px; /* Space for the eye icon */
    }

    .eye-icon {
        position: absolute; /* Absolute positioning within the container */
        right: 10px; /* Adjust as needed */
        top: 50%; /* Center vertically */
        transform: translateY(-50%); /* Center vertically */
        cursor: pointer; /* Pointer cursor for interaction */
        color: #ffffff; /* White icon color */
    }

    button {
        background-color: #ffffff; /* Button background */
        color: #000000; /* Black text for button */
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1em;
        transition: background-color 0.3s ease;
    }

    button:hover {
        background-color: #f0f0f0; /* Light grey on hover */
    }

    /* Error Message Styles */
    .stError {
        color: red; /* Red text for error messages */
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("Signup", anchor="signup")

    name = st.text_input("Full Name", key="signup_name")
    email = st.text_input("Email", key="signup_email")
    username = st.text_input("Username", key="signup_username")
    
    # Password input with eye icon for both password and confirm password
    password_container = st.container()
    password_container.markdown(
        """
        <div class="password-container">
            <input type="password" id="password" class="password-input" placeholder="Password" />
            <span class="eye-icon" onclick="togglePasswordVisibility('password')" title="Toggle Password Visibility">
                👁️
            </span>
        </div>
        """, unsafe_allow_html=True
    )
    
    confirm_password_container = st.container()
    confirm_password_container.markdown(
        """
        <div class="password-container">
            <input type="password" id="confirm_password" class="password-input" placeholder="Re-enter Password" />
            <span class="eye-icon" onclick="togglePasswordVisibility('confirm_password')" title="Toggle Password Visibility">
                👁️
            </span>
        </div>
        <script>
            function togglePasswordVisibility(id) {
                const passwordInput = document.getElementById(id);
                if (passwordInput.type === 'password') {
                    passwordInput.type = 'text';
                } else {
                    passwordInput.type = 'password';
                }
            }
        </script>
        """, unsafe_allow_html=True
    )
    
    if st.button("Signup"):
        password = st.session_state.get("password")
        confirm_password = st.session_state.get("confirm_password")
        
        if password != confirm_password:
            st.error("Passwords do not match")
        elif len(password) < 8:
            st.error("Password must be at least 8 characters")
        elif not name or not email or not username:
            st.error("Please fill in all the fields")
        else:
            st.success("Signup successful!")
            # Here, you would save the signup data and proceed to the login page

# Main application logic
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    signup()
else:
    # Dashboard content
    st.title("Family Expense Tracker Dashboard")
    st.write("Welcome to the dashboard!")
    
    selected = option_menu(
        menu_title=None,
        options=["Data Entry", "Data Overview", "Data Visualization"],
        icons=["pencil-fill", "clipboard2-data", "bar-chart-fill"],
        orientation="horizontal",
    )
    
    if selected == "Data Entry":
        st.write("Data Entry Page")
        # Data Entry logic here
    elif selected == "Data Overview":
        st.write("Data Overview Page")
        # Data Overview logic here
    elif selected == "Data Visualization":
        st.write("Data Visualization Page")
        # Data Visualization logic here