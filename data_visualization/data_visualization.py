import pandas as pd
import plotly.graph_objects as go
col_names = ['id', 'tweet', 'sentiment']
programming = pd.read_csv('./analyzed_data/programming.csv', header=None, names=col_names)
olympics = pd.read_csv('./analyzed_data/olympics.csv', header=None, names=col_names)

'''
    We don't do much in our data visulization, since we have done 
    most of the pre-processing job already. Here, we need only represent
    our data in a graphical format and try to make sense of it.

    We do this with plotly, an interactive python data visualizatioon library.
    For the purpose of our exercise, we will be using bar graphs.

    We realize that sentiments towards programming and the olympics so far in 2021
    have been positive, which is good news!

    We data, we can learn insights that are not immediately obvious, 
    by extracting, transforming and loading data into a form that we can
    analyze. One can do this in several ways, and some ways are simpler than
    others, but they all can achieve near same results.

    Data is the new currency
'''



# print(olympics['sentiment'].head())

fig1 = go.Figure(
    data =[go.Bar(y=olympics['sentiment'])],
    layout_title_text="Positive/Negative snetiments around the 2021 olympics"
)

fig2 = go.Figure(
    data =[go.Bar(y=programming['sentiment'])],
    layout_title_text="Positive/Negative snetiments about programming so far in 2021"
)


fig1.show()
fig2.show()