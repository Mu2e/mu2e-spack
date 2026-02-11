# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Codetools(Package):
    """A set of convenience scripts specific to code management of the Mu2e experiment at Fermilab"""

    homepage = "https://github.com/Mu2e/codetools"
    url = "https://github.com/Mu2e/codetools/archive/refs/tags/v1_10.tar.gz"
    git = "https://github.com/Mu2e/codetools.git"
    maintainers = ["rlcee", "kutschke"]

    version("1.10", sha256="e4330546549f3c18d286f2772d6e31e0bffb4b0e103708f323e5a8692dd1e124")
    version("1.9", sha256="332ff5167ee93064b7e84af6e4ccea88947d531863fd816b5ac8ecaef4601a95")
    version("1.8", sha256="98ec9d9ab511175469f22321fc95828a415b715cfb36184d51ef3ae3812be5a4")

    version("develop", branch="main")

    # always take the python from the envset
    #depends_on("python@3.9", type=("build", "run"))

    def url_for_version(self, version):
        url = "https://github.com/Mu2e/codetools/archive/refs/tags/v{:d}_{:d}.tar.gz"
        aa = str(version.dotted).split('.')
        return url.format(int(aa[0]),int(aa[1]))

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.python)
        install_tree(self.stage.source_path + "/bin", prefix.bin)
        install_tree(self.stage.source_path + "/python", prefix.python)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.bin)
        env.prepend_path("PATH", self.prefix+"/KinKal_to_UPS")
        env.prepend_path("PYTHONPATH", self.prefix + "/python")
        env.set("CODETOOLS_DIR",self.prefix)
