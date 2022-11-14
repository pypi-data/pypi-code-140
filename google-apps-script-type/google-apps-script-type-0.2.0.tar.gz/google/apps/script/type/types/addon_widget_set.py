# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from typing import MutableMapping, MutableSequence

import proto  # type: ignore

__protobuf__ = proto.module(
    package="google.apps.script.type",
    manifest={
        "AddOnWidgetSet",
    },
)


class AddOnWidgetSet(proto.Message):
    r"""The widget subset used by an add-on.

    Attributes:
        used_widgets (MutableSequence[google.apps.script.type.types.AddOnWidgetSet.WidgetType]):
            The list of widgets used in an add-on.
    """

    class WidgetType(proto.Enum):
        r"""The Widget type. DEFAULT is the basic widget set."""
        WIDGET_TYPE_UNSPECIFIED = 0
        DATE_PICKER = 1
        STYLED_BUTTONS = 2
        PERSISTENT_FORMS = 3
        FIXED_FOOTER = 4
        UPDATE_SUBJECT_AND_RECIPIENTS = 5
        GRID_WIDGET = 6
        ADDON_COMPOSE_UI_ACTION = 7

    used_widgets: MutableSequence[WidgetType] = proto.RepeatedField(
        proto.ENUM,
        number=1,
        enum=WidgetType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
