"""
Copyright 2018 Oliver Smith

This file is part of pmbootstrap.

pmbootstrap is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pmbootstrap is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pmbootstrap.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import pytest
import sys

# Import from parent directory
pmb_src = os.path.realpath(os.path.join(os.path.dirname(__file__) + "/.."))
sys.path.append(pmb_src)
import pmb.aportgen.device
import pmb.config
import pmb.config.init
import pmb.helpers.logging


@pytest.fixture
def args(tmpdir, request):
    import pmb.parse
    sys.argv = ["pmbootstrap.py", "init"]
    args = pmb.parse.arguments()
    args.log = args.work + "/log_testsuite.txt"
    pmb.helpers.logging.init(args)
    request.addfinalizer(args.logfd.close)
    return args


def test_build_local_src_checks(args):
    func = pmb.helpers.frontend._build_local_src_checks

    # No tree folder defined
    args.linux_tree = "none"
    with pytest.raises(RuntimeError) as e:
        func(args)
    assert str(e.value).startswith("Please specify the path to your local")

    # Package without PMB_LOCAL_SRC
    args.linux_tree = pmb_src
    args.packages = ["hello-world"]
    with pytest.raises(RuntimeError) as e:
        func(args)
    assert "does not use the PMB_LOCAL_SRC" in str(e.value)

    # Package with PMB_LOCAL_SRC raises no exception
    args.linux_tree = pmb_src
    args.packages = ["linux-postmarketos-mainline"]
    func(args)
