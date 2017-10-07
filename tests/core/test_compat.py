from __future__ import absolute_import, division, print_function

import unittest

from tinyboard.core import compat


class TestCompat(unittest.TestCase):

    def test_clean_tag_valid(self):
        assert compat.clean_tag('tinymind') == 'tinymind'
        assert compat.clean_tag('tiny-mind') == 'tiny-mind'

    def test_clean_tag_invalid(self):
        assert compat.clean_tag('!!tiny!!') == '__tiny__'

    def test_clean_tag_none(self):
        assert compat.clean_tag('') == ''
        assert compat.clean_tag(None) == ''
