# 3D-printing-info

**An open, curated knowledge base for Voron, Klipper and Bambu 3D printers, created and maintained by [Oliver Ernster](https://github.com/oernster) over more than eight years.**

[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](LICENSE)
[![Focus: Voron · Klipper · Bambu](https://img.shields.io/badge/Focus-Voron%20%C2%B7%20Klipper%20%C2%B7%20Bambu-38bdf8.svg)](#what-is-inside)
[![Maintained: 8+ years](https://img.shields.io/badge/Maintained-8%2B%20years-brightgreen.svg)](#)
[![Live site](https://img.shields.io/badge/Live-oernster.github.io-5aa2ff.svg)](https://oernster.github.io/3D-printing-info/)

<img width="1767" height="989" alt="3D-printing-info: a sculpted head contemplating a workbench of 3D printers, filament spools, tools and printed parts on a blue schematic backdrop" src="https://github.com/user-attachments/assets/ca95d5ac-e456-43af-9cec-20937c5ac8d2" />

FAQs, Klipper guides, working printer configs, board pinout schematics, hard-won tool and filament recommendations, curated bookmarks and STL links, all in one place. Most of this was learned the hard way, one layer shift, clog and failed first layer at a time.

There is a browsable web version of this repository at **[oernster.github.io/3D-printing-info](https://oernster.github.io/3D-printing-info/)**.

---

## Why it exists

Voron and Klipper reward tinkering, but the knowledge is scattered: a pinout on one forum, a drying temperature on another, the macro you need buried in a Discord thread from two years ago.

So this repo is my working notebook, kept public. The configs are the ones running on my own machines; the recommendations are things I actually bought and used; the guides are the write-ups I wish I had found the first time. If it saves you an evening of searching, it has done its job.

## Who it is for

Anyone running or building a Voron, a Klipper-based printer or a Bambu machine, from first setup through tuning and troubleshooting. Much of it is Voron-focused but the guides on drying, adhesion, slicers and clogs apply to any FDM printer.

---

## Support this work

If you find this repository of use and would like to offer a tip for creating and maintaining it, please feel free to buy me a coffee via PayPal. It is entirely optional and supports the ongoing maintenance of this repo and general help.

### [Friendly coffee donation here](https://www.paypal.com/donate/?hosted_button_id=R3DFLDWT2PFC4)

---

## What is inside

Eleven sections, each a folder in the repo. Click any section to open it.

| Section | What is inside |
| --- | --- |
| [**guides**](guides) | The largest section: PID tuning, Shake n Tune, filament drying, bed adhesion, levelling, painting, resolving Stealthburner clogs, temp towers, slicer choices, colour swaps and Klipper setup. |
| [**printers**](printers) | Real, working configs for my Vorons past and present: Trident 350 and Voron 0.2, plus a Qidi Q1 Pro, Nevermore, sensorless and LED configs and a summary of every upgrade on the Trident. |
| [**FAQs**](FAQs) | Bambu and Voron frequently asked questions: AMS feeding failures and cleaning, stuck cutters, layer-shift causes, sensorless steppers, motor wiring and levelling with or without a probe. |
| [**diagrams-schematics**](diagrams-schematics) | Common Voron board pinouts in one place: BTT Octopus and Octopus Pro, SKR Mini E3, EBB36 and SB CAN toolheads, Raspberry Pi 4 GPIO and a Trident assembly model, to save you scouring the internet. |
| [**recommendations**](recommendations) | A curated list of 3D-printing tools, electrical tools and tool accessories, plus my personal filament experiences across brands and materials. |
| [**browser-bookmarks**](browser-bookmarks) | Over six years of curated Voron and 3D-printing bookmarks, exported and importable straight into your favourite browser. |
| [**stls**](stls) | Personal STL collections curated from around the web, alongside links to many additional STL resources worth knowing. |
| [**voron-startup**](voron-startup) | PRINT_START style startup configs for the Voron 2.4 and Voron Trident, ready to adapt into your own printer setup. |
| [**handy-linux-cmds**](handy-linux-cmds) | The Debian and Raspbian commands every Klipper host needs but nobody remembers, kept in one cheatsheet. |
| [**moonraker**](moonraker) | A handy reference for calling a Klipper g-code macro through the Moonraker API. |
| [**buy-stickers**](buy-stickers) | A few fun "Oliver Certified" and "Tuned By" sticker artworks to print or stick on your machine. |

---

## Related projects

Two companion pieces that grew out of the same hobby.

- **[3D-Printer-Launcher](https://github.com/oernster/3D-Printer-Launcher)** ([site](https://oernster.github.io/3D-Printer-Launcher/)): a lovely UI for temperature displays, one window that launches Klipper temperature dashboards you can drop into OBS Studio as overlays. A guide to setting up OBS Studio with it lives in that repo.
- **[PrinterShameBot](https://github.com/oernster/snark3Dprinter-discord-bot)** ([site](https://oernster.github.io/snark3Dprinter-discord-bot/)): a Discord bot to politely torment your friends' 3D prints.

### Invite PrinterShameBot

Got a Discord server and want to politely torment your friends' 3D prints?

**[Click here to invite PrinterShameBot to your Discord](https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=PERMISSIONS_INTEGER&scope=bot%20applications.commands)**

Once invited, in any channel the bot has permission to read and send messages:

- Just send the command: `!printquote`
- The [PrinterShameBot code can be found here](https://github.com/oernster/snark3Dprinter-discord-bot).

---

## License

Free and open source under the GNU [GPL-3.0](LICENSE) licence.

---

Created and maintained by [Oliver Ernster](https://github.com/oernster). 8+ years and counting.

Thanks, and enjoy.
