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

class OtsdaqMu2eTrigger(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://mu2e.fnal.gov"
    git = "https://github.com/Mu2e/otsdaq_mu2e_trigger.git"
    url = "https://github.com/Mu2e/otsdaq_mu2e_trigger/archive/refs/tags/v1_04_00.tar.gz"

    maintainers("eflumerf", "rrivera747")

    license("BSD")

    version("develop", branch="develop", get_full_repo=True)
    version("v3_03_00", commit="e5a81b80574a3f9f42f7db289ddea715279cbdd5")
    version("v3_02_00", commit="c9454dd65511de02331f0e822e34c68e2665b7ff")
    version("v3_01_00", commit="10d134e1178895ddf51c5c9aae97e15ebb703740")
    version("v3_00_00", commit="a3b1c45cf41ffc92f455ca5eb07d9623d7f7a4fc")
    version("v1_04_00", sha256="44a92dcb2c5fa5fb0aa8525062e1254768f6617dd4593402dbfb8de67cd11e48")

    def url_for_version(self, version):
        url = "https://github.com/Mu2e/otsdaq_mu2e_trigger/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    variant(
        "cxxstd",
        default="20",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("otsdaq-mu2e")
    depends_on("Offline")
    depends_on("cetmodules", type="build")

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
