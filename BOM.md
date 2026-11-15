# Bobbin bill of materials

Prices checked on **2026-11-14**. *verified* = the price was read from the linked page that day.
*estimate* = an engineering estimate for that volume; the link is where to get the real quote.
Nothing here has been quoted by a factory yet.

## Volume BOM (10k-unit run, landed at the contract manufacturer)

**Total: $28.88 per robot, dock and packaging included.** Target retail: under $99.

| Item | Qty | Unit @10k | Line | Price source | Status | Note |
|---|---:|---:|---:|---|---|---|
| ESP32-S3-WROOM-1-N8R8 module | 1 | $3.48 | $3.48 | [LCSC C2913201, 1,300+ break](https://www.lcsc.com/product-detail/C2913201.html) | verified | brain, Wi-Fi/BLE, 8 MB PSRAM |
| GC9A01 1.28" round IPS 240x240 panel | 1 | $1.86 | $1.86 | [Alibaba wholesale listings $1.62-2.03](https://electronics.alibaba.com/product/gc9a01-display) | verified | the eye |
| OV2640 2 MP camera, 120 deg, 24-pin FPC | 1 | $2.40 | $2.40 | [AliExpress single-unit $4.07-6.93](https://alitools.io/en/showcase/2mp-fpc-ov2640-camera-module-robot-fish-eye-lens-normal-lens-lengthened-fisheye-lens-lengthened-normal-lens-33051369006) | estimate | volume quote needed |
| N20 6 V 1:150 gear motor + 7 PPR hall encoder | 2 | $1.90 | $3.80 | [AliExpress single-unit $3.95-4.41](https://alitools.io/en/showcase/dc-3v-6v-12v-encoder-motor-gear-n20-electric-micro-gear-motor-with-43mm-wheel-screws-mounting-bracket-coupling-kit-32926152520) | estimate | factory quote needed |
| DRV8833PWPR dual H-bridge | 1 | $1.01 | $1.01 | [LCSC C50506, 1,000+ break](https://www.lcsc.com/product-detail/C50506.html) | verified | a $0.15 clone driver would save $0.85 |
| QMI8658C 6-axis IMU | 1 | $0.74 | $0.74 | [LCSC C2842151](https://www.lcsc.com/product-detail/C2842151.html) | verified | was out of stock at LCSC on check |
| VL53L0CXV0DH/1 time-of-flight sensor | 1 | $1.62 | $1.62 | [LCSC C91199, 1,000+ break](https://www.lcsc.com/product-detail/C91199.html) | verified |  |
| ITR8307 IR reflective cliff sensor | 2 | $0.12 | $0.24 | [LCSC search](https://www.lcsc.com/search?q=ITR8307) | estimate |  |
| I2S MEMS microphone (MSM261S4030H0R class) | 1 | $0.45 | $0.45 | [LCSC search](https://www.lcsc.com/search?q=MSM261S4030H0R) | estimate |  |
| NS4168 I2S class-D amp | 1 | $0.12 | $0.12 | [LCSC search](https://www.lcsc.com/search?q=NS4168) | estimate |  |
| 20 mm 8 ohm 1 W speaker | 1 | $0.35 | $0.35 | [LCSC search](https://www.lcsc.com/search?q=20mm%20speaker) | estimate |  |
| 18650 2000 mAh grade-A Li-ion cell | 1 | $1.05 | $1.05 | [Made-in-China, $0.50-1.05 at 3,000+](https://howellenergy.en.made-in-china.com/product/YZkmpXIlaRVt/China-Bis-Approved-Rechargeable-18650-Battery-2000mAh-2200mAh-2600mAh-3-7V-Li-ion-Lithium-Battery-Cell.html) | verified | buy UN38.3-certified cells |
| Charger + protection + 3.3 V buck (TP4056-class, DW01A, FS8205) | 1 | $0.35 | $0.35 | [TP4056 $0.03-0.08 at LCSC; rest est.](https://www.lcsc.com/search?q=TP4056) | estimate |  |
| Main PCB 2-layer 62 x 44 mm + passives + connectors | 1 | $1.40 | $1.40 | [quote at JLCPCB/LCSC](https://jlcpcb.com/quote) | estimate |  |
| SMT assembly + board test | 1 | $1.20 | $1.20 | [EMS quote](https://jlcpcb.com/smt-assembly) | estimate |  |
| Sensor flex (FPC) for ToF + cliff sensors | 1 | $0.30 | $0.30 | [FPC quote](https://jlcpcb.com/flex-pcb) | estimate |  |
| Molded plastics: face shell, drive shell, 2 wheels, IMD lens, TPU tail (145 g) | 1 | $1.20 | $1.20 | [resin ~$2.6/kg + cycle cost](https://www.plasticsnews.com/resin-pricing) | estimate | see DFM.md |
| Stock O-ring 95 x 3.5 mm (tyre) | 2 | $0.04 | $0.08 | [bulk NBR O-rings](https://www.aliexpress.com/w/wholesale-o-ring-95x3.5.html) | estimate |  |
| Touch foil, belly charge pads, cell contacts | 1 | $0.15 | $0.15 | [stamped parts](https://www.lcsc.com/search?q=18650%20battery%20contact) | estimate |  |
| M2 x 8 PT thread-forming screw | 4 | $0.01 | $0.04 | [bulk fasteners](https://www.aliexpress.com/w/wholesale-m2-pt-screw.html) | estimate |  |
| Dock: molded base + 2 pogo pins + USB-C board + fiducial label + feet | 1 | $1.25 | $1.25 | [molded 39 g + parts](https://www.lcsc.com/search?q=pogo%20pin) | estimate |  |
| USB-A to USB-C cable (no wall adapter) | 1 | $0.45 | $0.45 | [bulk cable](https://www.alibaba.com/showroom/usb-c-cable.html) | estimate |  |
| Retail box, pulp insert, quick-start card | 1 | $0.90 | $0.90 | [packaging quote](https://www.alibaba.com/showroom/pulp-packaging.html) | estimate |  |
| Final assembly (~7 min) + end-of-line test | 1 | $1.10 | $1.10 | CM labour estimate | estimate |  |
| Tooling amortisation (~$60k of tools over 50k units) | 1 | $1.20 | $1.20 | tooling estimate | estimate | see DFM.md |
| Certification amortisation (FCC/CE/UN38.3 on a pre-certified module) | 1 | $0.40 | $0.40 | estimate | estimate |  |
| Contingency: 10% on every estimated line | 1 | $1.74 | $1.74 | until factory quotes are in | estimate |  |
| **Total** | | | **$28.88** | | | |

## Prototype BOM (one hand-built unit, 3D printed)

**Total: $56.41** (before shipping and tax).

| Item | Qty | Unit @1 | Line | Price source | Status | Note |
|---|---:|---:|---:|---|---|---|
| Seeed XIAO ESP32S3 Sense (ESP32-S3 + OV2640 camera + mic) | 1 | $13.99 | $13.99 | [Seeed Studio](https://www.seeedstudio.com/XIAO-ESP32S3-Sense-p-5639.html) | verified | replaces module + camera + mic |
| 1.28" GC9A01 round LCD module | 1 | $8.60 | $8.60 | [Elecrow](https://www.elecrow.com/1-28-inch-round-lcd-module-gc9a01-240x240-lcd-display.html) | verified |  |
| N20 6 V encoder gear motor (150 rpm) | 2 | $4.41 | $8.82 | [AliExpress (via Alitools)](https://alitools.io/en/showcase/dc-3v-6v-12v-encoder-motor-gear-n20-electric-micro-gear-motor-with-43mm-wheel-screws-mounting-bracket-coupling-kit-32926152520) | verified | top of $3.95-4.41 range |
| DRV8833 breakout | 1 | $1.50 | $1.50 | [AliExpress search](https://www.aliexpress.com/w/wholesale-drv8833-module.html) | estimate |  |
| VL53L0X ToF breakout | 1 | $2.50 | $2.50 | [AliExpress search](https://www.aliexpress.com/w/wholesale-vl53l0x.html) | estimate |  |
| 6-axis IMU breakout (QMI8658 / MPU-6050) | 1 | $2.00 | $2.00 | [AliExpress search](https://www.aliexpress.com/w/wholesale-gy-521.html) | estimate |  |
| MAX98357A I2S amp breakout | 1 | $2.00 | $2.00 | [AliExpress search](https://www.aliexpress.com/w/wholesale-max98357a.html) | estimate | Adafruit #3006 if you want US stock |
| 20 mm speaker | 1 | $1.50 | $1.50 | [AliExpress search](https://www.aliexpress.com/w/wholesale-20mm-speaker-8ohm.html) | estimate |  |
| 18650 cell (name-brand) + TP4056 USB-C protected charger board | 1 | $5.50 | $5.50 | [local / AliExpress](https://www.aliexpress.com/w/wholesale-tp4056-type-c.html) | estimate |  |
| TCRT5000 / ITR8307 cliff sensors | 2 | $0.50 | $1.00 | [AliExpress search](https://www.aliexpress.com/w/wholesale-tcrt5000.html) | estimate |  |
| PETG filament for shells, wheels, dock (~210 g) | 1 | $4.20 | $4.20 | [$20/kg spool](https://www.amazon.com/s?k=petg+filament) | estimate |  |
| TPU 85A-95A filament for the tail (~6 g) | 1 | $0.30 | $0.30 | [$25/kg spool](https://www.amazon.com/s?k=tpu+filament) | estimate |  |
| Clear PETG / acrylic sheet for the lens | 1 | $0.50 | $0.50 | offcut | estimate | or print in clear PETG |
| 95 x 3.5 mm O-rings | 2 | $0.50 | $1.00 | [O-ring assortment](https://www.amazon.com/s?k=95mm+x+3.5mm+o-ring) | estimate |  |
| Pogo pins, copper tape, M2 screws, wire, perfboard | 1 | $3.00 | $3.00 | hardware bin | estimate |  |
| **Total** | | | **$56.41** | | | |

## Where the money goes (volume)

- Brain + eye + camera: $7.74 of $28.88. This is what makes it a pet with a face that sees you.
- Motion (2 encoder motors, driver, tyres): $4.89.
- Plastics are cheap ($1.20); labour, tooling, test and packaging ($3.60) matter more.

## Cost-down levers already identified

- Clone dual H-bridge (RZ7899 class, ~$0.15) instead of DRV8833: -$0.85.
- Plain N20 + one shared optical encoder disc molded into the wheel: about -$1.00.
- ESP32-S3 bare chip + flash/PSRAM on our own board instead of the module: about -$0.80, but adds RF certification cost.
