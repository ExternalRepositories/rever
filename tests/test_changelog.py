"""Tests the changelog activity."""
import os

from rever import vcsutils
from rever.logger import current_logger
from rever.main import env_main


REVER_XSH = """
$ACTIVITIES = ['changelog']

$DAG['changelog'].kwargs = {
    'filename': 'CHANGELOG.rst',
    'ignore': ['TEMPLATE.rst'],
    'news': 'nuws',
}
"""
CHANGELOG_RST = """.. current developments

v42.1.0
============
* And some other stuff happeneded.
"""
TEMPLATE_RST = """**Added:**

* <news item>

**Changed:**

* <news item>

**Deprecated:**

* <news item>

**Removed:**

* <news item>

**Fixed:**

* <news item>

**Security:**

* <news item>
"""
N0_RST = """**Added:**

* from n0

**Changed:**

* <news item>

**Deprecated:**

* <news item>

**Removed:**

* here
* and here

**Fixed:**

* <news item>

**Security:**

* <news item>
"""
N1_RST = """**Added:**

* from n1

**Changed:**

* But what martial arts are they mixing?

**Deprecated:**

* <news item>

**Removed:**

* There

**Fixed:**

* <news item>

**Security:** None
"""
CHANGELOG_42_1_1 = """.. current developments

v42.1.1
====================

**Added:**

* from n0
* from n1

**Changed:**

* But what martial arts are they mixing?

**Removed:**

* here
* and here
* There



v42.1.0
============
* And some other stuff happeneded.
"""


def test_changelog(gitrepo):
    os.makedirs('nuws', exist_ok=True)
    files = [('rever.xsh', REVER_XSH),
             ('CHANGELOG.rst', CHANGELOG_RST),
             ('nuws/TEMPLATE.rst', TEMPLATE_RST),
             ('nuws/n0.rst', N0_RST),
             ('nuws/n1.rst', N1_RST),
             ]
    for filename, body in files:
        with open(filename, 'w') as f:
            f.write(body)
    vcsutils.track('.')
    vcsutils.commit('initial changelog and news')
    env_main(['42.1.1'])
    # now see if this worked
    newsfiles = os.listdir('nuws')
    assert 'TEMPLATE.rst' in newsfiles
    assert 'n0.rst' not in newsfiles
    assert 'n1.rst' not in newsfiles
    with open('CHANGELOG.rst') as f:
        cl = f.read()
    assert CHANGELOG_42_1_1 == cl
    # ensure that the updates were commited
    logger = current_logger()
    entries = logger.load()
    assert entries[-2]['rev'] != entries[-1]['rev']


SETUP_XSH = """
$PROJECT = 'castlehouse'
$ACTIVITIES = ['changelog']
$REVER_DIR = 'rvr'

$CHANGELOG_FILENAME = 'CHANGELOG.rst'
$CHANGELOG_NEWS = 'nuws'
$CHANGELOG_TEMPLATE = 'TEMPLATE.rst'
"""

def test_changelog_setup(gitrepo):
    os.makedirs('nuws', exist_ok=True)
    files = [('rever.xsh', SETUP_XSH),
             ]
    for filename, body in files:
        with open(filename, 'w') as f:
            f.write(body)
    vcsutils.track('.')
    vcsutils.commit('initial changelog')
    env_main(['setup'])
    # now see if this worked
    newsfiles = os.listdir('nuws')
    assert 'TEMPLATE.rst' in newsfiles
    basefiles = os.listdir('.')
    assert 'CHANGELOG.rst' in basefiles
    with open('CHANGELOG.rst') as f:
        cl = f.read()
    assert 'castlehouse' in cl
    assert '.gitignore' in basefiles
    with open('.gitignore') as f:
        gi = f.read()
    assert '\n# Rever\nrvr/\n' in gi


CONDA_BUILD_REVER_XSH = """
$ACTIVITIES = ['changelog']
$RELEASE_DATE = "2001-01-02"

$CHANGELOG_FILENAME = "CHANGELOG.txt"
$CHANGELOG_PATTERN = "# current developments"
$CHANGELOG_HEADER = '''# current developments
$RELEASE_DATE $VERSION:
------------------

'''
$CHANGELOG_CATEGORIES = (
    "Enhancements",
    "Bug fixes",
    "Deprecations",
    "Docs",
    "Other",
    )


def title_formatter(category):
    s = category + ':\\n'
    s += "-" * (len(category) + 1)
    s += "\\n\\n"
    return s


$CHANGELOG_CATEGORY_TITLE_FORMAT = title_formatter
$CHANGELOG_AUTHORS_TITLE = "Contributors"
"""
CONDA_BUILD_CHANGELOG_RST = """# current developments

1999-09-12 42.1.0:
------------------
* And some other stuff happeneded.
"""
CONDA_BUILD_TEMPLATE_RST = """Enhancements:
-------------

* <news item>

Bug fixes:
----------

* <news item>

Deprecations:
-------------

* <news item>

Docs:
-----

* <news item>

Other:
------

* <news item>
"""
CONDA_BUILD_N0_RST = """
Enhancements:
-------------

* from n0

Bug fixes:
----------

* <news item>

Deprecations:
-------------

* here
* and here

Docs:
-----

* <news item>

Other:
------

* <news item>
"""
CONDA_BUILD_N1_RST = """
Enhancements:
-------------

* from n1

Bug fixes:
----------

* <news item>

Deprecations:
-------------

* There

Docs:
-----

* But what martial arts are they mixing?

Other:
------

* <news item>
"""
CONDA_BUILD_CHANGELOG_42_1_1 = """# current developments
2001-01-02 42.1.1:
------------------

Enhancements:
-------------

* from n0
* from n1

Deprecations:
-------------

* here
* and here
* There

Docs:
-----

* But what martial arts are they mixing?



1999-09-12 42.1.0:
------------------
* And some other stuff happeneded.
"""


def test_changelog_conda_build_style(gitrepo):
    os.makedirs('news', exist_ok=True)
    files = [('rever.xsh', CONDA_BUILD_REVER_XSH),
             ('CHANGELOG.txt', CONDA_BUILD_CHANGELOG_RST),
             ('news/TEMPLATE', CONDA_BUILD_TEMPLATE_RST),
             ('news/n0', CONDA_BUILD_N0_RST),
             ('news/n1', CONDA_BUILD_N1_RST),
             ]
    for filename, body in files:
        with open(filename, 'w') as f:
            f.write(body)
    vcsutils.track('.')
    vcsutils.commit('initial changelog and news')
    env_main(['42.1.1'])
    # now see if this worked
    newsfiles = os.listdir('news')
    assert 'TEMPLATE' in newsfiles
    assert 'n0' not in newsfiles
    assert 'n1' not in newsfiles
    with open('CHANGELOG.txt') as f:
        cl = f.read()
    assert  CONDA_BUILD_CHANGELOG_42_1_1 == cl
    # ensure that the updates were commited
    logger = current_logger()
    entries = logger.load()
    assert entries[-2]['rev'] != entries[-1]['rev']


