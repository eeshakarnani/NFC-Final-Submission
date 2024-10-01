import streamlit as st
from main import FamilyExpenseTracker
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from pathlib import Path
import google.generativeai as genai
from login import login
from signup import signup
from landing import landing
from stock import stock
import PIL.Image
import re
from datetime import datetime
#import fitz   PyMuPDF for PDF processing
from pypdf import PdfReader

# Create a file uploader widget for PDF
css = """
<style>
    .big-button .stButton>button {
        font-size:20px !important;  /* Adjust the font size as needed */
        padding:10px 20px !important;  /* Adjust the padding for button size */
    }
</style>
"""

genai.configure(api_key="")

model = genai.GenerativeModel('gemini-1.5-flash')

# Streamlit configuration
st.set_page_config(page_title="AI-Based Finance Tracker", page_icon="💰")
st.title("")  # Clear the default title

# Path Settings
current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "styles" / "main.css"

with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

# Create a session state object
session_state = st.session_state
# Ensure session state variables for login and signup exist
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "signup" not in st.session_state:
    st.session_state["signup"] = False
# Check if the 'expense_tracker' object exists in the session state
if "expense_tracker" not in session_state:
    # If not, create and initialize it
    session_state.expense_tracker = FamilyExpenseTracker()

# Navigation bar setup
selected_page = option_menu(
    menu_title="Main Menu",  # Required
    options=["Landing", "Login", "Signup", "Dashboard", "Stock Analysis"],  # Required
    icons=["house", "door-open", "file-earmark-person", "graph-up"],  # Optional
    menu_icon="cast",  # Optional
    default_index=0,  # Optional
    orientation="horizontal",  # Can be "horizontal" or "vertical"
)

# Page navigation based on selected option
if selected_page == "Landing":
    landing()
elif selected_page == "Login":
    if st.session_state["logged_in"]:
        st.session_state.page = "Dashboard"
    else:
        login()
elif selected_page == "Signup":
    signup()
elif selected_page == "Stock Analysis":
    stock()
elif selected_page == "Dashboard":
        # Main dashboard code starts here
        st.markdown(
                    '<h1 style="text-align: center;">AI-Based Finance Tracker</h1>',
                     unsafe_allow_html=True,
                    )

        selected = option_menu(
            menu_title=None,
            options=["Data Entry", "Data Overview", "Data Visualization"],
            icons=["pencil-fill", "clipboard2-data", "bar-chart-fill"],
            orientation="horizontal",
        )



        # Access the 'expense_tracker' object from session state
        expense_tracker = session_state.expense_tracker

        if selected == "Data Entry":
            st.header("Enter your name")
            with st.expander("Enter your name"):
                # Sidebar for adding family members
                member_name = st.text_input("Name").title()
                earning_status = st.checkbox("Earning Status")
                if earning_status:
                    earnings = st.number_input("Earnings", value=1, min_value=1)
                else:
                    earnings = 0

                if st.button("Add Member"):
                    try:
                        # Check if family member exists
                        member = [
                            member
                            for member in expense_tracker.members
                            if member.name == member_name
                        ]
                        # If not exist add family member
                        if not member:
                            expense_tracker.add_family_member(
                                member_name, earning_status, earnings
                            )
                            st.success("Member added successfully!")
                        # Else, update it
                        else:
                            expense_tracker.update_family_member(
                                member[0], earning_status, earnings
                            )
                            st.success("Member updated successfully!")
                    except ValueError as e:
                        st.error(str(e))

                
            # Sidebar for adding expenses
            st.header("Add Expenses")
            with st.expander("Add Expenses"):
                expense_category = st.selectbox(
                    "Category",
                    (
                        "Housing",
                        "Food",
                        "Transportation",
                        "Entertainment",
                        "Education",
                        "Medical",
                        "Investment",
                        "Miscellaneous",
                    ),
                )
                expense_description = st.text_input("Description (optional)").title()
                expense_value = st.number_input("Value", min_value=0)
                expense_date = st.date_input("Date", value="today")

                if st.button("Add Expense"):
                    try:
                        # Add the expense
                        expense_tracker.merge_similar_category(
                            expense_value, expense_category, expense_description, expense_date
                        )
                        st.success("Expense added successfully!")
                    except ValueError as e:
                        st.error(str(e))
            st.header("Add Transaction Message")
            expense_text = st.text_input("Enter transaction message")
            st.write(expense_text)
            pattern = r"INR\s([\d,]+\.\d{2})\s+spent\s+on\s+.+\s+on\s+(\d{2}-\w{3}-\d{4})\s+at\s+(.+)\."
            match = re.search(pattern, expense_text)
            months_dict = {
                            'JAN': '01',
                            'FEB': '02',
                            'MAR': '03',
                            'APR': '04',
                            'MAY': '05',
                            'JUN': '06',
                            'JUL': '07',
                            'AUG': '08',
                            'SEP': '09',
                            'OCT': '10',
                            'NOV': '11',
                            'DEC': '12'
                        }
            if match:
                expense_value = float(match.group(1))
                date = match.group(2)
                for month_abbr, month_num in months_dict.items():
                    date = re.sub(rf'\b{month_abbr}\b', month_num, date, flags=re.IGNORECASE)
                expense_date = datetime.strptime(date, "%d-%m-%Y").date()
                #expense_date = date
                item = match.group(3)
                if item in ['MC DONALDS', 'ZOMATOCOM', 'CAMY WAFER INDIA PVT L', 'ZOMATO LIMITED', 'The Little Easy by Dha']:
                    expense_category = 'Food'
                elif item in ['UBER INDIA SYSTE PVT LTD', 'OLA']:
                    expense_category = 'Transportation'
                elif item in ['NOBLE PLUS', 'AURO SKIN CLINIC AND P']:
                    expense_category = 'Medical'
                expense_description = 'NA'
                if st.button("Add Transaction"):
                    try:
                        # Add the expense
                        expense_tracker.merge_similar_category(
                            expense_value, expense_category, expense_description, expense_date
                        )
                        st.success("Expense added successfully!")
                    except ValueError as e:
                        st.error(str(e))
            uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
            if uploaded_file is not None:
                reader = PdfReader(uploaded_file)
                page = reader.pages[0]
                text = page.extract_text()
                lines = text.split('\n')
                lines = lines[2:]
                data_list = []
                for line in lines:
                    info_list = line.split(' ')
                    info_list[1] = info_list[1].replace('Child-Related', 'Education')
                    info_list[2] = info_list[2].replace(',','')
                    expense_value = float(info_list[2])
                    expense_category = info_list[1]
                    expense_description = info_list[3]
                    expense_date = datetime.strptime(info_list[0], "%Y-%m-%d").date()
                    try:
                        # Add the expense
                        expense_tracker.merge_similar_category(
                            expense_value, expense_category, expense_description, expense_date
                        )
                    except ValueError as e:
                        st.error(str(e))
                st.success("Expenses added successfully!")

        elif selected == "Data Overview":
            # Display family members
            if not expense_tracker.members:
                st.info(
                    "Get started by entering data from the Data Entry Tab"
                )
            else:
                st.header("Your Expenses")
                (
                    name_column,
                    earning_status_column,
                    earnings_column,
                    family_delete_column,
                ) = st.columns(4)
                name_column.write("**Name**")
                earning_status_column.write("**Earning status**")
                earnings_column.write("**Earnings**")
                family_delete_column.write("**Action**")

                for member in expense_tracker.members:
                    name_column.write(member.name)
                    earning_status_column.write(
                        "Earning" if member.earning_status else "Not Earning"
                    )
                    earnings_column.write(member.earnings)

                    if family_delete_column.button(f"Delete {member.name}"):
                        expense_tracker.delete_family_member(member)
                        st.rerun()

                # Display expenses
                st.header("Expenses")
                if not expense_tracker.expense_list:
                    st.info(
                    "Currently, no expenses have been added. Get started by clicking the 'Add Expenses' from the Data Entry Tab"
                )
                else:
                    (
                        value_column,
                        category_column,
                        description_column,
                        date_column,
                        expense_delete_column,
                    ) = st.columns(5)
                    value_column.write("**Value**")
                    category_column.write("**Category**")
                    description_column.write("**Description**")
                    date_column.write("**Date**")
                    expense_delete_column.write("**Delete**")

                    for expense in expense_tracker.expense_list:
                        value_column.write(expense.value)
                        category_column.write(expense.category)
                        description_column.write(expense.description)
                        date_column.write(expense.date)

                        st.markdown(css, unsafe_allow_html=True)
                        if expense_delete_column.button(f"Delete {expense.category}"):
                            expense_tracker.delete_expense(expense)
                            st.rerun()

                total_earnings = expense_tracker.calculate_total_earnings()               # Calculate total earnings
                total_expenditure = expense_tracker.calculate_total_expenditure()         # Calculate total expenditure
                remaining_balance = total_earnings - total_expenditure                    # Calculate remaining balance
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Earnings", f"{total_earnings}")          # Display total earnings
                col2.metric("Total Expenditure", f"{total_expenditure}")    # Display total expenditure 
                col3.metric("Remaining Balance", f"{remaining_balance}")    # Display remaining balance 

        elif selected == "Data Visualization":
            # Create a list of expenses and their values
            expense_data = [
                (expense.category, expense.value) for expense in expense_tracker.expense_list
            ]
            if expense_data:
                # Calculate the percentage of expenses for the pie chart
                expenses = [data[0] for data in expense_data]
                values = [data[1] for data in expense_data]
                total = sum(values)
                percentages = [(value / total) * 100 for value in values]

                col1, col2= st.columns(2)

        # Create and display the pie chart in the first column
                with col1:
                    fig1, ax1 = plt.subplots(figsize=(3, 3), dpi=300)
                    ax1.pie(
                        percentages,
                        labels=expenses,
                        autopct="%1.1f%%",
                        startangle=140,
                        textprops={"fontsize": 6, "color": "black"},
                    )
                    ax1.set_title("Expense Distribution", fontsize=12, color="white")
                    fig1.savefig("piechart.png")
                    ax1.pie(
                        percentages,
                        labels=expenses,
                        autopct="%1.1f%%",
                        startangle=140,
                        textprops={"fontsize": 6, "color": "white"},
                    )
                    fig1.patch.set_facecolor("none")
                    ax1.set_facecolor('none')
                    st.pyplot(fig1)
                    img = PIL.Image.open("piechart.png")
                    response = model.generate_content(["The given image is a graph of my expenses. Analyse the trends.",img])
                    st.write("""**Analysis**""")
                    st.write(response.text)

        # Create and display the bar graph in the second column
                with col2:
                    fig2, ax2 = plt.subplots(figsize=(5, 5), dpi=300)
                    ax2.bar(expenses, values, color='skyblue')
                    ax2.set_title("Expense Distribution", fontsize=24, color='white')
                    #st.write("""""")
                    ax2.set_xlabel("Expense Categories", color='black')
                    ax2.set_ylabel("Amount", color='black')
                    
                    # Set x-tick and y-tick labels to white
                    ax2.tick_params(axis='x', colors='black')
                    ax2.tick_params(axis='y', colors='black')
                    fig2.savefig("barchart.png")
                    # Set axis labels with white text color
                    ax2.set_xlabel("Expense Categories", color='white')
                    ax2.set_ylabel("Amount", color='white')
                    
                    # Set x-tick and y-tick labels to white
                    ax2.tick_params(axis='x', colors='white')
                    ax2.tick_params(axis='y', colors='white')
                    
                    # Make the figure background transparent
                    fig2.patch.set_facecolor('none')
                    ax2.set_facecolor('none')
                    #st.write(""" **Expenses Bar Graph**""")
                    st.pyplot(fig2)
                    img = PIL.Image.open("barchart.png")
                    response = model.generate_content(["The given image is a graph of my expenses. Analyse the trends.",img])
                    st.write("""**Analysis**""")
                    st.write(response.text)
                    

        # Space for text under the visualizations
                img = PIL.Image.open("piechart.png")
                response = model.generate_content(["The given image is a graph of my expenses. Give me tips on how i can save money",img])
                st.write("""**TIPS TO SAVE MONEY**""")
                st.write(response.text)
                #bargraph

            else:
                st.info(
                    "Start by adding family members to track your expenses together! Currently, no members have been added. Get started by clicking the 'Add Member' from the Data Entry Tab."
                )
