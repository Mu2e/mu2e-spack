# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDashMantineComponents(PythonPackage):
    """Mantine themed components for use in Plotly Dash"""

    homepage = "https://www.dash-mantine-components.com/"
    pypi = "dash_mantine_components/dash_mantine_components-2.6.1.tar.gz"
    git = "https://github.com/snehilvj/dash-mantine-components"

    license("Apache-2.0")

    version(
        "2.6.1",
        sha256="40fd21b94784ebc4c2248eff702a7ce705f67bf9b7e75c0dc3c3389745744a84",
    )
    version(
        "2.6.0",
        sha256="46dadc90cf261b951f087eb96fb64b4b2d9616f854354e1f382c66209dce82c4",
    )
    version(
        "2.5.1",
        sha256="8162c71e9eee7e02bf2d88456413c829faa95c1e648d40e4205591465723dca5",
    )
    version(
        "2.5.0",
        sha256="fa977da9094b931f9082aa1a1eb89f2c34c90dff3bd607d9de4eae006a7feef9",
    )
    version(
        "2.4.1",
        sha256="617b01592dac3eba9154c7371c08cd52907fefb3317c2fb8538ad697402d1902",
    )

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-dash")
