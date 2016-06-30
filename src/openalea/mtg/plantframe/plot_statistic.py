from vplants.statistic import *
from openalea.mtg.mtg import MTG
import datetime

def to_graphs(g, roots=0, **kwargs):
    if type(roots) is int:
        return [to_graph(g.sub_tree(i, copy=True),**kwargs) for i in self.roots(scale=roots)]
    else:
        return [to_graph(g.sub_tree(i, copy=True),**kwargs) for i in roots]

def to_graph(g, **kwargs):
    gph = Graph()
    node = dict.pop(kwargs, "node", {})
    arc = dict.pop(kwargs, "arc", {})
    def _to_graph(vertex):
        gph.add_node(vertex)
        for i in node:
            gph.node[vertex][i] = node[i](self, vertex)
        for i in g.children(vertex):
            _to_graph(i)
            gph.add_arc(vertex, i)
    _to_graph(g.root)
    return gph


def _plot(g, roots=0, layout="graphviz", show=True, **kwargs):
    if "prog" in kwargs:
        plot_kwargs = dict(prog=kwargs.pop("prog"))
    else: plot_kwargs = {}
    gphs = to_graphs(g,roots=roots, **kwargs)
    fig = pyplot.figure()
    index = 0
    for i in gphs:
        axes = fig.add_subplot(1, len(gphs), index+1)
        i.plot(axes=axes, show=False, algo=layout+"_layout", **plot_kwargs)
        index += 1
    if show: pyplot.show()

MTG.plot = _plot

