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

class OtsdaqMu2eCrv(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://mu2e.fnal.gov"
    git = "https://github.com/Mu2e/otsdaq-mu2e-crv.git"
    url = "https://github.com/Mu2e/otsdaq-mu2e-crv/archive/refs/tags/v1_04_00.tar.gz"

    maintainers("eflumerf", "rrivera747")

    license("BSD")

    version("develop", branch="develop", get_full_repo=True)

    version("v4_00_00", commit="d60064f3ee5f045fd5f62cb8bbd90d52c28a0a6e")
    version("v3_04_00", commit="09d8ad6194ebb463721b019f83a947db018ba2fc")
    version("v3_03_01", commit="88d2661aa164ff54740765a327ae976ce964c72a")
    version("v3_03_00", commit="f7e1a8ef3f8710f5db961ec62ef78a28c50114f2")
    version("v3_02_00", commit="13b95db97eed103a563aa25631a8d86c536a88b1")
    version("v3_01_00", commit="9963ca6cb6e9696902a3ab4c5303d69100bcb6b2")
    version("v3_00_00", commit="2d8c4fbca966e0838f4aeb0fa805c818ab6abb5d")
    version("v1_04_00", sha256="c371bfd91be61104eb0964cdbc4ba681dc57a3bb378f81081b1f09674a02c877")

    def url_for_version(self, version):
        url = "https://github.com/Mu2e/otsdaq-mu2e-crv/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="20",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("otsdaq-mu2e@:v4_00_00", when="@:v4_00_00")
    depends_on("otsdaq-mu2e@v4_00_00:,develop", when="@v4_00_00:,develop")
    depends_on("otsdaq-suite")
    depends_on("cetmodules@3.26.00:", type="build")
    depends_on("root+webgui+http+root7")

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
