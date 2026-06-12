# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from pathlib import Path
from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage


class ArtAnalysis(CMakePackage):
    """Mu2e Art Modules for Analysis"""

    homepage = "https://mu2e.fnal.gov"
    git = "https://github.com/Mu2e/ArtAnalysis"
    url = "https://github.com/Mu2e/ArtAnalysis/archive/refs/tags/v00_01_00.tar.gz"

    maintainers("brownd1978", "rlcee")

    license("Apache-2.0")

    version("main", branch="main", get_full_repo=True)
    version("develop", branch="main", get_full_repo=True)

    version(
        "00_01_00",
        sha256="102597a16d8428fb9cd8c61b43235503ca3aff0809f9805603df00534216bc87",
    )

    variant(
        "cxxstd",
        default="20",
        values=("14", "17", "20"),
        multi=False,
        sticky=True,
        description="Use the specified C++ standard when building.",
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # Direct dependencies
    depends_on("Offline")
    depends_on("production")
    depends_on("mu2e-trig-config")

    def url_for_version(self, version):
        url = "https://github.com/Mu2e/EventNtuple/archive/refs/tags/v{:02d}_{:02d}_{:02d}.tar.gz"
        aa = str(version.dotted).split(".")
        return url.format(int(aa[0]), int(aa[1]), int(aa[2]))

    def cmake_args(self):
        return [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

    def setup_run_environment(self, env):
        prefix = self.prefix
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        env.prepend_path("ROOT_LIBRARY_PATH", prefix.lib)
        env.prepend_path("ROOT_INCLUDE_PATH", prefix.include)
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
