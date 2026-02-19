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

class OtsdaqMu2eTracker(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://mu2e.fnal.gov"
    git = "https://github.com/Mu2e/otsdaq-mu2e-tracker.git"
    url = "https://github.com/Mu2e/otsdaq-mu2e-tracker/archive/refs/tags/v1_04_00.tar.gz"

    maintainers("eflumerf", "rrivera747")

    license("BSD")

    version("develop", branch="develop", get_full_repo=True)

    version("v8_00_00", commit="87784fd40559aa6380afdb58133ec1b1f71f3ede")
    version("v7_00_00", commit="f294dcaa30ef7a0d92a783a54949406835c9973f")
    version("v6_00_00", commit="3b81e543b5f1358a21f520d93d48bbee3a35f239")
    version("v5_00_00", commit="4a4ffb706592034945e529183e6b2ead6eeba355")
    version("v4_00_00", commit="31ecebcd40c26e98b8a33c21a2a5bedadafb46f8")
    version("v3_04_00", commit="15e98583e9f0c4dab6f2b6d26ced5bf46de8b049")
    version("v3_03_01", commit="22cd17fe4aa21f82ee0f42682992a3c3c2e2dbf1")
    version("v3_03_00", commit="0911662b152a239faff831625985e8c30b6c8357")
    version("v3_02_00", commit="aca901c7655eee59bab3ca6b42ed354e8d7f7bac")
    version("v3_01_00", commit="e7b7abb733e00e8a97f31f02f87746fb29c4949e")
    version("v3_00_00", commit="a93e0362837d38271002a5c700f7d140d115773e")

    def url_for_version(self, version):
        url = "https://github.com/Mu2e/otsdaq-mu2e-tracker/archive/refs/tags/{0}.tar.gz"
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
    depends_on("artdaq-core-demo@:v1_99_00", when="@:v3_99_00")
    depends_on("artdaq-core-demo@v2_00_00:,develop", when="@v4_00_00:,develop")
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
