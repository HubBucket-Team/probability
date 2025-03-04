# Copyright 2018 The TensorFlow Probability Authors.
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
# ============================================================================
"""TestCase class for use in TensorFlow Probability tests.

Inherits from and adds functionality on top of TensorFlow's tf.test.TestCase.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow.compat.v1 as tf1
import tensorflow.compat.v2 as tf

__all__ = [
    'TestCase',
]


class TestCase(tf.test.TestCase):
  """Class to provide TensorFlow Probability specific test features."""

  def maybe_static(self, x, is_static=True):
    """If `not is_static`, return placeholder_with_default with unknown shape.

    Args:
      x: A `Tensor`
      is_static: a Python `bool`; if True, x is returned unchanged. If False, x
        is wrapped with a tf1.placeholder_with_default with fully dynamic shape.

    Returns:
      maybe_static_x: `x`, possibly wrapped with in a
      `placeholder_with_default` of unknown shape.
    """
    if is_static:
      return x
    else:
      return tf1.placeholder_with_default(x, shape=None)

  def assertAllFinite(self, a):
    """Assert that all entries in a `Tensor` are finite.

    Args:
      a: A `Tensor` whose entries are checked for finiteness.
    """
    is_finite = np.isfinite(self._GetNdArray(a))
    all_true = np.ones_like(is_finite, dtype=np.bool)
    self.assertAllEqual(all_true, is_finite)

  def assertAllNan(self, a):
    """Assert that every entry in a `Tensor` is NaN.

    Args:
      a: A `Tensor` whose entries must be verified as NaN.
    """
    is_nan = np.isnan(self._GetNdArray(a))
    all_true = np.ones_like(is_nan, dtype=np.bool)
    self.assertAllEqual(all_true, is_nan)

  def assertAllNotNone(self, a):
    """Assert that no entry in a collection is None.

    Args:
      a: A Python iterable collection, whose entries must be verified as not
      being `None`.
    """
    each_not_none = [x is not None for x in a]
    if all(each_not_none):
      return

    msg = (
        'Expected no entry to be `None` but found `None` in positions {}'
        .format([i for i, x in enumerate(each_not_none) if not x]))
    raise AssertionError(msg)
