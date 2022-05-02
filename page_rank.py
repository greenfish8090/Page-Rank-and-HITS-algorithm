import numpy as np
from scipy import linalg
import argparse
import pydot

def compute_trans(mask, rtp = True, random_tp = 0.1):
    """A function to compute transition probability matrix.

    Args
    ----
        mask    : adjacency matrix of the graph
        rtp     : whether or not to perform random teleportation
        random_tp: the random teleportation probability

    Returns
    -------
        trans   : the transition probability matrix
        
    """

    #Calculating sum of each row and dividing from mask to get probabilities
    sums = np.sum(mask, axis=1, keepdims=True)
    trans = np.divide(mask, sums, out=np.zeros_like(mask), where=sums!=0)
    
    if rtp:
        #Accounting for random teleportations
        temp1 = np.divide(random_tp, (len(mask) - sums), out=np.zeros_like(mask), where=(len(mask) - sums)!=0)
        temp2 = np.divide(1 - random_tp, sums, out=np.zeros_like(mask), where=sums!=0)
        trans = temp1 * (1 - mask) + temp2 * mask
        trans = trans / np.sum(trans, axis=1, keepdims=True)
    
    return trans

def left_eig(trans):
    """A function to compute left eigen vector.

    Args
    ----
        trans   : transition probability matrix

    Returns
    -------
        ss      : the staedy-state probability vector
        
    """

    _, vl = linalg.eig(trans, left=True, right=False)
    ss = vl[:, 0] / np.sum(vl[:, 0])
    return ss

def power_iter(transition_matrix, epsilon = 1e-15, max_iters = 100):
    """A function to compute steady state probabilities by using power iteration method.

    Args
    ----
        trans           : transition probability matrix
        epsilon         : when the difference between consecutive steady states is less than epsilon, we terminate power iteration
        max_iters       : the maximum number of iterations

    Returns
    -------
        steady_state    : the transition probability matrix
        current_iter    : the last iteration conducted
        
    """

    current_iter = 0
    starting_page = np.random.choice(len(transition_matrix))
    steady_state = np.zeros((1, len(transition_matrix)))
    prev_steady_state =  np.zeros((1, len(transition_matrix)))
    steady_state[0, starting_page] = 1
    
    while (np.linalg.norm(steady_state - prev_steady_state) > epsilon and current_iter < max_iters):
        prev_steady_state = steady_state
        steady_state = np.matmul(steady_state, transition_matrix)
        current_iter += 1
    
    return steady_state, current_iter

def main(args):
    """The main function.

    Args
    ----
        args   : file, rtp
    
    """

    graph = pydot.Dot("Graph")
    with open(args.file, 'r') as f:
        lines = f.readlines()
        n_nodes = int(lines[0])
        mask = np.zeros((n_nodes, n_nodes))
        n_edges = int(lines[1])
        for e in lines[2:]:
            src, dst = e.rstrip().split(' ')
            src, dst = int(src), int(dst)
            
            mask[src-1, dst-1] = 1
            graph.add_edge(pydot.Edge(e.split(' ')[0], e.split(' ')[1]))
    
    trans = compute_trans(mask, args.rtp)
    ss_1 = left_eig(trans)
    print("Steady state calculated using left eigen decomposition:\n" + str(np.real(ss_1)))

    ss_2, ci = power_iter(trans)
    print("Steady state calculated using power iteration:\n" + str(ss_2[0]))
    print(f"Converged in {ci} steps")



if __name__ == "__main__":
    np.set_printoptions(precision=4)
    parser = argparse.ArgumentParser(description="Page rank algorithm")
    parser.add_argument('--file', type=str, required=True, help='path to input file')
    parser.add_argument('--rtp', type=bool, required=True, help='whether to perform random teleportation or not')
    args = parser.parse_args()
    main(args)

