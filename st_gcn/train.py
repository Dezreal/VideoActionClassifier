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
        out = F.log_softmax(model(x), dim=1)
        loss = F.nll_loss(out, labels)
        acc = accuracy(out, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print("epoch: %d\tloss: %.4f\tacc: %.3f" % (i + 1, loss.item(), acc))


def test(verbose=False):
    n = tx.shape[0]
    r = 0
    for i in range(n):
        data = tx[i: i+1]
        truth = tl[i]
        pred = F.log_softmax(model(data), dim=1).argmax()
        if pred.item() == truth.item():
            r = r + 1
            if verbose:
                print(str(pred) + " <- " + str(truth))
        else:
            if verbose:
                print(str(pred) + " <- " + str(truth) +
                      get_action_name(pred.item()) + " <- " + get_action_name(truth.item()))
    print("%.3f%% (%d/%d)" % (float(r) * 100 / n, r, n))


if __name__ == "__main__":

    # train(epoch=100)
    # torch.save(model, "model.pt")
    model = torch.load("model.pt")

    model.eval()
    test(verbose=True)
