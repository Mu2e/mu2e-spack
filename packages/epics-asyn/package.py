# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class EpicsAsyn(MakefilePackage):
    """A general purpose facility for interfacing device specific code to low level drivers. asynDriver allows non-blocking device support that works with both blocking and non-blocking drivers."""

    homepage = "https://epics-modules.github.io/master/asyn/"
    url = "https://github.com/epics-modules/asyn/archive/R4-43.tar.gz"

    # https://github.com/epics-modules/asyn/blob/master/LICENSE
    license("Other", checked_by="eflumerf")

    version("4-43", sha256="2cd1da9bafc6e09d18992d00797ea4b966d7404be2fb0d309bc3f542e6b3c7ba")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("epics-base")
    depends_on("libtirpc")

    def edit(self, spec, prefix):
        release = FileFilter("configure/RELEASE")
        release.filter("^#EPICS_BASE *=.*", f"EPICS_BASE = {spec['epics-base'].prefix}")
        config_site = FileFilter("configure/CONFIG_SITE")
        config_site.filter("^# TIRPC=YES", "TIRPC=YES")
        pass

    def install(self, spec, prefix):
        make("INSTALL_LOCATION=" + prefix, "install")
