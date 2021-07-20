# Copyright (c) 2016-2017, NVIDIA CORPORATION.  All rights reserved.
from __future__ import absolute_import

from flask_wtf import Form
import os
from wtforms import validators

from digits import utils
from digits.utils import subclass
from digits.utils.forms import validate_required_if_set
from flask_babel import Babel, gettext as _, lazy_gettext


@subclass
class DatasetForm(Form):
    """
    A form used to create an image processing dataset
    """

    def validate_folder_path(form, field):
        if not field.data:
            pass
        else:
            # make sure the filesystem path exists
            if not os.path.exists(field.data) or not os.path.isdir(field.data):
                raise validators.ValidationError(lazy_gettext('Folder does not exist or is not reachable'))
            else:
                return True

    train_image_folder = utils.forms.StringField(
        lazy_gettext(u'Training image folder'),
        validators=[
            validators.DataRequired(),
            validate_folder_path,
        ],
        tooltip=lazy_gettext("Indicate a folder of images to use for training")
    )

    train_label_folder = utils.forms.StringField(
        lazy_gettext(u'Training label folder'),
        validators=[
            validators.DataRequired(),
            validate_folder_path,
        ],
        tooltip=lazy_gettext("Indicate a folder of training labels")
    )

    val_image_folder = utils.forms.StringField(
        lazy_gettext(u'Validation image folder'),
        validators=[
            validate_required_if_set('val_label_folder'),
            validate_folder_path,
        ],
        tooltip=lazy_gettext("Indicate a folder of images to use for training")
    )

    val_label_folder = utils.forms.StringField(
        lazy_gettext(u'Validation label folder'),
        validators=[
            validate_required_if_set('val_image_folder'),
            validate_folder_path,
        ],
        tooltip=lazy_gettext("Indicate a folder of validation labels")
    )

    resize_image_width = utils.forms.IntegerField(
        lazy_gettext(u'Resize Image Width'),
        validators=[
            validate_required_if_set('resize_image_height'),
            validators.NumberRange(min=1),
        ],
        tooltip=lazy_gettext("If specified, images will be resized to that dimension after padding")
    )

    resize_image_height = utils.forms.IntegerField(
        lazy_gettext(u'Resize Image Height'),
        validators=[
            validate_required_if_set('resize_image_width'),
            validators.NumberRange(min=1),
        ],
        tooltip=lazy_gettext("If specified, images will be resized to that dimension after padding")
    )

    padding_image_width = utils.forms.IntegerField(
        lazy_gettext(u'Padding Image Width'),
        default=1248,
        validators=[
            validate_required_if_set('padding_image_height'),
            validators.NumberRange(min=1),
        ],
        tooltip=lazy_gettext("If specified, images will be padded to that dimension")
    )

    padding_image_height = utils.forms.IntegerField(
        lazy_gettext(u'Padding Image Height'),
        default=384,
        validators=[
            validate_required_if_set('padding_image_width'),
            validators.NumberRange(min=1),
        ],
        tooltip=lazy_gettext("If specified, images will be padded to that dimension")
    )

    channel_conversion = utils.forms.SelectField(
        lazy_gettext(u'Channel conversion'),
        choices=[
            ('RGB', lazy_gettext('RGB')),
            ('L', lazy_gettext('Grayscale')),
            ('none', lazy_gettext('None')),
        ],
        default='RGB',
        tooltip=lazy_gettext("Perform selected channel conversion.")
    )

    val_min_box_size = utils.forms.IntegerField(
        lazy_gettext(u'Minimum box size (in pixels) for validation set'),
        default='25',
        validators=[
            validators.InputRequired(),
            validators.NumberRange(min=0),
        ],
        tooltip=lazy_gettext("Retain only the boxes that are larger than the specified "
                "value in both dimensions. This only affects objects in "
                "the validation set. Enter 0 to disable this threshold.")
    )

    custom_classes = utils.forms.StringField(
        lazy_gettext(u'Custom classes'),
        validators=[
            validators.Optional(),
        ],
        tooltip=lazy_gettext("Enter a comma-separated list of class names. "
                "Class IDs are assigned sequentially, starting from 0. "
                "Unmapped class names automatically map to 0. "
                "Leave this field blank to use default class mappings. "
                "See object detection extension documentation for more "
                "information.")
    )
