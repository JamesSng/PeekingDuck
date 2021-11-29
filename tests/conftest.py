# Copyright 2021 AI Singapore
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import gc
import os
import shutil
import tempfile
from pathlib import Path

import cv2
import numpy as np
import pytest
import tensorflow.keras.backend as K

TEST_HUMAN_IMAGES = ["t1.jpg", "t2.jpg", "t4.jpg"]
TEST_NO_HUMAN_IMAGES = ["black.jpg", "t3.jpg"]

TEST_NO_LP_IMAGES = ["black.jpg", "t3.jpg"]
TEST_LP_IMAGES = ["tcar1.jpg", "tcar3.jpg", "tcar4.jpg"]

TEST_CROWD_IMAGES = ["crowd1.jpg", "crowd2.jpg"]

PKD_DIR = Path(__file__).resolve().parents[1] / "peekingduck"


@pytest.fixture
def create_image():
    def _create_image(size):
        img = np.random.randint(255, size=size, dtype=np.uint8)
        return img

    return _create_image


@pytest.fixture
def create_input_image(create_image):
    def _create_input_image(path, size):
        img = create_image(size)
        cv2.imwrite(path, img)
        return img

    return _create_input_image


@pytest.fixture
def create_video():
    def _create_video(size, nframes):
        res = [
            np.random.randint(255, size=size, dtype=np.uint8) for _ in range(nframes)
        ]
        return res

    return _create_video


@pytest.fixture
def create_input_video(create_video):
    def _create_input_video(path, fps, size, nframes):
        vid = create_video(size, nframes)
        fourcc = cv2.VideoWriter_fourcc(*"FFV1")
        resolution = (size[1], size[0])
        writer = cv2.VideoWriter(path, fourcc, fps, resolution)
        for frame in vid:
            writer.write(frame)
        return vid

    return _create_input_video


@pytest.fixture
def tmp_dir():
    cwd = Path.cwd()
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)
    yield
    os.chdir(cwd)
    shutil.rmtree(newpath, ignore_errors=True)  # ignore_errors for windows developement


@pytest.fixture(params=TEST_HUMAN_IMAGES)
def test_human_images(request):
    test_img_dir = PKD_DIR.parent / "images" / "testing"

    yield str(test_img_dir / request.param)
    K.clear_session()
    gc.collect()


@pytest.fixture(params=TEST_NO_HUMAN_IMAGES)
def test_no_human_images(request):
    test_img_dir = PKD_DIR.parent / "images" / "testing"

    yield str(test_img_dir / request.param)
    K.clear_session()
    gc.collect()


@pytest.fixture(params=TEST_LP_IMAGES)
def test_lp_images(request):
    test_img_dir = PKD_DIR.parent / "images" / "testing"

    yield str(test_img_dir / request.param)
    K.clear_session()
    gc.collect()


@pytest.fixture(params=TEST_NO_LP_IMAGES)
def test_no_lp_images(request):
    test_img_dir = PKD_DIR.parent / "images" / "testing"

    yield str(test_img_dir / request.param)
    K.clear_session()
    gc.collect()


@pytest.fixture(params=TEST_CROWD_IMAGES)
def test_crowd_images(request):
    test_img_dir = PKD_DIR.parent / "images" / "testing"

    yield str(test_img_dir / request.param)
    K.clear_session()
    gc.collect()
