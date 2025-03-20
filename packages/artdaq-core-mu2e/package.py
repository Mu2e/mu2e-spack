# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)


class ArtdaqCoreMu2e(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://mu2e.fnal.gov"
    url = "https://github.com/Mu2e/artdaq-core-mu2e/archive/refs/tags/v1_08_04.tar.gz"
    git = "https://github.com/Mu2e/artdaq-core-mu2e.git"

    maintainers("eflumerf", "rrivera747")

    license("BSD")

    version("develop", branch="develop", get_full_repo=True)

    version("v4_00_00", commit="014d863b4713d42b0fb15c5d97ec2ffd36a83019")
    version("v3_04_00", commit="e023e3e79970a74628aba3cf6b122c50e1fea1de")
    version("v3_03_01", commit="c426d9775165539da76f6a813c007371460652c3")
    version("v3_03_00", commit="27aa987c0a7994c5d558d97c6fb00a3119b259ad")
    version("v3_02_00", commit="f0814116e7aaacbd69c5884fe56c8bbdf2b2d4da")
    version("v3_01_00", commit="ee419440459a7343692ae6042dcbc6653b59b8c5")
    version("v3_00_00", commit="2dcbb50e8495f616c1164a6514371b8314e11b7a")
    version("v2_01_03", sha256="32f1b0b0669beeaf3f85d578e225b04579507590cc3ae7c96f16aacb5aa541d2")
    version("v2_01_02", sha256="cb492dcd67c1676bc78cf251f3541fc583625f8b71f9486e29603f8a104de531")
    version("v1_09_02", sha256="4a2789b7a2bcff2a30b70562e5543d73f503e02eb6a990aa6bb80ceeec614cbf")
    version("v1_09_01", sha256="4f1d6097636ed48f2d0fad5b02ef0ddc2e64d3b75e2f1d1cd41bd2b24df62adb")
    version("v1_08_08", sha256="bfa5a5baf3a9bd2b874f1d0989d73f965b4aec1e820a458b29b5f3668e2a3ff4")
    version("v1_08_04", sha256="a145f195ebc93a2a20e08bcbc227325b03852c5fe0702cfca3ba92ffd91fb398")

    def url_for_version(self, version):
        url = "https://github.com/Mu2e/artdaq-core-mu2e/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="20",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cetmodules@3.26.00:", type="build")

    depends_on("mu2e-pcie-utils@:v2_09_00", when="@:v1_09_02")
    depends_on("artdaq-core@:v4_00_00", when="@:v4_00_00")
    depends_on("artdaq-core@v4_00_00:,develop", when="@v4_00_00:,develop")

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
