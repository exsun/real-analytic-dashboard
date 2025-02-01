import streamlit as st
import plotly.graph_objects as go

def bar_line_plot(x , y, xaxis_title, yaxis_title, title):
       # Create Bar Plot
        bar_trace = go.Bar(
            x=x,
            y=y,
            name="Bar Plot",
            marker=dict(color='rgb(58, 71, 80)')
        )

        # Create Line Plot
        line_trace = go.Scatter(
            x=x,
            y=y,
            mode='lines+markers',
            name="Line Plot",
            line=dict(color='rgb(255, 100, 100)', width=2)
        )

        # Combine both traces in a single figure
        fig = go.Figure(data=[bar_trace, line_trace])

        # Set layout properties
        fig.update_layout(
            title=title,
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title,
            barmode='group',
            template="plotly_white",
            xaxis=dict(type="category"),
            title_x=0.5,  # Center the title
        )
            

        # Display the plot in Streamlit
        st.plotly_chart(fig, key=title)

def multi_bar_line_plot(x, y, xaxis_title, yaxis_title, title, athletes):
    """
    Create a grouped bar-line plot for multiple athletes with unique colors.

    Parameters:
    - x: List of test dates (x-axis values)
    - y: Dictionary of athlete data where key is athlete name and value is a list of corresponding values
    - xaxis_title: Title for the x-axis
    - yaxis_title: Title for the y-axis
    - title: Plot title
    - athletes: List of athlete names

    Returns:
    - None (Displays plot in Streamlit)
    """

    # Define a color palette with enough distinct colors for athletes
    color_palette = [
        'rgb(0, 128, 0)', 'rgb(255, 20, 147)', 'rgb(12, 122, 200)', 'rgb(255, 100, 100)', 'rgb(100, 150, 255)',
        'rgb(255, 165, 0)', 'rgb(128, 0, 128)'
    ]
    
    # Assign colors to athletes dynamically
    athlete_colors = {athlete: color_palette[i % len(color_palette)] for i, athlete in enumerate(athletes)}

    bar_traces = []
    line_traces = []

    for athlete in athletes:
        athlete_data = y.get(athlete, [])
        color = athlete_colors.get(athlete)  # Default color if missing
        
        # Create Bar Trace for the athlete
        bar_traces.append(go.Bar(
            x=x,
            y=athlete_data,
            name=f"{athlete} (Bar)",
            marker=dict(color=color)
        ))

        # Create Line Trace for the athlete
        line_traces.append(go.Scatter(
            x=x,
            y=athlete_data,
            mode='lines+markers',
            name=f"{athlete} (Line)",
            line=dict(color=color, width=2),
            marker=dict(symbol='circle', size=8)
        ))

    # Combine both bar and line traces in a single figure
    fig = go.Figure(data=bar_traces + line_traces)

    # Update layout properties
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        barmode='group',
        template="plotly_white",
        xaxis=dict(type="category"),
        title_x=0.5,  # Center the title
    )

    st.plotly_chart(fig, use_container_width=True, key=title)