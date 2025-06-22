# 📊 Cryptocurrency Dashboard with Dash & Plotly

This project is an interactive cryptocurrency dashboard built using Python, Dash, and Plotly. It visualizes real-time market data from the CoinMarketCap API through five insightful charts, making it easier to understand the current trends and categories in the crypto ecosystem.

## 🚀 Features

* 📈 **Market Cap Bubble Chart**
  Visualizes cryptocurrencies' market cap and circulating supply, with bubble size and color representing category (platform).

* 📊 **Trading Volume Bar Chart**
  Displays the 24-hour trading volume per cryptocurrency, colored by platform/category.

* 🥧 **Market Dominance Pie Chart**
  Shows the market cap share of each platform/category.

* 🧮 **Circulating Supply vs. Market Cap Scatter Plot**
  Compares market capitalization against circulating supply, with bubble size showing market activity (market pairs).

* 📉 **Horizontal Market Dominance Bar Chart**
  Highlights individual cryptocurrencies' market dominance in percent.

## 🧩 Technologies Used

* **Python 3.x**
* **Dash** for web app framework
* **Plotly Express** for interactive visualizations
* **Pandas** for data processing
* **CoinMarketCap API** for live market data

## 🔌 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/crypto-dashboard.git
cd crypto-dashboard
```

### 2. Install Dependencies

```bash
pip install dash plotly pandas requests
```

### 3. Obtain API Key

Get a free API key from [CoinMarketCap Developer Portal](https://pro.coinmarketcap.com/).

### 4. Set API Key

In the `main.py` file, replace:

```python
api_key = '##'
```

with your actual API key:

```python
api_key = 'your_real_api_key'
```

Alternatively, you can load it from an environment variable for better security.

### 5. Run the App

```bash
python main.py
```

Visit [http://127.0.0.1:8050](http://127.0.0.1:8050) in your browser.

## 🌐 Dashboard Language and Localization

The dashboard contains a Hungarian-language explanatory section that describes each visualization and its purpose, ensuring accessibility for Hungarian-speaking users.

## 🧠 Key Insights

* Hover interactions provide on-the-fly details per data point
* Charts are dynamically colored by crypto platform/category
* Useful for investors, analysts, and crypto enthusiasts
