import cv2
import numpy as np
from pyopenpose import op

from data.feature_creator import OpSingleInstance, cal_rectangle_from_points, cal_area_of_recs


def get_keypoints(image2process):
    """
    get pose key points and output of the image(frame)
    :param image2process: one frame data
    :return: (datum.poseKeypoints, datum.cvOutputData)
    """
    op_wrapper = OpSingleInstance().op_wrapper
    datum = op.Datum()
    datum.cvInputData = image2process
    op_wrapper.emplaceAndPop([datum])
    n_people = 0
    if not datum.poseKeypoints.size == 1:
        n_people = datum.poseKeypoints.shape[0]

    if n_people == 0:
        return np.zeros(shape=(25, 3)), datum.cvOutputData
    elif n_people == 1:
        keypoints = datum.poseKeypoints[0]
        return keypoints, datum.cvOutputData
    else:
        recs = cal_rectangle_from_points(datum.poseKeypoints)
        areas = cal_area_of_recs(recs)
        main = areas.index(max(areas))
        keypoints = datum.poseKeypoints[main]
        return keypoints, datum.cvOutputData


def sliding(video_path, width, stride=1, dilation=1, padding=(0, 0), verbose=True, imshow=True):
    wait_key = 10

    frames = []
    start = 0
    end = width * dilation
    cap = cv2.VideoCapture(video_path)
    # for image show
    cvOutputs = []
    w_frame = int(cap.get(3))
    h_frame = int(cap.get(4))
    # for printing msg
    frame_idx = None
    if verbose:
        total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if video_path == 0:
            total_frame = 1 * 10 ** 4
        frame_idx = ["+" for _ in range(padding[0])]
        frame_idx.extend([str(n) for n in range(0, total_frame)])
        frame_idx.extend(["+" for _ in range(padding[1])])

    for padding_l in range(padding[0]):
        frames.append(np.zeros(shape=(25, 3)))
        cvOutputs.append(np.zeros(shape=(w_frame, h_frame, 3)))

    n_first = (width - 1) * dilation + 1
    for _ in range(n_first - padding[0]):
        boo, frame = cap.read()
        key, output = get_keypoints(frame)
        frames.append(key)
        cvOutputs.append(output)
        if imshow:
            cv2.imshow(str(video_path), output)
            cv2.waitKey(wait_key)

    n = 0
    padding_r = padding[1]
    while True:
        if n % stride == 0:
            index = slice(start, end, dilation)
            if verbose:
                print(frame_idx[index])
            yield frames[index], cvOutputs[index]
            start = start + stride
            end = end + stride
        n = n + 1

        boo, frame = cap.read()
        if not boo:
            if padding_r <= 0:
                break
            else:
                frames.append(np.zeros(shape=(25, 3)))
                cvOutputs.append(np.zeros(shape=(w_frame, h_frame, 3)))
                padding_r = padding_r - 1
        else:
            key, output = get_keypoints(frame)
            if imshow:
                cv2.imshow(str(video_path), output)
                cv2.waitKey(wait_key)
            frames.append(key)
            cvOutputs.append(output)

# if __name__ == "__main__":
#     path = "/datasets/Florence_3d_actions/GestureRecording_Id1actor1idAction1category1.avi"
#     for i in sliding(path, 8, stride=1, dilation=1, padding=(3, 3)):
#         print(str(i.__len__()) + str(i[0].shape))
