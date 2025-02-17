# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mdh(Package):
    """MDH is specific to Mu2e experiment at Fermilab. It is a layer
    of scripts which simplifies some data-handling steps for users"""

    homepage = "https://github.com/Mu2e/mdh"
    url = "https://github.com/Mu2e/mdh/archive/refs/tags/v01_03_00.tar.gz"
    git = "https://github.com/Mu2e/mdh.git"
    maintainers = ["rlcee", "kutschke"]

    version("1.8.0", sha256="925b3cbd86b4264fcfd745f70f4dbe2392ea49f6c433eadfa303815e3af7d410")
    version("1.7.0", sha256="aa92f1fde4d627871992f59f3ea4ec0b5f6a0cdcae94ef923bd6602a743a0874")
    version("1.6.0", sha256="776c9f2484065b32999b2b4e2501bbdce2f877ecd259ef2e02974a8d688f9271")
    version("1.5.0", sha256="9dd6934b7c322e0e51ea16a5aa7d8fe9d69401db9e4fb7c63377ac387d6c0fab")
    version("1.4.0", sha256="5b1f691ceac32f662ef8e5be35f7f656543565f4c604ad7633746f391681e9ea")
    version("1.3.1", sha256="8a45c234bc0ac98183356095d38aff544832f332a8d6ca3161c51935405e92c4")
    version("1.3.0", sha256="c4c2fd93e92721cea0062fdd27e19e1dbab68fcdd1f8ac005c3ba1fe9ad854ba")
    version("1.2.0", sha256="a15f0fe240c56a5ddd12e5587e5b27bb5fdee52ba93637c68c7f6571400205f3")
    version("1.1.0", sha256="88c3a3e3e4408db9eaf9a9827f24fafb467f0d2ca4d19e606425d3f29f77c994")

    version("develop", branch="main")

    # always take the python from the envset
    depends_on("python@3.9:", type=("run"))
    depends_on("metacat", type=("run"))
    depends_on("data-dispatcher", type=("run"))
    depends_on("rucio-clients", type=("run"))
    # faked with the link
    #depends_on("gfal2-python", type=("run"))

    def url_for_version(self, version):
        url = "https://github.com/Mu2e/Mdh/archive/refs/tags/v{:02d}_{:02d}_{:02d}.tar.gz"
        aa = str(version.dotted).split('.')
        return url.format(int(aa[0]),int(aa[1]),int(aa[2]))

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.python)
        install_tree(self.stage.source_path + "/bin", prefix.bin)
        install_tree(self.stage.source_path + "/python", prefix.python)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.bin)
        if self.version < Version("1.6.0") :
            env.prepend_path("PYTHONPATH", "/usr/lib64/python3.9/site-packages")
        env.prepend_path("PYTHONPATH", self.prefix + "/python")
