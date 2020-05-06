import torch
from torch.nn import functional as F
from data.sliding import sliding
from graph import Graph
from model import Model
from utils import get_action_name

graph_args = {"strategy": "spatial"}
graph = Graph(**graph_args)

model = Model(3, 9, graph, edge_importance_weighting=False)
model.load_state_dict(torch.load("model_param.pt"))
model.eval()
path = "/datasets/Florence_3d_actions/GestureRecording_Id1actor1idAction1category1.avi"
for i in sliding(0, 8, stride=1, dilation=1, padding=(1, 1)):
    # print(str(i.__len__()) + str(i[0].shape))
    data = torch.tensor(i, dtype=torch.float32).reshape((1, 8, 25, 3, 1)).permute(0, 3, 1, 2, 4)
    pred = F.log_softmax(model(data), dim=1).argmax()
    print(get_action_name(pred.item()))