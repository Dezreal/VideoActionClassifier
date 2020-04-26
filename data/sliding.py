import cv2
import numpy as np
from pyopenpose import op

from data.feature_creator import OpSingleInstance, cal_rectangle_from_points, cal_area_of_recs


# def linspace(start, num, step=1):
#     result = []
#     for i in range(0, num):
#         result.append(start + step * i)
#     return result


def sliding(video_path, width, stride=1, dilation=1, padding=(0, 0)):
    op_wrapper = OpSingleInstance().op_wrapper
    frames = []
    cap = cv2.VideoCapture(video_path)
    total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for padding_l in range(padding[0]):
        frames.append(np.zeros(shape=(25, 25, 3)))
    n_first = (width - 1) * dilation + 1
    for i in range(n_first - padding[0]):
        datum = op.Datum()
        boo, frame = cap.read()
        datum.cvInputData = frame
        op_wrapper.emplaceAndPop([datum])
        n_people = 0
        if not datum.poseKeypoints.size == 1:
            n_people = datum.poseKeypoints.shape[0]

        if n_people == 0:
            frames.append(np.zeros(shape=(25, 25, 3)))
        elif n_people == 1:
            keypoints = datum.poseKeypoints[0]
            frames.append(keypoints)
        else:
            recs = cal_rectangle_from_points(datum.poseKeypoints)
            areas = cal_area_of_recs(recs)
            main = areas.index(max(areas))
            keypoints = datum.poseKeypoints[main]
            frames.append(keypoints)

    index = slice(0, width * dilation, dilation)
    yield frames[index]





if __name__ == "__main__":
    arr = np.linspace(0, 10, 11)
    print(arr[slice(0, 6, 1)])