

/* ============================================================
   4. ПУТЬ ДНК — единственная анимация страницы.
   Ползунок и саму картинку можно тянуть: схема идёт за пальцем 1:1,
   после отпускания докатывается по инерции до ближайшего этапа
   (пружина с параметрами Apple: damping ratio + response).
   ============================================================ */
(function () {
  var root = document.getElementById('dnax');
  if (!root) return;
  var RM = window.matchMedia('(prefers-reduced-motion: reduce)');
  var view = root.querySelector('.dnax__view');
  var strip = root.querySelector('.dnax__strip');
  var zones = Array.prototype.slice.call(strip.querySelectorAll('.dnax__zone'));
  var track = root.querySelector('.dnax__track');
  var fill = root.querySelector('.dnax__fill');
  var knob = root.querySelector('.dnax__knob');
  var stops = Array.prototype.slice.call(root.querySelectorAll('.dnax__stop'));
  var cap = root.querySelector('.dnax__cap');
  var MAX = zones.length - 1;
  var STAGES = [
    ['Плацента', 'Во время беременности фрагменты ДНК плаценты постоянно попадают в кровь матери.'],
    ['Кровь мамы', 'Там они смешиваются с ДНК самой мамы. Доля ДНК плода — плодная фракция — к 10 неделям обычно достигает 4 % и выше.'],
    ['Взятие крови', 'Поэтому достаточно взять 20 мл крови из вены, как при обычном анализе: прокол плодных оболочек не нужен. Из плазмы выделяют внеклеточную ДНК.'],
    ['Секвенатор', 'Прочитывает фрагменты ДНК, а программа считает, сколько прочтений приходится на каждую хромосому.'],
    ['Заключение', 'Больше прочтений по хромосоме, чем ожидается, — признак анеуплоидии, например трисомии 21. Врач-генетик оформляет заключение: высокий или низкий риск.']
  ];

  function clamp(v, a, b) { return Math.min(b, Math.max(a, v)); }
  function rubber(over, dim) { var c = 0.55; return (over * dim * c) / (dim + c * Math.abs(over)); }
  function project(v) { var d = 0.998; return (v / 1000) * d / (1 - d); }   // проекция инерции, px

  // пружина: k = (2π/response)², c = 4πζ/response; стартует с текущего значения и скорости
  var s = { x: 0, v: 0, target: 0, raf: 0, last: 0, k: 0, c: 0 };
  function sset(x) { stop(); s.x = x; s.target = x; s.v = 0; render(x); }
  function stop() { if (s.raf) { cancelAnimationFrame(s.raf); s.raf = 0; } }
  function sto(target, velocity, damping) {
    s.target = target;
    if (velocity !== undefined) s.v = velocity;
    if (RM.matches) { sset(target); return; }
    var w = 2 * Math.PI / 0.45;
    s.k = w * w; s.c = 2 * (damping || 1) * w;
    if (!s.raf) { s.last = performance.now(); s.raf = requestAnimationFrame(tick); }
  }
  function tick(now) {
    var dt = Math.min((now - s.last) / 1000, 0.064); s.last = now;
    var n = Math.max(1, Math.ceil(dt / 0.004)), h = dt / n;
    for (var i = 0; i < n; i++) { var a = -s.k * (s.x - s.target) - s.c * s.v; s.v += a * h; s.x += s.v * h; }
    if (Math.abs(s.x - s.target) < 0.0005 && Math.abs(s.v) < 0.005) { s.x = s.target; s.v = 0; s.raf = 0; render(s.x); return; }
    render(s.x);
    s.raf = requestAnimationFrame(tick);
  }

  var viewW = 1, zoneW = 1, trackW = 1, cur = -1;
  function layout() {
    viewW = view.clientWidth;
    zoneW = viewW * (viewW < 600 ? 0.86 : 0.6);
    strip.style.width = zoneW * zones.length + 'px';
    strip.style.height = zoneW * 0.6 + 'px';
    trackW = track.clientWidth;
    render(s.x);
  }
  function render(p) {
    strip.style.transform = 'translate3d(' + (viewW / 2 - (p + 0.5) * zoneW) + 'px,0,0)';
    zones.forEach(function (z, i) { z.style.opacity = String(1 - 0.62 * Math.min(Math.abs(i - p), 1)); });
    var f = clamp(p / MAX, 0, 1);
    fill.style.transform = 'scaleX(' + f + ')';
    knob.style.transform = 'translate3d(' + (f * trackW) + 'px,0,0)';
    var i = Math.round(clamp(p, 0, MAX));
    if (i !== cur) setStage(i);
  }
  function setStage(i) {
    var first = cur < 0; cur = i;
    stops.forEach(function (b, j) { b.setAttribute('aria-current', String(j === i)); });
    track.setAttribute('aria-valuenow', String(i + 1));
    track.setAttribute('aria-valuetext', STAGES[i][0]);
    var html = '<span class="dnax__n mono">0' + (i + 1) + ' / 0' + (MAX + 1) + '</span><h3>' + STAGES[i][0] + '</h3><p>' + STAGES[i][1] + '</p>';
    if (first || RM.matches || !cap.animate) { cap.innerHTML = html; return; }
    cap.animate([{ opacity: 1, filter: 'blur(0px)' }, { opacity: 0, filter: 'blur(3px)' }], { duration: 90, easing: 'ease-out', fill: 'forwards' })
      .finished.then(function () {
        if (cur !== i) return;
        cap.innerHTML = html;
        cap.animate([{ opacity: 0, filter: 'blur(3px)' }, { opacity: 1, filter: 'blur(0px)' }], { duration: 200, easing: 'cubic-bezier(0.23, 1, 0.32, 1)', fill: 'forwards' });
      });
  }
  function go(i) { sto(clamp(i, 0, MAX), undefined, 1); }

  // скорость по короткой истории движений
  var hist = [];
  function push(x) { var t = performance.now(); hist.push([x, t]); while (hist.length > 2 && t - hist[0][1] > 100) hist.shift(); }
  function velocity() {
    if (hist.length < 2) return 0;
    var a = hist[0], b = hist[hist.length - 1];
    if (performance.now() - b[1] > 80) return 0;
    var dt = (b[1] - a[1]) / 1000; return dt > 0 ? (b[0] - a[0]) / dt : 0;
  }
  function settle(pxVel, pxPerStage, sign) {
    var vStage = sign * pxVel / pxPerStage;                         // этапов в секунду
    var target = Math.round(clamp(s.x + sign * project(pxVel) / pxPerStage, 0, MAX));
    sto(target, vStage, Math.abs(vStage) > 1.5 ? 0.85 : 1);
  }

  // ползунок: схватить кнопку — тянуть с учётом точки захвата; нажать на дорожку — перейти туда
  var drag = null;
  track.addEventListener('pointerdown', function (e) {
    if (drag || (e.pointerType === 'mouse' && e.button !== 0)) return;
    var r = track.getBoundingClientRect(), pAt = (e.clientX - r.left) / trackW * MAX;
    var onKnob = Math.abs(pAt - s.x) * trackW / MAX < 24;
    stop();
    drag = { el: track, id: e.pointerId, offset: onKnob ? pAt - s.x : 0, left: r.left };
    track.setPointerCapture(e.pointerId); track.classList.add('is-drag');
    hist = []; push(e.clientX);
    if (!onKnob) sto(clamp(pAt, 0, MAX), 0, 1);
  });
  track.addEventListener('pointermove', function (e) {
    if (!drag || drag.el !== track || e.pointerId !== drag.id) return;
    push(e.clientX);
    var p = (e.clientX - drag.left) / trackW * MAX - drag.offset;
    if (p < 0) p = -rubber(-p, 1); else if (p > MAX) p = MAX + rubber(p - MAX, 1);
    stop(); s.x = p; s.v = 0; render(p);
  });
  function endTrack() {
    if (!drag || drag.el !== track) return;
    track.classList.remove('is-drag'); drag = null;
    settle(velocity(), trackW / MAX, 1);
  }
  track.addEventListener('pointerup', endTrack);
  track.addEventListener('pointercancel', endTrack);

  // картинка: горизонтальный жест после порога 10 px, вертикальный остаётся прокрутке страницы
  var vs = null;
  view.addEventListener('pointerdown', function (e) {
    if (drag || (e.pointerType === 'mouse' && e.button !== 0)) return;
    vs = { id: e.pointerId, x: e.clientX, y: e.clientY, p: s.x, on: false };
    hist = []; push(e.clientX);
    if (e.pointerType === 'mouse') e.preventDefault();
  });
  view.addEventListener('pointermove', function (e) {
    if (!vs || e.pointerId !== vs.id) return;
    var dx = e.clientX - vs.x, dy = e.clientY - vs.y;
    if (!vs.on) {
      if (Math.abs(dx) > 10 && Math.abs(dx) > Math.abs(dy)) { vs.on = true; stop(); vs.p = s.x + dx / zoneW; view.setPointerCapture(vs.id); view.classList.add('is-drag'); }
      else if (Math.abs(dy) > 10) { vs = null; return; }
      else return;
    }
    push(e.clientX);
    var p = vs.p - dx / zoneW;
    if (p < 0) p = -rubber(-p, 1); else if (p > MAX) p = MAX + rubber(p - MAX, 1);
    s.x = p; s.v = 0; render(p);
  });
  function endView() {
    if (vs && vs.on) { view.classList.remove('is-drag'); settle(velocity(), zoneW, -1); }
    vs = null;
  }
  view.addEventListener('pointerup', endView);
  view.addEventListener('pointercancel', endView);

  stops.forEach(function (b, i) { b.addEventListener('click', function () { go(i); }); });
  track.addEventListener('keydown', function (e) {
    var k = e.key, i = Math.round(s.target);
    if (k === 'ArrowRight' || k === 'ArrowUp') go(i + 1);
    else if (k === 'ArrowLeft' || k === 'ArrowDown') go(i - 1);
    else if (k === 'Home') go(0);
    else if (k === 'End') go(MAX);
    else return;
    e.preventDefault();
  });

  if ('ResizeObserver' in window) new ResizeObserver(layout).observe(view); else window.addEventListener('resize', layout);
  layout();
})();
