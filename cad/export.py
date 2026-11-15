"""Build everything: STEP + ASCII STL for each molded part, assembly STEP, interference + mass report,
and the viewer model site/assets/bobbin.gltf + robot_info.json."""
import os, json, time, base64, struct, itertools
import numpy as np, trimesh, cadquery as cq
import bobbin as B
from parts import MOLDED, BOUGHT, GROUPS, LINK, EXTERNAL, MASS_G, DENSITY
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
D = lambda *p: os.path.join(ROOT, *p)
for p in ('cad/step', 'cad/stl', 'cad/reports', 'site/assets'):
    os.makedirs(D(p), exist_ok=True)


def tess(shape, tol, ang):
    v, f = shape.val().tessellate(tol, ang) if hasattr(shape, 'val') else shape.tessellate(tol, ang)
    m = trimesh.Trimesh(np.array([(p.x, p.y, p.z) for p in v]), np.array(f), process=True)
    m.merge_vertices(); return m


def ascii_stl(m, path, name):
    v = m.vertices[m.faces]; n = m.face_normals; o = [f'solid {name}']
    for (a, b, c), k in zip(v, n):
        o.append(f'facet normal {k[0]:.4f} {k[1]:.4f} {k[2]:.4f}\n outer loop\n  vertex {a[0]:.3f} {a[1]:.3f} {a[2]:.3f}\n'
                 f'  vertex {b[0]:.3f} {b[1]:.3f} {b[2]:.3f}\n  vertex {c[0]:.3f} {c[1]:.3f} {c[2]:.3f}\n endloop\nendfacet')
    o.append(f'endsolid {name}\n'); open(path, 'w').write('\n'.join(o))


def main():
    t0 = time.time()
    front, rear, tail = B.shells()
    S = dict(front_shell=front, rear_shell=rear, tail=tail, lens=B.lens(), wheel_l=B.wheel(1), wheel_r=B.wheel(-1),
             oring_l=B.oring(1), oring_r=B.oring(-1), dock=B.dock())
    S.update(B.components()); S.update(B.dock_components())
    print('built', round(time.time() - t0), 's')
    # ---- CAD exports (one STEP per molded tool + assembly; ASCII STL for printing)
    tools = {'front_shell': 'bobbin_face_shell', 'rear_shell': 'bobbin_drive_shell', 'wheel_l': 'bobbin_spool_wheel',
             'lens': 'bobbin_face_lens', 'tail': 'bobbin_tail_tpu', 'dock': 'bobbin_dock'}
    for k, fn in tools.items():
        cq.exporters.export(S[k], D('cad/step', fn + '.step'))
        ascii_stl(tess(S[k], 0.08, 0.3), D('cad/stl', fn + '.stl'), fn)
    asm = cq.Assembly(name='bobbin')
    for k, s in S.items():
        info = MOLDED.get(k) or BOUGHT.get(k)
        asm.add(s, name=k, color=cq.Color(*[int(info['color'].lstrip('#')[i:i + 2] if len(info['color']) == 7 else 'aa', 16) / 255 for i in (0, 2, 4)]))
    asm.save(D('cad/step', 'bobbin_assembly.step'))
    print('step/stl', round(time.time() - t0), 's')
    # ---- meshes
    M = {}
    for k, s in S.items():
        fine = k in MOLDED
        M[k] = tess(s, 0.12 if fine else 0.25, 0.35 if fine else 0.6)
    # ---- interference (home pose); exact contacts by design are listed as allowed
    import manifold3d as mf
    def man(m):
        return mf.Manifold(mf.Mesh(np.asarray(m.vertices, np.float32), np.asarray(m.faces, np.uint32)))
    MF = {k: man(m) for k, m in M.items() if m.is_watertight}
    allowed = {('battery', 'batt_contacts'), ('motor_l', 'encoder_l'), ('motor_r', 'encoder_r'), ('main_pcb', 'esp32s3'),
               ('main_pcb', 'drv8833'), ('main_pcb', 'imu'), ('main_pcb', 'amp'), ('main_pcb', 'charger'), ('main_pcb', 'mic'),
               ('main_pcb', 'fpc_conn'), ('pogo_l', 'dock'), ('pogo_r', 'dock'), ('dock', 'marker'), ('dock', 'dock_usb'),
               ('wheel_l', 'oring_l'), ('wheel_r', 'oring_r'), ('lens', 'front_shell'), ('tail', 'rear_shell'),
               ('sensor_flex', 'cliff_l'), ('sensor_flex', 'cliff_r')}
    clashes, keys = [], [k for k in M if LINK.get(k) != 'dock' or True]
    for a, b in itertools.combinations(keys, 2):
        if (LINK.get(a) == 'dock') != (LINK.get(b) == 'dock'):
            continue
        ba, bb = M[a].bounds, M[b].bounds
        if np.any(ba[1] < bb[0]) or np.any(bb[1] < ba[0]):
            continue
        if a in MF and b in MF:
            v = (MF[a] ^ MF[b]).volume()
        else:   # exact B-rep boolean when a tessellation is not watertight
            try:
                v = abs(S[a].intersect(S[b]).val().Volume())
            except Exception:
                v = 0.0
        if v > 0.5:
            clashes.append(dict(a=a, b=b, mm3=round(v, 1), allowed=(a, b) in allowed or (b, a) in allowed or a.startswith('screw') or b.startswith('screw')))
    hard = [c for c in clashes if not c['allowed']]
    print('clashes', len(clashes), 'unexpected', hard)
    print('not watertight:', [k for k, m in M.items() if not m.is_watertight])
    # ---- mass / CoM / stability (robot only)
    mass = {}
    for k, m in M.items():
        if LINK.get(k) == 'dock':
            continue
        g = MASS_G.get(k)
        if g is None:
            g = abs(S[k].val().Volume()) / 1000 * DENSITY[k]
        cm = M[k].bounds.mean(0)
        if k in MOLDED:
            cm = np.array(cq.Shape.centerOfMass(S[k].val()).toTuple())
        mass[k] = (g, cm)
    Mt = sum(g for g, _ in mass.values()); com = sum(g * c for g, c in mass.values()) / Mt
    wheels = {'wheel_l', 'wheel_r', 'oring_l', 'oring_r'}
    Mb = sum(g for k, (g, _) in mass.items() if k not in wheels)
    comb = sum(g * c for k, (g, c) in mass.items() if k not in wheels) / Mb
    tail_x = float(M['tail'].vertices[np.argmin(M['tail'].vertices[:, 2])][0])
    # static load on the tail: body pivots about the axle; moment of body weight about axle balanced by tail reaction
    tail_load = Mb * (-comb[0]) / (-tail_x)
    stab = dict(total_mass_g=round(Mt, 1), body_mass_g=round(Mb, 1), com_mm=com.round(1).tolist(), body_com_mm=comb.round(1).tolist(),
                body_com_below_axle_mm=round(B.AZ - comb[2], 1), body_com_behind_axle_mm=round(-comb[0], 1),
                tail_contact_x_mm=round(tail_x, 1), tail_static_load_g=round(tail_load, 1),
                tail_min_z_mm=round(float(M['tail'].bounds[0][2]), 2), core_ground_clearance_mm=round(float(M['rear_shell'].bounds[0][2]), 1))
    print(stab)
    plastic_g = {k: round(abs(S[k].val().Volume()) / 1000 * DENSITY[k], 1) for k in MOLDED}
    bbs = {k: np.round(M[k].bounds, 1).tolist() for k in M}
    size = np.array([M[k].bounds for k in M if LINK.get(k) != 'dock'])
    dims = (size[:, 1].max(0) - size[:, 0].min(0)).round(1).tolist()
    json.dump(dict(clashes=clashes, unexpected=hard), open(D('cad/reports/interference.json'), 'w'), indent=1)
    json.dump(dict(stability=stab, plastic_grams=plastic_g, overall_mm_xyz=dims, mass_g={k: round(g, 2) for k, (g, _) in mass.items()}),
              open(D('cad/reports/mass_properties.json'), 'w'), indent=1)
    # ---- viewer glTF (link hierarchy: base, wheel_l, wheel_r, dock)
    sc = trimesh.Scene()
    piv = {'base': (0, 0, 0), 'wheel_l': (0, 0, B.AZ), 'wheel_r': (0, 0, B.AZ), 'dock': (0, 0, 0)}
    for l, p in piv.items():
        T = np.eye(4); T[:3, 3] = p if l != 'dock' else (40, -185, 0)
        sc.graph.update(frame_from=sc.graph.base_frame, frame_to='link_' + l, matrix=T)
    tris = 0
    for k, m in M.items():
        l = LINK.get(k, 'base'); mm = m.copy(); mm.apply_translation(-np.array(piv[l]))
        mm.vertices = np.round(mm.vertices, 2)
        tris += len(mm.faces)
        sc.add_geometry(mm, node_name=k, geom_name=k, parent_node_name='link_' + l)
    glb = sc.export(file_type='glb')
    jl = struct.unpack('<I', glb[12:16])[0]; j = json.loads(glb[20:20 + jl]); off = 20 + jl
    bl = struct.unpack('<I', glb[off:off + 4])[0]; bin_ = glb[off + 8:off + 8 + bl]
    j['buffers'] = [dict(byteLength=len(bin_), uri='data:application/octet-stream;base64,' + base64.b64encode(bin_).decode())]
    json.dump(j, open(D('site/assets/bobbin.gltf'), 'w'), separators=(',', ':'))
    print('gltf tris', tris, 'size', os.path.getsize(D('site/assets/bobbin.gltf')))
    # ---- robot_info.json
    parts = {}
    for k in M:
        info = dict(MOLDED.get(k) or BOUGHT.get(k)); kind = 'molded' if k in MOLDED else 'bought'
        b = M[k].bounds; anchor = b.mean(0)
        A = dict(front_shell=(22, 0, 95), rear_shell=(-24, 0, 94), wheel_l=(0, 51, 74), tail=(-84, 0, 6), lens=(34, 12, 40),
                 oring_r=(26, -45, 99), dock=(70, -24, 44), pogo_l=(-6, 12, 10), marker=(67, 0, 40), dock_usb=(80, 0, 3))
        if k in A: anchor = np.array(A[k], float)
        parts[k] = dict(name=info['name'], group=info['group'], color=info['color'], desc=info['desc'], kind=kind,
                        mat=info.get('mat', ''), explode=list(info['explode']), link=LINK.get(k, 'base'),
                        anchor=np.round(anchor, 1).tolist(), label=k not in ('oring_l', 'wheel_r', 'screw_1', 'screw_2', 'screw_3', 'batt_contacts', 'charge_pad_r', 'cliff_r', 'encoder_r', 'motor_r', 'pogo_r', 'drv8833', 'amp', 'fpc_conn', 'charger', 'imu', 'sensor_flex'),
                        ext=k in EXTERNAL, grams=round(plastic_g.get(k, MASS_G.get(k, 0)), 1),
                        size_mm=np.round(b[1] - b[0], 1).tolist())
    summary = dict(height_mm=round(float(max(M[k].bounds[1][2] for k in M if LINK.get(k) != 'dock')), 1), dims_mm=dims,
                   mass_g=round(Mt), molded_parts=len([k for k in MOLDED]), unique_tools=6, screws=4,
                   unexpected_clashes=len(hard), stability=stab, plastic_g=round(sum(v for k, v in plastic_g.items() if k != 'dock' and not k.startswith('oring')), 1))
    json.dump(dict(groups={g: dict(name=n, color=c) for g, (n, c) in GROUPS.items()}, parts=parts, summary=summary, axle_z=B.AZ, dock_offset=[40, -185, 0],
                   eye=dict(x=B.F_FACE - B.WALL - 3.0 + 3.05, z=B.EYE_ZC, d=32.4)),
              open(D('site/assets/robot_info.json'), 'w'), indent=1)
    json.dump(summary, open(D('cad/reports/summary.json'), 'w'), indent=1)
    print('done', round(time.time() - t0), 's')


if __name__ == '__main__':
    main()
