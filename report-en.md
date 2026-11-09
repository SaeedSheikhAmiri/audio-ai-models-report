# The Complete Map of AI Audio Models

### Categories, Models, Capabilities, Costs, and Licensing

**Saeed Sheikh Amiri** · November 2026 · v1.0

---

## Before you read

I wrote this report because the audio AI market has become almost impossible to navigate from the outside. Vendor pages compare their own best model to everyone else's worst, benchmark tables measure English read speech and call it "multilingual," and license terms are buried three clicks away from the download button. What follows is my attempt to put the whole field on one page: eight functional categories, the models that matter in each, what they actually cost, and where the legal tripwires are.

A few notes on method. The comparison is organized by *function* rather than architecture, because that is how build-versus-buy decisions actually get made. Prices are list prices as of November 2026, converted to US dollars, and they move constantly — treat every number here as a starting point for a quote, not as a quote. Where I could verify a figure against a vendor page I did; where I could not, the number is an estimate and should be checked before it goes into a budget. Model versions churn monthly, so a name in this report may already have a successor by the time you read it.

I have tried to be honest about the parts that are genuinely uncertain: latency figures depend on region and payload, WER depends on domain, and "supports 99 languages" usually means "supports 99 languages badly, except English." Where the data is thin, I say so.

---

## 1. The short version

1. There are **eight functional categories**: text-to-speech (TTS), speech-to-text (ASR), voice conversion and cloning, music generation, sound-effect generation, singing synthesis, audio understanding, and audio processing/restoration.
2. The real dividing line is **cloud versus open weights**. Cloud gives you quality, uptime, and someone else's on-call rotation; open weights give you control and a fixed GPU bill, at the cost of maintenance and uneven quality.
3. TTS has stratified into three tiers: high-expression models (ElevenLabs v3, Hume Octave), low-latency agent models (Cartesia Sonic, Deepgram Aura-2, ElevenLabs Flash), and small open models (Kokoro, Piper, Chatterbox, CosyVoice).
4. Whisper remains the default "good and cheap" ASR. On English accuracy it has been overtaken by Parakeet/Canary, Nova-3, and AssemblyAI — but for Persian, Whisper plus Azure or Google is still the realistic stack.
5. Music splits into consumer products (Suno, Udio, Riffusion) and open models (ACE-Step, Stable Audio Open, MusicGen, YuE). Full-song vocals remain a commercial advantage.
6. Sound effects grew fastest: text-to-SFX is now routine, and video-to-Foley (MMAudio, HunyuanVideo-Foley) is close behind.
7. Audio understanding has moved to "Omni" models — GPT-4o/5 audio, Gemini, Qwen3-Omni, Kimi-Audio. These are no longer transcription tools; they are voice assistants with ears.
8. Cost should be measured per unit of work: TTS per million characters, ASR per minute, music per generation, self-hosting per GPU-hour. Rule of thumb: below roughly 500 hours of audio per month, APIs win; above it, dedicated GPUs do.
9. Licensing is the main trap in open weights: CC-BY-NC, community licenses, and "open code, closed weights." Always check the license on the *weights*, not the GitHub repo.
10. Legal risk is the most serious issue in the field: voice cloning without consent, and ownership of generated music. For a commercial product, the safe path is a model with an explicit commercial license plus a supplier contract.

---

## 2. The map

| # | Category | Input → output | What success means | Typical use |
|---|----------|----------------|--------------------|-------------|
| 1 | **TTS** | text → speech | naturalness, expression, latency, cloning | audiobooks, assistants, ads |
| 2 | **ASR** | speech → text | WER, diarization, streaming, language coverage | subtitles, calls, analytics |
| 3 | **Voice conversion** | audio + target → new voice | timbre similarity, content preservation, real-time | dubbing, games, creator tools |
| 4 | **Music generation** | text/melody → music | musicality, structure, vocals | songs, background, games |
| 5 | **Sound effects / Foley** | text/video → audio | sync with picture, realism | film, games, podcasts |
| 6 | **Singing synthesis** | lyrics + melody → singing | pronunciation, vibrato, emotion | song production, demos |
| 7 | **Audio understanding** | audio → meaning | reasoning, tagging, answering | voice assistants, monitoring |
| 8 | **Processing / restoration** | audio → audio | SNR, separation, naturalness | cleanup, stems, mastering |

Two secondary axes are useful. By **signal domain**: speech, music, and general/environmental sound. By **model direction**: generative (TTS, music, SFX) versus analytical (ASR, tagging, speaker recognition). Omni models do both.

---

## 3. How I compared them

Every model was assessed against the same twelve criteria, so the tables are at least internally consistent.

| Criterion | What it measures | Why it matters |
|-----------|------------------|----------------|
| **Perceptual quality** | MOS or arena ranking (TTS Arena, Artificial Analysis) | closest proxy for "does it sound real" |
| **Accuracy (ASR)** | WER on clean, noisy, and accented sets | the main purchase decision |
| **Latency** | time to first audio, or real-time factor | decides whether an agent feels alive |
| **Language coverage** | number of languages, and quality per language | Persian and multilingual work |
| **Cloning** | zero-shot, few-shot, fine-tune | personalization |
| **Control** | emotion, speed, prosody, pronunciation, audio tags | production quality |
| **Output length** | seconds or minutes per request | audiobooks, podcasts |
| **Streaming** | WebSocket / real-time support | telephony and agents |
| **Hardware** | CPU/GPU, memory, RTF | self-host cost |
| **License** | Apache/MIT/CC-BY-NC/community/proprietary | commercial use |
| **Price** | per character, minute, or generation | budget |
| **Maturity** | docs, SDKs, SLA, stability | operational risk |

---

## 4. Text-to-speech

### 4.1 The state of the market

Three generations of TTS are running in production at the same time:

- **Generation 1 (concatenative and parametric):** Tacotron, FastSpeech, VITS. Fast, small, medium quality, still common in embedded products and low-resource languages.
- **Generation 2 (diffusion and LLM-based):** XTTS, F5-TTS, CosyVoice, Chatterbox, Orpheus, Dia. Zero-shot cloning and high expressiveness.
- **Generation 3 (full duplex):** CSM, Moshi, GPT-4o audio, Gemini. TTS as one component of a conversational model that understands context.

### 4.2 Commercial services

| Model / service | What stands out | Latency | Languages | Cloning | Approx. price | Best for |
|---|---|---|---|---|---|---|
| **ElevenLabs v3** | Most expressive model on the market; emotion tags (`[whispers]`, `[laughs]`); 70+ languages | 0.5–1 s (non-streaming) | 70+ | Instant (1 min sample) + professional | $0.06–0.24 per 1k chars; plans $5–$1,320/mo | Audiobooks, ads, emotive dubbing |
| **ElevenLabs Flash v2.5** | Same engine, tuned for speed | ~75 ms | 32+ | Limited | Cheaper than v3 | Voice agents, IVR |
| **ElevenLabs Turbo v2.5** | Speed/quality balance | ~250–300 ms | 32+ | Yes | Mid | Voice chatbots |
| **OpenAI gpt-4o-mini-tts** | Instruction-following ("calm, serious tone"); native to the API | ~0.5 s | ~50 (variable quality) | No | ~$0.015/min of audio | OpenAI-centric products |
| **OpenAI tts-1 / tts-1-hd** | Simple, stable, 13 voices | Fast | ~50 | No | $15 / $30 per 1M chars | MVPs and prototypes |
| **Google Chirp 3 HD** | Natural voices, broad coverage, GCP | ~0.3 s | 50+ | Custom Voice (enterprise) | ~$30 per 1M chars | GCP shops |
| **Google Gemini TTS** | Natural-language control, multi-speaker | Medium | 24+ | No | Audio-token based (preview) | Conversational experiences |
| **Azure Neural TTS** | Official fa-IR support; full SSML; streaming | ~0.2 s | 140+ | Custom Neural Voice | ~$15 per 1M (HD: $30) | Enterprise Persian |
| **Amazon Polly** | Cheap, stable, generative voices | ~0.3 s | 40+ | Brand Voice | $4 standard / $16 neural / $30 generative | Cheap AWS scale |
| **Cartesia Sonic-3** | Very fast, very cheap for conversation; good quality | ~40 ms | 40+ | Instant clone | ~$20–40 per 1M chars | Phone agents |
| **Deepgram Aura-2** | Built for agents; low latency; SLA | ~200 ms | English-first | No | ~$30 per 1M chars | Calls, support |
| **Hume Octave** | Emotional "acting" controlled by description | Medium | 10+ | Yes | Per character, above average | Performance-driven content |
| **PlayHT Play 3.0** | Fast cloning, good language coverage | ~0.3 s | 30+ | Yes | From ~$39/mo; API per char | Podcasts, video |
| **LMNT** | Extremely fast, minimal | ~50 ms | 10+ | Yes | ~$0.03 per 1k chars | Low-latency streaming |
| **Rime** | Character-driven, conversational voices | ~0.2 s | 10+ | Yes | Per character | Games, personas |
| **MiniMax Speech-2.6** | High quality at aggressive prices; 40+ languages | Medium | 40+ | Yes | Low, competitive with ElevenLabs | Price-sensitive buyers |
| **Fish Audio S1** | Fast cloning, low price, open ecosystem | Medium | 13+ | Yes | ~$15 per 1M chars | Content creators |
| **Speechify / Murf / WellSaid / Resemble** | Product-first (studio, teams, brand voice) | Medium | 20–50 | Yes | $20–100/mo subscriptions | Content teams |

> **A note on price.** Measure TTS by the cost of one hour of audio, not by the headline per-character rate. One hour of speech is roughly 90,000 characters. So $15 per 1M characters is about **$1.35 per audio hour**; $30 per 1M is **$2.70**; ElevenLabs on a low-tier plan can reach **$10–20 per hour**.

### 4.3 Open-weight models

| Model | Params | Languages | Cloning | License | Hardware | Strength | Weakness |
|---|---|---|---|---|---|---|---|
| **Kokoro-82M** | 82M | 8 (en, ja, zh, es, fr, hi, it, pt) | No (voicepacks) | Apache 2.0 | Runs on CPU | Unbeatable quality per cost; very fast | No cloning; limited languages |
| **Piper** | 10–60M | 30+ (incl. fa_IR) | No | MIT | Raspberry Pi | Light, offline, multilingual | Robotic |
| **XTTS-v2** (Coqui) | ~467M | 17 | 6-second sample | CPML (non-commercial) | 4–6 GB VRAM | Mature multilingual cloning | Non-commercial; no Persian |
| **F5-TTS** | ~336M | en, zh (+finetunes) | Zero-shot | Code MIT / weights CC-BY-NC | 6–8 GB | High quality, trainable | Non-commercial weights; few languages |
| **Chatterbox** (Resemble) | 0.5B | en + 23 (multilingual release) | Yes | MIT | 6–8 GB | Adjustable emotion, Perth watermark | Uneven across languages |
| **Dia-1.6B** (Nari) | 1.6B | en | Yes | Apache 2.0 | 10 GB+ | Multi-speaker dialogue, laughs | English only; slow |
| **Orpheus-3B** (Canopy) | 3B | en + language variants | Yes | Apache 2.0 | 12 GB+ | Emotion tags, ~200 ms streaming | Heavy |
| **Sesame CSM-1B** | 1B | en | Yes | Apache 2.0 | 8 GB | Conversational context, natural | English; limited control |
| **VibeVoice** (Microsoft) | 1.5B / 7B | en, zh | Yes | MIT | 8–16 GB | Up to 4 speakers, up to 90 min | Limited languages |
| **Higgs Audio v2** (Boson) | 3B | multilingual | Yes | Apache (code) / open weights | 12 GB+ | High quality, music and singing | Resource-hungry |
| **IndexTTS-2** (Bilibili) | ~1B | zh, en | Zero-shot | Apache 2.0 | 8 GB | Emotion and duration control | Few languages |
| **CosyVoice 2/3** (Alibaba) | 0.5B | zh, en, ja, ko + dialects | Yes | Apache 2.0 | 4–6 GB | ~150 ms streaming, production quality | No Persian |
| **Fish Speech / OpenAudio** | ~0.5B | 13 | Yes | Code Apache / weights CC-BY-NC-SA | 6 GB | Multilingual, fast cloning | Non-commercial weights |
| **MegaTTS3** | 0.45B | zh, en | Yes | Apache 2.0 | 6 GB | Good cloning, light | Two languages |
| **Zonos** (Zyphra) | 1.6B | en + 7 | Yes | Apache 2.0 | 8 GB | Emotion control, good timbre | No Persian |
| **Bark** (Suno) | ~1B | 13+ | Yes | MIT | 6 GB | Non-verbal sounds, music | Unstable, slow, hallucinates |
| **Parler-TTS** | 0.9B | en | No | Apache 2.0 | 6 GB | Text-described voice control | English, average quality |
| **Spark-TTS** | 0.5B | zh, en | Yes | Apache 2.0 (code) | 4 GB | Light, controllable | Few languages |
| **MOSS-TTSD / FireRedTTS-2** | 1–3B | zh, en | Yes | Apache 2.0 | 8–12 GB | Long dialogue, podcasts | Few languages |

**Bottom line on TTS.** Best absolute quality: ElevenLabs v3, Hume Octave, MiniMax in commercial; Higgs Audio v2, IndexTTS-2, Chatterbox in open. Best quality per dollar in open: Kokoro (no cloning) and CosyVoice (with cloning). Best for real-time agents: Cartesia, Deepgram Aura-2, ElevenLabs Flash; on the open side, CosyVoice-2 and Orpheus. Best for Persian: Azure Neural/Custom Neural, Google Chirp 3, ElevenLabs (test it), Polly; open options are Piper fa_IR and community VITS/Coqui models trained on ManaTTS.

---

## 5. Speech-to-text

### 5.1 Commercial

| Service / model | Approx. price | WER (clean English) | Streaming | Diarization | Languages | Notes |
|---|---|---|---|---|---|---|
| **OpenAI whisper-1** | $0.006/min | ~8–12% | No | No | 99 | Cheap, simple, few features |
| **OpenAI gpt-4o-transcribe** | ~$0.006/min | ~5–8% | Limited | No | 50+ | Noise-robust, summarizes |
| **OpenAI gpt-4o-mini-transcribe** | ~$0.003/min | ~7–10% | Limited | No | 50+ | Cheapest OpenAI option |
| **Deepgram Nova-3** | ~$0.0043–0.0077/min | ~5–7% | Yes (strong) | Yes | 30+ | The agent/call-center default |
| **AssemblyAI Universal-3** | ~$0.0025–0.0045/min | ~5–7% | Yes | Yes | 99 | Conversation analytics |
| **Speechmatics** | ~$0.0017–0.0036/min | ~6–8% | Yes | Yes | 50+ | Strong on accents; EU-friendly |
| **Soniox** | ~$0.001–0.002/min | ~6–9% | Yes | Yes | 60+ | Cheap streaming |
| **Gladia** | ~$0.0025/min | ~7–9% | Yes | Yes | 100 | Simple, EU |
| **Rev AI** | $0.02/min (AI) | ~6–8% | No | Yes | 30+ | Quality plus human services |
| **Google Chirp 3** | ~$0.016/min | ~6–9% | Yes | Yes | 125 | GCP integration |
| **Azure Speech** | ~$0.017/min (real-time) | ~6–9% | Yes | Yes | 100+ | Official Persian, SSML |
| **Amazon Transcribe** | ~$0.024/min | ~7–10% | Yes | Yes | 100 | AWS, tiered |
| **ElevenLabs Scribe v2** | ~$0.0067/min | ~4–6% | No | Yes | 99 | High accuracy, cleanup |
| **Mistral Voxtral** | ~$0.003–0.006/min | ~6–8% | No | No | 8 | Cheap, EU |

### 5.2 Open weights

| Model | Params | License | English WER | Languages | Speed | Notes |
|---|---|---|---|---|---|---|
| **Whisper large-v3** | 1.5B | MIT | ~7–9% | 99 | Medium | The open standard; robust |
| **Whisper large-v3-turbo** | 809M | MIT | ~8–10% | 99 | ~8× faster | Best trade-off |
| **distil-whisper large-v3.5** | 756M | MIT | ~9–11% | en | 6× faster | English |
| **NVIDIA Parakeet-TDT-0.6B v3** | 0.6B | CC-BY-4.0 | ~5–6% | 25 (European) | Very fast | Tops the Open ASR leaderboard |
| **NVIDIA Canary-Qwen-2.5B** | 2.5B | CC-BY-4.0 | ~5.6% | en | Medium | Accuracy plus LLM |
| **NVIDIA Canary-1B-v2** | 1B | CC-BY-4.0 | ~6–7% | 25 | Fast | Also does speech translation |
| **Kyutai STT** | 1B / 2.6B | CC-BY-4.0 | ~6–8% | en, fr | Streaming | Real-time |
| **Moonshine** | 27–61M | MIT | ~9–12% | en | Very fast | Edge devices |
| **Vosk** | 50–500M | Apache 2.0 | ~10–15% | 20+ (incl. fa) | CPU | Small, offline |
| **MMS / Wav2Vec2** | 300M | MIT | Variable | 1100+ (incl. fa) | Medium | Unmatched language coverage |
| **SenseVoice** | ~234M | Apache 2.0 | ~7–9% | zh, en, ja, ko | Very fast | Emotion and audio events |
| **Qwen3-ASR** | 1.7B–8B | Apache 2.0 | ~5–7% | 52 | Medium | High accuracy, LLM-based |
| **Step-Audio 2 mini ASR** | ~8B | Apache 2.0 | ~5–7% | 30+ | Slow | Part of an Omni model |

**Bottom line on ASR.** Best accuracy: Nova-3, Universal-3, Scribe v2, Canary-Qwen-2.5B. Cheapest cloud: Soniox, Gladia, Speechmatics batch. Best open self-host: Whisper large-v3-turbo for breadth, Parakeet for speed on European languages, Canary for accuracy. Persian: Whisper large-v3 (WER ~10–15% depending on domain), Azure fa-IR, Google fa-IR, Speechmatics, Vosk fa for lightweight use, and NVIDIA NeMo Persian if you have training data.

---

## 6. Voice conversion and cloning

| Model / service | Type | License / price | Timbre similarity | Real-time | Notes |
|---|---|---|---|---|---|
| **RVC** | Open weights | MIT | High (with 10–30 min of data) | Yes (~90 ms) | The community workhorse; easy to train |
| **so-vits-svc** | Open weights | AGPL | High | Near | Popular for singing |
| **OpenVoice v2** (MyShell) | Open weights | MIT | Medium | Yes | Tone-color cloning, lightweight |
| **Seed-VC** | Open weights | Apache 2.0 | High | Yes | Zero-shot, speech and singing |
| **GPT-SoVITS** | Open weights | MIT | High | No | Strong quality from ~1 min of data |
| **Chatterbox VC** | Open weights | MIT | High | No | Same family as the TTS model |
| **ElevenLabs Voice Changer** | Cloud | Subscription | High | Yes | Simple, good quality |
| **Respeecher** | Cloud / studio | Enterprise (expensive) | Very high | No | Film and TV, with voice rights |
| **Altered Studio** | Cloud | Subscription | High | Yes | Dubbing and games |
| **Voice.ai / Kits VC** | Cloud / desktop | Freemium | Medium–high | Yes | Consumer |

**What matters here.** Cloning is a legal risk, not just a technical one. Under the EU AI Act and several US state laws, disclosing synthetic voice and obtaining consent from the voice owner is mandatory in many contexts. Take watermarking (e.g., Perth in Chatterbox) and consent logging seriously. RVC is the best cost/quality route to a custom voice; Seed-VC is the zero-shot option. For singing, RVC and so-vits-svc remain the community standard, while full-song generation is easier through Suno or ACE-Step.

---

## 7. Music generation

### 7.1 Commercial and consumer

| Service | Version | What it does | Approx. price | Output ownership |
|---|---|---|---|---|
| **Suno** | v5 | Full songs with vocals, many styles, section editing | Free (50 credits/day, non-commercial); Pro ~$10/mo; Premier ~$30/mo | Commercial on paid plans (with terms) |
| **Udio** | v2/v3 | High audio quality, style control | ~$10–30/mo | Commercial on paid plans; after deals with publishers |
| **Riffusion** | FUZZ | Free/freemium, fast generation | Free + paid tiers | Varies |
| **Stable Audio 2.5** (Stability) | 2.5 | Up to ~3-minute generations, loops, audio-to-audio | API credits | Commercial under license |
| **Google Lyria 2/3** | Vertex/Gemini | High-fidelity music, pro tools | Per minute/token | Commercial |
| **MiniMax Music 2** | — | Full songs, cheap | Cheap API | Commercial |
| **Mureka** | V8 | Full songs with vocals | Subscription | Commercial |
| **ElevenLabs Music** | — | Licensed-data music, commercial focus | Subscription | Commercial (fully licensed claim) |
| **Adobe Firefly Soundtrack** | — | Copyright-safe | Creative Cloud credits | Commercial |
| **Soundraw / Beatoven / AIVA / Boomy** | — | Royalty-free music for video | $10–30/mo | Commercial |

### 7.2 Open weights

| Model | Params | License | Length | Vocals | Notes |
|---|---|---|---|---|---|
| **ACE-Step** | 3.5B | Apache 2.0 | up to ~4 min | Yes (19 languages) | The most complete open option for full songs |
| **Stable Audio Open 2.0** | ~1B | Stability Community (commercial under $1M revenue) | ~47 s | No | Loops and effects, high quality |
| **MusicGen** (Meta) | 300M–3.3B | Code MIT / weights CC-BY-NC | 30 s | No | Research reference; melody/style |
| **YuE** | ~7B | Code Apache / weights CC-BY-NC | several minutes | Yes | Full songs with vocals |
| **DiffRhythm** | ~1B | Apache 2.0 | up to ~4 min | Yes | Very fast (seconds) |
| **Tango 2** | ~1B | CC-BY-NC | 30 s | No | Strong SFX/music quality |
| **AudioLDM 2** | ~1B | CC-BY-NC | 10 s | No | General audio |
| **MAGNeT** | 300M–1.5B | CC-BY-NC | 30 s | No | Fast, non-autoregressive |

**Bottom line on music.** For release-ready songs, Suno and Udio. For legally safe commercial background music, Firefly, Stable, or ElevenLabs Music. For local deployment and control, ACE-Step (best open) and DiffRhythm (fastest).

---

## 8. Sound effects and Foley

| Model / service | Input | License / price | Notes |
|---|---|---|---|
| **ElevenLabs SFX v2** | text | Subscription/credits | High quality, sound library, video sync |
| **Stable Audio Open / 2.5 API** | text | Community / credits | Effects and loops |
| **Meta AudioGen** | text | CC-BY-NC | Research reference |
| **TangoFlux** | text | Apache 2.0 | 515M, fast, good quality |
| **Woosh** | text | Apache 2.0 | Lightweight, effects-focused |
| **MMAudio** | video (+text) | MIT | Automatic Foley for video |
| **HunyuanVideo-Foley** (Tencent) | video | Open (research) | Tight picture sync |
| **AudioX** | video/text | Open | Audio from video |
| **Kling / Runway / Pika Foley** | video | Subscription | Inside video tools |
| **Mirelo SFX** | video | API | Professional Foley |

**What matters here.** For video, the metric is temporal sync, not just audio quality. Video-to-audio models (MMAudio, HunyuanVideo-Foley) beat text-to-audio on that metric.

---

## 9. Singing synthesis

| Option | Type | Price / license | Quality | Notes |
|---|---|---|---|---|
| **Synthesizer V Studio** (Dreamtonics) | Commercial software | ~$89 + voicebanks $50–100 | Best in class | Full phonetic and vibrato control |
| **Vocaloid 6 / CeVIO / Piapro** | Commercial | $100–300 | High | Large legacy ecosystem |
| **Suno / Udio** | Cloud | Subscription | High (generated vocals) | Limited fine control |
| **Kits.AI / Voicify / Jammable** | Cloud | Subscription | Medium–high | Voice cloning on singing |
| **DiffSinger** | Open | Apache 2.0 | Medium–high | Needs data/training |
| **ACE-Step / DiffRhythm / YuE** | Open | Apache/NC | Medium | Full vocals inside songs |
| **RVC / so-vits-svc / Seed-VC** | Open | MIT/AGPL | High (conversion) | Convert an existing vocal to a target voice |

**What matters here.** Singing from scratch (lyrics + notes) and voice conversion (a real singer → another timbre) are different problems. For studio-grade results Synthesizer V still wins; for speed and cost, Suno.

---

## 10. Audio understanding (Audio LLMs)

| Model | License | Capability | Notes |
|---|---|---|---|
| **GPT-4o / GPT-5 audio** (OpenAI) | API | Listening, reasoning, spoken replies, Realtime | The most expensive and the strongest in conversation |
| **Gemini 2.5 / 3** (Google) | API | Audio + video + text, long context | Deep Gemini integration |
| **Qwen3-Omni** (Alibaba) | Apache 2.0 | Audio/image/text, 30B-A3B MoE | The best open Omni model |
| **Qwen2.5-Omni** | Apache 2.0 | Real-time conversation | Lighter |
| **Kimi-Audio** (Moonshot) | MIT-ish | Understanding + generation, 13M hours of data | Strong benchmark scores |
| **Step-Audio 2 mini** | Apache 2.0 | ASR + TTS + audio reasoning | Strong in Chinese and English |
| **Moshi** (Kyutai) | CC-BY 4.0 | Full-duplex conversation (~200 ms) | Feels genuinely conversational |
| **SALMONN / Audio Flamingo 3** | Research | General audio and music understanding | Non-commercial |
| **GLM-4-Voice / MiniCPM-o** | Apache 2.0 | Lightweight conversation | Edge and mobile |

**Where these get used:** voice assistants, call analytics, factory monitoring, music description, accessibility. The benchmarks that matter are MMAU, AudioBench, and LongAudioBench.

---

## 11. Processing, separation, and restoration

| Tool / model | Task | License | Notes |
|---|---|---|---|
| **Demucs v4 (htdemucs)** | 4/6-stem separation | MIT | Open standard; good quality |
| **BS-RoFormer / Mel-Band RoFormer** | Stem separation | MIT-ish | Best separation quality |
| **MDX23C / UVR5** | Separation + GUI | GPL/MIT | Community favorite |
| **LavaSR** | Bandwidth/quality extension | Apache 2.0 | Audio reconstruction |
| **AudioSR** | Audio super-resolution | MIT | 44.1/48 kHz |
| **Apollo** | Restoration of degraded audio | Open | Loss restoration |
| **DeepFilterNet3** | Real-time noise suppression | MIT | Light, built for calls |
| **RNNoise** | Noise suppression | BSD | Ultra-light |
| **Resemble Enhance** | Speech enhancement | MIT/Apache | Denoise + enhance |
| **Adobe Podcast Enhance** | Speech enhancement | Free (web) | Good quality, limited |
| **Auphonic / iZotope RX** | Mastering/restoration | Subscription/license | Professional standard |
| **Krisp** | Noise/echo removal | Subscription | SDK for calls |

---

## 12. The cost question

### 12.1 Cost per unit of work (approximate, November 2026)

| Work | Unit | Cloud range | Equivalent per hour |
|---|---|---|---|
| Cheap TTS (Polly/Azure/OpenAI tts-1) | 1M chars | $4–16 | **$0.40–1.50** |
| Mid-tier TTS (Cartesia/Deepgram/Fish) | 1M chars | $15–30 | **$1.40–2.70** |
| Premium TTS (ElevenLabs/Hume) | 1M chars | $60–240 | **$5–22** |
| Cheap ASR (Soniox/Gladia/Speechmatics batch) | minute | $0.001–0.002 | **$0.06–0.12** |
| Mid-tier ASR (Deepgram/AssemblyAI) | minute | $0.0025–0.005 | **$0.15–0.30** |
| Premium ASR (Google/Azure/Rev) | minute | $0.016–0.02 | **$0.96–1.20** |
| Music (Suno/Udio) | track | — | $10–30/mo subscription |
| Music API (Stable/Lyria) | minute | $0.02–0.1 | **$1.20–6** |
| Sound effects | generation | $0.01–0.1 | varies |

One hour of speech is about 90,000 characters; one hour of audio is 60 minutes. Do not mix the two.

### 12.2 Self-hosting TCO

| Item | Approximate cost |
|---|---|
| Cloud GPU (L4/A10G) | $0.5–1.2 per hour |
| Cloud GPU (A100/H100) | $2–4 per hour |
| RTX 4090 (rented) | $0.3–0.7 per hour |
| Dedicated GPU server | $300–1,500 per month |
| MLOps/maintenance | 15–30% of infrastructure |

**The key sentence.** Whisper large-v3-turbo on a single L4 transcribes at roughly 30–60× real time — so one GPU-hour equals 30–60 hours of audio, or about **$0.01–0.04 per audio hour**. At scale (above roughly 500 hours per month) that undercuts any cheap API. What it does not include is engineering time and operational risk.

**Break-even.** If you produce or transcribe more than 300–500 hours of audio per month and have engineering capacity, self-hosting deserves serious consideration. Below that, APIs are cheaper and far less painful.

### 12.3 Hidden costs

- **Egress and bandwidth** on bulk audio delivery.
- **Retries and quality:** TTS error rates (mispronunciation, truncation) cause regeneration and double billing.
- **Version lock:** cloud models change without notice; yesterday's output is not today's. Pin versions or cache outputs.
- **Data governance:** voice is biometric data. In some sectors (health, banking), sending it to the cloud is prohibited, which forces self-hosting.

---

## 13. Licensing: a decision table

| License | Commercial use | Modification | Attribution | Examples |
|---|---|---|---|---|
| **Apache 2.0** | Yes | Yes | Yes (NOTICE) | Kokoro, CosyVoice, Dia, Orpheus, Qwen3-Omni |
| **MIT** | Yes | Yes | Yes | Whisper, Piper, Chatterbox, Demucs, RVC |
| **BSD** | Yes | Yes | Yes | RNNoise |
| **CC-BY 4.0** | Yes | Yes | Yes | Moshi, Parakeet/Canary |
| **CC-BY-NC** | No | Yes | Yes | MusicGen weights, F5-TTS weights, YuE weights |
| **Stability Community** | Yes below $1M revenue | Yes | Yes | Stable Audio Open |
| **Llama/Community proprietary** | Conditional | Conditional | — | Some Meta/Microsoft models |
| **CPML (Coqui)** | No | Yes | — | XTTS-v2 |
| **AGPL** | Yes (with service source obligation) | Yes | Yes | so-vits-svc |
| **Proprietary cloud** | Per contract | No | — | ElevenLabs, Suno, Deepgram |

**The golden rule:** the license on the repository is not the license on the weights. F5-TTS has MIT code and CC-BY-NC weights; Fish Speech has open code and non-commercial weights. Read the `LICENSE` file attached to the weights on Hugging Face.

---

## 14. Choosing by scenario

| Scenario | First choice | Alternative | Why |
|---|---|---|---|
| **Phone agent** | Cartesia Sonic-3 + Deepgram Nova-3 | ElevenLabs Flash + AssemblyAI | Sub-300 ms latency, predictable cost |
| **Persian audiobook** | Azure Neural (fa-IR) + editing | ElevenLabs (test first) | Official Persian coverage and pronunciation |
| **English podcast/video** | ElevenLabs v3 | PlayHT, Hume | Expression and cloning |
| **Film/TV dubbing** | Respeecher / ElevenLabs + processing | Synthesizer V for singing | Quality and voice rights |
| **Customer calls (ASR + analytics)** | AssemblyAI / Deepgram | Speechmatics | Diarization plus conversation analytics |
| **Bulk cheap transcription** | Whisper large-v3-turbo (self-host) | Soniox API | Lowest cost at scale |
| **Persian subtitles** | Whisper + human review | Azure fa-IR | Acceptable accuracy, low cost |
| **Commercial background music** | Adobe Firefly / Stable Audio | ACE-Step (self-host) | Legal safety |
| **Full songs with vocals** | Suno v5 / Udio | ACE-Step / YuE | Quality and speed |
| **Game sound effects** | ElevenLabs SFX / Stable Audio | TangoFlux, Woosh | Variety and control |
| **Automatic video Foley** | MMAudio / HunyuanVideo-Foley | Kling Foley | Picture sync |
| **Call noise suppression** | DeepFilterNet3 / Krisp | RNNoise | Real-time and light |
| **Stem separation for remixes** | BS-RoFormer / Demucs | UVR5 | Separation quality |
| **Research and fine-tuning** | Whisper + Qwen3-Omni + ACE-Step | Kokoro, Parakeet | Open and modifiable |

---

## 15. The Persian situation

**Persian ASR.** Whisper large-v3 works on Persian (WER around 10–15% on clean speech, higher in casual or noisy audio). Common failure modes: numbers, the zero-width non-joiner, Arabic versus Persian letter forms, and proper nouns. Azure fa-IR and Google fa-IR have official support and are solid on formal or news-style speech. Speechmatics supports Persian; Vosk fa is light but inaccurate; MMS covers it with lower quality. For high accuracy on conversational Persian, fine-tuning Whisper on labeled in-domain data is the most reliable path.

**Persian TTS.** Azure and Google are the stable official options. ElevenLabs covers Persian in its multilingual models, but pronunciation quality needs testing on your own vocabulary — numbers, idioms, names. On the open side: Piper fa_IR (fast, light, robotic) and community VITS/Coqui models trained on ManaTTS and Common Voice fa. The quality ceiling depends on data and training time.

**The real gap.** No open multilingual model at the current state of the art covers Persian at English-level quality. For a Persian product, a fine-tuned open model plus a pronunciation dictionary is more realistic than expecting a general model to handle it out of the box.

**Engineering notes for Persian:** text normalization (digits, half-spaces, alef variants), a pronunciation lexicon for proper nouns, and evaluation on an internal test set rather than public MOS numbers.

---

## 16. Benchmarks worth looking at

| Area | Benchmark / leaderboard | Caveat |
|---|---|---|
| TTS | **TTS Arena (Hugging Face)**, **Artificial Analysis Speech Arena** | Human votes; correlates well with perception |
| ASR | **Open ASR Leaderboard (HF)** | English WER; not valid for Persian |
| Multilingual ASR | **FLEURS**, **Common Voice** | Language coverage |
| Audio understanding | **MMAU**, **AudioBench**, **LongAudioBench** | Reasoning and long-form audio |
| Separation | **MUSDB18 / SDR** | Stem quality |
| Music | Human evaluation + FAD | Automated metrics are not enough |

**A warning.** Public benchmarks are not your domain. Always build a small test set from your own data (50–200 samples) and compare models on it. That is the only metric you can actually trust.

---

## 17. Risks and legal considerations

1. **Voice cloning** requires explicit consent, consent logging, and disclosure that the audio is synthetic. The EU AI Act and several US states (Tennessee, California) impose transparency requirements.
2. **Music copyright.** Suno and Udio reached agreements with publishers in 2025, but open models trained on protected data still carry risk. For commercial products, choose models with transparent data licensing.
3. **Biometric data.** Voice is sensitive personal data under GDPR and CCPA; storing or transferring it requires a DPIA.
4. **Vendor lock-in.** Dependence on one API means exposure to price and version changes. Keep an abstraction layer and a swap path.
5. **Safety and hallucination.** Audio models can generate harmful speech; output filtering and logging are necessary.
6. **Low-resource languages.** Quality drops sharply versus English. Manage expectations accordingly.

---

## 18. A practical evaluation checklist

- [ ] 50–200 real samples from your own data (including noise, accents, terminology).
- [ ] Numeric success criteria: target WER, MOS, TTFA, pronunciation error rate.
- [ ] Blind A/B testing between the three finalists.
- [ ] Cost per unit of work including retry rates.
- [ ] Weight license review for commercial use.
- [ ] Stability test: same input, ten runs, measure variance.
- [ ] Streaming/latency test on real networks, not just benchmarks.
- [ ] An exit plan: export format and model replacement path.

---

## 19. Sources

**Leaderboards and benchmarks:**
- [Artificial Analysis — Text to Speech Leaderboard](https://artificialanalysis.ai/text-to-speech/leaderboard)
- [Hugging Face — Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard)
- [Hugging Face — TTS Arena](https://huggingface.co/spaces/TTS-AGI/TTS-Arena-V2)

**Pricing and comparison (for verification):**
- [Deepgram Pricing](https://deepgram.com/pricing)
- [ElevenLabs Pricing](https://elevenlabs.io/pricing)
- [OpenAI API Pricing](https://openai.com/api/pricing/)
- [AssemblyAI Pricing](https://www.assemblyai.com/pricing)
- [Google Cloud TTS Pricing](https://cloud.google.com/text-to-speech/pricing)
- [Azure Speech Pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services/)
- [AWS Polly Pricing](https://aws.amazon.com/polly/pricing/)
- [Suno Pricing](https://suno.com/pricing)
- [Future AGI — TTS comparison 2026](https://futureagi.com/blog/best-text-to-speech-providers-2026/)
- [Future AGI — STT comparison 2026](https://futureagi.com/blog/speech-to-text-apis-in-2026-benchmarks-pricing-developer-s-decision-guide/)

**Open models (selection):**
- [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
- [Chatterbox](https://github.com/resemble-ai/chatterbox)
- [CosyVoice](https://github.com/FunAudioLLM/CosyVoice)
- [F5-TTS](https://github.com/SWivid/F5-TTS)
- [ACE-Step](https://github.com/ace-step/ACE-Step)
- [Demucs](https://github.com/facebookresearch/demucs)
- [Qwen3-Omni](https://github.com/QwenLM/Qwen3-Omni)
- [Whisper](https://github.com/openai/whisper)

---

## Appendix: ten quick picks

| If you need… | Pick |
|---|---|
| Cheapest good TTS | Kokoro-82M (self-host) or OpenAI tts-1 |
| Best commercial TTS | ElevenLabs v3 |
| Best commercial ASR | Deepgram Nova-3 / AssemblyAI Universal-3 |
| Best open ASR | Whisper large-v3-turbo or Parakeet-TDT |
| Best full songs | Suno v5 |
| Best open music | ACE-Step |
| Best text-to-SFX | ElevenLabs SFX v2 |
| Best video Foley | MMAudio / HunyuanVideo-Foley |
| Best open audio understanding | Qwen3-Omni |
| Best stem separation | BS-RoFormer |
