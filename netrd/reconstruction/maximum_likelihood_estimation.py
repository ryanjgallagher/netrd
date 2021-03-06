"""
maximum_likelihood_estimation.py
---------------------
Reconstruction of graphs using maximum likelihood estimation
author: Brennan Klein
email: brennanjamesklein at gmail dot com
submitted as part of the 2019 NeTSI Collabathon
"""
from .base import BaseReconstructor
import numpy as np
import networkx as nx

class MaximumLikelihoodEstimationReconstructor(BaseReconstructor):
    def fit(self, TS, rate=1.0, stop_criterion=True):
        """
        Given an NxL time series, infer inter-node coupling weights using 
        maximum likelihood estimation methods. 
        After [this tutorial]
        (https://github.com/nihcompmed/network-inference/blob/master/sphinx/codesource/inference.py) 
        in python.
        
        Params
        ------
        TS (np.ndarray): Array consisting of $L$ observations from $N$ sensors.
        rate (float): rate term in maximum likelihood
        stop_criterion (bool): if True, prevent overly-long runtimes
        
        Returns
        -------
        G (nx.Graph or nx.DiGraph): a reconstructed graph.

        """
        
        N, L = np.shape(TS)             # N nodes, length L
        rate = rate / L

        s1 = TS[:,:-1]
        W = np.zeros((N,N))

        nloop = 10000 
        for i0 in range(N):
            st1 = TS[i0,1:]             # time series activity of single node

            w    = np.zeros(N)
            h    = np.zeros(L-1) 
            cost = np.full(nloop,100.)

            for iloop in range(nloop):
                dw = np.dot(s1, (st1 - np.tanh(h)))

                w += rate * dw
                h  = np.dot(s1.T, w)

                cost[iloop] = ((st1 - np.tanh(h))**2).mean()

                if stop_criterion and cost[iloop] >= cost[iloop-1]: 
                    break

            W[i0,:] = w

        # construct the network
        self.results['graph'] = nx.from_numpy_array(W)
        self.results['matrix'] = W
        G = self.results['graph']

        return G