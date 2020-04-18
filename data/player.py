import cv2


def play_video(path):
    cap = cv2.VideoCapture(path)
    num_frame = cap.get(7)
    print num_frame
    i = 0
    while i < num_frame:
        boo, frame = cap.read()
        width = frame.shape[1]
        cv2.imshow("video", frame)
        cv2.waitKey(80)
        i = i + 1


if __name__ == "__main__":
    idvideo = 19
    idactor = 6
    idcategory = 9
    video = "GestureRecording_Id%dactor%didAction%dcategory%d.avi" % (idvideo, idactor, idvideo, idcategory)
    path = "/datasets/Florence_3d_actions/" + video
    play_video(path)