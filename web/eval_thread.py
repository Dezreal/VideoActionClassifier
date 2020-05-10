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
        self.info_detail = []
        self._stop = False
        self.cvOutput = []

    def set_path(self, video_path, video_name):
        self.video_path = video_path
        self.video_name = video_name

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username

    def get_video_name(self):
        return self.video_name

    def run(self):
        for i, o in sliding(self.video_path + self.video_name,
                         8, stride=3, dilation=1, padding=(0, 0), imshow=False, verbose=False):
            time.sleep(0.1)
            self.cvOutput = [o[1], o[5]]
            if self._stop:
                break
            # print(str(i.__len__()) + str(i[0].shape))
            data = torch.tensor(i, dtype=torch.float32).reshape((1, 8, 25, 3, 1)).permute(0, 3, 1, 2, 4)
            sm = F.softmax(self.model(data), dim=1)
            self.info_detail.append(sm.clone().detach().numpy().tolist()[0])
            predict = torch.log(sm).argmax()
            self.info.append(get_action_name(predict.item()))
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
        return self.video_path + self.video_name

    def get_info_detail(self):
        return self.info_detail

    def register_file(self):
        sql = "insert into user_files (username, filename, result, date) values (%s, %s, %s, %s);"
        username = self.username
        filename = self.video_name
        result = self.analysis_result()
        date = getLastDate()
        try:
            mysql.insertOne(sql, [username, filename, result, date])
            mysql.end()
        except Exception as e:
            print e

        sql = 'replace into user_last_file (username, filename, detail, date) values (%s, %s, %s, %s);'
        detail = ''
        for i, once in enumerate(self.info_detail):
            for j, item in enumerate(once):
                detail = detail + ("%.3f" % item)
                if j != once.__len__() - 1:
                    detail = detail + ' '
            if i != self.info_detail.__len__() - 1:
                detail = detail + ','
        try:
            mysql.insertOne(sql, [username, filename, detail, date])
            mysql.end()
        except Exception as e:
            print e

    def analysis_result(self):  # todo weights
        if self.info.__len__() == 0:
            return None
        output = dict()
        for i in self.info:
            if output.has_key(i):
                output[i] = output[i] + 1
            else:
                output[i] = 1
        sort = sorted(output.items(), key=lambda x: x[1])
        return sort[-1][0]

    def get_cv_output(self):
        return self.cvOutput
