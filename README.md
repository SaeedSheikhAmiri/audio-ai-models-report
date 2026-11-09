<div dir="rtl" align="right">

# نقشهٔ جامع مدل‌های صوتی هوش مصنوعی

گزارش پژوهشی دربارهٔ مدل‌های صوتی هوش مصنوعی: از تبدیل متن به گفتار (TTS) و تشخیص گفتار (ASR) تا تولید موسیقی، افکت صدا، سنتز آواز، درک صدا و پردازش سیگنال.

**نسخهٔ وب:** <https://saeedsheikhamiri.github.io/audio-ai-models-report/>

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

- [`index.html`](index.html) — نسخهٔ وب (GitHub Pages)
- [`report.pdf`](report.pdf) — نسخهٔ PDF (۳۴ صفحه)
- [`report.md`](report.md) — متن خام
- [`build.py`](build.py) — تبدیل‌کنندهٔ Markdown به HTML راست‌به‌چپ

## بازسازی خروجی

```bash
python3 build.py report.md report.html
cp report.html index.html
```

## هشدار

قیمت‌ها و نسخه‌ها در این حوزه ماهانه تغییر می‌کنند. اعداد این گزارش تقریبی‌اند و پیش از بودجه‌بندی باید از صفحهٔ رسمی قیمت هر سرویس تأیید شوند. این فهرست «نمایندهٔ کامل بازیگران مهم» است، نه فهرست حداکثری همهٔ مدل‌ها.

</div>
