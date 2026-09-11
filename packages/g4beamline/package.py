# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.build_systems.cmake import CMakeBuilder as _SpackCMakeBuilder


class G4beamline(CMakePackage):
    """G4beamline: a particle-tracking simulation program built on top of
    Geant4. Provides a scripting layer that lets users describe beamline
    geometries without writing C++ Geant4 code. Maintained by Tom Roberts at
    Muons Inc."""

    homepage = "https://muonsinc.com/Website1/tiki-index.php?page=G4beamline"

    # Upstream does not publish a stable, machine-fetchable tarball URL
    # (the download lives behind a Tiki wiki page). The hashes below were
    # computed against the tarballs archived in
    # /cvmfs/mu2e.opensciencegrid.org/DataFiles/G4beamlin
    url = "file:///cvmfs/mu2e.opensciencegrid.org/DataFiles/G4beamline/G4beamline-3.08-source.tar"

    def url_for_version(self, version):
        return "file:///cvmfs/mu2e.opensciencegrid.org/DataFiles/G4beamline/G4beamline-{0}-source.tar".format(
            version
        )

    maintainers("oksuzian")

    version(
        "3.08b",
        sha256="6000e4811fa7263d5a7551fa6821640b5cd10e0bfea58d987f9a4df92500ad3f",
    )
    version(
        "3.08a",
        sha256="27416645283b88bbbc9d464f11cbb86ee4c862ead83c3f83c3c004df92acf4cb",
    )
    version(
        "3.08",
        sha256="55519c23ed10c8430d4cc727ce4af7873f0abff93bb5ccf18d80a01e20b49c55",
    )

    variant("gui", default=False, description="Build the Qt-based GUI")
    variant("visual", default=False, description="Build OpenGL visualization support")

    depends_on("cmake@3.16:", type="build")
    depends_on("geant4@11.0:11.2", when="@3.08:3.08a")
    depends_on("geant4@11.3:", when="@3.08b")
    depends_on("geant4 +qt", when="+gui")
    depends_on("geant4 +opengl", when="+visual")
    depends_on("root")
    depends_on("fftw")
    depends_on("gsl")
    depends_on("xerces-c")

    def patch(self):
        # 1. Geant4Data: by default G4beamline downloads its own copy of the
        #    Geant4 datasets into a private directory. Flip the default to
        #    `false` so it instead picks up G4LEDATA / G4NEUTRONHPDATA / ...
        #    from the geant4 spack package's run environment.
        filter_file(
            r"static\s+bool\s+setup\s*\(\s*bool\s+overwriteEnv\s*=\s*true\s*\)\s*;",
            r"static bool setup(bool overwriteEnv=false);",
            "g4bl/Geant4Data.hh",
        )

        # 2. BLEvaluator: upstream allocates with `new[]` but frees with
        #    `free()`. Replace the free() with delete[].
        filter_file(
            r"free\(in\);",
            r"delete[] in;",
            "g4bl/BLEvaluator.hh",
        )

        # The two patches below were applied upstream in 3.08b, so they only
        # need to run for older releases.
        if self.spec.satisfies("@:3.08a"):
            # 3. BLRunManager: Geant4 11.3 added a required argument to
            #    G4StackManager::PrepareNewEvent.
            filter_file(
                r"stackManager->PrepareNewEvent\(\s*\)\s*;",
                r"stackManager->PrepareNewEvent(currentEvent);",
                "g4bl/BLRunManager.cc",
            )

            # 4. Newer GCC drops the `sighandler_t` typedef from <signal.h>
            #    in some contexts. Use an explicit function-pointer type at
            #    the declaration site; the local typedef on line ~87 is left
            #    in place but no longer needed.
            filter_file(
                r"sighandler_t\s+prevSighandler",
                r"void (*prevSighandler)(int)",
                "g4bl/BLRootNTuple.cc",
            )

    def setup_run_environment(self, env):
        env.set("G4BL_DIR", self.prefix)
        env.prepend_path("PATH", self.prefix.bin)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.set("G4BL_DIR", self.prefix)
        env.prepend_path("PATH", self.prefix.bin)


class CMakeBuilder(_SpackCMakeBuilder):
    def cmake_args(self):
        # G4beamline's CMakeLists reads GSL_DIR / FFTW_DIR from the env (or
        # accepts them as cache vars) instead of using find_package(). Pass
        # the spack prefixes explicitly.
        spec = self.pkg.spec
        return [
            self.define_from_variant("G4BL_GUI", "gui"),
            self.define_from_variant("G4BL_VISUAL", "visual"),
            self.define("GSL_DIR", spec["gsl"].prefix),
            self.define("FFTW_DIR", spec["fftw"].prefix),
        ]

    def install(self, pkg, spec, prefix):
        # Run upstream's CMake install target first. It populates
        # bin/doc/examples/etc. inside the build directory (and also bundles
        # everything into a tgz that ignores CMAKE_INSTALL_PREFIX, which is
        # why the spack prefix would otherwise be left empty and trigger
        # "Nothing was installed!").
        super().install(pkg, spec, prefix)

        # Now hand-copy just the artifacts we actually want into the spack
        # prefix, matching the layout Kevin documented on the Mu2e wiki.
        for d in ("bin", "doc", "examples", "share", "test", "validation"):
            src = join_path(self.build_directory, d)
            if os.path.isdir(src):
                install_tree(src, join_path(prefix, d))
        readme = join_path(self.build_directory, "README.txt")
        if os.path.isfile(readme):
            install(readme, prefix)
