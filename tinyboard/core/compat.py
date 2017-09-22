from __future__ import absolute_import, division, print_function

import logging
import re

INVALID_TAG_CHARS = re.compile(r'[^-/\w\.]')


def clean_tag(name):
    """Convert old tag names (pre-TF 1.3) to new ones.

    Historically, the first argument to summary ops was a tag, which allowed
    arbitrary characters. Now we are changing the first argument to be the node
    name. This function replaces all illegal characters with _s, and logs a
    warning. It also strips leading slashes from the name.

    :param string name: The original name of the tag.
    :returns string: The cleaned tag name.
    """
    if not name:
        return ''
    new_name = INVALID_TAG_CHARS.sub('_', name).lstrip('/')
    if new_name != name:
        logging.info('Summary name {} illegal; using {} instead.'.format(
            name, new_name,
        ))
    return new_name
