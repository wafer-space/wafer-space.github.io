---
layout: posts/post-boxed
title: "wafer.space x Tiny Tapeout - Hackaday 2026 Collaboration"
date: 2026-10-14 19:00:00 +0000
excerpt: "A look behind the scenes of open source silicon swag made in collaboration with Tiny Tapeout."
categories: [news]
tags: [gf180mcu, tiny-tapeout]
author: "Kristaps Jurkans"
post_image: "/assets/images/news/ws-tt-hackaday-collab-2026/epoxy-ready-tray.jpg"
badge_color: "bg-purple"
slider_post: false
trending: false
sidebar: true
permalink: "/news/ws-tt-hackaday-collab-2026"
galleries:
    logo-closeups:
        caption: "wafer.space and Tiny Tapeout logos visible on the die through a microscope"
        images:
            - img: "/assets/images/news/ws-tt-hackaday-collab-2026/wirebond-close-ws.jpg"
              alt: "wafer.space logo"
            - img: "/assets/images/news/ws-tt-hackaday-collab-2026/wirebond-close-tt.jpg"
              alt: "Tiny Tapeout logo"
    closeups:
        caption: "Close-up shots of the die -- note how delicate and thin the wire bonds are"
        images:
            - img: "/assets/images/news/ws-tt-hackaday-collab-2026/wirebond-done-med.jpg"
              alt: "Closeup shot of the bonded die on the PCB"
            - img: "/assets/images/news/ws-tt-hackaday-collab-2026/wirebond-done-close.jpg"
              alt: "Even closer shot, note how delicate and thin the wire bonds are"
---

# wafer.space x Tiny Tapeout - Hackaday 2026 Collaboration

Earlier this year the [wafer.space](https://wafer.space) team attended Hackaday 2026, and if you did too, then your
swag bag had a bit of open source silicon inside!

{% include image.html file="/assets/images/news/ws-tt-hackaday-collab-2026/closeup-multiple.jpg" description="A close-up image of the TTGF0p2 chip breakout boards" %}

Made in collaboration with [Tiny Tapeout](https://tinytapeout.com), these credit card sized breakout boards contain
an exposed [TTGF0p2](https://tinytapeout.com/chips/ttgf0p2/) die. This is an experimental shuttle run by Tiny Tapeout,
containing 52 unique open source designs, including a [ring oscillator](https://tinytapeout.com/chips/ttgf0p2/tt_um_dlmiles_ringosc_5inv),
[Zilog Z80 replica](https://tinytapeout.com/chips/ttgf0p2/tt_um_rejunity_z80), [TinyQV (a RISC-V processor)](https://tinytapeout.com/chips/ttgf0p2/tt_um_MichaelBell_tinyQV)
and many visual VGA demos.

Have you tried any of these projects yet? Let us know in the [wafer.space Discord](https://wafer.space/discord) and in
the [Tiny Tapeout Discord](https://tinytapeout.com/discord)!

Let's take a look at how they were made.

## Behind the Scenes

Tiny Tapeout opened the TTGF0p2 shuttle back in November 2026, where users could submit designs for free onto the shuttle
due to its experimental nature. It was only available for 18 days, but it filled up quickly. Once the deadline arrived,
TTGF0p2 was submitted onto Run #1 as `TTPG` and `TTP2`.

{% include image.html file="/assets/images/news/ws-tt-hackaday-collab-2026/ttp2-dies.jpg" description="TTP2 dies ready for processing" %}

Whilst Run #1 was being manufactured, the Tiny Tapeout team got to work on designing a colorful breakout board. Mounted
front and center is the die itself, covered with a glob of transparent epoxy. With a good enough eye (or a decent
microscope), you should be able to make out the tiny wire bonds that physically connect the die to the pins around
the edge of the breakout board. Surrounding the die is a render of the physical chip layout, where you can make out
each individual project (in green blocks) and the padring (in purple).

{% include image.html file="/assets/images/news/ws-tt-hackaday-collab-2026/blank-breakouts.jpg" description="Blank breakout boards" %}

The die is epoxied to the breakout board, and then mounted on a metal jig. This jig will help hold it in place while
the wire bonds are performed.

{% include image.html file="/assets/images/news/ws-tt-hackaday-collab-2026/mounted-breakout.jpg" description="A breakout board with a die, mounted in a metal jig" %}

The wire bonds are then programmed into the machine by the operator following a specification.

{% include image.html file="/assets/images/news/ws-tt-hackaday-collab-2026/wirebond-wide-tt.jpg" description="The operator programming the wire bond locations, the Tiny Tapeout logo on the die is visible on the screen" %}

[wafer.space](https://wafer.space) dies contain some area in the corners where artwork can be placed -- for this die,
both the Tiny Tapeout and [wafer.space](https://wafer.space) logos are visible.

{% include post-gallery.html gallery="logo-closeups" %}

After wire bonding, the breakout boards are carefully put aside for the next step -- covering the die and wire bonds
with a protective transparent epoxy. But not before some pictures!

{% include image.html file="/assets/images/news/ws-tt-hackaday-collab-2026/wirebond-done-wide.jpg" description="Wide shot of the breakout board and its die" %}

{% include post-gallery.html gallery="closeups" %}

Epoxy is mixed and then poured into a syringe. It will be manually applied for every board.

{% include image.html file="/assets/images/news/ws-tt-hackaday-collab-2026/epoxy-ready-tray.jpg" description="Breakout boards sitting on a tray ready for the epoxy treatment" %}

<!--
TODO video, see CS
-->

These are then moved into an oven for curing, and a vacuum is pulled to ensure that the epoxy is properly degassed.

{% include image.html file="/assets/images/news/ws-tt-hackaday-collab-2026/finished-tray.jpg" description="A finished batch of breakout boards, destined for Hackaday 2026" %}

Rinse and repeat a few more times, and eventually you'll have enough to give out one to each attendee of Hackaday 2026.

The process here is quite similar to what we already do for our chip-on-board packaging option, but you should check
out [our update]({{"/news/chip-on-board-progress" | relative_url }}) on it for more close-ups!

## Get Started Today
Run #3 is in full swing at the moment, so don't miss your opportunity to tape out. You've got until **9 December 2026**
to purchase a slot, and the submission deadline a week after on **16 December 2026**.

Read more on our [Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-3) page, jump in with our
[project template](https://github.com/wafer-space/gf180mcu-project-template) and join our
[community Discord](https://wafer.space/discord) to chat to other designers and get help.