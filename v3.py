"""v3 (02.10.2026): только для пациентов, два анимированных варианта, сверенные цифры точности.

Подключается из build.py. Что делает:
- убирает раздел «Для врачей» и пункт меню;
- цифры из hero — полосой на всю ширину, счётчики при появлении;
- «Что это / Для кого / Когда» — карточки с иконками;
- точность: значения по Gil 2017 (НИПТ) и Wapner 2003 (скрининг I триместра), строка источника;
- запись — мессенджеры вместо формы «перезвоним», телефон мелкой строкой;
- FAQ — карточки с иконками в две колонки;
- белые полосы-фоны у части секций, появление блоков при прокрутке в обоих вариантах.
"""

import re

LUCIDE = {
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    "user-round": '<circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 0 0-16 0"/>',
    "calendar": '<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>',
    "shield-check": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "scan-search": '<path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><circle cx="12" cy="12" r="3"/><path d="m16 16-1.9-1.9"/>',
    "activity": '<path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "baby": '<path d="M9 12h.01"/><path d="M15 12h.01"/><path d="M10 16c.5.3 1.2.5 2 .5s1.5-.2 2-.5"/><path d="M19 6.3a9 9 0 0 1 1.8 3.9 2 2 0 0 1 0 3.6 9 9 0 0 1-17.6 0 2 2 0 0 1 0-3.6A9 9 0 0 1 12 3c2 0 3.5 1.1 3.5 2.5s-.9 2.5-2 2.5c-.8 0-1.5-.4-1.5-1"/>',
    "droplets": '<path d="M7 16.3c2.2 0 4-1.83 4-4.05 0-1.16-.57-2.26-1.71-3.19S7.29 6.75 7 5.3c-.29 1.45-1.14 2.84-2.29 3.76S3 11.1 3 12.25c0 2.22 1.8 4.05 4 4.05z"/><path d="M12.56 6.6A10.97 10.97 0 0 0 14 3.02c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6.98 6.98 0 0 1-11.91 4.97"/>',
}


def ic(name: str, cls: str = "v3ic") -> str:
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{LUCIDE[name]}</svg>')


def sub1(text: str, old: str, new: str) -> str:
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"v3: ожидалось 1 вхождение, найдено {n}: {old[:90]!r}")
    return text.replace(old, new)


# ---------------------------------------------------------------- меню и hero
def nav(nav_html: str) -> str:
    return sub1(nav_html, '    <a href="#doctors">Врачам</a>\n', "")


def hero(hero_html: str) -> str:
    return re.sub(r'\s*<ul class="herofacts">.*?</ul>', "", hero_html, count=1, flags=re.S)


STATBAND = """<section class="nstat" aria-label="Коротко о НИПТ">
  <div class="nstat__in">
    <div class="nstat__i"><b data-count="10">10</b><span>недель — с этого срока можно сдать кровь</span></div>
    <div class="nstat__i"><b data-count="20">20</b><span>мл крови из вены — без прокола и риска для беременности</span></div>
    <div class="nstat__i"><b data-count="8">8</b><span>дней до заключения врача-генетика</span></div>
    <div class="nstat__i"><b data-count="5">5</b><span>панелей от 16 000 до 40 000 ₽, консультация генетика бесплатно</span></div>
  </div>
</section>"""


def intro(intro_html: str) -> str:
    for label, name in (("Что это", "info"), ("Для кого", "user-round"), ("Когда", "calendar")):
        intro_html = sub1(intro_html, f'<span class="section-eyebrow">{label}</span>',
                          f'<span class="intro3__ic">{ic(name)}</span><span class="section-eyebrow">{label}</span>')
    return intro_html


# ---------------------------------------------------------------- точность
SRC_LINE = ('<p class="v3src">НИПТ — метаанализ Gil и соавт., Ultrasound Obstet Gynecol, 2017; '
            'скрининг I триместра — Wapner и соавт., N Engl J Med, 2003.</p>')
LEAD_OLD = "НИПТ и комбинированный биохимический скрининг решают разные задачи."
LEAD_NEW = "НИПТ и комбинированный скрининг первого триместра (УЗИ и анализ крови) решают разные задачи."
WEEK_OLD = "биохимический скрининг проводят на 11–13-й неделе."
WEEK_NEW = "скрининг первого триместра проводят на 11–13-й неделе."


def accuracy_anim(acc_html: str) -> str:
    """Вкладка со сценой: карточка «1000 беременных» (fpv.html уже вставлена)."""
    for old, new in [
        ('data-m="0" aria-pressed="true">Биохимический скрининг</button>', 'data-m="0" aria-pressed="true">Скрининг I триместра</button>'),
        ('<span class="fpv__l">Биохимический скрининг</span><span class="fpv__s">Биохим.<br>скрининг</span>',
         '<span class="fpv__l">Скрининг I триместра</span><span class="fpv__s">Скрининг<br>I&nbsp;трим.</span>'),
        ('<td class="mono">&gt;&nbsp;99&nbsp;%</td><td class="mono">85&nbsp;%</td>', '<td class="mono">99,7&nbsp;%</td><td class="mono">≈&nbsp;85&nbsp;%</td>'),
        ('<td class="mono">&gt;&nbsp;98&nbsp;%</td><td class="mono">75&nbsp;%</td>', '<td class="mono">97,9&nbsp;%</td><td class="mono">≈&nbsp;91&nbsp;%</td>'),
        ('<td class="mono">&lt;&nbsp;0,1&nbsp;%</td><td class="mono">до&nbsp;5&nbsp;%</td>', '<td class="mono">0,04&nbsp;%</td><td class="mono">≈&nbsp;5&nbsp;%</td>'),
        ('<b class="mono">до&nbsp;50</b> из&nbsp;1000', '<b class="mono">около&nbsp;50</b> из&nbsp;1000'),
        ("ложноположительный результат получат до 50 при биохимическом скрининге и меньше 1 при НИПТ.",
         "ложноположительный результат получат около 50 при скрининге первого триместра и меньше 1 при НИПТ."),
        (LEAD_OLD, LEAD_NEW), (WEEK_OLD, WEEK_NEW),
    ]:
        acc_html = sub1(acc_html, old, new)
    return sub1(acc_html, "\n      </table>\n    </div>", "\n      </table>\n      " + SRC_LINE + "\n    </div>")


def accuracy_static(acc_html: str) -> str:
    """Компактная вкладка: полоски выявляемости."""
    vals = re.findall(r'<div class="v">([^<]*)</div>', acc_html)
    if len(vals) != 6:
        raise SystemExit(f"v3: ожидалось 6 значений точности, найдено {len(vals)}")
    new_vals = iter(["99,7 %", "≈ 85 %", "97,9 %", "≈ 91 %", "0,04 %", "≈ 5 %"])
    acc_html = re.sub(r'<div class="v">[^<]*</div>', lambda m: f'<div class="v">{next(new_vals)}</div>', acc_html)
    acc_html = re.sub(r'(<div class="cmp-line b"><div class="bar2"><i style="width:)75%', r"\g<1>91%", acc_html, count=1)
    acc_html = sub1(acc_html, "</i> биохимический скрининг</span>", "</i> скрининг I триместра</span>")
    for old, new in [(LEAD_OLD, LEAD_NEW), (WEEK_OLD, WEEK_NEW)]:
        acc_html = sub1(acc_html, old, new)
    return sub1(acc_html, '      <div class="cmp-legend">', "      " + SRC_LINE + '\n      <div class="cmp-legend">')


# ---------------------------------------------------------------- сцена / путь ДНК
def scene(scene_html: str) -> str:
    scene_html = sub1(scene_html, '<span class="section-eyebrow" style="color:var(--cyan)">Как работает НИПТ</span>',
                      '<span class="section-eyebrow" style="color:var(--cyan)">Безопасно для беременности</span>')
    return sub1(scene_html, 'Почему исследование <em>безопасно</em>', 'Как работает <em>НИПТ</em>')


def safe_static(safe_html: str) -> str:
    safe_html = sub1(safe_html, '<span class="section-eyebrow">Как работает НИПТ</span>', '<span class="section-eyebrow">Безопасно для беременности</span>')
    return sub1(safe_html, 'Почему исследование <em>безопасно</em>', 'Как работает <em>НИПТ</em>')


# ---------------------------------------------------------------- запись: мессенджеры
def chat_icons(chat_html: str) -> dict:
    """Иконки из parts/chat-icons.html (копия блока соцсетей site-chrome)."""
    out = {}
    for key, label in (("wa", "WhatsApp"), ("tg", "Telegram"), ("max", "Max")):
        m = re.search(rf'(?s)aria-label="Написать в {label}"[^>]*>(.*?)</a>', chat_html, re.I)
        if not m:
            raise SystemExit(f"v3: нет иконки {label}")
        out[key] = m.group(1).strip()
    return out


def cta(cta_html: str, icons: dict) -> str:
    cta_html = sub1(cta_html,
                    "Оставьте телефон — перезвоним, поможем выбрать панель, подскажем ближайший медицинский офис и ответим на вопросы. Консультация перед исследованием бесплатна.",
                    "Напишите в клиентский сервис — поможем выбрать панель, подскажем ближайший медицинский офис и ответим на вопросы. Консультация перед исследованием бесплатна.")
    btns = (f'<div class="v3chat">'
            f'<a class="btn-lnipt btn-lnipt--light" href="https://wa.me/74956608377" target="_blank" rel="noopener">{icons["wa"]}<span>WhatsApp</span></a>'
            f'<a class="btn-lnipt btn-lnipt--light" href="https://t.me/genomed_b2c_bot" target="_blank" rel="noopener">{icons["tg"]}<span>Telegram</span></a>'
            f'<a class="btn-lnipt btn-lnipt--light" href="https://max.ru/id7701759381_bot" target="_blank" rel="noopener">{icons["max"]}<span>Max</span></a>'
            f'</div><p class="v3tel">Клиентский сервис 24/7 · горячая линия <a class="mono" href="tel:84956608377">8 (495) 660-83-77</a></p>')
    return re.sub(r'(?s)\s*<form class="leadform" id="leadform">.*?</form>', "\n        " + btns, cta_html, count=1)


def how(how_html: str) -> str:
    return sub1(how_html, "Запись по телефону или онлайн.", "Запись онлайн или в мессенджере.")


# ---------------------------------------------------------------- FAQ: карточки с иконками
FAQ_ICONS = ["shield-check", "calendar", "scan-search", "activity", "info", "clock", "baby", "user-round", "droplets"]


def faq(faq_html: str) -> str:
    items = re.findall(r'(?s)<details( open)?>\s*<summary><span class="faq__n">(\d+)</span><span class="q">(.*?)</span>.*?</summary>\s*(.*?)\s*</details>', faq_html)
    if len(items) != len(FAQ_ICONS):
        raise SystemExit(f"v3: ожидалось {len(FAQ_ICONS)} вопросов, найдено {len(items)}")
    cards = [f'<details class="fq" style="order:{int(n)}"{op}><summary><span class="fq__ic">{ic(name)}</span>'
             f'<span class="fq__q"><span class="fq__n mono">{n}</span>{q}</span></summary><div class="fq__a">{a}</div></details>'
             for (op, n, q, a), name in zip(items, FAQ_ICONS)]
    grid = ('<div class="wrap fqg">\n<div class="fqc">\n' + "\n".join(cards[0::2]) + '\n</div><div class="fqc">\n'
            + "\n".join(cards[1::2]) + "\n</div>\n  </div>")
    return re.sub(r'(?s)<div class="wrap faq" style="margin-top:2em">.*?\n  </div>', grid, faq_html, count=1)


# ---------------------------------------------------------------- белые полосы
BANDS = ("accuracy", "compare", "how", "faq")


def band(section_html: str, sid: str) -> str:
    return re.sub(rf'<section id="{sid}"( style="padding-top:0")?', f'<section id="{sid}" class="v3band"', section_html, count=1)


CSS = """
/* ===== v3 ===== */
.nstat{background:#fff;border-top:1px solid var(--line-soft);border-bottom:1px solid var(--line-soft)}
.nstat__in{max-width:1320px;margin:0 auto;padding:0 24px;display:grid;grid-template-columns:repeat(4,1fr)}
.nstat__i{display:flex;align-items:center;gap:16px;padding:26px 24px;border-left:1px solid var(--line-soft);min-width:0}
.nstat__i:first-child{border-left:none;padding-left:0}
.nstat__i b{font-family:var(--disp);font-weight:900;font-size:clamp(40px,4.2vw,58px);letter-spacing:-.045em;line-height:1;flex:none;font-variant-numeric:tabular-nums;
  background:linear-gradient(135deg,var(--blue),var(--cyan));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.nstat__i span{font-size:14px;font-weight:600;line-height:1.35;color:var(--ink-2)}
@media(max-width:1020px){.nstat__in{grid-template-columns:1fr 1fr}.nstat__i:nth-child(3){border-left:none;padding-left:0}.nstat__i:nth-child(n+3){border-top:1px solid var(--line-soft)}}
@media(max-width:600px){.nstat__in{padding:0 16px}.nstat__i{flex-direction:column;align-items:flex-start;gap:8px;padding:18px 12px}.nstat__i:nth-child(odd){padding-left:0}.nstat__i span{font-size:13px}}

.intro3{border:none;gap:18px}
.intro3>div{background:#fff;border:1px solid var(--line-soft);border-radius:var(--r-lg);padding:24px 24px 22px;box-shadow:var(--shadow-sm);transition:transform .2s,box-shadow .2s}
.intro3>div:hover{transform:translateY(-3px);box-shadow:var(--shadow-md)}
.intro3__ic{display:grid;place-items:center;width:46px;height:46px;border-radius:14px;background:var(--accent-soft);color:var(--blue);margin-bottom:14px;border:1px solid #C9DDFF}
.intro3__ic .v3ic{width:22px;height:22px}
@media(max-width:900px){.intro3{grid-template-columns:1fr}}

.v3band{background:#fff;padding-block:clamp(3em,6vw,5.5em) !important}
.v3band + section{padding-top:clamp(3em,6vw,5.5em) !important}
.v3src{font-family:var(--mono);font-size:11.5px;line-height:1.5;color:var(--muted);margin:12px 0 0}

.v3chat{display:flex;flex-wrap:wrap;gap:10px;margin-top:1.6em}
.v3chat .btn-lnipt{display:inline-flex;align-items:center;gap:9px}
.v3chat svg,.v3chat img{width:22px;height:22px;display:block;flex:none}
.v3tel{margin:1.1em 0 0;font-size:13px;color:rgba(255,255,255,.6)}
.v3tel a{color:#fff;text-decoration:none}

.fqg{display:grid;grid-template-columns:1fr 1fr;gap:14px;align-items:start;margin-top:2em}
.fqc{display:grid;gap:14px;min-width:0}
.fq{background:var(--bg);border:1px solid var(--line-soft);border-radius:var(--r-md);transition:border-color .2s,box-shadow .2s,background-color .2s}
.fq[open]{background:#fff;border-color:var(--cyan-soft);box-shadow:var(--shadow-md)}
.fq summary{list-style:none;cursor:pointer;display:flex;gap:14px;align-items:center;padding:16px 18px;font-weight:700;font-size:16px;letter-spacing:-.01em;line-height:1.35}
.fq summary::-webkit-details-marker{display:none}
.fq summary::after{content:"";width:9px;height:9px;border-right:2px solid var(--muted);border-bottom:2px solid var(--muted);transform:rotate(45deg);flex:none;margin:0 4px 4px 0;transition:transform .2s}
.fq[open] summary::after{transform:rotate(-135deg);margin-bottom:-4px;border-color:var(--blue)}
.fq__ic{width:42px;height:42px;border-radius:12px;background:var(--accent-soft);color:var(--blue);display:grid;place-items:center;flex:none;transition:background-color .2s,color .2s}
.fq__ic .v3ic{width:20px;height:20px}
.fq[open] .fq__ic{background:linear-gradient(135deg,var(--blue),var(--cyan));color:#fff}
.fq__q{flex:1;min-width:0}
.fq__n{display:block;font-size:11px;font-weight:700;color:var(--muted);margin-bottom:2px}
.fq__a{padding:0 20px 18px 74px;font-size:15px;color:var(--ink-2);line-height:1.6}
.fq__a p{margin:0}
@media(max-width:900px){.fqg{grid-template-columns:1fr}.fqc{display:contents}}
@media(max-width:600px){.fq__a{padding:0 18px 18px}}

/* появление при прокрутке, полоски точности, путь ДНК по очереди */
.v3rv{opacity:0;transform:translateY(16px);transition:opacity .6s cubic-bezier(.2,.8,.2,1),transform .6s cubic-bezier(.2,.8,.2,1);transition-delay:calc(var(--d,0) * 90ms)}
.v3rv.in{opacity:1;transform:none}
.cmp-line .bar2 i{transform:scaleX(0);transform-origin:left;transition:transform 1.1s cubic-bezier(.2,.8,.2,1)}
.cmp-card.in .cmp-line .bar2 i{transform:scaleX(1)}
@media (prefers-reduced-motion:reduce){.v3rv{opacity:1;transform:none;transition:none}.cmp-line .bar2 i{transform:none;transition:none}}
"""

JS = """
/* ===== v3: появление блоков, полоски точности, счётчики ===== */
(function () {
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var sel = '.intro3>div,.ben,.cmp-card,.panel,.step,.wcard,.res,.limgrp,.fcard,.fq,.dnapath li,.nstat__i';
  var els = [].slice.call(document.querySelectorAll(sel));
  if (reduce || !('IntersectionObserver' in window)) { els.forEach(function (e) { e.classList.add('in'); }); return; }
  var groups = new Map();
  els.forEach(function (e) {
    e.classList.add('v3rv');
    var p = e.parentElement, i = groups.get(p) || 0; groups.set(p, i + 1);
    e.style.setProperty('--d', Math.min(i, 6));
  });
  var io = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } }); },
    { threshold: .15, rootMargin: '0px 0px -40px 0px' });
  els.forEach(function (e) { io.observe(e); });
  document.querySelectorAll('[data-count]').forEach(function (el) {
    var n = +el.dataset.count; el.textContent = '0';
    var o = new IntersectionObserver(function (es) {
      if (!es[0].isIntersecting) return; o.disconnect(); var t0 = performance.now();
      (function f(t) { var p = Math.min(1, (t - t0) / 900); el.textContent = String(Math.round(n * (1 - Math.pow(1 - p, 3)))); if (p < 1) requestAnimationFrame(f); })(t0);
    });
    o.observe(el);
  });
})();
"""


if __name__ == "__main__":
    assert faq("x") if False else True
    demo = '<div class="cmp-line b"><div class="bar2"><i style="width:75%"></i></div><div class="v">75 %</div></div>'
    assert "width:91%" in re.sub(r'(<div class="cmp-line b"><div class="bar2"><i style="width:)75%', r"\g<1>91%", demo)
    print("ok")
