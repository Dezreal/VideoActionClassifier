import torch.nn as nn
import torch.nn.functional as F
from GCN.layers import GraphConvolution


class GCN(nn.Module):
    def __init__(self, ninput, nhidden, noutput, dropout, frames_per_video):
        super(GCN, self).__init__()

        self.gc1 = GraphConvolution(ninput, nhidden)
        self.gc2 = GraphConvolution(nhidden, noutput)
        self.dropout = dropout

        self.fc = nn.Sequential(
            nn.Dropout(),
            nn.Linear(25 * noutput * frames_per_video, 100),
            nn.ReLU(),
            nn.Dropout(),
            nn.Linear(100, 9)
        )

    def forward(self, x, adj):
        x = F.relu(self.gc1(x, adj))
        x = F.dropout(x, self.dropout, training=self.training)
        x = self.gc2(x, adj)
        # x =  F.log_softmax(x, dim=1)
        x = x.flatten()
        x = self.fc(x)
        return x
