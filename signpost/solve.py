import networkx as nx

"""
NxN matrix 

A list of characters representing one of the directions as below
The numbers prefixing the chars represents the initial position

a: ↑
b: ↗
c: →
d: ↘
e: ↓ 
f: ↙
g: ←
h: ↖  

""" 
game_id = '4x4:1c2cegcgfebfggcbb16a'

"""
Gives matrix position given an index
"""
def matrix_pos(i, n): 
    import math
    return (math.floor(i/n), i%n)

"""
Params:
s: string

Returns:
N: int
d: dict(pos, direction, value )
"""
def game_from_string(s):
    dim, game_string = s.split(":")
    N = int(dim[0])
    d= {}
    i = 0
    curr_value = ''
    for c in game_string:
        cell = matrix_pos(i,N)
        if c.isdigit():
            if curr_value:
                curr_value = curr_value + c # a two digit number
                continue
            else:
                curr_value = c
                continue
        elif curr_value:
            d[cell] = {'direction': c, 'num': int(curr_value)}
            curr_value = None
        else:
            d[cell] =  {'direction': c, 'num': None}
        i = i + 1
    return N, d

n, d = game_from_string(game_id)

"""
Params: 
cell: (int, int)
direction: str

Returns:
valid_moves: Array of (int, int)

"""

def count_up(x, n):
    return range(x + 1, n)

def count_down(x):
    return range(x -1, -1, -1)

def get_next_cells(cell, direction):
    next_cells = []
    i, j = cell
    if direction == 'a':
        next_cells = [(u, j) for u in count_down(i)]
        
    if direction == 'b':
        next_cells = list(zip(count_down(i),
                              count_up(j, n)))

    if direction == 'c':
        next_cells = [(i, v) for v in count_up(j, n)]

    if direction == 'd':
        next_cells = list(zip(count_up(i, n),
                              count_up(j, n)))
            
    if direction == 'e':
        next_cells = [(u, j) for u in count_up(i, n)] 
        
    if direction == 'f':
        next_cells = list(zip(count_up(i, n),
                              count_down(j)))

    if direction == 'g':
        next_cells = [(i, v) for v in count_down(j)] 

    if direction == 'h':
        next_cells = list(zip(count_down(i),
                              count_down(j)))
        
    return next_cells

assert get_next_cells((2, 1),'a') == [(1,1),(0,1)]
assert get_next_cells((2, 1),'b') == [(1,2),(0,3)]
assert get_next_cells((2, 1),'c') == [(2,2),(2,3)]
assert get_next_cells((2, 1),'d') == [(3,2)]
assert get_next_cells((2, 1),'e') == [(3,1)]
assert get_next_cells((2, 1),'f') == [(3,0)]	
assert get_next_cells((2, 1),'g') == [(2,0)]
assert get_next_cells((2, 1),'h') == [(1,0)]

"""
Given a list of graphs, plot them in a matrix
Params: 
L: List of Graph objects

Returns:
Matplotlib plot

"""
def plot_graphs(L):
#     for G in L:
#         print(G.nodes(data=True))
    import matplotlib.pyplot as plt
    n = len(L)
    nrows, ncols = int(n/4)+1, 4
    fig = plt.figure(figsize=(15,15))
    fig.subplots_adjust(hspace=0.4, wspace=0.4)
    fig.suptitle('Current state', fontsize=16)
    for i in range(1,n+1):
        G = L[i-1]
        ax = fig.add_subplot(nrows, ncols, i,xmargin=0.2, ymargin=0.2)
        pos = nx.shell_layout(G)
        nx.draw_networkx_nodes(G,pos,ax=ax,node_size=1000, alpha=0.5)
        nx.draw_networkx_labels(G,pos,ax=ax,font_size=8)
        nx.draw_networkx_edges(G,pos,ax=ax)

        
        
def is_path_graph(G):
    return len(G) == 2

def is_solved(L):
    return all([is_path_graph(G) for G in L])

"""
For a given list of graphs L, delete the edges in each graph 
leading to the node `cell`

"""
def prune_edges(cell,L):
    for G in L:
        if not is_path_graph(G):
            if cell in G:
                G.remove_node(cell)
                
                
"""
For each graph, check if it is a path graph. 
If so, attach it to a suitable parent and prune other childs.
TBD: how to detect multiple possible parents
"""
def prune_list(L):
    for G in L:
        if is_path_graph(G):
            for cell, is_root in G.nodes(data='is_root'):
                if (is_root):
                    prune_edges(cell, L)

"""
Params: 
cell: (int, int)
direction: str
value: char

Returns:
node: NetworkX Graph object with next move

"""
def create_node(cell, direction, num):
    G = nx.DiGraph()
    G.add_node(cell, 
               num=num,
               is_root=True)
    next_cells = get_next_cells(cell, direction)
    if num:
        next_num = num + 1
        # https://stackoverflow.com/a/2569076/355344
        try: 
            next_cell = next(key for key, value in d.items() if value['num'] == next_num)
            G.add_node(next_cell,
                       num=d[next_cell]['num'])
            G.add_edge(cell, next_cell)
            return G
        except:
            next_cell = None
    for next_cell in next_cells:
        G.add_node(next_cell,
                   num=d[next_cell]['num'])
        G.add_edge(cell, next_cell)
    return G

L = [] #list of graphs

for item in d:
    G = create_node(item, d[item]['direction'], d[item]['num'])
    L.append(G)

def solve(L):
    i = 0
    while not is_solved(L):
        prune_list(L)
        print("{}th iteration".format(i))
        i = i + 1
        plot_graphs(L)

solve(L)