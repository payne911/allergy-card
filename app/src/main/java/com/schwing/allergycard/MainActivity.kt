package com.schwing.allergycard

import android.app.Activity
import android.os.Bundle
import android.webkit.WebView
import android.webkit.WebViewClient

/**
 * Allergy Card on Android is the same single-page app that lives in docs/
 * (the one GitHub Pages serves), bundled offline into a WebView.
 *
 * Keep this a thin shell on purpose: every feature — photos, severity levels,
 * URL/QR sharing, languages — ships from docs/ and never from Kotlin here.
 * Gradle copies docs/ into assets before every build; see app/build.gradle.kts.
 */
class MainActivity : Activity() {

    private lateinit var web: WebView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        web = WebView(this)
        web.settings.javaScriptEnabled = true
        web.settings.domStorageEnabled = true // saved profile persists like localStorage
        web.settings.allowFileAccess = true   // the card loads bundled allergen photos
        web.webViewClient = WebViewClient()   // keep navigation inside the shell
        setContentView(web)

        if (savedInstanceState != null) {
            web.restoreState(savedInstanceState)
        } else {
            web.loadUrl("file:///android_asset/index.html")
        }
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        web.saveState(outState)
    }

    // Step back through the in-app screens before falling back to closing.
    override fun onBackPressed() {
        if (web.canGoBack()) web.goBack() else super.onBackPressed()
    }

    override fun onDestroy() {
        if (::web.isInitialized) web.destroy()
        super.onDestroy()
    }
}
