package com.schwing.allergycard

import android.content.Context
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.schwing.allergycard.data.ALLERGENS
import com.schwing.allergycard.data.Allergen
import com.schwing.allergycard.data.LANGUAGES
import com.schwing.allergycard.data.PHRASES

private val AlertRed = Color(0xFFB00020)
private val CardBg = Color(0xFFFFF8F8)
private val SelectedBg = Color(0xFFFFE4E4)
private val PageBg = Color(0xFFFFFFFF)
private val Ink = Color(0xFF1B1B1B)

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { AllergyApp() }
    }
}

@Composable
fun AllergyApp() {
    val context = androidx.compose.ui.platform.LocalContext.current
    val prefs = remember { context.getSharedPreferences("allergy_card", Context.MODE_PRIVATE) }
    var selected by remember { mutableStateOf(prefs.getStringSet("selected", emptySet())?.toSet() ?: emptySet()) }
    var expanded by remember { mutableStateOf(setOf<String>()) }
    var lang by remember { mutableStateOf(prefs.getString("lang", "en") ?: "en") }
    var showCard by remember { mutableStateOf(false) }

    LaunchedEffect(selected) { prefs.edit().putStringSet("selected", selected).apply() }
    LaunchedEffect(lang) { prefs.edit().putString("lang", lang).apply() }

    Scaffold(
        containerColor = PageBg,
        bottomBar = {
            Box(Modifier.fillMaxWidth().padding(16.dp)) {
                Button(
                    onClick = { showCard = true },
                    enabled = selected.isNotEmpty(),
                    colors = ButtonDefaults.buttonColors(containerColor = AlertRed),
                    modifier = Modifier.fillMaxWidth().height(56.dp),
                    shape = RoundedCornerShape(28.dp),
                ) {
                    Text("SHOW THE WAITER CARD", fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color.White)
                }
            }
        },
    ) { padding ->
        Column(Modifier.padding(padding).fillMaxSize().padding(horizontal = 16.dp)) {
            Spacer(Modifier.height(12.dp))
            Text("Allergy Card", color = AlertRed, fontSize = 30.sp, fontWeight = FontWeight.Bold)
            Text("Tap the allergens you're allergic to — picking one shows the dishes that usually contain it.", color = Ink)
            Spacer(Modifier.height(8.dp))
            LanguagePicker(lang = lang, onPick = { lang = it })
            Spacer(Modifier.height(8.dp))
            LazyColumn(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                items(ALLERGENS) { allergen ->
                    AllergenRow(
                        allergen = allergen,
                        isSelected = selected.contains(allergen.id),
                        isExpanded = expanded.contains(allergen.id),
                        lang = lang,
                        onToggle = { selected = if (selected.contains(allergen.id)) selected - allergen.id else selected + allergen.id },
                        onExpand = { expanded = if (expanded.contains(allergen.id)) expanded - allergen.id else expanded + allergen.id },
                    )
                }
                item { Spacer(Modifier.height(8.dp)) }
            }
        }
    }

    if (showCard && selected.isNotEmpty()) {
        WaiterCard(lang = lang, selectedIds = selected, onChangeLang = { lang = it }, onClose = { showCard = false })
    }
}

@Composable
fun LanguagePicker(lang: String, onPick: (String) -> Unit, label: String? = null) {
    var open by remember { mutableStateOf(false) }
    val current = LANGUAGES.firstOrNull { it.code == lang } ?: LANGUAGES.first()
    Box {
        OutlinedButton(onClick = { open = true }, shape = RoundedCornerShape(24.dp)) {
            Text("🌐 ${label ?: "Language"}: ${current.nativeLabel}", color = Ink)
            Icon(Icons.Default.KeyboardArrowDown, contentDescription = null, tint = Ink)
        }
        DropdownMenu(expanded = open, onDismissRequest = { open = false }) {
            LANGUAGES.forEach { l ->
                DropdownMenuItem(
                    text = { Text("${l.nativeLabel} — ${l.label}") },
                    onClick = { onPick(l.code); open = false },
                )
            }
        }
    }
}

@Composable
fun AllergenRow(
    allergen: Allergen,
    isSelected: Boolean,
    isExpanded: Boolean,
    lang: String,
    onToggle: () -> Unit,
    onExpand: () -> Unit,
) {
    Surface(
        modifier = Modifier.fillMaxWidth().clickable { onToggle() },
        shape = RoundedCornerShape(14.dp),
        color = if (isSelected) SelectedBg else CardBg,
        border = androidx.compose.foundation.BorderStroke(
            1.dp, if (isSelected) AlertRed else Color(0xFFE0DADA)
        ),
    ) {
        Column(Modifier.padding(12.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(allergen.emoji, fontSize = 28.sp)
                Spacer(Modifier.width(10.dp))
                Column(Modifier.weight(1f)) {
                    Text(allergen.name(lang), fontWeight = FontWeight.Bold, fontSize = 18.sp, color = Ink)
                    if (lang != "en") Text(allergen.name("en"), fontSize = 13.sp, color = Color(0xFF555555))
                }
                if (isSelected) Icon(Icons.Default.Check, contentDescription = "selected", tint = AlertRed)
                IconButton(onClick = onExpand) {
                    Icon(Icons.Default.Info, contentDescription = "dishes", tint = Color(0xFF888888))
                }
            }
            if (isExpanded) {
                Spacer(Modifier.height(8.dp))
                Text("Usually in:", fontWeight = FontWeight.Bold, fontSize = 14.sp, color = Ink)
                allergen.dishes.forEach { Text("• $it", fontSize = 14.sp, color = Ink) }
                Spacer(Modifier.height(4.dp))
                Text("Watch out: ${allergen.watchOut}", fontSize = 13.sp, color = Color(0xFF666666))
            }
        }
    }
}

@Composable
fun WaiterCard(lang: String, selectedIds: Set<String>, onChangeLang: (String) -> Unit, onClose: () -> Unit) {
    Dialog(
        onDismissRequest = onClose,
        properties = DialogProperties(usePlatformDefaultWidth = false),
    ) {
        Surface(modifier = Modifier.fillMaxSize(), color = AlertRed) {
            Box(Modifier.fillMaxSize()) {
                Column(
                    Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        LanguagePicker(lang = lang, onPick = onChangeLang, label = "Card language")
                    }
                    Spacer(Modifier.height(28.dp))
                    Text("⚠️", fontSize = 72.sp)
                    Text("ALLERGY ALERT", color = Color.White, fontSize = 38.sp, fontWeight = FontWeight.ExtraBold)
                    Spacer(Modifier.height(16.dp))
                    Text(
                        PHRASES[lang] ?: PHRASES.getValue("en"),
                        color = Color.White, fontSize = 22.sp, fontWeight = FontWeight.Medium,
                    )
                    if (lang != "en") {
                        Spacer(Modifier.height(6.dp))
                        Text(PHRASES.getValue("en"), color = Color(0xFFFFD6D6), fontSize = 15.sp)
                    }
                    Spacer(Modifier.height(24.dp))
                    ALLERGENS.filter { selectedIds.contains(it.id) }.forEach { a ->
                        Row(
                            Modifier.fillMaxWidth().padding(vertical = 8.dp),
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            Text(a.emoji, fontSize = 44.sp)
                            Spacer(Modifier.width(16.dp))
                            Column {
                                Text(a.name(lang), color = Color.White, fontSize = 30.sp, fontWeight = FontWeight.Bold)
                                if (lang != "en") Text(a.name("en"), color = Color(0xFFFFD6D6), fontSize = 16.sp)
                            }
                        }
                        Divider(color = Color(0x55FFFFFF))
                    }
                }
                IconButton(
                    onClick = onClose,
                    modifier = Modifier.align(Alignment.TopEnd).padding(8.dp),
                ) {
                    Icon(Icons.Default.Close, contentDescription = "close", tint = Color.White)
                }
            }
        }
    }
}
