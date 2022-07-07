import plotly.express as px
from pathlib import Path

def generate_design_option_two(df, length):
    path = Path("option_2.py")
    upper_directory_path = str(path.parent.absolute())

    fig = px.scatter(x=length, y=df['light'], size=df["productivity"], labels=dict(x="Session Number", y="Light Values", size="Producitivity Rating"))
    fig.update_layout(title="Light Values VS. Session")
    fig.write_image(upper_directory_path + "/static/designoption2fig1.png")
    fig = px.scatter(x=length, y=df['humidity'], size=df["productivity"], labels=dict(x="Session Number", y="Humidity Values", size="Producitivity Rating"))
    fig.update_layout(title="Humidity Values VS. Session")
    fig.write_image(upper_directory_path + "/static/designoption2fig2.png")