import os
import re
import numpy as np
from pyopenpose import op
import cv2


class OpSingleInstance:

    _op_wrapper = op.WrapperPython()
    params = dict()
    params["model_folder"] = "/home/nya-chu/CV/openpose/models/"
    params["net_resolution"] = "400x-1"
    _op_wrapper.configure(params)
    _op_wrapper.start()

    def __init__(self):
        pass

    @property
    def op_wrapper(self):
        return OpSingleInstance._op_wrapper


def cal_rectangle_from_points(keypoints):
    rectangles = []
    for one in keypoints:
        widths = one[:, 1]
        widths = widths.ravel()[np.flatnonzero(widths)]
        left = widths.min()
        right = widths.max()
        heights = one[:, 0]
        heights = heights.ravel()[np.flatnonzero(heights)]
        top = heights.min()
        bottom = heights.max()
        rectangles.append([(top, left), (bottom, right)])
    return rectangles


def cal_area_of_recs(rectangles):
    _areas = [((rec[1][0] - rec[0][0]) * (rec[1][1] - rec[0][1])) for rec in rectangles]
    return _areas


def draw_rectangles(image, rectangles):
    for rectangle in rectangles:
        cv2.rectangle(image, rectangle[0], rectangle[1], (0, 0, 220))


def get_features_from_video_main_one(video_path, n_frame=0):

    op_wrapper = OpSingleInstance().op_wrapper

    cap = cv2.VideoCapture(video_path)
    total_frame = int(cap.get(7))
    # indices = np.linspace(0, total_frame - 1, n_frame, dtype=np.uint8)

    frames = []
    i = 0
    while i < total_frame:
        boo, frame = cap.read()
        frames.append(frame)
        i = i + 1
    # _frames = [frames[j] for j in indices]

    result = []

    for imageToProcess in frames:
        datum = op.Datum()
        datum.cvInputData = imageToProcess
        op_wrapper.emplaceAndPop([datum])

        image = datum.cvOutputData
        n_people = 0
        if not datum.poseKeypoints.size == 1:
            n_people = datum.poseKeypoints.shape[0]

        if n_people == 0:
            print("0!!!")
        elif n_people == 1:
            keypoints = datum.poseKeypoints[0]
            result.append(keypoints)
        else:
            recs = cal_rectangle_from_points(datum.poseKeypoints)
            areas = cal_area_of_recs(recs)
            main = areas.index(max(areas))
            keypoints = datum.poseKeypoints[main]
            # draw_rectangles(image, [recs[main]])
            result.append(keypoints)
        # cv2.imshow("frame", image)
        # cv2.waitKey(10)
    print "done!"
    return result


def get_people_num(video_path):
    op_wrapper = OpSingleInstance().op_wrapper
    cap = cv2.VideoCapture(video_path)
    boo, frame = cap.read()
    # cv2.imshow("f", frame)
    # cv2.waitKey(0)
    datum = op.Datum()
    datum.cvInputData = frame
    op_wrapper.emplaceAndPop([datum])
    if datum.poseKeypoints.size == 1:
        num = 0
    else:
        num = datum.poseKeypoints.shape[0]

    if not num == 1:
        print(num)
        print(video_path)
        with open("n.txt", 'a') as w:
            w.writelines(video_path + '\n')


def list2file(lines, filename):
    with open(filename, 'w') as w:
        for s in lines:
            w.writelines(s + '\n')


def append_feature_to_file(features, filepath, video_name):
    ids = re.sub("\D+", "_", video_name).split("_")
    pre = ids[1] + " " + ids[2] + " " + ids[4] + " "
    with open(filepath, 'a') as w:
        for i, feature in enumerate(features):
            w.write(pre)
            feature = feature.reshape(-1)
            for e in feature:
                w.write(str(e) + " ")
            w.write(str(i) + '\n')
    w.close()


if __name__ == "__main__":
    # files = os.listdir("/datasets/Florence_3d_actions/")
    # for video in files:
    #     if video.endswith(".avi"):
    #         get_people_num("/datasets/Florence_3d_actions/" + video)
    #
    # with open("a.txt", 'r') as r:
    #     for line in r:
    #         line = line.replace("\n", "")
    #         play_video(line)
    files = os.listdir("/datasets/Florence_3d_actions/")
    for video in files:
        if video.endswith(".avi"):
            print video
            features = get_features_from_video_main_one("/datasets/Florence_3d_actions/" + video)
            append_feature_to_file(features, "features.txt", video)

    # get_features_from_video("/datasets/Florence_3d_actions/GestureRecording_Id1actor1idAction1category1.avi")
    # get_features_from_video("/datasets/Florence_3d_actions/GestureRecording_Id1actor2idAction1category1.avi")