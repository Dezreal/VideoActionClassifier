import sys
from pydoc import help

try:
    sys.path.append('/home/nya-chu/CV/openpose/build/python')
    from openpose import pyopenpose
except ImportError as e:
    raise e


class op:

    PoseModel_ = pyopenpose.PoseModel

    def __init__(self):
        return

    @staticmethod
    def Datum():
        return pyopenpose.Datum()

    @staticmethod
    def Point():
        return pyopenpose.Point()

    @staticmethod
    def PoseModel():
        return pyopenpose.PoseModel()

    @staticmethod
    def Rectangle(*args, **kwargs):
        return pyopenpose.Rectangle(*args, **kwargs)

    @staticmethod
    def WrapperPython():
        return pyopenpose.WrapperPython()

    @staticmethod
    def get_gpu_number():
        return pyopenpose.get_gpu_number()

    @staticmethod
    def get_images_on_directory(image_dir):
        return pyopenpose.get_images_on_directory(image_dir)

    @staticmethod
    def getPoseBodyPartMapping(poseModel):
        return pyopenpose.getPoseBodyPartMapping(poseModel)

    @staticmethod
    def getPoseNumberBodyParts(poseModel):
        return pyopenpose.getPoseNumberBodyParts(poseModel)

    @staticmethod
    def getPosePartPairs(poseModel):
        return pyopenpose.getPosePartPairs(poseModel)

    @staticmethod
    def getPoseMapIndex(poseModel):
        return pyopenpose.getPoseMapIndex(poseModel)

    @staticmethod
    def help():
        help(pyopenpose)