
# -*- coding: utf-8 -*-
"""
Assignment 4 – Task 07 (final)
IMPORTANT: any pip install line must be commented for the auto-checker.
"""
# !pip install rdflib  # <-- keep commented

from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS
from validation import Report

github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2025-2026/master/Assignment4/course_materials"
ns = Namespace("http://somewhere#")

# Do not change these two lines (as in the notebook)
g = Graph()
g.namespace_manager.bind('ns', ns, override=False)
g.parse(github_storage + "/rdf/data06.ttl", format="TTL")

report = Report()

# --- TASK 7.1a (RDFLib): list of tuples (class, superclass or None) ---
classes = set()

# classes used by instances
for _, _, c in g.triples((None, RDF.type, None)):
    classes.add(c)

# classes appearing only as superclass
for c, _, sc in g.triples((None, RDFS.subClassOf, None)):
    classes.add(c)
    classes.add(sc)

result = []
for c in sorted(classes, key=lambda x: str(x)):
    sc = None
    for _, _, scandidate in g.triples((c, RDFS.subClassOf, None)):
        sc = scandidate
        break
    result.append((c, sc))

# Validation 7.1a
report.validate_07_1a(result)

# --- TASK 7.1b (SPARQL) ---
query_71b = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?c ?sc
WHERE {
  { ?i a ?c . }
  OPTIONAL { ?c rdfs:subClassOf ?sc . }
}
"""
report.validate_07_1b(query_71b, g)

# --- TASK 7.2a (RDFLib): individuals of Person including subclasses ---
individuals = []
person = ns.Person

# get subclasses closure
to_visit = [person]
seen = set([person])
while to_visit:
    t = to_visit.pop()
    for ssc, _, sup in g.triples((None, RDFS.subClassOf, t)):
        if ssc not in seen:
            seen.add(ssc)
            to_visit.append(ssc)

# collect instances
all_types = seen
for t in all_types:
    for ind, _, _ in g.triples((None, RDF.type, t)):
        individuals.append(ind)

report.validate_07_02a(individuals)

# --- TASK 7.2b (SPARQL) ---
query_72b = """
PREFIX ns:   <http://somewhere#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?ind
WHERE {
  ?ind a ?t .
  ?t rdfs:subClassOf* ns:Person .
}
"""
report.validate_07_02b(g, query_72b)

# --- TASK 7.3: name and type of those who know Rocky ---
query_73 = """
PREFIX ns:   <http://somewhere#>
SELECT DISTINCT ?name ?type
WHERE {
  ?x ns:knows ns:Rocky .
  ?x ns:name  ?name ;
     a        ?type .
}
"""
report.validate_07_03(g, query_73)

# --- TASK 7.4: colleague has a dog (1 or 2 hops) ---
query_74 = """
PREFIX ns:   <http://somewhere#>
SELECT DISTINCT ?name
WHERE {
  ?x ns:name ?name .
  ?x ns:hasColleague{1,2} ?col .
  ?col ?p ?dog .
  ?dog a ns:Dog .
}
"""
report.validate_07_04(g, query_74)
report.save_report("_Task_07")
