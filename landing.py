import streamlit as st

def landing():
    # Custom CSS to style the page
    st.markdown("""
        <style>
        .title {
            font-size: 2.3em;
            margin-top: 40px;
            color: #007BFF;
	    font-weight: bold;
        }
        .description {
            font-size: 1.2em;
            margin: 10px auto;
            color: #666;
            max-width: 800px;
        }
        .image {
            width: 100%;
            max-width: 300px;
            height: auto;
            margin: 20px auto;
        }
        .button-container {
            margin: 20px;
        }
        .button {
            display: inline-block;
            padding: 10px 20px;
            font-size: 1em;
            color: white;
            background-color: #007BFF;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }
        .button:hover {
            background-color: #0056b3;
        }
        .features {
            margin-top: 40px;
            text-align: left;
            display: inline-block;
            max-width: 800px;
            padding: 0 20px;
        }
        .features h2 {
            color: #007BFF;
            font-size: 2em;
            margin-bottom: 20px;
        }
        .features ul {
            list-style-type: none;
            padding: 0;
        }
        .features li {
            margin: 10px 0;
            font-size: 1.1em;
            line-height: 1.6;
        }
        .footer {
            margin-top: auto;
            padding: 20px;
            font-size: 0.9em;
            color: #999;
            background-color: #201c95;
        }
        .photo {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            margin: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    

    # HTML content
    st.markdown("""
        <div class="title">Welcome to Finance Expense Manager 💰</div>
        <div class="description">
            Manage your finances effortlessly. Track your income, monitor expenses, and optimize your budget with ease.
        </div>

     <img src="https://cdn.pixabay.com/photo/2020/08/03/10/00/cellphone-5459713_1280.png" class="image" alt="Finance Expense Manager Background">            <div class="features">
                <h2>Features</h2>
                <ul>
                    <li>💼 <strong>Track Income:</strong> Record all sources of income.</li>
                    <li>🧾 <strong>Monitor Expenses:</strong> Log daily expenses and categorize them.</li>
                    <li>📊 <strong>Visualize Data:</strong> Get insights into your spending habits with charts and graphs.</li>
                    <li>🎯 <strong>Budget Optimization:</strong> Set budget goals and track progress.</li>
                    <li>🔒 <strong>Secure:</strong> Your data is stored securely.</li>
                </ul>
            </div>
        </div>
        <div class="footer">
            © 2024 Finance Expense Manager. All rights reserved.
        </div>
    """, unsafe_allow_html=True)

    
