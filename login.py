import streamlit as st
from streamlit_option_menu import option_menu  # Ensure this import is included


# Simulate the login function
def login():
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
        background-color: #ffffff;  /* White background */
        opacity: 1;  /* Full opacity */
        background-image: none;  /* Remove any background image */
    }

    /* Login Page Styles */
    .login-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh; /* Full height for centering */
    }

    .login-title {
        font-size: 2em;
        color: #ffffff; /* White text for contrast */
        margin-bottom: 20px;
    }

    input[type="text"], input[type="password"] {
        width: 300px; /* Fixed width for input fields */
        padding: 10px;
        margin-bottom: 15px;
        border: 1px solid #000000; /* Black border */
        border-radius: 5px;
        background-color: #ffffff; /* White background */
        color: #000000; /* Black text color */
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
        color: #000000; /* Black icon color */
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

    st.title("Login", anchor="login")
    username = st.text_input("Username")
    
    # Password input with eye icon
    password_container = st.container()
    password_container.markdown(
        """
        <div class="password-container">
            <input type="password" id="password" class="password-input" placeholder="Password" />
            <span class="eye-icon" onclick="togglePasswordVisibility()" title="Toggle Password Visibility">
                👁️
            </span>
        </div>
        <script>
            function togglePasswordVisibility() {
                const passwordInput = document.getElementById('password');
                if (passwordInput.type === 'password') {
                    passwordInput.type = 'text';
                } else {
                    passwordInput.type = 'password';
                }
            }
        </script>
        """, unsafe_allow_html=True
    )
    
    if st.button("Login"):
        password = st.session_state.get("password")  # Store password state
        if username == "user" and password == "pass":  # Replace with actual login logic
            st.session_state["logged_in"] = True
            st.experimental_rerun()  # Refresh the page to navigate to the dashboard
        else:
            st.error("Invalid username or password")

# Main application logic
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
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