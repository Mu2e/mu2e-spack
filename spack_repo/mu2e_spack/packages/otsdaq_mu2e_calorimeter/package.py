# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
import os

def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)

class OtsdaqMu2eCalorimeter(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://mu2e.fnal.gov"
    git = "https://github.com/Mu2e/otsdaq-mu2e-calorimeter.git"
    url = "https://github.com/Mu2e/otsdaq-mu2e-calorimeter/archive/refs/tags/v1_04_00.tar.gz"

    maintainers("eflumerf", "rrivera747")

    license("BSD")

    version("develop", branch="develop", get_full_repo=True)

    version("v8_00_00", commit="40162c58086df92d062e4bc5f6d126474f5e7e89")
    version("v7_01_00", commit="487d43356ccaeb311d9d8b2c85316c0c64f4e50a")
    version("v7_00_00", commit="51048becb31ca04f7b98df7e54df398cecca53ec")
    version("v6_00_00", commit="3e8d6042ad5f8b0582d23417663f29f79c288ce5")
    version("v5_00_00", commit="dcf14e89043bbc292c394fa942dc869ee9981e01")
    version("v4_00_01", commit="a264ab53c3c8f52fb1e80f2ae14c4534ce50320f")
    version("v4_00_00", commit="bdbcff549d87adb1c71e92d35d6d66f8ead0a37a")
    version("v3_04_00", commit="1e89384ec6ee16c2ae6a099f47b68b932a028be2")
    version("v3_03_01", commit="b6f82e51e84a99870a2cf16ea65ee3fec3784215")
    version("v3_03_00", commit="2abf5f4f2e88fed5b8f68a4c65b6916809a07a31")
    version("v3_02_00", commit="28d8a50d574ad4dc6b7638dd2f8a47b0c74b940d")
    version("v3_01_00", commit="a48e8f6cbec21e71b48a9c28095cb37a6ab70ea4")
    version("v3_00_00", commit="196933cfc47d5f9d214218fbc7d8e08bf2569f67")
    version("v1_04_00", sha256="7df9ff2c6f1cdf5d13b7b744b38c24f1e7901c7fac07dc64ccacd80736cea5fa")

    def url_for_version(self, version):
        url = "https://github.com/Mu2e/otsdaq-mu2e-calorimeter/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="20",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("otsdaq-mu2e@:v3_99_00", when="@:v3_99_00")
    depends_on("otsdaq-mu2e@v4_00_00:,develop", when="@v4_00_00:,develop")
    depends_on("otsdaq-suite")
    # Offline dependency added for v4_00_00
    depends_on("Offline@12.00.00:,develop,main", when="@v4_00_00:,develop")
    depends_on("cetmodules@3.26.00:", type="build")

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

        env.prepend_path("MU2E_CALORIMETER_CONFIG_PATH", prefix + "/boardConfig")
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH", "MU2E_CALORIMETER_CONFIG_PATH")

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Ensure we can find fhicl files
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")

        env.prepend_path("MU2E_CALORIMETER_CONFIG_PATH", prefix + "/boardConfig")
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH", "MU2E_CALORIMETER_CONFIG_PATH")
