# Manhattan Emergency Routing Simulator

## Overview
This project provides a simulation of emergency routing in Manhattan, New York, using graph-based algorithms and dynamic traffic modeling. It demonstrates the capabilities of Dijkstra's Algorithm, Probabilistic Roadmaps (PRM), and Waze-like dynamic routing, complete with visualizations on detailed maps.

## Features
- **Shortest Path Routing:** Utilizes Dijkstra's algorithm to calculate the shortest path between two points.
- **Alternative Routing:** Generates alternative paths using a Probabilistic Roadmap (PRM) approach.
- **Dynamic Traffic Simulation:** Models traffic updates and recalculates routes dynamically, mimicking real-time navigation tools like Waze.
- **Customizable Input:** Allows input of coordinates for source and destination.
- **Visualizations:** Displays detailed maps with route overlays, distances, and optional node visibility.

## Prerequisites
- Python 3.8+
- Required Libraries:
  - `osmnx`
  - `networkx`
  - `matplotlib`
  - `pyproj`
  - `random`

Install dependencies using:
```bash
pip install osmnx networkx matplotlib pyproj
```

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-name/manhattan-routing-simulator.git
   cd manhattan-routing-simulator
   ```

2. Run the simulation:
   ```bash
   python simulate.py
   ```

3. Provide custom coordinates (optional):
   Edit the `simulate()` function or follow the updated input mechanism described below.

## Coordinate Input (New Feature)
The simulation supports custom coordinate input for the source and destination. When prompted, enter the latitude and longitude values for both points.

Example:
```
Enter source coordinates (latitude, longitude): 40.823479, -73.936095
Enter destination coordinates (latitude, longitude): 40.710148, -74.004925
```

The system will calculate and visualize the routes accordingly.

## Example Output
The simulation generates visualizations of:
- **Shortest Path**: Route using Dijkstra's Algorithm.
- **Alternative Routes**: Multiple paths computed via PRM.
- **Dynamic Routing**: Adjusted paths accounting for simulated traffic.

## Future Enhancements
- Real-time traffic data integration.
- Support for additional cities and road networks.
- Advanced user interface for input and visualization.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
