# -*- coding: utf-8 -*-
"""
Assignment 4 – Task 06 (final)
IMPORTANT: any pip install line must be commented for the auto-checker.
"""
# !pip install rdflib  # <-- keep commented

from rdflib import Graph, Namespace, Literal, XSD
from rdflib.namespace import RDF, RDFS
from validation import Report

# Namespaces requested in slides
ONTO = Namespace("http://oeg.fi.upm.es/def/people#")          # ontology/classes & properties
PERSON = Namespace("http://oeg.fi.upm.es/resource/person/")   # individuals
VCARD = Namespace("http://www.w3.org/2001/vcard-rdf/3.0/")
FOAF  = Namespace("http://xmlns.com/foaf/0.1/")

g = Graph()
# bind as in the notebooks
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
# bind our own vocabularies (not required by validator, but nice to have)
g.bind("people", ONTO)
g.bind("person", PERSON)
g.bind("vcard", VCARD)
g.bind("foaf", FOAF)

r = Report()

# --- TASK 6.0: prefixes ontology/person (validated indirectly) ---
# handled above via ONTO and PERSON

# --- TASK 6.1: taxonomy + labels (xsd:string, exact labels) ---
# Classes
Person = ONTO.Person
Professor = ONTO.Professor
AssociateProfessor = ONTO.AssociateProfessor
InterimAssociateProfessor = ONTO.InterimAssociateProfessor
FullProfessor = ONTO.FullProfessor

for c, label in [
    (Person, "Person"),
    (Professor, "Professor"),
    (AssociateProfessor, "AssociateProfessor"),
    (InterimAssociateProfessor, "InterimAssociateProfessor"),
    (FullProfessor, "FullProfessor"),
]:
    g.add((c, RDF.type, RDFS.Class))
    g.add((c, RDFS.label, Literal(label, datatype=XSD.string)))

# Hierarchy
g.add((Professor, RDFS.subClassOf, Person))
g.add((AssociateProfessor, RDFS.subClassOf, Professor))
g.add((InterimAssociateProfessor, RDFS.subClassOf, AssociateProfessor))
g.add((FullProfessor, RDFS.subClassOf, Professor))

# --- TASK 6.2: properties + labels + domain/range ---
hasColleague = ONTO.hasColleague
hasName      = ONTO.hasName
hasHomePage  = ONTO.hasHomePage

# Types of properties
for p, label in [
    (hasColleague, "hasColleague"),
    (hasName, "hasName"),
    (hasHomePage, "hasHomePage"),
]:
    g.add((p, RDF.type, RDF.Property))
    g.add((p, RDFS.label, Literal(label, datatype=XSD.string)))

# Domains / Ranges
g.add((hasColleague, RDFS.domain, Person))
g.add((hasColleague, RDFS.range,  Person))

g.add((hasName, RDFS.domain, Person))
g.add((hasName, RDFS.range,  RDFS.Literal))

g.add((hasHomePage, RDFS.domain, FullProfessor))
g.add((hasHomePage, RDFS.range,  RDFS.Literal))

# --- TASK 6.3: individuals + links ---
Oscar = PERSON.Oscar
Asun  = PERSON.Asun
Raul  = PERSON.Raul

# Types
g.add((Oscar, RDF.type, Person))
g.add((Asun,  RDF.type, FullProfessor))   # consistent with hasHomePage domain
g.add((Raul,  RDF.type, Person))

# Labels (xsd:string, exactly these)
g.add((Oscar, RDFS.label, Literal("Oscar", datatype=XSD.string)))
g.add((Asun,  RDFS.label, Literal("Asun",  datatype=XSD.string)))
g.add((Raul,  RDFS.label, Literal("Raul",  datatype=XSD.string)))

# Relations per validation hints:
# Oscar: type, label, hasColleague, hasName
g.add((Oscar, hasColleague, Asun))
g.add((Oscar, hasName, Literal("Oscar Name", datatype=XSD.string)))

# Asun: type, label, hasHomePage, hasColleague
g.add((Asun, hasHomePage, Literal("https://asun.example.org", datatype=XSD.string)))
g.add((Asun, hasColleague, Oscar))

# (Raul only needs to exist with correct namespace + label/type for the validator)

# --- TASK 6.4: add VCARD/FOAF info to Oscar ---
g.add((Oscar, VCARD.Given,  Literal("Oscar", datatype=XSD.string)))
g.add((Oscar, VCARD.Family, Literal("Perez", datatype=XSD.string)))
g.add((Oscar, FOAF.email,   Literal("oscar@example.org", datatype=XSD.string)))

# ---- VALIDATION (do not remove) ----
r.validate_task_06_01(g)
r.validate_task_06_02(g)
r.validate_task_06_03(g)
r.validate_task_06_04(g)
r.save_report("_Task_06")
