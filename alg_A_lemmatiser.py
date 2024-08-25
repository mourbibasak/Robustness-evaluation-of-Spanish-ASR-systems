import spacy
import spacy_spanish_lemmatizer
import json

# Load Spanish model with lemmatizer
nlp = spacy.load("es_core_news_sm")
nlp.replace_pipe("lemmatizer", "spanish_lemmatizer")

def lemmatize(text):
    """
    Lemmatize the input text and return only the morphemes.
    """
    doc = nlp(text)
    print("lemmatizing", doc)
    morphemes = ''.join([token.text.replace(token.lemma_, '') for token in doc])
    return morphemes

def sort_sentences(manifest):
    """
    Sort the manifest based on the length of morphemes in each text.
    """
    sorted_manifest = sorted(manifest, key=lambda x: len(lemmatize(x["text"])), reverse=True)
    return sorted_manifest


def process_manifest(input_manifest_path, output_manifest_path):
    """
    Process the input manifest, lemmatize sentences, sort by morpheme count,
    and create a new manifest with the top 2000 sentences.
    """
    processed_entries = []
    with open(input_manifest_path, 'r') as f:
        for line in f:
            entry = json.loads(line)
            text = entry['text']
            morphemes = lemmatize(text)
            entry['morphemes'] = morphemes
            processed_entries.append(entry)

    # Sort entries based on morpheme count
    sorted_entries = sort_sentences(processed_entries)
    # sorted_entries = sorted(processed_entries, key=lambda x: len(x['morphemes']), reverse=True)

    # Take top 2000 sentences
    top_2000_entries = sorted_entries[:2000]

    # Write the top 2000 entries to the output manifest
    with open(output_manifest_path, 'w', encoding='utf-8') as f:
        print("writing")
        for entry in top_2000_entries:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')

# Example usage:
input_manifest_path = "test/outofdomain_manifest.json"
output_manifest_path = "/home/mourb/nemo/test/exp4_manifest.json"
process_manifest(input_manifest_path, output_manifest_path)
