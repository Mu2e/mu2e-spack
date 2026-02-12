# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *


def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)

class ArtdaqMu2e(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://github.com/Mu2e/artdaq-mu2e"
    url = "https://github.com/Mu2e/artdaq-mu2e/archive/refs/tags/v1_05_02.tar.gz"
    git = "https://github.com/Mu2e/artdaq-mu2e.git"

    maintainers("eflumerf", "rrivera747")

    license("BSD")

    version("develop", branch="develop", get_full_repo=True)

    version("v7_00_00", commit="44ce394bafde2b509c15857ed34305a5ab468aa2")
    version("v6_00_00", commit="f20b4a58befa43052ac6c411a61cbd44752691f4")
    version("v5_00_00", commit="0e5b7bc4b82e9712f045906454faf9a0c64acadc")
    version("v4_00_00", commit="0f7792e86d97d2a401273d28d3ba275a82bb307b")
    version("v3_04_00", commit="83a9e195a7a9e992cf2b12e5a022f5cc59bb81fb")
    version("v3_03_01", commit="ea21383a8e95b2cda4a72c9cfb53f5d94b98963d")
    version("v3_03_00", commit="fc6b9c26023d3cb9ca43a501f2adcea0396e559f")
    version("v3_02_00", commit="f85274201adcf7008393bf36b0613f41498662f5")
    version("v3_01_00", commit="aaddd212757a9aa47a1b0f3a5269ba7d6a027e5a")
    version("v3_00_00", commit="32eceebf0806d729421e5e891591b63f6bd38a6f")
    version("v1_07_00", sha256="46ec46069ce45efc69cd9fc3dce8392255d07940fc44e4baac95f10a6c2d2b9e")
    version("v1_06_01", sha256="b10b287b27bae7c73665809ed67edfe7f692b7435810c0ef476a87ef206de4a0")
    version("v1_05_02", sha256="480fcd8580a11e08de55dbc0e71a16482e0de0ba23a4ac633ff2e2353877d3be")

    def url_for_version(self, version):
        url = "https://github.com/Mu2e/artdaq-mu2e/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="20",
        values=("17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cetmodules@3.26.00:", type="build")

    depends_on("artdaq@:v3_99_00",when="@:v3_99_00")
    depends_on("artdaq@v4_00_00:,develop",when="@v4_00_00:,develop")
    depends_on("mu2e-pcie-utils@:v3_99_00",when="@:v3_99_00")
    depends_on("mu2e-pcie-utils@v4_00_00:,develop",when="@v4_00_00:,develop")

    depends_on("artdaq cxxstd=17", when="cxxstd=17")
    depends_on("artdaq cxxstd=20", when="cxxstd=20")
    depends_on("artdaq-suite")

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
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH")

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Ensure we can find fhicl files
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH")
