# Bobbin: the pet robot that rolls on its own sides

**[Open the 3D viewer](https://wjb000.github.io/bobbin-spoolbot/)**: every part, layers, labels, X-ray, explode, standard views, click for info.

Bobbin is an autonomous home pet robot designed to sell for **under $99**. It is shaped like a spool: the body is the core
and the two big wheels are the flanges, so the wheels *are* the sides of the robot. The battery hangs below the axle as a
pendulum, which keeps the face upright and lets Bobbin nod, lean and wobble with only its two drive motors. A soft TPU tail
is the third foot.

| | |
|---|---|
| Size | 102 mm wide x 106 mm tall x 142 mm long (with tail) |
| Mass | 244 g (CAD estimate) |
| Plastic parts | 6 robot parts from 5 tools (face shell, drive shell, 2 identical wheels, lens, TPU tail) + 1 dock tool |
| Fasteners | 4 x M2 thread-forming screws |
| Motors | 2 x N20 gear motor with hall encoder (no servos) |
| Brain | ESP32-S3 (Wi-Fi + BLE, 8 MB PSRAM) |
| Senses | 2 MP camera, ToF range, 2 cliff sensors, 6-axis IMU, MEMS mic, capacitive "pet me" pad |
| Face | 1.28" round IPS eye + 20 mm speaker |
| Power | 1 x 18650 cell, belly pads + self-docking charger |
| **Volume BOM** | **$28.88** at 10k units, incl. dock, cable, box, labour, tooling, 10% contingency ([BOM.md](BOM.md)) |
| **Prototype BOM** | **$56.41** for one 3D-printed unit ([BOM.md](BOM.md)) |

## What it does
- **Home patrol**: roams while you're out; snapshot to your phone on a person, a pet, a smoke alarm, glass breaking or barking.
- **Pet sitter**: finds the dog or cat, plays chase, shows you how they're doing.
- **Follow + greet**: meets you at the door, follows you room to room.
- **Timers, reminders, clock**: on its eye, out loud, and it comes to find you.
- **Self-docking**: homes on a printed fiducial on the dock with the camera, final 10 cm with the ToF.
- **Pet it**: a touch pad inside the crown; it purrs, wiggles and blinks.

## Repo
- `site/`: the GitHub Pages viewer (three.js, no build step). `site/assets/bobbin.gltf` is generated.
- `cad/bobbin.py`: parametric CadQuery model (every dimension is a named parameter at the top).
- `cad/parts.py`: part catalogue (layers, labels, info text, masses).
- `cad/export.py`: builds STEP + ASCII STL per molded part, the assembly STEP, interference + mass reports and the viewer model.
- `cad/bom.py`: single source for [BOM.md](BOM.md) and the viewer's BOM tab.
- `cad/step/`, `cad/stl/`: generated CAD. `cad/reports/`: interference, mass and stability.
- [DFM.md](DFM.md): molding notes, assembly steps, printing the prototype.

Rebuild: `pip install cadquery trimesh manifold3d scipy && cd cad && python export.py && python bom.py`.

## Checks the CAD passes today
- Zero unexpected interferences in the home pose (`cad/reports/interference.json`).
- Watertight STL for every molded part.
- Body centre of mass 7.8 mm below and 3.7 mm behind the axle, so it hangs face-up and rests on its tail (8.2 g static tail load).
- 9.0 mm belly clearance.

## Honest status
Design model only. Nothing has been printed, wired or driven. Bought parts are datasheet envelopes, not vendor CAD.
Volume prices marked *estimate* in BOM.md still need factory quotes. Firmware does not exist yet.
