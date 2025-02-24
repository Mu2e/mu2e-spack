# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class Mu2ePcieUtils(CMakePackage):
    """The toolkit currently provides functionality for data transfer,
    event building, event reconstruction and analysis (using the art analysis
    framework), process management, system and process state behavior, control
    messaging, local message logging (status and error messages), DAQ process
    and art module configuration, and the writing of event data to disk in ROOT
    format."""

    homepage = "https://mu2e.fnal.gov"
    url = "https://github.com/Mu2e/mu2e-pcie-utils/archive/refs/tags/v2_08_00.tar.gz"
    git = "https://github.com/Mu2e/mu2e-pcie-utils.git"

    maintainers("eflumerf", "rrivera747")

    license("BSD")

    version("ryan_test", commit="112bf71f774d02dbee316232c82250beb4306885")
    version("develop", branch="develop", get_full_repo=True)

    version("v3_04_00", commit="b9e229970b1075990aa0ed007fa399583cc1c260")
    version("v3_03_01", commit="e2bf8f658055f43cd1a790456daf7c3495fb7061")
    version("v3_03_00", commit="bcbe4bdbc86e7d854f94abb813cb64da666d878d")
    version("v3_02_00", commit="2fc701067582ef63fdcc8ddfbf1437e5209fe2ea")
    version("v3_01_00", commit="b4d49d749a487b9b3150aa96a149af0b201a3f1b")
    version("v3_00_00", commit="757b66cb792ff5dae6bb1cdff566b60d6cfcfdc0")
    version("v2_09_01", sha256="de7debf74d81739dbfe3e7d4a7365a4c57ed3150ffd49fb5b5504f410dd469c6")
    version("v2_08_05", sha256="2e78e63c9f71b0293b6e09315a17f809b42a40d5bc1e7b2cc4efc8f3b042a79b")
    version("v2_08_00", sha256="e322ff8f4fbc2c8aaf59ce1afcc5ac410b459717df18ba5432ea9f96be609083")

    def url_for_version(self, version):
        url = "https://github.com/Mu2e/mu2e-pcie-utils/archive/refs/tags/{0}.tar.gz"
        return url.format(version)
  
    patch("v2_08_05.patch", when="@v2_08_05")

    variant(
        "cxxstd",
        default="20",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    variant("kmod",default=False,description="Build Kernel modules.")
    variant("root",default=False,description="Build ROOT interface")
    variant("python",default=False,description="Build Python bindings")

    depends_on("cetmodules", type="build")
    depends_on("messagefacility")
    depends_on("artdaq-core-mu2e@develop", when="@ryan_test")
    depends_on("artdaq-core-mu2e@develop", when="@develop")
    depends_on("artdaq-core-mu2e@v3_00_00:", when="@v3_00_00:")
    depends_on("artdaq-core-mu2e@v2_00_00:v2_01_03", when="@v2_09_01")
    depends_on("trace")
    depends_on("canvas-root-io",when="+root")
    depends_on("swig",when="+python")
    depends_on("python",when="+python")

    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"), "-DWANT_KMOD={0}".format("TRUE" if "+kmod" in self.spec else "FALSE"), "-DBUILD_ROOT_INTERFACE={0}".format("TRUE" if "+root" in self.spec else "FALSE"), "-DBUILD_PYTHON_INTERFACE={0}".format("TRUE" if "+python" in self.spec else "FALSE")]
        return args

    def setup_dependent_runtime_environment(self, env):
        env.set('MU2E_PCIE_UTILS_INC', '%s' % self.prefix.include)
        env.set('MU2E_PCIE_UTILS_LIB', '%s' % self.prefix.lib)
