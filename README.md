# csv-to-skos

Python scripts to create an importable skos rdf file in [TemaTres](https://github.com/tematres/TemaTres-Vocabulary-Server). Notebook and command line version.

They require a csv file of this form as input:

|ID     |Term     |Definition     |BibNote     |SourceIRI     |RelType     |Target     |
|-------|---------|---------------|------------|--------------|------------|-----------|
|Term ID|Term Name|Definition text|BibNote text|IRI           |BT/RT       |Target name|
|-------|---------|---------------|------------|--------------|------------|-----------|
