import plotly.express as px
from pathlib import Path

def generate_design_option_two(df, length):
    path = Path("option_2.py")
    upper_directory_path = str(path.parent.absolute())

    fig = px.scatter(x=length, y=df['light'], size=df["productivity"], error_y=df['std_light'], labels=dict(x="Session Number", y="Light Values (Lumens)", size="Productivity Rating"))
    fig.update_layout(title="Light Values VS. Study Session Number")
    fig.write_image(upper_directory_path + "/static/designoption2fig1.png")
    fig = px.scatter(x=length, y=df['humidity'], size=df["productivity"], error_y=df['std_humidity'], labels=dict(x="Session Number", y="Humidity Values (%)", size="Productivity Rating"))
    fig.update_layout(title="Humidity Values VS. Study Session Number")
    fig.write_image(upper_directory_path + "/static/designoption2fig2.png")