"""The site's information architecture.

Every page on the site is declared here: what repository content it is built
from, which section and group it sits in, the images it shows and the files it
offers. The repository stays the single home of the knowledge; this file only
says how to present it.

`rewrites` are exact substring replacements applied to a page's markdown before
rendering. They exist for presentation only: the site is timeless, so dated
phrases become "at the time of writing"; screenshot names become real captions;
a heading level that fights the page structure is corrected. The build fails
when a rewrite no longer matches its source, so editing a guide cannot silently
orphan one.
"""

from __future__ import annotations

from dataclasses import dataclass

REPO_OWNER = "oernster"
REPO_NAME = "3D-printing-info"
REPO_BRANCH = "main"
REPO_URL = f"https://github.com/{REPO_OWNER}/{REPO_NAME}"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{REPO_BRANCH}/"
BLOB_BASE = f"{REPO_URL}/blob/{REPO_BRANCH}/"
TREE_BASE = f"{REPO_URL}/tree/{REPO_BRANCH}/"

SITE_URL = "https://ernster.dev/3D-printing-info/"
SITE_PATH = "/3D-printing-info/"
SITE_NAME = "3D-printing-info"
SITE_TAGLINE = "An open Voron, Klipper and Bambu knowledge base"
AUTHOR = "Oliver Ernster"
AUTHOR_URL = "https://www.crankthecode.com"
GITHUB_PROFILE = "https://github.com/oernster"
DONATE_URL = "https://www.paypal.com/donate/?hosted_button_id=R3DFLDWT2PFC4"
ESSAY_URL = "https://www.crankthecode.com/posts/3D-printing-info"
LICENCE_URL = f"{BLOB_BASE}LICENSE"
HERO_IMAGE = "hero.png"
HERO_ALT = (
    "A sculpted head contemplating a workbench of 3D printers, filament spools "
    "and printed parts on a blue schematic backdrop"
)


@dataclass(frozen=True, slots=True)
class Figure:
    path: str
    caption: str
    group: str = ""


@dataclass(frozen=True, slots=True)
class FileRef:
    path: str
    label: str
    note: str = ""


@dataclass(frozen=True, slots=True)
class Page:
    slug: str
    title: str
    summary: str
    group: str = ""
    kind: str = "article"
    source: str | None = None
    extra_sources: tuple[str, ...] = ()
    intro: str = ""
    figures: tuple[Figure, ...] = ()
    files: tuple[FileRef, ...] = ()
    covers: tuple[str, ...] = ()
    rewrites: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class Section:
    key: str
    title: str
    nav_title: str
    blurb: str
    icon: str
    unit: str = ""
    groups: tuple[str, ...] = ()
    pages: tuple[Page, ...] = ()
    in_main_nav: bool = True


@dataclass(frozen=True, slots=True)
class Project:
    name: str
    tagline: str
    body: str
    site: str
    repo: str
    icon: str
    image: str
    image_alt: str
    extra: str = ""


@dataclass(frozen=True, slots=True)
class StartPath:
    title: str
    blurb: str
    slugs: tuple[str, ...]


_SNT_ASSETS = "https://github.com/user-attachments/assets/"


def _captioned(name: str, asset: str, alt: str, caption: str) -> tuple[str, str]:
    """A rewrite giving a screenshot named by its date real alt text and a caption."""
    url = f"{_SNT_ASSETS}{asset}"
    return f"![{name}]({url})", f'![{alt}]({url} "{caption}")'


GUIDES = Section(
    key="guides",
    title="Guides",
    nav_title="Guides",
    blurb=(
        "Step-by-step write-ups for tuning, printing technique, troubleshooting "
        "and getting Klipper running, each one learned on real machines."
    ),
    icon="book",
    unit="guides",
    groups=(
        "Tuning and calibration",
        "Printing technique",
        "Troubleshooting",
        "Klipper setup",
        "Hardware and reference",
    ),
    pages=(
        Page(
            slug="guides/shake-n-tune",
            title="Shake 'n' Tune: belts, input shaping and vibrations",
            summary=(
                "Tune the A and B belts to 110Hz, run input shaping and read the "
                "vibrations profile with Klippain Shake&Tune, with real result "
                "graphs to aim for."
            ),
            group="Tuning and calibration",
            source="guides/ShakeNTuneBriefIntro.md",
            rewrites=(
                _captioned(
                    "Screenshot 2025-03-18 221958",
                    "c6b014e4-a44a-44ab-93b2-f29f2d5c7ba9",
                    "Compare belts responses graph",
                    "Compare belts responses: the A and B belt peaks are almost aligned",
                ),
                _captioned(
                    "Screenshot 2025-03-18 222200",
                    "0217a276-59e0-486e-8093-a7b5ae789984",
                    "Y axis input shaper graph",
                    "Axis shaper calibration for Y: the shape to aim for on both axes",
                ),
                _captioned(
                    "Screenshot 2025-03-18 221840",
                    "d16b2b3c-9332-4cc6-b9ac-62b7901d8f63",
                    "Vibrations profile graphs",
                    "Create vibrations profile, run with TMC Autotune",
                ),
            ),
        ),
        Page(
            slug="guides/pid-tuning",
            title="Manual PID tuning",
            summary=(
                "How to raise P, I and D by hand when a heater will not settle on "
                "its setpoint."
            ),
            group="Tuning and calibration",
            source="guides/PIDTuning.md",
        ),
        Page(
            slug="guides/temperature-tower",
            title="Temperature towers",
            summary=(
                "Add M109 or M104 at each step of a temperature tower in the "
                "slicer preview to find a filament's sweet spot, on Marlin or "
                "Klipper."
            ),
            group="Tuning and calibration",
            source="guides/temp-tower-guide.md",
        ),
        Page(
            slug="guides/first-layer-levelling",
            title="First-layer levelling square",
            summary=(
                "Print a thin, scaled primitive cube and live-adjust Z until the "
                "square comes out perfect, with a photo of what good looks like."
            ),
            group="Tuning and calibration",
            source="guides/levelling/levelling.md",
            figures=(
                Figure(
                    "guides/levelling/LevellingSquare.jpg",
                    "A levelling square printed with a good first layer",
                ),
            ),
        ),
        Page(
            slug="guides/rotation-distance",
            title="Rotation distance calculators",
            summary=(
                "Two calculators for working out Klipper's rotation_distance when "
                "calibrating an extruder."
            ),
            group="Tuning and calibration",
            source="guides/klipper/rotation-distance-calc-klipper.md",
        ),
        Page(
            slug="guides/bed-adhesion",
            title="Bed adhesion",
            summary=(
                "Clean, degrease and pick an adhesive, including a home-made PVP "
                "glue recipe checked on a chemistry Discord."
            ),
            group="Printing technique",
            source="guides/adhesion.md",
        ),
        Page(
            slug="guides/drying-filament",
            title="Drying and storing filament",
            summary=(
                "Why wet filament ruins prints, how to dry it and how to keep it "
                "dry with a storage box and the right desiccant."
            ),
            group="Printing technique",
            source="guides/drying.md",
            rewrites=(
                (
                    "on the market currently (Jan 2025) is",
                    "on the market at the time of writing is",
                ),
            ),
        ),
        Page(
            slug="guides/colour-changes",
            title="Colour changes without a multi-material unit",
            summary=(
                "Multi-colour prints from a single extruder using slicer filament "
                "changes, with a Captain America key fob STL to practise on."
            ),
            group="Printing technique",
            source="guides/colour-swap/README-filament-change.md",
            figures=(
                Figure(
                    "guides/colour-swap/KeyFobCaptainAmericaTopDown.jpg",
                    "The finished Captain America key fob from above",
                ),
                Figure(
                    "guides/colour-swap/KeyFobCaptainAmericaSideShot.jpg",
                    "The Captain America key fob from the side",
                ),
                Figure(
                    "guides/colour-swap/PrusaSlicerScreenshot.jpg",
                    "The key fob sliced in PrusaSlicer with its colour changes",
                ),
                Figure(
                    "guides/colour-swap/tazmanian-devil-example.jpg",
                    "A Tasmanian Devil key fob printed the same way",
                ),
            ),
            files=(
                FileRef(
                    "guides/colour-swap/keyfob-Captain-America.stl",
                    "Captain America key fob STL",
                    "Needs red, blue and white PLA.",
                ),
            ),
        ),
        Page(
            slug="guides/painting-prints",
            title="Painting prints",
            summary="The acrylic paint set and brushes used for finishing models.",
            group="Printing technique",
            source="guides/painting.md",
        ),
        Page(
            slug="guides/slicers",
            title="Choosing a slicer",
            summary=(
                "Cura, PrusaSlicer, SuperSlicer, Orca Slicer and Bambu Studio, "
                "weighed up from long daily use."
            ),
            group="Printing technique",
            source="guides/slicers-guide.md",
        ),
        Page(
            slug="guides/stealthburner-clogs",
            title="Clearing a Stealthburner clog",
            summary=(
                "A six-step checklist from the extruder down to the nozzle, plus "
                "the declogging tools worth owning."
            ),
            group="Troubleshooting",
            source="guides/resolving-clogs-stealthburner.md",
        ),
        Page(
            slug="guides/klipper-setup",
            title="Klipper setup from scratch",
            summary=(
                "Flash Mainsail, install Klipper with KIAUH, build and flash the "
                "firmware, then find the MCU serial path for printer.cfg."
            ),
            group="Klipper setup",
            source="guides/klipper/klipper-general-setup-guide.md",
            rewrites=(
                ("do a \nmake\n\n and then copy", "run `make` then copy"),
                (" - that will show you whether", "That will show you whether"),
            ),
        ),
        Page(
            slug="guides/sovol-sv06-klipper",
            title="Sovol SV06 on Klipper",
            summary=(
                "Flash Klipper to a stock Sovol SV06 with a prebuilt firmware and "
                "a ready printer.cfg, then point the slicer at it."
            ),
            group="Klipper setup",
            source="guides/klipper/sovol-sv06/README.md",
            files=(
                FileRef(
                    "guides/klipper/sovol-sv06/printer.cfg",
                    "printer.cfg for the stock SV06",
                ),
                FileRef(
                    "guides/klipper/sovol-sv06/firmware.bin",
                    "Prebuilt Klipper firmware",
                    "Copy to the root of the SD card as firmware.bin.",
                ),
            ),
            rewrites=(("# Superslicer", "### Superslicer"),),
        ),
        Page(
            slug="guides/tronxy-x5sa-klipper",
            title="Tronxy X5SA on Klipper or Marlin",
            summary=(
                "Flash Klipper or Marlin to a Tronxy X5SA with an F446 board from "
                "the SD card update folder, then set up Mainsail and the slicer."
            ),
            group="Klipper setup",
            source="guides/klipper/tronxy-x5sa/README.md",
            files=(
                FileRef(
                    "guides/klipper/tronxy-x5sa/printer.cfg",
                    "printer.cfg for the X5SA",
                ),
                FileRef(
                    "guides/klipper/tronxy-x5sa/flashing-klipper/",
                    "Klipper update folder",
                    "Copy the whole update folder, the folder itself included, to "
                    "the root of the SD card.",
                ),
                FileRef(
                    "guides/klipper/tronxy-x5sa/flashing-marlin/",
                    "Marlin update folder",
                    "Copy the whole update folder, the folder itself included, to "
                    "the root of the SD card.",
                ),
            ),
            rewrites=(("# Prusa/Superslicer", "### Prusa/Superslicer"),),
        ),
        Page(
            slug="guides/klipper-sounds",
            title="Custom sounds in Klipper",
            summary=(
                "Play WAV samples at startup, print start and print end through "
                "gcode_shell_command and USB speakers on a Raspberry Pi."
            ),
            group="Hardware and reference",
            source="guides/setup-sounds-wavs-klipper.md",
            rewrites=(
                (
                    "defaults.ctl.card 0\n\ndefaults.pcm.card 0\n\ndefaults.pcm.device 0",
                    "```\ndefaults.ctl.card 0\ndefaults.pcm.card 0\ndefaults.pcm.device 0\n```",
                ),
            ),
        ),
        Page(
            slug="guides/eddy-current-probes",
            title="Eddy current probes compared",
            summary=(
                "Beacon, Cartographer and the other eddy current scanners weighed "
                "up, with the CNC mount and meshing around bed magnets."
            ),
            group="Hardware and reference",
            source="guides/eddy-current-probes.md",
            rewrites=(
                (
                    "on the market as of October 2024.",
                    "on the market at the time of writing.",
                ),
            ),
        ),
        Page(
            slug="guides/moonraker-macro",
            title="Run a Klipper macro through Moonraker",
            summary=(
                "A short Python script that fires a macro through the Moonraker "
                "API and skips the end-of-print sound during the small hours."
            ),
            group="Hardware and reference",
            source="moonraker/call_gcode_macro/README.md",
            files=(
                FileRef(
                    "moonraker/call_gcode_macro/call_gcode_macro.py",
                    "call_gcode_macro.py",
                ),
            ),
        ),
        Page(
            slug="guides/linux-commands",
            title="Handy Linux commands",
            summary=(
                "Find the printer's serial path and inspect connected webcams on a "
                "Klipper host."
            ),
            group="Hardware and reference",
            source="handy-linux-cmds/README.md",
        ),
    ),
)

FAQS = Section(
    key="faqs",
    title="FAQs",
    nav_title="FAQs",
    blurb=(
        "Short answers to the problems that come up again and again on Bambu Lab "
        "and Voron printers."
    ),
    icon="help",
    unit="answers",
    groups=("Bambu Lab", "Voron"),
    pages=(
        Page(
            slug="faqs/ams-feeding-failures",
            title="AMS feeding failures",
            summary=(
                "Six causes of filament shuttling back and forth or asking for a "
                "retry, from a frayed bowden clamp to a blunt cutter."
            ),
            group="Bambu Lab",
            source="FAQs/bambu/AMSFeedingFailures.md",
        ),
        Page(
            slug="faqs/ams-cleaning",
            title="Cleaning an AMS that flashes red",
            summary=(
                "A full strip-down and clean of the AMS feeder internals: the tools "
                "needed, what to watch for and the reassembly order."
            ),
            group="Bambu Lab",
            source="FAQs/bambu/BambuAMSCleaning.md",
            covers=("FAQs/README.md",),
            rewrites=(
                (
                    "# Hard work done - now to put it back together...",
                    "## Hard work done - now to put it back together...",
                ),
            ),
        ),
        Page(
            slug="faqs/cutter-stuck",
            title="Cutter stuck on the X1C",
            summary="Usually filament in the hotend: heat it to 250C and push it through.",
            group="Bambu Lab",
            source="FAQs/bambu/CutterStuck.md",
        ),
        Page(
            slug="faqs/layer-shift-causes",
            title="Unusual layer shift causes",
            summary=(
                "Five less documented causes of layer shifts, from dry rails to "
                "lead screw play and belt similarity."
            ),
            group="Voron",
            source="FAQs/voron/layershiftcauses.md",
        ),
        Page(
            slug="faqs/mellow-5160-sensorless",
            title="Mellow 5160 drivers sensorless on an Octopus Pro",
            summary=(
                "Jumpers, ribbon orientation, starting SGT values and the TMC "
                "commands that prove the drivers respond."
            ),
            group="Voron",
            source="FAQs/voron/mellow-5160-steppers-sensorless.md",
        ),
        Page(
            slug="faqs/ebb36-motor-wiring",
            title="EBB36 motor wire order",
            summary=(
                "Pulled the wires out of a motor connector? The colour order for "
                "an LDO NEMA14 on a BTT EBB36 v1.2."
            ),
            group="Voron",
            source="FAQs/voron/motor-wiring.md",
        ),
        Page(
            slug="faqs/trident-levelling-probe",
            title="Levelling a Trident with a probe",
            summary=(
                "PROBE_CALIBRATE with paper, then a thin scaled cube and live Z "
                "adjustment for a perfect first layer."
            ),
            group="Voron",
            source="FAQs/voron/voron-trident-levelling-probe.md",
        ),
        Page(
            slug="faqs/voron0-levelling-no-probe",
            title="Levelling a Voron 0 without a probe",
            summary=(
                "BED_SCREWS_ADJUST with paper, then a thin cube and live Z until "
                "the first layer is right."
            ),
            group="Voron",
            source="FAQs/voron/voron0-levelling-no-probe.md",
        ),
    ),
)

_LEVIATHAN = "printers/leviathan-sensorless-config/"
_LEVIATHAN_EXAMPLE = f"{_LEVIATHAN}example-leviathan-24-300-config/"
_V0 = "printers/voron0.2-now-sold-full-config/"
_QIDI = "printers/qidiq1pro/"

PRINTERS = Section(
    key="printers",
    title="Printers",
    nav_title="Printers",
    blurb=(
        "The machines behind the notes: build sheets, recovery procedures and the "
        "configs they ran."
    ),
    icon="box",
    unit="printer pages",
    groups=("Voron Trident 350", "Qidi Q1 Pro", "Voron 2.4", "Voron 0.2", "Add-on configs"),
    pages=(
        Page(
            slug="printers/voron-trident-350",
            title="Voron Trident 350 build",
            summary=(
                "A Formbot Trident rebuilt piece by piece: Hypernova toolhead, "
                "Cartographer probe, Mellow 5160 drivers, 48V motion and the "
                "Klipper plugins it runs."
            ),
            group="Voron Trident 350",
            source="printers/README.md",
            intro=(
                "The complete, current Trident config lives in its own repository, "
                "[VT350](https://github.com/oernster/VT350). This page is the "
                "build sheet: every upgrade with a link to the part."
            ),
            figures=(
                Figure("printers/my-printers-images/VT350.jpg", "The Voron Trident 350"),
            ),
            files=(
                FileRef(
                    "voron-startup/VORONTRIDENT-STARTUP.cfg",
                    "Trident PRINT_START and PRINT_END macros",
                ),
            ),
            covers=("printers/voronTrident350/README.md",),
            rewrites=(
                (
                    "# Klipper (Now Kalico) plugins...",
                    "## Klipper (Now Kalico) plugins...",
                ),
            ),
        ),
        Page(
            slug="printers/qidi-q1-pro-recovery",
            title="Qidi Q1 Pro: recover the operating system",
            summary=(
                "Bring a broken Q1 Pro back from a known-good OS image: eMMC "
                "adapter, WSL, rsync, the UI recovery file and a firmware update."
            ),
            group="Qidi Q1 Pro",
            source=f"{_QIDI}README.md",
            figures=(
                Figure("printers/my-printers-images/QidiQ1Pro.jpg", "The Qidi Q1 Pro"),
            ),
            files=(
                FileRef(f"{_QIDI}qidq1pro-os.tar.gz", "Q1 Pro operating system tarball"),
                FileRef(f"{_QIDI}updated-configs/gcode_macro.cfg", "Updated gcode_macro.cfg"),
                FileRef(f"{_QIDI}updated-configs/timelapse.cfg", "Updated timelapse.cfg"),
            ),
            covers=(f"{_QIDI}.gitattributes",),
            rewrites=(
                (
                    "(as of Xmas Day 2024 this is Q1_V4.4.24.zip)",
                    "(at the time of writing this is Q1_V4.4.24.zip)",
                ),
                (
                    "## As an aside the root password is `makerbase`",
                    "As an aside the root password is `makerbase`.",
                ),
            ),
        ),
        Page(
            slug="printers/qidi-q1-pro-mainsail",
            title="Qidi Q1 Pro: add Mainsail",
            summary=(
                "Serve Mainsail on port 8081 beside the stock interface, using the "
                "nginx site file from the repository."
            ),
            group="Qidi Q1 Pro",
            source=f"{_QIDI}mainsail-setup/README.md",
            files=(FileRef(f"{_QIDI}mainsail-setup/mainsail", "nginx site file for Mainsail"),),
        ),
        Page(
            slug="printers/qidi-q1-pro-emmc-clone",
            title="Qidi Q1 Pro: flash the cloned eMMC",
            summary=(
                "Extract the cloned eMMC backup with 7-Zip and write it to the "
                "module with BalenaEtcher."
            ),
            group="Qidi Q1 Pro",
            source=f"{_QIDI}qidi-emmc-clone/README.md",
            files=(FileRef(f"{_QIDI}qidi-emmc-clone/qidibackup.7z", "Cloned eMMC backup"),),
            covers=(f"{_QIDI}qidi-emmc-clone/.gitattributes",),
        ),
        Page(
            slug="printers/voron-2-4-leviathan",
            title="Voron 2.4 on a Leviathan, sensorless",
            summary=(
                "Sensorless X and Y homing for a 300mm Voron 2.4 on a BTT "
                "Leviathan, plus a complete example config with Nitehawk, Beacon "
                "and KAMP."
            ),
            group="Voron 2.4",
            source=f"{_LEVIATHAN}README.md",
            files=(
                FileRef(f"{_LEVIATHAN}LeviathanSteppersPrinter.cfg", "X and Y stepper sections"),
                FileRef(f"{_LEVIATHAN}leviathansensorless.cfg", "Sensorless homing macros"),
                FileRef(f"{_LEVIATHAN_EXAMPLE}printer.cfg", "Example printer.cfg"),
                FileRef(f"{_LEVIATHAN_EXAMPLE}mainsail.cfg", "mainsail.cfg"),
                FileRef(f"{_LEVIATHAN_EXAMPLE}moonraker.conf", "moonraker.conf"),
                FileRef(f"{_LEVIATHAN_EXAMPLE}KAMP_Settings.cfg", "KAMP_Settings.cfg"),
                FileRef(f"{_LEVIATHAN_EXAMPLE}KlipperScreen.conf", "KlipperScreen.conf"),
                FileRef(f"{_LEVIATHAN_EXAMPLE}crowsnest.conf", "crowsnest.conf"),
                FileRef(f"{_LEVIATHAN_EXAMPLE}webcam.txt", "webcam.txt"),
                FileRef(f"{_LEVIATHAN_EXAMPLE}hardware/SFS_v2.cfg", "BTT SFS v2 filament sensor"),
                FileRef(f"{_LEVIATHAN_EXAMPLE}hardware/auto_speed.cfg", "Klipper auto speed"),
                FileRef(f"{_LEVIATHAN_EXAMPLE}hardware/stealthburner_led.cfg", "Stealthburner LEDs"),
                FileRef(f"{_LEVIATHAN_EXAMPLE}macros/macros.cfg", "General macros"),
                FileRef(f"{_LEVIATHAN_EXAMPLE}macros/print_start.cfg", "PRINT_START macro"),
                FileRef(f"{_LEVIATHAN_EXAMPLE}KAMP/Adaptive_Meshing.cfg", "KAMP adaptive meshing"),
                FileRef(f"{_LEVIATHAN_EXAMPLE}KAMP/KAMP_Settings.cfg", "KAMP settings"),
                FileRef(f"{_LEVIATHAN_EXAMPLE}KAMP/Line_Purge.cfg", "KAMP line purge"),
                FileRef(f"{_LEVIATHAN_EXAMPLE}KAMP/Smart_Park.cfg", "KAMP smart park"),
                FileRef(f"{_LEVIATHAN_EXAMPLE}KAMP/Voron_Purge.cfg", "KAMP Voron purge"),
                FileRef(
                    "voron-startup/VORON2-4-STARTUP.cfg",
                    "Voron 2.4 PRINT_START and PRINT_END macros",
                ),
            ),
        ),
        Page(
            slug="printers/voron-0-2",
            title="Voron 0.2 config",
            summary=(
                "The complete Klipper config from a Voron 0.2 on an SKR Mini E3 V3 "
                "with an LDO Picobilical, kept for reference after the printer was "
                "sold."
            ),
            group="Voron 0.2",
            kind="files",
            intro=(
                "The printer has gone to a new home; its configuration stays here "
                "as a working reference for a Voron 0.2 on a BTT SKR Mini E3 V3 "
                "with an LDO Picobilical umbilical board. Open any file to read it "
                "with highlighting, copy it or download it."
            ),
            files=(
                FileRef(f"{_V0}printer.cfg", "printer.cfg"),
                FileRef(f"{_V0}picobilical.cfg", "LDO Picobilical"),
                FileRef(f"{_V0}display.cfg", "Display"),
                FileRef(f"{_V0}adxlmcu.cfg", "ADXL MCU"),
                FileRef(f"{_V0}mainsail_macros.cfg", "Mainsail macros"),
                FileRef(f"{_V0}kiauh_macros.cfg", "KIAUH macros"),
                FileRef(f"{_V0}moonraker.conf", "moonraker.conf"),
                FileRef(f"{_V0}webcam.txt", "webcam.txt"),
            ),
            covers=(f"{_V0}README.md",),
        ),
        Page(
            slug="printers/add-on-configs",
            title="Nevermore and Stealthburner LED configs",
            summary=(
                "Macros that run Nevermore filter fans from the bed temperature, "
                "plus Stealthburner LED status macros without Rainbow Barf."
            ),
            group="Add-on configs",
            kind="files",
            intro=(
                "Two drop-in Klipper configs. The Nevermore file adapts Andrew "
                "Ellis's bed fan macros so the filter fans run slowly while the bed "
                "heats then faster once it reaches temperature. The LED file sets "
                "Stealthburner status colours on the logo and nozzle LEDs."
            ),
            files=(
                FileRef(
                    "printers/nevermore-config/nevermore.cfg",
                    "Nevermore fans from bed temperature",
                ),
                FileRef(
                    "printers/non-rainbow-barf-LED-config/SBLEDs.cfg",
                    "Stealthburner status LEDs",
                ),
            ),
        ),
    ),
)

CONFIGS = Section(
    key="configs",
    title="Config library",
    nav_title="Configs",
    blurb=(
        "Every Klipper, Moonraker and host config in the repository, readable in "
        "the browser with highlighting, copy and download."
    ),
    icon="file",
    unit="config files",
)

_SCHEM = "diagrams-schematics/"

SCHEMATICS = Section(
    key="schematics",
    title="Schematics",
    nav_title="Schematics",
    blurb=(
        "Board pinouts and reference diagrams for common Voron electronics, "
        "gathered in one place so you can stop hunting for them."
    ),
    icon="cpu",
    unit="diagrams",
    pages=(
        Page(
            slug="schematics/index",
            title="Pinouts and schematics",
            summary=(
                "BTT Octopus, Octopus Pro, SKR Mini, EBB36 and Fly toolhead boards, "
                "Raspberry Pi GPIO and more, full resolution on click."
            ),
            kind="gallery",
            figures=(
                Figure(f"{_SCHEM}BTT Octopus v1.0.png", "BTT Octopus v1.0 pinout", "Main boards"),
                Figure(f"{_SCHEM}BTT Octopus v1.1.png", "BTT Octopus v1.1 pinout", "Main boards"),
                Figure(
                    f"{_SCHEM}BIGTREETECH Octopus Pro V1.0-Pin.png",
                    "BTT Octopus Pro v1.0 pinout",
                    "Main boards",
                ),
                Figure(
                    f"{_SCHEM}BIGTREETECH Octopus Pro V1.1-Pin.jpg",
                    "BTT Octopus Pro v1.1 pinout",
                    "Main boards",
                ),
                Figure(f"{_SCHEM}BTT SKR MINI E3 V2.png", "BTT SKR Mini E3 V2 pinout", "Main boards"),
                Figure(f"{_SCHEM}Einsy RAMBo connectors.jpeg", "Einsy RAMBo connectors", "Main boards"),
                Figure(f"{_SCHEM}BTT-EBB36v1-2.jpg", "BTT EBB36 v1.2 pinout", "Toolhead boards"),
                Figure(f"{_SCHEM}EBB36_PowerConnector2.jpg", "EBB36 power connector", "Toolhead boards"),
                Figure(f"{_SCHEM}EBB-SB0000-CAN-pinout.png", "BTT EBB SB0000 CAN pinout", "Toolhead boards"),
                Figure(f"{_SCHEM}FlySHT36V2pin.jpg", "Mellow Fly-SHT36 V2 pinout", "Toolhead boards"),
                Figure(f"{_SCHEM}R-Pi-4-GPIO-Pinout.jpg", "Raspberry Pi 4 GPIO pinout", "Host and reference"),
                Figure(f"{_SCHEM}ShoreTPUScales.jpg", "Shore hardness scales for TPU", "Host and reference"),
            ),
            files=(
                FileRef(f"{_SCHEM}BTT E3 SKR MINI V3.0_PIN.pdf", "BTT SKR Mini E3 V3.0 pinout", "PDF"),
                FileRef(f"{_SCHEM}Trident_Assembly.f3d", "Voron Trident assembly", "Fusion 360 model"),
            ),
        ),
    ),
)

KIT = Section(
    key="kit",
    title="Recommendations",
    nav_title="Kit",
    blurb=(
        "Tools, electrical kit, workshop accessories and filament brands, sorted "
        "by what actually earned its place on the bench."
    ),
    icon="tool",
    unit="picks",
    groups=("Tools", "Materials"),
    pages=(
        Page(
            slug="kit/3d-printing-tools",
            title="3D printing tools",
            summary=(
                "From bowden cutters and calipers to Knipex pliers, Wera drivers "
                "and cordless Ryobi kit, grouped by essentials, lovely tools and "
                "good-value picks."
            ),
            group="Tools",
            kind="tools",
            source="recommendations/3d-printing-tools.md",
        ),
        Page(
            slug="kit/electrical-tools",
            title="Electrical and soldering tools",
            summary=(
                "Crimpers, strippers, soldering irons, power supplies, multimeters "
                "and the connectors worth keeping in stock."
            ),
            group="Tools",
            kind="tools",
            source="recommendations/electrical-tools.md",
        ),
        Page(
            slug="kit/tool-accessories",
            title="Workshop accessories",
            summary=(
                "Cable management, storage, tapes, sanding and the small things "
                "that keep a printing bench tidy."
            ),
            group="Tools",
            kind="tools",
            source="recommendations/tool-accessories.md",
        ),
        Page(
            slug="kit/filament",
            title="Filament experiences",
            summary=(
                "Brands that print beautifully, brands that are fine and the few "
                "that damaged beds, sorted by material."
            ),
            group="Materials",
            kind="filament",
            source="recommendations/filament-experiences.md",
        ),
    ),
)

BOOKMARKS = Section(
    key="bookmarks",
    title="Bookmarks",
    nav_title="Bookmarks",
    blurb=(
        "A curated bookmark collection for Voron and 3D printing, browsable and "
        "searchable here or importable into your own browser."
    ),
    icon="bookmark",
    unit="bookmarks",
    pages=(
        Page(
            slug="bookmarks/index",
            title="Bookmark explorer",
            summary=(
                "Years of curated Voron and 3D printing links in folders, filterable "
                "here and importable straight into Chrome or Firefox."
            ),
            kind="bookmarks",
            source="browser-bookmarks/README.md",
            files=(
                FileRef(
                    "browser-bookmarks/3DPrintingBookmarks.html",
                    "3DPrintingBookmarks.html",
                    "Import through your browser's bookmark manager.",
                ),
            ),
        ),
    ),
)

STLS = Section(
    key="stls",
    title="STL sources",
    nav_title="STLs",
    blurb="Where to find models worth printing, free and paid, plus collections for inspiration.",
    icon="layers",
    unit="sources",
    pages=(
        Page(
            slug="stls/index",
            title="STL sources and collections",
            summary=(
                "Free and paid model libraries worth knowing, plus curated "
                "collections on Printables, MakerWorld and Thingiverse."
            ),
            kind="stls",
            source="stls/stl-sources.md",
            extra_sources=("stls/my-collections.md",),
        ),
    ),
)

STICKERS = Section(
    key="stickers",
    title="Stickers",
    nav_title="Stickers",
    blurb="Sticker artwork for a well tuned machine.",
    icon="star",
    in_main_nav=False,
    pages=(
        Page(
            slug="stickers/index",
            title="Stickers",
            summary=(
                "Oliver Certified, Tuned By and friends: sticker artwork for a well "
                "tuned machine."
            ),
            kind="gallery",
            source="buy-stickers/README.md",
            figures=(
                Figure("buy-stickers/Oliver_Certified.png", "Oliver Certified"),
                Figure("buy-stickers/Tuned_By.png", "Tuned By"),
                Figure("buy-stickers/Oliver_TUNED.png", "Oliver Tuned"),
                Figure("buy-stickers/OLIVER_SPEC.png", "Oliver Spec"),
                Figure("buy-stickers/Oliver_Trust.png", "Oliver Trust"),
            ),
        ),
    ),
)

PROJECTS_SECTION = Section(
    key="projects",
    title="Related projects",
    nav_title="Projects",
    blurb=(
        "Two companion projects from the same hobby: a dashboard launcher and a "
        "Discord bot."
    ),
    icon="zap",
    in_main_nav=False,
    pages=(
        Page(
            slug="projects/index",
            title="Related projects",
            summary=(
                "3D-Printer-Launcher for Klipper temperature dashboards and "
                "PrinterShameBot for tormenting your friends' prints on Discord."
            ),
            kind="projects",
        ),
    ),
)

PROJECTS = (
    Project(
        name="3D-Printer-Launcher",
        tagline="One window for your Klipper temperature dashboards",
        body=(
            "A small Windows launcher that starts your Qidi and Voron temperature "
            "dashboards and a webcam restart helper from one window, with live "
            "logs and per-printer config. The dashboards drop straight into OBS "
            "Studio as Browser Source overlays."
        ),
        site="https://ernster.dev/3D-Printer-Launcher/",
        repo="https://github.com/oernster/3D-Printer-Launcher",
        icon="launcher-icon.png",
        image="https://ernster.dev/3D-Printer-Launcher/screenshot-launcher.png",
        image_alt="The 3D-Printer-Launcher window listing temperature dashboards",
    ),
    Project(
        name="PrinterShameBot",
        tagline="A snarky 3D printer Discord bot",
        body=(
            "A self-hosted Discord bot that answers with a 3D printing put-down, "
            "for politely tormenting your friends' prints. Invite it to your "
            "server then send the command in any channel it can read."
        ),
        site="https://ernster.dev/snark3Dprinter-discord-bot/",
        repo="https://github.com/oernster/snark3Dprinter-discord-bot",
        icon="bot-icon.png",
        image="https://ernster.dev/snark3Dprinter-discord-bot/og.png",
        image_alt="PrinterShameBot banner",
        extra="!printquote",
    ),
)

SECTIONS: tuple[Section, ...] = (
    GUIDES,
    FAQS,
    PRINTERS,
    CONFIGS,
    SCHEMATICS,
    KIT,
    BOOKMARKS,
    STLS,
    STICKERS,
    PROJECTS_SECTION,
)

# Home page ---------------------------------------------------------------------

HOME_TITLE = "3D-printing-info: Voron, Klipper and Bambu guides, configs and pinouts"
HOME_DESCRIPTION = (
    "An open 3D printing knowledge base: Voron and Klipper guides, Bambu and Voron "
    "FAQs, working printer configs, board pinouts, tool and filament picks, curated "
    "bookmarks and STL sources."
)
HOME_EYEBROW = "Voron · Klipper · Bambu"
HOME_HEADLINE = "The 3D printing notebook,"
HOME_HEADLINE_ACCENT = "kept public"
HOME_LEAD = (
    "More than eight years of guides, fixes, working configs, pinouts and hard-won "
    "recommendations from running Voron, Klipper and Bambu machines as well as "
    "Tronxy, Biqu, Prusa, Anycubic and Qidi printers, gathered from one repository "
    "into one searchable site."
)
HOME_POINTS = (
    "Configs from machines that really ran them",
    "Kit that was bought and used",
    "Free and open source under GPL-3.0",
)
HOME_PATHS_LEAD = "Pick the situation you are in and follow the trail."
HOME_TILES_LEAD = "Every folder of the repository, presented as a section you can browse."
HOME_FEATURED_BUILD = "printers/voron-trident-350"
HOME_WHY = (
    (
        "Voron and Klipper reward tinkering but the knowledge is scattered: a pinout "
        "on one forum, a drying temperature on another, the macro you need buried in "
        "a Discord thread from years ago."
    ),
    (
        "So this repository is a working notebook, kept public. The configs are the "
        "ones that ran on real machines; the recommendations are things actually "
        "bought and used; the guides are the write-ups worth finding the first time. "
        "If it saves you an evening of searching, it has done its job."
    ),
)
HOME_FAQ = (
    (
        "Who is this for?",
        (
            "Anyone running or building a Voron, a Klipper printer or a Bambu "
            "machine, from first setup through tuning and troubleshooting. Much of it "
            "is Voron-focused but the guides on drying, adhesion, slicers and clogs "
            "apply to any FDM printer."
        ),
    ),
    (
        "Are the printer configs safe to copy?",
        (
            "They are real configs shared as reference. Never flash another "
            "machine's config wholesale: treat them as a guide, match them to your "
            "own hardware and pins, then test carefully."
        ),
    ),
    (
        "How do I use the bookmarks?",
        (
            "Browse and filter them in the bookmark explorer. To take them with you, "
            "download the export and import it through your browser's bookmark "
            "manager."
        ),
    ),
    (
        "Is it free?",
        (
            "Yes. The repository and this site are free and open source under the "
            "GNU GPL-3.0 licence. A coffee donation is welcome but entirely optional."
        ),
    ),
    (
        "Can I suggest additions?",
        (
            "It is a personal knowledge base, so it reflects its author's own "
            "printers and experience. Open an issue on the repository if something "
            "is out of date or you know a resource worth adding."
        ),
    ),
)
HOME_SUPPORT_TITLE = "Found something useful?"
HOME_SUPPORT_TEXT = (
    "The notebook is free and always will be. If it saved you an evening, a coffee "
    "helps keep it maintained."
)
START_PATHS = (
    StartPath(
        "Building or tuning a Voron",
        "Belts, input shaping, levelling and the macros that start every print.",
        (
            "guides/shake-n-tune",
            "printers/voron-trident-350",
            "faqs/trident-levelling-probe",
            "printers/voron-2-4-leviathan",
        ),
    ),
    StartPath(
        "A print just failed",
        "Clogs, layer shifts, poor adhesion and wet filament, roughly in the order worth checking.",
        (
            "guides/stealthburner-clogs",
            "faqs/layer-shift-causes",
            "guides/bed-adhesion",
            "guides/drying-filament",
        ),
    ),
    StartPath(
        "Bambu AMS trouble",
        "Feeding failures, a slot flashing red and a stuck cutter.",
        ("faqs/ams-feeding-failures", "faqs/ams-cleaning", "faqs/cutter-stuck"),
    ),
    StartPath(
        "Getting Klipper running",
        "From a blank SD card to a printer that answers in Mainsail.",
        (
            "guides/klipper-setup",
            "guides/sovol-sv06-klipper",
            "guides/tronxy-x5sa-klipper",
            "guides/linux-commands",
        ),
    ),
)

# Build rules -------------------------------------------------------------------

# Repository paths that are deliberately not pages of their own.
NOT_CONTENT = ("README.md", "LICENSE", ".gitignore")
NOT_CONTENT_PREFIXES = ("docs/",)

# Links inside the guides that point at a path which has since moved.
LINK_ALIASES = {
    "guides/setup-sounds-klipper.md": "guides/setup-sounds-wavs-klipper.md",
}

# File types the config viewer can show as text.
VIEWABLE_SUFFIXES = (".cfg", ".conf", ".txt", ".py")
VIEWABLE_NAMES = ("mainsail",)
