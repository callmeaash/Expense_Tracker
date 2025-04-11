import plotly.graph_objects as go


def plotGraph(fig, graph, df, title):
    if not fig:
        fig = go.Figure()

    if graph.lower().strip() == "bar":
        fig.add_trace(
            go.Bar(
                x=df.index,
                y=df.values,
                marker=dict(color=['green' if x == 'Income' else 'red' for x in df.index]),
                text=df.values,
                textposition='inside',
            )
        )
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center'
            }
        )
    
    elif graph.lower().strip() == "pie":
        fig.add_trace(
            go.Pie(
                labels=df.index,
                values=df.values,
                textinfo='label+percent',
                showlegend=False
            )
        )
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center'
            },
            autosize=True
        )
    elif graph.lower().strip() == 'line':
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df.values,
                mode='lines',
                name=df.name,
                showlegend=True,
                hovertemplate='%{x}<br>%{y}'
            )
        )
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center'
            }
        )
