
import json
import re

def count_inflectional_morphemes(text):
    inflectional_morphemes = [
        "o", "es", "e", "emos", "éis", "en",  # Present Indicative
        "é", "aste", "ó", "amos", "asteis", "aron",  # Preterite Indicative
        "aba", "abas", "aba", "ábamos", "abais", "aban",  # Imperfect Indicative
        "ía", "ías", "ía", "íamos", "íais", "ían",  # Conditional
        "é", "ás", "á", "emos", "éis", "án",  # Future
        "e", "es", "e", "emos", "éis", "en",  # Present Subjunctive
        "ara", "aras", "ara", "áramos", "arais", "aran",  # Imperfect Subjunctive (ara)
        "ase", "ases", "ase", "ásemos", "aseis", "asen",  # Imperfect Subjunctive (ase)
        "are", "ares", "are", "áremos", "areis", "aren",  # Future Subjunctive
        "aría", "arías", "aría", "aríamos", "aríais", "arían",  # Conditional Subjunctive
        "me", "te", "se", "nos", "os", "se",  # Reflexive Pronouns
        "me", "te", "lo", "la", "nos", "os", "los", "las",  # Direct Object Pronouns
        "me", "te", "le", "nos", "os", "les",  # Indirect Object Pronouns
        "se", "sela", "selo", "selas", "selos",  # Reflexive and Object Pronouns Combined
        "ase",  # Imperfect Subjunctive ending
        "voseo",  # Use of "vos" instead of "tú" for second person singular
        "os",  # Second person plural direct object pronoun (archaic)
        "ráis",  # Second person plural verb ending (archaic)
        "ierais", "ieras", "ieramos", "ieren",  # Imperfect Subjunctive alternate forms (archaic)
        "iereis", "ieres", "ieremos", "ieren",  # Future Subjunctive alternate forms (archaic)
        "iés",  # Second person singular present subjunctive ending (archaic)
        "abais",  # Second person plural imperfect indicative ending (archaic)
        "ades",  # Second person plural imperative ending (archaic)
        "ades",  # Second person plural imperative ending (archaic)
        "queredes", "ponedles",  # Archaic second person plural imperative forms
        "querrides",  # Archaic second person plural future indicative ending
        "digo", "pongo", "valgo",  # First person singular present indicative irregular verbs
    ]
    pattern = "|".join(inflectional_morphemes)
    matches = re.findall(r'\b\w+(?:{})\b'.format(pattern), text)
    return len(matches)

def sort_sentences(manifest):
    sorted_manifest = sorted(manifest, key=lambda x: count_inflectional_morphemes(x["text"]), reverse=True)
    return sorted_manifest

def filter_manifest(manifest):
    filtered_manifest = [item for item in manifest if count_inflectional_morphemes(item["text"]) >= 10]
    return filtered_manifest

def remove_duplicates_from_manifest(file_path):
    seen_entries = set()
    unique_entries = []

    with open(file_path, "r") as f:
        for line in f:
            entry = json.loads(line)
            # Convert each entry to a hashable tuple to check for duplicates
            entry_tuple = tuple(sorted(entry.items()))
            if entry_tuple not in seen_entries:
                seen_entries.add(entry_tuple)
                unique_entries.append(entry)

    with open(file_path, "w") as f:
        for entry in unique_entries:
            json.dump(entry, f)
            f.write('\n')

# Process JSON file, sort and filter manifest
def process_json_file(input_file_path, output_file_path):
    manifest = []

    # Read input manifest
    with open(input_file_path, "r") as f:
        for line in f:
            item = json.loads(line)
            manifest.append(item)

    # Sort and filter manifest
    sorted_manifest = sort_sentences(manifest)
    filtered_manifest = filter_manifest(sorted_manifest)

    # Write filtered manifest to output file
    with open(output_file_path, "w") as f:
        for item in filtered_manifest:
            json.dump(item, f)
            f.write('\n')

    # Remove duplicates from the output manifest
    remove_duplicates_from_manifest(output_file_path)


process_json_file(input_manifest_path, output_manifest_path)
