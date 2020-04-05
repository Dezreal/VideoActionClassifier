import torch
from pyopenpose import op
import numpy as np
import scipy.sparse as sp


def normalize(mx):
    """Row-normalize sparse matrix"""
    rowsum = np.array(mx.sum(1))
    r_inv = np.power(rowsum, -1).flatten()
    r_inv[np.isinf(r_inv)] = 0.
    r_mat_inv = sp.diags(r_inv)
    mx = r_mat_inv.dot(mx)
    return mx


def normalize_on_dim(arr, dim):
    max = np.max(arr, axis=dim, keepdims=True)
    min = np.min(arr, axis=dim, keepdims=True)
    _range = max - min
    return (arr - min) / _range


def sparse_mx_to_torch_sparse_tensor(sparse_mx):
    """Convert a scipy sparse matrix to a torch sparse tensor."""
    sparse_mx = sparse_mx.tocoo().astype(np.float32)
    indices = torch.from_numpy(
        np.vstack((sparse_mx.row, sparse_mx.col)).astype(np.int64))
    values = torch.from_numpy(sparse_mx.data)
    shape = torch.Size(sparse_mx.shape)
    return torch.sparse.FloatTensor(indices, values, shape)


def build_st_body25_graph(frames_per_video):
    # pose_model = op.PoseModel_.BODY_25
    # number_parts = op.getPoseNumberBodyParts(pose_model)
    # part_pairs = op.getPosePartPairs(pose_model)
    part_pairs = [1, 8, 1, 2, 1, 5, 2, 3, 3, 4, 5, 6, 6, 7, 8, 9, 9, 10, 10, 11, 8, 12, 12, 13, 13, 14, 1, 0,
                  0, 15, 15, 17, 0, 16, 16, 18, 2, 17, 5, 18, 14, 19, 19, 20, 14, 21, 11, 22, 22, 23, 11, 24]
    number_parts = 25

    edges = []
    # in_frame edges
    for i in range(0, frames_per_video):
        for j in range(0, len(part_pairs), 2):
            edges.append([part_pairs[j] + number_parts * i, part_pairs[j + 1] + number_parts * i])
    # frame_wise edges
    for i in range(0, frames_per_video - 1):
        for j in range(0, number_parts):
            edges.append([i * number_parts + j, (i + 1) * number_parts + j])

    edges = np.array(edges, dtype=np.uint16)
    adj = sp.coo_matrix((np.ones(len(edges)), (edges[:, 0], edges[:, 1])),
                        shape=(number_parts * frames_per_video, number_parts * frames_per_video),
                        dtype=np.float32)
    # build symmetric adjacency matrix
    adj = adj + adj.T.multiply(adj.T > adj) - adj.multiply(adj.T > adj)
    adj = normalize(adj + sp.eye(adj.shape[0]))
    adj = sparse_mx_to_torch_sparse_tensor(adj)
    return adj


if __name__ == "__main__":
    build_st_body25_graph(1)
