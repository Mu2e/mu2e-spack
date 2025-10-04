# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


def sanitize_environments(env, *vars):
    for var in vars:
        env.prune_duplicate_paths(var)
        env.deprioritize_system_paths(var)

class Offline(CMakePackage):
    """The Mu2e Offline analysis code suite"""

    homepage = "https://mu2e.fnal.gov"
    git = "https://github.com/Mu2e/Offline"

    maintainers("eflumerf", "kutschke", "rlcee")

    license("Apache-2.0")

    version("main", branch="main", get_full_repo=True)
    version("develop", branch="main", get_full_repo=True) # spack-mpd expects develop version

    version("12.05.00", commit="ee56883fbd6752350952e975b7a843cc900d905c")
    version("12.04.00", commit="5c4a7548f98b2be43eb73ae44980b4e7ad7c90c8")
    version("12.03.00", commit="fb0c0b1c05d9a22eae512270fe9ff110cb9174fb")
    version("12.02.00", commit="01611bdf4f75e5d99335dd64dc4158848406a9a4")
    version("12.01.00", commit="5dad8f10d16258944d403aa6f7dfd451f61be8d1")
    version("12.00.00", commit="ed4c7b311747289b80b4a061e1bc7cd23d8191a9")
    version("11.05.01", commit="da34cccbf365f0b85194e0ce10108ddfb286d38a")
    version("11.04.00", commit="86ef8c73e1683532cec252bbfe6fa64815a9d4d3")
    version("11.03.00", commit="57339a5a43a073c9657f221b1d96d5a7b3c48b4b")
    version("11.02.00", commit="83ca01342f4ad86c4452babbb8a7083412dcfa88")
    version("11.01.00", commit="1560c76")
    version("11.00.01", commit="67f7904d5")
    version("10.40.00", commit="90410d6ca1ffe37d6ce1b0314dccbe7e28cc804a")
    version("10.36.00", commit="86ef8c73e1683532cec252bbfe6fa64815a9d4d3")

    variant("g4", default=True, description="Whether to build Geant4-dependent packages")

    variant(
        "cxxstd",
        default="20",
        values=("14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    variant("build_type", default="RelWithDebInfo",
            description="CMake build type")

    # Direct dependencies, see ups/product_deps
    depends_on("geant4", when="+g4")
    depends_on("cetmodules@3.26.00:", type="build")
    depends_on("artdaq-core-mu2e@:v3_99_00",when="@:11.99.00")
    depends_on("artdaq-core-mu2e@v4_00_00:,develop",when="@12.00.00:,develop")
    depends_on("art-root-io")
    depends_on("kinkal")

    depends_on("kinkal@3:", when="@11.01.00:")
    depends_on("kinkal@3.0.1", when="@11.02.00")
    depends_on("kinkal@3.1.3", when="@11.03.00")
    depends_on("kinkal@3.1.4", when="@11.04.00")
    depends_on("kinkal@3.1.5", when="@11.05.01")
    depends_on("kinkal@3.2.1", when="@develop") # UPDATE AS NEEDED
    depends_on("kinkal@3.2.1,main", when="@main") # UPDATE AS NEEDED

    depends_on("btrk")
    depends_on("gallery")
    depends_on("cry", when="+g4")
    depends_on("swig", type="build")
    depends_on("gsl")
    depends_on("xerces-c")

    # Indirect dependencies (But still required by CMake)
    depends_on("postgresql")
    depends_on("openblas")
    depends_on("root+tmva-sofie+spectrum+opengl")
    depends_on("boost+iostreams+program_options")

    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"), "-DWITH_G4={0}".format("TRUE" if "+g4" in self.spec else "FALSE")]
        return args

    def setup_run_environment(self, env):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # so event-ntuple can find dictionaries
        env.prepend_path("ROOT_LIBRARY_PATH", prefix.lib)
        # Ensure we can find fhicl files
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
        env.prepend_path("MU2E_SEARCH_PATH", "/cvmfs/mu2e.opensciencegrid.org/DataFiles")
        env.prepend_path("MU2E_SEARCH_PATH", prefix + "/fcl")
        env.prepend_path("MU2E_SEARCH_PATH", prefix + "/share")
        # show summary of configuration at start of mu2e exe
        pkgs = ["art", "root", "kinkal", "artdaq-core-mu2e"]
        banner = " ".join(f"{pkg}@{self.spec[pkg].version}" for pkg in pkgs)
        env.set("OFFLINE_BANNER",banner)
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH", "MU2E_SEARCH_PATH")

    def setup_dependent_run_environment(self, env, dependent_spec):
        prefix = self.prefix
        # Ensure we can find plugin libraries.
        env.prepend_path("CET_PLUGIN_PATH", prefix.lib)
        # Ensure we can find fhicl files
        env.prepend_path("FHICL_FILE_PATH", prefix + "/fcl")
        env.prepend_path("MU2E_SEARCH_PATH", prefix + "/fcl")
        # Ensure we can find data files
        env.prepend_path("MU2E_DATA_PATH", prefix + "/share")
        # Cleaup.
        sanitize_environments(env, "CET_PLUGIN_PATH", "FHICL_FILE_PATH", "MU2E_SEARCH_PATH", "MU2E_DATA_PATH")
