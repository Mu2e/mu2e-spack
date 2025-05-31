# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import glob
import os
import sys

from spack import *

#def patcher(x):
#    cetmodules_20_migrator(".", "cry", "1.7")


class Crvteststand(MakefilePackage):
    """performs calibration and reco on midas readout of Mu2e CRV teststand data."""

    homepage = "https://github.com/Mu2e/CRVteststand"
    url = "https://github.com/Mu2e/CRVteststand/archive/refs/tags/v19.tar.gz"
    git = "https://github.com/Mu2e/CRVteststand.git"
    maintainers = ["ehrlich-uva","YongyiBWu","rlcee", "kutschke"]


    version("develop", branch="main")

    depends_on("root", type=["build","link","run"])

    version("24", sha256="3ada16bc046fbc83af41954526bd28de1e056f95665dd2b135888beace717df1")
    version("23", sha256="b70961b1c3ee0b781dd61711ffd7fce92f5c857715eee028fccbb5108d63ac8a")
    version("22", sha256="50e0d46dd07db72b24cd9f21ab98fe3e4be06b76ad736a81d3c6992a2445236b")
    version("21", sha256="65f6b344b358e43138339bf64cf522d7dfade64560a5ddeeba07d0db8d34ccfc")
    version("20", sha256="103186d06fdac5c0bfee98f6c6a914a38aa725886d0457d65e7f4f41be8b2da2")
    version("19", sha256="154f71916d174e3adc1fe44fe0b3034696a7d28150071a05412eb9f8c9203fc3")
    version("18", sha256="cbb11690851d0b8f8c8cf9b5011593b3825541ec3275c0052a0ed2260d2de850")
    version("17", sha256="3e68dd48cc04056fbde93708033c5b4758b9405a0ca7fec8b8a1e6f10a720aff")
    version("16", sha256="9562ef0bdd67860add49acc1dedf6e4d22a135194a9e5ae300c15653a5392998")
    version("15", sha256="fdc2eb633ad7356b7f83e88dece04ce91563d70311b19c5e7720ddfddddc2ff9")
    version("14", sha256="39b5c1e3aa82babeecfdbab38e3d160899fcb4008f571ea4d80f80cfc43068d7")
    version("13", sha256="10deb50adf3bdd838c999cb872c800f86ed30fdcbe84a79c8c2c0656dcbdb3d7")
    version("12", sha256="42fa193942acf3adb237dd1ec51ee10230edd98d7eb28c8f0718f2e14bf6d17b")
    version("11", sha256="50513b2cdda64d0f76a9fecdc6c3372f9b84f8f8638347bebf37adab0cc54071")
    version("10", sha256="26102b316415dc4f214e8e3c7ed1a042dc0bbe48be3def71e1217795d9d3ed7c")


    def url_for_version(self, version):
        url = "https://github.com/Mu2e/CRVteststand/archive/refs/tags/v{:s}.tar.gz"
        return url.format(version.string)

    def install(self, spec, prefix):
        with open("/exp/mu2e/app/users/rlc/spack/RLCDEBUG", "a") as myfile:
                myfile.write(prefix.string)

        mkdir(prefix.bin)
        copy(self.stage.source_path+"/*Crv",prefix.bin)
        copy(self.stage.source_path+"/*.sh",prefix.bin)
        copy(self.stage.source_path+"/*.C",prefix.bin)
        copy(self.stage.source_path+"/*.txt",prefix)
        mkdir(prefix.python)
        install_tree(self.stage.source_path + "/analysis", prefix.analysis)
        install_tree(self.stage.source_path + "/eventdisplay", prefix.eventdisplay)
        install_tree(self.stage.source_path + "/preprocess", prefix.preprocess)


    def setup_run_environment(self, run_env):
        run_env.set("CRVTESTSTAND_DIR", self.prefix)
