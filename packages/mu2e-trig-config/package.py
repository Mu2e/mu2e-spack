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
    url = "https://github.com/Mu2e/mu2e_trig_config/archive/refs/tags/v01_02_00.tar.gz"
    git = "https://github.com/Mu2e/mu2e_trig_config.git"

    maintainers("gianipez", "brownd1978")

    license("Apache-2.0")

    version("main", branch="main", get_full_repo=True)
    version(
        "develop", branch="main", get_full_repo=True
    )  # spack-mpd expects develop version
    version("v3_03_01", commit="e2c8b4dc4f21ccd759d2ac1c21522e0ac54b1b75")
    version("v3_03_00", commit="81759c02641607a4792235bca47c156f1e5b1d64")
    version("v3_02_00", commit="667dc545953b59ed377c7e99bf9de87ce8b9da3c")
    version("v3_01_00", commit="2eb0afc3be6b1895ad4a927cea30c233e2c08fdc")
    version("v01_02_00", commit="25933fed70415367ad6ef1fd3c857bcc66e3bc24")

    def url_for_version(self, version):
        url = "https://github.com/Mu2e/mu2e_pcie_utils/archive/refs/tags/{0}.tar.gz"
        return url.format(version)

    depends_on("cetmodules", type="build")

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
