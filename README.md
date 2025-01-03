# 🚀 ClusterX

**ClusterX** is an advanced algorithmic trading bot built using Python. It applies the **Smart Money Concept (SMC)** strategy to analyze market conditions and execute trades based on key liquidity levels and market structure.

## Features
- 🧠 **Smart Money Concept (SMC)**: Uses market structure analysis to make informed trading decisions.
- 📈 **Backtesting**: Test the strategy on historical data to ensure robustness before going live.
- ⚡ **Real-Time Execution**: Executes trades based on real-time market data.
- 💡 **Customizable Parameters**: Adjust key parameters such as risk management, trading pairs, and strategy settings.

## Getting Started

### Prerequisites
Before running **ClusterX**, make sure you have the following installed:
- Python 3.7+
- Required libraries: please check `requirements.txt` file.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ClusterX.git
   ```
2. Navigate into the project folder:
   ```bash
   cd ClusterX
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
1. **API Keys**: Configure your exchange API keys and other required credentials, use the `.env` file. Below is an example of how to structure the `.env` file:
   ```.env
   API_KEY=...
   DISCORD_TOKEN=...
   DISCORD_CHANNEL_ID=...
   ```
2. **Set Trading Pairs**: Modify the trading pairs and risk parameters as per your preferences.

### Running the Bot
To start the bot and begin trading, run:
```bash
python main.py
```

### Backtesting (not implemented yet)
Before running the bot live, you can backtest it with historical data:
```bash
python backtest.py --data data/your_data_folder # This should contain different timeframes
```

### Monitoring
Monitor the bot’s performance through the logs.

## Contributing
Feel free to fork this project and submit pull requests. Contributions are welcome! If you have ideas for improvement or new features, open an issue or contribute directly.

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements
- Inspired by the Smart Money Concept (SMC) and algorithmic trading strategies.

---

**ClusterX** is an ongoing project. Stay tuned for more features and improvements! 🚀
