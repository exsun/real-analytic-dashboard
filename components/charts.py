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
        st.plotly_chart(fig, key=title, use_container_width=False)

def multi_bar_line_plot(athlete_data, xaxis_title, yaxis_title, title, athletes):
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
        '#005B41', '#22177A', 'rgb(12, 122, 200)', 'rgb(255, 100, 100)', 'rgb(100, 150, 255)',
        'rgb(255, 165, 0)', 'rgb(128, 0, 128)'
    ]
    
    # Assign colors to athletes dynamically
    athlete_colors = {athlete: color_palette[i % len(color_palette)] for i, athlete in enumerate(athletes)}

  
    fig = go.Figure()
    # Add Bar & Line for Each Athlete
    for athlete in athletes:
        # Extract only existing dates & values (Exclude missing ones)
        athlete_dates = list(athlete_data[athlete].keys())  # Dates where data exists
        athlete_scores = list(athlete_data[athlete].values())  # Scores where data exists
        athlete_color = athlete_colors[athlete]  # Get assigned color

        # Add Bar Chart
        fig.add_trace(go.Bar(
            x=athlete_dates,
            y=athlete_scores,
            name=f"{athlete} (Bar)",
            marker=dict(color=athlete_color),  # Set bar color

        ))

        # Add Line Chart
        fig.add_trace(go.Scatter(
            x=athlete_dates,
            y=athlete_scores,
            name=f"{athlete} (Line)",
            mode="lines+markers",
            marker=dict(color=athlete_color),  # Set bar color
            
        ))
    # Update layout properties
    fig.update_layout(
        # width=800,  # Set width in pixels
        # height=600,  # Set height in pixels
        title_font=dict(family="dana, sans-serif", size=24, color="black"),  # Title Font
        font=dict(family="dana, sans-serif", size=14, color="black"),
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        barmode='group',
        template="plotly_white",
        xaxis=dict(type="category"),
        title_x=0.5,  # Center the title
    )

    st.plotly_chart(fig, use_container_width=False, key=title)