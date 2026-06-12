# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
import os


class Mu2eOrt(CMakePackage):
    """ONNX Runtime: cross-platform, high performance ML inferencing and training accelerator"""

    homepage = "https://onnxruntime.ai/"
    url = "https://github.com/microsoft/onnxruntime/archive/refs/tags/v1.25.1.tar.gz"
    git = "https://github.com/microsoft/onnxruntime.git"

    maintainers("rlcee")

    license("MIT")

    # patch version to force rebuild after tweaking recipe
    # version("1.25.1c", sha256="b0c49a093976bf84f099a19aa13a46bd1d213e1d13b34ffe3b0916657209a844")
    # version("1.25.1b", sha256="b0c49a093976bf84f099a19aa13a46bd1d213e1d13b34ffe3b0916657209a844")
    # version("1.25.1a", sha256="b0c49a093976bf84f099a19aa13a46bd1d213e1d13b34ffe3b0916657209a844")
    version(
        "1.25.1",
        sha256="b0c49a093976bf84f099a19aa13a46bd1d213e1d13b34ffe3b0916657209a844",
    )

    # Build system
    depends_on("cmake@3.26:", type="build")
    depends_on("python@3.8:", type="build")

    # Core dependencies
    # Note: protobuf, re2, abseil-cpp, and flatbuffers are ALL vendored by ONNX Runtime
    # Using system versions causes the build to create shared library dependencies
    # that won't be found at runtime. ONNX Runtime is designed to statically link
    # all these dependencies into libonnxruntime.so for portability.
    # depends_on("protobuf")  # REMOVED - must be vendored
    # depends_on("re2")
    # depends_on("abseil-cpp")
    # depends_on("flatbuffers")
    depends_on("nlohmann-json")

    # Optional: CUDA support
    variant("cuda", default=False, description="Build with CUDA support")
    depends_on("cuda", when="+cuda")
    depends_on("cudnn", when="+cuda")

    # Build variants
    variant("shared", default=True, description="Build shared libraries")
    variant("tests", default=False, description="Build and run tests")

    # The build.sh script is a Python wrapper around CMake
    # We need to bypass it and call CMake directly in Spack

    # Tell Spack this is a CMake project but the root CMakeLists.txt
    # is in the cmake subdirectory
    root_cmakelists_dir = "cmake"

    def cmake_args(self):
        """
        Generate CMake arguments.

        The build.sh script normally calls tools/ci_build/build.py which:
        1. Parses command-line arguments
        2. Translates them to CMake flags
        3. Runs cmake with those flags

        In Spack, we bypass build.sh/build.py and call CMake directly,
        providing the same flags that build.py would generate.
        """
        args = [
            # Build configuration
            # CRITICAL: Do NOT use BUILD_SHARED_LIBS - it's a global CMake variable
            # that affects ALL subprojects including vendored dependencies!
            # When BUILD_SHARED_LIBS=ON, vendored protobuf/abseil/re2 build as shared libs
            # that are never installed, causing unresolved dependencies.
            # self.define_from_variant("BUILD_SHARED_LIBS", "shared"),  # WRONG!
            # Instead, use ONNX Runtime's specific flag
            self.define("onnxruntime_BUILD_SHARED_LIB", self.spec.satisfies("+shared")),
            # Explicitly set BUILD_SHARED_LIBS=OFF to ensure vendored deps are static
            self.define("BUILD_SHARED_LIBS", False),
            # Architecture compatibility: Force x86_64_v2 for portability
            # This ensures the binary runs on older CPUs without AVX/AVX2
            # Building on x86_64_v3 with default flags may generate AVX instructions
            # that will crash on x86_64_v2 machines with "Illegal instruction"
            self.define("CMAKE_C_FLAGS", "-march=x86-64-v2 -mtune=generic"),
            self.define("CMAKE_CXX_FLAGS", "-march=x86-64-v2 -mtune=generic"),
            # Disable warnings as errors (needed for GCC compatibility)
            self.define("onnxruntime_ENABLE_WERROR", False),
            # Core build options (matching our successful build)
            self.define("onnxruntime_BUILD_UNIT_TESTS", self.spec.satisfies("+tests")),
            self.define("onnxruntime_BUILD_BENCHMARKS", False),
            # Disable language bindings (we only need C++ library)
            self.define("onnxruntime_BUILD_CSHARP", False),
            self.define("onnxruntime_BUILD_JAVA", False),
            self.define("onnxruntime_BUILD_NODEJS", False),
            self.define("onnxruntime_BUILD_OBJC", False),
            self.define("onnxruntime_BUILD_SHARED_LIB", self.spec.satisfies("+shared")),
            self.define("onnxruntime_BUILD_APPLE_FRAMEWORK", False),
            # Disable Python bindings
            self.define("onnxruntime_ENABLE_PYTHON", False),
            # CRITICAL: Prevent CMake from finding system dependencies!
            # Even without depends_on("protobuf"), Spack's unified view allows CMake
            # to find protobuf automatically via find_package(). When found, ONNX Runtime
            # uses it and creates shared library dependencies that won't be installed.
            # We must explicitly disable find_package() for vendored dependencies.
            self.define("CMAKE_DISABLE_FIND_PACKAGE_Protobuf", True),
            self.define("CMAKE_DISABLE_FIND_PACKAGE_absl", True),
            self.define("CMAKE_DISABLE_FIND_PACKAGE_re2", True),
            self.define("CMAKE_DISABLE_FIND_PACKAGE_Flatbuffers", True),
            # This forces ONNX Runtime to vendor and statically link these dependencies
            # into libonnxruntime.so, creating a self-contained library with only system deps
            # Disable training (we only need inference)
            self.define("onnxruntime_ENABLE_TRAINING", False),
            self.define("onnxruntime_ENABLE_TRAINING_OPS", False),
            self.define("onnxruntime_ENABLE_TRAINING_APIS", False),
            # Keep all operators (full-featured build)
            # Note: We're NOT using --disable_contrib_ops or --disable_ml_ops
            # to maintain full inference capability
        ]

        # CUDA support
        if self.spec.satisfies("+cuda"):
            args.extend(
                [
                    self.define("onnxruntime_USE_CUDA", True),
                    self.define("onnxruntime_USE_CUDNN", True),
                    self.define(
                        "CMAKE_CUDA_ARCHITECTURES", "70;75;80;86"
                    ),  # Adjust as needed
                ]
            )

        return args

    def setup_build_environment(self, env):
        """Set up the build environment."""
        # Ensure Python is available for the build process
        # (Some build scripts still need Python even though we're using CMake directly)
        env.set("PYTHONPATH", self.stage.source_path)

    @run_after("install")
    def check_install(self):
        """Verify the installation."""
        if self.spec.satisfies("+shared"):
            # Check that the shared library was installed
            # ONNX Runtime installs to lib64 on some systems
            lib_path = join_path(self.prefix.lib64, "libonnxruntime.so")
            if not os.path.exists(lib_path):
                # Try lib directory as fallback
                lib_path = join_path(self.prefix.lib, "libonnxruntime.so")
                if not os.path.exists(lib_path):
                    raise InstallError("Shared library not found in lib or lib64")
