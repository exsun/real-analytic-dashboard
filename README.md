# Athletics Analytic Dashboard

## Description

This project is a real-time monitoring dashboard for **athletics performance** and **health analytics**. It visualizes data collected from **smart rings** and **wearable sensors** to provide insights into metrics like heart rate, sleep quality, HRV, and fatigue levels. The system is designed to separate **sensor detection** from **data monitoring**, with **BLE sensors** managed by an in-house **BLE hub** and the **monitoring** package deployed on a server for data processing and visualization.

## Features
- Real-time data collection and visualization.
- Interactive dashboards with charts and metrics.
- Data received from BLE devices and processed in real-time.
- Health and performance insights for athletes.

## Architecture Overview

### System Components:
1. **Smart Rings & Wearable Sensors**: Collect health metrics (e.g., heart rate, HRV, fatigue).
2. **BLE Hub (In-House Transmitter)**: Handles the Bluetooth communication between the sensors and the monitoring server.
3. **Monitoring Server**: Receives and processes data for real-time visualization.
4. **Real-Time Analytics Engine**: Analyzes the sensor data and provides insights for athlete performance.
5. **Dashboard**: A web-based interface to visualize the processed data and metrics.

### Data Flow Diagram

```mermaid
graph LR
  A[Smart Rings & Wearable Sensors] -->|BLE Data| B[BLE Hub (In-House Transmitter)]
  B -->|Sensor Data (Heart Rate, HRV, Sleep, Fatigue)| C[Monitoring Server]
  C -->|Data Processing| D[Real-Time Analytics Engine]
  D -->|Processed Data| E[Dashboard (Streamlit)]
  E -->|Interactive Visualization| F[User Interface]
```

## Setup and Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/streamlit-dashboard.git
   cd streamlit-dashboard
