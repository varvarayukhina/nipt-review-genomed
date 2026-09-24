

/* ============================================================
   4. ПУТЬ ДНК — сцена, привязанная к прокрутке.
   Одни и те же точки-фрагменты текут в крови, собираются в пробирку,
   выстраиваются в прочтения секвенатора и раскладываются по хромосомам.
   Прокрутка назад отматывает сцену назад.
   ============================================================ */
(function () {
  var sec = document.getElementById('safe');
  if (!sec || !sec.querySelector('.nstage canvas')) return;
  var RM = window.matchMedia('(prefers-reduced-motion: reduce)');
  var canvas = sec.querySelector('.nstage canvas');
  var ctx = canvas.getContext('2d');
  var caps = Array.prototype.slice.call(sec.querySelectorAll('.ncap'));
  var legA = sec.querySelector('.nleg__a'), legB = sec.querySelector('.nleg__b');
  // относительные размеры хромосом 1–22 — только для пропорций схемы
  var SIZE = [248, 242, 198, 190, 181, 171, 159, 145, 138, 134, 135, 133, 114, 107, 102, 90, 83, 80, 59, 64, 47, 51];
  var MOM = [75, 142, 255], PLA = [0, 194, 255], XTR = [255, 181, 71];

  function clamp(v, a, b) { return Math.min(b, Math.max(a, v)); }
  function ease(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function smooth(t) { return t * t * (3 - 2 * t); }
  var seed = 21;
  function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }

  var W = 0, H = 0, dpr = 1, parts = [], extras = [], cells = [], tube = null, cols = [], perRow = 2, step = 6, base = 0, rCol = 3;

  function build() {
    if (canvas.clientWidth === W && W) return;
    W = canvas.clientWidth;
    H = Math.round(clamp(W * (W < 600 ? 0.78 : 0.42), 240, 400));
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr); canvas.style.height = H + 'px';
    seed = 21;
    var N = W < 600 ? 300 : 520;

    // пробирка
    var tw = clamp(W * 0.12, 54, 96), th = H * 0.84, tx = W / 2 - tw / 2, ty = H * 0.08;
    tube = { x: tx, y: ty, w: tw, h: th, plasma: ty + th * 0.5 };

    // колонки хромосом
    var total = SIZE.reduce(function (a, b) { return a + b; }, 0);
    var counts = SIZE.map(function (s) { return Math.round(N * s / total); });
    N = counts.reduce(function (a, b) { return a + b; }, 0);
    var areaW = W * (W < 600 ? 0.94 : 0.86), x0 = (W - areaW) / 2, cw = areaW / 22;
    perRow = W < 600 ? 2 : 3;
    var maxRows = Math.ceil(Math.max.apply(null, counts) / perRow) + 3;
    base = H * 0.86;
    step = Math.min((H * 0.72) / maxRows, (cw * 0.84) / perRow);
    rCol = step * 0.4;
    cols = counts.map(function (c, k) { return { x: x0 + k * cw, w: cw, n: c, top: base - Math.ceil(c / perRow) * step }; });

    // порядок частиц перемешан, чтобы в колонках цвета смешались
    var order = [];
    counts.forEach(function (c, k) { for (var j = 0; j < c; j++) order.push([k, j]); });
    for (var i = order.length - 1; i > 0; i--) { var r = Math.floor(rnd() * (i + 1)); var t = order[i]; order[i] = order[r]; order[r] = t; }

    var rows = W < 600 ? 11 : 13, per = Math.ceil(N / rows), rx0 = W * 0.08, rdx = (W * 0.84) / per;
    parts = order.map(function (kj, i) {
      var k = kj[0], j = kj[1], col = cols[k];
      var inX = tube.x + 5 + rnd() * (tube.w - 10), inY = tube.y + 14 + rnd() * (tube.plasma - tube.y - 20);
      var row = Math.floor(i / per), inRow = i % per;
      return {
        type: rnd() < 0.12 ? 1 : 0,
        s0: [-0.25 * W + rnd() * 1.25 * W, H * 0.16 + rnd() * H * 0.68],
        s1: [inX, inY],
        s2: [rx0 + (inRow + 0.5) * rdx + (row % 2) * rdx * 0.35, H * 0.1 + row * ((H * 0.8) / (rows - 1))],
        s3: [col.x + col.w * 0.08 + ((j % perRow) + 0.5) * (col.w * 0.84 / perRow), base - (Math.floor(j / perRow) + 0.5) * step],
        st: rnd()
      };
    });
    // лишняя копия 21-й: столбец выше ожидаемого (схематично крупнее, чем в реальности)
    var c21 = cols[20], nx = Math.max(3, Math.round(c21.n * 0.45));
    extras = [];
    for (var e = 0; e < nx; e++) {
      var jj = c21.n + e;
      extras.push({ s4: [c21.x + c21.w * 0.08 + ((jj % perRow) + 0.5) * (c21.w * 0.84 / perRow), base - (Math.floor(jj / perRow) + 0.5) * step], st: rnd() });
    }
    // эритроциты в первом кадре — просто фон
    cells = [];
    for (var c = 0; c < 16; c++) cells.push([rnd() * W, H * 0.16 + rnd() * H * 0.68, 9 + rnd() * 7]);
    draw();
  }

  function seg(P, a, b) { return clamp((P - a) / (b - a), 0, 1); }
  function lerp(a, b, t) { return [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t]; }
  function rgba(c, a) { return 'rgba(' + c[0] + ',' + c[1] + ',' + c[2] + ',' + a + ')'; }

  function tubePath(x, y, w, h) {
    var r = w / 2;
    ctx.beginPath();
    ctx.moveTo(x, y); ctx.lineTo(x, y + h - r);
    ctx.arc(x + r, y + h - r, r, Math.PI, 0, true);
    ctx.lineTo(x + w, y);
  }

  function draw() {
    var P = progress();
    var u1, u2, u3, u4;
    if (RM.matches) {
      u1 = P > 0.16 ? 1 : 0; u2 = P > 0.4 ? 1 : 0; u3 = P > 0.64 ? 1 : 0; u4 = P > 0.84 ? 1 : 0;
    } else {
      u1 = seg(P, 0.14, 0.3); u2 = seg(P, 0.4, 0.56); u3 = seg(P, 0.64, 0.78); u4 = seg(P, 0.84, 0.94);
    }
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);

    // кадр 1: кровоток
    var a0 = 1 - smooth(u1);
    if (a0 > 0.01) {
      ctx.fillStyle = 'rgba(255,255,255,' + (0.035 * a0) + ')';
      ctx.fillRect(0, H * 0.12, W, H * 0.76);
      ctx.strokeStyle = 'rgba(255,138,128,' + (0.35 * a0) + ')'; ctx.lineWidth = 2;
      ctx.beginPath(); ctx.moveTo(0, H * 0.12); ctx.lineTo(W, H * 0.12); ctx.moveTo(0, H * 0.88); ctx.lineTo(W, H * 0.88); ctx.stroke();
      cells.forEach(function (c) {
        ctx.fillStyle = 'rgba(255,120,110,' + (0.24 * a0) + ')';
        ctx.beginPath(); ctx.ellipse(c[0] + P * W * 0.5, c[1], c[2], c[2] * 0.72, 0, 0, 6.2832); ctx.fill();
      });
    }
    // кадр 2: пробирка — плазма сверху, клетки крови снизу
    var aT = smooth(u1) * (1 - smooth(u2));
    if (aT > 0.01) {
      var t = tube;
      ctx.save(); tubePath(t.x, t.y, t.w, t.h); ctx.closePath(); ctx.clip();
      ctx.fillStyle = 'rgba(255,224,160,' + (0.12 * aT) + ')'; ctx.fillRect(t.x, t.y, t.w, t.plasma - t.y);
      ctx.fillStyle = 'rgba(232,112,100,' + (0.75 * aT) + ')'; ctx.fillRect(t.x, t.plasma, t.w, t.h);
      ctx.restore();
      ctx.strokeStyle = 'rgba(255,255,255,' + (0.7 * aT) + ')'; ctx.lineWidth = 2.5;
      tubePath(t.x, t.y, t.w, t.h); ctx.stroke();
      ctx.fillStyle = 'rgba(184,236,255,' + (0.9 * aT) + ')';
      ctx.beginPath(); ctx.roundRect ? ctx.roundRect(t.x - 6, t.y - 16, t.w + 12, 18, 6) : ctx.rect(t.x - 6, t.y - 16, t.w + 12, 18); ctx.fill();
    }
    // кадр 4–5: ожидаемый уровень и номера хромосом
    var aC = smooth(u3);
    if (aC > 0.01) {
      ctx.font = '600 ' + (W < 600 ? 9 : 11) + 'px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      cols.forEach(function (c, k) {
        var hi = k === 12 || k === 17 || k === 20;
        ctx.strokeStyle = 'rgba(255,255,255,' + (0.35 * aC) + ')'; ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.moveTo(c.x + c.w * 0.04, c.top - 2); ctx.lineTo(c.x + c.w * 0.96, c.top - 2); ctx.stroke();
        if (W >= 600 || hi || k % 2 === 0) {
          ctx.fillStyle = hi ? 'rgba(0,194,255,' + aC + ')' : 'rgba(169,196,226,' + (0.7 * aC) + ')';
          ctx.fillText(String(k + 1), c.x + c.w / 2, base + (W < 600 ? 13 : 17));
        }
      });
    }
    // частицы
    var dash = smooth(u2) * (1 - smooth(u3));
    parts.forEach(function (p) {
      var s0 = [p.s0[0] + Math.min(P, 0.14) / 0.14 * W * 0.25, p.s0[1]];
      var t1 = ease(clamp(u1 * 1.35 - p.st * 0.35, 0, 1));
      var t2 = ease(clamp(u2 * 1.35 - p.st * 0.35, 0, 1));
      var t3 = ease(clamp(u3 * 1.35 - p.st * 0.35, 0, 1));
      var pos = lerp(lerp(lerp(s0, p.s1, t1), p.s2, t2), p.s3, t3);
      var r = 3.1 + (2.3 - 3.1) * t1;
      r = r + (2.6 - r) * t2;
      r = r + (rCol - r) * t3;
      ctx.fillStyle = rgba(p.type ? PLA : MOM, p.type ? 1 : 0.9);
      if (dash > 0.02) {
        var w = r * 2 + dash * r * 2.6;
        ctx.beginPath();
        if (ctx.roundRect) ctx.roundRect(pos[0] - w / 2, pos[1] - r, w, r * 2, r); else ctx.rect(pos[0] - w / 2, pos[1] - r, w, r * 2);
        ctx.fill();
      } else {
        ctx.beginPath(); ctx.arc(pos[0], pos[1], r, 0, 6.2832); ctx.fill();
      }
    });
    // лишняя копия 21-й
    if (u4 > 0) {
      var c21 = cols[20];
      extras.forEach(function (e) {
        var te = ease(clamp(u4 * 1.4 - e.st * 0.4, 0, 1));
        if (te <= 0) return;
        var pos = lerp([e.s4[0], -20], e.s4, te);
        ctx.fillStyle = rgba(XTR, clamp(te * 3, 0, 1));
        ctx.beginPath(); ctx.arc(pos[0], pos[1], rCol, 0, 6.2832); ctx.fill();
      });
      var topX = base - Math.ceil((c21.n + extras.length) / perRow) * step;
      ctx.strokeStyle = rgba(XTR, 0.85 * smooth(u4)); ctx.lineWidth = 1.5; ctx.setLineDash([4, 4]);
      ctx.strokeRect(c21.x + 1, topX - 3, c21.w - 2, c21.top - topX + 2);
      ctx.setLineDash([]);
    }

    // подписи: у каждой свой отрезок прокрутки
    var win = [[-1, 0.15], [0.19, 0.39], [0.43, 0.63], [0.67, 0.83], [0.87, 2]];
    caps.forEach(function (cap, j) {
      var a = win[j][0], b = win[j][1];
      var o = RM.matches ? (P >= a && P < b ? 1 : 0) : clamp((P - a) / 0.04, 0, 1) * clamp((b - P) / 0.04, 0, 1);
      cap.style.opacity = String(o);
      cap.style.transform = RM.matches ? '' : 'translate3d(0,' + ((1 - o) * (P < (a + b) / 2 ? 12 : -12)) + 'px,0)';
      cap.setAttribute('aria-hidden', String(o < 0.5));
    });
    legA.style.opacity = String(1 - smooth(u4));
    legB.style.opacity = String(smooth(u4));
  }

  function progress() {
    var r = sec.getBoundingClientRect();
    return clamp(-r.top / (sec.offsetHeight - window.innerHeight), 0, 1);
  }
  var queued = false;
  window.addEventListener('scroll', function () {
    if (queued) return; queued = true;
    requestAnimationFrame(function () { queued = false; draw(); });
  }, { passive: true });
  if ('ResizeObserver' in window) new ResizeObserver(function () { requestAnimationFrame(build); }).observe(canvas); else { window.addEventListener('resize', build); build(); }
})();


/* ============================================================
   5. ТОЧНОСТЬ — 1000 беременных: ложные тревоги скрининга и НИПТ.
   Переключатель на пружине (damping 1), точки гаснут волной.
   ============================================================ */
(function () {
  var root = document.getElementById('fpv');
  if (!root) return;
  var RM = window.matchMedia('(prefers-reduced-motion: reduce)');
  var canvas = root.querySelector('canvas'), ctx = canvas.getContext('2d');
  var thumb = root.querySelector('.fpv__thumb');
  var btns = Array.prototype.slice.call(root.querySelectorAll('.fpv__seg button'));
  var v0 = root.querySelector('.fpv__v0'), v1 = root.querySelector('.fpv__v1');
  var N = 1000, cols = 50, W = 0, H = 0, cell = 10, dpr = 1, touched = false;
  var seed = 5;
  function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
  var fp = [], keep = -1;
  while (fp.length < 50) { var i = Math.floor(rnd() * N); if (fp.indexOf(i) < 0) fp.push(i); }
  keep = fp[0];
  var fpSet = {}; fp.forEach(function (i, k) { fpSet[i] = k; });
  function clamp(v, a, b) { return Math.min(b, Math.max(a, v)); }

  // пружина: значение 0 — скрининг, 1 — НИПТ; стартует с текущей точки и скорости
  function Spring(x, on) { this.x = x; this.v = 0; this.t = x; this.raf = 0; this.on = on; this.tick = this.tick.bind(this); }
  Spring.prototype.to = function (t, response) {
    this.t = t;
    if (RM.matches) { this.x = t; this.v = 0; this.on(t); return; }
    var w = 2 * Math.PI / response; this.k = w * w; this.c = 2 * w;
    if (!this.raf) { this.last = performance.now(); this.raf = requestAnimationFrame(this.tick); }
  };
  Spring.prototype.tick = function (now) {
    var dt = Math.min((now - this.last) / 1000, 0.064); this.last = now;
    var n = Math.max(1, Math.ceil(dt / 0.004)), h = dt / n;
    for (var i = 0; i < n; i++) { var a = -this.k * (this.x - this.t) - this.c * this.v; this.v += a * h; this.x += this.v * h; }
    if (Math.abs(this.x - this.t) < 0.001 && Math.abs(this.v) < 0.01) { this.x = this.t; this.v = 0; this.raf = 0; this.on(this.x); return; }
    this.on(this.x); this.raf = requestAnimationFrame(this.tick);
  };

  function layout() {
    if (canvas.clientWidth === W && W) return;
    W = canvas.clientWidth;
    cols = W < 480 ? 40 : 50;
    cell = W / cols;
    H = Math.ceil(N / cols) * cell;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr); canvas.style.height = H + 'px';
    draw(m.x);
  }
  function draw(x) {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    for (var i = 0; i < N; i++) {
      var c = i % cols, r = Math.floor(i / cols);
      var on = 0;
      if (i in fpSet) {
        if (i === keep) on = 1;
        else on = 1 - clamp(x * 1.5 - (fpSet[i] / 50) * 0.5, 0, 1);   // гаснут по очереди
      }
      var rad = cell * (0.3 + 0.08 * on);
      ctx.fillStyle = on > 0.01 ? 'rgba(245,165,36,' + (0.35 + 0.65 * on) + ')' : '#C9D6E8';
      if (on <= 0.01) ctx.fillStyle = '#C9D6E8';
      ctx.beginPath(); ctx.arc((c + 0.5) * cell, (r + 0.5) * cell, rad, 0, 6.2832); ctx.fill();
    }
    v0.style.opacity = String(clamp(1 - x * 1.4, 0, 1));
    v1.style.opacity = String(clamp(x * 1.4 - 0.4, 0, 1));
  }
  var m = new Spring(0, draw);
  var th = new Spring(0, function (x) { thumb.style.transform = 'translate3d(' + (x * 100) + '%,0,0)'; });
  function set(mode, response) {
    btns.forEach(function (b) { b.setAttribute('aria-pressed', String(+b.dataset.m === mode)); });
    th.to(mode, 0.32);
    m.to(mode, response);
  }
  btns.forEach(function (b) {
    b.addEventListener('pointerdown', function () { touched = true; });
    b.addEventListener('click', function () { set(+b.dataset.m, 0.9); });
  });
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) {
        if (!en.isIntersecting) return;
        io.disconnect();
        setTimeout(function () { if (!touched) set(1, 1.4); }, 700);
      });
    }, { threshold: 0.5 });
    io.observe(canvas);
  }
  if ('ResizeObserver' in window) new ResizeObserver(function () { requestAnimationFrame(layout); }).observe(canvas); else { window.addEventListener('resize', layout); layout(); }
})();
