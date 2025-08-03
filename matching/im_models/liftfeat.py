import torch
import numpy as np

from matching import THIRD_PARTY_DIR, BaseMatcher
from matching.utils import to_numpy, resize_to_divisible, add_to_path

add_to_path(THIRD_PARTY_DIR.joinpath("LiftFeat"))
from models.liftfeat_wrapper import LiftFeat, MODEL_PATH


class LyftFeatMatcher(BaseMatcher):
    def __init__(self, device="cpu", detect_threshold=0.05, *args, **kwargs):
        super().__init__(device, **kwargs)

        self.detect_threshold = detect_threshold
        self.model = LiftFeat(weight=MODEL_PATH, detect_threshold=self.detect_threshold)

    def preprocess(self, img):
        "LiftFeat requires input as raw ndarray (result of cv2.imread)"
        # convert axis, (C x H x W) -> (H x W x C)
        if isinstance(img, torch.Tensor):
            img = to_numpy(img).transpose(1, 2, 0)

        assert isinstance(img, np.ndarray), "LiftFeatModel requires input as np.ndarray"

        orig_shape = img.shape[:2]
        return img, orig_shape

    def _forward(self, img0, img1):
        img0, img0_orig_shape = self.preprocess(img0)
        img1, img1_orig_shape = self.preprocess(img1)

        mkpts0, mkpts1 = self.model.match_liftfeat(img0, img1)

        return (
            mkpts0,
            mkpts1,
            None,  # keypoints_0
            None,  # keypoints_1
            None,  # desc0
            None,  # desc1
        )
