

import os
import numpy as np
from easydict import EasyDict as edict

config = edict()
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

config.DETECT = edict()
config.DETECT.model_path='./model/detector.pb'
config.DETECT.topk=10                              ###max boxes
config.DETECT.thres=0.5
config.DETECT.input_shape=(512,512,3)


config.KEYPOINTS = edict()
config.KEYPOINTS.model_path='./model/keypoints.pb'
config.KEYPOINTS.p_num=68
config.KEYPOINTS.base_extend_range=[0.2,0.3]
config.KEYPOINTS.input_shape = (160,160,3)  # input size during training , 240

config.TRACE= edict()
config.TRACE.pixel_thres=1
config.TRACE.smooth_box=0.3
config.TRACE.smooth_landmark=0.95
config.TRACE.iou_thres=0.5

config.DATA = edict()
config.DATA.pixel_means = np.array([123., 116., 103.]) # RGB








