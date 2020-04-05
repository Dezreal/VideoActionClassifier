# coding=utf-8
import scipy.io as scio
import h5py
import numpy as np
import cv2
import utils


def load_features(datasets, frames_per_video):
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
    points = data[:, 3: -1].reshape((-1, frames_per_video, 25, 3)).copy()
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

    train_points = train_points.reshape((-1, 25*frames_per_video, 3))
    test_points = test_points.reshape((-1, 25*frames_per_video, 3))

    # normalize
    train_points = utils.normalize_on_dim(train_points, 1)
    test_points = utils.normalize_on_dim(test_points, 1)

    return train_points.copy(), train_labels.copy(), test_points.copy(), test_labels.copy()


# f = "../FLIC/examples.mat"
# data = scio.loadmat(f)
#
# print(data)
#
# f = "/home/nya-chu/下载/features_cropped/depth_cropped_a02_s01_e01.mat"
# mat = h5py.File(f,mode='r')
# print(mat.keys())
# print(mat.values())
# print(mat['cropped_depth'].shape)
# mat_t = np.transpose(mat['cropped_depth'])
# print(np.array(mat['cropped_depth'][0][0]))

# data = np.loadtxt("/datasets/Florence_3d_actions/Florence_dataset_Features.txt")
if __name__ == "__main__":
    load_features("features.txt", 6)
