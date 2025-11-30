---
layout: posts/post-boxed
title: "We Have Some Amazing Projects This Run: MOSbius"
date: 2025-11-19 12:00:00 +0000
categories: [news]
tags: [crowdsupply, gf180mcu, campaign]
author: "Tim 'mithro' Ansell"
badge_color: "bg-info"
slider_post: false
trending: false
sidebar: true
permalink: "/news/mosbius-feature"
post_image: "/assets/images/news/gf180mcu-run-1/mosbius-feature/mosbius_flow.png"
crowdsupply_url: "https://www.crowdsupply.com/wafer-space/gf180mcu-run-1/updates/mosbius"
---

Our first shuttle run spans from solo makers like Tholin to universities. This week we highlight [MOSbius](https://mosbius.org/), an educational platform from Columbia University bringing hands-on silicon learning to students worldwide.

Through wafer.space, MOSbius gains 3.3V compatible I/Os, high part counts, and COB packaging—all for a low cost. What was once an expensive demonstration can now equip every student in a classroom with their own chip, for less than the cost of a textbook.

## [MOSbius](https://mosbius.org/)

![MOSbius platform enables hands-on exploration of transistor-level MOS circuits on breadboard]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/mosbius-feature/mosbius_flow.png)

*MOSbius platform enables hands-on exploration of transistor-level MOS circuits on breadboard*

**[MOSbius](https://mosbius.org/)**, developed by **[Professor Peter Kinget](https://peterkinget.github.io/)** and his students at **[Columbia University](http://www.cisl.columbia.edu/kinget_group/)**, is an innovative educational platform that helps students and designers explore **MOS circuit topologies** typically found on silicon and now accessible on a breadboard.

The goal of [MOSbius](https://mosbius.org/) is to give learners hands-on experience with **transistor-level design**, including circuit debugging, measurement, and the full "chip bring-up" process. The platform allows users to compare calculations, simulations, and real measurements using provided **[LTspice](https://wiki.analog.com/resources/tools-software/ltspice) models**, bridging the gap between theory and silicon.

![MOSbius – A Field Programmable Transistor Array for Chip Designers (Interview with Peter Kinget)]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/mosbius-feature/mosbius_interview.png)

*MOSbius – A Field Programmable Transistor Array for Chip Designers (Interview with Peter Kinget)*

**[Watch the interview on YouTube](https://www.youtube.com/watch?v=abu3u6UX6wE)**

### Building on Previous Success

MOSbius isn't new to custom silicon. Previous generations of the MOSbius chip demonstrated the educational value of hands-on transistor exploration, but faced a significant barrier: cost. At $50 per packaged chip, widespread educational deployment remained challenging.

The project's educational impact extends beyond the classroom. The [IEEE SSCS Chipathon 2025](https://github.com/mosbiuschip/chipathon2025) featured a MOSbius track where students learned chip design using GF180MCU—the same process used by wafer.space. This gave Chipathon participants hands-on experience with the same technology they could use for future fabrication runs.

### Their Own COB Format

Given the unique requirements of the MOSbius project, the team is designing their own version of a **Chip-on-Board (COB)** package based on the [wafer.space standard padframe](https://www.crowdsupply.com/wafer-space/gf180mcu-run-1/updates/chip-on-board).

Their application prioritizes **a high number of I/O connections** over power and ground pads, allowing for the maximum number of accessible signals from their transistor array.

<table>
  <tr>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/mosbius-feature/mos_pcb.png" alt="" /></td>
    <td><img src="{{ site.baseurl }}/assets/images/news/gf180mcu-run-1/mosbius-feature/mos_3d.png" alt="" /></td>
  </tr>
  <tr>
    <td colspan="2"><em>MOSbius custom COB package design - PCB layout and 3D visualization</em></td>
  </tr>
</table>

**Peter's student, @xianglin_pui**, has taken the lead on this effort and developed derivative designs that extend the wafer.space COB standard for MOSbius's specialized needs.

### wafer.space and MOSbius

We're thrilled to have **MOSbius** as part of this shuttle run and proud to support a project that aligns so perfectly with wafer.space's mission.

Their current board design requires numerous passive components due to varying pin voltage levels, and each packaged chip can cost upwards of **$50**. With their new design on the **[wafer.space](https://wafer.space/)** platform, all pins will be **3.3 V tolerant**, eliminating the need for numerous passive components and dramatically simplifying their demo board, while wafer.space's affordable pricing and **COB packaging** reduce costs.

## Don't Miss Your Chance to Join the First Shuttle

![wafer.space - Accessible custom silicon fabrication]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/mosbius-feature/rainbow_narrow2.svg)

*wafer.space - Accessible custom silicon fabrication*

MOSbius is part of this run because accessible silicon enables their educational mission. What becomes possible at $7/chip? Whether you're building educational tools, [exploring new architectures](https://www.crowdsupply.com/wafer-space/gf180mcu-run-1/updates/openfasoc), or [bringing vintage designs back to life](https://www.crowdsupply.com/wafer-space/gf180mcu-run-1/updates/tholin-feature) - this is your opportunity.

We're rapidly approaching the final milestones for this shuttle run, and now is the time to secure your spot:

- **November 28, 2025** - Last day to purchase a slot / [Crowd Supply campaign](https://www.crowdsupply.com/wafer-space/gf180mcu-run-1) closes

- **December 3, 2025** - [Final GDS submission deadline](https://wafer.space/how)

If you’ve been thinking about getting your own silicon made — whether it’s your first chip or your fiftieth — this is your moment. The tools are ready, the ecosystem is growing, and we’re here to help you every step of the way.

[Reserve your slot](https://www.crowdsupply.com/wafer-space/gf180mcu-run-1), finish your design, and join us in shaping the future of accessible custom silicon.

---

*This update was originally published on [Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-1/updates/mosbius).*
