import re

try:
    import textstat
except ImportError:
    textstat = None


def count_words(text: str) -> int:
    """Retorna o número de palavras no texto."""
    return len(text.split())


def count_sentences(text: str) -> int:
    """Retorna uma estimativa de número de sentenças no texto."""
    # conta pontos finais, interrogações e exclamações
    return len(re.findall(r'[\.\!\?]+', text))


def average_sentence_length(text: str) -> float:
    """Calcula o tamanho médio das sentenças em palavras."""
    sentences = count_sentences(text)
    words = count_words(text)
    return words / sentences if sentences > 0 else 0.0


def estimated_reading_time(text: str, wpm: int = 200) -> float:
    """Tempo de leitura estimado em minutos, com base em WPM (padrão 200)."""
    words = count_words(text)
    return words / wpm


def flesch_reading_ease(text: str) -> float | None:
    """Calcula o índice Flesch Reading Ease se textstat estiver disponível."""
    if textstat:
        try:
            return textstat.flesch_reading_ease(text)
        except Exception:
            return None
    return None


def grammar_error_count(text: str) -> int | None:
    """Retorna número de possíveis erros gramaticais usando language_tool_python, se instalado."""
    try:
        import language_tool_python
        tool = language_tool_python.LanguageTool('pt-BR')
        matches = tool.check(text)
        return len(matches)
    except ImportError:
        return None


def collect_metrics(text: str) -> dict:
    """Retorna um dicionário com as principais métricas do texto."""
    return {
        'words': count_words(text),
        'sentences': count_sentences(text),
        'avg_sentence_length': average_sentence_length(text),
        'reading_time_min': estimated_reading_time(text),
        'flesch_reading_ease': flesch_reading_ease(text),
        'grammar_errors': grammar_error_count(text)
    }
