#!/usr/bin/env python3
"""ورود سیارات به نشانه‌ها و ایستگاه‌های رجعت/استقامت در یک بازهٔ زمانی (UTC).
python3 tools/sky_events.py 2026-01-01 2028-01-01
"""
import sys
import datetime as dt
import swisseph as swe

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
BODIES = [("Mercury", swe.MERCURY), ("Venus", swe.VENUS), ("Mars", swe.MARS),
          ("Jupiter", swe.JUPITER), ("Saturn", swe.SATURN), ("Uranus", swe.URANUS),
          ("Neptune", swe.NEPTUNE), ("Pluto", swe.PLUTO), ("North Node", swe.TRUE_NODE)]


def jd(d):
    return swe.julday(d.year, d.month, d.day, 0.0)


def show(j):
    y, m, d, h = swe.revjul(j)
    return (dt.datetime(y, m, d) + dt.timedelta(hours=h)).strftime("%Y-%m-%d %H:%M")


def main():
    a = dt.date.fromisoformat(sys.argv[1]); b = dt.date.fromisoformat(sys.argv[2])
    events = []
    for name, pid in BODIES:
        step = 0.25
        t = jd(a)
        prev = swe.calc_ut(t, pid, swe.FLG_SPEED)[0]
        while t < jd(b):
            t2 = t + step
            cur = swe.calc_ut(t2, pid, swe.FLG_SPEED)[0]
            if int(prev[0] // 30) != int(cur[0] // 30):
                lo, hi = t, t2
                for _ in range(40):
                    mid = (lo + hi) / 2
                    if int(swe.calc_ut(mid, pid)[0][0] // 30) == int(prev[0] // 30):
                        lo = mid
                    else:
                        hi = mid
                s = int(cur[0] // 30)
                direction = " (Rx)" if cur[3] < 0 else ""
                events.append((hi, f"{name} enters {SIGNS[s]}{direction}"))
            if name != "North Node" and (prev[3] > 0) != (cur[3] > 0):
                lo, hi = t, t2
                for _ in range(40):
                    mid = (lo + hi) / 2
                    if (swe.calc_ut(mid, pid, swe.FLG_SPEED)[0][3] > 0) == (prev[3] > 0):
                        lo = mid
                    else:
                        hi = mid
                p = swe.calc_ut(hi, pid)[0][0]
                kind = "stations Retrograde" if prev[3] > 0 else "stations Direct"
                events.append((hi, f"{name} {kind} at {p % 30:.1f}° {SIGNS[int(p // 30)]}"))
            t, prev = t2, cur
    # Eclipses
    t = jd(a)
    while True:
        r = swe.sol_eclipse_when_glob(t)[1][0]
        if r > jd(b):
            break
        s = swe.calc_ut(r, swe.SUN)[0][0]
        events.append((r, f"Solar eclipse at {s % 30:.1f}° {SIGNS[int(s // 30)]}"))
        t = r + 10
    t = jd(a)
    while True:
        r = swe.lun_eclipse_when(t)[1][0]
        if r > jd(b):
            break
        m = swe.calc_ut(r, swe.MOON)[0][0]
        events.append((r, f"Lunar eclipse at {m % 30:.1f}° {SIGNS[int(m // 30)]}"))
        t = r + 10
    for j, e in sorted(events):
        print(f"{show(j)} UTC  {e}")


if __name__ == "__main__":
    main()
