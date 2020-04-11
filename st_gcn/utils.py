import torch


def accuracy(output, labels, verbose=False):
    x = output.argmax(dim=1)
    y = labels
    right = torch.zeros(x.shape[0])
    right[x == y] = 1
    if verbose:
        for x, y in zip(x, y):
            print(str(x) + ">" + str(y))
    return float(right.sum().item()) / right.shape[0]