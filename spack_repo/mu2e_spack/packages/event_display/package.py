# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from pathlib import Path
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *


class EventDisplay(CMakePackage):
    """The Mu2e Event Display"""

    homepage = "https://mu2e.fnal.gov"
    git = "https://github.com/Mu2e/EventDisplay"
    url = "https://github.com/Mu2e/EventDisplay/archive/refs/tags/v07_00_01.tar.gz"

    maintainers("sophiemiddleton","NamithaChitrazee","brownd1978")

    license("Apache-2.0")

    version("main", branch="main", get_full_repo=True)
    version("develop", branch="main", get_full_repo=True)

    version("07_00_01", sha256="74c99e67b8e5dbe955da2bedd88acec619ef067bf0ad359214b93e052b941b92")
    version("07_00_00", sha256="280cee943035a2dee4290f6395b73baec201299942a248d9afb7c8140abdcf3c")
    version("06_04_00", sha256="d76efd7d9e604302fa7c35272113ed14e3635d2155e5dbe8a5728ed407e02e6e")

    variant(
        "cxxstd",
        default="20",
        values=("14", "17", "20"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
    )

    # Direct dependencies
    depends_on("Offline")
    depends_on("production")
    depends_on("mu2e-trig-config")

    def url_for_version(self, version):
        url = "https://github.com/Mu2e/EventNtuple/archive/refs/tags/v{:02d}_{:02d}_{:02d}.tar.gz"
        aa = str(version.dotted).split('.')
        return url.format(int(aa[0]),int(aa[1]),int(aa[2]))

    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    def setup_run_environment(self, env):
        prefix = self.prefix
        env.set("ED_DIR", prefix)
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        env.prepend_path("ROOT_LIBRARY_PATH", prefix.lib)
        env.prepend_path("ROOT_INCLUDE_PATH", prefix.include)
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
        env.prepend_path("MU2E_SEARCH_PATH", prefix + "/share")
