# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from collections import defaultdict
import os
import sys

from spack.package import *


def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)


class OtsdaqMu2e(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://mu2e.fnal.gov"
    url = "https://github.com/Mu2e/otsdaq-mu2e/archive/refs/tags/v1_02_02.tar.gz"
    git = "https://github.com/Mu2e/otsdaq-mu2e.git"

    maintainers("eflumerf", "rrivera747")

    license("BSD")

    version("develop", branch="develop", get_full_repo=True)

    version("v4_00_00", commit="af80e7917f73dcf06bb40465609be82827f4d26a")
    version("v3_04_00", commit="7f1e42edb3bc1590e6ea5add941aafdaf9222bc2")
    version("v3_03_01", commit="50a13f6747f4e03579c6152440d597b203e96ea0")
    version("v3_03_00", commit="29f817d994f86ebab7868b77c89da7ed700513f9")
    version("v3_02_00", commit="d4fe57c28582a28712f8560d4384654796350068")
    version("v3_01_00", commit="e2438814a42ee1a84a2838eb23fc90c2c8b32f2a")
    version("v3_00_00", commit="e49148cbe548865661def8b51f2c5f64cbf66b71")
    version("v1_04_00", sha256="9c5c2b2b39650cf0716f95a2b3b62f71f4f856cf55810e31f1d9b96c6ddd22de")
    version("v1_03_01", sha256="5b8fb4065ae3733d4280ddb87dd3822637e7ed00f0d7dda9a676abe6921c493d")
    version("v1_02_02", sha256="19334074df56fed7c81e01d8689a50a8ab456e58e01f8ae83fb2461a32ad316a")

    def url_for_version(self, version):
        url = "https://github.com/Mu2e/otsdaq-mu2e/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="20",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("cetmodules@3.26.00:", type="build")

    depends_on("otsdaq@:v3_00_00", when="@:v4_00_00")
    depends_on("otsdaq@v3_00_00:", when="@v4_00_00:,develop")
    depends_on("otsdaq-utilities@:v3_00_00", when="@:v4_00_00")
    depends_on("otsdaq-utilities@v3_00_00:", when="@v4_00_00:,develop")
    depends_on("otsdaq-components@:v3_00_00", when="@:v4_00_00")
    depends_on("otsdaq-components@v3_00_00:", when="@v4_00_00:,develop")
    depends_on("otsdaq-epics@:v3_00_00", when="@:v4_00_00")
    depends_on("otsdaq-epics@v3_00_00:", when="@v4_00_00:,develop")
    depends_on("artdaq-mu2e@:v4_00_00", when="@:v4_00_00")
    depends_on("artdaq-mu2e@v4_00_00:", when="@v4_00_00:,develop")

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
