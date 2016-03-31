import os
import time
import networkx as nx
from algs.algs import *
from algs.dsa import *
import sys


def get_graph(filename, with_root=False):
    DG = nx.DiGraph()
    f = open(filename, 'r')
    line = None
    edges = []
    coordinates = []
    terms = []
    if with_root:
        root = None
    while line != 'EOF':
        line = f.readline().strip()
        toks = line.split(' ')
        if toks[0] == 'A':
            t = tuple(int(x) for x in toks[1:])
            edges.append(t)
        if toks[0] == 'T':
            terms.append(int(toks[1]))
        if toks[0] == 'Root':
            if with_root:
                root = int(toks[1])
        if toks[0] == 'DD':
            t = tuple(int(x) for x in toks[1:])
            coordinates.append(t)
    for coord in coordinates:
        DG.add_node(coord[0], pos=(coord[1], coord[2]))
    terms.sort()
    DG.add_weighted_edges_from(edges)
    # print_graph(DG)
    # nx.draw(DG, node_size=50)
    # plt.show()
    # f.close()
    if with_root:
        return DG, terms, root
    else:
        print_graph(DG)
        max_len = 0
        max_node = None
        for node in nx.nodes(DG):
            # print(node, tr_cl.out_edges(node))
            descs = nx.descendants(DG, node)
            # desc_numb = len(descs)
            if len(set(terms) & set(descs)) == len(descs):
                # max_len = desc_numb
                max_node = node
        if max_len == len(nx.nodes(DG)):
            return DG, terms, max_node
        else:
            reachable = set(nx.descendants(DG, max_node)) | {max_node}
            unreachable = set(nx.nodes(DG)) - reachable
            for node in unreachable:
                DG.remove_node(node)
        terms = list(set(terms) & reachable)
        print('terms =', len(terms))
        return DG, terms, max_node


# save times in format: <vertex number> <edge number> <alg> <time> <res>
def save_time(v, e, terms, alg, t, res):
    f = open('vi2time.txt', 'r')
    f_strs = f.readlines()
    f.close()
    row_to_put = -1
    i = 0
    for f_str in f_strs:
        toks = f_str.strip().split(' ')
        if toks[0] == str(v) and toks[1] == str(e) and toks[2] == str(alg) and toks[3] == str(terms):
            row_to_put = i
        i += 1
    if row_to_put == -1:
        f_strs.append(str(v) + " " + str(e) + " " + str(terms) + " " + str(alg) + " " + str(t) + " " + str(res) + '\n')
    else:
        f_strs[row_to_put] = str(v) + " " + str(e) + " " + str(terms) + " " + str(alg) + " " + str(t) + " " + str(
            res) + "\n"
    f = open('vi2time.txt', 'w')
    f.writelines(f_strs)
    f.close()


def induce_graph(DG=nx.DiGraph(), n=0, t=0, root=1):  # induce graph to have n nodes
    bfs_list = list(set(sum(list(nx.algorithms.bfs_tree(DG, root).edges()), ())))
    t = int(t)
    bfs_list = bfs_list[:n]
    DG = DG.subgraph(bfs_list)
    import random
    terms = random.sample(set(nx.nodes(DG)) - {root}, t)
    return DG, terms


def graph_test(filename):
    print('')
    print('Getting graph..')
    DG, terms, root = get_graph(filename, with_root=True)
    print('Getting graph is finished')
    print("")
    terms = list(set(terms) - {root})
    # DG, terms = get_graph('WRP4/wrp4-11.stp')
    print_graph(DG)
    v = nx.number_of_nodes(DG)
    e = nx.number_of_edges(DG)
    print("Number of vertices: ", v)
    print("Number of reachable vertices: ", len(nx.descendants(DG, root)) + 1)
    print("Number of edges: ", e)
    print('')
    print('apsp started')
    start_time = time.time()
    tr_cl = trans_clos(DG)
    elapsed_time = time.time() - start_time
    print('apsp finished in', elapsed_time)
    # print_graph(tr_cl)
    max_len = 0
    max_node = None
    for node in nx.nodes(tr_cl):
        # print(node, tr_cl.out_edges(node))
        if len(tr_cl.out_edges(node)) > max_len:
            max_len = len(tr_cl.out_edges(node))
            max_node = node
    print("max node ", max_node)
    print("intersect", set(v for x, v in tr_cl.out_edges(max_node)) & set(terms))
    i = 1
    print('Alg6 with i = ', i, 'started')
    start_time = time.time()
    set_start_time(start_time)
    terms.sort()
    tree = alg6(tr_cl, i=2, k=len(terms), r=root, x=terms)
    elapsed_time = time.time() - start_time
    print('Elapsed time = ', elapsed_time)
    tot_weight = tree.size(weight='weight')
    print('Weight of MSTw = ', tot_weight)
    print_graph(tree)
    exit()
    prev = dict()
    for i in [1, 2]:
        # try:
        #     if not (('alg3-' + str(i)) not in prev or prev[('alg3-' + str(i))]):
        #         raise Exception('')
        #     raise Exception()
        #     print('alg3-' + str(i), 'started..')
        #     start_time = time.time()
        #     set_start_time(start_time)
        #     tree = alg3(tr_cl, i=i, k=len(terms.copy()), r=root, x=terms.copy())
        #     elapsed_time = time.time() - start_time
        #     tot_weight = tot_weight = tree.size(weight='weight')
        #     print('alg3-' + str(i), 'finished in', elapsed_time, 'with res =', tot_weight)
        #     print('')
        #     save_time(v, e, 'alg3-' + str(i), elapsed_time, tot_weight)
        #     prev['alg3-' + str(i)] = True
        # except:
        #     save_time(v, e, 'alg3-' + str(i), '-', '-')
        #     print('Alg took to long to compute')
        #     prev['alg3-' + str(i)] = False
        # try:
        #     if not (('alg4-' + str(i)) not in prev or prev[('alg3-' + str(i))]):
        #         raise Exception('')
        #     raise Exception()
        #     print('alg4-' + str(i), 'started..')
        #     start_time = time.time()
        #     set_start_time(start_time)
        #     tree = alg4(tr_cl, i=i, k=len(terms.copy()), r=root, x=terms.copy())
        #     elapsed_time = time.time() - start_time
        #     tot_weight = tree.size(weight='weight')
        #     print('alg4-' + str(i), 'finished in', elapsed_time, 'with res =', tot_weight)
        #     print('')
        #     save_time(v, e, 'alg4-' + str(i), elapsed_time, tot_weight)
        #     prev['alg4-' + str(i)] = True
        # except:
        #     save_time(v, e, 'alg4-' + str(i), '-', '-')
        #     print('Alg took to long to compute')
        #     prev['alg4-' + str(i)] = False
        # try:
        if not (('alg6-' + str(i)) not in prev or prev[('alg6-' + str(i))]):
            raise Exception('')
        print('alg6-' + str(i), 'started..')
        start_time = time.time()
        set_start_time(start_time)
        tree = alg6(tr_cl, i=i, k=len(terms.copy()), r=root, x=terms.copy())
        elapsed_time = time.time() - start_time
        tot_weight = tree.size(weight='weight')
        print('alg6-' + str(i), 'finished in', elapsed_time, 'with res =', tot_weight)
        print('')
        save_time(v, e, 'alg6-' + str(i), elapsed_time, tot_weight)
        prev['alg6-' + str(i)] = True
        # except:
        #     save_time(v, e, 'alg6-' + str(i), '-', '-')
        #     print('Alg took to long to compute')
        #     prev['alg6-' + str(i)] = False


def wrp_test(filename=None, g=None, terms=None, root=None):
    global prev
    if g is None:
        # print('')
        # print('Getting graph..')
        DG, terms, root = get_graph(filename, with_root=True)
        # print_graph(DG)

        v = nx.number_of_nodes(DG)
        e = nx.number_of_edges(DG)

        print('root is', root)
        print("Number of vertices: ", v)
        print("Number of reachable vertices: ", len(nx.descendants(DG, root)) + 1)
        print("Number of edges: ", e)
        print('')
        print('apsp started')
        start_time = time.time()
        tr_cl = trans_clos_dense(DG)
        # print_graph(tr_cl)
        elapsed_time = time.time() - start_time
        print('apsp finished in', elapsed_time)

        terms = list(set(terms) - {root})
        terms.sort()

        i = 2
        print('Alg6 with i = ', i, 'started')
        start_time = time.time()
        set_start_time(start_time)
        terms.sort()
        tree = alg3(tr_cl, i=4, k=len(terms), r=root, x=terms)
        elapsed_time = time.time() - start_time
        print('Elapsed time = ', elapsed_time)
        tot_weight = tree.size(weight='weight')
        print('Weight of MSTw = ', tot_weight)
        print_graph(tree)
        exit()
    else:
        DG = g

        v = nx.number_of_nodes(DG)
        e = nx.number_of_edges(DG)

        print('root is', root)
        print("Number of vertices: ", v)
        print("Number of reachable vertices: ", len(nx.descendants(DG, root)) + 1)
        print("Number of edges: ", e)
        print('')
        print('apsp started')
        start_time = time.time()
        tr_cl = trans_clos_dense(DG)
        # print_graph(tr_cl)
        elapsed_time = time.time() - start_time
        print('apsp finished in', elapsed_time)

        terms = list(set(terms) - {root})
        terms.sort()

    for i in [4]:
        try:
            if not (('alg3-' + str(i)) not in prev or prev[('alg3-' + str(i))]):
                raise Exception('')
            print('alg3-' + str(i), 'started..')
            start_time = time.time()
            set_start_time(start_time)
            tree = alg3(tr_cl, i=i, k=len(terms.copy()), r=root, x=terms.copy())
            elapsed_time = time.time() - start_time
            tot_weight = tree.size(weight='weight')
            print('alg3-' + str(i), 'finished in', elapsed_time, 'with res =', tot_weight)
            print('')
            save_time(v, e, len(terms), 'alg3-' + str(i), elapsed_time, tot_weight)
            prev['alg3-' + str(i)] = True
        except:
            save_time(v, e, len(terms), 'alg3-' + str(i), '-', '-')
            print('Alg took to long to compute')
            prev['alg3-' + str(i)] = False
        try:
            if not (('alg4-' + str(i)) not in prev or prev[('alg3-' + str(i))]):
                raise Exception('')
            print('alg4-' + str(i), 'started..')
            start_time = time.time()
            set_start_time(start_time)
            tree = alg4(tr_cl, i=i, k=len(terms.copy()), r=root, x=terms.copy())
            elapsed_time = time.time() - start_time
            tot_weight = tree.size(weight='weight')
            print('alg4-' + str(i), 'finished in', elapsed_time, 'with res =', tot_weight)
            print('')
            save_time(v, e, len(terms), 'alg4-' + str(i), elapsed_time, tot_weight)
            prev['alg4-' + str(i)] = True
        except:
            save_time(v, e, len(terms), 'alg4-' + str(i), '-', '-')
            print('Alg took to long to compute')
            prev['alg4-' + str(i)] = False
        try:
            if not (('alg6-' + str(i)) not in prev or prev[('alg6-' + str(i))]):
                raise Exception('')
            print('alg6-' + str(i), 'started..')
            start_time = time.time()
            set_start_time(start_time)
            tree = alg6(tr_cl, i=i, k=len(terms.copy()), r=root, x=terms.copy())
            elapsed_time = time.time() - start_time
            tot_weight = tree.size(weight='weight')
            print('alg6-' + str(i), 'finished in', elapsed_time, 'with res =', tot_weight)
            print('')
            save_time(v, e, len(terms), 'alg6-' + str(i), elapsed_time, tot_weight)
            prev['alg6-' + str(i)] = True
        except:
            save_time(v, e, len(terms), 'alg6-' + str(i), '-', '-')
            print('Alg took to long to compute')
            prev['alg6-' + str(i)] = False


def cmd_test(filename, alg, i):
    DG, terms, root = get_graph(filename, with_root=True)

    v = nx.number_of_nodes(DG)
    e = nx.number_of_edges(DG)

    print('root is', root)
    print("Number of vertices: ", v)
    print("Number of reachable vertices: ", len(nx.descendants(DG, root)) + 1)
    print("Number of edges: ", e)
    print('')
    print('apsp started')
    start_time = time.time()
    tr_cl = trans_clos_dense(DG)
    # print_graph(tr_cl)
    elapsed_time = time.time() - start_time
    print('apsp finished in', elapsed_time)

    if alg == 'alg3':
        print('Alg3 with i = ', i, 'started')
        start_time = time.time()
        set_start_time(start_time)
        terms.sort()
        tree = alg3(tr_cl, i=i, k=len(terms), r=root, x=terms)
        elapsed_time = time.time() - start_time
        print('Elapsed time = ', elapsed_time)
        tot_weight = tree.size(weight='weight')
        print('Weight of MSTw = ', tot_weight)
    if alg == 'alg4':
        print('Alg4 with i = ', i, 'started')
        start_time = time.time()
        set_start_time(start_time)
        terms.sort()
        tree = alg4(tr_cl, i=i, k=len(terms), r=root, x=terms)
        elapsed_time = time.time() - start_time
        print('Elapsed time = ', elapsed_time)
        tot_weight = tree.size(weight='weight')
        print('Weight of MSTw = ', tot_weight)
    if alg == 'alg6':
        print('Alg6 with i = ', i, 'started')
        start_time = time.time()
        set_start_time(start_time)
        terms.sort()
        tree = alg6(tr_cl, i=i, k=len(terms), r=root, x=terms)
        elapsed_time = time.time() - start_time
        print('Elapsed time = ', elapsed_time)
        tot_weight = tree.size(weight='weight')
        print('Weight of MSTw = ', tot_weight)

args = sys.argv
filename = args[1]
alg = args[2]
i = int(args[3])
cmd_test(filename, alg, i)