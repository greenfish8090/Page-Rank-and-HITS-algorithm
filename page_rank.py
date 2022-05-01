import numpy as np
from scipy import linalg
import argparse
import pydot

def compute_trans(mask, rtp = True, random_tp = 0.1):
    
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

def compute_steady_state_by_calculating_left_eigen_vector_using_scipy_because_numpy_didnt_work_for_some_reason__we_also_ended_up_normalizing_the_eigen_vector_ourselves_why_does_scipy_not_do_it_even_though_it_says_it_does_in_the_docs_wtf(trans):
    _, vl = linalg.eig(trans, left=True, right=False)
    return vl[:, 0] / np.sum(vl[:, 0])

def power_iter(transition_matrix, epsilon = 1e-15, max_iters = 100):
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
    ss_1 = compute_steady_state_by_calculating_left_eigen_vector_using_scipy_because_numpy_didnt_work_for_some_reason__we_also_ended_up_normalizing_the_eigen_vector_ourselves_why_does_scipy_not_do_it_even_though_it_says_it_does_in_the_docs_wtf(trans)
    print("Steady state calculated using left eigen decomposition:\n" + str(np.real(ss_1)))

    ss_2, ci = power_iter(trans)
    print("Steady state calculated using power iteration:\n" + str(ss_2[0]))
    print(f"Converged in {ci} steps")



if __name__ == "__main__":
    np.set_printoptions(precision=4)
    parser = argparse.ArgumentParser(description="Page rank algorithm")
    parser.add_argument('--file', type=str, required=True)
    parser.add_argument('--rtp', type=bool, required=True)
    args = parser.parse_args()
    main(args)

