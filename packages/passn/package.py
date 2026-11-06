# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

import os


class Passn(Package):
    """FHICL scripts for Mu2e offline reco"""

    homepage = "https://github.com/Mu2e/PassN"
    url = "https://github.com/Mu2e/PassN/archive/refs/tags/v00_21_00.tar.gz"
    git = "https://github.com/Mu2e/PassN"

    maintainers("brownd1978", "oksuzian")

    license("Apache-2.0")

    version("main", branch="main", get_full_repo=True)
    version(
        "develop", branch="main", get_full_repo=True
    )  # spack-mpd expects develop version
    version(
        "0.7.0",
        sha256="667ef7430cd5fc76e49b7d01e679e50ed6fecd229c52603067ebeeb044a8c2f7",
    )
    version(
        "0.6.0",
        sha256="375487834b7c50c83046b223b866b38f34ab260bec0509342093c1d67d5ed78a",
    )

    # fcl only: these are needed to run the scripts, not to install them
    depends_on("Offline", type="run")
    depends_on("production", type="run")
    depends_on("mu2e-trig-config", type="run")
    depends_on("event-ntuple", type="run")

    def url_for_version(self, version):
        if version.isdevelop():
            return None
        url = "https://github.com/Mu2e/PassN/archive/refs/tags/v{:02d}_{:02d}_{:02d}.tar.gz"
        aa = str(version.dotted).split(".")
        return url.format(int(aa[0]), int(aa[1]), int(aa[2]))

    def install(self, spec, prefix):
        # PassN fcl refers to itself as "PassN/<subdir>/<file>.fcl", so the tree
        # has to sit under a PassN/ directory on FHICL_FILE_PATH.
        dest = prefix.fcl.PassN
        mkdirp(dest)
        install("*.fcl", dest)
        # take whatever subdirectories upstream has, rather than a fixed list
        for dd in sorted(os.listdir(".")):
            if os.path.isdir(dd) and not dd.startswith("."):
                install_tree(dd, join_path(dest, dd))

    def setup_run_environment(self, env):
        env.prepend_path("FHICL_FILE_PATH", self.prefix.fcl)
