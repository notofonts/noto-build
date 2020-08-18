# Copyright 2020 Christopher Simpkins

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

from fontbakery.checkrunner import Section, PASS, FAIL
from fontbakery.callable import check
from fontbakery.fonts_profile import profile_factory

profile_imports = ()
profile = profile_factory(
    default_section=Section("An always pass custom profile for testing")
)

ALWAYSPASS_PROFILE_CHECKS = [
    "com.google.fonts/check/testing/alwayspass",
]


@check(
    id="com.google.fonts/check/testing/alwayspass",
    rationale="""
    This is an always passing fontbakery check for testing purposes.
    """,
)
def com_google_fonts_check_testing_alwayspass(ttFonts):
    """This is an always passing fontbakery check for testing purposes."""
    try:

        tests_passed = True
        for tt in ttFonts:
            pass

        if tests_passed:
          yield PASS, "This test always passes."

    except Exception as e:
        sys.stderr.write("[ERROR]: {}".format(str(e)))
        sys.exit(1)


# ================================================
#
# End check definitions
#
# ================================================

profile.auto_register(globals())
profile.test_expected_checks(ALWAYSPASS_PROFILE_CHECKS, exclusive=True)