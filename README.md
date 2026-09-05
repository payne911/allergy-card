# Allergy Card

A small native Android app for travellers with food allergies.

Pick your allergens, pick a language, and hand the waiter a big, unmistakable red card
listing what you can't eat — in *their* language.

**Live web preview:** https://payne911.github.io/allergy-card/ — the same app in your
browser, no download needed.

## Screenshots

| First-launch walkthrough | Picking allergens | The waiter card |
| --- | --- | --- |
| ![First-launch walkthrough](screenshots/onboarding.png) | ![Picking allergens](screenshots/select-allergens.png) | ![The waiter card in Japanese](screenshots/waiter-card.png) |

## Features

- The standard major allergens (peanuts, tree nuts, dairy, egg, wheat/gluten, soy, fish,
  shellfish, sesame, mustard, celery, sulfites, lupin).
- Example dishes that commonly contain each allergen, plus hidden-source notes
  (fish sauce in Southeast Asian cooking, wheat in soy sauce, shrimp paste in curries…).
- A full-screen, high-contrast "show the waiter" card.
- A first-launch walkthrough showing new users the three things to do:
  pick allergens, choose a language, show the red card.

## Fully offline, fully private

- **No internet needed at the table.** The Android app ships with everything on board
  and the web version caches itself on first load (service worker), so both work
  with airplane mode on.
- **No data leaves your device.** Your selected allergens and language are stored
  locally only — SharedPreferences on Android, `localStorage` in the browser.
  There is no account, no server, and nothing to "delete" anywhere else.

## Languages

English, French, Spanish, Italian, German, Portuguese, Japanese, Chinese,
Korean, Thai, Vietnamese, Arabic.

## Build (Android)

Open in Android Studio, or:

```bash
gradle assembleDebug
```

A GitHub Actions workflow that builds `app-debug.apk` is ready in
`android-workflow.yml.disabled`; move it into `.github/workflows/` to enable CI
(requires a token with the `workflow` scope).

## Web preview (this repo)

The preview site lives in [`docs/`](docs/index.html) and is a single self-contained
HTML file — all allergens, languages, example dishes, the onboarding, and the red
waiter card, with choices persisted in `localStorage` and a service worker
(`docs/sw.js`) for offline use.
