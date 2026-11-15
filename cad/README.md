# Bobbin CAD

Frame: x forward, y left, z up, millimetres, origin on the floor under the axle.

- `bobbin.py`: parametric model. The molded parts are true solids (walls, ribs, bosses, pockets); bought parts are datasheet envelopes.
- `parts.py`: part catalogue used by the viewer and reports.
- `export.py`: writes `step/*.step` (one per molded tool + `bobbin_assembly.step` with every part), `stl/*.stl` (ASCII, watertight,
  ready to print), `reports/*.json` and `../site/assets/bobbin.gltf` + `robot_info.json`.
- `bom.py`: writes `../BOM.md` and `../site/assets/bom.json`.

| File | Part |
|---|---|
| bobbin_face_shell | front body shell (T1) |
| bobbin_drive_shell | rear body shell (T2) |
| bobbin_spool_wheel | wheel, print/mold 2 |
| bobbin_face_lens | clear lens (T4) |
| bobbin_tail_tpu | TPU tail (T5) |
| bobbin_dock | charging dock (T6) |
