# Bobbin: design for manufacture, assembly, and prototyping

## Part list (plastic)
| Part | Tool | Material | Mass | Notes |
|---|---|---|---:|---|
| Face shell | T1 | ABS/PC | 30.4 g | Lens pocket, eye + mouth windows, brow visor, PCB rails, front motor saddles, screw pilots |
| Drive shell | T2 | ABS/PC (charcoal) | 42.0 g | Motor + cell cradle ribs, speaker grille, tail socket, belly pad pockets, switch slot, counterbores |
| Spool wheel x2 | T3 (2-cavity) | ABS (terracotta) | 31.5 g each | Same part both sides; O-ring groove; D-bore press fit |
| Face lens | T4 | PMMA/PC, IMD mask | 1.9 g | One clear part for eye and mouth windows |
| Tail | T5 | TPU 85A | 5.2 g | T-anchor snaps into T2 |
| Dock | T6 | ABS | 38.7 g | Pogo bosses, fiducial recess, USB-C pocket, cored underside |

Bought mechanical parts: 2 stock 95 x 3.5 mm O-rings (tyres), 4 M2 x 8 PT screws, cell contacts, 2 belly pads, 2 pogo pins.

## Molding rules used in the CAD
- **Parting at the axle plane (x = 0).** Both body shells open straight along x: no side actions or lifters. Side axle holes
  sit on the parting line, so they're formed by both halves.
- **2.0 mm nominal wall**, ribs 1.6 mm (0.8 x wall) to avoid sink, bosses 6 mm OD with 1.15 mm pilot holes for M2 PT screws.
- **Wheels cored out** from the inside to about 2.2 mm walls with 6 radial ribs; the outer flange dimples hide ejector pins.
- **Draft**: the CAD is modelled at 0 deg draft for clarity; apply 1-1.5 deg on all pulled faces in the tooling model (open item).
- **Lens** is in-mold decorated (printed black mask inside) so only the eye and the mouth bar show. That removes a separate bezel.
- **Tooling estimate**: about $55-65k for T1-T6 in P20 steel (single cavity, T3 2-cavity), about 6-8 weeks. That's amortised at
  $1.20 per unit over 50k units in the BOM. Get real quotes before you rely on it.

## Assembly (target about 7 minutes, no glue except the speaker)
1. **Drive shell:** snap the 18650 into the cradle contacts, then drop both N20 motors into their rib saddles, shafts out through the side holes.
2. Press the **TPU tail** T-anchor into its slot from inside. Stick the speaker over the grille (foam gasket + PSA).
3. **Face shell:** slide the main board (tested at the EMS supplier) into the rails, seat the round display in its pocket, then fit the camera behind the mouth and the sensor flex (ToF + 2 cliff sensors).
4. Plug the motor, cell and speaker leads into the board, close the shells on the axle plane and drive **4 M2 screws** from the back.
5. Press a **wheel** onto each D-shaft and roll an **O-ring** into each groove.
6. End-of-line test on the dock pogo pins: charge current, motors both ways, encoders, IMU, camera frame, mic level, ToF, cliff sensors and touch. Firmware goes on over the air.

## Prototype (3D printed)
- Print the STLs in `cad/stl/` as they are; it's the same CAD as the molded parts.
  - **Face shell:** face down, with tree supports under the visor.
  - **Drive shell:** open side down.
  - **Wheels:** outer face down, no supports.
  - **Tail:** TPU, flat.
  - **Lens:** clear PETG, or laser-cut 1.2 mm acrylic.
- PETG, 0.2 mm layers, 3 walls, 15 % gyroid infill. A full set uses about 210 g of PETG and 6 g of TPU.
- The prototype BOM swaps the custom board for breakouts: a XIAO ESP32S3 Sense (camera + mic), a GC9A01 module, a DRV8833, a VL53L0X, an IMU, a MAX98357A and a TP4056 USB-C charger. Fit these to the same mounting envelopes with hot glue and double-sided tape.

## Known open items
- Add draft and real gate/ejector locations with the toolmaker; run a moldflow on the wheels (thick rim).
- Pendulum margin is small: the body CoM is 7.8 mm below the axle. Firmware needs IMU pitch control for hard braking, or move the cell lower in v0.2.
- The tail carries only about 8.2 g statically. Check it keeps the body from rocking forward on carpet.
- Mic acoustic path, antenna keep-out next to the display, and ESD on the belly pads all still need a board layout.
- Cell safety: buy UN38.3-certified cells; add an NTC to the charger for production.
