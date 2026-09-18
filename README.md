# Allergy Card

A small app for travellers with food allergies.

Pick your allergens, pick a language, and hand the waiter a big, unmistakable red card
listing what you can't eat — in *their* language.

**Live web version:** https://payne911.github.io/allergy-card/ — the same app in your
browser, no download needed.

## One codebase

Everything lives in [`docs/`](docs/index.html): one single-page app in plain HTML/JS —
allergen emoji, languages, and shareable URLs.

- The **website** is those files served as-is (GitHub Pages from `main:/docs`).
- The **Android app** is a bare WebView shell (`app/…/MainActivity.kt`, ~50 lines)
  that bundles the exact same files offline. Gradle copies `docs/` into the APK
  before every build (`syncWebAssets` in `app/build.gradle.kts`).

Change something once in `docs/`, and both the site and the app get it.

## Screenshots

| First-launch walkthrough | Picking allergens | The waiter card |
| --- | --- | --- |
| ![First-launch walkthrough](screenshots/onboarding.png) | ![Picking allergens](screenshots/select-allergens.png) | ![The waiter card in Japanese](screenshots/waiter-card.png) |

## Features

- **44 built-in allergens**, each with a big emoji so the card reads at a glance —
  from the usual majors (peanuts, tree nuts, milk, egg, wheat, soy, fish, shellfish,
  sesame, mustard, sulfites) to meats, poultry, grains, fruits, vegetables, seeds,
  gelatin and chocolate. A search bar filters the list instantly, and a settings
  switch drops the emojis for a text-only layout.
- **Add your own restrictions.** Anything beyond the built-in list — a rare allergy, a
  preference, a medication interaction — can be added with your own wording; the emoji
  is optional (tap a preset or type one with your phone keyboard, or leave it blank).
  Custom entries select, search, edit, remove and share exactly like the
  built-ins; because they're free text, they appear on the card in every language
  word-for-word as typed.
- **188 languages.** On first launch you pick your own language for the app itself —
  the interface follows it from then on (change it later from the ⚙️ settings gear).
  The waiter's language is a separate, searchable picker covering everything from
  French and Japanese to Quechua, Cantonese and Amharic. Every dialog closes with a
  plain X, and on Android the back button closes the topmost dialog first.
- **Shareable card links.** The whole profile — allergens, custom entries, waiter
  language — is encoded in the URL (`?a=id,id&lang=xx`, custom entries as
  `c=emoji~text` params), so copying the link opens the identical card on anyone's
  phone. The waiter card also carries an offline QR code (generated on-device,
  caption in the waiter's language) for the same one-scan handoff. Older link
  formats keep working.
- A full-screen, high-contrast "show the waiter" card — big ⚠️ header, one allergen
  per line, subtitles in the waiter's language, no clutter — with a tap-to-copy 🔗
  button at the bottom and RTL support for right-to-left scripts.
- Example dishes that commonly contain each allergen, plus hidden-source notes
  (fish sauce in Southeast Asian cooking, wheat in soy sauce, shrimp paste in curries…).
- The ⚙️ settings gear in the title bar opens a small settings dialog: app
  language (one more tap to the full list) and an "allergen emojis" switch
  for a text-only layout.
- A first-launch walkthrough showing new users the three things to do:
  pick allergens, choose a language, show the red card.

## Fully offline, fully private

- **No internet needed at the table.** The Android app ships with everything on board
  and the web version caches itself on first load (service worker), so both work
  with airplane mode on.
- **No data leaves your device.** Your selected allergens and language are stored
  locally only (`localStorage` — the Android shell uses the same storage as
  the browser build). There is no account, no server, and nothing to "delete"
  anywhere else.

## Languages

188 languages, generated once and baked into static files
(`docs/languages.json.js` for the picker list, `docs/lang/<code>.json.js` per
language). Machine translation is done ahead of time by
[`tools/gen_languages.py`](tools/gen_languages.py), so the app itself never
needs the network to find a language — re-run the script to add or refresh
languages, it skips what's already on disk. English is always bundled; any other
pack loads on first use and is then cached for offline use (service worker on
the web build, plain files in the APK).

## Build (Android)

Debug builds in Android Studio, or:

```bash
gradle assembleDebug
```

Releases go through GitHub Actions: pushing a `v*` tag builds a signed
`bundleRelease` AAB (keystore comes from repo secrets) and uploads it to the
**internal testing** track on Google Play — see
[`.github/workflows/release.yml`](.github/workflows/release.yml).

No design decision to make about "keeping the app in sync": the Gradle
`syncWebAssets` task copies `docs/` into the app bundle on every build,
so the APK/AAB always ships the same card the website serves. The shell itself
needs nothing beyond the Android SDK — one WebView, zero dependencies.

## Disclaimer

**Reference only — not medical advice.** Always confirm with staff and carry your
medication. (This note also lives permanently in the app itself.)

This is a personal project, provided as-is, with no guarantee of any kind.
Translations and example dishes are best-effort reference material. I am not
responsible for any issues that come from using this app.

## Web preview (this repo)

The preview site lives in [`docs/`](docs/index.html) — all allergens, languages,
example dishes, shareable URLs, and the red waiter
card, with choices persisted in `localStorage` and a service worker
(`docs/sw.js`) for offline use. The site auto-deploys from `main:/docs` on every push.
