import plotly.express as px
from pathlib import Path

def generate_design_option_one(df, length):
    path = Path("option_1.py")
    upper_directory_path = str(path.parent.absolute())

    fig = px.scatter(x=length, y=df['light'], color=df["productivity"], labels=dict(x="Session Number", y="Light Values", color="Producitivity Rating"))
    fig.update_layout(title="Light Values VS. Session")
    fig.write_image(upper_directory_path + "/static/designoption1fig1.png")
    fig = px.scatter(x=length, y=df['humidity'], color=df["productivity"], labels=dict(x="Session Number", y="Humidity Values", color="Producitivity Rating"))
    fig.update_layout(title="Humidity Values VS. Session")
    fig.write_image(upper_directory_path + "/static/designoption1fig2.png")