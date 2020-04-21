# coding=utf-8
import numpy as np
import torch

import utils

# number of key points
NUM_V = 25


def load_features(datasets, frames_per_video):
    """

    :param datasets: file path
    :param frames_per_video: T
    :return: shape = [N, T, V, C]
    """
    data = np.loadtxt(datasets)

    frames_0th = np.argwhere(data[:, -1] == 0)
    num_sequences = frames_0th.size

    # the index of frames we need
    index = []
    for i, start in enumerate(frames_0th):
        if i == num_sequences - 1:
            end = data.shape[0] - 1
        else:
            end = frames_0th[i + 1] - 1
        index.extend(np.linspace(start, end, frames_per_video, dtype=np.uint16).tolist())

    index = [i for item in index for i in item]
    data = data[index, :]

    # sort by (actor > action > category > frame)
    actor = data[:, 1]
    frame = data[:, -1]
    action = data[:, 0]
    category = data[:, 2]
    index = np.lexsort((frame, category, action, actor))
    data = data[index]

    # get data and labels
    points = data[:, 3: -1].reshape((-1, frames_per_video, NUM_V, 3)).copy()
    labels = data[:, :3].reshape((-1, frames_per_video, 3))[:, 0, :].copy()

    # split train and test data
    actor_test = 10
    train_index = np.argwhere(labels[:, 1] != actor_test).reshape(-1)
    test_index = np.argwhere(labels[:, 1] == actor_test).reshape(-1)
    train_points = points[train_index]
    test_points = points[test_index]
    train_labels = labels[train_index]
    test_labels = labels[test_index]

    # shuffle train data
    shuffle = np.arange(train_points.shape[0])
    np.random.shuffle(shuffle)
    train_points = train_points[shuffle]
    train_labels = train_labels[shuffle]

    train_points = train_points.reshape((-1, NUM_V * frames_per_video, 3))
    test_points = test_points.reshape((-1, NUM_V * frames_per_video, 3))

    # normalize
    # train_points = utils.normalize_on_dim(train_points, 1)
    # test_points = utils.normalize_on_dim(test_points, 1)

    return train_points.copy(), train_labels.copy(), test_points.copy(), test_labels.copy()


def load_features_for_old(datasets, frames_per_video):
    train_points, train_labels, test_points, test_labels = load_features(datasets, frames_per_video)
    # normalize
    train_points = utils.normalize_on_dim(train_points, 1)
    test_points = utils.normalize_on_dim(test_points, 1)
    return train_points.copy(), train_labels.copy(), test_points.copy(), test_labels.copy()


def load_features_for_stgcn(datasets, frames_per_video):
    train_points, train_labels, test_points, test_labels = load_features(datasets, frames_per_video)
    train_points = torch.tensor(train_points, dtype=torch.float32)
    N, TVM, C = train_points.shape
    train_points = train_points.reshape((N, frames_per_video, NUM_V, C, 1))
    train_points = train_points.permute(0, 3, 1, 2, 4)
    test_points = torch.tensor(test_points, dtype=torch.float32)
    N, TVM, C = test_points.shape
    test_points = test_points.reshape((N, frames_per_video, NUM_V, C, 1))
    test_points = test_points.permute(0, 3, 1, 2, 4)
    return train_points.contiguous(), train_labels.copy(), test_points.contiguous(), test_labels.copy()


if __name__ == "__main__":
    train_data, _, test_data, _ = load_features_for_stgcn("features.txt", 6)
