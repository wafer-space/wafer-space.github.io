---
layout: posts/post-boxed
title: "Understanding wafer.space: Resources to Learn More About Our Mission"
date: 2025-10-31 12:00:00 +0000
categories: [news]
tags: [crowdsupply, gf180mcu, campaign]
author: "Tim 'mithro' Ansell"
badge_color: "bg-info"
slider_post: false
trending: false
sidebar: true
permalink: "/news/recent-publicity"
crowdsupply_url: "https://www.crowdsupply.com/wafer-space/gf180mcu-run-1/updates/recent-publicity"
---

*This update was originally published on [Crowd Supply](https://www.crowdsupply.com/wafer-space/gf180mcu-run-1/updates/recent-publicity).*

When Efabless shut down earlier this year, it left a critical gap: affordable access to custom silicon disappeared overnight. [wafer.space](https://wafer.space/) exists to fill that gap by providing pooled fabrication services that make custom silicon accessible at $7 per chip.

![wafer.space - Making custom silicon accessible]({{ site.baseurl }}/assets/images/news/gf180mcu-run-1/recent-publicity/shiny_sticker.svg)

*wafer.space - Making custom silicon accessible*

Since launching our campaign, we've had the opportunity to explain this mission across various platforms. Each conversation reveals different aspects of why accessible silicon matters and how we're making it happen. Here's your guide to learning more.

## Quick Start: Understanding the Vision

**Why does [wafer.space](https://wafer.space/) exist?** Start with these resources to quickly understand what we're building:

### [Electronics-Lab Interview](https://www.electronics-lab.com/e-lab-interview-wafer-space-founder-aims-to-make-custom-silicon-accessible-again/) (Article - 10 min read)
**What you'll learn:** Why Tim created wafer.space after Efabless collapsed, why GF180MCU was chosen (cost-optimized process from a major foundry), how the pricing works ($7k for 1,000 dies enables real product development), toolchain options (open source via LibreLane or proprietary), packaging choices, and the path from prototype to production. Covers the full journey from concept to manufactured chips.

### [HackWare Singapore Talk](https://www.youtube.com/watch?v=0nqV9Eo17wA) (Video - 30 min)
**What you'll learn:** The journey from requiring NDAs and expensive tools to accessible silicon design, how Tiny Tapeout demonstrated that anyone can create chips (5,000+ people have taped out), why [wafer.space](https://wafer.space/) uses GlobalFoundries' cost structure for better pricing, and making Arduino-like products with custom silicon at $7,000 for 1,000 parts.

## Deep Dive: Technical & Business Details

**How does it actually work?** These resources explore the mechanics, economics, and ecosystem:

### [Teardown Session 56: wafer.space with Tim Ansell & Leo Moser](https://youtu.be/tEOmnN8IAjs) (Video - 45 min)
**What you'll learn:** How silicon pooling works like PCB services (OSH Park for chips), the journey from Google's open PDK program through Efabless to [wafer.space](https://wafer.space/), why 1,000 chips for $7,000 ($7/chip) makes custom silicon accessible for small-scale production (100-1000 units), and how open-source tools (LibreLane) and open PDKs enable this infrastructure.

### [The Amp Hour #703](https://theamphour.com/703-building-wafer-space-with-tim-ansell/) (Podcast - 90 min)
**What you'll learn:** The economics of pooled fabrication ($7k for 1,000 dies vs eFabless $10k for 150-200 dies), packaging options (bare die, chip-on-board, wirebonding with secondhand equipment), design tools from Tiny Tapeout to Verilog to analog layout, post-eFabless ecosystem (IHP Europe, ChipFoundry US, [wafer.space](https://wafer.space/) Singapore), professional help options (ChipFlow, Mabrains), and honest discussion about what makes $7/chip sustainable. Essential listening for anyone considering their own silicon project.

## Community Perspectives: Why This Matters

The tech press and community discussions reveal something important—this isn't just about one company or service. It's about fundamental infrastructure:

### What Resonates: Three Key Themes

**"Like OSH Park for silicon"** - Writers keep making this comparison because it captures something essential: predictable pricing, regular runs, and community-driven infrastructure that just works. Read more in [Hackster.io's coverage](https://www.hackster.io/news/wafer-space-delivers-1-000-chips-of-your-own-design-starting-at-just-7-each-75bbf49fd8b0).

**"Democratizing chip design"** - When [CNX Software](https://www.cnx-software.com/2025/10/07/wafer-space-lets-you-design-your-custom-silicon-just-for-7-per-die/) and [LinuxGizmos](https://linuxgizmos.com/wafer-space-launches-gf180mcu-run-1-for-custom-silicon-fabrication/) cover the $7/die pricing, they're recognizing a shift: different people with different budgets can now participate in hardware innovation.

**"Post-Efabless infrastructure"** - The [Contextual Electronics forum discussion](https://forum.contextualelectronics.com/t/wafer-space-low-cost-silicon-manufacturing-7k-1-000-ics/7313) digs into what this means practically: continuing critical work that an existing community depends on.

### Active Discussions & Questions

Community conversations reveal the questions people are asking and projects they're planning:

**[David Shadoff on Bluesky](https://bsky.app/profile/dshadoff.bsky.social/post/3m2ie2vm2ns2y)** explores retro-computer and console chip designs: "Most can be done on FPGA today, custom silicon could make assembly cheaper (reducing FPGA support)." This captures a key use case—when custom ASICs make more sense than FPGAs for production.

**[Luke Wren on Mastodon](https://types.pl/@wren6991/115267990436492107)** does the math on what fits in 20mm²: "The smallest NAND2 is 11 square microns, so assuming 2/3rds of the die is non padding, that's 1.2 million gates. The densest SRAM macro they provide is 512 bytes in 0.21 mm², so if you fill the area with RAM that's around 31 kB. Enough for a small Linux SoC." Real calculations showing what's actually achievable.

Other discussions across [Mastodon (#OpenSilicon)](https://mastodon.social/tags/OpenSilicon), [Reddit (/r/chipdesign)](https://www.reddit.com/r/chipdesign/), and [LinkedIn](https://www.linkedin.com/feed/hashtag/opensilicon/) explore:
- Technical: "What's achievable in 20mm²?"
- Practical: "Can this work for small production runs?"
- Strategic: "How does this change who can design chips?"

Join these discussions to learn from others exploring the same questions.

## Your Learning Path Forward

Whether you're curious or committed, here's how to engage:

1. **Quick start** - Read the [Electronics-Lab interview](https://www.electronics-lab.com/e-lab-interview-wafer-space-founder-aims-to-make-custom-silicon-accessible-again/) or watch the [HackWare talk](https://www.youtube.com/watch?v=0nqV9Eo17wA) to grasp the mission
2. **Deep dive** - Watch the [Teardown session](https://youtu.be/tEOmnN8IAjs) or listen to [The Amp Hour](https://theamphour.com/703-building-wafer-space-with-tim-ansell/) for technical and business insights
3. **Connect with community** - Join [Discord](https://discord.gg/43y2t53jpE) or [Matrix](https://matrix.to/#/#gf180mcu:fossi-chat.org) to ask questions and learn from others
4. **Evaluate your project** - Use the resources above to determine if Run 1 fits your needs

**Ready to participate?** Campaign closes November 28th. Reserve your slot at [buy.wafer.space](https://buy.wafer.space/).

**Still learning?** That's perfect. Use these resources to understand not just what we're offering, but why rebuilding accessible silicon infrastructure matters for the future of open hardware.

## Coming Updates: Practical Guidance

Future updates will provide hands-on learning:
- Example designs - what fits in 20mm² with detailed analysis
- Submission process - step-by-step guide for December 3rd deadline
- Packaging options - understanding your choices from bare dies to chip on board option

## The Bigger Picture

When custom silicon costs $7 per chip instead of requiring $70,000 minimum orders, different people with different projects can participate. Students can learn chip design alongside programming. Hardware startups can prototype with custom ASICs instead of compromising with FPGAs. Retro computing enthusiasts can recreate vintage chips. Small production runs become viable.

The conversations above explore this shift from multiple angles—technical, economic, and practical. They document not just what [wafer.space](https://wafer.space/) offers, but why rebuilding accessible fabrication infrastructure matters for hardware innovation.
