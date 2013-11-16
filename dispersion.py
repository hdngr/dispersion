#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2013, Huston Hedinger
# 
# Licensed under the BSD 3 Clause License (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://github.com/hustonhedinger/dispersion/blob/master/LICENSE
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import networkx as nx
import json
from itertools import combinations

def dispersion(network_json, u, exclude_nodes=None, normal=True):
    """ An python implementation of 'dispersion' as defined by Lars Backstrom
    and Jon Kleinberg here: http://arxiv.org/pdf/1310.6753v1.pdf
    :param network_json: a graphAlchemist network json object (example in ./data)
    :param u: the interger id of the ego node of the network
    :param exclude_nodes: a list of ids to exclude from dispersion score
    :param normal: return a dispersion score with basic normalization dispersion/embededness 
    """
    
    exclude_nodes = []
    # initialize a networkx graph object
    G_u = nx.Graph()
    # and create a network from "network_json"
    for edge in network_json['edges']:
        start_node = edge['source']
        end_node = edge['target']
        if start_node in exclude_nodes or end_node in exclude_nodes:
            continue
        G_u.add_edge(start_node, end_node)

    dispersion = dict.fromkeys(G_u, 0.0)

    for v in G_u:
        if v == u:
            continue
        mutual = list(nx.all_simple_paths(G_u, u, v, cutoff=2))
        ST = set()
        embededness = len(mutual)
        for m in mutual:
            if (m[1] == u) or (m[1] == v):
                continue
            else:
                ST.add(m[1])

        possib = combinations(ST, 2)
        total = 0
        #each possible path between s and t
        for p in possib:
            s = p[0]
            t = p[1]
            #iterate through the neigbors of s
            neighbors_s = list(G_u.neighbors_iter(s))
            neighbors_t = list(G_u.neighbors_iter(t))
            Q = []
            for n in neighbors_s:
                #if one of the neigbors is t, no dispersion tick
                if (n == t):
                    score = False
                    break
                #if one of the neighbors is not the ego node, or the node we are
                #scoring dispersion for, add them to the que    
                elif (n != u) and (n != v):
                    Q.append(n)
                #if one of the neigbors is ego or test node, continue because dispersion
                #allows them to connect to other nodes in the network
                elif (n == u) or (n == v):
                    score = True
            #traverse the nodes in the Q       
            if score:
                while Q:
                    i = Q.pop(0)
                    #make sure that s is not directly connected to t
                    #s--t
                    if (i == t):
                        score = False
                        break
                    #make sure that s does not share a neibor with t
                    #s--i--t
                    elif i in neighbors_t:
                        score = False
                        break
                    #continue looping

            #if score is true for the 's' 't' on the possible path called 'p'
            #add a 1 for dispersion
            if score:
                total += 1

        #print total
        dispersion[v] = {'abs_disp': total}
        if normal == True:
            norm_disp = (total/embededness)
            dispersion[v]['norm_disp'] = norm_disp
            
    return dispersion