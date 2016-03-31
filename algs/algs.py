import time
from algs.dsa import *
import networkx as nx

start_time = -1
time_out = 10000


def trans_clos(DG):
    adjs = nx.all_pairs_dijkstra_path_length(DG)
    # adjs = nx.floyd_warshall_numpy(DG)
    edges = []
    tr_cl = nx.DiGraph()
    for source, adj in zip(adjs.keys(), adjs.values()):
        for dest, weight in zip(adj.keys(), adj.values()):
            t = (source, dest, weight)
            edges.append(t)
    tr_cl.add_weighted_edges_from(edges)
    return tr_cl


def trans_clos_dense(DG):
    adjs = nx.floyd_warshall_numpy(DG)
    edges = []
    nodes = nx.nodes(DG)
    i = 0
    for node1 in nodes:
        j = 0
        for node2 in nodes:
            t = (node1, node2, float(adjs[i, j]))
            edges.append(t)
            j += 1
        i += 1
    tr_cl = nx.DiGraph()
    tr_cl.add_weighted_edges_from(edges)
    return tr_cl


def set_start_time(t):
    global start_time
    start_time = t


def get_elapsed_time():
    return time.time() - start_time


def print_graph(g):
    # pos = nx.get_node_attributes(g, 'pos')
    nx.draw(g, node_size=300, with_labels=True, pos=nx.circular_layout(g))
    # nx.draw_networkx_edges(G=g, pos = nx.spring_layout(g))
    # plt.show()


def print_tree(g, root):
    tree = nx.bfs_tree(g, root)
    # pos=nx.graphviz_layout(g,prog='twopi',args='')
    nx.draw(tree, with_labels=True, pos=nx.shell_layout(g))
    # plt.show()


def alg3(tr_cl, i=0, k=0, r=0, x=[]):
    t = nx.DiGraph()
    prev = -1
    if i == 1:
        while k > 0:
            e = min_cost_edge(tr_cl, r, x)
            if e[1] is None:
                k -= 1
                continue

            t.add_edge(e[0], e[1], weight=e[2])
            k -= 1
            # pos = bin_search(x, e[1])
            pos = x.index(e[1])
            del x[pos]
    else:
        while k > 0:
            # x.sort()
            t_best = nx.DiGraph()
            den_best = float('inf')
            vertices = nx.nodes(tr_cl)
            # l1 = len(vertices)
            # l2 = len(vertices)
            # print(l1,l2)
            # exit()
            for v in vertices:
                if get_elapsed_time() > time_out:
                    raise Exception('Alg took too long to calculate')
                for kp in range(1, k + 1):
                    tp = alg3(tr_cl, i=i - 1, k=kp, r=v, x=x.copy())
                    tp.add_edge(r, v, weight=tr_cl[r][v]['weight'])
                    tp_den = get_density(tp, x)
                    if den_best > tp_den:
                        den_best = tp_den
                        t_best = tp
            t = merge_trees(t, t_best)
            k -= len(set(x) & set(nx.nodes(t_best)))
            x = list(set(x) - set(nx.nodes(t_best)))
            if i == 3:
                print("k3 =", k)
            if i == 4:
                print("k4 =", k)
            if prev == k:
                k -= 1
                break
            prev = k
    return t


def alg4(tr_cl, i=0, k=0, r=0, x=[]):
    t = nx.DiGraph()
    prev = -1
    if i == 1:
        while k > 0:
            e = min_cost_edge(tr_cl, r, x)
            if e[1] is not None:
                t.add_weighted_edges_from([e])
            k -= 1
            if e[1] is not None:
                # pos = bin_search(x, e[1])
                pos = x.index(e[1])
                del x[pos]
    else:
        while k > 0:
            t_best = nx.DiGraph()
            den_best = float('inf')
            vertices = nx.nodes(tr_cl)
            for v in vertices:
                edge = (r, v, tr_cl[r][v]['weight'])
                tp = alg5(tr_cl, i=i - 1, k=k, r=v, x=x.copy(), edge=edge)
                tp.add_edge(edge[0], edge[1], weight=edge[2])
                tp_den = get_density(tp, x)
                if den_best > tp_den:
                    den_best = tp_den
                    t_best = tp
            if get_elapsed_time() > time_out:
                raise Exception('Alg took too long to calculate')
            print('den_best = ', den_best)
            t = merge_trees(t, t_best)
            k -= len(set(x) & set(nx.nodes(t_best)))
            x = list(set(x) - set(nx.nodes(t_best)))
            print("k=", k)
            if prev == k:
                print('bad')
                k -= 1
            prev = k
    return t


def check_sorted(x):
    prev = x[0]
    for el in x:
        if el < prev:
            return False
        prev = el
    return True


def alg5(tr_cl, i=0, k=0, r=0, x=[], edge=None):
    t = nx.DiGraph()
    tc = nx.DiGraph()
    te_den = float('inf')
    oldx = x.copy()
    prev = -1
    if i == 1:
        while k > 0:
            e = min_cost_edge(tr_cl, r, x)
            if e[1] is not None:
                tc.add_edge(e[0], e[1], weight=e[2])
            k -= 1
            tce_den = get_density_with_edge(tc, oldx, edge)
            if e[1] is not None:
                pos = x.index(e[1])
                # pos = bin_search(x,e[1])
                del x[pos]
            if te_den > tce_den:
                te_den = tce_den
                t = tc.copy()
    else:
        while k > 0:
            t_best = nx.DiGraph()
            den_best = float('inf')
            vertices = nx.nodes(tr_cl)
            for v in vertices:
                edge = (r, v, tr_cl[r][v]['weight'])
                tp = alg5(tr_cl, i=i - 1, k=k, r=v, x=x.copy(), edge=edge)
                tp.add_edge(edge[0], edge[1], weight=edge[2])
                tp_den = get_density(tp, x)
                if den_best > tp_den:
                    den_best = tp_den
                    t_best = tp
            tc = merge_trees(tc, t_best)
            k -= len(set(x) & set(nx.nodes(t_best)))
            if get_density_with_edge(t, x, edge) > get_density_with_edge(tc, x, edge):
                t = tc
            if k == prev:
                k -= 1
                break
            x = list(set(x) - set(nx.nodes(t_best)))
            prev = k
    return t


def alg6(tr_cl, i=0, k=0, r=0, x=[]):
    t = nx.DiGraph()
    prev = -1
    if i == 1:
        while k > 0:
            e = min_cost_edge(tr_cl, r, x)
            if e[1] is not None:
                t.add_weighted_edges_from([e])
            k -= 1
            if e[1] is not None:
                pos = x.index(e[1])
                del x[pos]
    else:
        first = True
        vertices = nx.nodes(tr_cl)
        x = list(set(x) & set(vertices))
        m = dict()
        while k > 0:
            t_best = nx.DiGraph()
            den_best = float('inf')
            if first:
                for v in vertices:
                    edge = (r, v, tr_cl[r][v]['weight'])
                    tp = alg7(tr_cl, i=i - 1, k=k, r=v, x=x.copy(), edge=edge)
                    tp.add_edge(edge[0], edge[1], weight=edge[2])
                    tp_den = get_density(tp, x)
                    m[v] = tp_den
                    if den_best > tp_den:
                        den_best = tp_den
                        t_best = tp
                vertices.sort(key=m.get)
                first = False
            else:
                for v in vertices:
                    if m[v] < den_best:
                        edge = (r, v, tr_cl[r][v]['weight'])
                        tp = alg7(tr_cl, i=i - 1, k=k, r=v, x=x.copy(), edge=edge)
                        tp.add_edge(edge[0], edge[1], weight=edge[2])
                        tp_den = get_density(tp, x)
                        m[v] = tp_den
                        if den_best > tp_den:
                            den_best = tp_den
                            t_best = tp
                    else:
                        vertices.sort(key=m.get)
                        break
            if get_elapsed_time() > time_out:
                raise Exception('Alg took too long to calculate')
            t = merge_trees(t, t_best)
            k -= len(set(x) & set(nx.nodes(t_best)))
            x = list(set(x) - set(nx.nodes(t_best)))
            print("k=", k)
            if prev == k:
                print('bad')
                k -= 1
            prev = k
    return t


def alg7(tr_cl, i=0, k=0, r=0, x=[], edge=None):
    t = nx.DiGraph()
    tc = nx.DiGraph()
    te_den = float('inf')
    oldx = x.copy()
    prev = -1
    if i == 1:
        while k > 0:
            e = min_cost_edge(tr_cl, r, x)
            if e[1] is not None:
                tc.add_edge(e[0], e[1], weight=e[2])
            k -= 1
            tce_den = get_density_with_edge(tc, oldx, edge)
            if e[1] is not None:
                pos = x.index(e[1])
                # pos = bin_search(x,e[1])
                del x[pos]
            if te_den > tce_den:
                te_den = tce_den
                t = tc.copy()
    else:
        first = True
        vertices = nx.nodes(tr_cl)
        x = list(set(x) & set(vertices))
        m = dict()
        while k > 0:
            t_best = nx.DiGraph()
            den_best = float('inf')
            if first:
                for v in vertices:
                    edge = (r, v, tr_cl[r][v]['weight'])
                    tp = alg7(tr_cl, i=i - 1, k=k, r=v, x=x.copy(), edge=edge)
                    tp.add_edge(edge[0], edge[1], weight=edge[2])
                    tp_den = get_density(tp, x)
                    m[v] = tp_den
                    if den_best > tp_den:
                        den_best = tp_den
                        t_best = tp
                vertices.sort(key=m.get)
                first = False
            else:
                for v in vertices:
                    if m[v] < den_best:
                        edge = (r, v, tr_cl[r][v]['weight'])
                        tp = alg7(tr_cl, i=i - 1, k=k, r=v, x=x.copy(), edge=edge)
                        tp.add_edge(edge[0], edge[1], weight=edge[2])
                        tp_den = get_density(tp, x)
                        m[v] = tp_den
                        if den_best > tp_den:
                            den_best = tp_den
                            t_best = tp
                    else:
                        vertices.sort(key=m.get)
                        break

            tc = merge_trees(tc, t_best)
            k -= len(set(x) & set(nx.nodes(t_best)))
            if get_density_with_edge(t, x, edge) > get_density_with_edge(tc, x, edge):
                t = tc
            if k == prev:
                k -= 1
                break
            x = list(set(x) - set(nx.nodes(t_best)))
            prev = k
    return t
