# csv-to-skos

Python scripts to create an importable skos rdf file in [TemaTres](https://github.com/tematres/TemaTres-Vocabulary-Server). Notebook and command line version.

They require a csv file of this form as input:

|ID     |Term     |Definition     |BibNote     |SourceIRI     |RelType     |Target     |
|-------|---------|---------------|------------|--------------|------------|-----------|
|Term ID|Term Name|Definition text|BibNote text|IRI           |BT/RT       |Target name|

Before use, edit the fields related to your folder structure for your instance of TemaTres. In the code, edit where `INSERT_HERE` appears.
You can verify these fields by inspecting the skos metadata of a term created in TemaTres UI.
