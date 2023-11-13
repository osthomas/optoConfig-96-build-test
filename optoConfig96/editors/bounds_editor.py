# ------------------------------------------------------------------------------
# Copyright (c) 2020 Oliver Thomas

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

    # This file incorporates work covered by the following copyright and
    # permission notice:

    # Copyright (c) 2005, Enthought, Inc.
    # All rights reserved.

    # This software is provided without warranty under the terms of the BSD
    # license included in enthought/LICENSE.txt and may be redistributed only
    # under the conditions described in the aforementioned license.  The license
    # is also available online at http://www.enthought.com/licenses/BSD.txt

    # Thanks for using Enthought open source!

# ------------------------------------------------------------------------------


"""
Re-Implementation of traitsui.qt4.extra.bounds_editor to provide extra
validation: min and max cannot be exceeded by entering values in the text box
Furthermore, this suffers from the same limitation as the range editor:
Entering commas treats the value as tuple, not a decimal number, which
raises an unhandled TypeError - fixed here.

Also handles explicitly casting slider values to int for dependency with
Python>=3.10
"""

import six

from traitsui.qt4.extra.bounds_editor import _BoundsEditor as _OriginalBoundsEditor
from traitsui.qt4.extra.range_slider import RangeSlider as OriginalRangeSlider


class _BoundsEditor(_OriginalBoundsEditor):
    def update_low_on_enter(self):
        try:
            text = self._label_lo.text().replace(',', '.')
            self._label_lo.setText(text)
            low = eval(six.text_type(self._label_lo.text()).strip())
            if low < self.min:
                self._label_lo.setText(str(self.min))
        except:
            pass
        super().update_low_on_enter()

    def update_high_on_enter(self):
        try:
            text = self._label_hi.text().replace(',', '.')
            self._label_hi.setText(text)
            high = eval(six.text_type(self._label_hi.text()).strip())
            if high > self.max:
                self._label_hi.setText(str(self.max))
        except:
            pass
        super().update_high_on_enter()


class RangeSlider(OriginalRangeSlider):
    """
    Add additional indirection to the RangeSlider class in order to explicitly
    cast values to int.
    Fix for: https://github.com/enthought/traitsui/issues/1906
    """

    @property
    def _low(self):
        try:
            return int(self.__low)
        except TypeError:
            return self.__low

    @_low.setter
    def _low(self, value):
        self.__low = value

    @property
    def _high(self):
        try:
            return int(self.__high)
        except TypeError:
            return self.__high

    @_high.setter
    def _high(self, value):
        self.__high = value


# Dependency injection of fixed RangeEditor
from traitsui.qt4.extra import bounds_editor as DI_bounds_editor
DI_bounds_editor.RangeSlider = RangeSlider


class BoundsEditor(DI_bounds_editor.BoundsEditor):
    def _get_simple_editor_class(self):
        return _BoundsEditor

    def _get_custom_editor_class(self):
        return _BoundsEditor
