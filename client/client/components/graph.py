import plotly.figure_factory as ff
import plotly.graph_objects as go

x1 = [*range(1, 10)]
y2 = [*range(1, 10)]

x1 = [*range(10, 20)]
y2 = [*range(10, 20)]

fig1 = ff.create_quiver(x1, y1, name='Driver 1')
fig2 = ff.create_quiver(x2, y2, name='Driver 2')

for i in range(len(fig1.data)):
    fig1.data[i].xaxis='x1'
    fig1.data[i].yaxis='y1'

fig1.layout.xaxis1.update({'anchor': 'y1'})
fig1.layout.yaxis1.update({'anchor': 'x1'})

for i in range(len(fig2.data)):
    fig2.data[i].xaxis='x2'
    fig2.data[i].yaxis='y2'

# initialize xaxis2 and yaxis2
fig2['layout']['xaxis2'] = {}
fig2['layout']['yaxis2'] = {}

fig2.layout.xaxis2.update({'anchor': 'y2'})
fig2.layout.yaxis2.update({'anchor': 'x2'})

fig = go.Figure()
fig.add_traces([fig1.data[0], fig2.data[0]])

fig.layout.update(fig1.layout)
fig.layout.update(fig2.layout)
