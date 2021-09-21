import pandas as pd
import plotly.graph_objects as go

programming = pd.read_csv('./analyzed_data/programming.csv', sep="\n")
olympics = pd.read_csv('./analyzed_data/olympics.csv', sep="\n")

fig = go.Figure(
    data =[go.Bar(y=olympics['sentiment'])],
    layout_title_text="Positive/Negative snetiments around the 2021 olympics"
)