import os
import threading
import time

import torch
from torch.nn import functional as F

from data.sliding import sliding
from model import gcn
from st_gcn.utils import get_action_name
from web.db.mysqlpool import Mysql
from web.login import getLastDate

mysql = Mysql()


class EvalThread(threading.Thread):

    def __init__(self):
        super(EvalThread, self).__init__()
        self.video_path = ""
        self.video_name = ""
        self.username = ""
        self.model = gcn
        self.model.eval()
        self.info = []
        self._stop = False

    def set_path(self, video_path, video_name):
        self.video_path = video_path
        self.video_name = video_name

    def set_username(self, username):
        self.username = username

    def run(self):
        for i in sliding(self.video_path + self.video_name,
                         8, stride=2, dilation=1, padding=(1, 1), imshow=False, verbose=True):
            time.sleep(0.1)
            if self._stop:
                break
            # print(str(i.__len__()) + str(i[0].shape))
            data = torch.tensor(i, dtype=torch.float32).reshape((1, 8, 25, 3, 1)).permute(0, 3, 1, 2, 4)
            pred = F.log_softmax(self.model(data), dim=1).argmax()
            self.info.append(get_action_name(pred.item()))
        try:
            os.remove(self.video_path + self.video_name)
        except Exception:
            pass
        if not self._stop:
            self.register_file()

    def get_info(self):
        # str = ""
        # for s in self.info:
        #     str = str + s
        # return str
        return self.info

    def stop(self):
        self._stop = True

    def get_filename_abs(self):
        return self.video_path

    def register_file(self):
        sql = "insert into user_files (username, filename, result, date) values (%s, %s, %s, %s);"
        username = self.username
        filename = self.video_name
        result = self.analysis_result()
        date = getLastDate()
        try:
            mysql.insertOne(sql, [username, filename, result, date])
            mysql.end()
            return True
        except Exception as e:
            print e
            return False

    def analysis_result(self):  # todo weights
        output = dict()
        for i in self.info:
            if output.has_key(i):
                output[i] = output[i] + 1
            else:
                output[i] = 1
        sort = sorted(output.items(), key=lambda x: x[1])
        return sort[-1][0]
