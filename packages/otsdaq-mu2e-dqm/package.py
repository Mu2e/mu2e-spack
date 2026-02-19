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

class OtsdaqMu2eDqm(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://mu2e.fnal.gov"
    git = "https://github.com/Mu2e/otsdaq-mu2e-dqm.git"
    url = "https://github.com/Mu2e/otsdaq-mu2e-dqm/archive/refs/tags/v1_04_00.tar.gz"

    maintainers("eflumerf", "rrivera747")

    license("BSD")

    version("develop", branch="develop", get_full_repo=True)

    version("v7_01_00", commit="401dd39dfda94c1cc22d3a7c4a103382beecb156")
    version("v7_00_00", commit="a631ee1dbb862e57618f813052fa03516a9764d1")
    version("v6_00_00", commit="6634d1e0810321910984e06833e2f5dc87dcdad4")
    version("v5_00_00", commit="fcfa3fdd6dce62202efeed1387a1717974a0938b")
    version("v4_00_00", commit="d320d43d07847f1aa841daa0cb3a31ea4d55a2de")
    version("v3_04_00", commit="181dcf40b42f0b4ad9cd2d4510347bbd45cf28de")
    version("v3_03_01", commit="8711d0c2cf455a86d7675997d57fcdf76c49ac4e")
    version("v3_03_00", commit="9aa1075a2df5c0fbcfd0bd44723be55ebcf81453")
    version("v3_02_00", commit="c2f4fd5f94cadf8cee755f112dac74a41c1d2612")
    version("v3_01_00", commit="737a5b86614b096f1c29e2655fb20d7bd4a2f7a1")
    version("v3_00_00", commit="793461d0c8baf93c0e5fa2fbf9b29c119517d6e3")
    version("v1_04_00", sha256="363762bd66604d961dd6ec1f4f8cc5651e937456153806b942744ffe1d5246a0")

    def url_for_version(self, version):
        url = "https://github.com/Mu2e/otsdaq-mu2e-dqm/archive/refs/tags/{0}.tar.gz"
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
    depends_on("Offline@:11.99.00", when="@:v3_99_00")
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
