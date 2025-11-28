
|--------------------|----------------------------------------|----------------------------------|-------------------------------------|--------------------------------------|
| Feature Group      | Feature Name                           | Model Name                       | Mask #                              | GDS Layer #                          |
|--------------------|----------------------------------------|----------------------------------|-------------------------------------|--------------------------------------|
| Always Included    | Base features for 0.18u MCU            |                                  | 10,05,18,38,60,61,11,64,65,70,68,75 | 22,21,204,55,30,47,15,10,32,31,49,33 |
|--------------------|----------------------------------------|----------------------------------|-------------------------------------|--------------------------------------|
| Metal stack 5LM    | Top Metal Thickness 11kÅ, 5-layers     |                                  | 80,85,88,91,93,94,96,97,98          | 34,35,36,38,42,40,46,41,53           |
|--------------------|----------------------------------------|----------------------------------|-------------------------------------|--------------------------------------|
| Diode              | 5V/6V N+/LPWELL Diode (Outside DNWELL) | `np_6p0`                         |                                     |                                      |
| Diode              | 5V/6V P+/Nwell Diode (Outside DNWELL)  | `pn_6p0`                         |                                     |                                      |
|--------------------|----------------------------------------|----------------------------------|-------------------------------------|--------------------------------------|
| MOSFET             | 5V NMOS (Outside DNWELL)               | `nmos_5p0`                       |                                     |                                      |
| MOSFET             | 5V NMOS (Inside DNWELL)                | `nmos_5p0_dw`                    | 06                                  | 12                                   |
| MOSFET             | 5V PMOS (Outside DNWELL)               | `pmos_5p0`                       |                                     |                                      |
| MOSFET             | 5V PMOS (Inside DNWELL)                | `pmos_5p0_dw`                    | 06                                  | 12                                   |
|--------------------|----------------------------------------|----------------------------------|-------------------------------------|--------------------------------------|
| ESD (SAB MOSFET)   | 5V SAB NMOS (Outside DNWELL)           | `nmos_5p0_sab`                   |                                     |                                      |
| ESD (SAB MOSFET)   | 5V SAB NMOS (Inside DNWELL)            | `nmos_5p0_dw_sab`                | 06                                  | 12                                   |
| ESD (SAB MOSFET)   | 5V SAB PMOS (Outside DNWELL)           | `pmos_5p0_sab`                   |                                     |                                      |
| ESD (SAB MOSFET)   | 5V SAB PMOS (Inside DNWELL)            | `pmos_5p0_dw_sab`                | 06                                  | 12                                   |
|--------------------|----------------------------------------|----------------------------------|-------------------------------------|--------------------------------------|
| RESISTOR           | N+ Poly Unsalicided Rs                 | `npolyf_u`                       |                                     |                                      |
| RESISTOR           | P+ Poly Unsalicided Rs                 | `ppolyf_u`                       |                                     |                                      |
| Resistor (HRES)    | 1K P+ HRS                              | `ppolyf_u_1k`, `ppolyf_u_1k_6p0` | 63                                  | 62                                   |
|--------------------|----------------------------------------|----------------------------------|-------------------------------------|--------------------------------------|
| CAPACITOR (MOS)    | 5V/6V NMOS capacitor (Outside DNWELL)  | `nmoscap_6p0`                    |                                     |                                      |
|--------------------|----------------------------------------|----------------------------------|-------------------------------------|--------------------------------------|
| MIM Capacitor      | Type B (Plate between n-1) TM / TM     |                                  |                                     |                                      |
| MIM Capacitor      | 2.0fF/um2 MIM capacitor                | `mim_single_2p0fF`               | 92                                  | 75                                   |
|--------------------|----------------------------------------|----------------------------------|-------------------------------------|--------------------------------------|
| Passivation        | Single passivation                     | `Single_passivation`             | 95                                  | 37                                   |
|--------------------|----------------------------------------|----------------------------------|-------------------------------------|--------------------------------------|


|--------|----------------------------|---------------------------------------------|-------------|
| Mask # | Layer Name (GF180MCU)      | Used By Feature Group(s)                    | GDS Layer # |
|--------|----------------------------|---------------------------------------------|-------------|
| 05     | NWELL                      | Always Included                             | 21          |
| 06     | DNWELL (Deep N-well)       | MOSFET (Inside DNWELL), ESD (Inside DNWELL) | 12          |
| 10     | COMP                       | Always Included                             | 22          |
| 11     | AD (Planarization Aid)     | Always Included                             | 15          |
| 18     | LVPWELL                    | Always Included                             | 204         |
| 38     | DualGate                   | Always Included                             | 55          |
| 60     | POLY2                      | Always Included                             | 30          |
| 61     | TN (NMOS implant)          | Always Included                             | 47          |
| 63     | Resistor layer             | Resistor (HRES)                             | 62          |
| 64     | TP (PMOS implant)          | Always Included                             | 10          |
| 65     | N+ implant                 | Always Included                             | 32          |
| 68     | SAB (Salicide block)       | Always Included, ESD (SAB MOSFET)           | 49          |
| 70     | P+ implant                 | Always Included                             | 31          |
| 75     | Contact                    | Always Included                             | 33          |
| 80     | Metal1                     | Metal stack 5LM                             | 34          |
| 85     | Via1                       | Metal stack 5LM                             | 35          |
| 88     | Metal2                     | Metal stack 5LM                             | 36          |
| 91     | Via2                       | Metal stack 5LM                             | 38          |
| 93     | Metal3                     | Metal stack 5LM                             | 42          |
| 94     | Via3                       | Metal stack 5LM                             | 40          |
| 96     | Metal4                     | Metal stack 5LM                             | 46          |
| 97     | Via4                       | Metal stack 5LM                             | 41          |
| 98     | MetalTop                   | Metal stack 5LM                             | —           |
| 92     | MIM Top Plate              | MIM Capacitor (2.0 fF/µm²)                  | 75          |
| 95     | Pad / Passivation          | Passivation                                 | 37          |
|--------|----------------------------|---------------------------------------------|-------------|

Unused Layers

|--------|-------------|----------------------------|-------------|--------------------|--------------------------------|
| Mask # | Layer Name  | Description                | GDS Layer # | Optional (per PDK) | Notes                          |
|--------|-------------|----------------------------|-------------|--------------------|--------------------------------|
| 1L     | MVNVT       | 5V or 6V NLDD              | 205         | No                 | High-voltage NMOS LDD implant  |
| 2E     | MVPVT       | MTP Cell Implant           | 206         | No                 | For OTP / MTP cells            |
| 67     | ESD         | ESD implant                | 24          | Yes                | Dedicated ESD implant layer    |
| 9Z     | POLYFUSE    | POLY FUSE Window           | 220         | Yes                | Poly fuse mask                 |
|--------|-------------|----------------------------|-------------|--------------------|--------------------------------|
| 9E     | Metal5      | Metal5                     | 81          | No                 | Extra metal layer above M4     |
| 9D     | Via5        | Via5                       | 82          | No                 | Via between Metal4 and Metal5  |
|--------|-------------|----------------------------|-------------|--------------------|--------------------------------|
| 99     | PIB         | Bond / Passivation opening | 50          | Yes                | Bond & passivation openings    |
| 9A     | FuseWindow  | Metal FuseWindow (Optional)| 96          | Yes                | Metal fuse window              |
|--------|-------------|----------------------------|-------------|--------------------|--------------------------------|

