import torch
import torch.nn.functional as F
from torch import optim
from models import GCN
from data.utils import build_st_body25_graph
from data.dataloader import *

frames_per_video = 5
model = GCN(3, 16, 100, 0.5, frames_per_video)
# optimizer = torch.optim.Adam(model.parameters(),
#                        lr=0.01, weight_decay=5e-4)
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)

adj = build_st_body25_graph(frames_per_video)
train_points, train_labels, test_points, test_labels = load_features_for_old("../data/features.txt", frames_per_video)

train_points = torch.tensor(train_points, dtype=torch.float32)
train_labels = torch.tensor(train_labels[:, 2], dtype=torch.long).reshape((-1, 1)) - 1
test_points = torch.tensor(test_points, dtype=torch.float32)
test_labels = torch.tensor(test_labels[:, 2], dtype=torch.long).reshape((-1, 1)) - 1

# train_labels = torch.zeros(train_labels.shape[0], 9).scatter_(1, train_labels, 1)


def train(epoch):
    model.train()
    for e in range(0, epoch):
        outputs = []
        for i in range(0, train_points.shape[0]):
            input = train_points[i]
            label = train_labels[i]
            output = model(input, adj).reshape((1, -1))
            outputs.append(output)
            # loss = F.nll_loss(output, label)
            # loss.backward()
            # optimizer.step()
            # print loss
        out = torch.cat(outputs, 0)
        loss = F.nll_loss(out, train_labels.reshape(-1))
        # optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print loss


def test():
    # model.eval()
    r = 0
    for i in range(0, test_points.shape[0]):
        pred = model(test_points[i], adj).argmax().item()
        print(str(pred) + "<=>" + str(test_labels[i].item()))
        if int(pred) == int(test_labels[i].item()):
            r = r + 1

    print float(r) / test_points.shape[0]


if __name__ == "__main__":
    train(50)
    print("")
    test()
