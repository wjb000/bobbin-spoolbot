"""Part catalogue: every molded and bought part with its layer, label, explode offset and info text."""
# group: shell | drive | power | brain | sensors | face | fasteners | dock
MOLDED = {
    'front_shell': dict(name='Face shell', group='shell', color='#f1eadf', mat='ABS/PC, 2.0 mm wall, 1.5 deg draft',
        desc='Front half of the spool body. Brow visor, lens pocket, eye and mouth windows, PCB rails, front motor saddles and screw pilots are all molded in.', explode=(48, 0, 6)),
    'rear_shell': dict(name='Drive shell', group='shell', color='#3d4148', mat='ABS/PC, 2.0 mm wall, 1.5 deg draft',
        desc='Rear half: motor and battery cradle ribs, speaker grille, tail socket, charge-pad pockets, switch slot and 4 screw counterbores.', explode=(-48, 0, 6)),
    'wheel_l': dict(name='Spool wheel (left)', group='shell', color='#d4663f', mat='ABS, cored to ~2.2 mm walls, 6 ribs',
        desc='The two wheels ARE the sides of the robot: one tool makes both (the right wheel is the same part turned around). D-bore presses straight onto the N20 shaft.', explode=(0, 46, 0)),
    'wheel_r': dict(name='Spool wheel (right)', group='shell', color='#d4663f', mat='ABS (same part as left)',
        desc='Identical to the left wheel, rotated 180 degrees. Five flange dimples give the bobbin look and hide the knock-out pins.', explode=(0, -46, 0)),
    'oring_l': dict(name='Tyre O-ring (left)', group='drive', color='#2b2c30', mat='Stock 95 x 3.5 mm NBR/silicone O-ring',
        desc='A stock O-ring is the cheapest tyre there is: grippy, quiet on wood floors, replaceable.', explode=(0, 62, 0)),
    'oring_r': dict(name='Tyre O-ring (right)', group='drive', color='#2b2c30', mat='Stock 95 x 3.5 mm O-ring',
        desc='Same stock O-ring as the left side.', explode=(0, -62, 0)),
    'lens': dict(name='Face lens', group='face', color='#16191e', mat='PMMA/PC, in-mold-decorated mask',
        desc='One clear part covers the eye screen and the mouth bar (camera + range sensor). The printed mask on the inside hides everything but the eye and mouth.', explode=(80, 0, 6)),
    'tail': dict(name='Tail skid', group='shell', color='#d4663f', mat='TPU 85A, T-anchor',
        desc='The tail is the third contact point and the reaction arm for the drive. It flexes when Bobbin leans and gives it a springy, alive gait. Pops into a slot in the drive shell.', explode=(-40, 0, 14)),
    'dock': dict(name='Charging dock', group='dock', color='#ddd5c8', mat='ABS, one part, 2.4 mm top skin',
        desc='A low tongue that Bobbin drives over between its wheels. Two pogo pins meet the belly pads; the tilted post carries a printed fiducial the camera homes on.', explode=(95, 0, -4)),
}
BOUGHT = {
    'motor_l': dict(name='N20 gear motor (left)', group='drive', color='#a9afb8', desc='N20 6 V, 1:150, ~150 rpm at 6 V (~0.4 m/s at 3.7 V with 106 mm wheels). Clamped between shell ribs, no bracket.', explode=(0, 24, 0)),
    'motor_r': dict(name='N20 gear motor (right)', group='drive', color='#a9afb8', desc='Same motor, mirrored. The two motors are the axle.', explode=(0, -24, 0)),
    'encoder_l': dict(name='Hall encoder (left)', group='drive', color='#2e7d4f', desc='7 PPR magnetic encoder on the motor tail: odometry for mapping and docking.', explode=(0, 14, 0)),
    'encoder_r': dict(name='Hall encoder (right)', group='drive', color='#2e7d4f', desc='Odometry, right side.', explode=(0, -14, 0)),
    'battery': dict(name='18650 Li-ion cell', group='power', color='#3b6fb6', desc='One 2000 mAh 18650 hangs below the axle: it is the pendulum weight that keeps the face upright and lets Bobbin nod. ~2.5-3 h roaming.', explode=(-22, 0, -22)),
    'batt_contacts': dict(name='Cell spring contacts', group='power', color='#c9b26a', desc='Stamped nickel spring contacts at each end of the cradle.', explode=(-22, 0, -22)),
    'charge_pad_l': dict(name='Belly charge pad +', group='power', color='#c9a14a', desc='Nickel-plated pad flush with the belly; meets a dock pogo pin.', explode=(-10, 0, -30)),
    'charge_pad_r': dict(name='Belly charge pad -', group='power', color='#c9a14a', desc='Second charge pad.', explode=(-10, 0, -30)),
    'charger': dict(name='Charger + protection', group='power', color='#3b6fb6', desc='TP4056-class linear charger, DW01A + dual FET protection, 3.3 V buck. All on the main board.', explode=(26, 0, 0)),
    'switch': dict(name='Ship-mode slide switch', group='power', color='#555a62', desc='Hidden under the belly; cuts the cell for shipping.', explode=(-10, 0, -36)),
    'main_pcb': dict(name='Main board', group='brain', color='#1f6f43', desc='Single 2-layer 62 x 44 mm board, fully SMT-assembled. Slides into rails molded in the face shell.', explode=(26, 0, 0)),
    'esp32s3': dict(name='ESP32-S3 module (N8R8)', group='brain', color='#b8bec7', desc='Dual-core 240 MHz + vector ML instructions, Wi-Fi + BLE, 8 MB PSRAM: runs vision (person/pet detection), wake word, behaviour and the face. Antenna at the top, clear of the motors.', explode=(26, 0, 0)),
    'drv8833': dict(name='Dual H-bridge', group='brain', color='#222', desc='DRV8833-class dual motor driver.', explode=(26, 0, 0)),
    'imu': dict(name='6-axis IMU', group='sensors', color='#7a2fa0', desc='QMI8658 accel + gyro: pitch of the hanging body (nod/lean control), bump and pick-up detection.', explode=(26, 0, 0)),
    'amp': dict(name='I2S class-D amp', group='face', color='#222', desc='NS4168-class 2.5 W mono I2S amplifier.', explode=(26, 0, 0)),
    'mic': dict(name='MEMS microphone', group='sensors', color='#7a2fa0', desc='I2S MEMS mic under a top pinhole: wake word, sound events (glass break, dog barking, smoke alarm).', explode=(26, 0, 0)),
    'fpc_conn': dict(name='FPC connectors', group='brain', color='#333', desc='Display, camera and sensor-flex connectors.', explode=(26, 0, 0)),
    'display': dict(name='1.28" round IPS eye', group='face', color='#0b0d10', desc='GC9A01 240 x 240 round IPS panel: the eye(s), expressions, clock, timers and alerts.', explode=(62, 0, 6)),
    'camera': dict(name='Camera (mouth)', group='sensors', color='#30343b', desc='OV2640 2 MP, 120 deg lens behind the mouth bar: sees people, pets, the dock fiducial and obstacles; can send you a snapshot.', explode=(56, 0, 0)),
    'tof': dict(name='Time-of-flight sensor', group='sensors', color='#7a2fa0', desc='VL53L0X laser range (2 m) beside the camera: obstacle distance and final docking approach.', explode=(56, 0, 0)),
    'cliff_l': dict(name='Cliff sensor (left)', group='sensors', color='#7a2fa0', desc='IR reflective sensor looking down through the belly: stops at stair edges and table edges.', explode=(30, 0, -26)),
    'cliff_r': dict(name='Cliff sensor (right)', group='sensors', color='#7a2fa0', desc='Second cliff sensor.', explode=(30, 0, -26)),
    'sensor_flex': dict(name='Sensor flex', group='sensors', color='#c98a2b', desc='Single flex tail that carries the cliff sensors and ToF to the main board.', explode=(30, 0, -20)),
    'speaker': dict(name='20 mm speaker', group='face', color='#444a52', desc='Fires down-and-back through the molded grille; the floor acts as a baffle.', explode=(-30, 0, -24)),
    'touch_pad': dict(name='"Pet me" touch pad', group='sensors', color='#c98a2b', desc='Copper foil inside the crown, read by the ESP32 capacitive touch pin. Pat Bobbin on the head; zero added cost.', explode=(-6, 0, 30)),
    'pogo_l': dict(name='Dock pogo pin +', group='dock', color='#c9a14a', desc='Spring pogo pin, 2 A.', explode=(95, 0, -4)),
    'pogo_r': dict(name='Dock pogo pin -', group='dock', color='#c9a14a', desc='Spring pogo pin.', explode=(95, 0, -4)),
    'dock_usb': dict(name='Dock USB-C input', group='dock', color='#555', desc='5 V USB-C receptacle board with polyfuse.', explode=(95, 0, -4)),
    'marker': dict(name='Dock fiducial label', group='dock', color='#111', desc='Printed ArUco-style marker. The camera finds it from across the room; ToF does the last 10 cm.', explode=(95, 0, -4)),
}
for k in range(4):
    BOUGHT[f'screw_{k}'] = dict(name='M2 x 8 PT screw', group='fasteners', color='#7d838c', desc='Thread-forming plastic screw. The whole robot closes with four.', explode=(-70, 0, 6))
GROUPS = {
    'shell': ('Body shells', '#efe7da'), 'drive': ('Drive', '#a9afb8'), 'power': ('Power', '#3b6fb6'),
    'brain': ('Brain board', '#1f6f43'), 'sensors': ('Sensors', '#7a2fa0'), 'face': ('Face + sound', '#ff8a3d'),
    'fasteners': ('Fasteners', '#7d838c'), 'dock': ('Dock', '#ddd5c8'),
}
LINK = {'wheel_l': 'wheel_l', 'oring_l': 'wheel_l', 'wheel_r': 'wheel_r', 'oring_r': 'wheel_r',
        'dock': 'dock', 'pogo_l': 'dock', 'pogo_r': 'dock', 'dock_usb': 'dock', 'marker': 'dock'}
EXTERNAL = {'front_shell', 'rear_shell', 'wheel_l', 'lens', 'tail', 'dock', 'oring_r'}
MASS_G = {'motor_l': 9.5, 'motor_r': 9.5, 'encoder_l': 1.0, 'encoder_r': 1.0, 'battery': 45.0, 'batt_contacts': 1.0,
          'main_pcb': 8.0, 'esp32s3': 3.0, 'drv8833': 0.2, 'imu': 0.1, 'amp': 0.1, 'charger': 0.3, 'mic': 0.1, 'fpc_conn': 0.4,
          'display': 5.0, 'camera': 2.0, 'tof': 0.3, 'cliff_l': 0.2, 'cliff_r': 0.2, 'sensor_flex': 0.5, 'speaker': 3.0,
          'touch_pad': 0.4, 'charge_pad_l': 0.2, 'charge_pad_r': 0.2, 'switch': 0.5,
          'screw_0': 0.3, 'screw_1': 0.3, 'screw_2': 0.3, 'screw_3': 0.3}
DENSITY = {'front_shell': 1.06, 'rear_shell': 1.06, 'wheel_l': 1.05, 'wheel_r': 1.05, 'lens': 1.19, 'tail': 1.2,
           'oring_l': 1.3, 'oring_r': 1.3, 'dock': 1.05}
