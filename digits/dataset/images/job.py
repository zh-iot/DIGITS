# Copyright (c) 2014-2017, NVIDIA CORPORATION.  All rights reserved.
from __future__ import absolute_import

from ..job import DatasetJob
from flask_babel import Babel, gettext as _, lazy_gettext

# NOTE: Increment this every time the pickled object changes
PICKLE_VERSION = 1


class ImageDatasetJob(DatasetJob):
    """
    A Job that creates an image dataset
    """

    def __init__(self, **kwargs):
        """
        Keyword arguments:
        image_dims -- (height, width, channels)
        resize_mode -- used in utils.image.resize_image()
        """
        self.image_dims = kwargs.pop('image_dims', None)
        self.resize_mode = kwargs.pop('resize_mode', None)

        super(ImageDatasetJob, self).__init__(**kwargs)
        self.pickver_job_dataset_image = PICKLE_VERSION

    @staticmethod
    def resize_mode_choices():
        return [
            ('crop', lazy_gettext('Crop')),
            ('squash', lazy_gettext('Squash')),
            ('fill', lazy_gettext('Fill')),
            ('half_crop', lazy_gettext('Half crop, half fill')),
        ]

    def resize_mode_name(self):
        c = dict(self.resize_mode_choices())
        return c[self.resize_mode]
