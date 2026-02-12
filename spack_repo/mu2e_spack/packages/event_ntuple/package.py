# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from pathlib import Path
from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *


class EventNtuple(CMakePackage):
    """The Mu2e Analysis Ntuple"""

    homepage = "https://mu2e.fnal.gov"
    git = "https://github.com/Mu2e/EventNtuple"
    url = "https://github.com/Mu2e/EventNtuple/archive/refs/tags/v06_01_01.tar.gz"

    maintainers("AndrewEdmonds11","brownd1978")

    license("Apache-2.0")

    version("main", branch="main", get_full_repo=True)
    version("develop", branch="main", get_full_repo=True)
    version("6.1.1", sha256="6a12d4f7434d17f28e93ffce3c702f0171aec39efcf5f1b147d34d6f325f5fb2")

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
        env.set("EN_DIR", prefix)
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        env.prepend_path("ROOT_LIBRARY_PATH", prefix.lib)
        env.prepend_path("ROOT_INCLUDE_PATH", prefix.include)
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
        env.prepend_path("PYTHONPATH", prefix + "/python/utils")
        env.prepend_path("PYTHONPATH", prefix + "/python/utils/helper")
        env.prepend_path("PYTHONPATH", prefix + "/python/utils/pyutils")
