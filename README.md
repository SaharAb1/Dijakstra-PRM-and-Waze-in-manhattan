# 🚀 Manhattan Emergency Route Simulation

This project calculates emergency routes in **Manhattan, New York** using **OpenStreetMap (OSM)** and **NetworkX**. It allows users to input custom coordinates or use default locations to find the shortest and alternative paths.

## 📌 Features

- 📍 **Dijkstra's Algorithm** for the shortest path
- 🔀 **Alternative Routes using PRM (Probabilistic Roadmaps)**
- 🚦 **Traffic Simulation (Dynamic Routing like Waze)**
- 🌙 **Dark Mode Route Visualization**

## 🛠️ Installation

### **1️⃣ Install Dependencies**

Ensure you have Python installed, then run:

```bash
pip install osmnx networkx matplotlib pyproj
```

### **2️⃣ Run the Script**

Run the following command:

```bash
python manhattan.py
```

You will be prompted to enter coordinates **or** use the default locations.

---

## 🎨 Dark Mode Plot Fix

The route visualization is **forced into dark mode** by:

- Using `plt.style.use("dark_background")`
- Setting `fig.patch.set_facecolor("black")`
- Adjusting `ax.set_facecolor("black")`

---

## 📖 How It Works

1️⃣ **User selects start and destination** (via input).
2️⃣ **Graph data is loaded** from OpenStreetMap (OSM).
3️⃣ **Routes are computed:**

- **Dijkstra’s Algorithm** (Shortest Path)
- **Alternative Paths** (PRM-based)
- **Dynamic Routing** (Simulating traffic delays)
  4️⃣ **The routes are plotted** with a dark background.

---

## 🚀 Example Output

1️⃣ **Dijkstra's Algorithm Route** (Shortest Path) 🟥
2️⃣ **Alternative Routes** (PRM-based) 🟨🟧🟣
3️⃣ **Traffic-Affected Route** (Dynamic) 🔵

---

## 🔧 Troubleshooting

❌ **ModuleNotFoundError:** Run:

```bash
pip install -r requirements.txt
```

---

## 📌 To-Do

- Make for it a gui 

---

## 👨‍💻 Author

Created by **SaharAxsus** 🎯

