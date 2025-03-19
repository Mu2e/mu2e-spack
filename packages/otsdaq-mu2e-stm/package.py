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

class OtsdaqMu2eStm(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://mu2e.fnal.gov"
    git = "https://github.com/Mu2e/otsdaq-mu2e-stm.git"
    url = "https://github.com/Mu2e/otsdaq-mu2e-stm/archive/refs/tags/v1_04_00.tar.gz"

    maintainers("eflumerf", "rrivera747")

    license("BSD")

    version("develop", branch="develop", get_full_repo=True)

    version("v4_00_00", commit="bc0835180191b512d472c9c26fb5c3b7839613d0")
    version("v3_04_00", commit="66abac00f6827c01c84922ed7439949696f72b1b")
    version("v3_03_01", commit="e3a40202b5f53457d3295a6b45d0ae4d3b6de10f")
    version("v3_03_00", commit="bae653f1dba66bed5e34d0572cc64bdd2964e344")
    version("v3_02_00", commit="60f66352d3446926eb74ff4f3b51b3b915a8f343")
    version("v3_01_00", commit="9ee314cff5f4596f8c5f657e412c4d7499ede9d2")
    version("v3_00_00", commit="77137d179a477e956f170baa5443a28ebd2a19f7")
    version("v1_04_00", sha256="242fa56a99a62a1790dbce9bddeb96ccb425e8771c909a96eaf58eba7fc9dd84")

    def url_for_version(self, version):
        url = "https://github.com/Mu2e/otsdaq-mu2e-stm/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="20",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("otsdaq-mu2e@:v4_00_00", when="@:v4_00_00")
    depends_on("otsdaq-mu2e@v4_00_00:", when="@v4_00_00:,develop")
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
