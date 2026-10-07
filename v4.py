"""v4 (06.10.2026): первый экран называет исследование, меньше карточек.

Подключается из build.py после v3. Что делает:
- первый экран: заголовок — название исследования «НИПТ — неинвазивный пренатальный тест»,
  строка простым языком и выжимка в три предложения: что это, кому, когда;
  иллюстрация «плацента → ДНК в крови мамы» во всю ширину, текст по центру (как у Фемабиома);
- под первым экраном — только полоса из четырёх цифр (v3.STATBAND), без карточек «Что это / Для кого / Когда»;
- квиз «Не знаете, какой НИПТ выбрать?»: шесть вопросов, лесенка панелей сбоку;
- «Что вы получаете» и вопросы — без рамок-карточек;
- «Что может показать заключение» — таблица-развилка «исход → что значит → что дальше»;
- из сцены убрана подпись про условный масштаб;
- «Когда НИПТ не подходит» переезжает вниз страницы, перед записью (порядок — в build.py).
"""

import re

from v3 import ic, sub1


# ---------------------------------------------------------------- первый экран
H1_OLD = '<h1>Риск синдрома Дауна у&nbsp;малыша&nbsp;— по&nbsp;анализу <em>крови мамы</em></h1>'
H1_NEW = ('<h1 class="v4h1"><em>НИПТ</em>&nbsp;— неинвазивный пренатальный тест</h1>\n'
          '      <p class="v4tag">Анализ крови мамы для точной оценки риска хромосомных аномалий у&nbsp;малыша</p>')
LEAD_OLD = ('<p class="lead">НИПТ — неинвазивный пренатальный тест. С 10-й недели беременности по крови мамы он оценивает '
            'вероятность синдрома Дауна и других хромосомных аномалий у плода — без прокола и риска для беременности. '
            'Заключение врача-генетика — через 8 дней.</p>')
LEAD_NEW = ('<p class="lead v4sum">Скрининг по&nbsp;ДНК плода в&nbsp;крови мамы: оценивает вероятность синдрома Дауна '
            'и&nbsp;других частых хромосомных аномалий. Рекомендуют всем беременным, особенно после 35&nbsp;лет, после ЭКО '
            'и&nbsp;при повышенном риске по&nbsp;биохимическому скринингу. Сдают с&nbsp;10 полных недель, заключение '
            'врача-генетика&nbsp;— через&nbsp;8&nbsp;дней.</p>')


def hero(hero_html: str) -> str:
    hero_html = sub1(hero_html, '      <p class="eyebrow">НИПТ · с 10 недель беременности</p>\n', "")
    hero_html = sub1(hero_html, H1_OLD, H1_NEW)
    return sub1(hero_html, LEAD_OLD, LEAD_NEW)


# ---------------------------------------------------------------- исходы: таблица-развилка
RESULTS = """<section id="results">
  <div class="wrap section-head">
    <span class="section-eyebrow">Результат</span>
    <h2>Что может показать <em>заключение</em></h2>
    <p class="lead">Заключение приходит на&nbsp;электронную почту через 8&nbsp;дней. Врач-генетик разбирает его вместе с&nbsp;вами и&nbsp;объясняет, что делать дальше.</p>
  </div>
  <div class="wrap">
    <div class="v4fork" role="table" aria-label="Варианты заключения">
      <div class="v4fork__hd" role="row"><span role="columnheader">Заключение</span><span role="columnheader">Что это значит</span><span role="columnheader">Что дальше</span></div>
      <div class="v4fork__row v4fork__row--ok" role="row">
        <div class="v4fork__k" role="cell"><i></i><b>Низкий риск</b></div>
        <p role="cell">Вероятность исследованных хромосомных аномалий у&nbsp;плода низкая.</p>
        <p role="cell">Беременность ведут как обычно: наблюдение у&nbsp;акушера-гинеколога и&nbsp;плановые УЗИ.</p>
      </div>
      <div class="v4fork__row v4fork__row--hi" role="row">
        <div class="v4fork__k" role="cell"><i></i><b>Высокий риск</b></div>
        <p role="cell">Вероятность аномалии повышена, но&nbsp;это ещё не&nbsp;диагноз&nbsp;— результат нужно подтвердить.</p>
        <p role="cell">Врач-генетик направит на&nbsp;амниоцентез или биопсию ворсин хориона. В&nbsp;расширенной и&nbsp;экспертной панелях хромосомный микроматричный анализ при высоком риске&nbsp;— бесплатно.</p>
      </div>
      <div class="v4fork__row v4fork__row--na" role="row">
        <div class="v4fork__k" role="cell"><i></i><b>Нет результата</b></div>
        <p role="cell">В&nbsp;крови мало ДНК плода: плодная фракция ниже 4&nbsp;%, надёжно оценить риск нельзя.</p>
        <p role="cell">Лаборатория бесплатно повторит анализ по&nbsp;новому образцу крови на&nbsp;более позднем сроке, генетик обсудит дальнейшую тактику.</p>
      </div>
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------- запись: НИПТ одинаковый на любом сроке, «под ваш срок» не по смыслу
CTA_H2_OLD = 'Подберём НИПТ <em style="color:var(--cyan)">под ваш срок</em> беременности'
CTA_H2_NEW = 'Поможем <em style="color:var(--cyan)">выбрать панель</em> и&nbsp;записаться'


def cta(cta_html: str) -> str:
    return sub1(cta_html, CTA_H2_OLD, CTA_H2_NEW)


# ---------------------------------------------------------------- сцена без подписи про масштаб
FINE = '<span class="nleg__fine">схема: разница показана крупнее, чем в&nbsp;реальности</span>'


def scene(scene_html: str) -> str:
    return sub1(scene_html, FINE, "") if FINE in scene_html else scene_html


CSS = """
/* ===== v4: первый экран — название исследования ===== */
.hero .v4h1{font-size:clamp(34px,4.4vw,58px)}
.v4tag{margin:.55em 0 0;font-family:var(--disp);font-weight:700;font-size:clamp(19px,1.9vw,24px);line-height:1.3;letter-spacing:-.015em;color:var(--ink);max-width:30em;text-wrap:balance}
.hero .v4sum{margin-top:1.1em;max-width:36em}
.v4hero{position:relative;overflow:hidden;display:grid;place-items:center;min-height:clamp(560px,46vw,700px);padding-block:clamp(3em,5vw,4.5em) !important;background:#FBF3F3}
.v4hero__pic{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 45%}
.v4hero::before{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;
  background:radial-gradient(50% 70% at 50% 50%,rgba(255,255,255,.92) 0%,rgba(255,255,255,.8) 55%,rgba(255,255,255,0) 85%)}
.v4hero__in{position:relative;z-index:2;text-align:center}
.v4hero__in>div{max-width:840px;margin-inline:auto}
.v4hero .v4h1{max-width:900px;margin-inline:auto}
.v4hero .v4tag,.v4hero .v4sum{margin-inline:auto}
.v4hero .v4sum{max-width:44em}
.v4hero .hero-cta{justify-content:center}
@media(max-width:760px){
  .v4hero{display:block;min-height:0;padding-bottom:0 !important;background:linear-gradient(180deg,var(--bg) 0%,#FBF1F1 100%)}
  .v4hero::before{display:none}
  .v4hero__in{text-align:left}.v4hero .hero-cta{justify-content:flex-start}
  .v4hero__pic{position:static;display:block;height:auto;margin-top:2em}
}

/* ===== v4: «Что вы получаете» — список без рамок ===== */
.bens .ben{background:none !important;border:none !important;box-shadow:none !important;border-radius:0 !important;padding:1.1em 0 0 !important;border-top:2px solid var(--ink) !important}
.bens .ben h3{margin:.7em 0 .35em}

/* ===== v4: исходы — таблица-развилка ===== */
.v4fork{border-top:2px solid var(--ink);margin-top:clamp(1.8em,3vw,2.6em)}
.v4fork__hd,.v4fork__row{display:grid;grid-template-columns:minmax(0,.7fr) minmax(0,1fr) minmax(0,1.3fr);gap:clamp(1em,3vw,2.4em)}
.v4fork__hd{padding:.9em 0;border-bottom:1px solid var(--line)}
.v4fork__hd span{font:700 .72em/1.4 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.v4fork__row{padding:1.4em 0;border-bottom:1px solid var(--line);align-items:start}
.v4fork__row p{margin:0;color:var(--ink-2);line-height:1.55}
.v4fork__k{display:flex;align-items:center;gap:.7em}
.v4fork__k b{font-family:var(--disp);font-weight:800;font-size:1.15em;letter-spacing:-.015em;color:var(--c)}
.v4fork__k i{width:12px;height:12px;border-radius:50%;background:var(--c);box-shadow:0 0 0 5px var(--s);flex:none}
.v4fork__row--ok{--c:var(--ok);--s:var(--ok-soft)}
.v4fork__row--hi{--c:var(--stop);--s:var(--stop-soft)}
.v4fork__row--na{--c:var(--warn);--s:var(--warn-soft)}
@media(max-width:760px){
  .v4fork__hd{display:none}
  .v4fork__row{grid-template-columns:minmax(0,1fr);gap:.55em}
  .v4fork__row p+p{color:var(--ink)}
  .v4fork__row p+p::before{content:"Что дальше: ";font-weight:700}
}

"""


# ---------------------------------------------------------------- «Как работает НИПТ» по шагам (вместо сцены на прокрутке)
SIZES = [248, 242, 198, 190, 181, 171, 159, 145, 138, 134, 135, 133, 114, 107, 102, 90, 83, 80, 59, 64, 47, 51]  # длины хромосом, млн п. н.


def _count_svg() -> str:
    """Этап 4: столбики 22 хромосом в пастельной гамме иллюстраций, капсулы фрагментов падают в столбики."""
    x0, x1, base, hmax = 110, 1290, 600, 430
    step = (x1 - x0) / 22
    bw = step * 0.62
    bars, labels, caps = [], [], []
    for k, s in enumerate(SIZES):
        h = hmax * s / max(SIZES)
        x = x0 + k * step + (step - bw) / 2
        hp = h * 0.36  # короткое плечо над перетяжкой
        bars.append(f'<g class="v4bar" style="--d:{k * 30}ms">'
                    f'<rect x="{x:.1f}" y="{base - h:.1f}" width="{bw:.1f}" height="{hp:.1f}" rx="{bw / 2:.1f}"/>'
                    f'<rect x="{x:.1f}" y="{base - h + hp + 5:.1f}" width="{bw:.1f}" height="{h - hp - 5:.1f}" rx="{bw / 2:.1f}"/>'
                    f'<rect class="v4hl" x="{x + bw * 0.2:.1f}" y="{base - h + bw * 0.35:.1f}" width="{bw * 0.16:.1f}" height="{max(h - bw * 0.7, 4):.1f}" rx="{bw * 0.08:.1f}"/></g>'
                    f'<line class="v4exp" x1="{x - 6:.1f}" x2="{x + bw + 6:.1f}" y1="{base - h - 10:.1f}" y2="{base - h - 10:.1f}"/>')
        labels.append(f'<text x="{x + bw / 2:.1f}" y="{base + 46}">{k + 1}</text>')
    for j, (k, c) in enumerate([(0, "b"), (3, "o"), (6, "b"), (9, "b"), (12, "o"), (15, "b"), (17, "b"), (20, "o"), (21, "b"), (5, "o"), (11, "b"), (19, "b")]):
        h = hmax * SIZES[k] / max(SIZES)
        cx = x0 + k * step + step / 2
        caps.append(f'<rect class="v4frag v4frag--{c}" style="--d:{300 + j * 90}ms;--y:{base - h - 30:.0f}px" x="{cx - 15:.1f}" y="0" width="30" height="14" rx="7"/>')
    return (f'<svg class="v4count" viewBox="0 0 1400 700" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            '<defs><linearGradient id="v4bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FCEFF3"/><stop offset="1" stop-color="#EDF0FF"/></linearGradient>'
            '<linearGradient id="v4bar" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#C4CEFF"/><stop offset=".55" stop-color="#9FB1F7"/><stop offset="1" stop-color="#8396EC"/></linearGradient>'
            '<filter id="v4glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="10"/></filter><filter id="v4sh" x="-50%" y="-10%" width="200%" height="130%"><feDropShadow dx="0" dy="8" stdDeviation="8" flood-color="#5A6FD6" flood-opacity=".22"/></filter></defs>'
            '<rect width="1400" height="700" fill="url(#v4bg)"/>'
            '<circle cx="1180" cy="120" r="140" fill="#fff" opacity=".45" filter="url(#v4glow)"/><circle cx="210" cy="600" r="120" fill="#FFD9D3" opacity=".35" filter="url(#v4glow)"/>'
            '<g fill="url(#v4bar)" filter="url(#v4sh)">' + "".join(bars) + "</g>"
            '<g class="v4lbl">' + "".join(labels) + "</g>"
            + "".join(caps)
            + f'<line x1="{x0}" x2="{x1}" y1="{base + 12}" y2="{base + 12}" stroke="#C9CFF0" stroke-width="2"/></svg>')


def _chip(x: float, y: float, text: str, tone: str = "b", n: int = 0, cls: str = "") -> str:
    """Чип-подпись поверх иллюстрации; cls="v4chip--l" — привязка к левому краю, а не к центру."""
    return f'<span class="v4chip v4chip--{tone} {cls}" style="left:{x}%;top:{y}%;--n:{n}"><i></i>{text}</span>'


HOW_STEPS = [
    ("Кровь мамы", "В&nbsp;крови мамы есть фрагменты ДНК плаценты.",
     "С&nbsp;10-й недели беременности их&nbsp;доля&nbsp;— плодная фракция&nbsp;— обычно достигает 4&nbsp;% и&nbsp;больше. Этого достаточно для анализа.",
     '<img src="img/step-1-blood.webp" alt="" width="1440" height="720" loading="lazy">'),  # подписи нарисованы на самой картинке
    ("Взятие крови", "Достаточно 20&nbsp;мл крови из&nbsp;вены.",
     "Как для обычного анализа&nbsp;— без прокола и&nbsp;риска для беременности. Из&nbsp;плазмы выделяют внеклеточную ДНК.",
     '<img src="img/step-2-tube.webp" alt="" width="1774" height="887" loading="lazy">'
     + _chip(55, 18, "20&nbsp;мл из&nbsp;вены", "r", 0) + _chip(30, 84, "без прокола и&nbsp;риска", "b", 1, "v4chip--hide-sm")),
    ("Секвенирование", "Секвенатор прочитывает фрагменты ДНК.",
     "Программа определяет, с&nbsp;какой хромосомы пришёл каждый фрагмент.",
     '<img src="img/step-3-reads.webp" alt="" width="1774" height="887" loading="lazy">'
     '<span class="v4reads" style="--n:0"><b>пример прочтений</b>'
     '<span>…GATTACAGGT <em>→ хр.&nbsp;7</em></span><span>…CCTAGGATCC <em>→ хр.&nbsp;21</em></span><span>…TTGACCAGTA <em>→ хр.&nbsp;13</em></span></span>'),
    ("Подсчёт", "Фрагменты раскладываются по&nbsp;хромосомам.",
     "Для каждой хромосомы считается, сколько фрагментов пришлось на&nbsp;неё, и&nbsp;это число сравнивается с&nbsp;ожидаемым.",
     _count_svg() + _chip(50, 9, "пунктир&nbsp;— ожидаемое число фрагментов", "b", 0)),
    ("Результат", "Лишняя хромосома видна в&nbsp;цифрах.",
     "Если фрагментов 21-й хромосомы больше ожидаемого, это признак синдрома Дауна. Врач-генетик оценивает риск; высокий риск подтверждают диагностическим исследованием.",
     '<img src="img/step-5-result.webp" alt="" width="1774" height="887" loading="lazy">'
     + _chip(58.5, 88, "21-я: фрагментов больше ожидаемого", "r", 0)),
]

STEPS = (
    '<section class="v4how" id="safe" aria-labelledby="v4how-t">\n  <div class="wrap">\n'
    '    <div class="section-head v4how__head"><span class="section-eyebrow">Безопасно для беременности</span>'
    '<h2 id="v4how-t">Как работает <em>НИПТ</em></h2></div>\n'
    '    <div class="v4how__tabs" role="tablist" aria-label="Этапы исследования">'
    + "".join(f'<button type="button" role="tab" id="v4t{i}" aria-controls="v4p" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">'
              f'<b class="mono">0{i + 1}</b><span>{name}</span></button>' for i, (name, *_r) in enumerate(HOW_STEPS))
    + "</div>\n"
    '    <div class="v4how__body">\n      <div class="v4how__stage">'
    + "".join(f'<figure class="v4scene{" is-on" if i == 0 else ""}" data-i="{i}" aria-hidden="{"false" if i == 0 else "true"}">{art}</figure>'
              for i, (*_r, art) in enumerate(HOW_STEPS))
    + "</div>\n"
    '      <div class="v4how__cap" id="v4p" role="tabpanel" aria-labelledby="v4t0" aria-live="polite">'
    '<div class="v4how__prog" aria-hidden="true">' + "<i></i>" * len(HOW_STEPS) + "</div>"
    + "".join(f'<div class="v4cap{" is-on" if i == 0 else ""}" data-i="{i}"><span class="v4cap__n mono">0{i + 1} / 0{len(HOW_STEPS)} · {name.lower()}</span><h3>{h}</h3><p>{p}</p></div>'
              for i, (name, h, p, _a) in enumerate(HOW_STEPS))
    + '<div class="v4how__nav"><button type="button" class="v4nav" data-a="prev">← Назад</button>'
      '<button type="button" class="v4nav v4nav--next" data-a="next">Дальше →</button></div>'
    "</div>\n    </div>\n  </div>\n</section>"
)

STEPS_CSS = """
/* ===== v4: «Как работает НИПТ» по шагам ===== */
.v4how{background:#fff;padding:clamp(3em,6vw,5em) 0;border-top:1px solid var(--line-soft);border-bottom:1px solid var(--line-soft)}
.v4how__head{margin-bottom:1.4em}
.v4how__tabs{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding:2px;margin:0 -2px 18px}
.v4how__tabs::-webkit-scrollbar{display:none}
.v4how__tabs button{flex:1 0 auto;display:flex;align-items:baseline;justify-content:center;gap:.55em;padding:.85em 1.1em;border-radius:100px;border:1px solid var(--line);background:var(--bg);color:var(--ink-2);font:700 .9em/1.2 var(--body);cursor:pointer;white-space:nowrap;transition:background-color .2s ease-out,color .2s ease-out,border-color .2s ease-out}
.v4how__tabs button b{font-size:.82em;color:var(--blue)}
.v4how__tabs button[aria-selected="true"]{background:var(--bg-deep);border-color:var(--bg-deep);color:#fff}
.v4how__tabs button[aria-selected="true"] b{color:var(--cyan)}
.v4how__body{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(0,.85fr);gap:clamp(1.4em,3.4vw,3em);align-items:center}
.v4how__stage{position:relative;aspect-ratio:2/1;border-radius:28px;overflow:hidden;background:#FBF4F0;box-shadow:0 1px 2px rgba(10,37,64,.04),0 18px 50px rgba(10,37,64,.10);touch-action:pan-y}
.v4scene{position:absolute;inset:0;margin:0;opacity:0;transform:scale(1.04);transition:opacity .45s ease-out,transform .9s cubic-bezier(.2,.7,.2,1);pointer-events:none}
.v4scene.is-on{opacity:1;transform:none}
.v4scene img,.v4scene svg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.v4chip{position:absolute;transform:translate(-50%,-50%) translateY(8px);opacity:0;display:inline-flex;align-items:center;gap:.5em;padding:.5em .9em .5em .7em;border-radius:100px;
  background:rgba(255,255,255,.94);color:var(--ink);font:700 clamp(11px,1.05vw,14px)/1.2 var(--body);white-space:nowrap;box-shadow:0 6px 18px rgba(10,37,64,.12);
  transition:opacity .35s ease-out,transform .35s ease-out;transition-delay:0s}
.v4chip i{width:9px;height:9px;border-radius:50%;background:var(--c);box-shadow:0 0 0 4px var(--s)}
.v4chip--b{--c:#4F7BF7;--s:rgba(79,123,247,.18)} .v4chip--o{--c:#F08A5D;--s:rgba(240,138,93,.2)} .v4chip--r{--c:#E0524A;--s:rgba(224,82,74,.18)}
.is-on .v4chip{opacity:1;transform:translate(-50%,-50%);transition-delay:calc(.35s + var(--n) * .14s)}
.v4chip--l{transform:translate(0,-50%) translateY(8px)}
.is-on .v4chip--l{transform:translate(0,-50%)}
.v4reads{position:absolute;right:4%;bottom:7%;display:grid;gap:.3em;padding:.9em 1.1em;border-radius:16px;background:rgba(10,37,64,.86);color:#DCE8F5;
  font:600 clamp(10px,1vw,13px)/1.35 var(--mono);opacity:0;transform:translateY(10px);transition:opacity .35s ease-out .4s,transform .35s ease-out .4s}
.v4reads b{font:700 .78em var(--body);letter-spacing:.06em;text-transform:uppercase;color:#8FB6FF}
.v4reads em{font-style:normal;color:var(--cyan)}
.is-on .v4reads{opacity:1;transform:none}
.v4count .v4bar{transform-box:fill-box;transform-origin:50% 100%;transform:scaleY(.05);transition:transform .7s cubic-bezier(.2,.7,.2,1)}
.is-on .v4count .v4bar{transform:none;transition-delay:var(--d)}
.v4count .v4exp{stroke:#7486D8;stroke-width:3;stroke-dasharray:6 6;opacity:0;transition:opacity .4s ease-out .9s}
.is-on .v4count .v4exp{opacity:.9}
.v4count .v4lbl text{font:600 24px var(--mono);fill:#7A86B8;text-anchor:middle}
.v4count .v4hl{fill:#fff;opacity:.5}
.v4frag{opacity:0;transform:translateY(0);transition:none}
.v4frag--b{fill:#7C9CF5}.v4frag--o{fill:#F59A7A}
.is-on .v4frag{animation:v4drop .9s cubic-bezier(.3,.6,.3,1) var(--d) both}
@keyframes v4drop{0%{opacity:0;transform:translateY(40px)}25%{opacity:1}100%{opacity:0;transform:translateY(var(--y))}}
.v4how__prog{display:flex;gap:6px;margin-bottom:1.2em}
.v4how__prog i{flex:1;height:4px;border-radius:4px;background:var(--line-soft);transition:background-color .3s ease-out}
.v4how__prog i.on{background:var(--blue)}
.v4how__cap{display:grid}
.v4cap{grid-area:2/1;opacity:0;transform:translateY(8px);transition:opacity .3s ease-out,transform .3s ease-out;pointer-events:none}
.v4cap.is-on{opacity:1;transform:none;pointer-events:auto}
.v4cap__n{display:block;font-size:.76em;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--blue);margin-bottom:.7em}
.v4how .v4cap h3{margin:0 0 .6em !important;font-family:var(--disp);font-weight:800;font-size:clamp(22px,2.3vw,30px) !important;line-height:1.14;letter-spacing:-.025em;color:var(--ink);text-wrap:balance}
#about{padding-top:clamp(3em,6vw,5em) !important}
.v4cap p{margin:0;color:var(--ink-2);line-height:1.6}
.v4how__nav{grid-area:3/1;display:flex;gap:10px;margin-top:1.6em}
.v4nav{height:48px;padding:0 20px;border-radius:100px;border:1.5px solid var(--line);background:#fff;color:var(--ink);font:700 .92em var(--body);cursor:pointer;transition:border-color .2s ease-out,background-color .2s ease-out,transform .1s}
.v4nav:active{transform:scale(.97)}
.v4nav:disabled{opacity:.4;cursor:default}
.v4nav--next{background:var(--bg-deep);border-color:var(--bg-deep);color:#fff}
@media (hover:hover) and (pointer:fine){.v4nav:hover:not(:disabled){border-color:var(--blue)}.v4nav--next:hover{background:var(--blue);border-color:var(--blue)}}
@media(max-width:900px){.v4how__body{grid-template-columns:minmax(0,1fr)}.v4how__stage{border-radius:20px}}
@media(max-width:560px){.v4how__tabs button span{display:none}.v4how__tabs button{padding:.8em 1em}.v4chip--hide-sm{display:none}.v4reads{right:3%;bottom:5%;padding:.6em .7em}}
@media(prefers-reduced-motion:reduce){.v4scene,.v4chip,.v4reads,.v4cap,.v4count .v4bar,.v4count .v4exp{transition:none!important}.is-on .v4frag{animation:none}}
"""

STEPS_JS = r"""
/* «Как работает НИПТ» по шагам: вкладки, «Назад / Дальше», стрелки, свайп */
(function () {
  var root = document.querySelector('.v4how'); if (!root) return;
  var tabs = [].slice.call(root.querySelectorAll('[role="tab"]'));
  var scenes = [].slice.call(root.querySelectorAll('.v4scene'));
  var caps = [].slice.call(root.querySelectorAll('.v4cap'));
  var prog = [].slice.call(root.querySelectorAll('.v4how__prog i'));
  var prev = root.querySelector('[data-a="prev"]'), next = root.querySelector('[data-a="next"]');
  var panel = root.querySelector('[role="tabpanel"]'), n = tabs.length, cur = 0;
  function go(i, focus) {
    cur = (i + n) % n;
    tabs.forEach(function (t, k) { var on = k === cur; t.setAttribute('aria-selected', String(on)); t.tabIndex = on ? 0 : -1; });
    scenes.forEach(function (s, k) { s.classList.toggle('is-on', k === cur); s.setAttribute('aria-hidden', String(k !== cur)); });
    caps.forEach(function (c, k) { c.classList.toggle('is-on', k === cur); });
    prog.forEach(function (p, k) { p.classList.toggle('on', k <= cur); });
    panel.setAttribute('aria-labelledby', tabs[cur].id);
    prev.disabled = cur === 0;
    next.textContent = cur === n - 1 ? 'Сначала ↺' : 'Дальше →';
    if (focus) tabs[cur].focus();
    tabs[cur].scrollIntoView({ block: 'nearest', inline: 'nearest' });
  }
  tabs.forEach(function (t, k) { t.addEventListener('click', function () { go(k); }); });
  prev.addEventListener('click', function () { go(cur - 1); });
  next.addEventListener('click', function () { go(cur === n - 1 ? 0 : cur + 1); });
  root.querySelector('[role="tablist"]').addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight') { e.preventDefault(); go(cur + 1, true); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); go(cur - 1, true); }
  });
  var stage = root.querySelector('.v4how__stage'), x0 = null;
  stage.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  stage.addEventListener('touchend', function (e) {
    if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 40) go(dx < 0 ? Math.min(cur + 1, n - 1) : Math.max(cur - 1, 0));
  });
  go(0);
})();
"""


# ---------------------------------------------------------------- квиз «Не знаете, какой НИПТ выбрать?»
# Панели и факты — из старого квиза прототипа (цены, состав, id корзины). Подбор ведёт к широким панелям,
# но только через реальные свойства панелей: микроделеции, все хромосомы, носительство, бесплатное подтверждение.
Q_LADDER = [  # ключ, название, синдромов, цена, ширина полосы (пропорционально числу синдромов, минимум 4 %)
    ("t21", "Т21", "1", "16&nbsp;000&nbsp;₽", 4),
    ("basic", "Базовая", "3", "19&nbsp;000&nbsp;₽", 8),
    ("standard", "Стандартная", "7", "23&nbsp;000&nbsp;₽", 18),
    ("extended", "Расширенная", "13", "34&nbsp;000&nbsp;₽", 34),
    ("expert", "Экспертная", "38+", "40&nbsp;000&nbsp;₽", 100),
]
QUESTIONS = [  # ключ, вопрос, подсказка, варианты, можно несколько
    ("term", "Какой у&nbsp;вас срок беременности?", "НИПТ сдают с&nbsp;10 полных недель.",
     [("lt10", "Меньше 10 недель"), ("ok", "10–13 недель"), ("late", "14 недель и&nbsp;больше")], False),
    ("fetus", "Сколько малышей вы&nbsp;ждёте?", "От&nbsp;этого зависит, какие панели можно сделать.",
     [("one", "Одного"), ("twin", "Двойню"), ("multi", "Тройню или больше"), ("unknown", "Пока не&nbsp;знаю")], False),
    ("age", "Сколько вам лет?", "С&nbsp;возрастом вероятность хромосомных аномалий меняется.",
     [("lt30", "До&nbsp;30"), ("30", "30–34"), ("35", "35 и&nbsp;старше")], False),
    ("hist", "Что-то из&nbsp;этого про вас?", "Можно выбрать несколько.",
     [("ivf", "Беременность после ЭКО"), ("risk", "Скрининг I&nbsp;триместра или УЗИ показали повышенный риск"),
      ("loss", "Были замершие беременности или выкидыши"), ("family", "В&nbsp;семье есть наследственные заболевания"),
      ("none", "Ничего из&nbsp;этого")], True),
    ("carrier", "Вы&nbsp;проверялись на&nbsp;носительство наследственных заболеваний?",
     "Носители обычно здоровы и&nbsp;не&nbsp;знают о&nbsp;носительстве.",
     [("yes", "Да, проверялась"), ("no", "Нет"), ("unknown", "Не&nbsp;знала, что это можно проверить")], False),
    ("goal", "Что для вас важнее?", "Последний вопрос.",
     [("max", "Узнать как можно больше за&nbsp;один анализ"), ("main", "Проверить основные хромосомные аномалии"),
      ("budget", "Минимальная цена")], False),
]


def _q_step(i: int, key: str, title: str, hint: str, opts: list[tuple[str, str]], multi: bool) -> str:
    pressed = ' aria-pressed="false"' if multi else ""
    buttons = "".join(f'<button type="button" class="v4q__opt" data-v="{v}"{pressed}><span class="mono">{n + 1:02d}</span>{t}</button>'
                      for n, (v, t) in enumerate(opts))
    back = '<button type="button" class="v4q__back">← Назад</button>' if i else "<span></span>"
    nxt = '<button type="button" class="btn-lnipt btn-lnipt--primary btn-lnipt--sm v4q__next" disabled><span>Дальше →</span></button>' if multi else ""
    return (f'<div class="v4q__step" data-k="{key}"' + (" data-multi" if multi else "") + (" hidden" if i else "") + ">"
            f'<h3 tabindex="-1">{title}</h3><p class="v4q__hint">{hint}</p>'
            f'<div class="v4q__opts">{buttons}</div><div class="v4q__nav">{back}{nxt}</div></div>')


QUIZ = (
    '<section id="quiz" class="v4qs" aria-labelledby="v4q-t">\n  <div class="wrap">\n'
    '    <div class="section-head"><span class="section-eyebrow">Подбор за&nbsp;минуту</span>'
    '<h2 id="v4q-t">Не&nbsp;знаете, какой НИПТ <em>выбрать</em>?</h2>'
    '<p class="lead">Шесть коротких вопросов&nbsp;— и&nbsp;покажем панель под вашу ситуацию. Контакты вводить не&nbsp;нужно.</p></div>\n'
    '    <div class="v4q" id="v4q">\n      <div class="v4q__main">'
    '<div class="v4q__top"><span class="v4q__n mono" id="v4q-n">01 / 06</span><span class="v4q__bar"><i id="v4q-bar"></i></span></div>'
    '<p class="v4q__now" id="v4q-now" aria-live="polite"></p>'
    + "".join(_q_step(i, *q) for i, q in enumerate(QUESTIONS))
    + '<div class="v4q__res" id="v4q-res" hidden></div></div>\n'
    '      <aside class="v4q__side" aria-label="Панели НИПТ от узкой к широкой">'
    '<p class="v4q__lbl mono">Панель под ваши ответы</p><ol class="v4q__lad">'
    + "".join(f'<li data-p="{k}"><span class="v4q__pn">{name}<small>{price}</small></span>'
              f'<span class="v4q__pb"><i style="width:{w}%"></i></span><span class="v4q__pc">{cnt}</span></li>'
              for k, name, cnt, price, w in Q_LADDER)
    + '</ol><p class="v4q__lbl mono">Учитываем</p>'
    '<ul class="v4q__chips" id="v4q-chips"><li class="v4q__empty">ответьте на&nbsp;первые вопросы</li></ul></aside>\n'
    "    </div>\n  </div>\n</section>"
)

QUIZ_CSS = """
/* ===== v4: квиз — шесть вопросов, лесенка панелей ===== */
.v4q{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,340px);margin-top:2.2em;background:#fff;border:1px solid var(--line-soft);border-radius:var(--r-xl);box-shadow:0 24px 60px rgba(10,37,64,.08);overflow:hidden}
.v4q__main{padding:clamp(1.4em,3.5vw,2.8em);min-width:0;min-height:420px}
.v4q__top{display:flex;align-items:center;gap:1em;margin-bottom:1.6em}
.v4q__n{font-size:.8em;font-weight:700;color:var(--blue);font-variant-numeric:tabular-nums;white-space:nowrap}
.v4q__bar{flex:1;height:6px;border-radius:100px;background:var(--line-soft);overflow:hidden}
.v4q__bar i{display:block;height:100%;background:linear-gradient(90deg,var(--blue),var(--cyan));transform-origin:left;transform:scaleX(var(--p,.1667));transition:transform .2s ease-out}
.v4q__now{display:none;margin:-.8em 0 1.3em;font-size:.86em;color:var(--muted)}
.v4q__now b{color:var(--blue)}
.v4q .v4q__step h3,.v4q .v4q__res h3{font-size:clamp(22px,2.4vw,30px) !important;line-height:1.2;margin:0;letter-spacing:-.02em;text-wrap:balance;outline:none}
.v4q__res h3 em{color:var(--blue);font-style:normal}
.v4q__hint{margin:.5em 0 0;color:var(--muted);font-size:.92em}
.v4q__opts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:1.4em}
.v4q__opt{font:inherit;text-align:left;display:flex;align-items:center;gap:.9em;padding:1em 1.1em;border:1.5px solid var(--line);border-radius:var(--r-md);background:#fff;font-weight:700;color:var(--ink);line-height:1.3;cursor:pointer;
  transition:border-color .15s ease-out,background-color .15s ease-out,transform .15s ease-out}
.v4q__opt .mono{font-size:.74em;color:var(--muted);flex:none}
.v4q__opt:active{transform:scale(.98)}
.v4q__opt:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
.v4q__opt[aria-pressed="true"]{border-color:var(--blue);background:var(--accent-soft)}
.v4q__opt[aria-pressed="true"] .mono{color:var(--blue)}
@media(hover:hover) and (pointer:fine){.v4q__opt:hover{border-color:var(--blue);background:#F5F9FF}}
.v4q__nav{display:flex;justify-content:space-between;align-items:center;gap:1em;margin-top:1.4em;min-height:2.6em}
.v4q__back{font:inherit;background:none;border:none;padding:0;cursor:pointer;color:var(--muted);font-weight:600;font-size:.9em}
.v4q__back:hover{color:var(--blue)}
.v4q__next[disabled]{opacity:.4;pointer-events:none}
.v4q__step:not([hidden]),.v4q__res:not([hidden]){animation:v4qIn .22s ease-out}
@keyframes v4qIn{from{opacity:0;transform:translateY(8px)}}
@keyframes v4qPop{from{opacity:0;transform:scale(.9)}}
.v4q__side{background:linear-gradient(180deg,#F5F9FF,#EAF2FF);border-left:1px solid var(--line-soft);padding:clamp(1.4em,3vw,2.2em);min-width:0}
.v4q__lbl{font-size:.7em;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:0 0 .9em}
.v4q__lad{list-style:none;margin:0 0 1.8em;padding:0;display:grid;gap:4px}
.v4q__lad li{display:grid;grid-template-columns:6.6em minmax(0,1fr) 2.4em;align-items:center;gap:.7em;padding:.55em .7em;border-radius:12px;transition:background-color .2s ease-out,box-shadow .2s ease-out}
.v4q__pn{font-weight:700;font-size:.86em;color:var(--ink-2);line-height:1.2}
.v4q__pn small{display:block;margin-top:.15em;font:600 .8em var(--mono);color:var(--muted);font-variant-numeric:tabular-nums}
.v4q__pb{height:8px;border-radius:100px;background:rgba(10,37,64,.07);overflow:hidden}
.v4q__pb i{display:block;height:100%;border-radius:inherit;background:#B9C8DE}
.v4q__pc{font:700 .8em var(--mono);color:var(--muted);text-align:right}
.v4q__lad li.on{background:#fff;box-shadow:0 10px 26px rgba(0,87,255,.14)}
.v4q__lad li.on .v4q__pn{color:var(--ink)}
.v4q__lad li.on .v4q__pb i{background:linear-gradient(90deg,var(--blue),var(--cyan))}
.v4q__lad li.on .v4q__pc{color:var(--blue)}
.v4q__chips{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px}
.v4q__chips li{padding:.45em .8em;border-radius:100px;background:#fff;border:1px solid var(--line);font-size:.78em;font-weight:700;color:var(--ink);line-height:1.25;animation:v4qPop .2s ease-out}
.v4q__chips .v4q__empty{background:none;border:none;padding:0;color:var(--muted);font-weight:500;animation:none}
.v4q__price{display:flex;flex-wrap:wrap;align-items:baseline;gap:.3em 1em;margin-top:.9em}
.v4q__price b{font-family:var(--mono);font-size:clamp(24px,2.8vw,34px);font-weight:700;color:var(--blue);font-variant-numeric:tabular-nums;white-space:nowrap}
.v4q__price span{color:var(--muted);font-size:.9em}
.v4q__what{margin:1em 0 1.5em;color:var(--ink-2);line-height:1.55;max-width:60ch}
.v4q__why{list-style:none;margin:0;padding:0;display:grid;gap:.75em}
.v4q__why li{display:flex;gap:.7em;align-items:flex-start;line-height:1.5;color:var(--ink);text-wrap:pretty}
.v4q__why svg{width:20px;height:20px;flex:none;margin-top:.12em;color:var(--blue)}
.v4q__duo{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:1.4em}
.v4q__duo div{padding:1em 1.1em;border:1.5px solid var(--line);border-radius:var(--r-md)}
.v4q__duo b{display:block;color:var(--ink)}
.v4q__duo span{display:block;margin:.2em 0 .8em;font:700 .95em var(--mono);color:var(--blue)}
.v4q__cta{display:flex;flex-wrap:wrap;gap:.7em;margin-top:1.6em}
.v4q__alt{margin:1.3em 0 0;padding-top:1.1em;border-top:1px solid var(--line-soft);color:var(--ink-2);font-size:.92em;line-height:1.5}
.v4q__alt a{color:var(--blue);font-weight:700;white-space:nowrap}
.v4q__note{margin:1em 0 0;padding:.8em 1em;border-radius:var(--r-sm);background:var(--warn-soft);color:var(--ink-2);font-size:.88em;line-height:1.5}
.v4q__foot{display:flex;flex-wrap:wrap;gap:.6em 1.6em;align-items:baseline;margin-top:1.4em}
.v4q__foot p{margin:0;font-size:.78em;line-height:1.5;color:var(--muted);flex:1 1 20em}
@media(max-width:900px){.v4q{grid-template-columns:minmax(0,1fr)}.v4q__side{display:none}.v4q__now{display:block}.v4q__main{min-height:0}}
@media(max-width:560px){.v4q__opts,.v4q__duo{grid-template-columns:minmax(0,1fr)}}
@media(prefers-reduced-motion:reduce){.v4q *{animation:none !important;transition:none !important}}
"""

QUIZ_JS = r"""
/* ============================================================
   1. КВИЗ — подбор панели (v4): шесть вопросов, лесенка панелей сбоку
   ============================================================ */
(function () {
  var q = document.getElementById('v4q');
  if (!q) return;
  var BASKET = 'https://price.genomed.ru/basket/add?id=';
  var P = {
    t21: { name: 'НИПТ Т21', price: '16 000 ₽', term: '8 календарных дней', id: 802,
      what: 'Синдром Дауна (трисомия 21) и пол малыша. Можно при двойне.' },
    basic: { name: 'НИПТ Базовая', price: '19 000 ₽', term: '8 календарных дней', id: 1934,
      what: 'Три частые трисомии — синдромы Дауна, Эдвардса и Патау — и пол малыша. Можно при двойне.' },
    standard: { name: 'НИПТ Стандартная', price: '23 000 ₽', term: '8 календарных дней', id: 1115,
      what: 'Трисомии 21, 18 и 13, аномалии половых хромосом и пол малыша.' },
    extended: { name: 'НИПТ Расширенная', price: '34 000 ₽', term: '8 рабочих дней', id: 1400,
      what: 'Всё, что в стандартной, плюс шесть микроделеционных синдромов и скрининг носительства рецессивных заболеваний у мамы. При высоком риске подтверждающая диагностика — бесплатно.' },
    expert: { name: 'НИПТ Экспертная', price: '40 000 ₽', term: '8 рабочих дней', id: 2468,
      what: 'Анеуплоидии всех хромосом плода, 31 микроделеционный синдром и скрининг носительства рецессивных заболеваний у мамы. При высоком риске подтверждающая диагностика — бесплатно.' }
  };
  var ORDER = ['t21', 'basic', 'standard', 'extended', 'expert'];
  var CHIP = { age35: '35+ — проверить все хромосомы', young: 'микроделеции — в любом возрасте', ivf: 'беременность после ЭКО',
    risk: 'повышенный риск по скринингу', loss: 'потери беременности', family: 'наследственные заболевания в семье',
    carrier: 'носительство не проверяли', max: 'хочу максимум' };
  var CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="m8 12 3 3 5-6"/></svg>';
  var RM = window.matchMedia('(prefers-reduced-motion: reduce)');
  var steps = [].slice.call(q.querySelectorAll('.v4q__step'));
  var res = document.getElementById('v4q-res');
  var lad = [].slice.call(q.querySelectorAll('.v4q__lad li'));
  var chips = document.getElementById('v4q-chips');
  var now = document.getElementById('v4q-now');
  var a = {}, cur = 0;

  function goal(name, params) {
    if (typeof window.ym === 'function') window.ym(21728914, 'reachGoal', name, params);
  }
  function flags() {
    var f = [];
    if (a.age === '35') f.push('age35');
    (a.hist || []).forEach(function (v) { if (v !== 'none') f.push(v); });
    if (a.carrier === 'no' || a.carrier === 'unknown') f.push('carrier');
    return f;
  }
  function has(v) { return flags().indexOf(v) > -1; }
  // подбор: чем больше поводов, тем шире панель; при повышенном риске — не уже расширенной
  function pick() {
    if (!a.age) return null;
    var n = flags().length, k;
    if (a.goal === 'max') k = 'expert';
    else if (a.goal === 'budget') k = n >= 2 ? 'extended' : 'basic';
    else k = n >= 2 ? 'expert' : n === 1 ? 'extended' : 'standard';
    if (has('risk') && ORDER.indexOf(k) < 3) k = 'extended';
    return k;
  }
  function side(keys) {
    lad.forEach(function (li) { li.classList.toggle('on', keys.indexOf(li.dataset.p) > -1); });
    var f = flags();
    if (a.age && a.age !== '35') f.unshift('young');
    if (a.goal === 'max') f.push('max');
    chips.innerHTML = f.length ? f.map(function (c) { return '<li>' + CHIP[c] + '</li>'; }).join('')
      : '<li class="v4q__empty">ответьте на первые вопросы</li>';
    var k = keys.length === 1 ? keys[0] : null;
    now.innerHTML = k ? nb('Сейчас подходит: <b>' + P[k].name + '</b> · ' + P[k].price) : '';
  }
  function prog(i, done) {
    document.getElementById('v4q-n').textContent = done ? 'Готово' : ('0' + (i + 1)).slice(-2) + ' / 0' + steps.length;
    document.getElementById('v4q-bar').style.setProperty('--p', done ? 1 : (i + 1) / steps.length);
  }
  function focus(el) {
    var h = el.querySelector('h3');
    var top = q.getBoundingClientRect().top;
    if (top < 0) window.scrollTo({ top: window.scrollY + top - 90, behavior: RM.matches ? 'auto' : 'smooth' });
    if (h) h.focus({ preventScroll: true });
  }
  function show(i) {
    cur = i;
    steps.forEach(function (s, n) { s.hidden = n !== i; });
    res.hidden = true;
    prog(i, false);
    var k = pick();
    side(k ? [k] : []);
    focus(steps[i]);
  }
  function why(k) {
    var r = [], X = k === 'expert';
    if (k === 'standard') return ['Трисомии 21, 18, 13 и аномалии половых хромосом — самый широкий вариант с результатом за 8 календарных дней.'];
    if (k === 'basic') return ['Все три частые трисомии — синдромы Дауна, Эдвардса и Патау. Т21 дешевле, но проверяет только синдром Дауна.'];
    if (has('age35') && X) r.push('После 35 лет вероятность хромосомных аномалий выше — экспертная панель проверяет все хромосомы плода, а не только 21, 18 и 13.');
    if (a.age && a.age !== '35') r.push('Микроделеционные синдромы не зависят от возраста мамы, а ищут их только расширенная и экспертная панели.');
    if (has('ivf')) r.push(X ? 'Беременность после ЭКО: за один анализ крови панель проверит все хромосомы плода и 31 микроделеционный синдром.'
      : 'Беременность после ЭКО: к основным трисомиям панель добавит шесть микроделеционных синдромов.');
    if (has('risk')) r.push('Скрининг показал повышенный риск. Если НИПТ тоже покажет высокий риск, подтверждающую диагностику сделают бесплатно.');
    if (has('family')) r.push('В семье есть наследственные заболевания — в панель входит скрининг носительства рецессивных заболеваний у мамы.');
    else if (has('carrier')) r.push('Носители рецессивных заболеваний обычно здоровы и не знают об этом — панель заодно проверит носительство у мамы.');
    if (has('loss')) r.push('Были потери беременности — врач-генетик бесплатно разберёт результат с учётом вашей истории.');
    if (a.goal === 'max' && X) r.push('Экспертная — самая широкая панель Геномед: 38 и более синдромов, в расширенной — 13.');
    return r.slice(0, 4);
  }
  var ALT = {
    expert: ['extended', 'Бюджет ограничен? <b>НИПТ Расширенная</b> — 34 000 ₽: шесть микроделеционных синдромов вместо 31, носительство у мамы тоже проверяется.'],
    extended: ['expert', 'Хотите проверить все хромосомы и 31 микроделеционный синдром? <b>НИПТ Экспертная</b> — 40 000 ₽, на 6 000 ₽ больше.'],
    standard: ['expert', 'Стандартная не ищет микроделеции. <b>НИПТ Экспертная</b> — все хромосомы, 31 микроделеционный синдром и носительство у мамы, 40 000 ₽.'],
    basic: ['standard', '<b>НИПТ Стандартная</b> за 23 000 ₽ добавит аномалии половых хромосом.']
  };
  function nb(t) { return t.replace(/(^|[\s(])([а-яёА-ЯЁ]{1,2}) /g, '$1$2\u00a0').replace(/(^|[\s(])([а-яёА-ЯЁ]{1,2}) /g, '$1$2\u00a0').replace(/ —/g, '\u00a0—').replace(/(\d) (\d{3})/g, '$1\u00a0$2').replace(/(\d) (₽|%)/g, '$1\u00a0$2'); }
  function foot() {
    return '<div class="v4q__foot"><button type="button" class="v4q__back" data-restart>← Пройти заново</button>' +
      '<p>Рекомендация справочная и не заменяет консультацию врача-генетика. Окончательный объём исследования определяет врач.</p></div>';
  }
  function finish(html, keys, tag) {
    steps.forEach(function (s) { s.hidden = true; });
    res.innerHTML = nb(html) + foot();
    res.hidden = false;
    prog(0, true);
    side(keys);
    now.innerHTML = '';
    goal('nipt_quiz_result', { panel: tag });
    focus(res);
  }
  function info(title, text) {
    finish('<p class="v4q__lbl mono">Нужна консультация</p><h3 tabindex="-1">' + title + '</h3><p class="v4q__what">' + text + '</p>' +
      '<div class="v4q__cta"><a class="btn-lnipt btn-lnipt--primary" href="#modal-callback"><span>Записаться на консультацию</span></a></div>', [], 'консультация');
  }
  function result() {
    if (a.term === 'lt10') return info('Пока рано сдавать',
      'НИПТ выполняется с 10 полных недель. До этого срока доля ДНК плода в крови мамы обычно меньше 4 %, и надёжный результат получить нельзя. Генетик подскажет, когда прийти, и заранее подберёт панель.');
    if (a.fetus === 'multi') return info('При тройне НИПТ не проводится',
      'Разделить вклад каждого плода в общую внеклеточную ДНК невозможно. Обсудите с врачом-генетиком, какие методы пренатального обследования подойдут вам.');
    if (a.fetus === 'unknown') return info('Подберём панель после УЗИ',
      'От числа плодов зависит, какие панели доступны: при двойне — Т21 и базовая, при тройне исследование не проводится. Генетик подберёт панель по результату ближайшего УЗИ.');
    if (a.fetus === 'twin') return finish('<p class="v4q__lbl mono">Ваш результат</p><h3 tabindex="-1">При двойне подходят <em>две панели</em></h3>' +
      '<p class="v4q__what">Обе выполняются при двуплодной беременности и после редукции одного эмбриона. Панели с аномалиями половых хромосом при двойне не применяются — разделить вклад плодов нельзя.</p>' +
      '<div class="v4q__duo">' + ['t21', 'basic'].map(function (k) {
        return '<div><b>' + P[k].name + '</b><span>' + P[k].price + '</span><a class="btn-lnipt btn-lnipt--secondary btn-lnipt--sm" href="' + BASKET + P[k].id + '&oneClick=1">Заказать</a></div>';
      }).join('') + '</div><div class="v4q__cta"><a class="btn-lnipt btn-lnipt--secondary" href="#modal-callback">Обсудить с генетиком</a></div>', ['t21', 'basic'], 'двойня — Т21 и базовая');
    var k = pick(), p = P[k], alt = ALT[k];
    finish('<p class="v4q__lbl mono">Ваш результат</p><h3 tabindex="-1">Вам подойдёт <em>' + p.name + '</em></h3>' +
      '<div class="v4q__price"><b>' + p.price + '</b><span>результат за ' + p.term + ' · консультация генетика бесплатно</span></div>' +
      '<p class="v4q__what">' + p.what + '</p>' +
      '<p class="v4q__lbl mono">Почему она</p><ul class="v4q__why">' + why(k).map(function (t) { return '<li>' + CHECK + '<span>' + t + '</span></li>'; }).join('') + '</ul>' +
      (has('risk') ? '<p class="v4q__note">Если на УЗИ нашли изменения, генетик может сразу предложить инвазивную диагностику — обсудите это на консультации.</p>' : '') +
      '<div class="v4q__cta"><a class="btn-lnipt btn-lnipt--primary" href="' + BASKET + p.id + '&oneClick=1" data-panel="' + p.name + '"><span>Заказать · ' + p.price + '</span></a>' +
      '<a class="btn-lnipt btn-lnipt--secondary" href="#modal-callback">Обсудить с генетиком</a></div>' +
      '<p class="v4q__alt">' + alt[1] + ' <a href="' + BASKET + P[alt[0]].id + '&oneClick=1">Заказать →</a></p>', [k], p.name);
  }
  function terminal() { return a.term === 'lt10' || (a.fetus && a.fetus !== 'one'); }
  function next() { if (terminal() || cur === steps.length - 1) result(); else show(cur + 1); }

  q.addEventListener('click', function (e) {
    if (e.target.closest('[data-restart]')) {
      a = {};
      q.querySelectorAll('.v4q__opt[aria-pressed]').forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
      q.querySelectorAll('.v4q__next').forEach(function (b) { b.disabled = true; });
      return show(0);
    }
    if (e.target.closest('.v4q__back')) return show(Math.max(cur - 1, 0));
    if (e.target.closest('.v4q__next')) return next();
    var opt = e.target.closest('.v4q__opt');
    if (!opt) return;
    var st = opt.closest('.v4q__step'), key = st.dataset.k, v = opt.dataset.v;
    if (!Object.keys(a).length) goal('nipt_quiz_start');
    if (st.hasAttribute('data-multi')) {
      var on = opt.getAttribute('aria-pressed') !== 'true';
      st.querySelectorAll('.v4q__opt').forEach(function (b) {
        if (b === opt) b.setAttribute('aria-pressed', String(on));
        else if (on && (v === 'none' || b.dataset.v === 'none')) b.setAttribute('aria-pressed', 'false');
      });
      a[key] = [].slice.call(st.querySelectorAll('.v4q__opt[aria-pressed="true"]')).map(function (b) { return b.dataset.v; });
      st.querySelector('.v4q__next').disabled = !a[key].length;
      var k = pick();
      side(k ? [k] : []);
      return;
    }
    a[key] = v;
    next();
  });
  prog(0, false);
})();
"""

QUIZ_OLD_START = "/* ============================================================\n   1. КВИЗ"
QUIZ_OLD_END = "/* ============================================================\n   2. ЯКОРНАЯ"


def script(js: str) -> str:
    """Старый квиз прототипа (три вопроса) → новый."""
    i, j = js.index(QUIZ_OLD_START), js.index(QUIZ_OLD_END)
    return js[:i] + QUIZ_JS.lstrip() + LIM_JS + "\n\n" + js[j:]


# ---------------------------------------------------------------- вопросы: слева заголовок и «спросите генетика», справа одна колонка карточек
def faq(faq_html: str) -> str:
    items = re.findall(r'(?s)<details class="fq" style="order:(\d+)"( open)?><summary><span class="fq__ic">.*?</span>'
                       r'<span class="fq__q"><span class="fq__n mono">(\d+)</span>(.*?)</span></summary><div class="fq__a">(.*?)</div></details>',
                       faq_html)
    if len(items) != 9:
        raise SystemExit(f"v4: ожидалось 9 вопросов, найдено {len(items)}")
    items.sort(key=lambda t: int(t[0]))
    cards = "\n".join(f'<details class="v4fq"{op}><summary><span class="v4fq__n mono">{n}</span><span class="v4fq__q">{q}</span>'
                      f'<span class="v4chev" aria-hidden="true"></span></summary><div class="v4fq__a">{a}</div></details>'
                      for _, op, n, q, a in items)
    return f"""<section id="faq" class="v3band">
  <div class="wrap v4faq">
    <div class="v4faq__side">
      <span class="section-eyebrow">Вопросы</span>
      <h2>Что чаще всего <em>спрашивают</em></h2>
      <div class="v4faq__ask"><img src="img/ic-doctor.webp" alt="" width="216" height="280" loading="lazy">
        <div><b>Не&nbsp;нашли ответа?</b><p>Спросите врача-генетика&nbsp;— консультация перед исследованием бесплатна.</p>
        <a class="btn-lnipt btn-lnipt--primary btn-lnipt--sm" href="#modal-callback"><span>Задать вопрос</span></a></div></div>
    </div>
    <div class="v4faq__list">
{cards}
    </div>
  </div>
</section>"""


# ---------------------------------------------------------------- ограничения: светлая полоса со стрелкой вместо тёмной плашки на экран
def limits(lim_html: str) -> str:
    lead = re.search(r'<p style="max-width:66ch;margin:1em 0 0">(.*?)</p>', lim_html, re.S).group(1)
    tail_m = re.search(r'\s*<p style="margin-top:1\.8em;font-size:\.92em">(.*?)</p>', lim_html, re.S)
    body = lim_html[lim_html.index('<h3 class="limgrp">'):tail_m.start()]
    groups = re.findall(r'(?s)<div class="limlist">(.*?)\n      </div>', body)
    if len(groups) != 2:
        raise SystemExit(f"v4: ожидалось 2 группы ограничений, найдено {len(groups)}")
    n_no, n_bad = (g.count('class="limrow"') for g in groups)
    return f"""<section id="limits" class="v4lim-sec">
  <div class="wrap">
    <details class="v4lim">
      <summary>
        <span class="v4lim__ic">{ic("info")}</span>
        <span class="v4lim__t"><span class="section-eyebrow">Ограничения</span><b>Когда НИПТ <em>не&nbsp;подходит</em></b>
          <small>{n_no} ситуации, когда исследование не&nbsp;проводится, и&nbsp;{n_bad}, когда результат может быть неточным</small></span>
        <span class="v4lim__btn"><span class="v4lim__more"><span>Подробнее</span><span>Свернуть</span></span><span class="v4chev" aria-hidden="true"></span></span>
      </summary>
      <div class="v4lim__body">
      <p class="v4lim__lead">{lead}</p>
      {body.strip()}
      <p class="v4lim__tail">{tail_m.group(1)}</p>
      </div>
    </details>
  </div>
</section>"""


LIM_JS = r"""
/* ограничения: ссылка «Ограничения» в меню раскрывает блок */
(function () {
  var d = document.querySelector('.v4lim');
  if (!d) return;
  document.querySelectorAll('a[href="#limits"]').forEach(function (a) { a.addEventListener('click', function () { d.open = true; }); });
  if (location.hash === '#limits') d.open = true;
})();
"""

FAQ_LIM_CSS = """
/* ===== v4: вопросы — заголовок слева, карточки справа ===== */
.v4faq{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.4fr);gap:clamp(2em,5vw,4.5em);align-items:start}
.v4faq__side{position:sticky;top:calc(96px + env(safe-area-inset-top,0px))}
.v4faq__side h2{margin:.35em 0 0}
.v4faq__ask{display:flex;gap:1.1em;align-items:center;margin-top:1.8em;padding:1.2em 1.3em;border-radius:var(--r-lg);background:linear-gradient(135deg,#EEF5FF,#E2F4FF);border:1px solid var(--line-soft)}
.v4faq__ask img{width:auto;height:88px;flex:none;filter:drop-shadow(0 10px 16px rgba(10,37,64,.15))}
.v4faq__ask b{display:block;font-family:var(--disp);font-weight:800;font-size:1.08em;color:var(--ink)}
.v4faq__ask p{margin:.3em 0 .9em;color:var(--ink-2);font-size:.92em;line-height:1.5}
.v4faq__list{display:grid;gap:10px;min-width:0}
.v4fq{background:var(--bg);border:1px solid var(--line-soft);border-radius:var(--r-md);transition:background-color .2s ease-out,border-color .2s ease-out,box-shadow .2s ease-out}
.v4fq[open]{background:#fff;border-color:var(--cyan-soft);box-shadow:var(--shadow-md)}
.v4fq summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:2.2em minmax(0,1fr) 36px;align-items:center;gap:.8em;padding:1.05em 1.2em;font-weight:700;color:var(--ink);line-height:1.35}
.v4fq summary::-webkit-details-marker,.v4lim summary::-webkit-details-marker{display:none}
.v4fq summary:focus-visible,.v4lim summary:focus-visible{outline:2px solid var(--blue);outline-offset:2px;border-radius:var(--r-md)}
.v4fq__n{font-size:.78em;color:var(--blue)}
.v4fq__a{padding:0 calc(2.4em + 36px) 1.25em calc(1.2em + 2.2em + .8em)}
.v4fq__a p{margin:0;padding:0;color:var(--ink-2);line-height:1.6;text-wrap:pretty}
.v4chev{flex:none;width:36px;height:36px;border-radius:50%;background:#fff;border:1px solid var(--line);position:relative;transition:transform .2s ease-out,background-color .2s ease-out,border-color .2s ease-out}
.v4chev::after{content:"";position:absolute;left:50%;top:45%;width:8px;height:8px;border-right:2px solid var(--ink);border-bottom:2px solid var(--ink);transform:translate(-50%,-50%) rotate(45deg)}
details[open]>summary .v4chev{transform:rotate(180deg);background:var(--blue);border-color:var(--blue)}
details[open]>summary .v4chev::after{border-color:#fff}
@media(hover:hover) and (pointer:fine){.v4fq:not([open]) summary:hover .v4chev,.v4lim:not([open]) summary:hover .v4chev{border-color:var(--blue)}}
@media(max-width:900px){.v4faq{grid-template-columns:minmax(0,1fr)}.v4faq__side{position:static}}
@media(max-width:560px){.v4fq summary{grid-template-columns:minmax(0,1fr) 32px}.v4fq__n{display:none}.v4fq__a{padding:0 1.2em 1.2em}.v4chev{width:32px;height:32px}}

/* ===== v4: ограничения — раскрывающаяся полоса ===== */
#limits.v4lim-sec{padding-block:clamp(2em,4vw,3em) !important}
.v4lim{background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);box-shadow:var(--shadow-sm);transition:box-shadow .2s ease-out}
.v4lim[open]{box-shadow:var(--shadow-md)}
.v4lim summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:52px minmax(0,1fr) auto;gap:1.1em;align-items:center;padding:clamp(1.1em,2.5vw,1.6em) clamp(1.1em,3vw,2em)}
.v4lim__ic{width:52px;height:52px;border-radius:16px;background:var(--warn-soft);color:var(--warn);display:grid;place-items:center}
.v4lim__ic svg{width:24px;height:24px}
.v4lim__t{display:grid;gap:.3em;min-width:0}
.v4lim__t .section-eyebrow{margin:0}
.v4lim__t b{font-family:var(--disp);font-weight:800;font-size:clamp(22px,2.4vw,30px);letter-spacing:-.025em;line-height:1.15;color:var(--ink)}
.v4lim__t b em{color:var(--blue);font-style:normal}
.v4lim__t small{color:var(--muted);font-size:.9em;font-weight:500;line-height:1.45}
.v4lim__btn{display:flex;align-items:center;gap:.7em;font-weight:700;color:var(--blue);font-size:.92em}
.v4lim__more span+span,.v4lim[open] .v4lim__more span:first-child{display:none}
.v4lim[open] .v4lim__more span+span{display:inline}
.v4lim__body{padding:0 clamp(1.1em,3vw,2em) clamp(1.3em,3vw,2em);border-top:1px solid var(--line-soft)}
.v4lim__lead{margin:1.3em 0 0;max-width:70ch;color:var(--ink-2);line-height:1.6}
.v4lim .limgrp{color:var(--blue) !important}
.v4lim .limlist>.limrow{border-top-color:var(--line-soft)}
.v4lim .limrow__ic{background:var(--accent-soft);border-color:#C9DDFF;color:var(--blue)}
.v4lim .limrow h3{color:var(--ink)}
.v4lim .limrow p{color:var(--ink-2)}
.v4lim .limnote p{background:var(--bg);border-color:var(--line-soft);color:var(--ink-2)}
.v4lim .limnote b{color:var(--ink)}
.v4lim__tail{margin:1.5em 0 0;color:var(--muted);font-size:.92em}
@media(max-width:640px){.v4lim summary{grid-template-columns:minmax(0,1fr) auto}.v4lim__ic,.v4lim__more{display:none}}
@media(prefers-reduced-motion:reduce){.v4fq,.v4chev,.v4lim{transition:none}}
"""
