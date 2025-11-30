---
layout: posts/post-boxed
title: "Building Real Sensors with GF180MCU"
date: 2025-11-05 12:00:00 +0000
categories: [news]
tags: [crowdsupply, gf180mcu, campaign]
author: "Tim 'mithro' Ansell"
badge_color: "bg-info"
slider_post: false
trending: false
sidebar: true
permalink: "/news/openfasoc-sensors"
crowdsupply_url: "https://www.crowdsupply.com/wafer-space/gf180mcu-run-1/updates/openfasoc"
---

As we get closer to our **December 3rd tape-in deadline** (that's coming up fast!), I wanted to share something that really shows the power of what you can build with the [GF180MCU process](https://gf180mcu-pdk.readthedocs.io/) we're pooling together.

## Real Silicon, Real Applications

[Saligane](https://vivo.brown.edu/display/msaligan)'s group at the University of Michigan - now at Brown University - recently published [a paper in IEEE Solid-State Circuits Magazine](https://ieeexplore.ieee.org/document/10584418) showing off an analog front-end (AFE) chip they designed entirely with open-source tools on GF180MCU. And it's not just a test chip — they're using it to read out flexible laser-induced graphene sensors for wearables!

![The fabricated GF180MCU chip showing OPAMP blocks, SAR ADC, and switched-capacitance circuits]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/openfasoc-sensors/annotated_shot.png)

*The fabricated GF180MCU chip showing OPAMP blocks, SAR ADC, and switched-capacitance circuits*

([View high-resolution die photography on Silicon Prawn](https://siliconprawn.org/archive/doku.php?id=mcmaster:efabless:gf180mcu-mpw18h1-18100004))

The chip integrates operational amplifiers, a 14-bit SAR ADC, and a capacitive DAC to create a complete sensor readout platform. They demonstrated it working with:

- **Strain/flex sensors** (detecting finger bending in real-time)
- **Temperature sensors** (tracking body temperature with 0.9989 R² accuracy)
- **Multi-modal sensing** (combining different sensor types on one platform)

![The fabricated chip wire-bonded to a PCB, ready to interface with flexible sensor patches]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/openfasoc-sensors/test_setup.png)

*The fabricated chip wire-bonded to a PCB, ready to interface with flexible sensor patches*

## The Open Source Flow Works!

What's exciting is they used the exact same open-source toolchain you have access to:
- [XSchem](https://xschem.sourceforge.io/stefan/index.html) for schematic capture
- [Ngspice](https://ngspice.sourceforge.io/) for simulation
- [KLayout](https://www.klayout.de/) and [Magic](https://github.com/RTimothyEdwards/magic) for layout
- Standard DRC/LVS checks

They've published their designs on GitHub in the [OpenFASoC-Tapeouts repository](https://github.com/idea-fasoc/openfasoc-tapeouts?tab=readme-ov-file#user-content-analog-front-end-and-mixed-signal), and the [final submission is available on foss-eda-tools](https://foss-eda-tools.googlesource.com/third_party/shuttle/gf180mcu/mpw-18h1/slot-004/+/refs/heads/main), which means you can actually look at exactly how they did it.

![The complete open-source analog design flow used for this project]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/openfasoc-sensors/analog_flow.png)

*The complete open-source analog design flow used for this project*

## Reuse, Don't Reinvent!

This is where it gets really interesting for your designs. The [OpenFASoC project](https://github.com/idea-fasoc/OpenFASOC) provides **building blocks you can directly reuse**:

- **[Folded-cascode OPAMP](https://github.com/idea-fasoc/openfasoc-tapeouts/tree/main/mpw18h1/opamp-gen/Programmable_2stage)** with programmable bias for noise/power trade-offs
- **[14-bit SAR ADC](https://github.com/idea-fasoc/openfasoc-tapeouts/tree/main/mpw18h1/adc-gen/comparator)** (asynchronous, monotonic switching)
- **[Bootstrapper and switch circuits](https://github.com/idea-fasoc/openfasoc-tapeouts/tree/main/mpw18h1/cisar-gen/spice)** for high-performance sampling
- **[Comparator circuits](https://github.com/idea-fasoc/openfasoc-tapeouts/tree/main/mpw18h1/adc-gen/comparator)** (double-tail latch and StrongArm topologies)

You can literally take their [GDSII files](https://github.com/idea-fasoc/openfasoc-tapeouts/tree/main/mpw18h1/gds), study their layout techniques, and adapt their circuits for your own sensor applications. Need to read out a resistive sensor? Temperature probe? Custom transducer? The hard work of building reliable analog blocks is already done.

![Real-time flex sensor demonstration showing finger bending detection with the AFE chip]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/openfasoc-sensors/testing.png)

*Real-time flex sensor demonstration showing finger bending detection with the AFE chip*

## What Could You Build?

Think about applications like:
- Environmental monitoring devices
- Biomedical wearables  
- Industrial sensor nodes
- Custom instrumentation
- IoT edge devices with analog sensing

With [GF180MCU's](https://gf180mcu-pdk.readthedocs.io/) 5 metal layers, MIM capacitors, multiple resistor types, and mixed-signal capabilities, you have everything needed for serious analog and mixed-signal designs.

## Get Inspired, Get Building

Check out the [full paper](https://siliconprawn.org/archive/lib/exe/fetch.php?media=mcmaster:efabless:gf180mcu-mpw18h1-18100004:rapid-prototyping-of-laser-induced-graphene-sensors-with-open-source-silicon-paving-the-way-small.pdf) to see detailed schematics, measurement results, and their complete design flow. This is real silicon, designed with open tools, doing real work — exactly what we're enabling with this pooled run.

For questions about the campaign or getting started with GF180MCU, join the community on [Discord](https://discord.gg/43y2t53jpE) or [Matrix](https://matrix.to/#/#gf180mcu:fossi-chat.org).

---

*Reserve your slot at [buy.wafer.space](https://buy.wafer.space/) before November 28th to be part of Run 1.*

---

*This update was originally published on [Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-1/updates/openfasoc).*
