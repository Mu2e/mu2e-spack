# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
import os

class Kinkal(CMakePackage):
    """Kinematic Kalman filter track fit code package"""

    homepage = "https://github.com/KFTrack/KinKal#readme"
    url = "https://github.com/KFTrack/KinKal/archive/refs/tags/v2.4.2.tar.gz"
    git = "https://github.com/KFTrack/KinKal"

    maintainers = ['brownd1978','rlcee']

    version("main", branch="main", get_full_repo=True)

    version("3.1.6", sha256="0d2af69c36b8c17f3887fbd9d879a0647d438d0ba5929b0fd53631ae429a40ad")
    version("3.1.5", sha256="5a964a0a88a7b55b277524d4280c8b428841f6953e9b133adc1dd2f9e9bb1a17")
    version("3.1.4", sha256="04492cae4b473e75e4240ff76c590e6f0a7f9528da367e74b2041cf9c4b0fef2")
    version("3.1.3", sha256="7b465f7e788d42a5f0310dc31a38b32161ebe582fdc6f0ee178439b12e172fc6")
    version("3.1.2", sha256="4417844e7885825f1c51f23fa69312192a5bb6918aa43553d307b81b2347962f")
    version("3.1.1", sha256="f2dc3db40ae851f4e9047299516a65606bcc3dd081cb5523509f324cbd8a79b0")
    version("3.1.0", sha256="2b6e6f23d200f3e3acfcbcebb252de64086356321f2e4894a315ed688851dda8")
    version("3.0.1", sha256="0185f88b9e8e346b5d6ba03763c2ebc8640d345564e3215c7821f0741a5ae3b9")
    version("3.0.0", sha256="690c68303c464e11817c145aa7d3bb2ec21f41e003b1d045e1ad1c840055a93f")
    version("2.5.0", sha256="45bfd2fd9b0eea7f78345bf31d280baf6ae17214a3afab97a54bd6c02a332017")
    version("2.4.3", sha256="543b9b3569242f298c7c433ba45945e38a440c4fb410029946318d2e2202ee6e")
    version("2.4.2", sha256="7a9aebf925fb2f354ccd5483078661767db7ced59e826ce234effe0e7bc49aa7")
    version("2.4.1", sha256="ee239f6f9d396d02da6523fb4961f78c55494439775ffcef83aa1362854d2f19")
    version("2.4.0", sha256="638323087e11d03a10f6499080ef8e5a6edcb976f79843ee39b81bfbda3dca2a")
    version("2.3.1", sha256="25dbfcbd684010cd61eb34b46c4416a52ca53ab1c95b5d9e20f551da5cab2fbb")
    version("2.3.0", sha256="33522e797cbfa0b4953de74028ef573ffe7c2067eafa4d27bc51627b1c64ab6d")
    version("2.2.1", sha256="6fa99d0d4265d7d857936f02f2d2a605e2d6109b7e017f74568ef2f2cf4525c3")
    version("2.2.0", sha256="a3e4269339dd3cebdd709aa7d474dc5a5db905c2181cf9d5e08bd9233c4ec895")
    version("2.1.0", sha256="8232f5e9862db1dc2c73bad1e52b64b8524c2be1d7ea966943f27516b6f34fae")
    version("2.0.1", sha256="d845e1232168dd22b8e1b2ddde6ff4da6f511c81aa8b56c2cf64b9dfa27c0203")
    version("2.0.0", sha256="90286168ebf222fdc227adcbb8fed0b60208f7431511afe128f85f1e76fc10b0")

    depends_on("root+mlp")

    variant(
        "cxxstd",
        default="17",
        values=("17", "20", "23"),
        multi=False,
        sticky=True,
        description="C++ standard",
    )

    def patch(self):
        filter_file(
            r"(set\(CMAKE_CXX_STANDARD )17\)",
            r"\1 %s)" % self.spec.variants["cxxstd"].value,
            "CMakeLists.txt",
        )

    def cmake_args(self):
        args = ["-DPROJECT_SOURCE_DIR=%s" % self.stage.source_path, self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),]
        return args

    @run_before('build')
    def makelink(self):
        # at some point the stage.path changed from the
        # repo dir to /tmp
        wdir = self.stage.path
        if wdir[:4] == "/tmp" :
            tdir = self.stage.source_path
            linkname = '%s/../KinKal' % self.stage.source_path
        else :
            with working_dir(self.stage.path):
                if os.path.isdir("spack-src") :
                    tdir = '%s/spack-src' % self.stage.path
                    linkname = '%s/KinKal' % self.stage.path
                else :
                    tdir = self.stage.path
                    linkname = '%s/../KinKal' % self.stage.path
        if not os.path.islink(linkname) :
            os.symlink(tdir, linkname)

    @run_after('install')
    def copy_headers(self):
        if self.version >= Version("3.0.0"):
            return
        with working_dir(self.stage.path):
            copy('%s/spack-src/General/PhysicalConstants.h' % self.stage.path,
                 '%s/include/KinKal/General/PhysicalConstants.h' % self.prefix)
            copy('%s/spack-src/General/SystemOfUnits.h' % self.stage.path,
                 '%s/include/KinKal/General/SystemOfUnits.h' % self.prefix)

    def setup_run_environment(self, env):
        prefix = self.prefix
        # Emulate UPS variables
        env.set("KINKAL_LIB", prefix.lib64)
        env.set("KINKAL_INC", prefix.include)

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Emulate UPS variables
        env.set("KINKAL_LIB", prefix.lib64)
        env.set("KINKAL_INC", prefix.include)

    def setup_build_environment(self, env):
        prefix = self.prefix
        # Emulate UPS variables
        env.set("KINKAL_LIB", prefix.lib64)
        env.set("KINKAL_INC", prefix.include)

    def setup_dependent_build_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Emulate UPS variables
        env.set("KINKAL_LIB", prefix.lib64)
        env.set("KINKAL_INC", prefix.include)
