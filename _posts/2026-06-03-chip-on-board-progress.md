---
layout: posts/post-boxed
title: "Chip-on-Board Packaging Progress"
date: 2026-06-03 12:00:00 +0000
excerpt: "Run 1 bare dies have shipped. Now we are working through chip-on-board packaging for customers who ordered that add-on."
categories: [news]
tags: [gf180mcu, run1, packaging, chip-on-board]
author: "Tim 'mithro' Ansell"
post_image: "/assets/images/news/chip-on-board-progress/thumbnail.jpg"
badge_color: "bg-purple"
slider_post: false
trending: false
sidebar: true
permalink: "/news/chip-on-board-progress"
galleries:
    cob_panels:
        caption: "Blank COB boards waiting for their die"
        images:
            - img: "/assets/images/news/chip-on-board-progress/cob-panel-front-back-view.jpg"
              alt: "Two panels held side-by-side"
            - img: "/assets/images/news/chip-on-board-progress/cob-single-top.jpg"
              alt: "Top view of the board"
            - img: "/assets/images/news/chip-on-board-progress/cob-single-bottom.jpg"
              alt: "Bottom view of the board"
    cob_bonds:
        caption: "Tiny Tapeout's TTGF0p2 die fully wirebonded and ready for epoxy"
        images:
            - img: "/assets/images/news/chip-on-board-progress/cob-bonded-top-view.jpg"
              alt: "Top view of TTGF0p2 on a black COB PCB"
            - img: "/assets/images/news/chip-on-board-progress/cob-bonded-side-view.jpg"
              alt: "Side view of TTGF0p2 on a black COB PCB"
    cob_finished:
        caption: "Finished COBs: wirebonded and epoxied, ready for your project"
        images:
            - img: "/assets/images/news/chip-on-board-progress/closeup-multiple-cobs.jpg"
              alt: "Four COBs next to each other"
            - img: "/assets/images/news/chip-on-board-progress/closeup-single-cob.jpg"
              alt: "A single COB"
    cloneless1_showcase:
        caption: "Thorben Moos' Cloneless1 die in a ceramic package"
        images:
            - img: "/assets/images/news/chip-on-board-progress/cloneless1-closeup.jpg"
              alt: "Closeup image of the Cloneless1 die"
            - img: "/assets/images/news/chip-on-board-progress/cloneless1-breadboard.jpg"
              alt: "Cloneless1 mounted in a ceramic package on a breadboard, wired to a microcontroller"

---

Run 1 bare dies and chips-on-board (COBs) have shipped - join us to have a look into the process.

{% include image.html file="/assets/images/news/chip-on-board-progress/closeup-single-cob.jpg" description="A wafer.space die wirebonded to a PCB, covered in protective epoxy" %}

## The Chip-on-Board Boards

If you've been following along, you may remember a [previous update](/news/chip-on-board-strategy)
where we discussed different potential strategies for chip-on-board packaging. In this update we will see all that hard
work come to fruition, as we wirebond some of the very first dies from this run.

The top-level view of the process is that each die is placed onto a small PCB and wirebonded to connect the die to the board.
Then, an epoxy glob-top is applied to protect the sensitive die and wires. The result is a packaged part that you can
plug into your own board and start testing immediately, no specialized equipment needed.

Wirebonding is inaccessible for most people, and traditional packaging solutions remain cost prohibitive due to the low
volume nature of the manufacturing runs. The COB boards were designed as an accessible way for people to use their
wafer.space dies.

These boards use an easily sourceable mezzanine connector for you to make your own motherboard. As always, the design
of this COB is available on [GitHub](https://github.com/wafer-space/chip-on-board-wire-bonded-pcbs).

{% include post-gallery.html gallery="cob_panels" %}

## Preparing for Wirebonding

The COB boards arrive as a panel of 20 from the PCB house, but these are too large to fit onto the vacuum chuck used by
the wirebonders. The solution is simple: snap the panels in half!

{% include image.html file="/assets/images/news/chip-on-board-progress/cob-on-vacuum-chuck.jpg" description="Half-a-panel of COBs fixed to the vacuum chuck" %}

Components moving during the wirebonding process is a concern. Tiny pads on the die and sharp movements caused by the
wirebonder mean that any misalignment could result in a failed bond (or multiple). These failed bonds could prevent
the chip from working properly, so our goal is to minimize any excessive movement.

The PCB itself is affixed to the chuck using a vacuum, and the die is physically glued to the PCB.

{% include image.html file="/assets/images/news/chip-on-board-progress/die-glueing-to-cob.jpg" description="wafer.space dies being glued to a COB board" %}

{% include image.html file="/assets/images/news/chip-on-board-progress/cob-empty-vs-populated.jpg" description="An unpopulated COB (left) next to one with a die (right)" %}

## Performing the Wirebonding

Everything so far has been quite hands-on, and this is no different with the wirebonding machine. Before any bonding
can take place, the machine must first be programmed with the desired locations and settings, and only then can it
proceed. The machine operator is provided with a diagram showing all of our requested bonds, which they will interpret
and configure the machine with.

{% include image.html file="/assets/images/news/chip-on-board-progress/BTAP-wirebond-diagram.png" description="Example wirebonding diagram showcasing visual landmarks and bond locations" %}

Since the die is mounted by hand, the machine uses a computer vision system to readjust the bond based on the visual
location.

{% include image.html file="/assets/images/news/chip-on-board-progress/wirebonder-operator.jpg" description="Wirebond operator configuring the bond path visually using a high-power microscope" %}

{% include youtube.html id="TODO" caption="Wirebond operator programming the bonds the machine needs to perform" autoplay=true %}

Now we're ready for the fun part! Once programmed, the machine will begin performing the wirebonding - all 74 pins.

{% include post-gallery.html gallery="cob_bonds" %}

We're not finished yet - the die and bonds are extremely fragile, so for them to survive the journey back to you, we must
first cover them with an epoxy resin and bake them in the oven to harden.

{% include post-gallery.html gallery="cob_finished" %}

## Final Steps

_Do they work?_

...

**Yes!!**

We've been able to successfully run Tiny Tapeout's own factory test on their TTGF0p2 shuttle, and can confirm that it
works as expected. We'd love to hear about your testing successes when you get your hands on your COBs, so please
come join our community on [Discord](https://discord.gg/43y2t53jpE)!

{% include youtube.html id="TODO" caption="Tiny Tapeout's TTGF0p2 factory test counting up (in binary, as shown on the LEDs)" autoplay=true %}


That's not all though - check out this scrolling VGA screensaver with the [wafer.space](https://wafer.space) logo. You can
view the source code for this on [GitHub](https://github.com/TinyTapeout/tt-waferspace-vga-screensaver), or experiment
with it on [VGA Playground](https://vga-playground.com/?repo=https://github.com/TinyTapeout/tt-waferspace-vga-screensaver).

{% include youtube.html id="TODO" caption="An animated wafer.space logo screensaver output over VGA" autoplay=true %}

[Sylvain "tnt" Munaut](https://github.com/smunaut) has also been hard at work testing several designs onboard the TTGF0p2
shuttle and reporting their status. You can view these on Tiny Tapeout's "Silicon Proven Projects" page - head to
[tinytapeout.com/chips/silicon-proven/#ttgf0p2](https://tinytapeout.com/chips/silicon-proven/#ttgf0p2) to view the
currently tested projects on TTGF0p2.

If you'd like to see some more packaging goodness, Tiny Tapeout recently uploaded a video with some more behind the scenes
footage for their TT08 shuttle.

{% include youtube.html id="okJ7NFNJdfs" caption="Behind the scenes footage of TT08 being wirebonded" autoplay=false mute=false controls=true fs=true %}

Of course, COBs aren't the only way to package your chip. Community member [Thorben Moos](https://www.thorbenmoos.de/)
bonded their die to a stunning ceramic DIP, with others doing (or planning to do) their own bonding too.

{% include post-gallery.html gallery="cloneless1_showcase" %}

## Shipping Timeline

COB packaged parts have started to ship. You will receive a notification from Crowd Supply when your order is on its way.

## Run 2: Slots Still Available

Run 2 slots are available on Crowd Supply until **30 June 2026**. Standard pricing is now in effect:

* **1x1 (full) slot**: $7,500 ($7.50/die)
* **0.5x1 (half width) slot**: $4,500 ($4.50/die)
* **1x0.5 (half height) slot**: $4,500 ($4.50/die)

Chip-on-board packaging is available as an add-on for $1,500 ($1.50/die).

* [Run 2 on Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-2)
* [Discord](https://discord.gg/43y2t53jpE)

\- Tim 'mithro' Ansell
