# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/FacultadInformatica-LinkedData/Curso2022-2023/blob/master/Assignment4/course_materials/notebooks/Task07.ipynb

**Task 07: Querying RDF(s)**
"""

!pip install rdflib 
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"
from rdflib.plugins.sparql import prepareQuery

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/rdf/example6.rdf", format="xml")

"""**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**"""

# TO DO
ns = Namespace("http://somewhere#")
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
  print(s)
# Visualize the results
q1 =  ("""SELECT ?s WHERE{
    ?s (rdfs:subClassOf) ns:Person.
  } """)
for r in g.query(q1):
  print(r)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""

# TO DO
print("RDFLib:")
ns = Namespace("http://somewhere#")
for s, _,_ in g.triples((None, RDF.type, ns.Person)):
  print(s, "is a Person.")
for s, _, _ in g.triples((None, RDFS.subClassOf, ns.Person)):
  for s2, _,_ in g.triples((None, RDF.type, s)):
    print(s2, "is subClassOf", s)

#SPARQL
print("SPARQL:")
q2 = prepareQuery("""
  SELECT DISTINCT ?x
  WHERE{
    {?x rdf:type ns:Person} UNION
	  {
    ?p (rdfs:subClassOf/rdfs:subClassOf*) ns:Person .
    ?x rdf:type ?p
    }
  }
  """,
  initNs = {"rdf": RDF, "rdfs": RDFS, "ns": ns}
)
for j in g.query(q2):
  print(j)
# Visualize the results

"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**

"""

print("RDFLib:")
for s,_,_ in g.triples((None, RDFS.subClassOf, ns.Person)):
  for s2, _, _ in g.triples((None, RDF.type, s)):
    print(s2)
    for s3, p3, _ in g.triples((s2, None, None)):
      print(p3)

for s, _, _ in g.triples((None, RDF.type, ns.Person)):
  print(s)
  for s2, p2, _ in g.triples((s, None, None)):
      print(p2)
print("SPARQL:")
q1 = prepareQuery("""
  SELECT ?s ?p
  WHERE {
    {
      ?s rdf:type ns:Person.
      ?s ?p ?x.
    }
    UNION {
      ?s rdf:type ?y.
      ?y rdfs:subClassOf* ns:Person.
      ?s ?p ?x.
    }
  }
  """,
  initNs = { "rdf": RDF, "rdfs": RDFS, "ns" : ns}
)
# Visualize the results
for j in g.query(q1):
  print(j)
# Visualize the results