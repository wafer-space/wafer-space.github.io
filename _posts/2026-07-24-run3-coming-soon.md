---
layout: posts/post-boxed
title: "GF180MCU Run 3 is Coming!"
date: 2026-07-24 12:00:00 +0000
excerpt: "GF180MCU Run 3 is coming! Featuring a new slot size and $2/die prices."
categories: [news]
tags: [gf180mcu, run3, crowd-supply]
author: "Tim 'mithro' Ansell"
post_image: "/assets/images/news/gf180mcu-gelpack-dice.jpg"
badge_color: "bg-purple"
slider_post: false
trending: false
sidebar: true
permalink: "/news/run3-coming-soon"
---

Hey folks,

We're pleased to announce Run 3 is coming very soon! Following on the successes of Run 1 and Run 2, we've continued
to iterate and improve all aspects of the flow to help you bring your idea to life with cheaper and easier-to-manufacture
chips.

## What is wafer.space?

[wafer.space](https://wafer.space/) is pooled silicon fabrication. Think [OSH Park](https://oshpark.com), but for custom
chips instead of PCBs. You design a chip using GlobalFoundries' open [GF180MCU](https://gf180mcu-pdk.readthedocs.io/)
PDK, submit your layout, and we handle fabrication, dicing, and delivery. $7 per chip, 1,000 chips per slot.

The tools are open source. The PDK is open source. Your design can be open or closed. No NDAs required to get started.

## Run 1 and Run 2

Run 1 has been packaged and shipped to all of our customers -- from hobbyists to academics, and from industry specialists
to community groups, people have been able to get their hands on their very own custom silicon. Many are testing their
designs right now, and our chip-on-board packaging solution has been popular and successful! Read more about it in
our dedicated [chip-on-board progress update](/news/chip-on-board-progress).

Run 2 has now been closed and will begin manufacturing shortly. It features several interesting projects such as:

- **[FABulous FPGA](https://github.com/mole99/wsrun2-fabulous-fpga)**: Back for Run 2, now with four times as much SRAM
and much faster thanks to a community created standard cell library.

- **[SRAM Macro](https://github.com/RTimothyEdwards/gf180mcu_ocd_sram_test)**: A selection of SRAMs for design
validation, removing the hurdle of designing your own.

- **[MPW by Avalon Semiconductors](https://github.com/AvalonSemiconductors/ws-submission-2026/)**: Multi-project die
containing various designs such as a replica 6502, a DRAM controller, NTSC test signal generator and more.

- **[EuroSynth](https://github.com/anfroholic/eurosynth)**: A fully digital eurorack kitchen-sink synthesizer,
containing a bank of isolated sound engines. Capable of streaming to an external DAC.

- **[SlugTPU](https://github.com/SlugTPU/gf180mcu-slugtpu)**: An open-source tensor processing unit designed to
accelerate quantized neural network inference. It features an 8x8 matrix multiply unit, a scalar post processing
pipeline, 2 KiB SRAM data cache and a 256 byte instruction cache.

- **[µTheia](https://github.com/dhgaddy/microTheia)**: An event-based machine vision ASIC for motion pattern
classification. Uses EVT2 event streams, which are then decoded, compressed, sorted and computed. Detections can be
reported through SPI or physical pins.

## What's New in Run 3

Run 3 introduces several improvements based on what we learned from shipping Run 1 & 2.

- **Quarter-sized slot**: We're adding another size option for Run 3. This tiny slot packs a punch with 4.9 mm² of
silicon starting from just $2,000! Tapeout test structures, analog circuits, or compact digital designs without paying
for silicon you do not need.

- **Further improvements to the toolchain**: The submission platform has once again been updated to catch more issues,
earlier, and faster. Bugfixes and stricter DRC mean you can be confident in your tapeout.

- **More examples**: Run 1 contains 29 public designs, and Run 2 adds many more. These are real tapeouts which you can 
se to study and build upon. Projects vary from simple test structures to Linux-capable SoCs, covering digital, analog,
and mixed-signal approaches.

## Schedule

| Date | Milestone |
|------|-----------|
| 1 August 2026 | Campaign opens on Crowd Supply. |
| 15 December 2026 | Slot purchase deadline. |
| 29 December 2026 | Deadline to submit GDS files. |
| Q2 2027 | Bare dies and packaged parts shipped to customers. |

<br>

## Get Involved Now

You do not need to wait for the campaign to launch to start designing. The tools and PDK are available today:

- **Start designing**: Clone the [gf180mcu-project-template](https://github.com/wafer-space/gf180mcu-project-template)
and start experimenting. It includes a complete Nix environment with all the tools you need.
- **Join the community**: The [wafer.space Discord](https://wafer.space/discord) is where designers help each other with
pad rings, DRC issues, floorplanning, and everything in between. It is also the fastest way to get answers from the
wafer.space team.
- **Study previous designs**: Browse the [29 public designs from Run 1](https://github.com/wafer-space/ws-run1) to see what
fits in the die area and how others approached their layouts. *(The Run 2 repository is still being finalised -- we'll
let you know when it's ready.)*

The earlier you start, the more time you have to iterate. The best designs were the ones that started early and took
advantage of community feedback.