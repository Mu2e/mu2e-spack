# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Muse(Package):
    """Muse is specific to Mu2e expriment at Fermilab. It is a layer
    of scripts which helps users coordinate multiple repos during
    code builds"""

    homepage = "https://github.com/Mu2e/Muse"
    url = "https://github.com/Mu2e/Muse/archive/refs/tags/v4_12_00.tar.gz"
    git = "https://github.com/Mu2e/Muse.git"
    maintainers = ["rlcee", "kutschke"]

    version("4.14.1", sha256="f4dc6896668c8fe78ff25838bad10d6bbd4483560e1ab2d2e3149d17389157d5")
    version("4.14.0", sha256="2afd2f97cd6fff057ada8ad4120cab72ddbd8a7f0891f029a836ac930c0c834e")
    version("4.13.4", sha256="03355e801787377f68047205b8740130c73fa16085661caeb7cef78c884c28c4")
    version("4.13.3", sha256="8618c56a1e52820d7f1e808a51b3588bda4021abb4645c7e596f06c86794455d")
    version("4.13.2", sha256="1570edd1dda5d1c860a275a31aa82587b764aef18d788b66a90eb6bcb2365257")
    version("4.13.1", sha256="6326b161655c3406619a89131452a8132cdf6fa8c77073fb47324fe3a2aae831")
    version("4.13.0",  sha256="35006e6a8d660143153496bd2dd074f4d285b19570aa1978a1091d6a6032ad91")
    version("4.12.0",  sha256="9ac1e979f0c6346889879bf5660e09752ccf892a0ee4b026db897c0d84deff10")
    version("4.11.00", sha256="f7d8a045cca035a9009a9b2e3985031ec89c4dba5b353076aad492cbf490b87c")
    version("4.10.00", sha256="6dc8da6f051a263d80be12c91f7a1e5de0d7e9aaf7758eb64ec5e92dd536c31c")
    version("4.09.02", sha256="a5b769485b3fe79649f78f8e8f21799655c5ef59737e599b70a0ffa36a1bf171")
    version("4.09.01", sha256="fb24611defc2d20ce0d25ef239baa7b0be4586364dd450e0ff30cceb1df9fed0")
    version("4.09.00", sha256="09f3eaa2df1fd90d10596d3e8d58cf30d948e59b2b4e189a2d774e047a73014d")
    version("4.08.00", sha256="df086837e8708e5bbc4d83bd74c67315838964b98ebe77f8cf3eadf28ca8871c")
    version("4.07.01", sha256="02e6d14d1d697929f7c8ef2f03554ebfba0a53c656957776ed8a2c30ded128ba")
    version("4.07.00", sha256="c835861ae8ef286dfe611538939770fe8f5063735e8caa40650b0fcd5029c348")
    version("4.06.00", sha256="2aeb837dc77ceabe38601f03e02c1e371be008e621cdd674019eb773d848aef4")

    version("develop", branch="main")

    # always take the python from the envset
    #depends_on("python@3.9", type=("build", "run"))

    def url_for_version(self, version):
        url = "https://github.com/Mu2e/Muse/archive/refs/tags/v{:1d}_{:02d}_{:02d}.tar.gz"
        aa = str(version.dotted).split('.')
        return url.format(int(aa[0]),int(aa[1]),int(aa[2]))

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        mkdir(prefix.python)
        install_tree(self.stage.source_path + "/bin", prefix.bin)
        install_tree(self.stage.source_path + "/python", prefix.python)
        install_tree(self.stage.source_path + "/config", prefix + "/config")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.bin)
        env.prepend_path("PYTHONPATH", self.prefix + "/python")
        env.set("MUSE_DIR",self.prefix)
        env.set("MUSE_ENVSET_DIR","/cvmfs/mu2e.opensciencegrid.org/DataFiles/Muse")
