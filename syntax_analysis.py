from razdel import sentenize
from natasha import Segmenter, NewsEmbedding, NewsSyntaxParser, Doc
import pandas as pd
import os
import re


def syntax_analysis():
    # Инициализация Natasha
    segmenter = Segmenter()
    syntax_parser = NewsSyntaxParser(NewsEmbedding())

    # Папка, содержащая пути к текстам
    folders = [ r'C:\project2025\ScientificStyle\Texts/', r'C:\project2025\ProseStyle/']

    # Подготовка структур для результатов
    results = {
        'text': [],
        'avg_len_simple': [],
        'avg_len_complex': [],
        'personal': [],
        'impersonal': [],
        'intro': [],
        'no_intro': []
    }

    for folder in folders:
        for filename in os.listdir(folder):
            try:
                with open(os.path.join(folder, filename), 'r', encoding='utf-8') as f:
                    text = f.read()

                    # Считаем статистику для файла
                    file_stats = {
                        'complex_count': 0,
                        'simple_count': 0,
                        'complex_words': 0,
                        'simple_words': 0,
                        'personal': 0,
                        'impersonal': 0,
                        'intro': 0,
                        'no_intro': 0
                    }

                    for sent in (s.text for s in sentenize(text)):
                        # Анализируем предложение
                        words = re.findall(r'[а-яА-ЯёЁa-zA-Z]+', sent)
                        doc = Doc(sent)
                        doc.segment(segmenter)
                        doc.parse_syntax(syntax_parser)

                        # Проверка на сложное предложение
                        roots = [t for t in doc.tokens if t.rel == "root"]
                        has_mark = any(t.rel == "mark" for t in doc.tokens)
                        has_conj = any(t.rel == "conj" and t.rel == 'cc' for t in doc.tokens)
                        has_ccomp = any(t.rel == "ccomp" for t in doc.tokens)
                        has_aclrelcl = any(t.rel == "acl:relcl" for t in doc.tokens)

                        is_complex = len(roots) > 1 or has_mark or has_ccomp or has_conj or has_aclrelcl

                        # Обновляем статистику
                        if is_complex:
                            file_stats['complex_count'] += 1
                            file_stats['complex_words'] += len(words)
                        else:
                            file_stats['simple_count'] += 1
                            file_stats['simple_words'] += len(words)

                        # Проверка на личное предложение
                        has_nsubj = any(t.rel in 'nsubj, nsubj:pass, nsubj:outer' for t in doc.tokens)
                        if has_nsubj:
                            file_stats['personal'] += 1
                        else:
                            file_stats['impersonal'] += 1

                        # Проверка на вводные слова
                        if any(t.rel == "parataxis" for t in doc.tokens):
                            file_stats['intro'] += 1
                        else:
                            file_stats['no_intro'] += 1

                    # Сохранение результатов
                    results['text'].append(filename[:-4])
                    results['avg_len_simple'].append(
                        round(file_stats['simple_words'] / file_stats['simple_count'], 2) if file_stats['simple_count'] else 0
                    )
                    results['avg_len_complex'].append(
                        round(file_stats['complex_words'] / file_stats['complex_count'], 2) if file_stats['complex_count'] else 0
                    )
                    results['personal'].append(file_stats['personal'])
                    results['impersonal'].append(file_stats['impersonal'])
                    results['intro'].append(file_stats['intro'])
                    results['no_intro'].append(file_stats['no_intro'])

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # Создание DataFrame
    df_avg = pd.DataFrame({
        'text': results['text'],
        'average length (simple)': results['avg_len_simple'],
        'average length (complex)': results['avg_len_complex']
    })

    df_pers = pd.DataFrame({
        'text': results['text'],
        'personal sent': results['personal'],
        'impersonal sent': results['impersonal']
    })

    df_intro = pd.DataFrame({
        'text': results['text'],
        'intro (+)': results['intro'],
        'intro (-)': results['no_intro']
    })

    print(df_avg)
    print(df_pers)
    print(df_intro)


syntax_analysis()
