<div dir="rtl" align="right">

# نقشهٔ جامع مدل‌های صوتی هوش مصنوعی

### The Complete Map of AI Audio Models

**سعید شیخ‌امیری** · نوامبر ۲۰۲۶ · نسخهٔ ۱.۰

---

گزارشی دربارهٔ مدل‌های صوتی هوش مصنوعی: از تبدیل متن به گفتار (TTS) و تشخیص گفتار (ASR) تا تولید موسیقی، افکت صدا، سنتز آواز، درک صدا و پردازش سیگنال. هشت دستهٔ کارکردی، بیش از ۲۰۰ مدل و سرویس، همراه با قیمت، مجوز، سخت‌افزار لازم، بنچمارک و وضعیت زبان فارسی.

**نسخهٔ وب فارسی:** <https://saeedsheikhamiri.github.io/audio-ai-models-report/>
**English edition:** <https://saeedsheikhamiri.github.io/audio-ai-models-report/en.html>

## در این گزارش چه هست؟

| # | دسته | نمونه مدل‌ها |
|---|------|--------------|
| ۱ | تبدیل متن به گفتار (TTS) | ElevenLabs v3، Cartesia Sonic-3، Kokoro، Chatterbox، CosyVoice |
| ۲ | تشخیص گفتار (ASR) | Whisper، Deepgram Nova-3، AssemblyAI، Parakeet، Canary |
| ۳ | تبدیل صدا و کلونینگ | RVC، Seed-VC، OpenVoice، GPT-SoVITS |
| ۴ | تولید موسیقی | Suno v5، Udio، ACE-Step، Stable Audio، MusicGen |
| ۵ | افکت صدا و Foley | ElevenLabs SFX، MMAudio، HunyuanVideo-Foley، TangoFlux |
| ۶ | سنتز آواز | Synthesizer V، Vocaloid، DiffSinger |
| ۷ | درک و تحلیل صدا | GPT-4o/5 audio، Gemini، Qwen3-Omni، Kimi-Audio |
| ۸ | پردازش و بهبود صدا | Demucs، BS-RoFormer، DeepFilterNet، AudioSR |

علاوه بر فهرست مدل‌ها: تحلیل هزینه بر واحد کار و TCO سلف‌هاست، جدول مجوزها (Apache/MIT/CC-BY-NC/Community)، راهنمای انتخاب بر اساس سناریو، وضعیت خاص زبان فارسی، بنچمارک‌ها و ریسک‌های حقوقی.

## فایل‌ها

| فایل | توضیح |
|------|-------|
| [`index.html`](index.html) | نسخهٔ وب فارسی (GitHub Pages) |
| [`en.html`](en.html) | English edition |
| [`report-fa.pdf`](report-fa.pdf) | PDF فارسی (۳۴ صفحه) |
| [`report-en.pdf`](report-en.pdf) | PDF انگلیسی (۳۶ صفحه) |
| [`report.md`](report.md) | متن خام فارسی |
| [`report-en.md`](report-en.md) | متن خام انگلیسی |
| [`build.py`](build.py) | تبدیل‌کنندهٔ Markdown به HTML (دو‌زبانه) |

## بازسازی خروجی

```bash
python3 build.py report.md index.html fa
python3 build.py report-en.md en.html en
```

## هشدار

قیمت‌ها و نسخه‌ها در این حوزه ماهانه تغییر می‌کنند. اعداد این گزارش تقریبی‌اند و پیش از بودجه‌بندی باید از صفحهٔ رسمی قیمت هر سرویس تأیید شوند. این فهرست «نمایندهٔ کامل بازیگران مهم» است، نه فهرست حداکثری همهٔ مدل‌ها.

</div>

---

<details>
<summary><b>English</b></summary>

### The Complete Map of AI Audio Models

**Saeed Sheikh Amiri** · November 2026 · v1.0

A structured survey of AI audio models across eight functional categories: TTS, ASR, voice conversion, music generation, sound effects, singing synthesis, audio understanding, and audio processing. Includes pricing, licensing, hardware requirements, benchmarks, and a dedicated section on Persian-language support.

- **Web (Persian):** `index.html`
- **Web (English):** `en.html`
- **PDF:** `report-fa.pdf`, `report-en.pdf`
- **Source:** `report.md`, `report-en.md`

Rebuild:

```bash
python3 build.py report.md index.html fa
python3 build.py report-en.md en.html en
```

</details>
