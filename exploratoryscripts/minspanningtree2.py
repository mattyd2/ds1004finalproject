
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_edges_from([(0, 1), (0, 2), (1, 1), (1, 2)])
nx.draw_networkx(G)
plt.show()

# import networkx as nx
# import pandas as pd
# import matplotlib.pyplot as plt

# G = nx.Graph()

# fname = '/Users/matthewdunn/Dropbox/NYU/Spring2016/BigData/GroupProject/ds1004finalproject/generalized_map_reduce/busreduced2.txt'
# lines = [line.rstrip('\n') for line in open(fname)]
# final_list = []
# for i in lines:
#     tmp = i.split(',')
#     final_list.append(tmp)
# # final_list = [[int(number) for number in group] for group in final_list]
# for i in final_list:
#     G.add_edge(int(i[0]), int(i[2]), weight=int(i[1]))

# nx.draw_networkx(G)
# plt.savefig("test.png")

# min_span_tree = nx.minimum_spanning_tree(G)
# test = sorted(min_span_tree.edges(data=True))
# # nx.draw(test)
# # print len(final_list)
# # print len(test)

# df = pd.DataFrame(test)
# df.columns = ['start_station', 'end_station', 'weight']
# df['weight_value'] = df.weight.apply(lambda x: x.get('weight'))

# print df[['start_station', 'end_station', 'weight_value']]
# # df.columns = ['start_id', 'tuple']
# # df['orig'] = df['tuple'].apply(lambda x : 'bus'+str(x.tail))
# # df['time'] = df['tuple'].apply(lambda x : x.weight)
# # df['dest'] = df['tuple'].apply(lambda x : 'bus'+str(x.head))
# # df[['orig', 'time', 'dest']].to_csv('bustree.csv', index=False)
