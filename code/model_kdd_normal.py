import numpy as np
import pandas as pd
import random

from collections import defaultdict
import pickle
from scipy.sparse import diags, vstack, hstack, lil_matrix, csr_matrix
import networkx as nx
import argparse


def average_opposite_color(from_color, to_color, A, alpha=0.2, iterations=15):
    
    initial_red = np.array([1 for n in from_color])
    norm_initial_red = initial_red/np.sum(initial_red)
    p = np.zeros((1, A.shape[0]))
    p[:,from_color] = norm_initial_red


    # Confirmation bias
    #conf_bias = np.zeros((1, A.shape[0]))
    #conf_bias[:,from_color] = conf_bias[:,from_color] + conf_bias_param*conf_bias[:,from_color]

    #iterations = 15
    p_new = p @ A
    p_new = p_new/np.sum(p_new)
    d = [1/(i+1) for i in p_new[0]]
    diagonal = diags(d, offsets=0)
    D = (diagonal @ A.transpose()).transpose()
    norm = [1/i[0] if i!=0 else 1 for i in np.array(D.sum(axis=1))[:]]
    D = diags(norm, offsets=0) @ D
    rrrr = [np.mean(p_new[:,to_color][p_new[:,to_color]!=0])]
    mmmm = [np.mean(p_new[:,to_color])]
    ssss = [np.sum(p_new[:,to_color])]
    same = [np.sum(p_new[:,from_color])]
    same_avg = [np.mean(p_new[:,from_color])]
    same_avg_ = [np.mean(p_new[:,from_color][p_new[:,from_color]!=0])]
    nnnn = [np.sum(p_new[:,to_color])/(np.sum(p_new[:,to_color])+np.sum(p_new[:,from_color]))]
    
    for it in range(iterations):    
        #conf_bias[:,from_color] = conf_bias[:,from_color] + conf_bias_param*(conf_bias_param*conf_bias[:,from_color])
        p_tmp = (1-alpha)*(p_new @ D) + alpha*(p @ D) #+  bias*conf_bias
        p_tmp = p_tmp/np.sum(p_tmp)
        p_new = p_tmp

        d = [1/(i+1) for i in p_new[0]]
        diagonal = diags(d, offsets=0)

        D = (diagonal @ D.transpose()).transpose()
        norm = [1/i[0] if i!=0 else 1 for i in np.array(D.sum(axis=1))[:]]
        D = diags(norm, offsets=0) @ D
        
        
        #rrrr += [np.mean(p_new[:,to_color][p_new[:,to_color]!=0])]
        #mmmm += [np.mean(p_new[:,to_color])]
        ssss += [np.sum(p_new[:,to_color])]
        same += [np.sum(p_new[:,from_color])]
        #same_avg += [np.mean(p_new[:,from_color])]
        #same_avg_ += [np.mean(p_new[:,from_color][p_new[:,from_color]!=0])]
        #nnnn += [np.sum(p_new[:,to_color])/(np.sum(p_new[:,to_color])+np.sum(p_new[:,from_color]))]
        
    return ssss, same#mmmm#rrrr, mmmm, ssss, same, same_avg, same_avg_, nnnn



parser = argparse.ArgumentParser(description='Process graphs.')
parser.add_argument('--topic', type=str, help='topic name')
parser.add_argument('--sample', type=int, help='number of random samples')

args = parser.parse_args()

MATRIX_FOLDER = 'data/adj_matrix/'
topic = args.topic
sample_iter = int(args.sample)



with open(MATRIX_FOLDER  + topic + '_' + 'uniform' + '_' + '_adj_matrix.p', 'rb') as f_pickle_info:
    A = pickle.load(f_pickle_info)
with open(MATRIX_FOLDER  + topic + '_' + 'uniform' + '_' + 'node_id.p', 'rb') as f_pickle_info:
    node_id = pickle.load(f_pickle_info)
with open(MATRIX_FOLDER  + topic + '_' + 'uniform' + '_' + 'node_color.p', 'rb') as f_pickle_info:
    node_color = pickle.load(f_pickle_info)

id_node = {j:i for i,j in node_id.items()}
# Get nodes
red = []
blue = []
green = []
for n in node_id:
    if node_color[n] == 'R':
        red.append(n)
    elif node_color[n] == 'B':
        blue.append(n)
    elif node_color[n] == 'G':
        green.append(n)

#random_samples = []

#if len(red) < len(blue):
#    for rand_op in range(sample_iter): 
#        random_samples += [random.sample(blue, len(red))]

#elif len(red) > len(blue):
#    for rand_op in range(sample_iter): 
#        random_samples += [random.sample(red, len(blue))]


dictionary_sequences = {}

for alpha in [0, 0.2, 0.5, 0.8, 1]:  
    print(alpha)
    dictionary_sequences[alpha] = {}
    
    
    for kind in ['uniform', 'clicks']:#'position', 
        print(kind)

        #kind = 'uniform'
        with open(MATRIX_FOLDER  + topic + '_' + kind + '_' + '_adj_matrix.p', 'rb') as f_pickle_info:
            A = pickle.load(f_pickle_info)
        with open(MATRIX_FOLDER  + topic + '_' + kind + '_' + 'node_id.p', 'rb') as f_pickle_info:
            node_id = pickle.load(f_pickle_info)
        with open(MATRIX_FOLDER  + topic + '_' + kind + '_' + 'node_color.p', 'rb') as f_pickle_info:
            node_color = pickle.load(f_pickle_info)

        id_node = {j:i for i,j in node_id.items()}
        # Get nodes
        red = []
        blue = []
        green = []
        for n in node_id:
            if node_color[n] == 'R':
                red.append(node_id[n])
            elif node_color[n] == 'B':
                blue.append(node_id[n])
            elif node_color[n] == 'G':
                green.append(node_id[n])

        dictionary_sequences[alpha][kind] = {}
        #dictionary_sequences[alpha][kind]['red'] = {}
        #dictionary_sequences[alpha][kind]['blue'] = {}
        #dictionary_sequences[alpha][kind]['red_red'] = {}
        #dictionary_sequences[alpha][kind]['blue_blue'] = {}


        print(alpha)
        red_repetitions = []
        blue_repetitions = []
        red_red_repetitions = []
        blue_blue_repetitions = []
        #if len(red) < len(blue):
        #    for rand_op in range(sample_iter):
                #print(rand_op)
        #blue_random = [node_id[node] for node in random_samples[rand_op]]#random.sample(blue, len(red))
        sim_rb, sim_rr = average_opposite_color(list(red), list(blue), A, alpha=alpha)
        sim_br, sim_bb = average_opposite_color(list(blue), list(red), A, alpha=alpha)
        red_repetitions += [sim_rb]
        blue_repetitions += [sim_br]
        red_red_repetitions += [sim_rr]
        blue_blue_repetitions += [sim_bb]
                #print(red_repetitions,blue_repetitions)
        #elif len(red) > len(blue):
        #    for rand_op in range(sample_iter):
        #        print(rand_op)
        #        red_random = [node_id[node] for node in random_samples[rand_op]]#random.sample(red, len(blue))
        #        sim_rb, sim_rr = average_opposite_color(list(red_random), list(blue), A, alpha=alpha)
        #        sim_br, sim_bb = average_opposite_color(list(blue), list(red_random), A, alpha=alpha)

        #        red_repetitions += [sim_rb]
        #        blue_repetitions += [sim_br]
        #        red_red_repetitions += [sim_rr]
        #        blue_blue_repetitions += [sim_bb]

        diff_same_red = np.array(red_repetitions)/np.array(red_red_repetitions)
        diff_same_blue = np.array(blue_repetitions)/np.array(blue_blue_repetitions)
        dictionary_sequences[alpha][kind]['red_out_in'] = (np.mean(diff_same_red, axis=0), np.std(diff_same_red, axis=0))#, st.t.interval(0.90, len(diff_same_red)-1, loc=np.mean(diff_same_red), scale=st.sem(diff_same_red)))#uniform_from_red np.std(np.array(red_repetitions), axis=0)
        dictionary_sequences[alpha][kind]['blue_out_in'] = (np.mean(diff_same_blue, axis=0), np.std(diff_same_blue, axis=0))#, st.t.interval(0.90, len(diff_same_blue)-1, loc=np.mean(diff_same_blue), scale=st.sem(diff_same_blue)))#uniform_from_blue
        
        red_to_blue = np.array(red_repetitions)/np.array(blue_repetitions)
        blue_to_red = np.array(blue_repetitions)/np.array(red_repetitions)
        dictionary_sequences[alpha][kind]['red_to_blue'] = (np.mean(red_to_blue, axis=0),np.std(red_to_blue, axis=0))#, st.t.interval(0.90, len(red_to_blue)-1, loc=np.mean(np.array(red_to_blue)), scale=st.sem(np.array(red_to_blue))))#uniform_from_red
        dictionary_sequences[alpha][kind]['blue_to_red'] = (np.mean(blue_to_red, axis=0),np.std(blue_to_red, axis=0))#, st.t.interval(0.90, len(blue_to_red)-1, loc=np.mean(np.array(blue_to_red)), scale=st.sem(np.array(blue_to_red))))#uniform_from_blue

        #dictionary_sequences[alpha][kind]['red'] = (np.mean(np.array(red_repetitions), axis=0), np.std(np.array(red_repetitions), axis=0))#uniform_from_red np.std(np.array(red_repetitions), axis=0)
        #dictionary_sequences[alpha][kind]['blue'] = (np.mean(np.array(blue_repetitions), axis=0),np.std(np.array(blue_repetitions), axis=0))#uniform_from_blue

        
        #dictionary_sequences[alpha][kind]['red_red'] = (np.mean(np.array(red_red_repetitions), axis=0),np.std(np.array(red_red_repetitions), axis=0))#uniform_from_red
        #dictionary_sequences[alpha][kind]['blue_blue'] = (np.mean(np.array(blue_blue_repetitions), axis=0),np.std(np.array(blue_blue_repetitions), axis=0))#uniform_from_blue
            
with open('data/models/' + topic + '_' + 'sequences_KDD_normal.p', 'wb') as f_pickle_info:
    pickle.dump(dictionary_sequences, f_pickle_info)