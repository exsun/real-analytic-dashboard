# Real-Time Athletics Analytics Dashboard

## Description

This project is a real-time monitoring dashboard built with **Streamlit**. It visualizes data collected from **smart rings** and **wearable sensors**, providing insights into health metrics such as heart rate, sleep quality, HRV, and fatigue levels. Data is collected via Bluetooth Low Energy (BLE) devices and transmitted in real-time using **MQTT** to a central server for processing and visualization.

## Features
- Real-time data collection and visualization.
- Interactive dashboards with charts and metrics.
- Data received from BLE devices and sent to the dashboard via MQTT.
- Customizable widgets for user interaction.
- Integration with time-series databases for long-term data storage.

## Technologies Used
- **Streamlit**: For building interactive data applications.
- **BLE (Bluetooth Low Energy)**: For reading sensor data from smart rings.
- **MQTT**: For real-time data streaming to the dashboard.
- **Pandas**: For data manipulation and processing.
- **Matplotlib/Plotly**: For visualizing data (graphs, charts).
- **SQLite/PostgreSQL/TimescaleDB**: For data storage (optional).
- **Docker**: For containerizing the app (optional).

## Requirements
1. Python 3.x
2. Streamlit: `pip install streamlit`
3. Bleak (for BLE communication): `pip install bleak`
4. Paho MQTT (for MQTT communication): `pip install paho-mqtt`
5. (Optional) Database for storing data, e.g., PostgreSQL, SQLite.
6. (Optional) Docker for containerization.

## Setup and Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/streamlit-dashboard.git
   cd streamlit-dashboard
