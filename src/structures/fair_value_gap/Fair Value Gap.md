# 🌟 Fair Value Gap Detection Algorithm

This algorithm identifies **Fair Value Gaps (FVGs)** in market data. A Fair Value Gap occurs when there is a large difference between consecutive candles, leaving a "gap" in price action that could indicate potential market inefficiencies.

---

## 🧠 Core Principles

### 1️⃣ **Fair Value Gap Definition**

A Fair Value Gap is identified when:

- **Bearish Gap**: The **low** of the candle before is higher than the **high** of the candle after.
- **Bullish Gap**: The **high** of the candle before is lower than the **low** of the candle after.

### 2️⃣ **Dynamic Updates**

- If previous Fair Value Gaps are provided, the algorithm continues detection from the last gap's datetime.
- Otherwise, it starts from the second candle.

---

## ⚙️ Summary

- **Identifies bearish and bullish gaps** based on price action.
- **Dynamic tracking**: Allows continuation from the last identified gap.
- **Outputs**: A DataFrame containing details for each detected gap, including direction, high, low, and datetime.

---

## 🚀 Features

- **Efficient gap detection**: Recognizes gaps in market data dynamically.
- **Adaptable**: Can resume from the last detected gap or start afresh.
- **Comprehensive output**: Provides all relevant details for identified Fair Value Gaps.

