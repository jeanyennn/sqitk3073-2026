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

def performance_category(return_pct):

    if return_pct < 0:
        return "Negative Return"

    elif return_pct <= 2:
        return "Moderate Return"

    else:
        return "High Return"


df["Performance Category"] = df[
    "Return Percentage"
].apply(performance_category)

group_analysis = df.groupby(
    "Performance Category"
)["Estimated Total Return"].mean()

plt.figure(figsize=(12,6))

for name, ticker in stocks.items():

    data = yf.download(
        ticker,
        period="1mo",
        progress=False
    )

    plt.plot(
        data.index,
        data["Close"],
        label=name
    )

#3a
plt.title("1-Month Closing Price Trend")
plt.xlabel("Date")
plt.ylabel("Closing Price (RM)")
plt.legend()
plt.grid(True)

plt.show()

#3b
import squarify
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

sizes = abs(df["Return Percentage"])

sizes = [max(x, 1) for x in sizes]

colors = []
labels = []

for ticker, ret in zip(df["Ticker"], df["Return Percentage"]):

   
    if abs(ret) < 0.01:
        colors.append("#808080")  
        pct = "0.00%"

    elif ret > 0:
        colors.append("#00A878")  
        pct = f"+{ret:.2f}%"

    else:
        colors.append("#DC3545")  
        pct = f"{ret:.2f}%"

    labels.append(f"{ticker}\n{pct}")

plt.figure(figsize=(14, 8))

squarify.plot(
    sizes=sizes,
    label=labels,
    color=colors,
    alpha=0.9,
    edgecolor="white",
    linewidth=0.5,
    pad=False,
    text_kwargs={
        "fontsize": 12,
        "fontweight": "bold",
        "color": "white"
    }
)

plt.axis("off")
plt.title(
    "Portfolio Performance Treemap",
    fontsize=18,
    fontweight="bold"
)

legend_items = [
    mpatches.Patch(color="#00A878", label="> 0% (Positive)"),
    mpatches.Patch(color="#808080", label="= 0% (Neutral)"),
    mpatches.Patch(color="#DC3545", label="< 0% (Negative)")
]

plt.legend(
    handles=legend_items,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.08),
    ncol=3,
    frameon=False,
    fontsize=11
)

plt.tight_layout()
plt.show()