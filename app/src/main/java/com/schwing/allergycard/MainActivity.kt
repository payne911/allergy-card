package com.schwing.allergycard

import android.app.Activity
import android.graphics.Rect
import android.os.Build
import android.os.Bundle
import android.view.WindowInsets
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.FrameLayout
import android.window.OnBackInvokedDispatcher

/**
 * Allergy Card on Android is the same single-page app that lives in docs/
 * (the one GitHub Pages serves), bundled offline into a WebView.
 *
 * Keep this a thin shell on purpose: every feature — photos, severity levels,
 * URL/QR sharing, languages — ships from docs/ and never from Kotlin here.
 * Gradle copies docs/ into assets before every build; see app/build.gradle.kts.
 *
 * Android 16 notes (targetSdk 36):
 * - Edge-to-edge is mandatory; windowOptOutEdgeToEdgeEnforcement is a no-op.
 *   The shell pads the WebView's *container* by the system-bar insets itself.
 *   (Padding the WebView directly does nothing: it ignores its own padding
 *   when rendering page content.)
 * - onBackPressed() is never called; back must go through
 *   OnBackInvokedDispatcher.
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

        // Container for the WebView, padded by the system-bar insets so the
        // page never draws under the status or navigation bars.
        val root = FrameLayout(this)
        root.addView(
            web,
            FrameLayout.LayoutParams(
                FrameLayout.LayoutParams.MATCH_PARENT,
                FrameLayout.LayoutParams.MATCH_PARENT
            )
        )
        root.setOnApplyWindowInsetsListener { v, insets ->
            val bars = systemBars(insets)
            v.setPadding(bars.left, bars.top, bars.right, bars.bottom)
            insets
        }
        setContentView(root)

        // API 33+: back is delivered through the dispatcher. On API 36 the
        // onBackPressed() override below is never invoked at all.
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            onBackInvokedDispatcher.registerOnBackInvokedCallback(
                OnBackInvokedDispatcher.PRIORITY_DEFAULT
            ) { handleBack() }
        }

        if (savedInstanceState != null) {
            web.restoreState(savedInstanceState)
        } else {
            web.loadUrl("file:///android_asset/index.html")
        }
    }

    private fun systemBars(insets: WindowInsets): Rect =
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            insets.getInsets(WindowInsets.Type.systemBars())
        } else {
            @Suppress("DEPRECATION")
            Rect(
                insets.systemWindowInsetLeft,
                insets.systemWindowInsetTop,
                insets.systemWindowInsetRight,
                insets.systemWindowInsetBottom
            )
        }

    // Step back through the in-app screens before falling back to closing.
    // Ask the page first: dialogs (waiter card, settings, pickers) are tracked
    // in JS, which stays correct even where WebView history entries don't
    // exist (file://). Only then fall back to history, then to closing.
    private fun handleBack() {
        web.evaluateJavascript("window.AllergyApp ? AllergyApp.topDialog() : null") { r ->
            val top = r?.trim()?.trim('"')
            if (!top.isNullOrEmpty() && top != "null") {
                web.evaluateJavascript("AllergyApp.closeTopDialog()", null)
            } else if (web.canGoBack()) {
                web.goBack()
            } else {
                finish()
            }
        }
    }

    // API < 33 fallback; on 33+ the dispatcher callback above owns back.
    @Suppress("DEPRECATION")
    override fun onBackPressed() {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.TIRAMISU) {
            handleBack()
        }
    }

    override fun onSaveInstanceState(outState: Bundle) {
        super.onSaveInstanceState(outState)
        web.saveState(outState)
    }

    override fun onDestroy() {
        if (::web.isInitialized) web.destroy()
        super.onDestroy()
    }
}
