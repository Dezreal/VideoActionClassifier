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

x, l, tx, tl = load_features_for_stgcn("../data/features.txt", 8)
labels = torch.tensor(l[:, 2] - 1, dtype=torch.long)
tl = torch.tensor(tl[:, 2] - 1, dtype=torch.long)

# load graph
graph_args = {"strategy": "spatial"}
graph = Graph(**graph_args)

model = Model(in_channel, num_classes, graph, edge_importance_weighting=False)
optimizer = optim.SGD(model.parameters(), lr=0.09, momentum=0.9)


def train(epoch=100):
    model.train()
    for i in range(epoch):
        # for training
        out = F.log_softmax(model(x), dim=1)
        # for validation
        v_out = F.log_softmax(model(tx), dim=1)
        loss = F.nll_loss(out, labels)
        acc = accuracy(out, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        valid = accuracy(v_out, tl, verbose=False)
        print("epoch: %d\tloss: %.4f\tacc: %.3f\tval: %.4f" % (i + 1, loss.item(), acc, valid))


def test():
    n = tx.shape[0]
    r = 0
    for i in range(n):
        data = tx[i: i+1]
        pred = F.log_softmax(model(data), dim=1).argmax()
        if pred.item() == tl[i].item():
            r = r + 1
    print("%.3f%% (%d/%d)" % (float(r) * 100 / n, r, n))


train(100)

model.eval()
test()

# print("testing")
#
# p = F.log_softmax(model(tx), dim=1)
# print(accuracy(p, tl, verbose=True))
