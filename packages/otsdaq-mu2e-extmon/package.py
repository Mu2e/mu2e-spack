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

class OtsdaqMu2eExtmon(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://mu2e.fnal.gov"
    git = "https://github.com/Mu2e/otsdaq-mu2e-extmon.git"
    url = "https://github.com/Mu2e/otsdaq-mu2e-extmon/archive/refs/tags/v1_04_00.tar.gz"

    maintainers("eflumerf", "rrivera747")

    license("BSD")

    version("develop", branch="develop", get_full_repo=True)

    version("v4_01_00", commit="3da8e6c9e1239049997927af6553221e346c4f56")
    version("v4_00_00", commit="ecef3061a4f4af07b4815372e4fcad09a79f7c31")
    version("v3_04_00", commit="45487ff03d26db846b7bfd75f012bd08550ce777")
    version("v3_03_01", commit="28a6db8f67326889ccf1a48173d0cd7d96b99bb3")
    version("v3_03_00", commit="fc794c683bdc4d352d595995555796d30f0c6a21")
    version("v3_02_00", commit="9e9127ad8d66048095b79af6359f9d5f1f66b2d3")
    version("v3_01_00", commit="eb43178079085ce12a7c6456a0c56cec55b072a2")
    version("v3_00_00", commit="5b9c8e67480435dedcfa20724e3c707fcf508f1e")
    version("v1_04_00", sha256="ee06ffed0f1e013a83be9d7387339b8353f8b53db4ed299dc9dd96ce2d8649a9")

    def url_for_version(self, version):
        url = "https://github.com/Mu2e/otsdaq-mu2e-extmon/archive/refs/tags/{0}.tar.gz"
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
