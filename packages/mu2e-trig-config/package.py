# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *
import os


def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)


class Mu2eTrigConfig(CMakePackage):
    """Trigger configurations for the Mu2e experiment"""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https:/mu2e.fnal.gov"
    url = "https://github.com/Mu2e/mu2e-trig-config/archive/refs/tags/v01_02_00.tar.gz"
    git = "https://github.com/Mu2e/mu2e-trig-config.git"

    maintainers("gianipez", "brownd1978")

    license("Apache-2.0")

    version("main", branch="main", get_full_repo=True)
    version("develop", branch="main", get_full_repo=True)  # spack-mpd expects develop version

    version("v8_01_00", commit="15d4fbf4b029e03a8caf397b5d03783a879124e6")
    version("v8_00_00", commit="dc9ef6de8b4d2bc2b9c68511c1d7c0682b5be7e9")
    version("v7_03_00", commit="284cc216ccc0c22295901d063d78f90533f7dee1")
    version("v7_00_00", commit="332b9bc3b23ff161f976f2ddf7d45240298fdab4")
    version("v6_00_00", commit="c10b1f65e17ac4840a7efc4591b61dc0f26cd980")
    version("v5_00_00", commit="58b79c3377bf88e36dfcdaed4e2c3a7c8a48f341")
    version("v4_00_00", commit="b716190c43c112cdd809a58a4cc14d26fab0d379")
    version("v3_07_00", commit="a2428b1cf5be5d0c27414305c0047bc5865abdd1")
    version("v3_05_00", commit="fa2bba9d587c20a4506fd119634122a8990c11e4")
    version("v3_03_01", commit="e2c8b4dc4f21ccd759d2ac1c21522e0ac54b1b75")
    version("v3_03_00", commit="81759c02641607a4792235bca47c156f1e5b1d64")
    version("v3_02_00", commit="667dc545953b59ed377c7e99bf9de87ce8b9da3c")
    version("v3_01_00", commit="2eb0afc3be6b1895ad4a927cea30c233e2c08fdc")
    version("v01_02_00", commit="25933fed70415367ad6ef1fd3c857bcc66e3bc24")

    def url_for_version(self, version):
        url = "https://github.com/Mu2e/mu2e-trig-config/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    depends_on("cetmodules@3.26.00:", type="build")
    depends_on("python")

    def setup_run_environment(self, env):
        prefix = self.prefix
        # Ensure we can find fhicl files
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
        env.prepend_path("MU2E_SEARCH_PATH", prefix + "/fcl")
        # Ensure we can find data files
        env.prepend_path("MU2E_DATA_PATH", prefix + "/share")
        # Cleaup.
        sanitize_environments(
            env, "FHICL_FILE_PATH", "MU2E_SEARCH_PATH", "MU2E_DATA_PATH"
        )

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find fhicl files
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
        env.prepend_path("MU2E_SEARCH_PATH", prefix + "/fcl")
        # Ensure we can find data files
        env.prepend_path("MU2E_DATA_PATH", prefix + "/share")
        # Cleaup.
        sanitize_environments(
            env, "FHICL_FILE_PATH", "MU2E_SEARCH_PATH", "MU2E_DATA_PATH"
        )
