---
layout: posts/post-boxed
title: "GF180MCU Linux/XV6 RISC-V SoC"
date: 2026-04-10 12:00:00 +0000
excerpt: "KianV is a custom GF180MCU-based RISC-V SoC capable of running uLinux, Linux, and XV6 using a fully open-source ASIC flow."
categories: [news]
tags: [gf180mcu, run1, featured-project, risc-v, kianv]
author: "Hirosh Dabui"
badge_color: "bg-purple"
slider_post: false
trending: false
sidebar: true
permalink: "/news/kianv-riscv-soc"
post_image: "/assets/images/news/kianv-riscv-soc/soc-overview.svg"
---

## Introduction

This article presents **KianV**, a custom **GF180MCU-based RISC-V SoC** capable of
running **uLinux, Linux, and XV6** using a fully open-source ASIC flow.
The project was developed as part of the **wafer.space GF180MCU Run 1**.

In addition to the ASIC, a compact bring-up PCB was designed to enable hardware
validation and early software development.

Repository: [github.com/splinedrive/kianRiscV](https://github.com/splinedrive/kianRiscV)

---

## SoC Overview

The KianV SoC is built around an **RV32 RISC-V core (RV32IMA)** with support for
**Zicntr, Zicsr, Zifencei, and SSTC**, and implements **SV32 virtual memory**,
enabling **uLinux, Linux, and XV6** to run on custom silicon.

The CPU includes a **2-way set-associative instruction cache**, a
**direct-mapped data cache**, and **4-way associative instruction and data TLBs**,
sufficient for MMU-based operating systems.

The SoC integrates a minimal peripheral set connected via an internal system bus:

- **SDRAM controller** (32 MiB external memory)
- **UART**
- **2× SPI**
- **GPIO**
- **NOR flash controller**

The system boots from an **SD card**, provides **network connectivity**, and
operates at **3.3 V** on a mature **180 nm technology node**.

![Block diagram of the KianV RV32 SV32-capable RISC-V SoC.](/assets/images/news/kianv-riscv-soc/soc-overview.svg)

---

## Pinout
The following table summarizes the external IO signals of the **KianV SoC**.
The pinout is designed around a strict **58 external IO signal** limit.
In total, the chip provides **74 pads**, including **power** and **ground** connections.
The external IO supports **SDRAM**, **SPI flash**, **SD card**, **Ethernet**, and **UART**.


![KianV SoC external IO pinout.](/assets/images/news/kianv-riscv-soc/chip_symbol.png)

| Interface | Signals                       | Dir | Description        |
|:---------:|-------------------------------|:---:|--------------------|
| **UART**  | `RX`, `TX`                    | I/O | Serial console     |
| **SPI0**  | `CS#`, `SCLK`, `MOSI`, `MISO` | I/O | SD card            |
| **SPI1**  | `CS#`, `SCLK`, `MOSI`, `MISO` | I/O | Ethernet           |
| **Flash** | `CS#`, `SCLK`, `MOSI`, `MISO` | I/O | SPI NOR flash      |
| **SDRAM** | `CLK`, `CKE`                  | Out | Clocking           |
|           | `ADDR[12:0]`                  | Out | Address bus        |
|           | `BA[1:0]`                     | Out | Bank select        |
|           | `DQ[15:0]`                    | I/O | Data bus           |
|           | `DQM[1:0]`                    | Out | Byte mask          |
|           | `CS#`, `RAS#`, `CAS#`, `WE#`  | Out | Control signals    |
| **GPIO**  | `GPIO0`                       | I/O | General-purpose IO |

*Signals are grouped by function; directions are given from the SoC perspective.*

---

## Design Philosophy

The RISC-V processor in this SoC is a **multi-cycle RV32 core, optimized for area**.

The architecture was validated prior to the GF180MCU ASIC implementation on
FPGA platforms, where **SV32-capable mainline Linux** and **network connectivity**
were demonstrated.

A **uLinux (no-MMU) version** of the KianV SoC was fabricated via **Tiny Tapeout**,
providing silicon validation of the core and peripheral subsystems. The KianV SoC
is **mentioned in a FOSSi Foundation article**
(https://fossi-foundation.org/blog/2025-01-14-ecl82) and **referenced in an IEEE
Solid-State Circuits Magazine publication**
(https://ieeexplore.ieee.org/document/10584359).

![SkyWater 130 nm die layout of the Tiny Tapeout KianV uLinux (no-MMU) SoC.](/assets/images/news/kianv-riscv-soc/tt_ulinux_soc_kianv.png)

---

## ASIC Design Flow

The SoC was implemented using **LibreLane**, based on the
**wafer.space GF180MCU project template** and the **gf180mcu PDK**.
The flow covers RTL synthesis, floorplanning, place-and-route,
clock tree synthesis, and physical verification using open-source tools.

---

## Implementation Results

Linux was booted in **gate-level simulation** (approximately one month runtime)
using a **mainline Linux kernel 6.19**, and validated against a
**Micron SDRAM simulation model** driven by the author’s SDRAM controller.

**Silicon validation is pending.**

Key metrics:

- **Die size:** 3.93 mm × 5.12 mm (≈ 20.1 mm²)
- **Core utilization:** ~65%
- **IO count:** 58
- **Estimated power:** ~13 mW (nominal)

---

## ASIC GF180MCU Layout

![KianV SoC ASIC layout. Cache SRAM blocks surround the central core, with peripherals and IO placed around the perimeter.](/assets/images/news/kianv-riscv-soc/chip_top_white.png)


---

## PCB Design

A small bring-up PCB was designed to support validation and software bring-up.
The board provides **32 MiB SDRAM**, **SPI-based Ethernet**,
**SPI flash / SPI card**, **UART**, power regulation.

![KianV GF180MCU ASIC bring-up PCB (top and bottom views).](/assets/images/news/kianv-riscv-soc/pcb_top.png)

![KianV GF180MCU ASIC bring-up PCB (top and bottom views).](/assets/images/news/kianv-riscv-soc/pcb_bottom.png)

---

## Software Status

The system uses a **custom bootloader**, followed by **OpenSBI**, and then boots
the **Linux kernel**. Only **minimal driver adaptations** were required to boot
**mainline Linux with SV32 MMU support** on the SoC.

In addition to Linux, the system also runs **uLinux** and **XV6** on the same
hardware platform.

![Linux mainline (6.19.0-rc1) booting on the KianV RISC-V SoC.](/assets/images/news/kianv-riscv-soc/console.png)

---

## Acknowledgments

- **Andrew Wingate** – board design review (wafer.space)
- **Christian Stredicke** – Voida PBX
- **Goran Maholvic** – board design support and SDRAM routing
- **Leo Moser** – ASIC flow and PDK support (wafer.space)
- **Marcelo Samsoniuk** - for the technical and personal exchange over the past few years (DarkRiscV)
- **Matt Venn** – Tiny Tapeout
- **Sylvain Munaut** – Tiny Tapeout
- **Tim Ansell** – founder of wafer.space
- **Uri Shaked** – Tiny Tapeout

---

## Conclusion

This project demonstrates a **minimal, Linux-capable RV32 SoC** implemented using
an **open-source ASIC flow** on **GF180MCU**, manufactured through **wafer.space**.


## Additional Resources

- Carl Karsten - [Direct access to the KianV uLinux ASIC SoC](https://ps1.fpgas.online/fpgas/tt6.html)
- Matt Venn - [RISC-V/Open Source Silicon Stream updates](https://www.linkedin.com/posts/matt-venn_riscv-opensourcesiliconstream-activity-7290765655132274690-Hfgw)
- Matt Venn - [Tiny Tapeout ASIC/Open Source development](https://www.linkedin.com/posts/matt-venn_asic-opensource-riscv-activity-7279556029233704960-d5ZO)
- Uri Shaked — [Tiny Tapeout project update (LinkedIn)](https://www.linkedin.com/feed/update/urn:li:activity:7312742011252490240/)
- [Zero to ASIC Course 2024 Highlights](https://www.zerotoasiccourse.com/post/year_update_2024/#2024-highlights)
- [PCB Design](https://github.com/splinedrive/gf180mcu-kianv-pcb)
- [ASIC Design](https://github.com/splinedrive/gf180mcu-kianv-rv32ima-sv32)
