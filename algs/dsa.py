import networkx as nx


# returns e = (r,v)  from x such that weight of (r,v) is minimum
def min_cost_edge(tr_cl, r, x):
    min = 9999999
    res_v = None
    adjs = [a[1] for a in tr_cl.out_edges(r)]
    adjs = set(adjs) - {r}
    intersect = adjs & set(x)
    for v in intersect:
        val = tr_cl[r][v]['weight']
        if val < min:
            res_v = v
            min = val
    return r, res_v, min


def sort_list_intersect(a=[], b=[]):
    res = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] > b[j]:
            j += 1
        elif b[j] > a[i]:
            i += 1
        else:
            res.append(a[i])
            i += 1
            j += 1
    return res


# return -1 if not exist
def bin_search(a, x, lo=0, hi=None):
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        midval = a[mid]
        if midval < x:
            lo = mid + 1
        elif midval > x:
            hi = mid
        else:
            return mid
    return -1


def get_density(tree=nx.DiGraph(), x=[]):
    tot_weight = float(tree.size(weight='weight'))
    nodes = nx.nodes(tree)
    intersect = set(nodes) & set(x)
    if len(intersect) == 0:
        return float('inf')
    else:
        return tot_weight / len(intersect)


def get_density_with_edge(tree=nx.DiGraph(), x=[], edge=tuple()):
    tot_weight = float(tree.size(weight='weight'))
    tot_weight += edge[2]
    nodes = set(nx.nodes(tree)) | {edge[0], edge[1]}  # union of vertices from tree and from edge
    intersect = nodes & set(x)
    if len(intersect) == 0:
        return float('inf')
    else:
        return tot_weight / len(intersect)


def merge_trees(tree1=nx.DiGraph(), tree2=nx.DiGraph()):
    # print(tree1.edges(data=True))
    # print(tree2.edges(data=True))
    edges2 = [(v, u, tree2[v][u]['weight']) for v, u in nx.edges(tree2)]
    tree1.add_weighted_edges_from(edges2)
    # print(tree1.edges(data=True))
    return tree1
