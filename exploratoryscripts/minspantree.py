from __future__ import print_function, division
import numpy
from numpy import *
import networkx as nx
from networkx import *
import matplotlib.pyplot as plt

N = 30
G = nx.grid_2d_graph(N, N)
pos = dict((n, n) for n in G.nodes())
labels = dict(((i, j), i + (N-1-j) * N) for i, j in G.nodes())
nx.relabel_nodes(G, labels, False)
inds = labels.keys()
vals = labels.values()
inds.sort()
vals.sort()
pos2 = dict(zip(vals, inds))
nx.draw_networkx(T, pos=pos2, with_labels=False, node_size=15)
