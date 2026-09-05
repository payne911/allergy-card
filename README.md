# Allergy Card

A small native Android app for travellers with food allergies.

Pick your allergens, pick a language, and hand the waiter a big, unmistakable red card
listing what you can't eat — in *their* language.

## Features

- The standard major allergens (peanuts, tree nuts, dairy, egg, wheat/gluten, soy, fish,
  shellfish, sesame, mustard, celery, sulfites, lupin).
- Example dishes that commonly contain each allergen, plus hidden-source notes
  (fish sauce in Southeast Asian cooking, wheat in soy sauce, shrimp paste in curries…).
- A full-screen, high-contrast "show the waiter" card.
- Everything works offline — no account, no internet needed at the table.

## Languages

English, French, Spanish, Italian, German, Portuguese, Japanese, Chinese,
Korean, Thai, Vietnamese, Arabic.

## Build

Open in Android Studio, or:

```bash
gradle assembleDebug
```

Every push to GitHub also builds `app-debug.apk` via GitHub Actions (see Actions tab →
latest run → Artifacts).
