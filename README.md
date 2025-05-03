# 🧠 ClusterX

**ClusterX** is a modular and extensible desktop platform for algorithmic trading. It enables users to build, run, and monitor multiple trading strategies—powered by indicators, statistical tools, and AI models—executed either locally or remotely.

The application features a high-performance backend in Rust, a modern UI powered by Tauri + React, and seamless integration of real-time market data, AI engines, and custom strategy runners.

This project is open-source and available under the MIT License. Contributions are welcome!

---

## 📦 Features

- 🔍 **Live Market Analysis** – Ingest and process live OHLCV candles from stocks or crypto sources.
- 📊 **Real-Time Indicators** – Built-in support for MACD, Bollinger Bands, Normal Distribution models, and more.
- ⚙️ **Strategy Engine** – Plug-and-play strategy execution with shared indicators and market data.
- 🤖 **AI Integration** – User-selectable AI models to help make or validate trading decisions.
- 🖥️ **Cross-platform Desktop App** – Built with Tauri, runs natively on Windows, macOS, and Linux.
- 📡 **High-Frequency Updates** – WebSocket and IPC architecture for fast communication between core, backend, and UI.

---

## 🧱 Project Structure

```
ClusterX/
├── core/              # Market data processing, indicator computation (Rust)
│   ├── market_data/   # Fetching market data in real-time (API, WebSocket)
│   ├── indicators/    # Indicator computation (MACD, moving averages, etc.)
│   └── strategies/    # User-defined trading strategies execution
├── strategy-runner/   # Isolated execution of user-defined trading strategies (Rust)
├── ai-engine/         # AI models in Rust or Python via bindings
├── app/
│   ├── src-tauri/     # Tauri backend (Rust)
│   └── frontend/      # UI (React)
├── server/            # Central server to manage WebSockets, real-time data distribution
│   ├── websocket/     # WebSocket server for real-time data streaming
│   └── api/           # REST API for historical data retrieval
├── storage/           # Local database layer (SQLite, TimescaleDB)
├── common/            # Shared types, messages, protocol definitions
├── tests/             # Integration and component tests
└── Cargo.toml         # Workspace configuration
```

---

## 🚀 Getting Started

### Prerequisites

- 🦀 Rust (latest stable)
- 🧱 Node.js (LTS) + pnpm / yarn / npm
- 🖼️ Tauri prerequisites ([See official guide](https://tauri.app/v1/guides/getting-started/prerequisites))

### Setup

```ash
# Clone the repository
git clone https://github.com/yourname/clusterx
cd clusterx

# Install frontend dependencies
cd app/frontend
pnpm install

# Start the desktop app (frontend + backend)
pnpm tauri dev
```

---

## 📡 Architecture Overview

ClusterX is designed as a **modular monorepo** using a [Cargo workspace](https://doc.rust-lang.org/book/ch14-03-cargo-workspaces.html). Components communicate via:

- **IPC (Tauri)**: Frontend ↔ Backend for native desktop interaction  
- **WebSocket (internal)**: For real-time updates between backend and strategy engines  
- **Database layer**: Local shared access to candles, indicators, and metadata  

---

## 🧠 AI Strategy Engine

- AI models can be loaded from internal Rust models.
- Users can choose which AI model to use in real-time through the UI.

---

## 📈 Data Sources

ClusterX supports live data ingestion from:
- 📉 **Crypto**: Polygon.io, Binance, KuCoin, etc.
- 📈 **Stocks**: Polygon.io, Alpha Vantage, Twelve Data, etc.
- You can configure data providers in a future config system (`storage/config.toml`)

---

## 🛠️ Development Tools

```
cargo run -p strategy-runner       # Run the strategy engine in isolation
cargo build -p core                # Build the indicator and market core
pnpm tauri dev                     # Launch full desktop app (UI + backend)
cargo test                         # Run all tests
```

---

## 🗺️ Roadmap

- [ ] **Candle data retrieval and storage**: Collect market data (candles) in real-time, store them locally, and provide them to users via WebSockets or API for fast access.
- [ ] **Live chart generation**: Create interactive charts with various options (time frames, indicators, overlays) and update them in real-time as new data arrives.
- [ ] **Real-time indicator calculations**: Implement and display indicators like MACD, Bollinger, (even some SMC), etc., in real-time as new candle data is received.
- [ ] **Strategy creation and real-time performance monitoring**: Allow users to define trading strategies and monitor their live performance (open positions, profit/loss, etc.).
- [ ] **AI model creation and optimization**: Provide functionality for creating and optimizing AI models that can help users with strategy suggestions and improvements, including the ability to combine multiple strategies and let the AI decision-making system choose the best course of action based on real-time data and user-defined goals.
- [ ] **Real-time strategy execution with broker integration**: Connect trading strategies to real brokers for live execution, with real-time updates on performance and positions.
- [ ] **Social features**: Implement a social network within the app where users can share their strategies, post trading tips, screenshots, and discuss ideas.
- [ ] **Marketplace for trading strategies**: Create a marketplace where users can buy, sell, and share strategies with others, creating an ecosystem of shared trading ideas.

---

## Contributing

We welcome contributions to **ClusterX**! Whether it's fixing bugs, improving documentation, adding new features, or submitting ideas, your help is greatly appreciated.

### How to contribute

1. **Fork the repository**: Start by forking the repository to your own GitHub account.
2. **Clone the repository**: Clone your forked repository to your local machine.
   ```bash
   git clone https://github.com/enzoblain/clusterx.git
   ```
3. **Create a branch**: Create a new branch for your changes.
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes**: Implement the changes or fix the issue you're working on.
5. **Commit your changes**: Commit your changes with a clear message.
   ```bash
   git commit -m "Add feature XYZ"
   ```
6. **Push your changes**: Push your changes back to your forked repository.
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Submit a pull request**: Open a pull request on the original repository with a description of your changes.

### Reporting Issues

If you find a bug or have a feature request, please [open an issue](https://github.com/[YourUsername]/clusterx/issues). Be sure to include detailed information so we can understand and address the problem efficiently.

Thank you for contributing to **ClusterX**!

---

## 📄 License

MIT © [Enzo Blain]