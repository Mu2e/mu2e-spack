# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Production(Package):
    """Bash and FHICL scripts for Mu2e offline reco and simulation"""

    homepage = "https://github.com/Mu2e/Production"
    url = "https://github.com/Mu2e/Production/archive/refs/tags/v00_21_00.tar.gz"
    git = "https://github.com/Mu2e/Production"
    maintainers = ["brownd1978","kutschke","rlcee"]

    version("main", branch="main")
    version("0.28.0", sha256="6c4d931e4d67e47447c543243f8615e7704fc3ef8cec10f04070ec7b95f25cec")
    version("0.27.0", sha256="436b5aff72a50a11b19a56d5e60c739cc9afb48e1760498ec90bc417f409ade8")
    version("0.26.0", sha256="030dc89ae7c79281cd75c88cfc3b7b2201e2f1da4fb90597e0690ada37d90ab4")
    version("0.25.0", sha256="219498963a2241db613f58480dd22f678cca2ef1ae0840268906d5109bb4e1c9")
    version("0.24.0", sha256="f2b39ce699c2a487304c276f3693d40969a920904e7a283add89fc274a512ef8")
    version("0.23.0", sha256="746c5a967834f273ba7e8271db1728d3824bef83309945e6f8ac0e71a1a3b743")
    version("0.22.0", sha256="a9917606f4d1b0980b8841982d480d9ec16afb3b676210cb57b5018b60d6b1c7")
    version("0.21.0", sha256="e4330546549f3c18d286f2772d6e31e0bffb4b0e103708f323e5a8692dd1e124")


    def url_for_version(self, version):
        url = "https://github.com/Mu2e/Production/archive/refs/tags/v{:02d}_{:02d}_{:02d}.tar.gz"
        aa = str(version.dotted).split('.')
        return url.format(int(aa[0]),int(aa[1]),int(aa[2]))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(self.stage.source_path + "/Scripts/*.sh", prefix.bin)
        install(self.stage.source_path + "/Scripts/POMS/*.sh", prefix.bin)
        for dd in ["JobConfig","Processing","Tests","Validation"] :
            install_tree(self.stage.source_path + "/" + dd,
                         prefix + "/fcl/Production/" + dd)
        install_tree(self.stage.source_path + "/CampaignConfig",
                     prefix + "/share/CampaignConfig/" )

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.bin)
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
