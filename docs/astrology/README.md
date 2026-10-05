# مرجع استرولوژی (فارسی)

مرجع جامع استرولوژی سنتی، مدرن و ودیک + ابزار محاسبهٔ دقیق با Swiss Ephemeris.

| فایل | موضوع |
|---|---|
| [01-foundations.md](01-foundations.md) | زودیاک‌ها، ۱۲ نشانه، سیارات و چرخه‌ها، خانه‌ها و نظام‌ها، جنبه‌ها و اُرب، سهم‌ها، ستارگان ثابت |
| [02-dignities.md](02-dignities.md) | دیگنیتی ذاتی (بیت، شرف، مثلثه، حدود، وجوه) و عرضی، فرقه، آلمتن، هیلاج/کدخدا، سال‌های سیارات |
| [03-natal-chart-and-house-rulers.md](03-natal-chart-and-house-rulers.md) | روش خوانش چارت تولد، منطق حاکمان خانه، جدول کامل ۱۲×۱۲ |
| [04-profection-lord-of-year.md](04-profection-lord-of-year.md) | پروفکشن سالانه/ماهانه، ارباب سال |
| [05-solar-return.md](05-solar-return.md) | سولار ریترن، طالع سال در ۱۲ نشانه و در ۱۲ خانهٔ چارت تولد، تلفیق با پروفکشن، ریترن‌های دیگر |
| [06-transits.md](06-transits.md) | ترانزیت‌ها، چرخه‌های عمر، آسمان ۲۰۲۶–۲۰۲۷، پروگرشن و جهت‌ها |
| [07-firdaria.md](07-firdaria.md) | فرداریا (روز/شب، زیردوره‌ها، تفسیر) |
| [08-vedic-dasha.md](08-vedic-dasha.md) | جیوتیش، ناکشاتراها، ویمشوتاری و داشاهای دیگر، مقایسهٔ ارباب‌های زمان |
| [09-branches-and-other-techniques.md](09-branches-and-other-techniques.md) | سنت‌ها و شاخه‌ها (هوراری، انتخاباتی، جهانی، سیناستری…)، زودیاکال ریلیزینگ، تکنیک‌های ایرانی |
| [10-annual-forecast-workflow.md](10-annual-forecast-workflow.md) | روش‌کار تلفیقی پیش‌بینی سالانه + چک‌لیست |
| [appendix-sky-2026-2027.md](appendix-sky-2026-2027.md) | ورودها، رجعت‌ها و کسوف/خسوف‌ها ۲۰۲۶–۲۰۲۷ |

## ابزار محاسبه
```bash
pip install pyswisseph
B="--date 1995-06-21 --time 14:30 --tz 4.5 --lat 35.6892 --lon 51.3890"   # داده‌های تولد
python3 tools/astro.py natal      $B
python3 tools/astro.py profection $B --on 2026-10-04
python3 tools/astro.py sr         $B --year 2026 --sr-lat 35.69 --sr-lon 51.39 --sr-tz 3.5
python3 tools/astro.py transit    $B --on 2026-10-04 --orb 2
python3 tools/astro.py firdaria   $B            # --alt-night برای نسخهٔ دوم شبانه
python3 tools/astro.py dasha      $B            # ویمشوتاری، آیانامشای لاهیری
python3 tools/sky_events.py 2026-01-01 2028-01-01
```
- ورودی تاریخ میلادی است. `--tz` = اختلاف با UTC در همان لحظه (ایران ۳.۵؛ تابستان تا ۱۴۰۱: ۴.۵).
- خانه‌ها: Whole Sign (WS) و Placidus هر دو نمایش داده می‌شوند. گره = True Node.
- دیگنیتی‌ها با امتیاز لیلی، مثلثهٔ دوروتئوس، حدود مصری، وجوه کلدانی.
