#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import datetime
from lxml import etree as ET
import os


# In[ ]:


csv_file = input("Enter the name of the CSV file: ")
csv_separator = input("Enter the CSV separator (comma or semicolon): ")

if not os.path.exists(csv_file):
    print(f"The file {csv_file} does not exist.")
    exit(1)

if csv_separator.lower() == "comma":
    sep = ","
elif csv_separator.lower() == "semicolon":
    sep = ";"
else:
    print("Invalid separator. Please enter either 'comma' or 'semicolon'.")
    exit(1)

df = pd.read_csv(csv_file, sep=sep, index_col=False)

# In[21]:


# Create a lookup dictionary to map term names to IDs
lookup_dict = dict(zip(df['Term'], df['ID']))

# Replace the term names in the 'Target' column with their corresponding IDs
df['Target'] = df['Target'].map(lookup_dict)

# In[23]:


# Define the namespaces
namespaces = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'skos': 'http://www.w3.org/2004/02/skos/core#',
    'map': 'http://www.w3c.rl.ac.uk/2003/11/21-skos-mapping#',
    'dct': 'http://purl.org/dc/terms/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'xml': 'http://www.w3.org/XML/1998/namespace'
}


# In[24]:


# Create an empty XML document with a root element of RDF
root = ET.Element(f"{{{namespaces['rdf']}}}RDF", nsmap=namespaces)


# In[25]:


# Create the ConceptScheme element and add it to the root
concept_scheme = ET.SubElement(root, f"{{{namespaces['skos']}}}ConceptScheme",
                               attrib={f"{{{namespaces['rdf']}}}about": ""})
ET.SubElement(concept_scheme, f"{{{namespaces['dc']}}}title").text = "INSERT_HERE"
ET.SubElement(concept_scheme, f"{{{namespaces['dc']}}}creator").text = "INSERT_HERE"
ET.SubElement(concept_scheme, f"{{{namespaces['dc']}}}contributor")
ET.SubElement(concept_scheme, f"{{{namespaces['dc']}}}publisher")
ET.SubElement(concept_scheme, f"{{{namespaces['dc']}}}rights")
ET.SubElement(concept_scheme, f"{{{namespaces['dc']}}}subject")
ET.SubElement(concept_scheme, f"{{{namespaces['dc']}}}description").text = "<![CDATA[ ]]>"
ET.SubElement(concept_scheme, f"{{{namespaces['dc']}}}date").text = datetime.datetime.now().strftime('%Y-%m-%d')
ET.SubElement(concept_scheme, f"{{{namespaces['dct']}}}modified").text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
ET.SubElement(concept_scheme, f"{{{namespaces['dc']}}}language").text = "en-EN"


# In[26]:


# Create a dictionary to store the relations
relations = {}

# Create a dictionary to store the XML elements for each ID
elements = {}


# In[27]:


# Iterate over the dataframe and create the XML elements
for i, row in df.iterrows():
    # Create a new Concept element
    concept = ET.Element(f"{{{namespaces['skos']}}}Concept",
                         attrib={f"{{{namespaces['rdf']}}}about": f"={int(row['ID'])}"})

    # Add the prefLabel, definition, note, inScheme, created, and exactMatch elements
    if pd.notna(row['Term']):
        ET.SubElement(concept, f"{{{namespaces['skos']}}}prefLabel", attrib={f"{{{namespaces['xml']}}}lang": "en-EN"}).text = row['Term']
    if pd.notna(row['Definition']):
        ET.SubElement(concept, f"{{{namespaces['skos']}}}definition", attrib={f"{{{namespaces['xml']}}}lang": "en-EN"}).text = row['Definition']
    if pd.notna(row['BibNote']):
        ET.SubElement(concept, f"{{{namespaces['skos']}}}note", attrib={f"{{{namespaces['xml']}}}lang": "en-EN"}).text = row['BibNote']
    ET.SubElement(concept, f"{{{namespaces['skos']}}}inScheme", attrib={f"{{{namespaces['rdf']}}}resource": "INSERT_HERE"})
    ET.SubElement(concept, f"{{{namespaces['dct']}}}created").text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if pd.notna(row['SourceIRI']):
        exact_match = ET.SubElement(concept, f"{{{namespaces['skos']}}}exactMatch")
        ET.SubElement(exact_match, f"{{{namespaces['skos']}}}Concept", attrib={f"{{{namespaces['rdf']}}}about": row['SourceIRI']})

    # If there is a relation, add it to the relations dictionary
    if pd.notna(row['RelType']) and pd.notna(row['Target']):
        if row['RelType'] not in relations:
            relations[row['RelType']] = {}
        if row['ID'] not in relations[row['RelType']]:
            relations[row['RelType']][row['ID']] = []
        relations[row['RelType']][row['ID']].append(int(row['Target']))

    # Add the concept to the elements dictionary
    elements[int(row['ID'])] = concept


# In[28]:


# Add the relations to the concepts
for rel_type, ids in relations.items():
    for id, targets in ids.items():
        for target in targets:
            if rel_type == "RT":
                ET.SubElement(elements[id], f"{{{namespaces['skos']}}}related",
                               attrib={f"{{{namespaces['rdf']}}}resource": f"INSERT_HERE={target}"})
                ET.SubElement(elements[target], f"{{{namespaces['skos']}}}related",
                               attrib={f"{{{namespaces['rdf']}}}resource": f"INSERT_HERE={id}"})
            elif rel_type == "BT":
                ET.SubElement(elements[id], f"{{{namespaces['skos']}}}broader",
                               attrib={f"{{{namespaces['rdf']}}}resource": f"INSERT_HERE={target}"})
                ET.SubElement(elements[target], f"{{{namespaces['skos']}}}narrower",
                               attrib={f"{{{namespaces['rdf']}}}resource": f"INSERT_HERE={id}"})


# In[29]:


# Add the concepts to the root
for id, element in elements.items():
    root.append(element)


# In[30]:


# Create an XML string
xml_str = ET.tostring(root, pretty_print=True, encoding="unicode")


# In[31]:


# Write the XML string to a file
with open('output.rdf', 'w') as f:
    f.write(xml_str)
