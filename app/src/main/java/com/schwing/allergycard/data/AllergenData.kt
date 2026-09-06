package com.schwing.allergycard.data

data class Language(val code: String, val label: String, val nativeLabel: String)

val LANGUAGES = listOf(
    Language("en", "English", "English"),
    Language("fr", "French", "Français"),
    Language("es", "Spanish", "Español"),
    Language("it", "Italian", "Italiano"),
    Language("de", "German", "Deutsch"),
    Language("pt", "Portuguese", "Português"),
    Language("ja", "Japanese", "日本語"),
    Language("zh", "Chinese", "中文"),
    Language("ko", "Korean", "한국어"),
    Language("th", "Thai", "ไทย"),
    Language("vi", "Vietnamese", "Tiếng Việt"),
    Language("ar", "Arabic", "العربية"),
)

/** "I am allergic to these foods. Please do not put them in my meal." in each language. */
val PHRASES = mapOf(
    "en" to "I am allergic to these foods. Please do not put them in my meal.",
    "fr" to "Je suis allergique à ces aliments. Merci de les exclure de mon repas.",
    "es" to "Soy alérgico/a a estos alimentos. Por favor, no los incluya en mi comida.",
    "it" to "Sono allergico/a a questi alimenti. Per favore, non li mettete nel mio pasto.",
    "de" to "Ich bin gegen diese Lebensmittel allergisch. Bitte lassen Sie sie aus meinem Essen weg.",
    "pt" to "Sou alérgico(a) a estes alimentos. Por favor, não os inclua na minha refeição.",
    "ja" to "私はこれらの食べ物にアレルギーがあります。食事に入れないでください。",
    "zh" to "我对以下食物过敏。请不要在我的餐点中放这些。",
    "ko" to "저는 아래 음식에 알레르기가 있습니다. 식사에 넣지 말아 주세요.",
    "th" to "ฉันแพ้อาหารเหล่านี้ กรุณาอย่าใส่ในอาหารของฉัน",
    "vi" to "Tôi bị dị ứng với những thức ăn này. Vui lòng không cho vào món ăn của tôi.",
    "ar" to "لدي حساسية من هذه الأطعمة. يرجى عدم وضعها في وجبتي.",
)

data class Allergen(
    val id: String,
    val emoji: String,
    /** Example dishes that commonly contain it. */
    val dishes: List<String>,
    /** Common hidden sources to watch out for. */
    val watchOut: String,
    /** Allergen name per language code. */
    val names: Map<String, String>,
) {
    fun name(lang: String): String = names[lang] ?: names.getValue("en")
}

val ALLERGENS = listOf(
    Allergen(
        id = "peanuts",
        emoji = "🥜",
        dishes = listOf("Pad Thai", "Satay skewers", "Peanut butter cookies", "Mole sauce"),
        watchOut = "Often hidden in Asian sauces, garnishes, and desserts.",
        names = mapOf(
            "en" to "peanuts", "fr" to "arachides", "es" to "cacahuetes / maní",
            "it" to "arachidi", "de" to "Erdnüsse", "pt" to "amendoim",
            "ja" to "ピーナッツ", "zh" to "花生", "ko" to "땅콩",
            "th" to "ถั่วลิสง", "vi" to "đậu phộng", "ar" to "فول سوداني",
        ),
    ),
    Allergen(
        id = "tree_nuts",
        emoji = "🌰",
        dishes = listOf("Pesto (pine nuts)", "Baklava", "Almond croissants", "Granola"),
        watchOut = "Includes almonds, cashews, walnuts, hazelnuts, pistachios, and pine nuts. Watch nut oils in salads and pastries.",
        names = mapOf(
            "en" to "tree nuts", "fr" to "fruits à coque", "es" to "frutos secos",
            "it" to "frutta a guscio", "de" to "Nüsse", "pt" to "frutos de casca rija",
            "ja" to "木の実類", "zh" to "坚果", "ko" to "견과류",
            "th" to "ถั่วเปลือกแข็ง", "vi" to "các loại hạt", "ar" to "مكسرات",
        ),
    ),
    Allergen(
        id = "milk",
        emoji = "🥛",
        dishes = listOf("Butter chicken", "Mac & cheese", "Bechamel lasagna", "Crème brûlée"),
        watchOut = "Butter, cream, cheese, and ghee count too. Many curries and sauces use cream or butter.",
        names = mapOf(
            "en" to "milk / dairy", "fr" to "lait", "es" to "leche",
            "it" to "latte", "de" to "Milch", "pt" to "leite",
            "ja" to "牛乳", "zh" to "牛奶", "ko" to "우유",
            "th" to "นม", "vi" to "sữa", "ar" to "حليب",
        ),
    ),
    Allergen(
        id = "egg",
        emoji = "🥚",
        dishes = listOf("Quiche", "Caesar dressing", "Tamago sushi", "Custard"),
        watchOut = "Also in fresh pasta, mayo, glazing on pastries, and many desserts.",
        names = mapOf(
            "en" to "eggs", "fr" to "œufs", "es" to "huevos",
            "it" to "uova", "de" to "Eier", "pt" to "ovos",
            "ja" to "卵", "zh" to "鸡蛋", "ko" to "계란",
            "th" to "ไข่", "vi" to "trứng", "ar" to "بيض",
        ),
    ),
    Allergen(
        id = "wheat_gluten",
        emoji = "🌾",
        dishes = listOf("Ramen", "Pizza", "Dumplings", "Soy sauce dishes"),
        watchOut = "Regular soy sauce contains wheat. Gluten also hides in seitan, malt, and many sauces.",
        names = mapOf(
            "en" to "wheat / gluten", "fr" to "blé / gluten", "es" to "trigo / gluten",
            "it" to "grano / glutine", "de" to "Weizen / Gluten", "pt" to "trigo / glúten",
            "ja" to "小麦・グルテン", "zh" to "小麦 / 麸质", "ko" to "밀 / 글루텐",
            "th" to "ข้าวสาลี / กลูเตน", "vi" to "lúa mì / gluten", "ar" to "قمح / جلوتين",
        ),
    ),
    Allergen(
        id = "soy",
        emoji = "🫘",
        dishes = listOf("Miso soup", "Edamame", "Tofu dishes", "Veggie burgers"),
        watchOut = "Common in Asian cooking via soy sauce, tofu, and tempeh; soy lecithin is in many packaged foods.",
        names = mapOf(
            "en" to "soy", "fr" to "soja", "es" to "soja",
            "it" to "soia", "de" to "Soja", "pt" to "soja",
            "ja" to "大豆", "zh" to "大豆", "ko" to "대두",
            "th" to "ถั่วเหลือง", "vi" to "đậu nành", "ar" to "صويا",
        ),
    ),
    Allergen(
        id = "peas",
        emoji = "🫛",
        dishes = listOf("Split pea soup", "Pea & ham soup", "Risi e bisi", "Matar paneer"),
        watchOut = "Pea protein is now common in meat substitutes and protein snacks. Peas also mix invisibly into fried rice, pilafs, and soups.",
        names = mapOf(
            "en" to "peas", "fr" to "pois", "es" to "guisantes",
            "it" to "piselli", "de" to "Erbsen", "pt" to "ervilhas",
            "ja" to "グリーンピース", "zh" to "豌豆", "ko" to "완두콩",
            "th" to "ถั่วลันเตา", "vi" to "đậu Hà Lan", "ar" to "بازلاء",
        ),
    ),
    Allergen(
        id = "chickpeas",
        emoji = "🧆",
        dishes = listOf("Hummus", "Falafel", "Chana masala", "Pakora fritters"),
        watchOut = "Hummus arrives unasked with many mezze and wraps. Chickpea flour (gram / besan) thickens fritters like pakora and some batters.",
        names = mapOf(
            "en" to "chickpeas", "fr" to "pois chiches", "es" to "garbanzos",
            "it" to "ceci", "de" to "Kichererbsen", "pt" to "grão-de-bico",
            "ja" to "ひよこ豆", "zh" to "鹰嘴豆", "ko" to "병아리콩",
            "th" to "ถั่วชิกพี", "vi" to "đậu gà", "ar" to "حمص",
        ),
    ),
    Allergen(
        id = "lentils",
        emoji = "🍛",
        dishes = listOf("Dal curries", "Lentil soup", "Mujadara", "Mercimek köfte"),
        watchOut = "Dal and lentil soups rarely say 'lentil' on the menu. Lentils also stand in for meat in many vegan patties and sauces.",
        names = mapOf(
            "en" to "lentils", "fr" to "lentilles", "es" to "lentejas",
            "it" to "lenticchie", "de" to "Linsen", "pt" to "lentilhas",
            "ja" to "レンズ豆", "zh" to "扁豆", "ko" to "렌틸콩",
            "th" to "ถั่วเลนทิล", "vi" to "đậu lăng", "ar" to "عدس",
        ),
    ),
    Allergen(
        id = "fish",
        emoji = "🐟",
        dishes = listOf("Bouillabaisse", "Sushi", "Fish sauce dishes", "Caesar dressing"),
        watchOut = "Fish sauce is ubiquitous in Southeast Asian cooking. Worcestershire sauce contains anchovies.",
        names = mapOf(
            "en" to "fish", "fr" to "poisson", "es" to "pescado",
            "it" to "pesce", "de" to "Fisch", "pt" to "peixe",
            "ja" to "魚", "zh" to "鱼类", "ko" to "생선",
            "th" to "ปลา", "vi" to "cá", "ar" to "سمك",
        ),
    ),
    Allergen(
        id = "shellfish",
        emoji = "🦐",
        dishes = listOf("Shrimp scampi", "Crab rangoon", "Lobster bisque", "Shrimp paste curries"),
        watchOut = "Shrimp paste (belacan / kapi / mắm tôm) hides in many Southeast Asian curries and dips. Shared fryers are risky too.",
        names = mapOf(
            "en" to "shellfish & crustaceans", "fr" to "crustacés et mollusques",
            "es" to "mariscos", "it" to "crostacei e molluschi",
            "de" to "Schalentiere", "pt" to "mariscos",
            "ja" to "甲殻類・貝類", "zh" to "贝类 / 甲壳类", "ko" to "갑각류·조개류",
            "th" to "อาหารทะเล (กุ้ง ปู หอย)", "vi" to "hải sản có vỏ", "ar" to "ثمار البحر القشرية",
        ),
    ),
    Allergen(
        id = "sesame",
        emoji = "🌱",
        dishes = listOf("Hummus / tahini", "Sesame buns", "Goma-ae spinach", "Halva"),
        watchOut = "Sesame oil is heavily used in East Asian kitchens. Sesame seeds cover most burger buns.",
        names = mapOf(
            "en" to "sesame", "fr" to "sésame", "es" to "sésamo / ajonjolí",
            "it" to "sesamo", "de" to "Sesam", "pt" to "gergelim",
            "ja" to "ごま", "zh" to "芝麻", "ko" to "참깨",
            "th" to "งา", "vi" to "mè / vừng", "ar" to "سمسم",
        ),
    ),
    Allergen(
        id = "mustard",
        emoji = "🟡",
        dishes = listOf("Dijon vinaigrette", "Deli sausages", "Curry pastes", "Pickled dishes"),
        watchOut = "Mustard seed powder sneaks into sauces, sausages, pickles, and many prepared foods.",
        names = mapOf(
            "en" to "mustard", "fr" to "moutarde", "es" to "mostaza",
            "it" to "senape", "de" to "Senf", "pt" to "mostarda",
            "ja" to "マスタード・からし", "zh" to "芥末", "ko" to "겨자",
            "th" to "มัสตาร์ด", "vi" to "mù tạt", "ar" to "خردل",
        ),
    ),
    Allergen(
        id = "celery",
        emoji = "🥬",
        dishes = listOf("Vegetable stocks & soups", "Waldorf salad", "Seasoning mixes", "Bouillon cubes"),
        watchOut = "Celery is a base of most stocks and bouillons across Europe, plus spice mixes. It is rarely listed on the plate.",
        names = mapOf(
            "en" to "celery", "fr" to "céleri", "es" to "apio",
            "it" to "sedano", "de" to "Sellerie", "pt" to "aipo",
            "ja" to "セロリ", "zh" to "芹菜", "ko" to "셀러리",
            "th" to "ขึ้นฉ่าย", "vi" to "cần tây", "ar" to "كرفس",
        ),
    ),
    Allergen(
        id = "sulfites",
        emoji = "🍷",
        dishes = listOf("Wine & beer", "Dried fruit", "Shrimp cocktail", "French fries (frozen)"),
        watchOut = "Used as a preservative in wine, dried fruit, some processed shrimp, and some frozen potatoes.",
        names = mapOf(
            "en" to "sulfites", "fr" to "sulfites", "es" to "sulfitos",
            "it" to "solfiti", "de" to "Sulfite", "pt" to "sulfitos",
            "ja" to "亜硫酸塩", "zh" to "亚硫酸盐", "ko" to "아황산염",
            "th" to "ซัลไฟต์", "vi" to "sunfit", "ar" to "كبريتيت",
        ),
    ),
    Allergen(
        id = "lupin",
        emoji = "🌼",
        dishes = listOf("Lupin beans", "Gluten-free pastas", "Some biscuits", "Lupin-flour bread"),
        watchOut = "Lupin flour is increasingly used in gluten-free and protein-enriched baked goods.",
        names = mapOf(
            "en" to "lupin", "fr" to "lupin", "es" to "altramces / lupino",
            "it" to "lupini", "de" to "Lupinen", "pt" to "tremoços",
            "ja" to "ルピナス", "zh" to "羽扇豆", "ko" to "루핀",
            "th" to "ถั่วลูพิน", "vi" to "đậu lupin", "ar" to "لوبين",
        ),
    ),
)
