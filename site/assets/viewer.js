import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';
import {toCreasedNormals} from 'three/addons/utils/BufferGeometryUtils.js';

const $ = id => document.getElementById(id);
const el = $('viewer'), Q = new URLSearchParams(location.search);
const scene = new THREE.Scene();
const cam = new THREE.PerspectiveCamera(26, innerWidth / innerHeight, 5, 6000);
const r = new THREE.WebGLRenderer({antialias: true, alpha: true, preserveDrawingBuffer: true});
r.setPixelRatio(Math.min(devicePixelRatio, 2)); r.setSize(innerWidth, innerHeight);
r.shadowMap.enabled = true; r.shadowMap.type = THREE.PCFSoftShadowMap;
r.toneMapping = THREE.ACESFilmicToneMapping; r.toneMappingExposure = 1.0; r.outputColorSpace = THREE.SRGBColorSpace;
el.prepend(r.domElement);
const pm = new THREE.PMREMGenerator(r); scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture; scene.environmentIntensity = 0.6;
const ctl = new OrbitControls(cam, r.domElement); ctl.enableDamping = true; ctl.minDistance = 120; ctl.maxDistance = 1800;

// robot frame: x forward, y left, z up (mm) -> three (x, z, -y)
const TGT = new THREE.Vector3(0, 46, 40);
const VIEWS = {'34': [500, 270, -440], front: [600, 60, 0], side: [0, 80, -600], back: [-600, 100, 0], top: [0.1, 640, 0], bottom: [60, -500, -40]};
const OFF = new THREE.Vector3(-55, 0, 0); // shift target so the model sits left of the right panel
function setView(n) {
  const v = VIEWS[n] || VIEWS['34'];
  const t = TGT.clone();
  cam.position.set(...v).add(t); ctl.target.copy(t); ctl.update();
  document.querySelectorAll('[data-view]').forEach(b => b.classList.toggle('on', b.dataset.view === n));
}
scene.add(new THREE.HemisphereLight(0xfff7ee, 0x9b8f80, 0.85));
const key = new THREE.DirectionalLight(0xffffff, 2.2); key.position.set(300, 620, -360); key.castShadow = true;
key.shadow.mapSize.set(2048, 2048); Object.assign(key.shadow.camera, {left: -260, right: 260, top: 260, bottom: -260, near: 50, far: 1800});
key.shadow.bias = -0.0004; key.shadow.normalBias = 0.8; scene.add(key);
const rim = new THREE.DirectionalLight(0xffe2c4, 1.0); rim.position.set(-500, 300, 300); scene.add(rim);
const floor = new THREE.Mesh(new THREE.CircleGeometry(900, 96), new THREE.ShadowMaterial({opacity: 0.15}));
floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; scene.add(floor);
const root = new THREE.Group(); root.rotation.x = -Math.PI / 2; scene.add(root);

let RI, BOM, xray = Q.get('xray') === '1', showLabels = Q.get('labels') !== '0', explodeT = +(Q.get('explode') || 0), demo = Q.get('demo') === '1', sel = null;
const items = {}, links = {}, labels = [], visible = {};
const SHELLISH = new Set(['shell', 'dock']);

function eyeTexture() {
  const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d');
  const draw = (blink = 0, look = 0) => {
    g.fillStyle = '#06080b'; g.fillRect(0, 0, 256, 256);
    const grd = g.createRadialGradient(128, 128, 10, 128, 128, 128); grd.addColorStop(0, 'rgba(255,170,90,.10)'); grd.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = grd; g.fillRect(0, 0, 256, 256);
    g.fillStyle = '#ffd9a8'; g.shadowColor = '#ff9a4a'; g.shadowBlur = 18;
    const h = 92 * (1 - blink) + 8;
    for (const x of [86, 170]) { g.beginPath(); g.roundRect(x - 23 + look, 128 - h / 2 - 4, 46, h, 23); g.fill(); }
    g.shadowBlur = 0; g.fillStyle = 'rgba(255,255,255,.85)';
    if (blink < .5) for (const x of [96, 180]) { g.beginPath(); g.arc(x + look, 100, 7, 0, 7); g.fill(); }
  };
  draw(); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.draw = (b, l) => { draw(b, l); t.needsUpdate = true; }; return t;
}
const eyeTex = eyeTexture();

function material(p) {
  const col = new THREE.Color(p.color);
  if (p.key === 'lens') return new THREE.MeshPhysicalMaterial({color: 0x0d0f13, roughness: 0.05, metalness: 0, clearcoat: 1, transparent: true, opacity: 0.5, depthWrite: false});
  if (p.group === 'shell' || p.key === 'dock') return new THREE.MeshPhysicalMaterial({color: col, roughness: p.key === 'tail' ? 0.75 : 0.42, clearcoat: p.key === 'tail' ? 0 : 0.35, clearcoatRoughness: 0.35, side: THREE.DoubleSide});
  if (p.key.startsWith('oring')) return new THREE.MeshStandardMaterial({color: col, roughness: 0.85});
  const metal = /motor|screw|pad|contact|pogo|esp32/.test(p.key);
  return new THREE.MeshStandardMaterial({color: col, roughness: metal ? 0.35 : 0.6, metalness: metal ? 0.6 : 0.05});
}

Promise.all([fetch('assets/robot_info.json').then(r => r.json()), fetch('assets/bom.json').then(r => r.json()),
  new GLTFLoader().loadAsync('assets/bobbin.gltf')]).then(([ri, bom, gl]) => {
  RI = ri; BOM = bom;
  for (const g of Object.keys(RI.groups)) visible[g] = true;
  (Q.get('hide') || '').split(',').filter(Boolean).forEach(g => visible[g] = false);
  root.add(gl.scene);
  gl.scene.traverse(o => {
    if (o.name && o.name.startsWith('link_')) links[o.name.slice(5)] = o;
    const k = o.name; const p = RI.parts[k];
    if (!p) return;
    const meshes = []; o.traverse(m => { if (m.isMesh) meshes.push(m); });
    p.key = k;
    for (const m of meshes) {
      m.geometry = toCreasedNormals(m.geometry, Math.PI / 7);
      m.material = material(p); m.castShadow = !p.key.startsWith('lens'); m.receiveShadow = true; m.userData.key = k;
      m.userData.baseOpacity = m.material.opacity;
    }
    items[k] = {node: o, p, meshes, pos0: o.position.clone()};
  });
  for (const l of Object.values(links)) { l.userData.p0 = l.position.clone(); l.userData.q0 = l.quaternion.clone(); }
  // glowing eye on the display face
  const eye = new THREE.Mesh(new THREE.CircleGeometry(RI.eye.d / 2, 64), new THREE.MeshBasicMaterial({map: eyeTex, toneMapped: false}));
  eye.rotation.set(0, Math.PI / 2, 0); eye.rotation.order = 'YXZ';
  const eh = new THREE.Group(); eh.position.set(RI.eye.x, 0, RI.eye.z); eh.rotation.x = Math.PI / 2; eh.add(eye);
  items.display.node.add(eh); eh.position.sub(items.display.pos0); eh.userData.key = 'display'; eye.userData.key = 'display'; items.display.meshes.push(eye);
  buildUI(); applyAll();
  setView(Q.get('view') || '34');
  requestAnimationFrame(() => requestAnimationFrame(() => document.body.classList.add('loaded')));
}).catch(e => { $('loading').textContent = 'Could not load the model: ' + e; console.error(e); });

function buildUI() {
  const counts = {};
  for (const it of Object.values(items)) counts[it.p.group] = (counts[it.p.group] || 0) + 1;
  $('layers').innerHTML = Object.entries(RI.groups).map(([g, v]) =>
    `<label><input type="checkbox" data-g="${g}" ${visible[g] ? 'checked' : ''}><span class="sw" style="background:${v.color}"></span>${v.name}<span class="n">${counts[g] || 0}</span></label>`).join('');
  $('layers').onchange = e => { visible[e.target.dataset.g] = e.target.checked; applyAll(); };
  const S = RI.summary;
  $('stats').innerHTML = [['Size', `${S.dims_mm[1].toFixed(0)} w x ${S.height_mm.toFixed(0)} h mm`], ['Mass', `${S.mass_g} g`],
    ['Plastic parts', '6 + dock'], ['Unique tools', S.unique_tools], ['Screws', S.screws], ['Motors', '2'],
    ['Volume BOM', `$${BOM.volume_total.toFixed(2)}`], ['Prototype BOM', `$${BOM.proto_total.toFixed(2)}`], ['CAD clashes', S.unexpected_clashes]]
    .map(([a, b]) => `<span>${a}</span><b>${b}</b>`).join('');
  // component list
  const byG = {};
  for (const [k, it] of Object.entries(items)) (byG[it.p.group] ||= []).push([k, it.p]);
  $('clist').innerHTML = Object.entries(RI.groups).filter(([g]) => byG[g]).map(([g, v]) =>
    `<div class="g"><span class="sw" style="width:9px;height:9px;border-radius:2px;background:${v.color};display:inline-block"></span>${v.name}</div>` +
    byG[g].map(([k, p]) => `<div class="c" data-k="${k}"><span>${p.name}</span><i>${p.kind === 'molded' ? p.grams + ' g' : (p.size_mm.map(x => x.toFixed(0)).join('x') + ' mm')}</i></div>`).join('')).join('');
  $('clist').onclick = e => { const c = e.target.closest('.c'); if (c) select(c.dataset.k, true); };
  // labels
  for (const [k, it] of Object.entries(items)) {
    if (!it.p.label) continue;
    const d = document.createElement('div'); d.className = 'lbl'; d.innerHTML = `<span>${it.p.name.replace(/ \((left|right)\)/, '')}</span>`;
    d.onclick = () => select(k, true); $('labels').appendChild(d);
    labels.push({k, it, d, a: new THREE.Vector3(...it.p.anchor)});
  }
  // BOM tab
  const vol = BOM.volume.map(x => `<tr><td>${x.item}${x.qty > 1 ? ' &times;' + x.qty : ''}${x.status === 'estimate' ? ' <span class="est">est.</span>' : ''}</td><td>$${(x.qty * x.unit).toFixed(2)}</td></tr>`).join('');
  const pro = BOM.proto.map(x => `<tr><td>${x.item}${x.qty > 1 ? ' &times;' + x.qty : ''}${x.status === 'estimate' ? ' <span class="est">est.</span>' : ''}</td><td>$${(x.qty * x.unit).toFixed(2)}</td></tr>`).join('');
  $('bom').innerHTML = `<div class="big"><div><b>$${BOM.volume_total.toFixed(2)}</b><span>volume BOM @10k, dock + box included</span></div><div><b>$${BOM.proto_total.toFixed(2)}</b><span>prototype, 3D printed, qty 1</span></div></div>
    <p class="small">Prices checked ${BOM.checked}. Lines marked est. are estimates until quoted. Every line links its source in <a href="https://github.com/wjb000/bobbin-spoolbot/blob/main/BOM.md">BOM.md</a>.</p>
    <h4>Volume</h4><table class="bomt">${vol}</table><h4>Prototype</h4><table class="bomt">${pro}</table>`;
  // tabs + buttons
  $('tabs').onclick = e => { const b = e.target.closest('button'); if (!b) return; document.querySelectorAll('#tabs button').forEach(x => x.classList.toggle('on', x === b));
    document.querySelectorAll('.tab').forEach(t => t.classList.toggle('on', t.id === 'tab-' + b.dataset.tab)); };
  if (Q.get('tab')) document.querySelector(`#tabs [data-tab="${Q.get('tab')}"]`)?.click();
  $('views').onclick = e => { const b = e.target.closest('button'); if (b) setView(b.dataset.view); };
  $('xray').onclick = () => { xray = !xray; applyAll(); };
  $('lbls').onclick = () => { showLabels = !showLabels; applyAll(); };
  $('demo').onclick = () => { demo = !demo; $('demo').classList.toggle('on', demo); if (!demo) resetPose(); };
  $('explode').value = explodeT; $('explode').oninput = e => { explodeT = +e.target.value; applyAll(); };
  $('info-x').onclick = () => select(null);
  $('xray').classList.toggle('on', xray); $('demo').classList.toggle('on', demo);
  if (Q.get('sel')) select(Q.get('sel'), false);
}

function applyAll() {
  $('xray').classList.toggle('on', xray); $('lbls').classList.toggle('on', showLabels);
  for (const it of Object.values(items)) {
    it.node.visible = visible[it.p.group];
    const e = new THREE.Vector3(...it.p.explode).multiplyScalar(explodeT);
    it.node.position.copy(it.pos0).add(e);
    const ghost = xray && SHELLISH.has(it.p.group) || xray && it.p.key === 'lens';
    for (const m of it.meshes) {
      if (m.material.isMeshBasicMaterial) continue;
      m.material.transparent = ghost || m.userData.baseOpacity < 1;
      m.material.opacity = ghost ? (it.p.key === 'lens' ? 0.18 : 0.13) : m.userData.baseOpacity;
      m.material.depthWrite = !ghost && it.p.key !== 'lens';
      m.castShadow = !ghost && it.p.key !== 'lens';
      m.material.needsUpdate = true;
    }
  }
}
function select(k, focus) {
  if (sel && items[sel]) for (const m of items[sel].meshes) m.material.emissive?.set(0x000000);
  labels.forEach(L => L.d.classList.toggle('sel', L.k === k));
  document.querySelectorAll('#clist .c').forEach(c => c.classList.toggle('sel', c.dataset.k === k));
  sel = k;
  if (!k) { $('info').classList.add('hidden'); return; }
  const it = items[k]; for (const m of it.meshes) { if (m.material.emissive) { m.material.emissive.set(0xd4663f); m.material.emissiveIntensity = 0.45; } }
  const p = it.p; $('info').classList.remove('hidden');
  $('info-t').textContent = p.name; $('info-k').textContent = `${RI.groups[p.group].name} · ${p.kind === 'molded' ? 'molded part' : 'bought part'}`;
  $('info-d').textContent = p.desc;
  $('info-m').innerHTML = [p.mat && `Material: ${p.mat}`, p.kind === 'molded' ? `Mass: ${p.grams} g` : '', `Envelope: ${p.size_mm.map(x => x.toFixed(1)).join(' x ')} mm`].filter(Boolean).join('<br>');
  if (focus && !visible[p.group]) { visible[p.group] = true; document.querySelector(`#layers [data-g="${p.group}"]`).checked = true; applyAll(); }
}
const ray = new THREE.Raycaster(), ptr = new THREE.Vector2(); let down = null;
r.domElement.addEventListener('pointerdown', e => down = [e.clientX, e.clientY]);
r.domElement.addEventListener('pointerup', e => {
  if (!down || Math.hypot(e.clientX - down[0], e.clientY - down[1]) > 4) return;
  ptr.set(e.clientX / innerWidth * 2 - 1, -(e.clientY / innerHeight) * 2 + 1); ray.setFromCamera(ptr, cam);
  const hits = ray.intersectObject(root, true).filter(h => h.object.userData.key && shown(h.object) && !(xray && (SHELLISH.has(items[h.object.userData.key].p.group) || h.object.userData.key === 'lens')) && h.object.userData.key !== 'lens');
  select(hits.length ? hits[0].object.userData.key : null);
});
function shown(o) { while (o) { if (!o.visible) return false; o = o.parent; } return true; }

const axle = () => new THREE.Vector3(0, 0, RI.axle_z), qy = new THREE.Quaternion(), Y = new THREE.Vector3(0, 1, 0);
function resetPose() { for (const l of Object.values(links)) { l.position.copy(l.userData.p0); l.quaternion.copy(l.userData.q0); } eyeTex.draw(0, 0); }
function stepDemo(t) {
  if (!demo || !RI) return;
  const roll = t * 2.4, pitch = 0.10 * Math.sin(t * 1.7) * Math.max(0, Math.sin(t * 0.5)) - 0.03;
  for (const w of ['wheel_l', 'wheel_r']) if (links[w]) { qy.setFromAxisAngle(Y, roll); links[w].quaternion.copy(links[w].userData.q0).multiply(qy); }
  const b = links.base; if (b) { qy.setFromAxisAngle(Y, pitch); b.quaternion.copy(qy); const a = axle(); b.position.copy(a).sub(a.clone().applyQuaternion(qy)); }
  const ph = (t % 4.2); eyeTex.draw(ph < 0.16 ? Math.sin(ph / 0.16 * Math.PI) : 0, 14 * Math.sin(t * 0.8));
}
const v = new THREE.Vector3();
function placeLabels() {
  if (!RI) return;
  const w = innerWidth, h = innerHeight;
  for (const L of labels) {
    const it = L.it;
    const on = showLabels && visible[it.p.group] && (it.p.ext || xray || explodeT > 0.3 || !visible.shell);
    if (!on || (xray && it.p.ext && SHELLISH.has(it.p.group) && it.p.key !== 'dock' && it.p.key !== 'tail')) { L.d.style.display = 'none'; continue; }
    v.copy(L.a).addScaledVector(new THREE.Vector3(...it.p.explode), explodeT); if (it.p.link === 'dock') v.add(new THREE.Vector3(...RI.dock_offset));
    root.localToWorld(v); v.project(cam);
    if (v.z > 1) { L.d.style.display = 'none'; continue; }
    L.d.style.display = ''; L.d.style.transform = `translate(${(v.x * .5 + .5) * w}px,${(-v.y * .5 + .5) * h}px)`;
  }
}
addEventListener('resize', () => { cam.aspect = innerWidth / innerHeight; cam.updateProjectionMatrix(); r.setSize(innerWidth, innerHeight); });
(function loop(t) { requestAnimationFrame(loop); stepDemo((t || 0) / 1000); ctl.update(); placeLabels(); r.render(scene, cam); })();
