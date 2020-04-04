import torch
import torch.nn.functional as F
from models import GCN
from data.utils import build_st_body25_graph
from data.dataloader import load_features

frames_per_video = 10
model = GCN(3, 16, 10, 0.5)
optimizer = torch.optim.Adam(model.parameters(),
                       lr=0.01, weight_decay=5e-4)

adj = build_st_body25_graph(frames_per_video)
train_points, train_labels, test_points, test_labels = load_features("../data/features.txt", frames_per_video)

train_points = torch.tensor(train_points, dtype=torch.float32)
train_labels = torch.tensor(train_labels[:, 2], dtype=torch.long).reshape((-1, 1)) - 1
test_points = torch.tensor(test_points, dtype=torch.float32)
test_labels = torch.tensor(test_labels[:, 2], dtype=torch.long).reshape((-1, 1)) - 1

# train_labels = torch.zeros(train_labels.shape[0], 9).scatter_(1, train_labels, 1)


def train(epoch):
    model.train()
    for e in range(0, epoch):
        for i in range(0, train_points.shape[0]):
            input = train_points[i]
            input = input.reshape((-1, input.shape[-1]))
            label = train_labels[i]
            output = model(input, adj).reshape((1, -1))
            loss = F.nll_loss(output, label)
            loss.backward()
            optimizer.step()
            print loss


def test():
    model.eval()
    r = 0
    for i in range(0, test_points.shape[0]):
        pred = model(test_points[i].reshape((-1, test_points[i].shape[-1])), adj).argmax().item()
        print(str(pred) + str(test_labels[i]))
        if int(pred) == int(test_labels[i].item()):
            r = r + 1

    print float(r) / test_points.shape[0]



if __name__ == "__main__":
    train(1)
    print("")
    test()
