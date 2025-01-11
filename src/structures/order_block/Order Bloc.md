# 🏦 Order Block Recognition Algorithm

This algorithm identifies **Order Blocks**, key liquidity zones in the **Smart Money Concepts (SMC)** strategy, by iterating through pre-identified market trends.

---

## 🧠 Core Principles

### 1️⃣ **What Are Order Blocks?**
- **Order Blocks** are areas of liquidity formed by institutional trading activities.
- They are found by identifying the **last candle** of a trend:
  - **Bullish Order Block**: The last bearish candle before a bullish trend begins.
  - **Bearish Order Block**: The last bullish candle before a bearish trend begins.
  
These blocks represent potential points of reversal or continuation based on institutional order flow.

### 2️⃣ **Trend and Order Block Relationship**
- The algorithm focuses on already defined trends (not identifying them).
- An **Order Block** is the **last candle** before the price changes direction significantly:
  - For **Bullish Order Blocks**: The last bearish candle before price starts moving upwards.
  - For **Bearish Order Blocks**: The last bullish candle before price starts moving downwards.

---

## ⚙️ Algorithm Workflow

### **Step-by-Step Process**
1. **Iterating Through Trends**:
   - The algorithm takes in pre-identified market trends (either bullish or bearish).
   
2. **Order Block Recognition**:
   - For each trend:
     - **Bullish Trend**: Identify the last bearish candle before the price begins to rise.
     - **Bearish Trend**: Identify the last bullish candle before the price begins to fall.

3. **Marking Order Blocks**:
   - The identified candle (either bearish or bullish) is marked as an **Order Block**.
   - These blocks are potential areas for price reversals or continuations.

---

## ⚙️ Dynamic Updates
- The algorithm processes trends iteratively, identifying and updating Order Blocks as price moves through the given trends.
  
---

## 🚀 Features
- **Identifies key liquidity zones (Order Blocks)** based on predefined trends.
- **Simple iteration** through trends to mark Order Blocks.
- **Real-time updates** as new trends are provided to the algorithm.

---

## 🧩 Summary
The Order Block Recognition Algorithm:
- **Iterates through predefined trends** to identify Order Blocks.
- **Marks key liquidity zones** where price may reverse or continue.
- **Provides real-time insights** for traders using the SMC strategy.
