import threading
import time

import torch
from torch.nn import functional as F

from data.sliding import sliding
from model import gcn
from st_gcn.utils import get_action_name


class EvalThread(threading.Thread):

    def __init__(self):
        super(EvalThread, self).__init__()
        self.video_path = ""
        self.model = gcn
        self.model.eval()
        self.info = []
        self._stop = False

    def set_path(self, video_path):
        self.video_path = video_path

    def run(self):
        for i in sliding(self.video_path, 8, stride=1, dilation=1, padding=(1, 1), imshow=False, verbose=True):
            time.sleep(1)
            if self._stop:
                break
            # print(str(i.__len__()) + str(i[0].shape))
            data = torch.tensor(i, dtype=torch.float32).reshape((1, 8, 25, 3, 1)).permute(0, 3, 1, 2, 4)
            pred = F.log_softmax(self.model(data), dim=1).argmax()
            self.info.append(get_action_name(pred.item()))

    def get_info(self):
        str = ""
        for s in self.info:
            str = str + s
        return str

    def stop(self):
        self._stop = True
