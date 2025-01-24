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

