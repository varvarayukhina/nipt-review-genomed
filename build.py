"""Сборка двух версий лендинга НИПТ из прототипа ~/Downloads/НИПТ-прототип/index.html.

index.html       — исправленная версия: порядок блоков для пациента, вычитка, без анимаций
naglyadnaya.html — наглядная версия: то же + интерактивный путь ДНК и мобильная доводка
"""

import re
import shutil
from pathlib import Path

HERE = Path(__file__).parent
SRC = Path.home() / "Downloads" / "НИПТ-прототип"
src = (SRC / "index.html").read_text(encoding="utf-8")


def sub1(text: str, old: str, new: str) -> str:
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"ожидалось 1 вхождение, найдено {n}: {old[:90]!r}")
    return text.replace(old, new)


def cut(text: str, start: str, end: str, keep_end: bool = True) -> tuple[str, str]:
    """Вырезает кусок от start до end (end остаётся в тексте, если keep_end)."""
    i = text.index(start)
    j = text.index(end, i)
    piece = text[i:j] if keep_end else text[i : j + len(end)]
    rest = text[:i] + (text[j:] if keep_end else text[j + len(end) :])
    return piece, rest


# ---------------------------------------------------------------- голова и стили
head_links = src[src.index('<link rel="preconnect"') : src.index("<style>")]
css = src[src.index("<style>") + 7 : src.index("</style>")]
body = src[src.index("</style>") + 8 :]

# служебные стили демо-режима не нужны
_, css = cut(css, "/* ——— служебная полоса демо-режима ——— */", "/* ——— якорная навигация страницы ——— */")
_, css = cut(css, "/* ——— подсказка «куда ведёт кнопка» ——— */", "/* ——— форма заявки в блоке #cta ——— */")
css = sub1(css, "house-style Геномеда", "house-style Геномед")
css = sub1(css, ":root{--chrome-h:48px}\n@media(max-width:760px){:root{--chrome-h:88px}}", ":root{--chrome-h:0px}")

# ---------------------------------------------------------------- вычитка текстов
# Правило как в MEMA: врачебный тон, но доступно; без жаргона, разговорных оборотов,
# повторов «не диагноз» и внутренних пометок для заказчика. «Геномед» — без кавычек и склонения.
EDITS = [
    # hero: понятный заголовок + пара предложений о сути теста
    ('<p class="eyebrow">Пренатальный скрининг · с 10 полных недель</p>', '<p class="eyebrow">НИПТ · с 10 недель беременности</p>'),
    ("<h1>НИПТ с 10 недель — точный скрининг <em>хромосомных аномалий</em> по\u00a0крови мамы</h1>",
     "<h1>Риск синдрома Дауна у&nbsp;малыша&nbsp;— по&nbsp;анализу <em>крови мамы</em></h1>"),
    ("Не нужно самостоятельно разбираться в пяти панелях. Ответьте на три вопроса — подскажем подходящий вариант, а врач-генетик подтвердит выбор на бесплатной консультации.",
     "НИПТ — неинвазивный пренатальный тест. С 10-й недели беременности по крови мамы он оценивает вероятность синдрома Дауна и других хромосомных аномалий у плода — без прокола и риска для беременности. Заключение врача-генетика — через 8 дней."),
    # что это / для кого
    ("Скрининговый тест по венозной крови мамы: анализирует внеклеточную ДНК плода и оценивает вероятность самых частых хромосомных аномалий — например, синдрома Дауна.",
     "Скрининговое исследование по венозной крови матери. Оно анализирует ДНК плода, которая попадает в кровь из плаценты, и оценивает вероятность самых частых хромосомных аномалий — например, синдрома Дауна."),
    ("Рекомендован всем беременным (ACOG, SMFM, ISPD, ACMG). Особенно — после 35 лет, после ЭКО, при повышенном риске по УЗИ или скринингу, если раньше была беременность с хромосомной аномалией.",
     "Международные профессиональные сообщества рекомендуют исследование всем беременным. Особенно оно показано после 35 лет, после ЭКО, при повышенном риске по биохимическому скринингу и если ранее была беременность с хромосомной аномалией."),
    # фотополоса
    ("<p>Восемь дней ожидания — самая длинная неделя за всю беременность. Заключение разбирает генетик, строку за строкой.</p>\n    <span>Фото — из медиатеки Геномеда</span>",
     "<p>Результат — через 8 дней. Заключение врач-генетик разбирает вместе с вами.</p>"),
    # что вы получаете
    ("Одна пробирка венозной крови вместо процедуры, которую многие боятся, — и заключение, которое разбирают вместе с вами.",
     "Для исследования достаточно взять кровь из вены — без инвазивной процедуры. Заключение врач-генетик разбирает вместе с вами."),
    ("<p>Ни амниоцентеза, ни биопсии хориона</p>", "<p>Без амниоцентеза и биопсии ворсин хориона</p>"),
    # панели
    ("Забор крови во всех случаях одинаковый — 20 мл из вены. Различается объём анализа и, соответственно, срок и стоимость.",
     "Кровь для всех панелей берут одинаково — 20 мл из вены. Панели различаются объёмом анализа, сроком и стоимостью."),
    ("<p class=\"desc\">Плюс микроделеции и носительство у мамы</p>", "<p class=\"desc\">Микроделеции и носительство у будущей мамы</p>"),
    ('alt="Врач-генетик Геномеда"', 'alt="Врач-генетик лаборатории Геномед"'),
    # сравнение
    ("Поимённо — и количество синдромов, и состав. Первая колонка закреплена: на узких экранах таблица тянется вбок, а названия строк остаются на месте.",
     "Состав каждой панели по синдромам и итоговое число синдромов."),
    ("В разделе НИПТ поимённо названы 13 синдромов из 31, остальные идут формулировкой «и другие клинически значимые». Полный перечень стоит запросить в лаборатории — на странице он смотрелся бы весомее списка с «и другими».",
     "Ниже — 13 синдромов из 31. Полный перечень можно уточнить у врача-генетика."),
    ("Скрининг носительства патогенных вариантов у мамы. Значим при совпадении мутаций у обоих родителей — тогда риск для ребёнка достигает 25 %. Входит в расширенную и экспертную панели.",
     "Скрининг носительства патогенных вариантов у будущей мамы. Важен, если носителями вариантов в одном и том же гене окажутся оба родителя: тогда вероятность заболевания у ребёнка составляет 25 %. Входит в расширенную и экспертную панели."),
    # квиз
    ("Это займёт меньше минуты, никаких контактов вводить не нужно.", "Это займёт меньше минуты, контакты вводить не нужно."),
    ("<small>Нужно уточнить картину без прокола</small>", "<small>Нужно уточнить риск без инвазивной процедуры</small>"),
    ("Скрининг или УЗИ показали повышенный риск<small>", "Биохимический скрининг показал повышенный риск<small>"),
    ("<p>Запись по телефону или онлайн. Врач-генетик помогает выбрать панель под срок беременности и анамнез.</p>",
     "<p>Запись по телефону или онлайн. Врач-генетик — в центре или онлайн — помогает выбрать панель под срок беременности и анамнез.</p>"),
    ("<small>Все хромосомы плода и носительство у родителей</small>", "<small>Все хромосомы плода и носительство у будущей мамы</small>"),
    # почему Геномед
    ("Забор крови доступен в медицинском офисе, у партнёра в вашем городе или с выездом медсестры на дом.",
     "Сдать кровь можно в медицинском офисе, у партнёра в вашем городе или дома — с выездом медсестры."),
    # как проходит
    ("<h3>Забор крови</h3><p>20 мл венозной крови с 10 полных недель беременности.",
     "<h3>Взятие крови</h3><p>20 мл венозной крови с 10 полных недель беременности."),
    ("<h3>Взятие крови</h3><p>20 мл венозной крови с 10 полных недель беременности. Процедура ничем не отличается от обычного анализа.",
     "<h3>Взятие крови</h3><p>20 мл венозной крови с 10 полных недель беременности, как при обычном анализе. Перед этим подписывается договор информированного согласия."),
    ("<p>Выделение внеклеточной ДНК из плазмы и высокопроизводительное секвенирование. Каждый этап проходит внутрилабораторный контроль качества.</p>",
     "<p>В лаборатории из плазмы выделяют внеклеточную ДНК и прочитывают её на секвенаторе. Каждый этап проходит контроль качества.</p>"),
    ("Забор крови выполняет персонал лаборатории.", "Кровь берёт персонал лаборатории."),
    ("Набор для забора крови привозит медсестра.", "Медсестра приезжает с набором для взятия крови."),
    ("Подскажем ближайшее место сдачи и время — по телефону или в мессенджере.", "Подскажем ближайший медицинский офис и удобное время. Работаем по всей России, тест можно заказать и в другую страну."),
    # точность
    ("Оба метода безопасны для беременности и оба остаются скринингом: ни один из них не ставит диагноз. Разница — в сроке начала (с 10 полных недель против 11–13 недель) и в цене ошибки.",
     "Оба метода безопасны для беременности. НИПТ можно пройти раньше — с 10 полных недель, биохимический скрининг проводят на 11–13-й неделе."),
    # ограничения
    ("разделить вклад каждого плода в общий пул ДНК невозможно.", "ДНК разных плодов в крови матери разделить невозможно."),
    ("Если её меньше 4 %, результат не выдаётся — повторный забор крови на большем сроке лаборатория выполняет бесплатно.",
     "Если её меньше 4 %, результат не выдаётся — повторное взятие крови на большем сроке бесплатно."),
    # FAQ
    ("В отличие от амниоцентеза и биопсии ворсин хориона, НИПТ не требует прокола плодных оболочек и не несёт риска для беременности.",
     "Фрагменты ДНК плаценты сами попадают в кровь матери, поэтому прокол плодных оболочек, как при амниоцентезе или биопсии ворсин хориона, не нужен и риска для беременности нет."),
    ("если она оказалась ниже 4 %, потребуется повторный забор крови позже.", "если она оказалась ниже 4 %, кровь потребуется сдать повторно на более позднем сроке."),
    ("Так в заключении представлена отрицательная прогностическая ценность теста (NPV) — вероятность того, что низкий результат окажется ложноотрицательным. NPV исследования превышает 99,9 %, то есть остаточный риск крайне мал, но формально не равен нулю.",
     "Это вероятность того, что при низком риске по результату хромосомная аномалия у плода всё же есть. Для НИПТ она очень мала: надёжность низкого результата (NPV) превышает 99,9 %, но формально остаточный риск не равен нулю."),
    ("Через 8 дней после забора крови", "Через 8 дней после взятия крови"),
    ("вклад каждого плода в общий пул ДНК разделить нельзя.", "ДНК каждого плода в крови матери разделить нельзя."),
    # запись
    ("подскажем ближайшее место сдачи и ответим на вопросы.", "подскажем ближайший медицинский офис и ответим на вопросы."),
    ('\n        <p class="cta-phone">Если удобнее голосом — <a href="tel:+74956608377" class="mono">8 (495) 660-83-77</a>, клиентский сервис работает круглосуточно.</p>', ""),
    # подвал страницы
    ("ООО «Геномед», лаборатория сертифицирована", "ООО Геномед, лаборатория сертифицирована"),
    # раздел для врачей (переезжает из «Точности»)
    ("Порог, который делит результат надвое, — <b>1 : 100</b>.", "Граница между высоким и низким риском — <b>1 : 100</b>."),
    ("Лишняя 21-я хромосома — синдром Дауна, лишняя 18-я — синдром Эдвардса.", "Дополнительная копия 21-й хромосомы — признак синдрома Дауна, 18-й — синдрома Эдвардса."),
]
for old, new in EDITS:
    body = sub1(body, old, new)

# атрибуты демо-подсказок в форме
body = re.sub(r'\sdata-hint(?:-go|-text)?="[^"]*"', "", body)

# ---------------------------------------------------------------- разбор на блоки
def section(text: str, sid: str) -> str:
    m = re.search(rf'<section id="{sid}"[^>]*>.*?</section>', text, re.S)
    if not m:
        raise SystemExit(f"нет секции {sid}")
    return m.group(0)


blocks = {sid: section(body, sid) for sid in
          ["about", "panels", "compare", "quiz", "why", "how", "accuracy", "limits", "faq", "cta"]}
hero = re.search(r'<section class="hero">.*?</section>', body, re.S).group(0)
intro, notice = re.findall(r'<section style="padding-top:0;padding-bottom:[^"]*">.*?</section>', body, re.S)
photo = re.search(r'<figure class="photoband">.*?</figure>', body, re.S).group(0)
footer = re.search(r'<footer class="ldisc">.*?</footer>', body, re.S).group(0)
sticky = re.search(r'<div class="sticky-cta">.*?</div>', body, re.S).group(0)
script = re.search(r"<script>(.*?)</script>", body, re.S).group(1)
script = script[: script.index("/* ============================================================\n   3. ДЕМО-РЕЖИМ")]

# «Как это работает» из «Что вы получаете» переезжает в новый блок «Почему безопасно»
about = blocks["about"]
how_note = re.search(r'\n  <div class="wrap" style="max-width:1240px;margin-top:1.6em">\s*<div class="notice" style="border-left-color:var\(--cyan\)">.*?</div>\n  </div>\n', about, re.S)
about = about.replace(how_note.group(0), "\n")

# технические аккордеоны из «Точности» уходят в раздел «Для врачей»
acc = blocks["accuracy"]
acc_i = acc.index('<div class="wrap faq" style="margin-top:2.4em;">')
acc_main = acc[:acc_i].rstrip() + "\n</section>"
acc_details = acc[acc_i : acc.rindex("</section>")].rstrip()
acc_main = re.sub(r'\s*<p class="src">Показатели выявляемости[^<]*</p>', "", acc_main)

NAV = """<nav class="lnav" aria-label="Разделы страницы">
  <div class="wrap lnav__in">
    <span class="lnav__logo">НИПТ</span>
    <a href="#safe">Как работает</a>
    <a href="#accuracy">Точность</a>
    <a href="#panels">Панели и цены</a>
    <a href="#how">Как проходит</a>
    <a href="#results">Результат</a>
    <a href="#limits">Ограничения</a>
    <a href="#faq">Вопросы</a>
    <a href="#doctors">Врачам</a>
    <a class="btn-lnipt btn-lnipt--primary btn-lnipt--sm" href="#quiz"><span>Подобрать НИПТ</span></a>
  </div>
</nav>"""

IC = {
    "placenta": '<circle cx="12" cy="12" r="8"/><path d="M12 12V7"/><path d="m12 12 4 2.5"/><path d="m12 12-4 2.5"/><path d="M12 7l-2-2"/><path d="m12 7 2-2"/>',
    "drop": '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7Z"/>',
    "syringe": '<path d="m18 2 4 4"/><path d="m17 7 3-3"/><path d="M19 9 8.7 19.3c-1 1-2.5 1-3.4 0l-.6-.6c-1-1-1-2.5 0-3.4L15 5"/><path d="m9 11 4 4"/><path d="m5 19-3 3"/><path d="m14 4 6 6"/>',
    "dna": '<path d="m10 16 1.5 1.5"/><path d="m14 8-1.5-1.5"/><path d="M15 2c-1.798 1.998-2.518 3.995-2.807 5.993"/><path d="m16.5 10.5 1 1"/><path d="m17 6-2.891-2.891"/><path d="M2 15c6.667-6 13.333 0 20-6"/><path d="m20 9 .891.891"/><path d="M3.109 14.109 4 15"/><path d="m6.5 12.5 1 1"/><path d="m7 18 2.891 2.891"/><path d="M9 22c1.798-1.998 2.518-3.995 2.807-5.993"/>',
    "report": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="m9 15 2 2 4-4"/>',
}
STAGES = [
    ("placenta", "Плацента", "Во время беременности фрагменты ДНК плаценты постоянно попадают в кровь матери."),
    ("drop", "Кровь мамы", "Там они смешиваются с ДНК самой мамы. Доля ДНК плода — плодная фракция — к 10 неделям обычно достигает 4 % и выше."),
    ("syringe", "Взятие крови", "Поэтому достаточно взять 20 мл крови из вены, как при обычном анализе. Из плазмы выделяют внеклеточную ДНК."),
    ("dna", "Секвенатор", "Прочитывает фрагменты ДНК, а программа считает, сколько прочтений приходится на каждую хромосому."),
    ("report", "Заключение", "Больше прочтений по хромосоме, чем ожидается, — признак анеуплоидии. Врач-генетик оформляет заключение: высокий или низкий риск."),
]


def svg_icon(name: str) -> str:
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{IC[name]}</svg>'


SAFE_HEAD = """<section id="safe" style="padding-top:0">
  <div class="wrap section-head">
    <span class="section-eyebrow">Как работает НИПТ</span>
    <h2>Почему исследование <em>безопасно</em></h2>
    <p class="lead">Во время беременности фрагменты ДНК плаценты попадают в кровь матери. Поэтому для анализа достаточно взять кровь из вены: прокол плодных оболочек не нужен, риска для беременности нет.</p>
  </div>
"""
SAFE_STATIC = SAFE_HEAD + '  <div class="wrap">\n    <ol class="dnapath">\n' + "".join(
    f'      <li><span class="dnapath__ic">{svg_icon(ic)}</span><span class="dnapath__n mono">0{i + 1}</span><b>{t}</b><span class="dnapath__t">{d}</span></li>\n'
    for i, (ic, t, d) in enumerate(STAGES)
) + "    </ol>\n  </div>\n</section>"

DOCTORS = f"""<section id="doctors" style="padding-top:0">
  <div class="wrap section-head">
    <span class="section-eyebrow">Для врачей</span>
    <h2>Интерпретация <em>заключения</em></h2>
    <p class="lead">Рекомендация предлагать скрининг по внеклеточной ДНК всем беременным — ACOG, SMFM, ISPD, ACMG. Показатели выявляемости на странице приведены по опубликованным данным для комбинированного скрининга первого триместра и скрининга по внеклеточной ДНК.</p>
  </div>
  {acc_details}
</section>"""

MODAL = """<div class="pmodal" id="modal-callback" hidden>
  <div class="pmodal__scrim" data-pm-close></div>
  <div class="pmodal__card" role="dialog" aria-modal="true" aria-labelledby="pm-title">
    <button class="pmodal__x" type="button" aria-label="Закрыть" data-pm-close>×</button>
    <h3 id="pm-title">Выберите удобный способ связи</h3>
    <p>Поможем выбрать панель, подскажем ближайший медицинский офис и ответим на вопросы.</p>
    <div class="pmodal__row">
      <a class="btn-lnipt btn-lnipt--primary" href="https://t.me/genomed_b2c_bot" target="_blank" rel="noopener"><span>Telegram</span></a>
      <a class="btn-lnipt btn-lnipt--primary" href="https://wa.me/74956608377" target="_blank" rel="noopener"><span>WhatsApp</span></a>
      <a class="btn-lnipt btn-lnipt--primary" href="https://max.ru/id7701759381_bot" target="_blank" rel="noopener"><span>MAX</span></a>
    </div>
    <p class="pmodal__tel">или по телефону <a href="tel:+74956608377" class="mono">8 (495) 660-83-77</a></p>
    <p class="pmodal__note">Превью: на сайте здесь открывается штатная форма заявки.</p>
  </div>
</div>"""

MODAL_JS = """
/* ============================================================
   3. ПРЕВЬЮ: окно «способ связи» вместо сайтовой формы #modal-callback
   На genomed.ru эту роль выполняет штатная форма темы — блок не переносится.
   ============================================================ */
(function () {
  var m = document.getElementById('modal-callback');
  if (!m) return;
  var last = null;
  function open(from) { last = from; m.hidden = false; document.documentElement.style.overflow = 'hidden'; m.querySelector('.pmodal__x').focus(); }
  function close() { m.hidden = true; document.documentElement.style.overflow = ''; if (last) last.focus(); }
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href="#modal-callback"]');
    if (a) { e.preventDefault(); open(a); return; }
    if (e.target.closest('[data-pm-close]')) close();
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !m.hidden) close(); });
  var form = document.getElementById('leadform');
  if (form) form.addEventListener('submit', function (e) { e.preventDefault(); open(form.querySelector('button')); });
})();
"""

EXTRA_CSS = """
/* ——— полоса версий (только для превью) ——— */
.vbar{background:#0A2540;color:#fff;font-family:var(--body);font-size:13px}
.vbar__in{display:flex;align-items:center;gap:6px 20px;flex-wrap:wrap;min-height:44px;padding-block:6px}
.vbar b{font-weight:500;color:#8FAECF}
.vbar a{color:rgba(255,255,255,.66);text-decoration:none;font-weight:600;padding:3px 0;border-bottom:2px solid transparent}
.vbar a:hover{color:#fff}
.vbar a.on{color:#fff;border-bottom-color:var(--cyan)}

/* ——— путь ДНК: плацента → кровь → пробирка → секвенатор → заключение ——— */
.dnapath{list-style:none;margin:2.2em 0 0;padding:0;display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:1em;counter-reset:none}
.dnapath li{position:relative;background:var(--bg-card);border:1px solid var(--line);border-radius:var(--r-lg);padding:1.4em 1.2em 1.5em}
.dnapath li:not(:last-child)::after{content:"";position:absolute;right:-.85em;top:2.35em;width:.7em;height:.7em;border-top:2px solid var(--blue);border-right:2px solid var(--blue);transform:rotate(45deg);z-index:1}
.dnapath__ic{display:grid;place-items:center;width:44px;height:44px;border-radius:var(--r-md);background:var(--accent-soft);color:var(--blue);margin-bottom:1em}
.dnapath__ic svg{width:24px;height:24px}
.dnapath__n{display:block;font-size:.72em;font-weight:700;color:var(--blue);letter-spacing:.06em;margin-bottom:.3em}
.dnapath b{display:block;font-family:var(--disp);font-size:1.02em;font-weight:800;letter-spacing:-.01em}
.dnapath__t{display:block;margin-top:.45em;font-size:.88em;line-height:1.5;color:var(--ink-2)}
@media(max-width:1000px){.dnapath{grid-template-columns:minmax(0,1fr)}.dnapath li{display:grid;grid-template-columns:44px minmax(0,1fr);column-gap:1em}
  .dnapath__ic{grid-row:span 3;margin:0}.dnapath li:not(:last-child)::after{right:auto;left:2.2em;top:auto;bottom:-.75em;transform:rotate(135deg)}}

/* ——— окно «способ связи» (превью) ——— */
.pmodal{position:fixed;inset:0;z-index:200;display:grid;place-items:center;padding:1em}
.pmodal[hidden]{display:none}
.pmodal__scrim{position:absolute;inset:0;background:rgba(10,37,64,.5)}
.pmodal__card{position:relative;width:min(460px,100%);background:#fff;border-radius:var(--r-lg);padding:2em 1.8em 1.6em;box-shadow:var(--shadow-lg)}
.pmodal__card h3{margin:0 2em .5em 0;font-family:var(--disp);font-size:1.3em;letter-spacing:-.02em}
.pmodal__card p{margin:0;color:var(--ink-2);font-size:.95em;line-height:1.5}
.pmodal__row{display:grid;gap:.5em;margin:1.3em 0 1em}
.pmodal__row .btn-lnipt{width:100%;justify-content:center}
.pmodal__tel a{color:var(--blue);font-weight:700}
.pmodal__note{margin-top:1em !important;font-size:.78em !important;color:var(--muted) !important}
.pmodal__x{position:absolute;top:.7em;right:.8em;width:36px;height:36px;border-radius:50%;border:0;background:var(--line-soft);color:var(--ink);font-size:1.3em;cursor:pointer}
"""


def vbar(active: str) -> str:
    tabs = [("anim", "index.html", "С анимацией"), ("static", "bez-animacii.html", "Без анимации")]
    links = "".join(f'<a href="{href}"' + (' class="on" aria-current="page"' if key == active else "") + f">{label}</a>"
                    for key, href, label in tabs)
    return f'<div class="vbar"><div class="wrap vbar__in"><b>Версии для сравнения:</b>{links}</div></div>'


def page(version: str, blocks_in: dict, css_all: str, js_extra: str = "") -> str:
    title = "НИПТ — Геномед · с анимацией" if version == "anim" else "НИПТ — Геномед · без анимации"
    head_extra = '<meta name="theme-color" content="#0A2540">\n'
    order = [
        vbar(version), NAV, blocks_in["hero"], intro, notice, blocks_in["safe"], blocks_in["about"], blocks_in["acc"],
        blocks_in["panels"], blocks["compare"], blocks["quiz"], blocks_in["how"], RESULTS, LIMITS,
        blocks["why"], blocks["faq"], DOCTORS, blocks["cta"], footer, sticky, MODAL,
    ]
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
{head_extra}<title>{title}</title>
{head_links}<style>{css_all}</style>
</head>
<body>
{chr(10).join(x for x in order if x)}
<script>{script}{MODAL_JS}{js_extra}</script>
</body>
</html>
"""


PARTS = HERE / "parts"
V2 = HERE / "v2"
RESULTS = (PARTS / "results.html").read_text(encoding="utf-8")
LIMITS = (PARTS / "limits.html").read_text(encoding="utf-8")
common_css = (PARTS / "common.css").read_text(encoding="utf-8")
static_css = (PARTS / "static.css").read_text(encoding="utf-8")
anim_css = (V2 / "v2.css").read_text(encoding="utf-8")
anim_js = (V2 / "fx.js").read_text(encoding="utf-8")
scene = (V2 / "scene.html").read_text(encoding="utf-8")
fpv = (V2 / "fpv.html").read_text(encoding="utf-8")

# ---------------------------------------------------------------- общее для обеих вкладок
# первый экран: текст слева, 3D-пробирка справа (фото с поцелуем малыша убрано)
hero_new = sub1(hero, '<div class="wrap hero__grid">', '<div class="wrap hv2">')
hero_new = sub1(hero_new, "\n\n    \n  </div>\n</section>",
    '\n    <figure class="hv2__tube"><img src="img/hero-tube.webp" alt="Пробирка с кровью: в плазме — фрагменты ДНК" width="279" height="1100" fetchpriority="high">'
    '<figcaption class="l"><b>20 мл крови из вены</b>без прокола и подготовки</figcaption>'
    '<figcaption><b>Результат — через 8 дней</b>заключение врач-генетик разбирает вместе с вами</figcaption></figure>\n  </div>\n</section>')


def swap_badges(block: str, scope_start: str, images: list[tuple[str, str]]) -> str:
    """Плоские значки <span class="badge">…</span> → 3D-картинки, по порядку."""
    head, tail = block[: block.index(scope_start)], block[block.index(scope_start):]
    for name, cls in images:
        m = re.search(r'<span class="badge"><svg.*?</svg></span>', tail, re.S)
        if not m:
            raise SystemExit(f"не нашла значок для {name}")
        tail = tail[: m.start()] + f'<img class="{cls}" src="img/{name}.webp" alt="" loading="lazy">' + tail[m.end():]
    return head + tail


about_new = swap_badges(about, '<div class="wrap bens"', [(n, "ben__img") for n in
                        ("ic-chromosomes", "ic-drop", "ic-calendar", "ic-doctor", "ic-shield")])

# панели: число синдромов точками + для чего результаты экспертной
LADDER = [(1, "1 синдром"), (3, "3 синдрома"), (7, "7 синдромов"), (13, "13 синдромов"), (38, "38+ синдромов")]
parts = re.split(r'(<p class="desc">[^<]*</p>)', blocks["panels"])
if len(parts) != 11:
    raise SystemExit(f"ожидалось 5 карточек панелей, найдено {(len(parts) - 1) // 2}")
for n, (cnt, label) in enumerate(LADDER):
    parts[1 + n * 2] += f'\n      <div class="ladder" aria-label="{label}">' + "<i></i>" * cnt + f"<b>{label}</b></div>"
parts[9] += ('\n      <p class="use">Результаты пригодятся и&nbsp;при планировании следующих беременностей,'
             ' и&nbsp;чтобы решить, нужно ли обследовать партнёра.</p>')
panels_new = "".join(parts)

# как проходит: 3D-иконки «где сдать» и восемь дней полосой
DAYS8 = """
  <div class="wrap days8" aria-label="Восемь дней: день 0 — взятие крови, дни 1–7 — лаборатория, день 8 — заключение">
    <div class="days8__row"><div class="d0"><b>День 0</b><span>Взятие крови</span></div>""" + "".join(f"<i>{d}</i>" for d in range(1, 8)) + """<div class="d8"><b>День 8</b><span>Заключение на почте</span></div></div>
    <div class="days8__lab"><span></span><span>лаборатория: выделение ДНК, секвенирование, расчёт риска</span><span></span></div>
    <p class="days8__note">Т21, базовая и стандартная панели — 8 календарных дней, расширенная и экспертная — 8 рабочих.</p>
  </div>"""
how_new = sub1(blocks["how"], '\n\n  <div class="wrap where">', DAYS8 + '\n\n  <div class="wrap where">')
how_new = swap_badges(how_new, '<div class="wrap where">', [(n, "wcard__img") for n in ("ic-office", "ic-partner", "ic-home")])

# hover только у мыши (mobile-native): иначе на телефоне залипает после тапа
css_base = re.sub(r"(?m)^([^@\n{]*:hover[^{\n]*\{[^}\n]*\})\s*$", r"@media (hover:hover) and (pointer:fine){\1}", css) + EXTRA_CSS + common_css

# ---------------------------------------------------------------- вкладка «С анимацией»
ci = acc_main.index('<div class="cmp-card">')
cj = acc_main.rindex("  </div>\n</section>")
acc_anim = acc_main[:ci] + fpv.strip() + "\n" + acc_main[cj:]
anim = page("anim", {"hero": hero_new, "safe": scene, "about": about_new, "acc": acc_anim, "panels": panels_new, "how": how_new},
            css_base + anim_css, anim_js)
(HERE / "index.html").write_text(anim, encoding="utf-8")

# ---------------------------------------------------------------- вкладка «Без анимации»
static = page("static", {"hero": hero_new, "safe": SAFE_STATIC, "about": about_new, "acc": acc_main, "panels": panels_new, "how": how_new},
              css_base + static_css)
(HERE / "bez-animacii.html").write_text(static, encoding="utf-8")

# старый адрес наглядной версии ведёт на вкладку с анимацией
(HERE / "naglyadnaya.html").write_text(
    '<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow">'
    '<meta http-equiv="refresh" content="0; url=index.html"><link rel="canonical" href="index.html"><title>НИПТ — Геномед</title></head>'
    '<body><a href="index.html">Открыть страницу</a></body></html>\n', encoding="utf-8")

shutil.copy(SRC / "doctor.jpg", HERE / "doctor.jpg")
print("ok:", len(anim), len(static))
