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
    morphemes = ''.join([token.text.replace(token.lemma_, '') for token in doc])
    return morphemes

def preprocess_manifest(input_manifest_path, output_processed_manifest_path):
    """
    Preprocess the input manifest, lemmatize sentences, and save the processed manifest to a file.
    """
    processed_entries = []
    with open(input_manifest_path, 'r') as f:
        for line in f:
            entry = json.loads(line)
            text = entry['text']
            morphemes = lemmatize(text)
            entry['morphemes'] = morphemes
            processed_entries.append(entry)

    with open(output_processed_manifest_path, 'w', encoding='utf-8') as f:
        for entry in processed_entries:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')


preprocess_manifest("test/test_manifest.json", "test/lemmatize_manifest.json" )