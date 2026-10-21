"""WriteGenius: Multilingual Natural Language Processing & Readability Demo (Streamlit)."""

from __future__ import annotations
import streamlit as st
import json
from writegenius.pipeline import analyze_text
from writegenius.metrics.polish_metrics import calculate_pisarek_index

st.set_page_config(
    page_title="WriteGenius — European NLP & Readability Studio",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom header styling
st.markdown(
    """
    <style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 16px;
        border: 1px solid #e9ecef;
        margin-bottom: 12px;
    }
    .badge-easy { background-color: #d4edda; color: #155724; padding: 4px 8px; border-radius: 4px; font-weight: 600; }
    .badge-medium { background-color: #fff3cd; color: #856404; padding: 4px 8px; border-radius: 4px; font-weight: 600; }
    .badge-hard { background-color: #f8d7da; color: #721c24; padding: 4px 8px; border-radius: 4px; font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🧠 WriteGenius Studio")
st.caption("Multilingual Natural Language Processing & Readability Engine for European Languages")

# Sidebar
st.sidebar.header("⚙️ Configuration")
lang_option = st.sidebar.selectbox(
    "Target Language",
    ["Auto-detect", "Polish (pl)", "English (en)", "German (de)", "French (fr)", "Spanish (es)", "Italian (it)", "Ukrainian (uk)"],
)

lang_map = {
    "Auto-detect": None,
    "Polish (pl)": "pl",
    "English (en)": "en",
    "German (de)": "de",
    "French (fr)": "fr",
    "Spanish (es)": "es",
    "Italian (it)": "it",
    "Ukrainian (uk)": "uk",
}
selected_lang = lang_map[lang_option]

preset_choice = st.sidebar.selectbox(
    "Load Preset Sample",
    [
        "None (Custom Input)",
        "Polish: Legal / Corporate (High Complexity)",
        "Polish: Daily News (Medium Complexity)",
        "Polish: Children's Story (Easy)",
        "English: Technical Whitepaper",
        "English: Conversational News",
    ],
)

presets = {
    "Polish: Legal / Corporate (High Complexity)": (
        "Zgodnie z art. 299 Kodeksu spółek handlowych, członkowie zarządu odpowiadają solidarnie "
        "za zobowiązania spółki, jeżeli egzekucja przeciwko spółce okaże się bezskuteczna. "
        "Właściwa diagnoza stanu niewypłacalności oraz terminowe złożenie wniosku restrukturyzacyjnego "
        "stanowią kluczowe przesłanki egzoneracyjne chroniące prywatny majątek członków zarządu."
    ),
    "Polish: Daily News (Medium Complexity)": (
        "Od początku przyszłego miesiąca wchodzą w życie nowe przepisy dotyczące transportu publicznego. "
        "Pasażerowie skorzystają z nowoczesnych biletomatów oraz aplikacji mobilnych ułatwiających podróż. "
        "Władze miasta zapowiadają także dodatkowe kursy autobusów w godzinach szczytu."
    ),
    "Polish: Children's Story (Easy)": (
        "Mały kotek biegał po zielonej trawie. Zobaczył małą myszkę i zaczął się z nią bawić. "
        "Słońce świeciło jasno na błękitnym niebie. Wszyscy byli bardzo zadowoleni."
    ),
    "English: Technical Whitepaper": (
        "The distributed consensus protocol leverages cryptographic primitives to guarantee "
        "byzantine fault tolerance across asynchronous network partitions. Transaction throughput "
        "scales linearly with validator sharding while maintaining deterministic finality guarantees."
    ),
    "English: Conversational News": (
        "The local library opened a new community garden this weekend. Dozens of families joined "
        "to plant flowers and learn about sustainable urban agriculture. Volunteers handed out free seeds."
    ),
}

default_text = presets.get(preset_choice, "")

# Main input
user_text = st.text_area(
    "Paste text to evaluate:",
    value=default_text,
    height=180,
    placeholder="Wpisz lub wklej dowolny tekst w języku polskim, angielskim lub innym języku europejskim...",
)

if user_text.strip():
    with st.spinner("Analyzing linguistic structures..."):
        report = analyze_text(user_text, lang=selected_lang)

    # Top high-level metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Language", report.language.upper())
    with col2:
        st.metric("Words", report.statistics.word_count)
    with col3:
        st.metric("Sentences", report.statistics.sentence_count)
    with col4:
        st.metric("Avg Sentence Len", f"{report.statistics.avg_sentence_length} wds")
    with col5:
        st.metric("Sentiment", f"{report.sentiment.label.upper()} ({report.sentiment.polarity})")

    st.markdown("---")

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🇵🇱 Indeks Pisarka & Readability",
        "📊 Readability Suite",
        "📚 Vocabulary & Lexical Diversity",
        "💡 Diagnostics & Recommendations",
        "⚙️ Raw JSON",
    ])

    with tab1:
        if report.language == "pl" and report.polish_metrics:
            p_res = report.polish_metrics
            st.subheader("🇵🇱 Indeks Pisarka (W) — Oficjalny polski wzorzec czytelności")

            badge_class = "badge-easy" if p_res.pisarek_index < 26 else ("badge-medium" if p_res.pisarek_index < 34 else "badge-hard")

            c_p1, c_p2 = st.columns([1, 2])
            with c_p1:
                st.metric("Wskaźnik Pisarka (W)", p_res.pisarek_index)
                st.markdown(f"**Poziom trudności:** <span class='{badge_class}'>{p_res.pisarek_difficulty_level}</span>", unsafe_allow_html=True)
                st.markdown(f"**Docelowy odbiorca:** {p_res.pisarek_target_audience}")
            with c_p2:
                st.markdown(
                    f"""
                    - **Odsetek trudnych słów (4+ sylaby):** `{p_res.hard_words_ratio_percent}%`
                    - **Adaptowany wskaźnik FOG dla polszczyzny:** `{p_res.fog_polish}`
                    - **Średnia długość zdania:** `{p_res.avg_sentence_length}` słów
                    """
                )
                st.info(
                    "W języku polskim słowa 4-sylabowe stanowią rzeczywistą barierę percepcyjną (w przeciwieństwie "
                    "do języka angielskiego, gdzie tradycyjnie liczy się słowa 3-sylabowe). "
                    "Formuła: W = (Słowa / Zdania) + (Trudne słowa 4+ / Słowa) * 100."
                )
        else:
            st.info(f"Tekst zidentyfikowano jako język **{report.language.upper()}**. Indeks Pisarka dotyczy języka polskiego.")

    with tab2:
        st.subheader("🌍 International Readability Benchmarks")
        r_cols = st.columns(4)
        with r_cols[0]:
            st.metric("Flesch Reading Ease", report.readability.flesch_reading_ease)
        with r_cols[1]:
            st.metric("Gunning Fog Index", report.readability.gunning_fog)
        with r_cols[2]:
            st.metric("Flesch-Kincaid Grade", report.readability.flesch_kincaid_grade)
        with r_cols[3]:
            st.metric("Automated Readability (ARI)", report.readability.automated_readability_index)

    with tab3:
        st.subheader("📚 Lexical Diversity & Vocabulary Richness")
        l_cols = st.columns(4)
        with l_cols[0]:
            st.metric("Type-Token Ratio (TTR)", report.lexical_diversity.type_token_ratio)
        with l_cols[1]:
            st.metric("Root TTR (Guiraud)", report.lexical_diversity.root_ttr)
        with l_cols[2]:
            st.metric("Hapax Legomena Ratio", report.lexical_diversity.hapax_ratio)
        with l_cols[3]:
            st.metric("Lexical Density", report.lexical_diversity.lexical_density)

        st.caption("TTR mierzy unikalność słownictwa (0-1). Gęstość leksykalna określa stosunek słów niosących treść do słów posiłkowych (stopwords).")

    with tab4:
        st.subheader("💡 Automated Recommendations")
        if report.recommendations:
            for rec in report.recommendations:
                st.warning(f"⚠️ {rec}")
        else:
            st.success("✅ Tekst spełnia standardy czytelności! Brak zidentyfikowanych barier percepcyjnych.")

    with tab5:
        st.subheader("⚙️ Structured Output (JSON)")
        st.code(report.to_json(), language="json")

else:
    st.info("👆 Wpisz tekst lub wybierz jeden z gotowych przykładów z lewego panelu, aby zobaczyć analizę na żywo.")
