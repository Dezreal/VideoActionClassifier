from __future__ import print_function

from torch import optim
from torch.nn import functional as F

from data.dataloader import load_features_for_stgcn
from graph import Graph
from model import Model
from utils import *

in_channel = 3
num_classes = 9

# N, in_channels, T_{in}, V_{in}, M_{in}

x, l, t, tl = load_features_for_stgcn("../data/features.txt", 10)
labels = torch.tensor(l[:, 2] - 1, dtype=torch.long)
tl = torch.tensor(tl[:, 2] - 1, dtype=torch.long)

# load graph
graph_args = dict()
graph = Graph(**graph_args)

model = Model(in_channel, num_classes, graph, edge_importance_weighting=False)
optimizer = optim.SGD(model.parameters(), lr=0.08, momentum=0.9)

model.train()
for i in range(40):
    out = F.log_softmax(model(x), dim=1)
    loss = F.nll_loss(out, labels)
    acc = accuracy(out, labels)
    print("epoch: %d\tloss: %.4f\tacc: %.3f" % (i + 1, loss.item(), acc))
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

# model.eval()
p = F.log_softmax(model(t), dim=1)
print(accuracy(p, tl, verbose=True))
