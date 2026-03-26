# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack_repo.builtin.build_systems.bundle import BundlePackage
from spack.package import *


class Mu2eTdaqSuite(BundlePackage):
    """The Mu2e TDAQ Suite, the software used for Mu2e trigger and data acquisition"""

    version("develop")
    version("v12_00_00")
    version("v11_00_00")
    version("v10_00_00")
    version("v9_00_00")
    version("v8_00_00")
    version("v7_01_00_cand")
    version("v7_00_00_cand")
    version("v6_00_00_cand")
    version("v5_00_00")
    version("v4_00_00")

    # The art-suite Dependency
    squals = (
        "112",
        "117",
        "118",
        "122",
        "123",
        "126",
        "128",
        "130",
        "131",
        "132",
        "133",
        "134",
    )
    variant(
        "s",
        default="134",
        values=("0",) + squals,
        multi=False,
        description="Art suite version to use",
    )
    for squal in squals:
        depends_on(f"art-suite@s{squal}+root", when=f"s={squal}")
    depends_on("art-suite+root", when="s=0")

    # The artdaq Dependency
    variant(
        "artdaq",
        default="40700",
        values=("0", "40000", "40100", "40200", "40300", "40401", "40500", "40600", "40700"),
        multi=False,
        description="Artdaq suite version to use",
    )
    depends_on("artdaq-suite@v4_07_00", when="artdaq=40700")
    depends_on("artdaq-suite@v4_06_00", when="artdaq=40600")
    depends_on("artdaq-suite@v4_05_00", when="artdaq=40500")
    depends_on("artdaq-suite@v4_04_01", when="artdaq=40401")
    depends_on("artdaq-suite@v4_03_00", when="artdaq=40300")
    depends_on("artdaq-suite@v4_02_00", when="artdaq=40200")
    depends_on("artdaq-suite@v4_01_00", when="artdaq=40100")
    depends_on("artdaq-suite@v4_00_00", when="artdaq=40000")
    depends_on("artdaq-suite@v3_16_00", when="artdaq=31600")
    depends_on("artdaq-suite@v3_15_00", when="artdaq=31500")
    depends_on("artdaq-suite@v3_14_01", when="artdaq=31401")
    depends_on("artdaq-suite@v3_14_00", when="artdaq=31400")
    depends_on("artdaq-suite@v3_13_01", when="artdaq=31301")
    depends_on("artdaq-suite@v3_13_00", when="artdaq=31300")
    depends_on("artdaq-suite@v3_12_07", when="artdaq=31207")
    depends_on("artdaq-suite@v3_12_03", when="artdaq=31203")
    depends_on("artdaq-suite@v3_12_02", when="artdaq=31202")
    depends_on("artdaq-suite+db+epics~demo~pcp")

    # The otsdaq Dependency
    variant(
        "otsdaq",
        default="30600",
        values=(
            "0",
            "30000",
            "30100",
            "30200",
            "30300",
            "30401",
            "30402",
            "30501",
            "30600",
            "30700",
        ),
        multi=False,
        description="Otsdaq version to use",
    )
    depends_on("otsdaq-suite@v3_06_00", when="otsdaq=30700")
    depends_on("otsdaq-suite@v3_06_00", when="otsdaq=30600")
    depends_on("otsdaq-suite@v3_05_01", when="otsdaq=30501")
    depends_on("otsdaq-suite@v3_04_02", when="otsdaq=30402")
    depends_on("otsdaq-suite@v3_04_01", when="otsdaq=30401")
    depends_on("otsdaq-suite@v3_03_00", when="otsdaq=30300")
    depends_on("otsdaq-suite@v3_02_00", when="otsdaq=30200")
    depends_on("otsdaq-suite@v3_01_00", when="otsdaq=30100")
    depends_on("otsdaq-suite@v3_00_00", when="otsdaq=30000")
    depends_on("otsdaq-suite")

    # g4 Variant
    variant(
        "g4",
        default=False,
        description="Whether to build the G4 variant of the Offline",
    )

    variant("ci", default=True, description="Install utilities used by CI builds")
    with when("+ci"):
        depends_on("lcov")
        depends_on("py-black")
        depends_on("py-cmake-format")

    # Bundle package, list packages that are part of the bundle
    with when("@v12_00_00"):
        depends_on("artdaq-core-mu2e@v9_03_00")
        depends_on("mu2e-pcie-utils@v8_03_00")
        depends_on("artdaq-mu2e@v7_03_00")
        depends_on("otsdaq-mu2e@v11_01_00")
        depends_on("otsdaq-mu2e-calorimeter@v8_03_00")
        depends_on("otsdaq-mu2e-crv@v6_03_00")
        depends_on("otsdaq-mu2e-extmon@v5_02_00")
        depends_on("otsdaq-mu2e-sync@v1_01_00")
        depends_on("otsdaq-mu2e-stm@v5_02_00")
        depends_on("Offline@13.04.00~g4", when="~g4")
        depends_on("Offline@13.04.00+g4", when="+g4")
        depends_on("otsdaq-mu2e-tracker@v8_02_00")
        depends_on("otsdaq-mu2e-dqm@v7_02_00")
        depends_on("otsdaq-mu2e-trigger@v7_03_00")
        depends_on("mu2e-trig-config@v8_03_00")
    with when("@v11_00_00"):
        depends_on("artdaq-core-mu2e@v9_03_00")
        depends_on("mu2e-pcie-utils@v8_02_00")
        depends_on("artdaq-mu2e@v7_02_00")
        depends_on("otsdaq-mu2e@v11_00_00")
        depends_on("otsdaq-mu2e-calorimeter@v8_02_00")
        depends_on("otsdaq-mu2e-crv@v6_02_00")
        depends_on("otsdaq-mu2e-extmon@v5_01_00")
        depends_on("otsdaq-mu2e-stm@v5_01_00")
        depends_on("offline@13.04.00~g4", when="~g4")
        depends_on("offline@13.04.00+g4", when="+g4")
        depends_on("otsdaq-mu2e-tracker@v8_01_00")
        depends_on("otsdaq-mu2e-dqm@v7_01_00")
        depends_on("otsdaq-mu2e-trigger@v7_02_00")
        depends_on("mu2e-trig-config@v8_03_00")
    with when("@v10_00_00"):
        depends_on("artdaq-core-mu2e@v9_02_00")
        depends_on("mu2e-pcie-utils@v8_01_00")
        depends_on("artdaq-mu2e@v7_01_00")
        depends_on("otsdaq-mu2e@v10_00_00")
        depends_on("otsdaq-mu2e-calorimeter@v8_01_00")
        depends_on("otsdaq-mu2e-crv@v6_01_00")
        depends_on("otsdaq-mu2e-extmon@v5_01_00")
        depends_on("otsdaq-mu2e-stm@v5_01_00")
        depends_on("offline@13.01.00~g4", when="~g4")
        depends_on("offline@13.01.00+g4", when="+g4")
        depends_on("otsdaq-mu2e-tracker@v8_00_00")
        depends_on("otsdaq-mu2e-dqm@v7_01_00")
        depends_on("otsdaq-mu2e-trigger@v7_01_00")
        depends_on("mu2e-trig-config@v8_01_00")
    with when("@v9_00_00"):
        depends_on("artdaq-core-mu2e@v9_00_00")
        depends_on("mu2e-pcie-utils@v8_00_00")
        depends_on("artdaq-mu2e@v7_00_00")
        depends_on("otsdaq-mu2e@v9_00_00")
        depends_on("otsdaq-mu2e-calorimeter@v8_00_00")
        depends_on("otsdaq-mu2e-crv@v6_00_00")
        depends_on("otsdaq-mu2e-extmon@v5_00_00")
        depends_on("otsdaq-mu2e-stm@v5_00_00")
        depends_on("offline@13.00.08~g4", when="~g4")
        depends_on("offline@13.00.08+g4", when="+g4")
        depends_on("otsdaq-mu2e-tracker@v7_00_00")
        depends_on("otsdaq-mu2e-dqm@v7_00_00")
        depends_on("otsdaq-mu2e-trigger@v7_00_00")
        depends_on("mu2e-trig-config@v8_00_00")
    with when("@v8_00_00"):
        depends_on("artdaq-core-mu2e@v8_01_00")
        depends_on("mu2e-pcie-utils@v7_00_00")
        depends_on("artdaq-mu2e@v6_00_00")
        depends_on("otsdaq-mu2e@v8_00_00")
        depends_on("otsdaq-mu2e-calorimeter@v7_01_00")
        depends_on("otsdaq-mu2e-crv@v5_00_00")
        depends_on("otsdaq-mu2e-extmon@v4_01_00")
        depends_on("otsdaq-mu2e-stm@v4_01_00")
        depends_on("offline@12.05.00~g4", when="~g4")
        depends_on("offline@12.05.00+g4", when="+g4")
        depends_on("otsdaq-mu2e-tracker@v6_00_00")
        depends_on("otsdaq-mu2e-dqm@v6_00_00")
        depends_on("otsdaq-mu2e-trigger@v6_00_00")
        depends_on("mu2e-trig-config@v7_03_00")
    with when("@v7_01_00_cand"):
        depends_on("artdaq-core-mu2e@v8_00_02")
        depends_on("mu2e-pcie-utils@v6_00_00")
        depends_on("artdaq-mu2e@v6_00_00")
        depends_on("otsdaq-mu2e@v7_00_00")
        depends_on("otsdaq-mu2e-calorimeter@v7_00_00")
        depends_on("otsdaq-mu2e-crv@v5_00_00")
        depends_on("otsdaq-mu2e-extmon@v4_00_00")
        depends_on("otsdaq-mu2e-stm@v4_00_00")
        depends_on("offline@12.04.00~g4", when="~g4")
        depends_on("offline@12.04.00+g4", when="+g4")
        depends_on("otsdaq-mu2e-tracker@v6_00_00")
        depends_on("otsdaq-mu2e-dqm@v6_00_00")
        depends_on("otsdaq-mu2e-trigger@v6_00_00")
        depends_on("mu2e-trig-config@v7_00_00")
    with when("@v7_00_00_cand"):
        depends_on("artdaq-core-mu2e@v8_00_02")
        depends_on("mu2e-pcie-utils@v6_00_00")
        depends_on("artdaq-mu2e@v6_00_00")
        depends_on("otsdaq-mu2e@v7_00_00")
        depends_on("otsdaq-mu2e-calorimeter@v7_00_00")
        depends_on("otsdaq-mu2e-crv@v5_00_00")
        depends_on("otsdaq-mu2e-extmon@v4_00_00")
        depends_on("otsdaq-mu2e-stm@v4_00_00")
        depends_on("offline@12.03.00~g4", when="~g4")
        depends_on("offline@12.03.00+g4", when="+g4")
        depends_on("otsdaq-mu2e-tracker@v6_00_00")
        depends_on("otsdaq-mu2e-dqm@v6_00_00")
        depends_on("otsdaq-mu2e-trigger@v6_00_00")
        depends_on("mu2e-trig-config@v7_00_00")
    with when("@v6_00_00_cand"):
        depends_on("artdaq-core-mu2e@v7_00_00")
        depends_on("mu2e-pcie-utils@v5_00_00")
        depends_on("artdaq-mu2e@v5_00_00")
        depends_on("otsdaq-mu2e@v6_00_00")
        depends_on("otsdaq-mu2e-calorimeter@v6_00_00")
        depends_on("otsdaq-mu2e-crv@v4_00_00")
        depends_on("otsdaq-mu2e-extmon@v4_00_00")
        depends_on("otsdaq-mu2e-stm@v4_00_00")
        depends_on("offline@12.02.00~g4", when="~g4")
        depends_on("offline@12.02.00+g4", when="+g4")
        depends_on("otsdaq-mu2e-tracker@v5_00_00")
        depends_on("otsdaq-mu2e-dqm@v5_00_00")
        depends_on("otsdaq-mu2e-trigger@v5_00_00")
        depends_on("mu2e-trig-config@v6_00_00")
    with when("@v5_00_00"):
        depends_on("artdaq-core-mu2e@v5_01_00")
        depends_on("mu2e-pcie-utils@v4_00_00")
        depends_on("artdaq-mu2e@v5_00_00")
        depends_on("otsdaq-mu2e@v5_00_00")
        depends_on("otsdaq-mu2e-calorimeter@v5_00_00")
        depends_on("otsdaq-mu2e-crv@v4_00_00")
        depends_on("otsdaq-mu2e-extmon@v4_00_00")
        depends_on("otsdaq-mu2e-stm@v4_00_00")
        depends_on("offline@12.01.00~g4", when="~g4")
        depends_on("offline@12.01.00+g4", when="+g4")
        depends_on("otsdaq-mu2e-tracker@v4_00_00")
        depends_on("otsdaq-mu2e-dqm@v4_00_00")
        depends_on("otsdaq-mu2e-trigger@v5_00_00")
        depends_on("mu2e-trig-config@v5_00_00")
    with when("@v4_00_00"):
        depends_on("artdaq-core-mu2e@v4_00_00")
        depends_on("mu2e-pcie-utils@v4_00_00")
        depends_on("artdaq-mu2e@v4_00_00")
        depends_on("otsdaq-mu2e@v4_00_00")
        depends_on("otsdaq-mu2e-calorimeter@v4_00_01")
        depends_on("otsdaq-mu2e-crv@v4_00_00")
        depends_on("otsdaq-mu2e-extmon@v4_00_00")
        depends_on("otsdaq-mu2e-stm@v4_00_00")
        depends_on("offline@12.00.00~g4", when="~g4")
        depends_on("offline@12.00.00+g4", when="+g4")
        depends_on("otsdaq-mu2e-tracker@v4_00_00")
        depends_on("otsdaq-mu2e-dqm@v4_00_00")
        depends_on("otsdaq-mu2e-trigger@v4_00_00")
        depends_on("mu2e-trig-config@v4_00_00")

    with when("@develop"):
        depends_on("artdaq-core-mu2e")
        depends_on("mu2e-pcie-utils")
        depends_on("artdaq-mu2e")
        depends_on("otsdaq-mu2e")
        depends_on("otsdaq-mu2e-calorimeter")
        depends_on("otsdaq-mu2e-crv")
        depends_on("otsdaq-mu2e-extmon")
        depends_on("otsdaq-mu2e-stm")
        depends_on("otsdaq-mu2e-tracker")
        depends_on("offline")
        depends_on("otsdaq-mu2e-dqm")
        depends_on("otsdaq-mu2e-trigger")
        depends_on("mu2e-trig-config")
