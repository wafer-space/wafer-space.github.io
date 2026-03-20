---
layout: posts/post-boxed
title: "GF180MCU Run 2 is Coming!"
date: 2026-03-01 12:00:00 +0000
categories: [news]
tags: [gf180mcu, run2, crowd-supply]
author: "Tim 'mithro' Ansell"
post_image: "/assets/images/news/gf180mcu-gelpack-dice.jpg"
badge_color: "bg-purple"
slider_post: false
trending: false
sidebar: true
permalink: "/news/run2-coming-soon"
---

Hey folks,

If you are reading this, you have just subscribed to the [wafer.space GF180MCU Run 2 campaign](https://www.crowdsupply.com/wafer-space/gf180mcu-run-2). Welcome! Whether you followed Run 1 or this is your first time hearing about wafer.space, we are glad you are here.

## What is wafer.space?

[wafer.space](https://wafer.space/) is pooled silicon fabrication. Think [OSH Park](https://oshpark.com), but for custom chips instead of PCBs. You design a chip using GlobalFoundries' open [GF180MCU](https://gf180mcu-pdk.readthedocs.io/) PDK, submit your layout, and we handle fabrication, dicing, and delivery. $7 per chip, 1,000 chips per slot.

The tools are open source. The PDK is open source. Your design can be open or closed. No NDAs required to get started.

## Run 1: Designs on Silicon

Run 1 closed in late November 2025 and the wafers are currently in production at GlobalFoundries. We filled the reticle with **many designs** from individuals, universities, startups, and community groups. 29 of those designs are public and available for you to study at [github.com/wafer-space/ws-run1](https://github.com/wafer-space/ws-run1).

Some highlights from the run:

- **KianV**: A 32-bit RISC-V SoC (RV32IMA with SV32 MMU) capable of running mainline Linux, built entirely with open-source tools.
- **FABulous**: An open-source FPGA fabric with 480 LUT4s, programmable via Yosys and nextpnr. Yes, an FPGA implemented as an ASIC on an open PDK.
- **Z80 Open Silicon**: A pin-compatible, open-source reimplementation of the classic Zilog Z80, targeting drop-in compatibility with vintage 8-bit computers.
- **Tiny Tapeout GF**: The Tiny Tapeout multi-project chip ported to GF180MCU, with dozens of community designs packed onto a single die.
- **ISHI-KAI**: 14 novice designers from the Japanese ISHI-KAI community submitted their first silicon designs together, creating analog circuits from inverters to PLLs.

The range of projects was incredible: from production-ready SoCs to first-time tapeouts, from retro computing to cutting-edge research. That is exactly what accessible fabrication enables.

## What is New in Run 2

Run 2 builds on everything we learned from Run 1, with some significant improvements:

- **Multiple slot sizes**: We are introducing quarter, half, and full slot options. Not every design needs 20 mm2. Smaller slots mean a lower cost of entry for simpler designs, while full slots remain available for larger projects.
- **Improved DRC and submission platform**: The [platform.wafer.space](https://platform.wafer.space/) submission system has been refined based on Run 1 experience. Faster checks, clearer error messages, smoother workflow.
- **Better tooling**: LibreLane, the project template, and the precheck tools all continue to improve. Every run makes the process smoother for the next one.
- **Early-bird pricing**: Early supporters will be able to lock in discounted pricing. Stay subscribed for details.

Things get better with every run. That is the whole point of building sustainable infrastructure.

## Timeline

The current target is a **2 July 2026 GDS submission deadline**, with the campaign closing on 30 June 2026. The campaign will go live well before that, giving you plenty of time to design, verify, and submit. Bare dies are expected to ship by mid-October 2026.

Pricing details are coming soon. Subscribe to this campaign to be notified the moment we have them.

## Get Involved Now

You do not need to wait for the campaign to launch to start designing. The tools and PDK are available today:

- **Start designing**: Clone the [gf180mcu-project-template](https://github.com/wafer-space/gf180mcu-project-template) and start experimenting. It includes a complete Nix environment with all the tools you need.
- **Join the community**: The [wafer.space Discord](https://discord.gg/43y2t53jpE) is where designers help each other with pad rings, DRC issues, floorplanning, and everything in between. It is also the fastest way to get answers from the wafer.space team.
- **Study Run 1 designs**: Browse the [29 public designs from Run 1](https://github.com/wafer-space/ws-run1) to see what fits in the die area and how others approached their layouts.

The earlier you start, the more time you have to iterate. The best designs from Run 1 were the ones that started early and took advantage of community feedback.

More updates coming soon with pricing details, slot sizes, and timeline specifics. Stay tuned.

-Tim 'mithro' Ansell
