# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Mu2eTdaqSuite(BundlePackage):
    """The Mu2e TDAQ Suite, the software used for Mu2e trigger and data acquisition"""

    version("develop")
    version("v6_00_00")
    version("v5_00_00")
    version("v4_00_00")
    version("v3_04_00")
    version("v3_03_01")
    version("v3_03_00")
    version("v3_02_00")
    version("v3_01_00")
    version("v3_00_00")
    version("v1_04_00")
    version("v1_02_03")
    version("v1_02_02")

    # The art-suite Dependency
    squals = ("112", "117", "118", "122", "123", "126", "128", "130", "131", "132")
    variant(
        "s",
        default="132",
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
        default="31600",
        values=(
            "0",
            "31202",
            "31203",
            "31204",
            "31205",
            "31207",
            "31300",
            "31301",
            "31400",
            "31401",
            "31500",
            "31600",
        ),
        multi=False,
        description="Artdaq suite version to use",
        when="@:v4_00_00",
    )
    variant(
        "artdaq",
        default="40200",
        values=("0", "40000", "40100", "40200"),
        multi=False,
        description="Artdaq suite version to use",
        when="@v4_00_00:,develop",
    )
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
        default="21000",
        values=(
            "0",
            "20608",
            "20609",
            "20700",
            "20800",
            "20801",
            "20802",
            "20900",
            "20901",
            "21000",
        ),
        multi=False,
        description="Otsdaq version to use",
        when="@:v4_00_00",
    )
    variant(
        "otsdaq",
        default="30100",
        values=("0", "30000", "30100", "30200"),
        multi=False,
        description="Otsdaq version to use",
        when="@v4_00_00:,develop",
    )
    depends_on("otsdaq-suite@v3_02_00", when="otsdaq=30200")
    depends_on("otsdaq-suite@v3_01_00", when="otsdaq=30100")
    depends_on("otsdaq-suite@v3_00_00", when="otsdaq=30000")
    depends_on("otsdaq-suite@v2_10_00", when="otsdaq=21000")
    depends_on("otsdaq-suite@v2_09_01", when="otsdaq=20901")
    depends_on("otsdaq-suite@v2_09_00", when="otsdaq=20900")
    depends_on("otsdaq-suite@v2_08_02", when="otsdaq=20802")
    depends_on("otsdaq-suite@v2_08_01", when="otsdaq=20801")
    depends_on("otsdaq-suite@v2_08_00", when="otsdaq=20800")
    depends_on("otsdaq-suite@v2_07_00", when="otsdaq=20700")
    depends_on("otsdaq-suite@v2_06_09", when="otsdaq=20609")
    depends_on("otsdaq-suite@v2_06_08", when="otsdaq=20608")
    depends_on("otsdaq-suite")

    # g4 Variant
    variant(
        "g4",
        default=False,
        description="Whether to build the G4 variant of the Offline",
    )

    # Bundle package, list packages that are part of the bundle
    with when("@v6_00_00"):
        depends_on("artdaq-core-mu2e@v7_00_00")
        depends_on("mu2e-pcie-utils@v5_00_00")
        depends_on("artdaq-mu2e@v5_00_00")
        depends_on("otsdaq-mu2e@v6_00_00")
        depends_on("otsdaq-mu2e-calorimeter@v6_00_00")
        depends_on("otsdaq-mu2e-crv@v4_00_00")
        depends_on("otsdaq-mu2e-extmon@v4_00_00")
        depends_on("otsdaq-mu2e-stm@v4_00_00")
        depends_on("Offline@12.02.00~g4", when="~g4")
        depends_on("Offline@12.02.00+g4", when="+g4")
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
        depends_on("Offline@12.01.00~g4", when="~g4")
        depends_on("Offline@12.01.00+g4", when="+g4")
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
        depends_on("Offline@12.00.00~g4", when="~g4")
        depends_on("Offline@12.00.00+g4", when="+g4")
        depends_on("otsdaq-mu2e-tracker@v4_00_00")
        depends_on("otsdaq-mu2e-dqm@v4_00_00")
        depends_on("otsdaq-mu2e-trigger@v4_00_00")
        depends_on("mu2e-trig-config@v4_00_00")
    with when("@v3_04_00"):
        depends_on("artdaq-core-mu2e@v3_04_00")
        depends_on("mu2e-pcie-utils@v3_04_00")
        depends_on("artdaq-mu2e@v3_04_00")
        depends_on("otsdaq-mu2e@v3_04_00")
        depends_on("otsdaq-mu2e-calorimeter@v3_04_00")
        depends_on("otsdaq-mu2e-crv@v3_04_00")
        depends_on("otsdaq-mu2e-extmon@v3_04_00")
        depends_on("otsdaq-mu2e-stm@v3_04_00")
        depends_on("Offline@11.05.01~g4", when="~g4")
        depends_on("Offline@11.05.01+g4", when="+g4")
        depends_on("otsdaq-mu2e-tracker@v3_04_00")
        depends_on("otsdaq-mu2e-dqm@v3_04_00")
        depends_on("otsdaq-mu2e-trigger@v3_04_00")
        depends_on("mu2e-trig-config@v3_07_00")
    with when("@v3_03_01"):
        depends_on("artdaq-core-mu2e@v3_03_01")
        depends_on("mu2e-pcie-utils@v3_03_01")
        depends_on("artdaq-mu2e@v3_03_01")
        depends_on("otsdaq-mu2e@v3_03_01")
        depends_on("otsdaq-mu2e-calorimeter@v3_03_01")
        depends_on("otsdaq-mu2e-crv@v3_03_01")
        depends_on("otsdaq-mu2e-extmon@v3_03_01")
        depends_on("otsdaq-mu2e-stm@v3_03_01")
        depends_on("Offline@11.04.00~g4", when="~g4")
        depends_on("Offline@11.04.00+g4", when="+g4")
        depends_on("otsdaq-mu2e-tracker@v3_03_01")
        depends_on("otsdaq-mu2e-dqm@v3_03_01")
        depends_on("otsdaq-mu2e-trigger@v3_03_01")
        depends_on("mu2e-trig-config@v3_03_01")
    with when("@v3_03_00"):
        depends_on("artdaq-core-mu2e@v3_03_00")
        depends_on("mu2e-pcie-utils@v3_03_00")
        depends_on("artdaq-mu2e@v3_03_00")
        depends_on("otsdaq-mu2e@v3_03_00")
        depends_on("otsdaq-mu2e-calorimeter@v3_03_00")
        depends_on("otsdaq-mu2e-crv@v3_03_00")
        depends_on("otsdaq-mu2e-extmon@v3_03_00")
        depends_on("otsdaq-mu2e-stm@v3_03_00")
        depends_on("Offline@11.03.00~g4", when="~g4")
        depends_on("Offline@11.03.00+g4", when="+g4")
        depends_on("otsdaq-mu2e-tracker@v3_03_00")
        depends_on("otsdaq-mu2e-dqm@v3_03_00")
        depends_on("otsdaq-mu2e-trigger@v3_03_00")
        depends_on("mu2e-trig-config@v3_03_00")
    with when("@v3_02_00"):
        depends_on("artdaq-core-mu2e@v3_02_00")
        depends_on("mu2e-pcie-utils@v3_02_00")
        depends_on("artdaq-mu2e@v3_02_00")
        depends_on("otsdaq-mu2e@v3_02_00")
        depends_on("otsdaq-mu2e-calorimeter@v3_02_00")
        depends_on("otsdaq-mu2e-crv@v3_02_00")
        depends_on("otsdaq-mu2e-extmon@v3_02_00")
        depends_on("otsdaq-mu2e-stm@v3_02_00")
        depends_on("Offline@11.02.00~g4", when="~g4")
        depends_on("Offline@11.02.00+g4", when="+g4")
        depends_on("otsdaq-mu2e-tracker@v3_02_00")
        depends_on("otsdaq-mu2e-dqm@v3_02_00")
        depends_on("otsdaq-mu2e-trigger@v3_02_00")
        depends_on("mu2e-trig-config@v3_02_00")
    with when("@v3_01_00"):
        depends_on("artdaq-core-mu2e@v3_01_00")
        depends_on("mu2e-pcie-utils@v3_01_00")
        depends_on("artdaq-mu2e@v3_01_00")
        depends_on("otsdaq-mu2e@v3_01_00")
        depends_on("otsdaq-mu2e-calorimeter@v3_01_00")
        depends_on("otsdaq-mu2e-crv@v3_01_00")
        depends_on("otsdaq-mu2e-extmon@v3_01_00")
        depends_on("otsdaq-mu2e-stm@v3_01_00")
        depends_on("Offline@11.02.00")
        depends_on("otsdaq-mu2e-tracker@v3_01_00")
        depends_on("otsdaq-mu2e-dqm@v3_01_00")
        depends_on("otsdaq-mu2e-trigger@v3_01_00")
        depends_on("mu2e-trig-config@v3_01_00")
    with when("@v3_00_00"):
        depends_on("artdaq-core-mu2e@v3_00_00")
        depends_on("mu2e-pcie-utils@v3_00_00")
        depends_on("artdaq-mu2e@v3_00_00")
        depends_on("otsdaq-mu2e@v3_00_00")
        depends_on("otsdaq-mu2e-calorimeter@v3_00_00")
        depends_on("otsdaq-mu2e-crv@v3_00_00")
        depends_on("otsdaq-mu2e-extmon@v3_00_00")
        depends_on("otsdaq-mu2e-stm@v3_00_00")
        depends_on("Offline@11.01.00")
        depends_on("otsdaq-mu2e-tracker@v3_00_00")
        depends_on("otsdaq-mu2e-dqm@v3_00_00")
        depends_on("otsdaq-mu2e-trigger@v3_00_00")
    with when("@v1_04_00"):
        depends_on("artdaq-core-mu2e@v2_01_02")
        depends_on("mu2e-pcie-utils@v2_09_01")
        depends_on("artdaq-mu2e@v1_07_00")
        depends_on("otsdaq-mu2e@v1_04_00")
        depends_on("otsdaq-mu2e-calorimeter@v1_04_00")
        depends_on("otsdaq-mu2e-crv@v1_04_00")
        depends_on("otsdaq-mu2e-extmon@v1_04_00")
        depends_on("otsdaq-mu2e-stm@v1_04_00")
        # depends_on("otsdaq-mu2e-tracker@v1_04_00")
        depends_on("Offline@11.00.01")
        depends_on("otsdaq-mu2e-dqm@v1_04_00")
        depends_on("otsdaq-mu2e-trigger@v1_04_00")
    with when("@v1_02_02"):
        depends_on("mu2e-pcie-utils@v2_08_00")
        depends_on("artdaq-core-mu2e@v1_08_04")
        depends_on("artdaq-mu2e@v1_05_02")
        depends_on("otsdaq-mu2e@v1_02_02")

    with when("@develop"):
        depends_on("artdaq-core-mu2e@develop")
        depends_on("mu2e-pcie-utils@develop")
        depends_on("artdaq-mu2e@develop")
        depends_on("otsdaq-mu2e@develop")
        depends_on("otsdaq-mu2e-calorimeter@develop")
        depends_on("otsdaq-mu2e-crv@develop")
        depends_on("otsdaq-mu2e-extmon@develop")
        depends_on("otsdaq-mu2e-stm@develop")
        depends_on("otsdaq-mu2e-tracker@develop")
        depends_on("Offline@main")
        depends_on("otsdaq-mu2e-dqm@develop")
        depends_on("otsdaq-mu2e-trigger@develop")
        depends_on("mu2e-trig-config@main")
