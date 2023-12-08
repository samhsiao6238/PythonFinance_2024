import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Let's assume some sample data for the purpose of this script, the user can replace it with their actual data
words = ['report', 'accounts', 'reporting', 'file', 'dispute', 'bureau', 'time', 'score', 'sent', 'still',
         'disputed', 'number', 'removed', 'day', 'will', 'creditor', 'debt', 'received', 'item', 'year',
         'Please', 'letter', 'never', 'provide', 'reported']
frequencies = [0.9, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5, 0.45, 0.4,
               0.35, 0.3, 0.25, 0.2, 0.15, 0.1, 0.09, 0.08, 0.07, 0.06,
               0.05, 0.04, 0.03, 0.02, 0.01]

# Creating subplots
fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=("Treemap", "Wordcloud"),
    column_widths=[0.5, 0.5]
)

# Adding treemap
fig.add_trace(
    go.Treemap(
        labels=words,
        parents=[""]*len(words),
        values=frequencies,
        marker_colors=[
            '#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A',
            '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52'
        ] * 3,  # Repeating the color pattern to cover all words
    ),
    row=1, col=1
)

# Adding bar chart for frequencies
fig.add_trace(
    go.Bar(
        x=frequencies,
        y=words,
        orientation='h',
    ),
    row=1, col=2
)

# Update layout for a nice display
fig.update_layout(
    title_text='Most frequently used words in complaints',
    showlegend=False
)

# Display the figure
fig.show()
