import yfinance as yf
from prettytable import PrettyTable

# Portfolio dictionary to store stock symbols and quantity
portfolio = {}

def add_stock(symbol, quantity):
    """Add a stock to the portfolio."""
    if symbol in portfolio:
        portfolio[symbol] += quantity
    else:
        portfolio[symbol] = quantity
    print(f"{quantity} shares of {symbol} added to portfolio.")

def remove_stock(symbol, quantity):
    """Remove a stock from the portfolio."""
    if symbol in portfolio:
        if portfolio[symbol] > quantity:
            portfolio[symbol] -= quantity
            print(f"{quantity} shares of {symbol} removed.")
        else:
            del portfolio[symbol]
            print(f"{symbol} completely removed from portfolio.")
    else:
        print(f"{symbol} is not in the portfolio.")

def fetch_stock_data(symbol):
    """Fetch real-time stock price and other details."""
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")
    
    if data.empty:
        return None
    return {
        "symbol": symbol,
        "price": round(data['Close'].iloc[-1], 2),
        "change": round(data['Close'].iloc[-1] - data['Open'].iloc[-1], 2)
    }

def show_portfolio():
    """Display the portfolio with stock performance."""
    if not portfolio:
        print("Portfolio is empty.")
        return

    table = PrettyTable(["Stock", "Quantity", "Current Price ($)", "Change ($)", "Total Value ($)"])
    total_portfolio_value = 0

    for symbol, quantity in portfolio.items():
        stock_data = fetch_stock_data(symbol)
        if stock_data:
            total_value = stock_data["price"] * quantity
            table.add_row([symbol, quantity, stock_data["price"], stock_data["change"], round(total_value, 2)])
            total_portfolio_value += total_value

    print(table)
    print(f"Total Portfolio Value: ${round(total_portfolio_value, 2)}")

# Sample usage
add_stock("AAPL", 10)  # Add 10 shares of Apple
add_stock("GOOGL", 5)  # Add 5 shares of Google
show_portfolio()
remove_stock("AAPL", 5)  # Remove 5 shares of Apple
show_portfolio()
