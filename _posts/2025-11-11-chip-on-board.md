---
layout: posts/post-boxed
title: "Community Progress on Chip-on-Board Packaging Strategy"
date: 2025-11-11 12:00:00 +0000
categories: [news]
tags: [crowdsupply, gf180mcu, campaign]
author: "Tim 'mithro' Ansell"
badge_color: "bg-info"
slider_post: false
trending: false
sidebar: true
permalink: "/news/chip-on-board"
post_image: "/assets/images/news/gf180mcu-run-1/chip-on-board/padframes-cob-tt-cob.jpg"
crowdsupply_url: "https://www.crowdsupply.com/wafer-space/gf180mcu-run-1/updates/chip-on-board"
---

## Community Progress on Chip-on-Board Packaging Strategy

Today we have a guest post from **[Andrew Wingate](https://www.crowdsupply.com/evezor-inc)** (of Evezor Inc), sharing his perspective on the progress the [wafer.space](https://wafer.space/) community has been making in developing a chip-on-board packaging strategy. This work includes contributions from **[Tiny Tapeout](https://tinytapeout.com/)**, **[MosBius](https://mosbius.org/)** ([Columbia University](https://peterkinget.github.io/)), and community members like **[@Tholin](https://github.com/AvalonSemiconductors)** and **@xianglin_pu**.

---

[**wafer.space**](https://wafer.space/) exists to make custom silicon affordable. At **$7 per chip** for production quantities, the cost barrier to fabrication has been removed, but that's only part of the story. Working with bare dies is challenging and typically requires specialized, expensive equipment.

To make post-fabrication development more accessible, the community has been working on **COB (Chip on Board)** standard templates. Over the past months, various package options have been explored, including **DIP, LGA, castellated breakouts,** and **breadboardable** versions.

The leading contender is currently a **mezzanine breakout board** using connectors similar to those found on the Raspberry Pi Compute Modules. This design allows wirebonding houses to mount and wirebond your dies directly onto the COB packages, which can then be shipped to you ready for integration into your own systems.

When designing your motherboards, you'll be able to source compatible connectors like [this one](https://www.lcsc.com/product-detail/C19089262.html) and have your PCBA house assemble them. The community is also working on a range of breakout boards that follow a **community-developed standard digital padring**, to make development faster and more consistent.

> **What This Means For You:** If you're backing this campaign or considering it, you won't need specialized equipment or expensive packaging services to use your chips. While the community continues developing these COB standards, [wafer.space is offering wire-bonded COB packaging at buy.wafer.space](https://buy.wafer.space) for this campaign run (1,000 dies mounted and wire-bonded to PCBs). Alternatively, you can work with your own wirebonding partner using these community-developed designs. Either way, you'll solder the connector to your custom PCB and plug them in just like adding any other component to your board.

---

### The Community-Developed Standard Padframe and COB Design

While you're free to use any pad configuration you wish, adhering to the **community-developed standard** ensures compatibility with wirebonding partners and simplifies the fabrication process.

**Key Details:**

* **74-pad padframe** on your die

* **20 pads** on the east and west sides

* **17 pads** on the north and south sides

* **74-pad wirebonding footprint**

* **14 mm × 16 mm PCB**

* **70-pin mezzanine connector:** [C19089236](https://www.lcsc.com/product-detail/C19089236.html) *or compatible*

* **1 µF decoupling capacitors** on VDD_IO, VDD_CORE, and PWR_AUX pins

Find most current designs on the [chip-on-board-wire-bonded-pcbs repo](https://github.com/wafer-space/chip-on-board-wire-bonded-pcbs)

## Why Standardize?

With the technical details established, it's worth stepping back to consider why standardization matters for the open silicon ecosystem.

### A Standard for the Broader Community

While this standard emerged from the wafer.space community's needs, the goal is to create something that could benefit the broader open silicon ecosystem. By documenting the design openly and making the [KiCad](https://www.kicad.org/) symbols, PCB layouts, and specifications freely available, other projects and communities could adopt or adapt this approach for their own chip-on-board needs.

The work you see here comes from contributors across the community: Discord members testing designs and providing feedback, Tiny Tapeout contributors sharing lessons from their COB runs, Columbia University students developing educational chips through the MosBius project, and veteran engineers refining the wirebonding footprints. Each brought different expertise: some from PCB design, others from silicon layout, still others from manufacturing and assembly experience.

The hope is that as more projects use compatible footprints and connectors, the ecosystem benefits grow:
- Wirebonding houses can optimize their processes for a common standard
- More off-the-shelf breakout boards and adapters become available
- Designers can share compatible motherboard designs across projects
- The barrier to entry for COB assembly continues to decrease

This isn't about mandating a single approach. Diversity in packaging solutions remains valuable. Rather, it's about establishing a well-documented baseline that communities can rally around when standardization helps everyone. If this standard proves useful beyond wafer.space, that would represent exactly the kind of collaborative progress that makes open silicon compelling.

This design hopefully meets the needs of a majority of projects on wafer.space. If your project needs something different, other open source packaging options are available to explore, such as the University of Washington's **[BaseJump project](https://bjump.org/)**, which offers **[BGA packaging standards](https://github.com/bespoke-silicon-group/bsg_packaging)** including their 352-pin BaseJump Socket for designs requiring hundreds of I/O pins or more complex integration.

## The Implementation: From Concept to Physical Boards

So what does this standard look like in practice? Let's walk through the actual hardware, tools, and resources the community has developed.

### 70-Pin Mezzanine COB

The centerpiece of the standard is a 70-pin mezzanine COB board that connects your wirebonded die to a standard connector.

<table>
  <tr>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/chip-on-board/padframes-cob-mezzanine-front.png" alt="" /></td>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/chip-on-board/padframes-cob-mezzanine-back.png" alt="" /></td>
  </tr>
  <tr>
    <td colspan="2"><em>70-pin mezzanine COB front and back views</em></td>
  </tr>
</table>


Panelized for efficient handling and assembly by wirebonding partners:

<table>
  <tr>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/chip-on-board/padframes-cob-mezzanine-panel-front.png" alt="" /></td>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/chip-on-board/padframes-cob-mezzanine-panel-rear.png" alt="" /></td>
  </tr>
  <tr>
    <td colspan="2"><em>Mezzanine panel front and rear for efficient wirebonding assembly</em></td>
  </tr>
</table>

The standard configuration can be found in the [GitHub repository](https://github.com/wafer-space/gf180mcu-project-template/blob/main/librelane/config.yaml). For easier viewing, it's also available as a [Google Sheet](https://docs.google.com/spreadsheets/d/1pI2BAEWEexXcXN3vah3SR85zPIV6eAXPGXc2bcvoSGU/edit?gid=0#gid=0) that shows the complete pad mapping.

![Die padring layout with 74-pad configuration]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/chip-on-board/padframes-cob-die-padring.png)

*Die padring layout with 74-pad configuration*

To help visualize your own pad layouts, Discord user **@Tholin** has developed a Python-based pad viewer that generates an image of the pad layout defined in your template. This is useful for verifying your configuration matches your design intent. You can find the tool [here](https://github.com/AvalonSemiconductors/ws-submission-2025/blob/main/padout_gen.py).

---

## Design Tools and Ecosystem

Having the physical COB boards is only part of the picture. To actually use them, designers need schematic symbols, footprints, and integration tools. Here's what the community has built to support the full design workflow.

### Default KiCad Symbols

The community has developed several **[KiCad](https://www.kicad.org/) symbols** to support design and integration with COB layouts.

The **pad mapping symbol** corresponds to the default 74-pad wirebonding padframe and [default configuration](https://github.com/wafer-space/gf180mcu-project-template/blob/main/librelane/config.yaml) from the [**GF180MCU Project Template**](https://github.com/wafer-space/gf180mcu-project-template).

> Some users have suggested reducing the number of ground and power pads. If there is sufficient demand, an alternate default configuration will be created.
> Join the discussion on our [**Discord server**](https://discord.gg/43y2t53jpE).

![Default 74-pad wirebonding padframe symbol]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/chip-on-board/padframes-cob-default-74pad-wirebond-symbol.png)

*Default 74-pad wirebonding padframe symbol*

---

### 70-Pin Mezzanine Connector Symbol

The **mezzanine connector symbol** provides a 1:1 pin mapping to the 70-pin default layout.
All pins are aliased to match [Tiny Tapeout](https://tinytapeout.com/) naming conventions, useful for those familiar with the TT ecosystem who are designing custom chips for this wafer.space run.

!["Default 70-pin mezzanine COB breakout symbol"]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/chip-on-board/padframes-cob-default-70pin-mezzanine-symbol.png)

*"Default 70-pin mezzanine COB breakout symbol"*

An alternate version is also available that organizes pins by signal type. This version is particularly useful for Tiny Tapeout-style breakout motherboard designs where grouping by function makes routing clearer.

!["70-pin mezzanine COB symbol organized by signal type (Tiny Tapeout version)"]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/chip-on-board/padframes-cob-tinytapeout-kicad-symbols.png)

*"70-pin mezzanine COB symbol organized by signal type (Tiny Tapeout version)"*

### KiCad Resources for COB Design

While the initial symbols are in KiCad, the community welcomes contributions of symbols and libraries for other PCB design tools. If you use Altium, Eagle, or another tool, please submit a pull request to the [chip-on-board-wire-bonded-pcbs repo](https://github.com/wafer-space/chip-on-board-wire-bonded-pcbs)!

For those new to KiCad or looking to deepen their PCB design skills, **Pat Deegan** (developer of the **[Tiny Tapeout demo board](https://github.com/TinyTapeout/tt-demo-pcb)**) offers **[KiCad:Unlocked](https://inductive-kickback.com/2025/07/kicadunlocked-a-course-for-deep-kicad/)**, a comprehensive free course that covers everything from basic circuit design to advanced PCB layout techniques. The community hopes to work with Pat in the future on a tutorial specifically focused on wire bonding integration and designing motherboards for wafer.space COB packages.

If you want to quickly review KiCad designs without installing software, **[KiCanvas](https://kicanvas.org/)** provides a browser-based viewer for KiCad files. You can use it to inspect the standard COB layouts, verify connector pinouts, and review community-contributed designs, all directly in your browser.

---

### Beyond the Standard: Expanding Options

While the 70-pin mezzanine connector serves as the standard, the community recognizes that different projects have different needs.

#### Castellated and Breadboardable Breakouts

The community is developing a series of breakout boards designed to make it easier to prototype, experiment, and integrate your dies into existing systems.

![Castellated and breadboardable breakout board designs]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/chip-on-board/padframes-cob-breakouts.png)

*Castellated and breadboardable breakout board designs*

---

## Real-World Adoption

The real test of any standard is whether people actually use it. Here's how the community is already building on this work.

### Derivative Designs

It's exciting to see others building on the [wafer.space](https://wafer.space/) platform!
**[Professor Peter Kinget](https://peterkinget.github.io/)** and his students at **[Columbia University](https://peterkinget.github.io/)** are developing educational chips using [wafer.space](https://wafer.space/) for their [**MosBius Project**](https://mosbius.org/0_front_matter/intro.html).

MosBius provides students and designers the opportunity to explore MOS circuit topologies through a unique **analog switch matrix**, where each pin can connect to any of ten on-chip buses. This enables flexible on-chip circuit wiring and simplifies testing setups.

![MosBius Project chip design from Columbia University]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/chip-on-board/padframes-cob-mosbius.png)

*MosBius Project chip design from Columbia University*

*Image and design by @xianglin_pu on [wafer.space Discord](https://discord.gg/43y2t53jpE)*

---

### The Path Not (Yet) Taken

Before settling on the mezzanine connector as the standard, the community explored several alternative packaging approaches. While these didn't become the primary standard, they represent valuable experiments that informed the final design and may still serve specialized use cases.

#### LGA (Land Grid Array)

![LGA (Land Grid Array) COB package design]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/chip-on-board/padframes-cob-lga-cob.png)

*LGA (Land Grid Array) COB package design*

#### DIP

<table>
  <tr>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/chip-on-board/padframes-cob-dip.png" alt="" /></td>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/chip-on-board/padframes-cob-dip1.png" alt="" /></td>
  </tr>
  <tr>
    <td colspan="2"><em>DIP package designs for through-hole applications</em></td>
  </tr>
</table>

#### Castellated

![Castellated edge COB package design]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/chip-on-board/padframes-cob-castellated.png)

*Castellated edge COB package design*

---

## Learning from Pioneers

The wafer.space COB work doesn't exist in isolation. Other projects have tackled similar challenges, and their experiences directly inform this effort.

![Tiny Tapeout chip-on-board implementation]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/chip-on-board/padframes-cob-tt-cob.jpg)

*Tiny Tapeout chip-on-board implementation*

Tiny Tapeout recently [published an update](https://www.zerotoasiccourse.com/post/cob/) on their first successful Chip-on-Board (COB) implementation, highlighting their bare-die submission on the Zero to ASIC Course "MPW-7" run.

![Video thumbnail - Tiny Tapeout 9 First COB samples]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/chip-on-board/padframes-cob-tt-youtube.png)

*Video thumbnail - Tiny Tapeout 9 First COB samples*

[**Watch the video: Tiny Tapeout 9 - First COB samples!**](https://www.youtube.com/watch?v=XJmWoBJjvlI)

While Tiny Tapeout achieved a significant milestone, they also noted limitations: the long bonding wires increased inductance and degraded performance, and securing small-volume wire-bonding services remains difficult.

For those interested in understanding the wire bonding process in detail, Stephan Bökelmann's talk at Kicon 2025 provides an excellent introduction to the practical challenges and techniques:

[**Watch: Poor man's intro to Wire-Bonding @ Kicon 2025**](https://www.youtube.com/watch?v=dNBwY7L6niI)

The [wafer.space](https://wafer.space/) community views these learnings as a springboard. By introducing standardized COB templates, the goal is to make COB packaging more accessible, more scalable, and better optimized. The objective is to build upon the success of Tiny Tapeout and improve their future runs by reducing parasitics, streamlining the supply chain, and enabling anyone to pick up a COB-mounted die and integrate it into their system with ease.

---

## Join the Effort

This community-developed standard is exactly that: community-developed. The designs, symbols, and approaches documented here represent months of collaborative work, but they're far from finished.

The community is exploring multiple **COB packaging varieties** and would love your contribution:

**If you're designing a chip for this run:**
- Share your I/O requirements in the **#cob** Discord channel. Your needs help refine future designs
- Test the pad viewer tool and report any issues or feature requests

**If you have COB or wirebonding experience:**
- Share vendor recommendations or tips for small-volume runs
- Provide feedback on the wirebonding footprint design
- Help identify potential manufacturing issues before they become problems

**If you use other PCB design tools:**
- Contribute symbols and footprints for Altium, Eagle, or other platforms
- Submit pull requests to the [chip-on-board-wire-bonded-pcbs repo](https://github.com/wafer-space/chip-on-board-wire-bonded-pcbs)

**If you're curious or have questions:**
- Ask in Discord. The community includes experienced designers happy to help
- Review the designs using KiCanvas and suggest improvements
- Help test breakout board designs and report what works (or doesn't)

Join the community and help shape the future of accessible silicon design:

* **Discord:** [discord.gg/43y2t53jpE](https://discord.gg/43y2t53jpE) (see **#cob** channel)

* **Matrix:** [#gf180mcu.org](https://matrix.to/#/#gf180mcu:fossi-chat.org)

Together, the community can make custom silicon as easy and affordable as PCB design.

---

**Thanks to Andrew Wingate for this guest post!** If you're interested in chip-on-board packaging, join the **#cob channel** on the [wafer.space Discord](https://discord.gg/43y2t53jpE) to discuss designs, share feedback, and help contribute to making COB packaging accessible for everyone.

---

*This update was originally published on [Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-1/updates/chip-on-board).*
