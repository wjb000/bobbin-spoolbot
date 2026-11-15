"""Single source for both BOMs -> ../BOM.md and ../site/assets/bom.json.
status: 'verified' = price read from the linked page on 2026-11-14; 'estimate' = engineering estimate
for that volume (the link is where to quote it)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = 'verified'; E = 'estimate'
LCSC = 'https://www.lcsc.com/search?q='
VOLUME = [  # (item, qty, unit USD @10k, status, source name, link, note)
    ('ESP32-S3-WROOM-1-N8R8 module', 1, 3.48, V, 'LCSC C2913201, 1,300+ break', 'https://www.lcsc.com/product-detail/C2913201.html', 'brain, Wi-Fi/BLE, 8 MB PSRAM'),
    ('GC9A01 1.28" round IPS 240x240 panel', 1, 1.86, V, 'Alibaba wholesale listings $1.62-2.03', 'https://electronics.alibaba.com/product/gc9a01-display', 'the eye'),
    ('OV2640 2 MP camera, 120 deg, 24-pin FPC', 1, 2.40, E, 'AliExpress single-unit $4.07-6.93', 'https://alitools.io/en/showcase/2mp-fpc-ov2640-camera-module-robot-fish-eye-lens-normal-lens-lengthened-fisheye-lens-lengthened-normal-lens-33051369006', 'volume quote needed'),
    ('N20 6 V 1:150 gear motor + 7 PPR hall encoder', 2, 1.90, E, 'AliExpress single-unit $3.95-4.41', 'https://alitools.io/en/showcase/dc-3v-6v-12v-encoder-motor-gear-n20-electric-micro-gear-motor-with-43mm-wheel-screws-mounting-bracket-coupling-kit-32926152520', 'factory quote needed'),
    ('DRV8833PWPR dual H-bridge', 1, 1.01, V, 'LCSC C50506, 1,000+ break', 'https://www.lcsc.com/product-detail/C50506.html', 'a $0.15 clone driver would save $0.85'),
    ('QMI8658C 6-axis IMU', 1, 0.74, V, 'LCSC C2842151', 'https://www.lcsc.com/product-detail/C2842151.html', 'was out of stock at LCSC on check'),
    ('VL53L0CXV0DH/1 time-of-flight sensor', 1, 1.62, V, 'LCSC C91199, 1,000+ break', 'https://www.lcsc.com/product-detail/C91199.html', ''),
    ('ITR8307 IR reflective cliff sensor', 2, 0.12, E, 'LCSC search', LCSC + 'ITR8307', ''),
    ('I2S MEMS microphone (MSM261S4030H0R class)', 1, 0.45, E, 'LCSC search', LCSC + 'MSM261S4030H0R', ''),
    ('NS4168 I2S class-D amp', 1, 0.12, E, 'LCSC search', LCSC + 'NS4168', ''),
    ('20 mm 8 ohm 1 W speaker', 1, 0.35, E, 'LCSC search', LCSC + '20mm%20speaker', ''),
    ('18650 2000 mAh grade-A Li-ion cell', 1, 1.05, V, 'Made-in-China, $0.50-1.05 at 3,000+', 'https://howellenergy.en.made-in-china.com/product/YZkmpXIlaRVt/China-Bis-Approved-Rechargeable-18650-Battery-2000mAh-2200mAh-2600mAh-3-7V-Li-ion-Lithium-Battery-Cell.html', 'buy UN38.3-certified cells'),
    ('Charger + protection + 3.3 V buck (TP4056-class, DW01A, FS8205)', 1, 0.35, E, 'TP4056 $0.03-0.08 at LCSC; rest est.', LCSC + 'TP4056', ''),
    ('Main PCB 2-layer 62 x 44 mm + passives + connectors', 1, 1.40, E, 'quote at JLCPCB/LCSC', 'https://jlcpcb.com/quote', ''),
    ('SMT assembly + board test', 1, 1.20, E, 'EMS quote', 'https://jlcpcb.com/smt-assembly', ''),
    ('Sensor flex (FPC) for ToF + cliff sensors', 1, 0.30, E, 'FPC quote', 'https://jlcpcb.com/flex-pcb', ''),
    ('Molded plastics: face shell, drive shell, 2 wheels, IMD lens, TPU tail (145 g)', 1, 1.20, E, 'resin ~$2.6/kg + cycle cost', 'https://www.plasticsnews.com/resin-pricing', 'see DFM.md'),
    ('Stock O-ring 95 x 3.5 mm (tyre)', 2, 0.04, E, 'bulk NBR O-rings', 'https://www.aliexpress.com/w/wholesale-o-ring-95x3.5.html', ''),
    ('Touch foil, belly charge pads, cell contacts', 1, 0.15, E, 'stamped parts', LCSC + '18650%20battery%20contact', ''),
    ('M2 x 8 PT thread-forming screw', 4, 0.01, E, 'bulk fasteners', 'https://www.aliexpress.com/w/wholesale-m2-pt-screw.html', ''),
    ('Dock: molded base + 2 pogo pins + USB-C board + fiducial label + feet', 1, 1.25, E, 'molded 39 g + parts', LCSC + 'pogo%20pin', ''),
    ('USB-A to USB-C cable (no wall adapter)', 1, 0.45, E, 'bulk cable', 'https://www.alibaba.com/showroom/usb-c-cable.html', ''),
    ('Retail box, pulp insert, quick-start card', 1, 0.90, E, 'packaging quote', 'https://www.alibaba.com/showroom/pulp-packaging.html', ''),
    ('Final assembly (~7 min) + end-of-line test', 1, 1.10, E, 'CM labour estimate', '', ''),
    ('Tooling amortisation (~$60k of tools over 50k units)', 1, 1.20, E, 'tooling estimate', '', 'see DFM.md'),
    ('Certification amortisation (FCC/CE/UN38.3 on a pre-certified module)', 1, 0.40, E, 'estimate', '', ''),
]
_est = round(0.10 * sum(q * u for _, q, u, st, *_ in VOLUME if st == 'estimate'), 2)
VOLUME.append(('Contingency: 10% on every estimated line', 1, _est, E, 'until factory quotes are in', '', ''))
PROTO = [  # (item, qty, unit USD @qty 1, status, source, link, note)
    ('Seeed XIAO ESP32S3 Sense (ESP32-S3 + OV2640 camera + mic)', 1, 13.99, V, 'Seeed Studio', 'https://www.seeedstudio.com/XIAO-ESP32S3-Sense-p-5639.html', 'replaces module + camera + mic'),
    ('1.28" GC9A01 round LCD module', 1, 8.60, V, 'Elecrow', 'https://www.elecrow.com/1-28-inch-round-lcd-module-gc9a01-240x240-lcd-display.html', ''),
    ('N20 6 V encoder gear motor (150 rpm)', 2, 4.41, V, 'AliExpress (via Alitools)', 'https://alitools.io/en/showcase/dc-3v-6v-12v-encoder-motor-gear-n20-electric-micro-gear-motor-with-43mm-wheel-screws-mounting-bracket-coupling-kit-32926152520', 'top of $3.95-4.41 range'),
    ('DRV8833 breakout', 1, 1.50, E, 'AliExpress search', 'https://www.aliexpress.com/w/wholesale-drv8833-module.html', ''),
    ('VL53L0X ToF breakout', 1, 2.50, E, 'AliExpress search', 'https://www.aliexpress.com/w/wholesale-vl53l0x.html', ''),
    ('6-axis IMU breakout (QMI8658 / MPU-6050)', 1, 2.00, E, 'AliExpress search', 'https://www.aliexpress.com/w/wholesale-gy-521.html', ''),
    ('MAX98357A I2S amp breakout', 1, 2.00, E, 'AliExpress search', 'https://www.aliexpress.com/w/wholesale-max98357a.html', 'Adafruit #3006 if you want US stock'),
    ('20 mm speaker', 1, 1.50, E, 'AliExpress search', 'https://www.aliexpress.com/w/wholesale-20mm-speaker-8ohm.html', ''),
    ('18650 cell (name-brand) + TP4056 USB-C protected charger board', 1, 5.50, E, 'local / AliExpress', 'https://www.aliexpress.com/w/wholesale-tp4056-type-c.html', ''),
    ('TCRT5000 / ITR8307 cliff sensors', 2, 0.50, E, 'AliExpress search', 'https://www.aliexpress.com/w/wholesale-tcrt5000.html', ''),
    ('PETG filament for shells, wheels, dock (~210 g)', 1, 4.20, E, '$20/kg spool', 'https://www.amazon.com/s?k=petg+filament', ''),
    ('TPU 85A-95A filament for the tail (~6 g)', 1, 0.30, E, '$25/kg spool', 'https://www.amazon.com/s?k=tpu+filament', ''),
    ('Clear PETG / acrylic sheet for the lens', 1, 0.50, E, 'offcut', '', 'or print in clear PETG'),
    ('95 x 3.5 mm O-rings', 2, 0.50, E, 'O-ring assortment', 'https://www.amazon.com/s?k=95mm+x+3.5mm+o-ring', ''),
    ('Pogo pins, copper tape, M2 screws, wire, perfboard', 1, 3.00, E, 'hardware bin', '', ''),
]

def tot(rows):
    return round(sum(q * u for _, q, u, *_ in rows), 2)

def table(rows, unit_hdr):
    L = [f'| Item | Qty | {unit_hdr} | Line | Price source | Status | Note |', '|---|---:|---:|---:|---|---|---|']
    for it, q, u, st, src, link, note in rows:
        s = f'[{src}]({link})' if link else src
        L.append(f'| {it} | {q} | ${u:.2f} | ${q * u:.2f} | {s} | {st} | {note} |')
    L.append(f'| **Total** | | | **${tot(rows):.2f}** | | | |')
    return '\n'.join(L)

if __name__ == '__main__':
    tv, tp = tot(VOLUME), tot(PROTO)
    md = f"""# Bobbin bill of materials

Prices checked on **2026-11-14**. *verified* = the price was read from the linked page that day.
*estimate* = an engineering estimate for that volume; the link is where to get the real quote.
Nothing here has been quoted by a factory yet.

## Volume BOM (10k-unit run, landed at the contract manufacturer)

**Total: ${tv:.2f} per robot, dock and packaging included.** Target retail: under $99.

{table(VOLUME, 'Unit @10k')}

## Prototype BOM (one hand-built unit, 3D printed)

**Total: ${tp:.2f}** (before shipping and tax).

{table(PROTO, 'Unit @1')}

## Where the money goes (volume)

- Brain + eye + camera: ${3.48 + 1.86 + 2.40:.2f} of ${tv:.2f}. This is what makes it a pet with a face that sees you.
- Motion (2 encoder motors, driver, tyres): ${2 * 1.90 + 1.01 + 0.08:.2f}.
- Plastics are cheap (${1.20:.2f}); labour, tooling, test and packaging (${0.90 + 1.10 + 1.20 + 0.40:.2f}) matter more.

## Cost-down levers already identified

- Clone dual H-bridge (RZ7899 class, ~$0.15) instead of DRV8833: -$0.85.
- Plain N20 + one shared optical encoder disc molded into the wheel: about -$1.00.
- ESP32-S3 bare chip + flash/PSRAM on our own board instead of the module: about -$0.80, but adds RF certification cost.
"""
    open(os.path.join(ROOT, 'BOM.md'), 'w').write(md)
    json.dump(dict(volume_total=tv, proto_total=tp, checked='2026-11-14',
                   volume=[dict(item=i, qty=q, unit=u, status=s) for i, q, u, s, *_ in VOLUME],
                   proto=[dict(item=i, qty=q, unit=u, status=s) for i, q, u, s, *_ in PROTO]),
              open(os.path.join(ROOT, 'site', 'assets', 'bom.json'), 'w'), indent=1)
    print(tv, tp)
