"""Stopword collections and filtering for European languages."""

from __future__ import annotations
from typing import Set, List

# Curated stopword sets for major European languages
STOPWORDS_PL: Set[str] = {
    "a", "aby", "ach", "acz", "aczkolwiek", "aj", "albo", "ale", "ani", "aż",
    "bardziej", "bardzo", "bez", "bo", "bowiem", "by", "byli", "być", "był",
    "była", "było", "były", "będzie", "będą", "cali", "cała", "cały", "ci",
    "ciebie", "cię", "co", "cokolwiek", "coś", "czasami", "czasem", "czemu",
    "czy", "czyli", "daleko", "dla", "dlaczego", "dlatego", "do", "dobrze",
    "dokąd", "dość", "dużo", "dwa", "dwaj", "dwie", "dwoje", "dziś", "dzisiaj",
    "gdy", "gdyby", "gdyż", "gdzie", "gdziekolwiek", "gdzieś", "go", "godzina",
    "i", "ich", "ile", "im", "inna", "inne", "inny", "innych", "iż", "ja",
    "ją", "jak", "jakaś", "jakby", "jaki", "jakichś", "jakie", "jakiś", "jakiż",
    "jakkolwiek", "jako", "jakoś", "je", "jeden", "jedna", "jednak", "jednakże",
    "jedno", "jego", "jej", "jemu", "jest", "jestem", "jeszcze", "jeśli", "jeżeli",
    "już", "ją", "każdy", "kiedy", "kilka", "kimś", "kto", "ktokolwiek", "ktoś",
    "która", "które", "którego", "której", "który", "których", "którym", "którzy",
    "ku", "lat", "lecz", "lub", "ma", "mają", "mam", "mamy", "mało", "mniej",
    "mi", "mimo", "może", "mogą", "moi", "moim", "moich", "moja", "moje", "może",
    "możliwe", "można", "mój", "mu", "musi", "my", "na", "nad", "nam", "nami",
    "nas", "nasi", "nasz", "nasza", "nasze", "naszego", "naszych", "natomiast",
    "nawet", "nic", "nich", "nie", "niech", "niego", "niej", "niemu", "nigdy",
    "nim", "nimi", "niż", "no", "o", "obok", "od", "około", "on", "ona", "one",
    "oni", "ono", "oraz", "oto", "owszem", "pan", "pana", "pani", "po", "pod",
    "podczas", "pomimo", "ponad", "ponieważ", "powinien", "powinna", "powinny",
    "poza", "prawie", "przecież", "przed", "przede", "przedtem", "przez", "przy",
    "roku", "również", "sam", "sama", "są", "się", "skąd", "sobie", "sobą",
    "sposób", "swoje", "ta", "tak", "taki", "takie", "także", "tam", "te",
    "tego", "tej", "ten", "teraz", "też", "to", "tobie", "tobą", "toteż", "totobą",
    "trzeba", "tu", "tutaj", "twoi", "twoim", "twoja", "twoje", "twój", "twym",
    "tych", "tylko", "tym", "u", "w", "wam", "wami", "was", "wasz", "wasza",
    "wasze", "we", "według", "wiele", "wielu", "więc", "więcej", "wszyscy",
    "wszystkich", "wszystkie", "wszystkim", "wszystko", "wtedy", "wy", "właśnie",
    "z", "za", "zapewne", "zawsze", "ze", "zł", "znowu", "znów", "został",
    "żaden", "żadna", "żadne", "żadnych", "że", "żeby"
}

STOPWORDS_EN: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it",
    "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my",
    "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
    "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same",
    "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so",
    "some", "such", "than", "that", "that's", "the", "their", "theirs", "them",
    "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll",
    "they're", "they've", "this", "those", "through", "to", "too", "under", "until",
    "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've",
    "were", "weren't", "what", "what's", "when", "when's", "where", "where's",
    "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't",
    "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your",
    "yours", "yourself", "yourselves"
}

STOPWORDS_DE: Set[str] = {
    "aber", "alle", "allem", "allen", "aller", "alles", "als", "also", "am", "an",
    "ander", "andere", "anderem", "anderen", "anderer", "anderes", "anderm", "andern",
    "anderr", "anders", "auch", "auf", "aus", "bei", "bin", "bis", "bist", "da",
    "damit", "dann", "der", "den", "des", "dem", "die", "das", "dass", "daß",
    "derselbe", "derselben", "denselben", "desselben", "demselben", "dieselbe",
    "dieselben", "dasselbe", "dazu", "dein", "deine", "deinem", "deinen", "deiner",
    "deines", "denn", "derer", "dessen", "dich", "dir", "du", "dies", "diese",
    "diesem", "diesen", "dieser", "dieses", "doch", "dort", "durch", "ein", "eine",
    "einem", "einen", "einer", "eines", "einig", "einige", "einigem", "einigen",
    "einiger", "einiges", "einmal", "er", "ihn", "ihm", "es", "etwas", "euer",
    "eure", "eurem", "euren", "eurer", "eures", "für", "gegen", "gewesen", "hab",
    "habe", "haben", "hat", "hatte", "hatten", "hier", "hin", "hinter", "ich",
    "mich", "mir", "ihr", "ihre", "ihrem", "ihren", "ihrer", "ihres", "euch",
    "im", "in", "indem", "ins", "ist", "jede", "jedem", "jeden", "jeder", "jedes",
    "jene", "jenem", "jenen", "jener", "jenes", "jetzt", "kann", "kein", "keine",
    "keinem", "keinen", "keiner", "keines", "können", "könnte", "machen", "man",
    "manche", "manchem", "manchen", "mancher", "manches", "mein", "meine", "meinem",
    "meinen", "meiner", "meines", "mit", "muss", "musste", "nach", "nicht", "nichts",
    "noch", "nun", "nur", "oder", "ohne", "sehr", "sein", "seine", "seinem", "seinen",
    "seiner", "seines", "selbst", "sich", "sie", "sind", "so", "solche", "solchem",
    "solchen", "solcher", "solches", "soll", "sollte", "sondern", "sonst", "über",
    "um", "und", "uns", "unser", "unsere", "unserem", "unseren", "unserer", "unseres",
    "unter", "viel", "vom", "von", "vor", "während", "war", "waren", "warst", "was",
    "weg", "weil", "weiter", "welche", "welchem", "welchen", "welcher", "welches",
    "wenn", "werde", "werden", "wie", "wieder", "will", "wir", "wird", "wirst", "wo",
    "wollen", "wollte", "würde", "würden", "zu", "zum", "zur", "zwar", "zwischen"
}

STOPWORDS_FR: Set[str] = {
    "au", "aux", "avec", "ce", "ces", "dans", "de", "des", "du", "elle", "en",
    "et", "eux", "il", "ils", "je", "la", "le", "les", "leur", "lui", "mais",
    "me", "même", "mes", "moi", "mon", "ne", "nos", "notre", "nous", "on", "ou",
    "par", "pas", "pour", "qu", "que", "qui", "sa", "se", "ses", "son", "sur",
    "ta", "te", "tes", "toi", "ton", "tu", "un", "une", "vos", "votre", "vous",
    "c", "d", "j", "l", "à", "m", "t", "y", "été", "étée", "étées", "étés",
    "étant", "étante", "étants", "étantes", "suis", "es", "est", "sommes", "êtes",
    "sont", "serai", "seras", "sera", "serons", "serez", "seront", "serais", "serait"
}

STOPWORDS_ES: Set[str] = {
    "de", "la", "que", "el", "en", "y", "a", "los", "del", "se", "las", "por",
    "un", "para", "con", "no", "una", "su", "al", "lo", "como", "más", "pero",
    "sus", "le", "ya", "o", "este", "sí", "porque", "esta", "entre", "cuando",
    "muy", "sin", "sobre", "también", "me", "hasta", "hay", "donde", "quien",
    "desde", "todo", "nos", "durante", "todos", "uno", "les", "ni", "contra",
    "otros", "ese", "eso", "ante", "ellos", "e", "esto", "mí", "antes", "algunos"
}

STOPWORDS_BY_LANG = {
    "pl": STOPWORDS_PL,
    "en": STOPWORDS_EN,
    "de": STOPWORDS_DE,
    "fr": STOPWORDS_FR,
    "es": STOPWORDS_ES,
}


def get_stopwords(lang: str = "pl") -> Set[str]:
    """Retrieve stopword set for the given language.

    Args:
        lang: ISO 639-1 language code ('pl', 'en', 'de', 'fr', 'es').

    Returns:
        Set of stopword strings in lowercase.
    """
    return STOPWORDS_BY_LANG.get(lang.lower(), STOPWORDS_EN)


def remove_stopwords(words: List[str], lang: str = "pl") -> List[str]:
    """Filter out stopwords from a list of tokens.

    Args:
        words: List of word tokens.
        lang: Target language code.

    Returns:
        Filtered list with stopwords removed.
    """
    stops = get_stopwords(lang)
    return [w for w in words if w.lower() not in stops]
