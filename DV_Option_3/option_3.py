
import plotly.graph_objects as go
def generate_design_option_three(df):
    fig = go.Figure(data=[go.Mesh3d(x=df['light'], y=df['humidity'], z=df['productivity'], color='lightpink', opacity=0.50)])
    fig.update_layout(title='HLBoost', scene = dict(
                    xaxis_title='Light Values (Lumens)',
                    yaxis_title='Humidity Values (%)',
                    zaxis_title='Productivity Rating'),
                    autosize=False,width=1000, height=1000, margin=dict(l=65, r=50, b=65, t=90))
    fig.show()