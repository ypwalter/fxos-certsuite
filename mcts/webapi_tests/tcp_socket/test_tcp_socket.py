# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from mcts.webapi_tests.semiauto import TestCase


class TestTcpSocketFormality(TestCase):
    def test_api_available(self):
        import pdb; pdb.set_trace()
        self.wait_for_obj("window.navigator.mozTCPSocket")
        assertTrue(True, "mozTCPSocket not found")
