# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

"""
    Base for ARM microcontrollers.
"""

from SCons.Script import Builder, DefaultEnvironment

env = DefaultEnvironment()

env.Replace(
    AR="arm-none-eabi-ar",
    AS="arm-none-eabi-gcc",
    CC="arm-none-eabi-gcc",
    CXX="arm-none-eabi-g++",
    OBJCOPY="arm-none-eabi-objcopy",
    RANLIB="arm-none-eabi-ranlib",
    SIZETOOL="arm-none-eabi-size",

    ASCOM=("$AS -o $TARGET -c -x assembler-with-cpp "
           "$CFLAGS $CCFLAGS $_CCCOMCOM $SOURCES"),

    ARFLAGS=["rcs"],

    CPPFLAGS=[
        "-g",   # include debugging info (so errors include line numbers)
        "-Os",  # optimize for size
        "-ffunction-sections",  # place each function in its own section
        "-fdata-sections",
        "-Wall",
        "-mthumb",
        "-mcpu=${BOARD_OPTIONS['build']['cpu']}",
        "-nostdlib",
        "-MMD"  # output dependancy info
    ],

    CXXFLAGS=[
        "-fno-rtti",
        "-fno-exceptions"
    ],

    CPPDEFINES=[
        "F_CPU=$BOARD_F_CPU"
    ],

    LINKFLAGS=[
        "-Os",
        "-Wl,--gc-sections",
        "-mthumb",
        "-mcpu=${BOARD_OPTIONS['build']['cpu']}"
    ],

    SIZEPRINTCMD='"$SIZETOOL" -B -d $SOURCES'
)

if env.get("BOARD_OPTIONS", {}).get("build", {}).get("cpu", "")[-2:] == "m4":
    env.Append(
        ASFLAGS=[
            "-mfloat-abi=hard",
            "-mfpu=fpv4-sp-d16",
            "-fsingle-precision-constant"
        ],
        CCFLAGS=[
            "-mfloat-abi=hard",
            "-mfpu=fpv4-sp-d16",
            "-fsingle-precision-constant"
        ],
        LINKFLAGS=[
            "-mfloat-abi=hard",
            "-mfpu=fpv4-sp-d16",
            "-fsingle-precision-constant"
        ]
    )

env.Append(
    BUILDERS=dict(
        ElfToBin=Builder(
            action=" ".join([
                "$OBJCOPY",
                "-O",
                "binary",
                "$SOURCES",
                "$TARGET"]),
            suffix=".bin"
        ),
        ElfToHex=Builder(
            action=" ".join([
                "$OBJCOPY",
                "-O",
                "ihex",
                "-R",
                ".eeprom",
                "$SOURCES",
                "$TARGET"]),
            suffix=".hex"
        )
    )
)
