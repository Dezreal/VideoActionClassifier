import cv2
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

arr_text = ["", "", ""]


def put_texts(src):
    color = (10, 10, 220)
    cv2.putText(src, arr_text[0], (20, 20), cv2.FONT_HERSHEY_PLAIN, 1.3, color, 2)
    cv2.putText(src, arr_text[1], (20, 40), cv2.FONT_HERSHEY_PLAIN, 1.3, color, 2)
    cv2.putText(src, arr_text[2], (20, 60), cv2.FONT_HERSHEY_PLAIN, 1.3, color, 2)
    return src


def next_texts(text):
    arr_text[0] = arr_text[1]
    arr_text[1] = arr_text[2]
    arr_text[2] = text


path = "/datasets/Florence_3d_actions/GestureRecording_Id1actor1idAction1category1.avi"
for i, images, indices in sliding(path, 8, stride=1, dilation=1, padding=(1, 1), imshow=False):
    # print(str(i.__len__()) + str(i[0].shape))
    data = torch.tensor(i, dtype=torch.float32).reshape((1, 8, 25, 3, 1)).permute(0, 3, 1, 2, 4)
    pred = F.log_softmax(model(data), dim=1).argmax()
    action = get_action_name(pred.item())
    print(action)
    r = action.rfind(" ")
    action = action[0: r]
    src = images[3]
    text = "frame " + indices[0] + "-" + indices[-1] + ": " + action
    next_texts(text)
    src = put_texts(src)
    cv2.imshow("Sliding", src)
    cv2.waitKey(27)
