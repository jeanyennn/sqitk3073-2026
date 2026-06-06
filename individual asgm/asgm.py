import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


stocks = {
    "Maybank": "1155.KL",
    "CIMB": "1023.KL",
    "Tenaga": "5347.KL",
    "Public Bank": "1295.KL",
    "Sunway": "5211.KL"
}

investment = 1000

results = []

for name, ticker in stocks.items():

    stock = yf.Ticker(ticker)

  
    hist = stock.history(period="1mo")

    yesterday_close = hist['Close'].iloc[-2]
    today_close = hist['Close'].iloc[-1]

    daily_return = today_close - yesterday_close

    shares_purchase = investment // yesterday_close

    estimated_return = shares_purchase * daily_return

    return_percentage = (estimated_return / investment) * 100

    results.append([
        ticker,
        round(yesterday_close, 2),
        round(today_close, 2),
        round(daily_return, 2),
        int(shares_purchase),
        round(estimated_return, 2),
        round(return_percentage, 2)
    ])


df = pd.DataFrame(
    results,
    columns=[
        "Ticker",
        "Previous Closing Price",
        "Latest Closing Price",
        "Daily Return",
        "Shares Purchasable",
        "Estimated Total Return",
        "Return Percentage"
    ]
)

portfolio_summary = df[
    [
        "Ticker",
        "Previous Closing Price",
        "Latest Closing Price",
        "Estimated Total Return",
        "Return Percentage"
    ]
]

print(portfolio_summary)

#print(df)