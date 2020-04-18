# coding=utf-8
import torch


def accuracy(output, labels, verbose=False):
    x = output.argmax(dim=1)
    y = labels
    right = torch.zeros(x.shape[0])
    right[x == y] = 1
    if verbose:
        for x, y in zip(x, y):
            print(str(x) + " < " + str(y))
            if x != y:
                print(get_action_name(x.item()) + " <- " + get_action_name(y.item()))
    return float(right.sum().item()) / right.shape[0]


def get_action_name(id_category):
    action = {
        0: "wave 挥手",
        1: "drink from a bottle 喝水",
        2: "answer phone 接电话",
        3: "clap 拍手",
        4: "tight lace 系鞋带",
        5: "sit down 坐下",
        6: "stand up 站起",
        7: "read watch 看表",
        8: "bow 鞠躬",
    }
    return action.get(id_category)
