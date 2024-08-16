import spacy
import spacy_spanish_lemmatizer
import json

nlp = spacy.load("es_core_news_sm")
nlp.replace_pipe("lemmatizer", "spanish_lemmatizer")

def lemmatize(text):
    """
    Lemmatize the input text and return the lemmatized text.
    """
    doc = nlp(text)
    lemmatized_tokens = [token.lemma_ for token in doc]
    return lemmatized_tokens

def process_manifest(manifest_path):
    """
    Load a manifest file, lemmatize the "text" column, and save the lemmatized morphemes to a text file.
    """
    with open(manifest_path, "r") as f:
        manifest = [json.loads(line) for line in f]

    with open("manifest_morphemes.txt", "w") as f:
        for item in manifest:
            text = item["text"]
            lemmatized_tokens = lemmatize(text)
            f.write(" ".join(lemmatized_tokens) + "\n")

    return "Lemmatized morphemes saved to 'manifest_morphemes.txt'"

# Example usage
process_manifest("/home/mourb/nemo/test/exp1_manifest.json")