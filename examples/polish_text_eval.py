"""Example: Evaluating Polish text readability with the Pisarek Index."""

from writegenius import analyze_text, calculate_pisarek_index

def main():
    polish_sample = (
        "Zgodnie z art. 299 Kodeksu spółek handlowych, członkowie zarządu "
        "odpowiadają solidarnie za zobowiązania spółki, jeżeli egzekucja "
        "przeciwko spółce okaże się bezskuteczna. Właściwa diagnoza stanu "
        "niewypłacalności oraz terminowe złożenie wniosku restrukturyzacyjnego "
        "stanowią kluczowe przesłanki egzoneracyjne chroniące prywatny majątek."
    )

    print("--- 1. Polish Pisarek Readability Assessment ---")
    pisarek = calculate_pisarek_index(polish_sample)
    print(f"Indeks Pisarka (W):        {pisarek.pisarek_index}")
    print(f"Poziom trudności:          {pisarek.pisarek_difficulty_level}")
    print(f"Sugerowany odbiorca:       {pisarek.pisarek_target_audience}")
    print(f"Odsetek trudnych słów 4+:  {pisarek.hard_words_ratio_percent}%")
    print(f"Adaptowany wskaźnik FOG:   {pisarek.fog_polish}")

    print("\n--- 2. Full Unified Report ---")
    report = analyze_text(polish_sample, lang="pl")
    print(report.summary())

if __name__ == "__main__":
    main()
