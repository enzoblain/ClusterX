# 🌟 Trend Recognition Algorithm

This document provides an explanation of the **Trend Recognition Algorithm**, which identifies whether the current trend is **bullish** 📈 or **bearish** 📉 and adapts dynamically based on market movements. The algorithm also handles sub-trends, trend reversals, and adjusts key levels dynamically.

---

## 🧠 Core Principles

### 1️⃣ **Initialization**
- The algorithm starts with the **first candle**:
  - If the first candle is bullish, the initial trend is **bullish** 📈.
  - If the first candle is bearish, the initial trend is **bearish** 📉.

---

### 2️⃣ **Trend Continuation**
- In a **bullish trend**:
  - The trend continues as long as each subsequent candle’s **low** is **not lower** than the previous candle’s low.
  - The **last valid high** is updated whenever a candle’s **high** exceeds the previous **last valid high**.
- In a **bearish trend**:
  - The trend continues as long as each subsequent candle’s **high** is **not higher** than the previous candle’s high.
  - The **last valid low** is updated whenever a candle’s **low** drops below the previous **last valid low**.

---

### 3️⃣ **Sub-Trend Detection**
A **sub-trend** forms when:
- In a **bullish trend**:
  - A candle’s **low** falls **below the last valid low**.
- In a **bearish trend**:
  - A candle’s **high** rises **above the last valid high**.

---

### 4️⃣ **Sub-Trend Validation**
A sub-trend can be either **validated** or **invalidated**:  

#### ✅ Validation:
- In a **bullish trend**:
  - If a candle **closes below** the last valid **low**, the sub-trend is validated, signaling a **trend reversal** (from bullish 📈 to bearish 📉).  
- In a **bearish trend**:
  - If a candle **closes above** the last valid **high**, the sub-trend is validated, signaling a **trend reversal** (from bearish 📉 to bullish 📈).  

#### ❌ Invalidation (Retest):
- In a **bullish trend**:
  - If a candle **closes above** the sub-trend’s **high**, the sub-trend is invalidated, and the **low of the sub-trend** becomes the new valid **low** for the main trend.  
- In a **bearish trend**:
  - If a candle **closes below** the sub-trend’s **low**, the sub-trend is invalidated, and the **high of the sub-trend** becomes the new valid **high** for the main trend.  

---

## ⚙️ Dynamic Updates
- The algorithm adjusts **key levels** (lows and highs) dynamically during the trend:
  - **Bullish trend**: The **last valid high** is updated each time a new high exceeds the previous one.  
  - **Bearish trend**: The **last valid low** is updated each time a new low drops below the previous one.  

This ensures the algorithm tracks the most recent market structure.

---

## ⚙️ Summary
- **Start**: The trend begins with the first candle.  
- **Continuation**: Check if the trend remains intact, adjusting the last valid low/high dynamically.  
- **Sub-Trend**: Detect and determine whether it is validated (reversal) or invalidated (retest).  
- **Output**: At any moment, the algorithm returns:
  - The **current trend** (bullish 📈 or bearish 📉).
  - The **last valid low/high** for tracking the trend.

---

## 🚀 Features
- **Dynamic tracking**: The algorithm adapts to market conditions by updating key levels.  
- **Real-time updates**: Detects sub-trends and potential reversals as they form.  
- **Robust analysis**: Provides clear decision-making points for trend validation.