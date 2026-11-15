"""Bobbin: parametric CadQuery model.  Frame: x forward, y left, z up, millimetres, origin on the floor
under the axle.  Molded parts are built as true solids (wall thickness, ribs, bosses, pockets); bought
parts are modelled from datasheet envelope dimensions so clearances and interference checks are real."""
import math
import cadquery as cq

# ---------------- master parameters
R_WHEEL  = 51.0          # wheel rim radius (O-ring sits in a groove on it)
ORING_CS = 3.5           # O-ring cross-section (stock 95 x 3.5 mm, ~4 % stretch)
R_TIRE   = R_WHEEL + 0.25 + ORING_CS / 2   # 53.0 mm -> axle height
AZ       = R_TIRE        # axle height above floor
R_CORE   = 44.0          # body (spool core) outer radius
WALL     = 2.0           # molded wall (ABS/PC 2.0 mm nominal)
F_FACE   = 34.0          # flat face plane (x)
L_CORE   = 74.0          # body length along the axle
FIL_FACE = 6.0           # fillet face->barrel
FIL_SIDE = 9.0           # fillet barrel->side
WHEEL_IN = 38.5          # wheel inner face |y|
WHEEL_T  = 12.5          # wheel thickness
LENS_W, LENS_H, LENS_ZC, LENS_T = 40.0, 48.0, 52.0, 1.2
EYE_ZC, EYE_D = 57.0, 33.0
MOUTH_ZC, MOUTH_W, MOUTH_H = 34.0, 20.0, 6.0
CAM_Y, TOF_Y = -4.0, 6.0
BATT = dict(d=18.4, L=65.0, x=-9.0, z=30.0)
MOTOR = dict(w=12.0, h=10.0, gear=9.0, can=15.0, enc=8.0)     # N20 + hall encoder, total 32 mm
SCREWS = [(0, 24.0, AZ + 33.0), (0, -24.0, AZ + 33.0), (0, 20.0, 15.5), (0, -20.0, 15.5)]


def _core(R, F, L, ff, fs):
    """Spool core: cylinder along the axle, rounded sides, then a flat face whose edge is blended (clean, watertight B-rep)."""
    s = cq.Workplane("XZ").center(0, AZ).circle(R).extrude(L / 2, both=True)
    s = s.faces(">Y").edges().fillet(fs).faces("<Y").edges().fillet(fs)
    s = s.cut(cq.Workplane("XY").box(2 * R, L + 20, 2 * R + 20).translate((F + R, 0, AZ)))
    return s.faces(">X").edges().fillet(ff)


def outer_core():
    return _core(R_CORE, F_FACE, L_CORE, FIL_FACE, FIL_SIDE)


def inner_core():
    return _core(R_CORE - WALL, F_FACE - WALL, L_CORE - 2 * WALL, FIL_FACE - WALL, FIL_SIDE - WALL)


def lens_profile():
    """Drop-shaped face window: convex hull of the eye circle and the mouth stadium."""
    import numpy as np
    pts = []
    for (cy, cz, rr) in ((0.0, EYE_ZC, 19.0), (-6.5, MOUTH_ZC, 4.8), (6.5, MOUTH_ZC, 4.8)):
        for t in np.linspace(0, 2 * np.pi, 32, endpoint=False):
            pts.append((cy + rr * np.cos(t), cz + rr * np.sin(t)))
    from scipy.spatial import ConvexHull
    P = np.array(pts); h = ConvexHull(P)
    return [tuple(map(float, P[i])) for i in h.vertices]


def lens_outline(depth, x0):
    return cq.Workplane("YZ", origin=(x0, 0, 0)).polyline(lens_profile()).close().extrude(depth)


def tail_solid():
    pts = [(-29.0, 45.0), (-45.0, 35.0), (-59.0, 17.0), (-70.0, 4.0), (-78.0, 1.8), (-84.0, 3.9), (-87.0, 8.4)]
    path = cq.Workplane("XZ").spline(pts, includeCurrent=False)
    t0 = cq.Vector(pts[1][0] - pts[0][0], 0, pts[1][1] - pts[0][1]).normalized()
    pl = cq.Plane(origin=(pts[0][0], 0, pts[0][1]), xDir=(0, 1, 0), normal=t0)
    prof = cq.Workplane(pl).rect(14.0, 3.6)
    t = prof.sweep(path, transition="round")
    # T-anchor that sits inside the body behind the cradle
    anchor = cq.Workplane("XY").box(8, 22, 4).rotate((0, 0, 0), (0, 1, 0), -35).translate((-29.5, 0, 45.5))
    return t.union(anchor)


def screw_boss(y, z, x0, x1, d=6.0):
    return cq.Workplane("YZ", origin=(x0, 0, 0)).center(y, z).circle(d / 2).extrude(x1 - x0)


def motor_env(side):
    """N20 + encoder envelope, gearbox face at the inner wall, shaft outwards."""
    s = 1 if side > 0 else -1
    y_face = L_CORE / 2 - WALL
    total = MOTOR['gear'] + MOTOR['can'] + MOTOR['enc']
    body = cq.Workplane("XZ", origin=(0, s * (y_face - total / 2), 0)).center(0, AZ).rect(MOTOR['h'], MOTOR['w']).extrude(total / 2, both=True)
    return body


def shells():
    out, inn = outer_core(), inner_core()
    # brow visor: a soft lip over the face that gives Bobbin its "eyebrow"
    visor = (cq.Workplane("XZ").polyline([(28, 76.5), (36.2, 79.0), (35.0, 82.5), (26, 83)]).close()
             .extrude(27, both=True).edges("|Y").fillet(1.2))
    try:
        visor = visor.faces(">Y").edges().fillet(1.0).faces("<Y").edges().fillet(1.0)
    except Exception:
        pass
    body = out.union(visor).cut(inn)
    # face: lens pocket + eye window + mouth slot
    body = body.cut(lens_outline(10, F_FACE - LENS_T))
    body = body.cut(cq.Workplane("YZ", origin=(F_FACE - 6, 0, 0)).center(0, EYE_ZC).circle(EYE_D / 2).extrude(10))
    body = body.cut(cq.Workplane("YZ", origin=(F_FACE - 6, 0, 0)).center(0, MOUTH_ZC).slot2D(MOUTH_W, MOUTH_H).extrude(10))
    # axle holes + bearing collars
    for s in (1, -1):
        body = body.cut(cq.Workplane("XZ", origin=(0, s * L_CORE / 2, 0)).center(0, AZ).circle(2.5).extrude(6, both=True))
    # mic pinhole on top, speaker grille (rear-low), cliff windows, charge pads, switch slot
    body = body.cut(cq.Workplane("XY", origin=(19, 0, AZ + 30)).circle(0.6).extrude(20))
    gd = cq.Vector(-0.707, 0, -0.707)
    for i in range(-3, 4):
        sl = cq.Workplane("XY").box(1.4, 16 - abs(i) * 2.6, 10).rotate((0, 0, 0), (0, 1, 0), 45).translate((-29.7 + i * 2.2 * 0.707, 0, AZ - 29.7 - i * 2.2 * 0.707))
        body = body.cut(sl)
    for y in (18, -18):
        body = body.cut(cq.Workplane("XY", origin=(25.0, y, 5)).rect(5, 4).extrude(16))
        body = body.cut(cq.Workplane("XY", origin=(-6.0, 12 if y > 0 else -12, 6)).rect(8.4, 5.4).extrude(4.2))
    body = body.cut(cq.Workplane("XY", origin=(-14.0, 0, 4)).rect(9, 2.2).extrude(12))
    # tail slot
    tail = tail_solid()
    body = body.cut(tail)

    inner_space = inn
    # ---- ribs / bosses / rails (clipped to the cavity)
    feats = cq.Workplane("XY")
    mot = motor_env(1).union(motor_env(-1))
    bat = cq.Workplane("XZ", origin=(BATT['x'], 0, 0)).center(BATT['x'], BATT['z']).circle(BATT['d'] / 2 + 0.3).extrude(BATT['L'] / 2 + 1.5, both=True)
    bat = cq.Workplane("XZ").center(BATT['x'], BATT['z']).circle(BATT['d'] / 2 + 0.3).extrude(BATT['L'] / 2 + 1.6, both=True)
    ribs = None
    for y in (14.0, -14.0, 23.0, -23.0, 31.0, -31.0):
        r = cq.Workplane("XY").box(60, 1.6, 2 * R_CORE).translate((-30 + 10, y, AZ))   # x from -40 .. 0 for rear, front clipped below
        r = r.union(cq.Workplane("XY").box(13, 1.6, 2 * R_CORE).translate((6.5, y, AZ)))
        ribs = r if ribs is None else ribs.union(r)
    # rib heights: rear ribs only cradle the motor and battery (stop 6 mm above motor), front ribs only around the motor
    keep = (cq.Workplane("XY").box(40, 80, 30).translate((-20, 0, AZ - 3))          # rear: battery + motor zone
            .union(cq.Workplane("XY").box(12, 80, 20).translate((6, 0, AZ))))      # front: motor zone
    ribs = ribs.intersect(keep).intersect(inner_space).cut(mot.translate((0, 0, 0))).cut(bat)
    # clear speaker and tail anchor
    spk_clear = cq.Workplane("XY").cylinder(9, 12).rotate((0, 0, 0), (0, 1, 0), 45).translate((-25.5, 0, AZ - 25.5))
    ribs = ribs.cut(spk_clear).cut(tail.translate((0, 0, 0)))
    bosses = None
    for (_, y, z) in SCREWS:
        b = screw_boss(y, z, -10, 10)
        bosses = b if bosses is None else bosses.union(b)
    bosses = bosses.intersect(inner_space.union(out.cut(inn)))
    # PCB rails in the front half
    rails = None
    for y in (30.6, -30.6):
        rl = cq.Workplane("XY").box(5, 3, 46).translate((19.8, y, AZ)).cut(cq.Workplane("XY").box(1.8, 6, 50).translate((19.8, y + (1.5 if y > 0 else -1.5), AZ)))
        rails = rl if rails is None else rails.union(rl)
    rails = rails.intersect(inner_space)
    body = body.union(ribs).union(bosses).union(rails)
    # screw holes: clearance in rear, pilot in front
    for (_, y, z) in SCREWS:
        body = body.cut(cq.Workplane("YZ", origin=(-30, 0, 0)).center(y, z).circle(1.15).extrude(38))
        body = body.cut(cq.Workplane("YZ", origin=(-60, 0, 0)).center(y, z).circle(2.2).extrude(60 - 6.0).intersect(
            cq.Workplane("XY").box(60, 200, 200).translate((-36, 0, 0))))
    # split into front (face) shell and rear (drive) shell at the axle plane x = 0
    front = body.intersect(cq.Workplane("XY").box(100, 200, 200).translate((50, 0, 50)))
    rear = body.intersect(cq.Workplane("XY").box(100, 200, 200).translate((-50, 0, 50)))
    return front, rear, tail


def lens():
    lp = lens_outline(LENS_T - 0.05, F_FACE - LENS_T + 0.05)
    return lp.intersect(outer_core().translate((0.0, 0, 0)))


def wheel(side=1):
    yi, yo = WHEEL_IN, WHEEL_IN + WHEEL_T
    pts = [(3.0, yi), (R_WHEEL, yi), (R_WHEEL, yo - 2.6), (R_WHEEL - 2.4, yo), (40.0, yo), (35.0, yo - 1.6),
           (17.0, yo - 3.2), (13.5, yo - 0.4), (3.0, yo - 0.4)]
    w = cq.Workplane("XY").polyline(pts).close().revolve(360, (0, 0, 0), (0, 1, 0))
    # tyre groove
    groove = cq.Workplane("XY").center(R_WHEEL + 0.25, (yi + yo) / 2 - 0.4).circle(ORING_CS / 2 + 0.05).revolve(360, (-R_WHEEL - 0.25, 0, 0), (-R_WHEEL - 0.25, 1, 0))
    w = w.cut(groove)
    # core-out from the inner side, following the dish, for ~2.2 mm walls; 6 radial ribs
    cpts = [(9.0, yi - 0.01), (R_WHEEL - 2.4, yi - 0.01), (R_WHEEL - 2.4, yo - 3.6), (40.0, yo - 2.2), (35.0, yo - 3.8),
            (17.0, yo - 5.4), (12.0, yo - 3.0), (9.0, yo - 3.0)]
    core = cq.Workplane("XY").polyline(cpts).close().revolve(360, (0, 0, 0), (0, 1, 0))
    ribs = None
    for k in range(6):
        rib = cq.Workplane("XY").box(R_WHEEL, WHEEL_T, 1.6).translate((R_WHEEL / 2 + 6, yi + WHEEL_T / 2, 0)).rotate((0, 0, 0), (0, 1, 0), k * 60)
        ribs = rib if ribs is None else ribs.union(rib)
    w = w.cut(core.cut(ribs.cut(cq.Workplane("XZ", origin=(0, yi + 1.2, 0)).circle(R_WHEEL).extrude(2))))
    # five flange dimples (the "bobbin" look) on the outer face
    for k in range(5):
        a = math.radians(90 + k * 72)
        d = cq.Workplane("XZ", origin=(0, yo + 2, 0)).center(27 * math.cos(a), 27 * math.sin(a)).circle(5.5).extrude(5.3)
        w = w.cut(d)
    # D-bore for the N20 3 mm D shaft
    bore = cq.Workplane("XZ", origin=(0, yi - 1, 0)).circle(1.5).extrude(-9.5).intersect(
        cq.Workplane("XY").box(2.5 + 3, 20, 3.2).translate((-1.5 + 1.25, yi + 4, 0)))
    w = w.cut(bore)
    w = w.translate((0, 0, AZ))
    if side < 0:
        w = w.rotate((0, 0, AZ), (0, 0, AZ + 1), 180)
    return w


def oring(side=1):
    yc = (WHEEL_IN + WHEEL_IN + WHEEL_T) / 2 - 0.4
    t = cq.Solid.makeTorus(R_WHEEL + 0.25, ORING_CS / 2, pnt=cq.Vector(0, 0, 0), dir=cq.Vector(0, 1, 0))
    return cq.Workplane("XY").add(t).translate((0, side * yc, AZ))


def dock():
    """Charging dock: one molded part.  A low tongue that slides under the belly between the wheels,
    two pogo pins, and a tilted marker post the camera homes on."""
    base = (cq.Workplane("XZ").polyline([(-44, 0), (62, 0), (62, 7.0), (12, 7.0), (-18, 6.4), (-44, 1.2)]).close()
            .extrude(31, both=True))
    try:
        base = base.edges("|X").fillet(2.5)
    except Exception:
        pass
    post = (cq.Workplane("XZ").polyline([(54, 0), (80, 0), (80, 4), (74, 52), (66, 52), (60, 7)]).close()
            .extrude(30, both=True).edges("|Y").fillet(2.0))
    d = base.union(post)
    # marker recess (printed fiducial label sits here), pogo holes, cable exit, shell-out underneath
    d = d.cut(cq.Workplane("XY").box(3, 44, 34).rotate((0, 0, 0), (0, 1, 0), -8.5).translate((67.6, 0, 30.5)))
    for y in (12, -12):
        d = d.cut(cq.Workplane("XY", origin=(-6, y, 1)).circle(1.1).extrude(8))
    d = d.cut(cq.Workplane("XY").box(84, 54, 4.6).translate((10, 0, 2.3 - 0.01)))   # underside core-out (2.4 mm top)
    d = d.cut(cq.Workplane("XZ").polyline([(62.6, -0.1), (77.4, -0.1), (77.4, 4), (72.2, 46), (68.4, 46), (62.6, 8)]).close().extrude(27.6, both=True))
    d = d.cut(cq.Workplane("XY").box(10, 10, 4).translate((76, 0, 2)))              # USB-C board pocket
    return d


# ---------------- bought components (datasheet envelopes)
def comp_box(sx, sy, sz, c):
    return cq.Workplane("XY").box(sx, sy, sz).translate(c)


def components():
    C = {}
    ytot = MOTOR['gear'] + MOTOR['can'] + MOTOR['enc']
    yf = L_CORE / 2 - WALL
    for s, nm in ((1, 'l'), (-1, 'r')):
        g = comp_box(MOTOR['h'], MOTOR['gear'], MOTOR['w'], (0, s * (yf - MOTOR['gear'] / 2), AZ))
        can = (cq.Workplane("XZ", origin=(0, s * (yf - MOTOR['gear']), 0)).center(0, AZ).circle(6.0).extrude(s * MOTOR['can'] * -1 if False else MOTOR['can'] * (1 if s < 0 else -1) * -1 * -1)
               .intersect(comp_box(MOTOR['h'], 80, 20, (0, 0, AZ))))
        can = cq.Workplane("XZ", origin=(0, s * (yf - MOTOR['gear'] - MOTOR['can'] / 2), 0)).center(0, AZ).circle(6.0).extrude(MOTOR['can'] / 2, both=True).intersect(comp_box(MOTOR['h'], 80, 20, (0, 0, AZ)))
        enc = comp_box(MOTOR['h'] + 1, MOTOR['enc'], MOTOR['w'] + 2, (0, s * (yf - MOTOR['gear'] - MOTOR['can'] - MOTOR['enc'] / 2), AZ))
        shaft = cq.Workplane("XZ", origin=(0, s * (yf + 5.0), 0)).center(0, AZ).circle(1.5).extrude(5.0, both=True)
        C['motor_' + nm] = g.union(can).union(shaft)
        C['encoder_' + nm] = enc
    C['battery'] = cq.Workplane("XZ").center(BATT['x'], BATT['z']).circle(BATT['d'] / 2).extrude(BATT['L'] / 2, both=True)
    C['batt_contacts'] = (comp_box(1.0, 0.6, 9, (BATT['x'], BATT['L'] / 2 + 0.6, BATT['z'])).union(comp_box(1.0, 0.6, 9, (BATT['x'], -BATT['L'] / 2 - 0.6, BATT['z']))))
    # main board (vertical, behind the face) + parts on it
    C['main_pcb'] = comp_box(1.6, 62.0, 44.0, (19.8, 0, AZ))
    C['esp32s3'] = comp_box(3.1, 18.0, 25.5, (19.0 - 1.55, -12.0, AZ + 8.5))
    C['drv8833'] = comp_box(1.2, 4.4, 5.0, (18.4, 14.0, AZ - 12.0))
    C['imu'] = comp_box(0.9, 2.5, 3.0, (18.5, 6.0, AZ - 2.0))
    C['amp'] = comp_box(0.9, 3.0, 3.0, (18.5, 14.0, AZ - 2.0))
    C['charger'] = comp_box(1.5, 5.0, 4.0, (18.2, 22.0, AZ - 14.0))
    C['mic'] = comp_box(3.0, 4.0, 1.0, (19.8, 0.0, AZ + 22.5))
    C['fpc_conn'] = comp_box(2.0, 14.0, 4.0, (21.6, 0.0, AZ - 14.0))
    # face
    C['display'] = (cq.Workplane("YZ", origin=(F_FACE - WALL - 3.0, 0, 0)).center(0, EYE_ZC).circle(37.5 / 2).extrude(3.0))
    C['camera'] = (comp_box(4.5, 8.5, 8.5, (F_FACE - WALL - 7.0, CAM_Y, MOUTH_ZC))
                   .union(cq.Workplane("YZ", origin=(F_FACE - WALL - 4.8, 0, 0)).center(CAM_Y, MOUTH_ZC).circle(3.6).extrude(4.6)))
    C['tof'] = comp_box(1.0, 9.0, 7.0, (F_FACE - WALL - 0.6, 9.5, MOUTH_ZC)).union(comp_box(1.0, 4.4, 2.4, (F_FACE - WALL - 0.0, 9.5, MOUTH_ZC)))
    C['tof'] = comp_box(1.0, 7.0, 6.0, (F_FACE - WALL - 1.6, 9.0, MOUTH_ZC)).union(comp_box(1.0, 4.4, 2.4, (F_FACE - WALL - 0.6, 9.0, MOUTH_ZC)))
    C['tof'] = comp_box(0.8, 7.0, 6.0, (F_FACE - WALL - 1.9, TOF_Y, MOUTH_ZC)).union(comp_box(1.0, 4.4, 2.4, (F_FACE - WALL - 1.0, TOF_Y, MOUTH_ZC)))
    for y, nm in ((18, 'l'), (-18, 'r')):
        C['cliff_' + nm] = comp_box(5.0, 4.0, 3.0, (25.0, y, 22.0)).union(comp_box(3.4, 2.7, 1.5, (25.0, y, 19.8)))
    C['sensor_flex'] = comp_box(10.0, 44.0, 0.3, (22.0, 0, 23.7))
    C['speaker'] = cq.Workplane("XY").cylinder(4.5, 10.0).rotate((0, 0, 0), (0, 1, 0), 45).translate((-25.5, 0, AZ - 25.5))
    # capacitive "pet me" pad: copper foil on the inside of the crown
    pad = (cq.Workplane("XZ").center(0, AZ).circle(R_CORE - WALL - 0.4).circle(R_CORE - WALL - 0.65).extrude(16, both=True)
           .intersect(comp_box(24, 40, 20, (-12.0, 0, AZ + 34))))
    C['touch_pad'] = pad
    for y, nm in ((12, 'l'), (-12, 'r')):
        C['charge_pad_' + nm] = comp_box(8.0, 5.0, 0.3, (-6.0, y, 53 - math.sqrt(44 ** 2 - 36) + 0.2 + 0.05))
    C['switch'] = comp_box(8.6, 3.6, 3.6, (-14.0, 0, 17.8)).union(comp_box(1.5, 1.5, 5.6, (-14.0, 0, 13.2)))
    for (_, y, z), k in zip(SCREWS, range(4)):
        C[f'screw_{k}'] = cq.Workplane("YZ", origin=(-9.0, 0, 0)).center(y, z).circle(1.0).extrude(17.0).union(
            cq.Workplane("YZ", origin=(-10.6, 0, 0)).center(y, z).circle(1.9).extrude(1.6))
    return C


def dock_components():
    C = {}
    for y, nm in ((12, 'l'), (-12, 'r')):
        C['pogo_' + nm] = cq.Workplane("XY", origin=(-6, y, 1.0)).circle(1.0).extrude(8.6).union(
            cq.Workplane("XY", origin=(-6, y, 1.0)).circle(1.4).extrude(5.0))
    C['dock_usb'] = comp_box(9.0, 12.0, 3.2, (76, 0, 1.9))
    C['marker'] = comp_box(0.3, 40, 30, (0, 0, 0)).rotate((0, 0, 0), (0, 1, 0), -8.5).translate((66.4, 0, 30.4))
    return C
