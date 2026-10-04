#!/usr/bin/env python3
"""ابزار محاسبات استرولوژی: چارت تولد، پروفکشن، سولار ریترن، ترانزیت، فرداریا، داشا.

نیازمندی: pip install pyswisseph
مثال‌ها:
  python3 tools/astro.py natal   --date 1995-06-21 --time 14:30 --tz 4.5 --lat 35.6892 --lon 51.3890
  python3 tools/astro.py profection --date 1995-06-21 --on 2026-10-04
  python3 tools/astro.py sr      --date 1995-06-21 --time 14:30 --tz 4.5 --lat 35.6892 --lon 51.3890 --year 2026 [--sr-lat .. --sr-lon .. --sr-tz ..]
  python3 tools/astro.py transit --date 1995-06-21 --time 14:30 --tz 4.5 --lat 35.6892 --lon 51.3890 --on 2026-10-04
  python3 tools/astro.py firdaria --date 1995-06-21 --time 14:30 --tz 4.5 --lat 35.6892 --lon 51.3890
  python3 tools/astro.py dasha   --date 1995-06-21 --time 14:30 --tz 4.5 --lat 35.6892 --lon 51.3890
--tz اختلاف ساعت محلی با UTC در لحظهٔ تولد است (ایران: 3.5، و در تابستان‌های پیش از ۱۴۰۱: 4.5).
"""
import argparse
import datetime as dt

import swisseph as swe

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
SIGNS_FA = ["حمل", "ثور", "جوزا", "سرطان", "اسد", "سنبله",
            "میزان", "عقرب", "قوس", "جدی", "دلو", "حوت"]

PLANETS = [("Sun", swe.SUN), ("Moon", swe.MOON), ("Mercury", swe.MERCURY),
           ("Venus", swe.VENUS), ("Mars", swe.MARS), ("Jupiter", swe.JUPITER),
           ("Saturn", swe.SATURN), ("Uranus", swe.URANUS), ("Neptune", swe.NEPTUNE),
           ("Pluto", swe.PLUTO), ("North Node", swe.TRUE_NODE), ("Chiron", swe.CHIRON)]
TRAD = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]

# حاکمان سنتی (هفت سیارهٔ کلاسیک) و حاکمان مدرن
RULER = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
         "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
MODERN_RULER = {7: "Pluto", 10: "Uranus", 11: "Neptune"}
EXALT = {"Sun": (0, 19), "Moon": (1, 3), "Mercury": (5, 15), "Venus": (11, 27),
         "Mars": (9, 28), "Jupiter": (3, 15), "Saturn": (6, 21)}
# مثلثه (دوروتئوس): روز، شب، شریک
TRIPLICITY = {0: ("Sun", "Jupiter", "Saturn"), 1: ("Venus", "Moon", "Mars"),
              2: ("Saturn", "Mercury", "Jupiter"), 3: ("Venus", "Mars", "Moon")}
# حدود مصری: (سیاره، درجهٔ پایان)
TERMS = [
    [("Jupiter", 6), ("Venus", 12), ("Mercury", 20), ("Mars", 25), ("Saturn", 30)],
    [("Venus", 8), ("Mercury", 14), ("Jupiter", 22), ("Saturn", 27), ("Mars", 30)],
    [("Mercury", 6), ("Jupiter", 12), ("Venus", 17), ("Mars", 24), ("Saturn", 30)],
    [("Mars", 7), ("Venus", 13), ("Mercury", 19), ("Jupiter", 26), ("Saturn", 30)],
    [("Jupiter", 6), ("Venus", 11), ("Saturn", 18), ("Mercury", 24), ("Mars", 30)],
    [("Mercury", 7), ("Venus", 17), ("Jupiter", 21), ("Mars", 28), ("Saturn", 30)],
    [("Saturn", 6), ("Mercury", 14), ("Jupiter", 21), ("Venus", 28), ("Mars", 30)],
    [("Mars", 7), ("Venus", 11), ("Mercury", 19), ("Jupiter", 24), ("Saturn", 30)],
    [("Jupiter", 12), ("Venus", 17), ("Mercury", 21), ("Saturn", 26), ("Mars", 30)],
    [("Mercury", 7), ("Jupiter", 14), ("Venus", 22), ("Saturn", 26), ("Mars", 30)],
    [("Mercury", 7), ("Venus", 13), ("Jupiter", 20), ("Mars", 25), ("Saturn", 30)],
    [("Venus", 12), ("Jupiter", 16), ("Mercury", 19), ("Mars", 28), ("Saturn", 30)],
]
CHALDEAN = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]

ASPECTS = [(0, "Conjunction ☌"), (60, "Sextile ⚹"), (90, "Square □"),
           (120, "Trine △"), (180, "Opposition ☍")]


def fmt(lon):
    s = int(lon // 30)
    d = lon % 30
    deg = int(d)
    minute = int(round((d - deg) * 60))
    if minute == 60:
        deg, minute = deg + 1, 0
    return f"{deg:2d}°{minute:02d}' {SIGNS[s]:<11} ({SIGNS_FA[s]})"


def to_jd(date, time, tz):
    y, m, d = map(int, date.split("-"))
    hh, mm = (map(int, time.split(":")) if time else (12, 0))
    local = dt.datetime(y, m, d, hh, mm)
    utc = local - dt.timedelta(hours=tz)
    return swe.julday(utc.year, utc.month, utc.day, utc.hour + utc.minute / 60 + utc.second / 3600)


def jd_to_local(jd, tz):
    y, m, d, h = swe.revjul(jd)
    base = dt.datetime(y, m, d) + dt.timedelta(hours=h) + dt.timedelta(hours=tz)
    return base.strftime("%Y-%m-%d %H:%M:%S")


def face(lon):
    s = int(lon // 30)
    idx = (CHALDEAN.index("Mars") + s * 3 + int((lon % 30) // 10)) % 7
    return CHALDEAN[idx]


def term(lon):
    s = int(lon // 30)
    for p, end in TERMS[s]:
        if lon % 30 < end:
            return p


def essential(name, lon, diurnal):
    """امتیاز دیگنیتی ذاتی به روش لیلی (فقط هفت سیارهٔ سنتی)."""
    if name not in TRAD:
        return "", 0
    s = int(lon // 30)
    tags, score = [], 0
    if RULER[s] == name:
        tags.append("Domicile+5"); score += 5
    if name in EXALT and EXALT[name][0] == s:
        tags.append("Exalt+4"); score += 4
    day, night, part = TRIPLICITY[s % 4]
    if name == (day if diurnal else night):
        tags.append("Trip+3"); score += 3
    if term(lon) == name:
        tags.append("Term+2"); score += 2
    if face(lon) == name:
        tags.append("Face+1"); score += 1
    if RULER[(s + 6) % 12] == name:
        tags.append("Detriment-5"); score -= 5
    if name in EXALT and (EXALT[name][0] + 6) % 12 == s:
        tags.append("Fall-4"); score -= 4
    if score <= 0 and not any(t.startswith(("Domicile", "Exalt", "Trip", "Term", "Face")) for t in tags):
        tags.append("Peregrine")
    return " ".join(tags), score


class Chart:
    def __init__(self, jd, lat, lon, hsys=b"P"):
        self.jd, self.lat, self.lon = jd, lat, lon
        self.cusps, self.ascmc = swe.houses(jd, lat, lon, hsys)
        self.asc, self.mc = self.ascmc[0], self.ascmc[1]
        self.armc = self.ascmc[2]
        self.eps = swe.calc_ut(jd, swe.ECL_NUT)[0][0]
        self.pos = {}
        for name, pid in PLANETS:
            try:
                xx, _ = swe.calc_ut(jd, pid, swe.FLG_SPEED)
            except swe.Error:
                continue
            self.pos[name] = (xx[0], xx[1], xx[3])
        sun = self.pos["Sun"]
        self.diurnal = self.house_float(sun[0], sun[1]) >= 7.0
        n = self.pos["North Node"]
        self.pos["South Node"] = ((n[0] + 180) % 360, 0.0, n[2])

    def house_float(self, lon, lat=0.0):
        return swe.house_pos(self.armc, self.lat, self.eps, (lon, lat), b"P")

    def ws_house(self, lon):
        return (int(lon // 30) - int(self.asc // 30)) % 12 + 1

    def quad_house(self, lon):
        c = list(self.cusps)
        for i in range(12):
            a, b = c[i], c[(i + 1) % 12]
            if (lon - a) % 360 < (b - a) % 360:
                return i + 1
        return 12

    def lot(self, kind):
        s, m = self.pos["Sun"][0], self.pos["Moon"][0]
        if (kind == "Fortune") == self.diurnal:
            return (self.asc + m - s) % 360
        return (self.asc + s - m) % 360


def aspects_between(a_pos, b_pos, orb, same=False):
    out = []
    names_a, names_b = list(a_pos), list(b_pos)
    for i, a in enumerate(names_a):
        for j, b in enumerate(names_b):
            if same and j <= i:
                continue
            if {a, b} <= {"North Node", "South Node"}:
                continue
            diff = abs((a_pos[a][0] - b_pos[b][0] + 180) % 360 - 180)
            for ang, label in ASPECTS:
                if abs(diff - ang) <= orb:
                    out.append((abs(diff - ang), a, label, b))
    return sorted(out)


def print_chart(ch, title):
    print(f"\n=== {title} ===")
    print(f"Sect (فرقه): {'Diurnal روزانه' if ch.diurnal else 'Nocturnal شبانه'}")
    print(f"ASC  {fmt(ch.asc)}   ruler: {RULER[int(ch.asc // 30)]}")
    print(f"MC   {fmt(ch.mc)}   (MC in whole-sign house {ch.ws_house(ch.mc)})")
    print(f"{'Planet':<11} {'Position':<32} R  WS  Plac  Dignity")
    for name, (lon, lat, spd) in ch.pos.items():
        tags, score = essential(name, lon, ch.diurnal)
        r = "R" if spd < 0 and name not in ("North Node", "South Node") else " "
        sc = f"[{score:+d}] {tags}" if name in TRAD else ""
        print(f"{name:<11} {fmt(lon):<32} {r} {ch.ws_house(lon):3d} {ch.quad_house(lon):5d}  {sc}")
    for lot in ("Fortune", "Spirit"):
        print(f"Lot of {lot:<8} {fmt(ch.lot(lot))}  WS house {ch.ws_house(ch.lot(lot))}")
    print("\nPlacidus cusps:")
    for i, c in enumerate(ch.cusps):
        print(f"  {i+1:2d}: {fmt(c)}")
    print("\nWhole-sign house rulers (حاکمان خانه‌ها) → where they sit:")
    for h in range(12):
        s = (int(ch.asc // 30) + h) % 12
        r = RULER[s]
        mod = f" / modern {MODERN_RULER[s]}" if s in MODERN_RULER else ""
        print(f"  H{h+1:<2} {SIGNS[s]:<11} ruler {r:<8} in H{ch.ws_house(ch.pos[r][0])}{mod}")


def profection(birth_date, on_date, asc_sign=None):
    b = dt.date.fromisoformat(birth_date)
    o = dt.date.fromisoformat(on_date)
    age = o.year - b.year - ((o.month, o.day) < (b.month, b.day))
    house = age % 12 + 1
    res = {"age": age, "house": house}
    if asc_sign is not None:
        s = (asc_sign + age) % 12
        res["sign"] = s
        res["lord"] = RULER[s]
        last_bd = dt.date(b.year + age, b.month, b.day if not (b.month == 2 and b.day == 29) else 28)
        month_idx = (o.year - last_bd.year) * 12 + o.month - last_bd.month - (o.day < last_bd.day)
        ms = (s + month_idx) % 12
        res["month"] = (month_idx + 1, ms, RULER[ms])
    return res


def solar_return(natal, year, birth_month, birth_day):
    target = natal.pos["Sun"][0]
    jd = swe.julday(year, birth_month, birth_day, 12.0)
    for _ in range(50):
        lon, _, _, spd = swe.calc_ut(jd, swe.SUN, swe.FLG_SPEED)[0][:4]
        diff = (target - lon + 180) % 360 - 180
        jd += diff / spd
        if abs(diff) < 1e-7:
            break
    return jd


FIRDAR_DAY = [("Sun", 10), ("Venus", 8), ("Mercury", 13), ("Moon", 9), ("Saturn", 11),
              ("Jupiter", 12), ("Mars", 7), ("North Node", 3), ("South Node", 2)]
FIRDAR_NIGHT = [("Moon", 9), ("Saturn", 11), ("Jupiter", 12), ("Mars", 7), ("Sun", 10),
                ("Venus", 8), ("Mercury", 13), ("North Node", 3), ("South Node", 2)]
FIRDAR_NIGHT_ALT = [("Moon", 9), ("Saturn", 11), ("Jupiter", 12), ("Mars", 7), ("North Node", 3),
                    ("South Node", 2), ("Sun", 10), ("Venus", 8), ("Mercury", 13)]


def firdaria(birth_dt, diurnal, alt_night=False, cycles=2):
    seq = FIRDAR_DAY if diurnal else (FIRDAR_NIGHT_ALT if alt_night else FIRDAR_NIGHT)
    rows, start = [], birth_dt
    for c in range(cycles):
        for planet, yrs in seq:
            end = add_years(start, yrs)
            subs = []
            if "Node" not in planet:
                k = CHALDEAN.index(planet)
                for i in range(7):
                    s0 = add_years(start, yrs * i / 7)
                    subs.append((CHALDEAN[(k + i) % 7], s0))
            rows.append((planet, yrs, start, end, subs))
            start = end
    return rows


def add_years(d, years):
    return d + dt.timedelta(days=years * 365.2422)


DASHA = [("Ketu", 7), ("Venus", 20), ("Sun", 6), ("Moon", 10), ("Mars", 7),
         ("Rahu", 18), ("Jupiter", 16), ("Saturn", 19), ("Mercury", 17)]
NAKSHATRAS = ["Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
              "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
              "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
              "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
              "Uttara Bhadrapada", "Revati"]


def vimshottari(jd, birth_dt, year_days=365.25):
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    moon = swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]
    span = 360 / 27
    nak = int(moon // span)
    frac_done = (moon % span) / span
    lord_idx = nak % 9
    lord, yrs = DASHA[lord_idx]
    elapsed = frac_done * yrs
    start = birth_dt - dt.timedelta(days=elapsed * year_days)
    out = []
    for k in range(9):
        p, y = DASHA[(lord_idx + k) % 9]
        end = start + dt.timedelta(days=y * year_days)
        subs, s0 = [], start
        for m in range(9):
            q, z = DASHA[(lord_idx + k + m) % 9]
            e0 = s0 + dt.timedelta(days=y * z / 120 * year_days)
            subs.append((q, s0, e0))
            s0 = e0
        out.append((p, y, start, end, subs))
        start = end
    return moon, NAKSHATRAS[nak], (moon % span) / (span / 4), out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["natal", "profection", "sr", "transit", "firdaria", "dasha"])
    ap.add_argument("--date", required=True, help="تاریخ تولد میلادی YYYY-MM-DD")
    ap.add_argument("--time", help="ساعت تولد HH:MM (محلی)")
    ap.add_argument("--tz", type=float, default=0.0)
    ap.add_argument("--lat", type=float)
    ap.add_argument("--lon", type=float)
    ap.add_argument("--on", help="تاریخ مورد نظر برای پروفکشن/ترانزیت")
    ap.add_argument("--year", type=int, help="سال سولار ریترن")
    ap.add_argument("--sr-lat", type=float)
    ap.add_argument("--sr-lon", type=float)
    ap.add_argument("--sr-tz", type=float)
    ap.add_argument("--orb", type=float, default=2.0, help="اُرب ترانزیت (درجه)")
    ap.add_argument("--alt-night", action="store_true", help="ترتیب جایگزین فرداریای شبانه (گره‌ها پس از مریخ)")
    a = ap.parse_args()

    swe.set_ephe_path(None)
    if a.cmd == "profection" and a.lat is None:
        p = profection(a.date, a.on or dt.date.today().isoformat())
        print(f"Age {p['age']} → profected house {p['house']} (برای نشانه و ارباب سال، ساعت و مکان تولد لازم است)")
        return

    jd = to_jd(a.date, a.time, a.tz)
    natal = Chart(jd, a.lat, a.lon)
    birth_dt = dt.datetime.fromisoformat(f"{a.date}T{a.time or '12:00'}")

    if a.cmd == "natal":
        print_chart(natal, "Natal Chart (چارت تولد)")
        print("\nNatal aspects (orb 6°):")
        for o, x, lab, y in aspects_between(natal.pos, natal.pos, 6.0, same=True):
            print(f"  {x:<10} {lab:<15} {y:<10} orb {o:.2f}°")

    elif a.cmd == "profection":
        on = a.on or dt.date.today().isoformat()
        p = profection(a.date, on, int(natal.asc // 30))
        lord = p["lord"]
        lon = natal.pos[lord][0]
        print(f"Date {on}: age {p['age']}")
        print(f"Profected house: {p['house']}  sign: {SIGNS[p['sign']]} ({SIGNS_FA[p['sign']]})")
        print(f"Lord of the Year (ارباب سال): {lord} — natal {fmt(lon)} WS house {natal.ws_house(lon)}")
        mi, ms, ml = p["month"]
        print(f"Monthly profection: month {mi} → {SIGNS[ms]} lord {ml}")
        occupants = [n for n, v in natal.pos.items() if int(v[0] // 30) == p["sign"]]
        print(f"Natal planets in profected sign (activated): {', '.join(occupants) or '—'}")

    elif a.cmd == "sr":
        year = a.year or dt.date.today().year
        jd_sr = solar_return(natal, year, birth_dt.month, birth_dt.day)
        lat = a.sr_lat if a.sr_lat is not None else a.lat
        lon = a.sr_lon if a.sr_lon is not None else a.lon
        tz = a.sr_tz if a.sr_tz is not None else a.tz
        sr = Chart(jd_sr, lat, lon)
        print(f"Solar Return {year}: {jd_to_local(jd_sr, tz)} local (UTC{tz:+g}) at {lat}, {lon}")
        print_chart(sr, f"Solar Return {year}")
        print("\n--- SR ⟷ Natal overlay ---")
        print(f"SR ASC {fmt(sr.asc)} falls in natal WS house {natal.ws_house(sr.asc)}, "
              f"Placidus house {natal.quad_house(sr.asc)}")
        r = RULER[int(sr.asc // 30)]
        print(f"SR ASC ruler {r}: SR WS house {sr.ws_house(sr.pos[r][0])}, natal WS house {natal.ws_house(sr.pos[r][0])}")
        print(f"SR Sun in SR WS house {sr.ws_house(sr.pos['Sun'][0])}; SR Moon {fmt(sr.pos['Moon'][0])} "
              f"SR house {sr.ws_house(sr.pos['Moon'][0])}, natal house {natal.ws_house(sr.pos['Moon'][0])}")
        p = profection(a.date, f"{year}-{birth_dt.month:02d}-{birth_dt.day:02d}", int(natal.asc // 30))
        lord = p["lord"]
        print(f"Profection for this year: house {p['house']} {SIGNS[p['sign']]}, Lord of Year {lord}; "
              f"in SR: {fmt(sr.pos[lord][0])} SR house {sr.ws_house(sr.pos[lord][0])}")
        print("\nSR planets → natal houses (WS):")
        for n, v in sr.pos.items():
            print(f"  {n:<11} natal H{natal.ws_house(v[0])}")

    elif a.cmd == "transit":
        on = a.on or dt.date.today().isoformat()
        tj = to_jd(on, "12:00", a.tz)
        tr = Chart(tj, a.lat, a.lon)
        print(f"Transits for {on} (noon local)")
        for n, (lon, lat, spd) in tr.pos.items():
            r = "R" if spd < 0 and "Node" not in n else " "
            print(f"  {n:<11} {fmt(lon)} {r} → natal WS H{natal.ws_house(lon):<2} Plac H{natal.quad_house(lon)}")
        pts = dict(natal.pos)
        pts["ASC"] = (natal.asc, 0, 0)
        pts["MC"] = (natal.mc, 0, 0)
        print(f"\nTransit → natal aspects (orb {a.orb}°):")
        for o, x, lab, y in aspects_between(tr.pos, pts, a.orb):
            print(f"  T.{x:<10} {lab:<15} N.{y:<10} orb {o:.2f}°")
        p = profection(a.date, on, int(natal.asc // 30))
        lord = p["lord"]
        print(f"\nLord of Year: {lord} — transiting {fmt(tr.pos[lord][0])}, natal WS H{natal.ws_house(tr.pos[lord][0])}")

    elif a.cmd == "firdaria":
        print(f"Sect: {'Diurnal' if natal.diurnal else 'Nocturnal'}")
        for planet, yrs, s, e, subs in firdaria(birth_dt, natal.diurnal, a.alt_night):
            print(f"{planet:<11} {yrs:2d}y  {s:%Y-%m-%d} → {e:%Y-%m-%d}")
            for q, s0 in subs:
                print(f"      {planet[:3]}/{q:<8} from {s0:%Y-%m-%d}")

    elif a.cmd == "dasha":
        moon, nak, pada, rows = vimshottari(jd, birth_dt)
        print(f"Sidereal (Lahiri) Moon {fmt(moon)} — Nakshatra {nak}, pada {int(pada)+1}")
        for p, y, s, e, subs in rows:
            print(f"{p:<8} {y:2d}y  {s:%Y-%m-%d} → {e:%Y-%m-%d}")
            for q, s0, e0 in subs:
                print(f"      {p[:3]}/{q:<8} {s0:%Y-%m-%d} → {e0:%Y-%m-%d}")


if __name__ == "__main__":
    main()
