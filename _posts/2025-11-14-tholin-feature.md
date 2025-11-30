---
layout: posts/post-boxed
title: "We Have Some Amazing Projects This Run: Tholin & Avalon Semiconductors"
date: 2025-11-14 12:00:00 +0000
categories: [news]
tags: [crowdsupply, gf180mcu, campaign]
author: "Tim 'mithro' Ansell"
badge_color: "bg-info"
slider_post: false
trending: false
sidebar: true
permalink: "/news/tholin-feature"
crowdsupply_url: "https://www.crowdsupply.com/wafer-space/gf180mcu-run-1/updates/tholin-feature"
---

Our first shuttle run includes a number of incredible projects, and we wanted to take a moment to highlight one of them.

---

## Tholin & Avalon Semiconductors

![Tholin's custom silicon designs showcase what's possible with open tooling]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tholin-feature/ic1.png)

*Tholin's custom silicon designs showcase what's possible with open tooling*

[Tholin](https://tholin.dev/) — the hardware designer behind [**Avalon Semiconductors**](https://github.com/AvalonSemiconductors) — has been exploring what's possible when open tooling meets personal silicon. Their journey, chronicled through detailed blog posts like [*Custom Silicon*](https://tholin.dev/custom_silicon/) and [*Custom Silicon Two: Electric Boogaloo*](https://tholin.dev/custom_silicon_two_electric_boogaloo/), shows how a single engineer can go from HDL to packaged chips using open-source flows, patience, and a healthy dose of curiosity.

---

### AS2650 and AS2650-2

![The AS2650(-2) is inspired by retro CPUs like the Signetics 2650]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tholin-feature/as2650.png)

*The AS2650(-2) is inspired by retro CPUs like the Signetics 2650*

Tholin's flagship projects are the **AS2650** and **AS2650-2**, re-implementations and extensions of the historic [Signetics 2650](https://en.wikipedia.org/wiki/Signetics_2650) microprocessor, recreated from the ground up using open EDA tools.
You can explore the repositories here:

* [AS2650 GitHub Repository](https://github.com/AvalonSemiconductors/AS2650)
* [AS2650 Documentation](https://avalonsemiconductors.github.io/AS2650/)

These chips aren’t just nostalgic exercises — they’re fully functional processors that have been designed, simulated, taped-out, and brought back to life with custom test boards and firmware. The AS2650-2 introduces expanded peripherals, enhanced bus control, and improved debug accessibility. All implemented with a custom cell library for GF180MCU.

---

### Porting the AS2650v2 to wafer.space

**Tholin** is currently porting the **AS2650v2** to the [**wafer.space**](https://wafer.space) template.
This serves as a **reference design**, demonstrating a complete CPU implementation, a multi-macro layout, and new methodologies for **instantiating SRAMs** within the wafer.space framework.

The project also makes use of **high-performance dynamic D-type flip-flop circuits (DFFs)** from the
[**gf180mcu_as_ex_mcu7t5v0**](https://github.com/AvalonSemiconductors/gf180mcu_as_ex_mcu7t5v0) library.

Tholin notes that the wafer.space padframe provides **more pads than the Efabless Caravel design**, resulting in a number of unused pins during this initial port. She suggests that future revisions may take advantage of these additional pads to support **expanded peripherals** and system features.

You can explore the design and accompanying documentation on GitHub:
👉 [**AvalonSemiconductors/as2650-ws**](https://github.com/AvalonSemiconductors/as2650-ws)

---

### wafer.space Submissions

Tholin has also created a companion repository,
[**ws-submission-2025**](https://github.com/AvalonSemiconductors/ws-submission-2025), documenting her submission for the current wafer.space fabrication run.

True to her style, the project includes **artwork integrated directly into the silicon layout**, reflecting the creative potential unlocked when advanced design tools are accessible and open.

![Tholin's logo, adapted for silicon artwork]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tholin-feature/logo_bw.png)

*Tholin's logo, adapted for silicon artwork*

Additionally, Tholin developed a [**Python script**](https://github.com/AvalonSemiconductors/ws-submission-2025/blob/main/padout_gen.py) that **automatically generates padout diagrams** from a [LibreLane](https://librelane.rtfd.io/) configuration file thereby simplifying visualization and documentation of pad assignments.

![Padout diagram generated from Python and LibreLane configuration]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tholin-feature/padout.png)

*Padout diagram generated from Python and LibreLane configuration*


---

### Multi-Project Die Exploration

<table>
  <tr>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tholin-feature/multidie.png" alt="" /></td>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tholin-feature/multilayout.png" alt="" /></td>
  </tr>
  <tr>
    <td colspan="2"><em>Multi-project die strategy - integrating multiple designs onto a single die to maximize wafer utilization</em></td>
  </tr>
</table>

Tholin is also pioneering **multi-project die (MPD)** strategies, maximizing wafer area by integrating multiple small designs onto a single die.
Projects such as [`gfmpw-1-multi`](https://github.com/AvalonSemiconductors/gfmpw1-multi) and [`AS2650-bring-up`](https://github.com/AvalonSemiconductors/AS2650-bring-up) demonstrate how careful planning and padframe reuse make it possible to test multiple subsystems in one run.

Tholin has also written thorough documentation on this project [here](https://avalonsemiconductors.github.io/GFMPW-1-MULTI/index.html)

This approach reflects the open ethos of wafer.space — making silicon exploration more accessible, modular, and repeatable for small teams and individuals.

---

### Open Flow & LibreLane Experience

Tholin has been an early adopter of [**LibreLane**](https://librelane.rtfd.io/), the open-source ASIC flow used by wafer.space. Their feedback and experiments with padframes, padrings, and packaging have helped refine the ecosystem for everyone.
From RTL through layout and DRC, to bonding and board testing, Tholin's work demonstrates that open tooling can now carry a chip from idea to reality — no closed vendor stack required.

![Standard cells are a key component of RTL to GDSII flows.]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tholin-feature/3d_view.png)

*Standard cells are a key component of RTL to GDSII flows.*

---

### Other Avalon Semiconductors Projects

Tholin has also created a number of fun and technically rich designs through **Tiny Tapeout**, showcasing creativity across digital design, display drivers, and compact CPUs:

| Name                     | Description                                                                          | GitHub Link                                                                                                     |
| ------------------------ | ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| **AS5401**               | 4-bit CPU                                                                            | [AvalonSemiconductors/tt2-AvalonSemi-5401](https://github.com/AvalonSemiconductors/tt2-AvalonSemi-5401)         |
| **TT02 Logisim Example** | Example and documentation on submitting Tiny Tapeout designs using Logisim Evolution | [AvalonSemiconductors/tt02-logisim-example](https://github.com/AvalonSemiconductors/tt02-logisim-example)       |
| **Diceroll**             | Animates a random number rolling on a 7-segment display                              | [AvalonSemiconductors/tt2-diceroll](https://github.com/AvalonSemiconductors/tt2-diceroll)                       |
| **TBB143**               | Programmable sound generator using a ring oscillator as a faster internal clock      | [AvalonSemiconductors/tt2-avalonsemi-TBB1143](https://github.com/AvalonSemiconductors/tt2-avalonsemi-TBB1143)   |
| **Multiplexed Counter**  | Drives 4 multiplexed 7-segment displays to count time up to 99 min 59 sec            | [AvalonSemiconductors/tt2-multiplexed-counter](https://github.com/AvalonSemiconductors/tt2-multiplexed-counter) |
| **4-bit Multiplier**     | Multiplies two 4-bit numbers into an 8-bit result                                    | [AvalonSemiconductors/tt2-4x4-multiply](https://github.com/AvalonSemiconductors/tt2-4x4-multiply)               |
| **LCD Namebadge**        | Experiment with character LCD interfacing                                            | [AvalonSemiconductors/tt2-lcd-namebadge](https://github.com/AvalonSemiconductors/tt2-lcd-namebadge)             |

Each of these designs exemplifies the open-hardware spirit: compact, educational, and fully reproducible — proof that anyone can design real silicon with today's open tools.

---

### Beyond Silicon

Beyond her silicon designs, **Tholin** has also developed a range of PCB projects and breakout boards that make working with custom dies more accessible.

<table>
  <tr>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tholin-feature/dip40.png" alt="" /></td>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tholin-feature/dip40_wirebond.png" alt="" /></td>
  </tr>
  <tr>
    <td colspan="2"><em>DIP40 breakout board and wirebonding setup - making custom silicon accessible through standard packages</em></td>
  </tr>
</table>

Tholin has also contributed extensively to the **wafer.space standard padframe**, helping shape the mechanical and electrical layout used across multiple projects.

---

### Why We’re Excited to Have Tholin Aboard

Tholin represents the kind of creative, self-driven engineering that wafer.space exists to empower. Her work with the AS2650 family, open flows, and multi-project dies captures the spirit of the growing open-silicon movement — one where innovation comes from curiosity, not corporate budgets.

We're thrilled to have **Tholin & Avalon Semiconductors** among the first wave of wafer.space participants and can't wait to see what they build next.

---

*This update was originally published on [Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-1/updates/tholin-feature).*
