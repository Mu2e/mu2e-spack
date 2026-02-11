# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from pathlib import Path
from spack.package import *


class Dqm(CMakePackage):
    """The Mu2e Offline Data Quality Monitor"""

    homepage = "https://mu2e.fnal.gov"
    git = "https://github.com/Mu2e/DQM"
    url = "https://github.com/Mu2e/DQM/archive/refs/tags/0.1.0.tar.gz"

    maintainers("tedeschi","rlcee")

    license("Apache-2.0")

    version("main", branch="main", get_full_repo=True)
    version("develop", branch="main", get_full_repo=True)
    version("0.1.0", sha256="")

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

    def cmake_args(self):
        args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
        ]
        if os.path.exists("CMakePresets.cmake"):
            args.extend(["--preset", "default"])
        else:
            self.define("artdaq_core_OLD_STYLE_CONFIG_VARS", True)
        return args

    def setup_run_environment(self, env):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Ensure we can find fhicl files
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
