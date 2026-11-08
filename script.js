/* Hermes Visual Agent Desk — pixel garden 3D
 * Bangun ulang script.js yang hilang (folder asli hanya punya index.html).
 * Jujur: HERMES_API_URL dibiarkan null — tidak ada server Hermes di :8000.
 * Chat berjalan offline (localStorage) sampai endpoint nyata dikonfigurasi. */

const HERMES_API_URL = null; // set ke URL endpoint nyata bila nanti ada, mis. office API
const CHAT_STORAGE_KEY = 'hvd_chat_history';
const THEME_STORAGE_KEY = 'hvd_theme';

/* ------------------------------------------------------------ helpers -- */
const $ = (id) => document.getElementById(id);
const status = (t) => { const el = $('status'); if (el) el.textContent = t; };

/* ---------------------------------------------------------------- 3D -- */
const PIXEL_SCALE = 3; // render kecil, CSS memperbesar -> look pixelated
let scene, camera, renderer, clock;
let agent, clouds = [], flowers = [], waterTiles = [];
let theta = Math.PI / 4, phi = 1.05, radius = 22;

const PALETTE = {
  grassA: 0x7ec850, grassB: 0x6ab63e, dirt: 0x8a5a33,
  water: 0x4fc3f7, waterDark: 0x29a3dd, trunk: 0x795548, leaf: 0x43a047,
  leafDark: 0x2e7d32, stone: 0x9e9e9e, wood: 0xa1887f,
  petalPink: 0xfb7185, petalGold: 0xfbbf24, petalSky: 0x38bdf8, petalWhite: 0xffffff,
  hermesBody: 0xf1f5f9, hermesAcc: 0x38bdf8, monitor: 0x1e293b,
  cloud: 0xffffff, fence: 0x8d6e63, mushroom: 0xef5350
};

const rand = (a, b) => a + Math.random() * (b - a);
const pick = (arr) => arr[Math.floor(Math.random() * arr.length)];

function box(w, h, d, color, x, y, z, parent) {
  const m = new THREE.Mesh(
    new THREE.BoxGeometry(w, h, d),
    new THREE.MeshLambertMaterial({ color })
  );
  m.position.set(x, y, z);
  (parent || scene).add(m);
  return m;
}

function buildGarden() {
  // tanah voxel 22x22, pola catur + variasi warna
  const N = 11;
  for (let gx = -N; gx <= N; gx++) {
    for (let gz = -N; gz <= N; gz++) {
      const even = (gx + gz) % 2 === 0;
      box(1, 0.5, 1, even ? PALETTE.grassA : PALETTE.grassB, gx, -0.25, gz);
    }
  }
  // kolam 4x3 di sisi kiri
  for (let px = -7; px <= -4; px++) {
    for (let pz = -1; pz <= 1; pz++) {
      box(1, 0.42, 1, PALETTE.waterDark, px, -0.28, pz);
      waterTiles.push(box(0.8, 0.46, 0.8, PALETTE.water, px, -0.26, pz));
    }
  }
  // jalan batu dari lobi meja ke kolam
  for (let i = 0; i < 7; i++) box(0.9, 0.55, 0.9, PALETTE.stone, 1 + i * 0.2, -0.2, 4 - i);
  // pagar keliling
  for (let i = -N; i <= N; i += 2) {
    box(0.15, 0.9, 0.15, PALETTE.fence, i, 0.45, -N);
    box(0.15, 0.9, 0.15, PALETTE.fence, i, 0.45, N);
    box(0.15, 0.9, 0.15, PALETTE.fence, -N, 0.45, i);
    box(0.15, 0.9, 0.15, PALETTE.fence, N, 0.45, i);
  }
  // pohon low-poly
  const treeSpots = [[-8, -6], [8, -7], [7, 6], [-7, 7], [-2, -8]];
  treeSpots.forEach(([tx, tz]) => {
    box(0.8, 2.2, 0.8, PALETTE.trunk, tx, 1.1, tz);
    box(2.4, 1.4, 2.4, PALETTE.leaf, tx, 2.8, tz);
    box(1.6, 1.0, 1.6, PALETTE.leafDark, tx, 3.9, tz);
  });
  // bunga + jamur
  for (let i = 0; i < 26; i++) {
    const fx = rand(-9.5, 9.5), fz = rand(-9.5, 9.5);
    if (fx > -8 && fx < -3 && fz > -2 && fz < 2) continue; // hindari kolam
    const g = new THREE.Group();
    g.position.set(fx, 0, fz);
    box(0.14, 0.5, 0.14, PALETTE.leafDark, 0, 0.25, 0, g);
    const petal = pick([PALETTE.petalPink, PALETTE.petalGold, PALETTE.petalSky, PALETTE.petalWhite]);
    box(0.45, 0.2, 0.45, petal, 0, 0.55, 0, g);
    box(0.2, 0.2, 0.2, PALETTE.petalGold, 0, 0.68, 0, g);
    scene.add(g);
    flowers.push({ grp: g, phase: rand(0, Math.PI * 2) });
  }
  for (let i = 0; i < 6; i++) {
    const mx = rand(-9, 9), mz = rand(-9, 9);
    box(0.25, 0.25, 0.25, PALETTE.petalWhite, mx, 0.12, mz);
    box(0.5, 0.18, 0.5, PALETTE.mushroom, mx, 0.3, mz);
  }
  // meja agent + monitor + lampu + cangkir
  const deskX = 2, deskZ = -3;
  box(2.4, 0.2, 1.2, PALETTE.wood, deskX, 1.1, deskZ);
  box(0.2, 1.0, 0.2, PALETTE.fence, deskX - 1.0, 0.5, deskZ - 0.4);
  box(0.2, 1.0, 0.2, PALETTE.fence, deskX + 1.0, 0.5, deskZ - 0.4);
  box(0.2, 1.0, 0.2, PALETTE.fence, deskX - 1.0, 0.5, deskZ + 0.4);
  box(0.2, 1.0, 0.2, PALETTE.fence, deskX + 1.0, 0.5, deskZ + 0.4);
  box(0.9, 0.65, 0.12, PALETTE.monitor, deskX + 0.4, 1.6, deskZ - 0.3);
  box(0.3, 0.5, 0.3, PALETTE.petalGold, deskX + 1.6, 1.45, deskZ);
  box(0.3, 0.25, 0.3, PALETTE.petalSky, deskX - 1.5, 1.32, deskZ + 0.2); // cangkir
  // Hermes si agent: badan putih + aksen biru, kepala besar, mata pixel
  agent = new THREE.Group();
  agent.position.set(deskX - 1.0, 0, deskZ + 1.2);
  box(0.7, 0.8, 0.5, PALETTE.hermesBody, 0, 0.9, 0, agent);
  box(0.7, 0.25, 0.5, PALETTE.hermesAcc, 0, 0.62, 0, agent);
  box(0.9, 0.75, 0.8, PALETTE.hermesBody, 0, 1.7, 0, agent);
  box(0.18, 0.18, 0.1, PALETTE.monitor, -0.2, 1.8, 0.42, agent);
  box(0.18, 0.18, 0.1, PALETTE.monitor, 0.2, 1.8, 0.42, agent);
  box(0.25, 0.12, 0.1, PALETTE.hermesAcc, 0, 1.55, 0.42, agent);
  scene.add(agent);
  // awan
  for (let i = 0; i < 5; i++) {
    const c = new THREE.Group();
    const cy = rand(9, 13), cx = rand(-14, 14), cz = rand(-14, 14);
    box(2.6, 0.9, 1.4, PALETTE.cloud, 0, 0, 0, c);
    box(1.6, 0.9, 1.2, PALETTE.cloud, 1.6, 0.3, 0, c);
    box(1.2, 0.8, 1.0, PALETTE.cloud, -1.4, 0.2, 0, c);
    c.position.set(cx, cy, cz);
    scene.add(c);
    clouds.push({ grp: c, speed: rand(0.15, 0.4) });
  }
  // matahari
  box(1.6, 1.6, 0.2, 0xfde68a, -16, 15, -18);
}

function applyTheme(dark) {
  document.body.classList.toggle('dark-theme', dark);
  $('toggle-theme').textContent = dark ? '☀️ Light' : '🌙 Dark';
  const sky = dark ? 0x0f172a : 0x7dd3fc;
  scene.background = new THREE.Color(sky);
  scene.fog.color = new THREE.Color(sky);
  window.hemi.intensity = dark ? 0.5 : 0.95;
  window.sun.intensity = dark ? 0.35 : 0.8;
  localStorage.setItem(THEME_STORAGE_KEY, dark ? 'dark' : 'light');
}

function init3D() {
  const container = $('canvas-container');
  scene = new THREE.Scene();
  const SKY = 0x7dd3fc;
  scene.background = new THREE.Color(SKY);
  scene.fog = new THREE.Fog(SKY, 34, 80);
  camera = new THREE.PerspectiveCamera(50, innerWidth / innerHeight, 0.1, 200);

  renderer = new THREE.WebGLRenderer({ antialias: false });
  renderer.setSize(innerWidth / PIXEL_SCALE, innerHeight / PIXEL_SCALE, false);
  container.appendChild(renderer.domElement);

  window.hemi = new THREE.HemisphereLight(0xffffff, 0x8a9a5b, 0.95);
  scene.add(window.hemi);
  window.sun = new THREE.DirectionalLight(0xfff3d6, 0.8);
  window.sun.position.set(-12, 20, -10);
  scene.add(window.sun);

  buildGarden();

  const savedDark = localStorage.getItem(THEME_STORAGE_KEY) === 'dark';
  applyTheme(savedDark);
  $('toggle-theme').addEventListener('click', () =>
    applyTheme(!document.body.classList.contains('dark-theme')));

  // orbit kamera: drag = putar, wheel = zoom
  let dragging = false, lx = 0, ly = 0;
  const dom = renderer.domElement;
  dom.style.pointerEvents = 'auto';
  addEventListener('mousedown', (e) => { dragging = true; lx = e.clientX; ly = e.clientY; });
  addEventListener('mouseup', () => { dragging = false; });
  addEventListener('mousemove', (e) => {
    if (!dragging) return;
    theta -= (e.clientX - lx) * 0.006;
    phi = Math.min(1.45, Math.max(0.55, phi - (e.clientY - ly) * 0.004));
    lx = e.clientX; ly = e.clientY;
  });
  addEventListener('wheel', (e) => {
    radius = Math.min(34, Math.max(10, radius + e.deltaY * 0.02));
  }, { passive: true });

  addEventListener('resize', () => {
    camera.aspect = innerWidth / innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth / PIXEL_SCALE, innerHeight / PIXEL_SCALE, false);
  });

  clock = new THREE.Clock();
  animate();
}

function animate() {
  requestAnimationFrame(animate);
  const t = clock.getElapsedTime();
  // Hermes melayang halus + menoleh ke kamera
  if (agent) {
    agent.position.y = Math.sin(t * 2) * 0.15;
    agent.rotation.y = Math.sin(t * 0.7) * 0.3;
  }
  flowers.forEach((f) => { f.grp.rotation.z = Math.sin(t * 3 + f.phase) * 0.08; });
  clouds.forEach((c) => {
    c.grp.position.x += c.speed * 0.02;
    if (c.grp.position.x > 18) c.grp.position.x = -18;
  });
  waterTiles.forEach((w, i) => {
    w.position.y = -0.26 + Math.sin(t * 2.4 + i) * 0.02;
  });
  camera.position.set(
    radius * Math.sin(phi) * Math.sin(theta),
    radius * Math.cos(phi),
    radius * Math.sin(phi) * Math.cos(theta)
  );
  camera.lookAt(0, 1, 0);
  renderer.render(scene, camera);
}

/* -------------------------------------------------------------- chat -- */
function loadChat() {
  try { return JSON.parse(localStorage.getItem(CHAT_STORAGE_KEY) || '[]'); }
  catch { return []; }
}
function saveChat(list) {
  try { localStorage.setItem(CHAT_STORAGE_KEY, JSON.stringify(list.slice(-100))); } catch {}
}
function renderChat(list) {
  const log = $('chat-log');
  log.innerHTML = '';
  list.forEach(({ who, text }) => {
    const div = document.createElement('div');
    div.className = who === 'you' ? 'text-right' : 'text-left';
    const bubble = document.createElement('span');
    bubble.className = who === 'you'
      ? 'inline-block bg-sky-200 rounded-lg px-2 py-1 text-sm max-w-[85%] break-words'
      : 'inline-block bg-amber-100 rounded-lg px-2 py-1 text-sm max-w-[85%] break-words';
    bubble.textContent = (who === 'you' ? '🧑 ' : '🤖 ') + text;
    div.appendChild(bubble);
    log.appendChild(div);
  });
  log.scrollTop = log.scrollHeight;
}

const OFFLINE_REPLIES = [
  'Mode offline — HERMES_API_URL belum dikonfigurasi, jadi aku tidak mengarang jawaban AI.',
  'Percakapan ini tersimpan lokal di browser (localStorage), bukan ke Drive — browser memang tidak boleh menulis ke I:\\.',
  'Untuk operasi task/agent yang nyata, pakai CHARISNA AI OFFICE di http://127.0.0.1:3000 — dia terhubung CLI Hermes.',
  'Pesanmu tercatat. Kalau nanti endpoint Hermes diisi, riwayat dan UI ini tinggal dipakai.'
];

async function sendChat() {
  const input = $('chat-input');
  const text = (input.value || '').trim();
  if (!text) return;
  input.value = '';
  const list = loadChat();
  list.push({ who: 'you', text });
  renderChat(list);

  if (HERMES_API_URL) {
    try {
      const res = await fetch(HERMES_API_URL, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });
      const data = await res.json();
      list.push({ who: 'bot', text: data.reply ?? JSON.stringify(data) });
    } catch (err) {
      list.push({ who: 'bot', text: 'Endpoint gagal: ' + err.message });
    }
  } else {
    const reply = OFFLINE_REPLIES[list.length % OFFLINE_REPLIES.length];
    setTimeout(() => {
      list.push({ who: 'bot', text: reply });
      renderChat(list); saveChat(list);
    }, 350);
  }
  saveChat(list);
}

/* -------------------------------------------------------------- boot -- */
addEventListener('DOMContentLoaded', () => {
  try {
    init3D();
    status('3D OK · chat offline');
  } catch (e) {
    status('3D gagal: ' + e.message);
  }
  renderChat(loadChat());
  $('send-btn').addEventListener('click', sendChat);
  $('chat-input').addEventListener('keydown', (e) => { if (e.key === 'Enter') sendChat(); });
});
