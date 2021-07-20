# Copyright (c) 2014-2017, NVIDIA CORPORATION.  All rights reserved.
from __future__ import absolute_import

import os.path
import requests

import wtforms
from wtforms import validators

from ..forms import ImageDatasetForm
from digits import utils
from digits.utils.forms import validate_required_iff, validate_greater_than
from flask_babel import Babel, gettext as _, lazy_gettext


class ImageClassificationDatasetForm(ImageDatasetForm):
    """
    Defines the form used to create a new ImageClassificationDatasetJob
    """

    backend = wtforms.SelectField(lazy_gettext('DB backend'),
                                  choices=[
                                      ('lmdb', lazy_gettext('LMDB')),
                                      ('hdf5', lazy_gettext('HDF5'))
                                  ],
                                  default='lmdb',
                                  )

    def validate_backend(form, field):
        if field.data == 'lmdb':
            form.compression.data = 'none'
        elif field.data == 'tfrecords':
            form.compression.data = 'none'
        elif field.data == 'hdf5':
            form.encoding.data = 'none'

    compression = utils.forms.SelectField(
        lazy_gettext('DB compression'),
        choices=[
            ('none', lazy_gettext('None')),
            ('gzip', lazy_gettext('GZIP')),
        ],
        default='none',
        tooltip=lazy_gettext('Compressing the dataset may significantly decrease the size '
                 'of your database files, but it may increase read and write times.'),
    )

    # Use a SelectField instead of a HiddenField so that the default value
    # is used when nothing is provided (through the REST API)
    method = wtforms.SelectField(lazy_gettext(u'Dataset type'),
                                 choices=[
                                     ('folder', lazy_gettext('Folder')),
                                     ('textfile', lazy_gettext('Textfiles')),
                                     ('s3', lazy_gettext('S3')),
                                 ],
                                 default='folder',
                                 )

    def validate_folder_path(form, field):
        if not field.data:
            pass
        elif utils.is_url(field.data):
            # make sure the URL exists
            try:
                r = requests.get(field.data,
                                 allow_redirects=False,
                                 timeout=utils.HTTP_TIMEOUT)
                if r.status_code not in [requests.codes.ok, requests.codes.moved, requests.codes.found]:
                    raise validators.ValidationError(lazy_gettext('URL not found'))
            except Exception as e:
                raise validators.ValidationError(lazy_gettext('Caught %(name)s while checking URL: %(url)s', dict(name=type(e).__name__, url=e)))
            else:
                return True
        else:
            # make sure the filesystem path exists
            # and make sure the filesystem path is absolute
            if not os.path.exists(field.data) or not os.path.isdir(field.data):
                raise validators.ValidationError(lazy_gettext('Folder does not exist'))
            elif not os.path.isabs(field.data):
                raise validators.ValidationError(lazy_gettext('Filesystem path is not absolute'))
            else:
                return True

    #
    # Method - folder
    #

    folder_train = utils.forms.StringField(
        lazy_gettext(u'Training Images'),
        validators=[
            validate_required_iff(method='folder'),
            validate_folder_path,
        ],
        tooltip=lazy_gettext('Indicate a folder which holds subfolders full of images. '
                 'Each subfolder should be named according to the desired label for the images that it holds. '
                 'Can also be a URL for an apache/nginx auto-indexed folder.'),
    )

    folder_pct_val = utils.forms.IntegerField(
        lazy_gettext(u'%% for validation'),
        default=25,
        validators=[
            validate_required_iff(method='folder'),
            validators.NumberRange(min=0, max=100)
        ],
        tooltip=lazy_gettext('You can choose to set apart a certain percentage of images '
                 'from the training images for the validation set.'),
    )

    folder_pct_test = utils.forms.IntegerField(
        lazy_gettext(u'%% for testing'),
        default=0,
        validators=[
            validate_required_iff(method='folder'),
            validators.NumberRange(min=0, max=100)
        ],
        tooltip=lazy_gettext('You can choose to set apart a certain percentage of images '
                 'from the training images for the test set.'),
    )

    folder_train_min_per_class = utils.forms.IntegerField(
        lazy_gettext(u'Minimum samples per class'),
        default=2,
        validators=[
            validators.Optional(),
            validators.NumberRange(min=1),
        ],
        tooltip=lazy_gettext('You can choose to specify a minimum number of samples per class. '
                 'If a class has fewer samples than the specified amount it will be ignored. '
                 'Leave blank to ignore this feature.'),
    )

    folder_train_max_per_class = utils.forms.IntegerField(
        lazy_gettext(u'Maximum samples per class'),
        validators=[
            validators.Optional(),
            validators.NumberRange(min=1),
            validate_greater_than('folder_train_min_per_class'),
        ],
        tooltip=lazy_gettext('You can choose to specify a maximum number of samples per class. '
                 'If a class has more samples than the specified amount extra samples will be ignored. '
                 'Leave blank to ignore this feature.'),
    )

    has_val_folder = wtforms.BooleanField(
        lazy_gettext('Separate validation images folder'),
        default=False,
        validators=[
            validate_required_iff(method='folder')
        ]
    )

    folder_val = wtforms.StringField(
        lazy_gettext(u'Validation Images'),
        validators=[
            validate_required_iff(
                method='folder',
                has_val_folder=True),
        ]
    )

    folder_val_min_per_class = utils.forms.IntegerField(
        lazy_gettext(u'Minimum samples per class'),
        default=2,
        validators=[
            validators.Optional(),
            validators.NumberRange(min=1),
        ],
        tooltip=lazy_gettext('You can choose to specify a minimum number of samples per class. '
                 'If a class has fewer samples than the specified amount it will be ignored. '
                 'Leave blank to ignore this feature.'),
    )

    folder_val_max_per_class = utils.forms.IntegerField(
        lazy_gettext(u'Maximum samples per class'),
        validators=[
            validators.Optional(),
            validators.NumberRange(min=1),
            validate_greater_than('folder_val_min_per_class'),
        ],
        tooltip=lazy_gettext('You can choose to specify a maximum number of samples per class. '
                 'If a class has more samples than the specified amount extra samples will be ignored. '
                 'Leave blank to ignore this feature.'),
    )

    has_test_folder = wtforms.BooleanField(
        lazy_gettext('Separate test images folder'),
        default=False,
        validators=[
            validate_required_iff(method='folder')
        ]
    )

    folder_test = wtforms.StringField(
        lazy_gettext(u'Test Images'),
        validators=[
            validate_required_iff(
                method='folder',
                has_test_folder=True),
            validate_folder_path,
        ]
    )

    folder_test_min_per_class = utils.forms.IntegerField(
        lazy_gettext(u'Minimum samples per class'),
        default=2,
        validators=[
            validators.Optional(),
            validators.NumberRange(min=1)
        ],
        tooltip=lazy_gettext('You can choose to specify a minimum number of samples per class. '
                 'If a class has fewer samples than the specified amount it will be ignored. '
                 'Leave blank to ignore this feature.'),
    )

    folder_test_max_per_class = utils.forms.IntegerField(
        lazy_gettext(u'Maximum samples per class'),
        validators=[
            validators.Optional(),
            validators.NumberRange(min=1),
            validate_greater_than('folder_test_min_per_class'),
        ],
        tooltip=lazy_gettext('You can choose to specify a maximum number of samples per class. '
                 'If a class has more samples than the specified amount extra samples will be ignored. '
                 'Leave blank to ignore this feature.'),
    )

    #
    # Method - textfile
    #

    textfile_use_local_files = wtforms.BooleanField(
        lazy_gettext(u'Use local files'),
        default=False,
    )

    textfile_train_images = utils.forms.FileField(
        lazy_gettext(u'Training images'),
        validators=[
            validate_required_iff(method='textfile',
                                  textfile_use_local_files=False)
        ]
    )

    textfile_local_train_images = wtforms.StringField(
        lazy_gettext(u'Training images'),
        validators=[
            validate_required_iff(method='textfile',
                                  textfile_use_local_files=True)
        ]
    )

    textfile_train_folder = wtforms.StringField(lazy_gettext(u'Training images folder'))

    def validate_textfile_train_folder(form, field):
        if form.method.data != 'textfile':
            field.errors[:] = []
            raise validators.StopValidation()
        if not field.data.strip():
            # allow null
            return True
        if not os.path.exists(field.data) or not os.path.isdir(field.data):
            raise validators.ValidationError(lazy_gettext('folder does not exist'))
        return True

    textfile_use_val = wtforms.BooleanField(lazy_gettext(u'Validation set'),
                                            default=True,
                                            validators=[
                                                validate_required_iff(method='textfile')
                                            ]
                                            )
    textfile_val_images = utils.forms.FileField(lazy_gettext(u'Validation images'),
                                                validators=[
                                                    validate_required_iff(
                                                        method='textfile',
                                                        textfile_use_val=True,
                                                        textfile_use_local_files=False)
                                                ]
                                                )
    textfile_local_val_images = wtforms.StringField(lazy_gettext(u'Validation images'),
                                                    validators=[
                                                        validate_required_iff(
                                                            method='textfile',
                                                            textfile_use_val=True,
                                                            textfile_use_local_files=True)
                                                    ]
                                                    )
    textfile_val_folder = wtforms.StringField(lazy_gettext(u'Validation images folder'))

    def validate_textfile_val_folder(form, field):
        if form.method.data != 'textfile' or not form.textfile_use_val.data:
            field.errors[:] = []
            raise validators.StopValidation()
        if not field.data.strip():
            # allow null
            return True
        if not os.path.exists(field.data) or not os.path.isdir(field.data):
            raise validators.ValidationError(lazy_gettext('folder does not exist'))
        return True

    textfile_use_test = wtforms.BooleanField(lazy_gettext(u'Test set'),
                                             default=False,
                                             validators=[
                                                 validate_required_iff(method='textfile')
                                             ]
                                             )
    textfile_test_images = utils.forms.FileField(lazy_gettext(u'Test images'),
                                                 validators=[
                                                     validate_required_iff(
                                                         method='textfile',
                                                         textfile_use_test=True,
                                                         textfile_use_local_files=False)
                                                 ]
                                                 )
    textfile_local_test_images = wtforms.StringField(lazy_gettext(u'Test images'),
                                                     validators=[
                                                         validate_required_iff(
                                                             method='textfile',
                                                             textfile_use_test=True,
                                                             textfile_use_local_files=True)
                                                     ]
                                                     )
    textfile_test_folder = wtforms.StringField(lazy_gettext(u'Test images folder'))

    def validate_textfile_test_folder(form, field):
        if form.method.data != 'textfile' or not form.textfile_use_test.data:
            field.errors[:] = []
            raise validators.StopValidation()
        if not field.data.strip():
            # allow null
            return True
        if not os.path.exists(field.data) or not os.path.isdir(field.data):
            raise validators.ValidationError(lazy_gettext('folder does not exist'))
        return True

    # Can't use a BooleanField here because HTML doesn't submit anything
    # for an unchecked checkbox. Since we want to use a REST API and have
    # this default to True when nothing is supplied, we have to use a
    # SelectField
    textfile_shuffle = utils.forms.SelectField(
        lazy_gettext('Shuffle lines'),
        choices=[
            (1, lazy_gettext('Yes')),
            (0, lazy_gettext('No')),
        ],
        coerce=int,
        default=1,
        tooltip=lazy_gettext("Shuffle the list[s] of images before creating the database.")
    )

    textfile_labels_file = utils.forms.FileField(
        lazy_gettext(u'Labels'),
        validators=[
            validate_required_iff(method='textfile',
                                  textfile_use_local_files=False)
        ],
        tooltip=lazy_gettext("The 'i'th line of the file should give the string label "
                 "associated with the '(i-1)'th numeric label. (E.g. the string label "
                 "for the numeric label 0 is supposed to be on line 1.)"),
    )

    textfile_local_labels_file = utils.forms.StringField(
        lazy_gettext(u'Labels'),
        validators=[
            validate_required_iff(method='textfile',
                                  textfile_use_local_files=True)
        ],
        tooltip=lazy_gettext("The 'i'th line of the file should give the string label "
                 "associated with the '(i-1)'th numeric label. (E.g. the string label "
                 "for the numeric label 0 is supposed to be on line 1.)"),
    )

    #
    # Method - S3
    #

    s3_endpoint_url = utils.forms.StringField(
        lazy_gettext(u'Training Images'),
        tooltip=lazy_gettext('S3 end point URL'),
    )

    s3_bucket = utils.forms.StringField(
        lazy_gettext(u'Bucket Name'),
        tooltip=lazy_gettext('bucket name'),
    )

    s3_path = utils.forms.StringField(
        lazy_gettext(u'Training Images Path'),
        tooltip=lazy_gettext('Indicate a path which holds subfolders full of images. '
                 'Each subfolder should be named according to the desired label for the images that it holds. '),
    )

    s3_accesskey = utils.forms.StringField(
        lazy_gettext(u'Access Key'),
        tooltip=lazy_gettext('Access Key to access this S3 End Point'),
    )

    s3_secretkey = utils.forms.StringField(
        lazy_gettext(u'Secret Key'),
        tooltip=lazy_gettext('Secret Key to access this S3 End Point'),
    )

    s3_keepcopiesondisk = utils.forms.BooleanField(
        lazy_gettext(u'Keep Copies of Files on Disk'),
        tooltip=lazy_gettext('Checking this box will keep raw files retrieved from S3 stored on disk after the job is completed'),
    )

    s3_pct_val = utils.forms.IntegerField(
        lazy_gettext(u'%% for validation'),
        default=25,
        validators=[
            validate_required_iff(method='s3'),
            validators.NumberRange(min=0, max=100)
        ],
        tooltip=lazy_gettext('You can choose to set apart a certain percentage of images '
                 'from the training images for the validation set.'),
    )

    s3_pct_test = utils.forms.IntegerField(
        lazy_gettext(u'%% for testing'),
        default=0,
        validators=[
            validate_required_iff(method='s3'),
            validators.NumberRange(min=0, max=100)
        ],
        tooltip=lazy_gettext('You can choose to set apart a certain percentage of images '
                 'from the training images for the test set.'),
    )

    s3_train_min_per_class = utils.forms.IntegerField(
        lazy_gettext(u'Minimum samples per class'),
        default=2,
        validators=[
            validators.Optional(),
            validators.NumberRange(min=1),
        ],
        tooltip=lazy_gettext('You can choose to specify a minimum number of samples per class. '
                 'If a class has fewer samples than the specified amount it will be ignored. '
                 'Leave blank to ignore this feature.'),
    )

    s3_train_max_per_class = utils.forms.IntegerField(
        lazy_gettext(u'Maximum samples per class'),
        validators=[
            validators.Optional(),
            validators.NumberRange(min=1),
            validate_greater_than('s3_train_min_per_class'),
        ],
        tooltip=lazy_gettext('You can choose to specify a maximum number of samples per class. '
                 'If a class has more samples than the specified amount extra samples will be ignored. '
                 'Leave blank to ignore this feature.'),
    )
