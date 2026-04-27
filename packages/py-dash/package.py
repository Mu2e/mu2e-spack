# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDash(PythonPackage):
    """Dash is the most downloaded, trusted Python framework
    for building ML & data science web apps."""

    homepage = "https://dash.plotly.com/"
    pypi = "dash/dash-2.17.1.tar.gz"
    git = "https://github.com/plotly/dash.git"

    license("MIT")

    version(
        "4.1.0",
        sha256="17a92a87b0c1eacc025079a705e44e72cd4c5794629c0a2909942b611faeb595",
    )
    version(
        "4.0.0",
        sha256="c5f2bca497af288f552aea3ae208f6a0cca472559003dac84ac21187a1c3a142",
    )
    version(
        "3.4.0",
        sha256="3944beb32000ee8b22cd7fbb33545a0a43e25916c63aa41ba59ee5611997815e",
    )
    version(
        "3.3.0",
        sha256="eaaa7a671540b5e1db8066f4966d0277d21edc2c7acdaec2fd6d198366a8b0df",
    )
    version(
        "3.2.0",
        sha256="93300b9b99498f8b8ed267e61c455b4ee1282c7e4d4b518600eec87ce6ddea55",
    )
    version(
        "3.1.1",
        sha256="916b31cec46da0a3339da0e9df9f446126aa7f293c0544e07adf9fe4ba060b18",
    )
    version(
        "2.17.1",
        sha256="ee2d9c319de5dcc1314085710b72cd5fa63ff994d913bf72979b7130daeea28e",
    )

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-typing-extensions")
    depends_on("py-flask")
    depends_on("py-plotly@5")
    depends_on("py-importlib-metadata")
