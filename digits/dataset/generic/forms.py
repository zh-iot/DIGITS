# Copyright (c) 2016-2017, NVIDIA CORPORATION.  All rights reserved.
from __future__ import absolute_import

import wtforms
from wtforms import validators

from ..forms import DatasetForm
from digits import utils
from flask_babel import Babel, gettext as _, lazy_gettext


class GenericDatasetForm(DatasetForm):
    """
    Defines the form used to create a new GenericDatasetJob
    """
    # Generic dataset options
    dsopts_feature_encoding = utils.forms.SelectField(
        lazy_gettext('Feature Encoding'),
        default='png',
        choices=[('none', lazy_gettext('None')),
                 ('png', lazy_gettext('PNG (lossless)')),
                 ('jpg', lazy_gettext('JPEG (lossy, 90% quality)')),
                 ],
        tooltip=lazy_gettext("Using either of these compression formats can save disk"
                " space, but can also require marginally more time for"
                " training.")
    )

    dsopts_label_encoding = utils.forms.SelectField(
        lazy_gettext('Label Encoding'),
        default='none',
        choices=[
            ('none', lazy_gettext('None')),
            ('png', lazy_gettext('PNG (lossless)')),
            ('jpg', lazy_gettext('JPEG (lossy, 90%% quality)')),
        ],
        tooltip=lazy_gettext("Using either of these compression formats can save disk"
                " space, but can also require marginally more time for"
                " training.")
    )

    dsopts_batch_size = utils.forms.IntegerField(
        lazy_gettext('Encoder batch size'),
        validators=[
            validators.DataRequired(),
            validators.NumberRange(min=1),
        ],
        default=32,
        tooltip=lazy_gettext("Encode data in batches of specified number of entries")
    )

    dsopts_num_threads = utils.forms.IntegerField(
        lazy_gettext('Number of encoder threads'),
        validators=[
            validators.DataRequired(),
            validators.NumberRange(min=1),
        ],
        default=4,
        tooltip=lazy_gettext("Use specified number of encoder threads")
    )

    dsopts_backend = wtforms.SelectField(
        lazy_gettext('DB backend'),
        choices=[
            ('lmdb', lazy_gettext('LMDB')),
        ],
        default='lmdb',
    )

    dsopts_force_same_shape = utils.forms.SelectField(
        lazy_gettext('Enforce same shape'),
        choices=[
            (1, lazy_gettext('Yes')),
            (0, lazy_gettext('No')),
        ],
        coerce=int,
        default=1,
        tooltip=lazy_gettext("Check that each entry in the database has the same shape."
        "Disabling this will also disable mean image computation.")
    )
