# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
import os


class Uhal(MakefilePackage):
    """The IPbus protocol is a simple packet-based control protocol for reading and modifying memory-mapped resources within FPGA-based hardware devices which have a virtual A32/D32 bus.

    The IPbus suite of software and firmware implement a reliable high-performance control link for particle physics electronics, based on the IPbus protocol.
    """

    homepage = "https://ipbus.web.cern.ch/doc/user/html/index.html"
    git = "https://github.com/ipbus/ipbus-software.git"
    url = "https://github.com/ipbus/ipbus-software/archive/refs/tags/v2.8.22.tar.gz"

    maintainers("eflumerf")

    license("gplv3", checked_by="eflumerf")

    version(
        "2.8.22",
        sha256="c31bf52bc834aef839377d86bc79651d08b943093c542a6b6a12a45cedd7b3ad",
    )

    variant("uhal", default=True, description="Whether to build the uhal component")
    variant(
        "controlhub",
        default=True,
        description="Whether to build the ControlHub component",
    )
    variant("gui", default=True, description="Whether to build the GUI component")
    variant("python", default=True, description="Whether to build the Python bindings")

    depends_on("boost")
    depends_on("pugixml")

    depends_on("erlang", when="+controlhub")
    extends("python", when="+python")
    depends_on("py-pybind11", when="+python")
    depends_on("py-setuptools", when="+python")
    extends("python", when="+gui")
    depends_on("py-setuptools", when="+gui")

    def edit(self, spec, prefix):
        os.environ["EXTERN_BOOST_INCLUDE_PREFIX"] = self.spec["boost"].prefix.include
        os.environ["EXTERN_BOOST_LIB_PREFIX"] = self.spec["boost"].prefix.lib
        os.environ["EXTERN_PUGIXML_INCLUDE_PREFIX"] = self.spec[
            "pugixml"
        ].prefix.include
        os.environ["EXTERN_PUGIXML_LIB_PREFIX"] = self.spec["pugixml"].prefix.lib

        os.environ["BUILD_UHAL_GUI"] = "1" if "+gui" in self.spec else "0"
        os.environ["BUILD_UHAL_PYTHON"] = "1" if "+python" in self.spec else "0"

        if "+python" in self.spec or "+gui" in self.spec:
            os.environ["PYTHON"] = self.spec["python"].command.path
            pyDefs = FileFilter("uhal/config/mfPythonRPMRules.mk")
            python_ver = self.spec["python"].version.up_to(2)
            pyDefs.filter(
                "PYTHONPATH=([^,]*),",
                "PYTHONPATH=\\1:"
                + join_path(
                    self.spec["py-setuptools"].prefix.lib,
                    f"python{python_ver}",
                    "site-packages",
                )
                + ",",
            )

        if "+uhal" in self.spec:
            if "+controlhub" in self.spec:
                os.environ["Set"] = "all"
            else:
                os.environ["Set"] = "uhal"
        elif "+controlhub" in self.spec:
            os.environ["Set"] = "controlhub"

        if "+controlhub" in self.spec:
            controlHub = FileFilter("controlhub/Makefile")
            controlHub.filter(" /etc", " ${sysconfdir}")
            controlHub.filter(" /var", " ${prefix}/var")
            controlHub.filter("=/etc", "=${sysconfdir}")
            controlHub.filter("-service rsyslog", "-echo service rsyslog")

        if "+python" in self.spec:
            pyMakefile = FileFilter("uhal/python/Makefile")
            pyMakefile.filter(
                "EXTERN_PYBIND11_INCLUDE_PREFIX=.*",
                "EXTERN_PYBIND11_INCLUDE_PREFIX="
                + self.spec["py-pybind11"].prefix.include,
            )

    @property
    def install_targets(self):
        return ["prefix={0}".format(self.prefix), "install"]

    def setup_run_environment(self, env):
        env.set("CACTUS_ROOT", self.prefix)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.set("CACTUS_ROOT", self.prefix)
