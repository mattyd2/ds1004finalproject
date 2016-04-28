import networkx as nx

undirected = nx.cycle_graph(0)

fname = '/Users/matthewdunn/Dropbox/NYU/Spring2016/BigData/GroupProject/ds1004finalproject/generalized_map_reduce/busreduced2.txt'
lines = [line.rstrip('\n') for line in open(fname)]
final_list = []
for i in lines:
    tmp = i.split(',')
    final_list.append(tmp)
# final_list = [[int(number) for number in group] for group in final_list]
for i in final_list:
    undirected.add_edge(i[0], i[2], weight=i[1])
min_span_tree = nx.minimum_spanning_tree(undirected)
test = sorted(min_span_tree.edges(data=True))
print len(test)
print len(final_list)
