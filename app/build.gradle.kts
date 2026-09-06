plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.schwing.allergycard"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.schwing.allergycard"
        minSdk = 26
        targetSdk = 34
        versionCode = 2
        versionName = "2.0"
    }

    // Manifest already picks .MainActivity (a plain Activity), no androidx needed.
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
}

/**
 * The whole product lives in docs/ — the exact same code GitHub Pages serves.
 * Copy it into the APK's bundled assets before every build so this Kotlin
 * shell stays a thin wrapper and the app works fully offline on a plane.
 */
val syncWebAssets = tasks.register<Copy>("syncWebAssets") {
    description = "Copies docs/ (the single codebase) into the bundled app assets"
    from("${projectDir}/../docs")
    into("${projectDir}/src/main/assets")
}

tasks.named("preBuild") {
    dependsOn(syncWebAssets)
}

dependencies {
    // Intentionally empty: the app is one WebView and needs no support libraries.
}
