import os
import re
import pymorphy2
from razdel import sentenize
import pandas as pd

def get_grammar(words, morph):
    c = e = a = n = sg = pl = pr = pst = fut = v = 0
    for word in words:
        parsed = morph.parse(word)[0]
        tag = parsed.tag
        p = str(tag.POS)
        g = str(tag.gender)
        num = str(tag.number)
        t = str(tag.tense)

        if p == 'NOUN':
            n += 1
            if g == 'neut':
                c += 1
            elif g == 'femn':
                e += 1
            elif g == 'masc':
                a += 1
            if num == 'sing':
                sg += 1
            elif num == 'plur':
                pl += 1
        elif p == 'VERB':
            v += 1
            if t == 'pres':
                pr += 1
            elif t == 'past':
                pst += 1
            elif t == 'futr':
                fut += 1
    return c, e, a, n, sg, pl, pr, pst, fut, v

def process_files(folder_path, morph, results):
    for file in os.listdir(folder_path):
        try:
            with open(os.path.join(folder_path, file), 'r', encoding='utf-8') as f:
                text = f.read()
                # делим текст на слова
                words = re.findall(r'[а-яА-ЯёЁa-zA-Z]+', text)
                c, e, a, n, sg, pl, pr, pst, fut, v = get_grammar(words[:200], morph)

                results['text'].append(file[:-4])
                results['nouns'].append(n)
                results['neut'].append(c)
                results['%neut'].append(round(100 / n * c if n > 0 else 0, 2))
                results['femn'].append(c)
                results['%femn'].append(round(100 / n * e if n > 0 else 0, 2))
                results['masc'].append(c)
                results['%masc'].append(round(100 / n * a if n > 0 else 0, 2))
                results['sing'].append(sg)
                results['plur'].append(pl)
                results['verbs'].append(v)
                #results['verb(pres)'].append(pr)
                results['%verb(pres)'].append(round(100 / v * pr if v > 0 else 0, 2))
                #results['verb(past)'].append(pst)
                results['%verb(past)'].append(round(100 / v * pst if v > 0 else 0, 2))
                #results['verb(fut)'].append(fut)
                results['%verb(fut)'].append(round(100 / v * fut if v > 0 else 0, 2))
        except Exception as e:
            print(f"Error processing file {file}: {e}")


def grammar_analysis():
    morph = pymorphy2.MorphAnalyzer()

    # Инициализация структуры для результатов
    results = {
        'text': [], 'nouns': [], 'neut': [], '%neut': [],
        'femn': [], '%femn': [], 'masc': [], '%masc': [],
        'sing': [], 'plur': [], 'verbs': [],
        #'verb(pres)': [], 'verb(past)': [], 'verb(fut)': [],
        '%verb(pres)': [], '%verb(past)': [], '%verb(fut)': []
    }

    # Обработка файлов
    process_files(r'C:\project2025\ScientificStyle\Texts/', morph, results)
    process_files(r'C:\project2025\ProseStyle/', morph, results)

    # Создание DataFrame
    grammar_nouns = pd.DataFrame({
        'text': results['text'],
        'nouns': results['nouns'],
        'neut': results['neut'],
        '%neut': results['%neut'],
        'femn': results['femn'],
        '%femn': results['%femn'],
        'masc': results['masc'],
        '%masc': results['%masc'],
        'sing': results['sing'],
        'plur': results['plur']
    })

    grammar_verbs = pd.DataFrame({
        'text': results['text'],
        'verbs': results['verbs'],
        #'verb(pres)': results['verb(pres)'],
        '%verb(pres)': results['%verb(pres)'],
        #'verb(past)': results['verb(past)'],
        '%verb(past)': results['%verb(past)'],
        #'verb(fut)': results['verb(fut)'],
        '%verb(fut)': results['%verb(fut)']
    })

    print(grammar_nouns)
    print(grammar_verbs)

grammar_analysis()
