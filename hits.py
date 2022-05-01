import networkx as nx
import numpy as np
from scipy import linalg
import argparse


def make_adj(graph):
    adj = np.zeros((len(graph.nodes), len(graph.nodes)))
    for edge in graph.edges:
        adj[edge[0], edge[1]] = 1
    return adj

def get_root_and_base(graph, adj, term):
    root_set = set()
    base_set = set()

    for i in range(len(graph.nodes)):
        if term in graph.nodes[i]['page_content'].lower():
            root_set.add(i)
            base_set = base_set.union(set(np.where(adj[:, i] == 1)[0]))
            base_set = base_set.union(set(np.where(adj[i, :] == 1)[0]))

    return root_set, base_set

def right_eig(matrix):
    _, vr =  linalg.eig(matrix, left=False, right=True)
    vr = vr[:, 0] / np.sum(vr[:, 0])
    vr = np.where(vr, vr > 1e-10, 1) * vr
    return vr

def main(args):
    web_graph = nx.read_gpickle(args.graph)

    adj = make_adj(web_graph)
    term = args.query.lower()

    root_set, base_set = get_root_and_base(web_graph, adj, term)

    A = adj[list(base_set), :][:, list(base_set)]
    hubs = right_eig(np.matmul(A, A.T))
    auths = right_eig(np.matmul(A.T, A))
    print("Hub scores: ")
    print(np.real(hubs))
    print("Authority scores: ")
    print(np.real(auths))

if __name__ == "__main__":
    np.set_printoptions(precision=4)
    parser = argparse.ArgumentParser(description="HITS algorithm")
    parser.add_argument('--graph', type=str, required=True)
    parser.add_argument('--query', type=str, required=True)
    args = parser.parse_args()
    main(args)