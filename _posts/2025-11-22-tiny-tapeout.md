---
layout: posts/post-boxed
title: "Tiny Tapeout Collaboration"
date: 2025-11-22 12:00:00 +0000
categories: [news]
tags: [crowdsupply, gf180mcu, campaign]
author: "Tim 'mithro' Ansell"
badge_color: "bg-info"
slider_post: false
trending: false
sidebar: true
permalink: "/news/tiny-tapeout"
crowdsupply_url: "https://www.crowdsupply.com/wafer-space/gf180mcu-run-1/updates/tiny-tapeout"
---

*This update was originally published on [Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-1/updates/tiny-tapeout).*

## Tiny Tapeout

![Tiny Tapeout - Democratizing chip design]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tiny-tapeout/tinytapeout-logo.png)

*Tiny Tapeout - Democratizing chip design*

[wafer.space](https://wafer.space/) is excited to collaborate with [Tiny Tapeout](https://tinytapeout.com/) to port their infrastructure to GF180MCU. Founded by [Matt Venn](https://zerotoasiccourse.com/), Tiny Tapeout has become a cornerstone of the open-silicon movement, empowering students, hobbyists, and even industry professionals to design and fabricate their own ASICs through approachable tools and collaborative workflows. Our collaboration provides an easy and affordable pathway from initial ideas and prototyping to building real products.

![With Tiny Tapeout, you get a ready-to-go development board]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tiny-tapeout/previous-tt-version.jpeg)

*With Tiny Tapeout, you get a ready-to-go development board*


Tiny Tapeout has already proven that accessible chip design works. By dramatically lowering the barrier to entry, they've enabled thousands of participants to bring their digital and analog designs to life. Now, our collaboration aims to take that further, helping designs move from prototype to product. The track record speaks for itself:

<table>
  <tr>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tiny-tapeout/tt03-gds.png" alt="" /></td>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tiny-tapeout/tt05-gds.png" alt="" /></td>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tiny-tapeout/tt06-gds.png" alt="" /></td>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tiny-tapeout/tt07-gds.png" alt="" /></td>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tiny-tapeout/tt09-gds.png" alt="" /></td>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tiny-tapeout/ttihp0p1-gds.png" alt="" /></td>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tiny-tapeout/ttsky25a-gds.png" alt="" /></td>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tiny-tapeout/ttsky25b-gds.png" alt="" /></td>
  </tr>
  <tr>
    <td colspan="8"><em>GDS renders from Tiny Tapeout shuttles [TT03](https://tinytapeout.com/chips/tt03/), [TT05](https://tinytapeout.com/chips/tt05/), [TT06](https://tinytapeout.com/chips/tt06/), [TT07](https://tinytapeout.com/chips/tt07/), [TT09](https://tinytapeout.com/chips/tt09/), [IHP 0.1](https://app.tinytapeout.com/shuttles/ttihp0p1), [Sky130 25a](https://tinytapeout.com/chips/ttsky25a/), and [Sky130 25b](https://tinytapeout.com/chips/ttsky25b/)</em></td>
  </tr>
</table>

Building on this experience, **Tiny Tapeout** now joins wafer.space to bring GF180MCU into the mix. Our collaboration has enabled Tiny Tapeout to get exactly what they need from the [standard wafer.space padframe](https://www.crowdsupply.com/wafer-space/gf180mcu-run-1/updates/chip-on-board), ensuring full compatibility, consistent manufacturability, and reliable integration with COB-based packaging workflows.

## What's Being Built on [GF0p2](https://app.tinytapeout.com/shuttles/ttgf0p2)

Both Tiny Tapeout and wafer.space have been thrilled by the community response. The [GF0p2 shuttle](https://app.tinytapeout.com/shuttles/ttgf0p2) already has dozens of projects submitted, and more are coming in every day. Here are just a few of the designs being built:

### Modern Free and Open Source Silicon Clone of Zilog's Z80

[Rejunity](https://github.com/rejunity) is recreating [Zilog's Z80](https://app.tinytapeout.com/projects/3434) with the goal to develop a drop-in replacement for 8-bit home computers such as the ZX Spectrum and recent DIY computer kits such as the [RC2014](https://rc2014.co.uk/).


### Tiny-QV: A RISC-V SoC for Tiny Tapeout

[Tiny-QV](https://github.com/MichaelBell/tinyQV/) is a 4-bit-at-a-time RV32 processor, optimized for use on Tiny Tapeout with QSPI RAM and Flash. The aim is to make a small microcontroller that is as fast as practical given the Tiny Tapeout constraints.

### Zedulo Test Chip

[Zedulo TestChip1](https://github.com/ZeduloTech/ttgf-zed_tc1) is a UART-to-SPI bridge built using two IP blocks from the [OpenTitan](https://opentitan.org/) project (an open-source Root of Trust). By porting these OpenTitan components to GF180MCU, Zedulo demonstrates that verified, trustworthy hardware IP can be reused across different processes and platforms.

### And Many More

| Project                                                                                        | Description / Notes                                                                                                             |
| ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **[2x2 MAC Systolic array with DFT](https://app.tinytapeout.com/projects/3441)**                        | ASIC design for a 2x2 systolic matrix multiplier supporting multiply and accumulate operations on int8 data.            |
| **[WaferSpace VGA Screensaver](https://github.com/TinyTapeout/tt-waferspace-vga-screensaver)** | A classic animated VGA demo that prominently features the **wafer.space** logo — great for verifying display output and timing. |
| **[Asicle v2 (2×2 tiles)](https://app.tinytapeout.com/projects/3248)**                                                                      | A compact, tile-based modular layout design that explores reconfigurable logic or array instantiation.                          |
| **[ROM / Memory Block (1×1)](https://app.tinytapeout.com/projects/3119)**                                                                   | A read-only memory block intended for basic data storage — ideal for boot code or test vectors.                                 |
| **[Ring Oscillator (5-inverter, 1×1)](https://app.tinytapeout.com/projects/3125)**                                                          | A simple analog / digital hybrid circuit that toggles signal through five inverters to create a ring oscillator.                |
| **[Simon Says Logic Game](https://app.tinytapeout.com/projects/3121)**                                                                      | Implements the classic “Simon Says” memory game in hardware logic — the chip will reproduce user-input sequences.               |
| **[Sound Generator (TBB143)](https://app.tinytapeout.com/projects/3430)**                                                                   | A programmable sound generator that uses a ring oscillator to generate tones or effects.                                        |

The project tiles are filling up fast:

![Project tiles already allocated on the GF0p2 run]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tiny-tapeout/current-run.png)

*Project tiles already allocated on the GF0p2 run*

## Join Us!

We're thrilled to have **Tiny Tapeout** and **Matt Venn** on board for our first wafer.space shuttle, but the most exciting part is having **you** join us too! Whether you're a complete beginner or an experienced designer, now is the perfect time to get started.

Explore the [Tiny Tapeout website](https://tinytapeout.com/) for project ideas and tutorials, and watch the [YouTube channel](https://www.youtube.com/@ZeroToASICcourse) for walkthroughs and interviews. If you need something more structured, Matt's excellent [Zero to ASIC course](https://zerotoasiccourse.com/) will give you the knowledge and confidence to bring your ideas to silicon.

Even if you haven't done a tapeout yet, join the community and start learning! Connect with us on the [wafer.space Discord](https://discord.gg/43y2t53jpE) and join the **#tinytapeout** channel, or the [Tiny Tapeout Discord](https://discord.gg/rPK2nSjxy8) and join the **#ttgf0p2-tapeout** channel. (You can also find us on [Matrix at #gf180mcu](https://matrix.to/#/#gf180mcu:fossi-chat.org).)

With Tiny Tapeout, anyone can get started with just a web browser and a few hours. [Why not give it a try?](https://tinytapeout.com/)

---

## Don't Miss Your Chance to Join the First Shuttle

![wafer.space bringing open accessible custom silicon fabrication]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tiny-tapeout/waferspace-rainbow-open.png)

*wafer.space bringing open accessible custom silicon fabrication*

We’re rapidly approaching the final milestones for this shuttle run, and now is the time to secure your spot:

- **November 28, 2025** - Last day to purchase a slot (Crowd Supply campaign closes)

- **December 3, 2025** - Final GDS submission deadline. Your design must be submitted to wafer.space by this date to be included in the run.

If you've been thinking about getting your own silicon made, whether it's your first chip or your fiftieth, this is your moment. The tools are ready, the ecosystem is growing, and we’re here to help you every step of the way.

Reserve your slot, finish your design, and join us in shaping the future of accessible custom silicon.

---

### Special Thanks

<table>
  <tr>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tiny-tapeout/tillitis-logo-std.png" alt="" /></td>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/tiny-tapeout/witcom-logo-std.png" alt="" /></td>
  </tr>
  <tr>
    <td colspan="2"><em>Sponsored by [Tillitis](https://www.tillitis.se/) and [WIT.com](https://wit.com/)</em></td>
  </tr>
</table>

[Tillitis](https://www.tillitis.se/) and [WIT.com](https://wit.com/) generously sponsored the work to bring Tiny Tapeout to GF180MCU, its third process technology. This funding is enabling the [improved multiplexer](https://www.youtube.com/watch?v=30emLKLpq50), [power gating, analog support](https://www.youtube.com/watch?v=_m_jK7twymM), and [more](https://www.youtube.com/watch?v=cCbTyfewaCw) (designed by [Sylvain "tnt" Munaut](https://github.com/smunaut)) to be ported to GF180MCU. Thank you for making this happen!
