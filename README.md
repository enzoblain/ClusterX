# 🚀 ClusterX - AI-Powered Trading Algorithm

## 📌 Overview
**ClusterX** is a high-performance, AI-powered trading algorithm written in Rust. It intelligently integrates multiple trading strategies and leverages machine learning to analyze signals and optimize trading decisions. This project aims to document progress in designing an efficient trading algorithm by combining mathematical models and machine learning.

## 🌟 Features
✅ **Multi-strategy framework** - Integrates different trading approaches.

✅ **AI-driven optimization** - Utilizes machine learning (likely Random Forest) to make trading decisions.

✅ **Blazing-fast performance** - Developed in Rust for efficient and reliable execution.

✅ **Modular and customizable** - Easily add or modify trading strategies.

✅ **Scalable & adaptable** - Designed to work with different markets and trading conditions.

## 🛠 Installation
1. Install Rust (if not already installed):
   ```sh
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```
2. Clone this repository:
   ```sh
   git clone https://github.com/enzoblain/ClusterX.git
   cd ClusterX
   ```
3. Build the project:
   ```sh
   cargo build --release
   ```

## 🚀 Usage
1. Add trading strategies in the `config/your-strategie.toml` file.
2. Configure the algorithm in `config/config.toml`.
3. Run ClusterX:
   ```sh
   cargo run --release
   ```
4. Monitor logs and adjust strategies based on performance.

## 🔥 Roadmap
### 📌 Phase 1: Research and Learning Fundamentals
- Gather resources to design a trading algorithm based on mathematical models. 📚
- Store these resources in the `resources/` folder.

### 📌 Phase 2: Defining Trading Strategies
- Identify and formalize multiple viable trading strategies.
- Determine indicators and decision-making criteria.

### 📌 Phase 3: Machine Learning for Optimization
- Implement a machine learning model (likely Random Forest) to determine the optimal strategy based on market conditions.
- Test and fine-tune the model's performance.

### 📌 Phase 4: Real-Time Execution
- Integrate the algorithm into a real-time trading environment.
- Implement order execution and risk management.

## 🤝 Contributing
Contributions are welcome! Feel free to fork the project, submit pull requests, and help improve **ClusterX** together.

## 📜 License
ClusterX is licensed under MIT.

## ⚠ Disclaimer
**This project is for educational and research purposes only. Trading involves financial risks, and users should exercise caution before deploying automated strategies. Use at your own risk.**

    