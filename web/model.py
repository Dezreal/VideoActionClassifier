import torch

from st_gcn.graph import Graph
from st_gcn.model import Model

graph_args = {"strategy": "spatial"}
graph = Graph(**graph_args)

gcn = Model(3, 9, graph, edge_importance_weighting=False)
gcn.load_state_dict(torch.load("../st_gcn/model_param.pt"))
gcn.eval()