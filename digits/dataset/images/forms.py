# Copyright (c) 2014-2017, NVIDIA CORPORATION.  All rights reserved.
from __future__ import absolute_import

import wtforms
from wtforms import validators

from ..forms import DatasetForm
from .job import ImageDatasetJob
from digits import utils
from flask_babel import Babel, gettext as _, lazy_gettext


class ImageDatasetForm(DatasetForm):
    """
    Defines the form used to create a new ImageDatasetJob
    (abstract class)
    """

    encoding = utils.forms.SelectField(
        lazy_gettext('Image Encoding'),
        default='png',
        choices=[
            ('none', lazy_gettext('None')),
            ('png', lazy_gettext('PNG (lossless)')),
            ('jpg', lazy_gettext('JPEG (lossy, 90%% quality)')),
        ],
        tooltip=lazy_gettext('Using either of these compression formats can save disk space, '
                 'but can also require marginally more time for training.')
    )

    # Image resize

    resize_channels = utils.forms.SelectField(
        lazy_gettext(u'Image Type'),
        default='3',
        choices=[('1', lazy_gettext('Grayscale')), ('3', lazy_gettext('Color'))],
        tooltip=lazy_gettext("Color is 3-channel RGB. Grayscale is single channel monochrome.")
    )
    resize_width = wtforms.IntegerField(
        lazy_gettext(u'Resize Width'),
        default=256,
        validators=[validators.DataRequired()]
    )
    resize_height = wtforms.IntegerField(
        lazy_gettext(u'Resize Height'),
        default=256,
        validators=[validators.DataRequired()]
    )
    resize_mode = utils.forms.SelectField(
        lazy_gettext(u'Resize Transformation'),
        default='squash',
        choices=ImageDatasetJob.resize_mode_choices(),
        tooltip=lazy_gettext("Options for dealing with aspect ratio changes during resize. See examples below.")
    )
