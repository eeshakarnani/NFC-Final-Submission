import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import streamlit as st
from streamlit_option_menu import option_menu
import concurrent.futures

sectors = {
    "Railway": [
        'IRCTC.NS', 'TITAN.NS', 'L&T.NS', 'BEML.NS', 'RVNL.NS', 
        'CONCOR.NS', 'RAILTEL.NS', 'GMRINFRA.NS', 'NCC.NS', 
        'IRBINFRA.NS', 'APOLLOHOSP.NS'
    ],
    "Banks": [
        'HDFCBANK.NS', 'ICICIBANK.NS', 'KOTAKBANK.NS', 'SBIN.NS', 
        'AXISBANK.NS', 'PNB.NS', 'YESBANK.NS', 'IDFCFIRSTBANK.NS', 
        'BANDHANBANK.NS', 'INDUSINDBK.NS', 'FEDERALBNK.NS', 
        'BANKBARODA.NS', 'AUBANK.NS'
    ],
    "Defense": [
        'BEL.NS', 'HAL.NS', 'BEML.NS', 'MTARTECH.NS', 'SOLARINDS.NS', 
        'MAZDOCK.NS', 'COCHINSHIP.NS', 'ALKEM.NS', 'AIAENG.NS', 
        'HIL.NS', 'SIEMENS.NS'
    ],
    "Renewable Energy": [
        'TATAPOWER.NS', 'ADANIGREEN.NS', 'NHPC.NS', 'RENUKA.NS', 
        'BOROSIL.NS', 'SUZLON.NS', 'INDIAGLYCO.NS', 'JSWENERGY.NS', 
        'NTPC.NS', 'NLCINDIA.NS', 'GREENPLY.NS', 'SJVN.NS'
    ],
    "Fertilizers": [
        'RALLIS.NS', 'NFL.NS', 'GSFC.NS', 'CHAMBLFERT.NS', 'ZUARI.NS', 
        'GNFC.NS', 'RCF.NS', 'FACT.NS', 'COROMANDEL.NS', 
        'SUDARSCHEM.NS', 'KRBL.NS', 'MUNJALAUSTR.NS'
    ],
    "Automobile": [
        'MARUTI.NS', 'TATAMOTORS.NS', 'MAHINDRA.NS', 'HEROMOTOCORP.NS', 
        'EICHERMOT.NS', 'ASHOKLEY.NS', 'TVS.NS', 'BAJAJ-AUTO.NS', 
        'MOTHERSUMI.NS', 'GLOBUSSPR.NS', 'JBMAUTO.NS', 'HERO.NS'
    ],
    "Information Technology": [
        'TCS.NS', 'INFY.NS', 'HCLTECH.NS', 'WIPRO.NS', 'TECHM.NS', 
        'LTI.NS', 'MINDTREE.NS', 'COFORGE.NS', 'CSE.NS', 'NIITTECH.NS', 
        'KPITTECH.NS', 'TATAELXSI.NS', 'HSTGLOBAL.NS'
    ],
    "Pharmaceuticals": [
        'SUNPHARMA.NS', 'DRREDDY.NS', 'CIPLA.NS', 'AUROPHARMA.NS', 
        'LUPIN.NS', 'DIVISLAB.NS', 'GLAND.NS', 'IPCALAB.NS', 
        'JUBILANT.NS', 'ALKEM.NS', 'TORNTPHARM.NS'
    ],
    "Consumer Goods": [
        'HINDUNILVR.NS', 'ITC.NS', 'NESTLEIND.NS', 'DABUR.NS', 
        'GODREJCP.NS', 'MARICO.NS', 'COLPAL.NS', 'EMAMILTD.NS', 
        'HAVELLS.NS', 'PIDILITIND.NS', 'BRITANNIA.NS', 'JUBLFOOD.NS'
    ],
    "Energy": [
        'ONGC.NS', 'OIL.NS', 'RELIANCE.NS', 'PETRONET.NS', 'GAIL.NS', 
        'IOC.NS', 'BPCL.NS', 'CASTROLIND.NS', 'HINDPETRO.NS', 
        'ADANIPORTS.NS', 'TATAPOWER.NS', 'SAIL.NS'
    ],
    "Telecommunications": [
        'BHARTIARTL.NS', 'RELIANCE.NS', 'IDEA.NS', 'MTNL.NS', 
        'VODAFONEIDEA.NS', 'GTPL.NS', 'HATHWAY.NS', 'TATAMETALIKS.NS'
    ],
    "Metals and Mining": [
        'TATASTEEL.NS', 'JSWSTEEL.NS', 'HINDALCO.NS', 'NMDC.NS', 
        'SAIL.NS', 'VEDANTA.NS', 'JINDALSTEL.NS', 'HINDUSTANZINC.NS', 
        'GALLANTT.NS', 'SANGHVI.NS', 'MANGALAM.NS'
    ],
    "Real Estate": [
        'DLF.NS', 'GODREJPROP.NS', 'OBEROIRLTY.NS', 'BRIGADE.NS', 
        'SOBHA.NS', 'MAHLIFE.NS', 'INDIABULLSREAL.NS', 'RELIANCEHOME.NS', 
        'PURAVANKARA.NS', 'SAREGAMA.NS', 'PRAJIND.NS'
    ],
    "Healthcare": [
        'APOLLOHOSP.NS', 'MAXHEALTH.NS', 'KIMSHEALTH.NS', 'HCG.NS', 
        'NARAYANH.NS', 'MEDANTA.NS', 'FORTISHEALTH.NS', 'BLUEDART.NS', 
        'KOTAKMAHINDRA.NS', 'PRISMJERSEY.NS', 'CDSL.NS'
    ],
    "Media and Entertainment": [
        'ZEEENT.NS', 'SUNTV.NS', 'TV18BRDCST.NS', 'BALAJITELE.NS', 
        'PVR.NS', 'EDELWEISS.NS', 'MUTHOOTFIN.NS', 'CINELINE.NS', 
        'SAREGAMA.NS', 'NETWORK18.NS', 'RELIANCECAP.NS'
    ],
    "Infrastructure": [
        'HUDCO.NS', 'L&T.NS', 'GMRINFRA.NS', 'IRBINFRA.NS', 'JPASSOCIATES.NS', 
        'KNRCON.NS', 'DLF.NS', 'GODREJPROP.NS', 'ACC.NS', 
        'SHREECEM.NS', 'AMBUJA.NS', 'MUTHOOTCAP.NS', 'TRIL.NS'
    ]
}


# Caching to avoid redundant fetches
@st.cache_data(ttl=3600)  # Cache the stock data for 1 hour
def fetch_single_stock(ticker, period="6mo"):
    return yf.download(ticker, period=period)

# Fetch multiple stocks concurrently for faster performance
def fetch_multiple_stocks_concurrently(tickers, period="6mo"):
    stock_data = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(fetch_single_stock, ticker, period): ticker for ticker in tickers}
        for future in concurrent.futures.as_completed(futures):
            ticker = futures[future]
            try:
                data = future.result()
                stock_data[ticker] = data
            except Exception as exc:
                st.warning(f"Stock {ticker} generated an exception: {exc}")
    return stock_data

# Prepare data for LSTM
def prepare_lstm_data(data, window_size=5):
    if data.empty:
        raise ValueError("The stock data is empty.")
    
    # Add 52-week High and Low features
    data['52_Week_High'] = data['High'].rolling(window=252, min_periods=1).max()
    data['52_Week_Low'] = data['Low'].rolling(window=252, min_periods=1).min()
    
    features = data[['Adj Close', '52_Week_High', '52_Week_Low']].dropna()
    
    if features.empty or len(features) < window_size:
        raise ValueError("Not enough data available after rolling calculations.")
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(features)

    X, y = [], []
    for i in range(window_size, len(scaled_data)):
        X.append(scaled_data[i-window_size:i])
        y.append(scaled_data[i, 0])  # Predicting 'Adj Close'

    return np.array(X), np.array(y), scaler

# Build LSTM model
def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Train and predict using LSTM
def train_and_predict_lstm(stock_data, window_size=5, epochs=10, batch_size=32):
    predictions = {}
    for ticker, data in stock_data.items():
        try:
            X, y, scaler = prepare_lstm_data(data, window_size=window_size)
            split_index = int(0.8 * len(X))
            X_train, X_test = X[:split_index], X[split_index:]
            y_train, y_test = y[:split_index], y[split_index:]

            model = build_lstm_model(input_shape=(X_train.shape[1], X_train.shape[2]))
            early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

            model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=0, validation_data=(X_test, y_test), callbacks=[early_stop])

            y_pred = model.predict(X_test)
            
            # Rescale predictions
            y_test_scaled = scaler.inverse_transform(np.concatenate((y_test.reshape(-1, 1), np.zeros((y_test.shape[0], 2))), axis=1))[:, 0]
            y_pred_scaled = scaler.inverse_transform(np.concatenate((y_pred, np.zeros((y_pred.shape[0], 2))), axis=1))[:, 0]

            predictions[ticker] = {
                'Next Day Predicted Price': y_pred_scaled[-1],
                'Actual Price': data['Adj Close'].iloc[-1],
                'Test MSE': mean_squared_error(y_test_scaled, y_pred_scaled)
            }

        except ValueError as e:
            st.warning(f"Skipping {ticker}: {str(e)}")

    return predictions

# Sort stocks based on criteria
def sort_stocks(stock_data, sort_by):
    valid_stocks = {ticker: data for ticker, data in stock_data.items() if not data.empty}
    
    if sort_by == "Lowest Price":
        sorted_stocks = sorted(valid_stocks.keys(), key=lambda ticker: valid_stocks[ticker]['Adj Close'].iloc[-1])
    elif sort_by == "Highest Price":
        sorted_stocks = sorted(valid_stocks.keys(), key=lambda ticker: valid_stocks[ticker]['Adj Close'].iloc[-1], reverse=True)
    elif sort_by == "Most Recommended":
        predictions = train_and_predict_lstm(valid_stocks)
        sorted_stocks = sorted(predictions.keys(), key=lambda ticker: predictions[ticker]['Next Day Predicted Price'] - predictions[ticker]['Actual Price'], reverse=True)
    else:
        sorted_stocks = list(valid_stocks.keys())
    
    return sorted_stocks

# Streamlit application
def stock():
    # Navigation bar
    selected_page = option_menu(None, ["Stock Prediction", "Add to Portfolio", "Portfolio"], icons=["graph-up", "plus-circle", "briefcase"], orientation="horizontal")

    if selected_page == "Stock Prediction":
        st.title("Stock Prediction by Sector")

        # Step 1: Select a sector
        selected_sector = st.selectbox("Select a Sector", list(sectors.keys()))

        # Allow users to select specific stocks to analyze
        selected_stocks = st.multiselect("Select specific stocks to analyze", sectors[selected_sector], default=sectors[selected_sector][:3])

        # Fetch stock data
        stock_data = fetch_multiple_stocks_concurrently(selected_stocks, period="6mo")

        # Step 2: Select sorting option
        sort_by = st.selectbox("Sort by", ["Default", "Lowest Price", "Highest Price", "Most Recommended"])

        # Sort stocks based on selected criteria
        sorted_stocks = sort_stocks(stock_data, sort_by)

        # Step 3: Select a stock from the sorted list
        selected_stock = st.selectbox("Select a Stock", sorted_stocks)

        # Get predictions for the selected stock
        predictions = train_and_predict_lstm({selected_stock: stock_data[selected_stock]})

        st.subheader(f"Stock: {selected_stock}")
        prediction = predictions[selected_stock]
        st.write(f"Next Day Predicted Price: ₹{prediction['Next Day Predicted Price']:.2f}")
        st.write(f"Actual Price: ₹{prediction['Actual Price']:.2f}")
        st.write(f"Test MSE: {prediction['Test MSE']:.4f}")

        # Plot the stock data
        data = stock_data[selected_stock]
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data.index, data['Adj Close'], label=f"{selected_stock} Adjusted Close", color='b')
        ax.axhline(y=data['High'].rolling(window=252, min_periods=1).max()[-1], color='g', linestyle='--', label="52-Week High")
        ax.axhline(y=data['Low'].rolling(window=252, min_periods=1).min()[-1], color='r', linestyle='--', label="52-Week Low")
        ax.axhline(y=prediction['Next Day Predicted Price'], color='purple', linestyle=':', label=f"Predicted: ₹{prediction['Next Day Predicted Price']:.2f}")
        ax.set_title(f"{selected_stock} Stock Price and Prediction")
        ax.legend()
        st.pyplot(fig)


    if selected_page == "Add to Portfolio":
       st.title("Add to Portfolio")

       # Select a sector to view and add stocks
       selected_sector = st.selectbox("Select a Sector to view stocks", list(sectors.keys()))
       selected_stocks = st.multiselect("Select stocks to add to portfolio", sectors[selected_sector], default=sectors[selected_sector][:1])

       if "portfolio" not in st.session_state:
           st.session_state.portfolio = {}

       if selected_stocks:
           for stock in selected_stocks:
               stock_data = fetch_single_stock(stock)
               if not stock_data.empty:
                   price = stock_data['Adj Close'].iloc[-1]
                   quantity = st.number_input(f"Enter quantity of {stock} to add", min_value=1, step=1, key=f"qty_{stock}")
                
                   if st.button(f"Add {stock} to Portfolio at ₹{price:.2f} with Quantity {quantity}", key=f"add_{stock}"):
                       if stock in st.session_state.portfolio:
                           # Update quantity if stock is already in portfolio
                           st.session_state.portfolio[stock]['quantity'] += quantity
                       else:
                           # Add stock with price and quantity
                           st.session_state.portfolio[stock] = {'price': price, 'quantity': quantity}
                       st.success(f"Added {quantity} shares of {stock} to portfolio at ₹{price:.2f} each.")

    if selected_page == "Portfolio":
        st.title("Portfolio")
        if "portfolio" not in st.session_state:
            st.session_state.portfolio = {}  # Format: {'stock_name': {'price': price, 'quantity': quantity}}

        if st.session_state.portfolio:
            st.subheader("Your Portfolio")
            total_investment = 0
            total_value = 0
            
            for stock, stock_data in st.session_state.portfolio.items():
                price = stock_data['price']
                quantity = stock_data['quantity']
                stock_value = price * quantity
                total_investment += stock_value
                
                # Smart valuation data (optional: integrate stock price changes)
                col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
                col1.write(stock)
                col2.write(f"Price: ₹{price:.2f}")
                col3.write(f"Quantity: {quantity}")
                col4.write(f"Value: ₹{stock_value:.2f}")
                if col5.button(f"Sell {stock}", key=f"sell_{stock}"):
                    # Selling logic: Reduce quantity or remove stock
                    if quantity > 1:
                        st.session_state.portfolio[stock]['quantity'] -= 1
                    else:
                        del st.session_state.portfolio[stock]
                    st.experimental_rerun()

            st.write(f"Total Investment Value: ₹{total_investment:.2f}")
            
            # Additional smart features: Profit/Loss (assuming you track purchase price)
            # You can add logic to show if stock is gaining or losing based on price changes
        else:
            st.write("Your portfolio is empty.")

# Example of how to add stocks to portfolio (this can be part of the stock selection page)
def add_to_portfolio(stock, price, quantity):
    if stock in st.session_state.portfolio:
        st.session_state.portfolio[stock]['quantity'] += quantity
    else:
        st.session_state.portfolio[stock] = {'price': price, 'quantity': quantity}
