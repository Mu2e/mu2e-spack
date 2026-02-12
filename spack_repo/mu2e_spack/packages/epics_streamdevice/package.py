# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage
from spack.package import *


class EpicsStreamdevice(MakefilePackage):
    """StreamDevice is a generic EPICS device support for devices with a "byte stream" based communication interface.
    That means devices that can be controlled by sending and receiving strings (in the broadest sense, including non-printable characters and even null-bytes).
    Examples for this type of communication interface are serial line (RS-232, RS-485, ...), IEEE-488 (also known as GPIB or HP-IB), and telnet-like TCP/IP."""

    homepage = "https://paulscherrerinstitute.github.io/StreamDevice/"
    url = "https://github.com/paulscherrerinstitute/StreamDevice/archive/refs/tags/2.8.26.tar.gz"

    license("LGPL-3.0-only", checked_by="eflumerf")

    version("2.8.26", sha256="0c212245fb4626a94e291a6744f5483343b3b896907693c6a71048de68faabc4")

    variant("asyn", default=True, description="Enable asyn support")
    variant("pcre", default=True, description="Enable pcre support")

    depends_on("epics-base")
    depends_on("epics-asyn", when="+asyn")
    depends_on("pcre", when="+pcre")

    def edit(self, spec, prefix):
        release = FileFilter("configure/RELEASE")
        release.filter("^EPICS_BASE *=.*", f"EPICS_BASE = {spec['epics-base'].prefix}")
        if "+asyn" in spec:
            release.filter("^ASYN *=.*", f"ASYN = {spec['epics-asyn'].prefix}")
        if "+pcre" in spec:
            release.filter("^PCRE *=.*", f"PCRE_INCLUDE = {spec['pcre'].prefix.include}\nPCRE_LIB = {spec['pcre'].prefix.lib}")
        release.filter("CALC *=.*", "#CALC") # No CALC support for now
        pass

    def install(self, spec, prefix):
        make("INSTALL_LOCATION=" + prefix, "install")
