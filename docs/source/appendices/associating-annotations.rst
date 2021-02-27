.. _associating-annotations:

Associating Annotations with VRS Objects
========================================

This example demonstrates how to associate information with VRS
objects.  Although the examples use the |vrs-python| library, the
principles apply regardless of implementation.

Information is never embedded within VRS objects. Instead, it is
associated with those objects by means of their ids. This approach to
annotations scales better in size and distributes better across multiple
data sources.

.. code:: ipython3

    import collections
    from ga4gh.vrs import ga4gh_identify, models
    from ga4gh.vrs.dataproxy import SeqRepoRESTDataProxy
    from ga4gh.vrs.extras.translator import Translator
    
    # Requires seqrepo REST interface is running on this URL (e.g., using docker image)
    seqrepo_rest_service_url = "http://localhost:5000/seqrepo"
    dp = SeqRepoRESTDataProxy(base_url=seqrepo_rest_service_url)
    
    tlr = Translator(data_proxy=dp)

.. code:: ipython3

    # Declare some data as human-readable RS id labels with HGVS expressions
    data = (
        ("rs7412C",   "NC_000019.10:g.44908822="),
        ("rs7412T",   "NC_000019.10:g.44908822C>T"),
        ("rs429358C", "NC_000019.10:g.44908684="),
        ("rs429358T", "NC_000019.10:g.44908684T>C")
    )

.. code:: ipython3

    # Parse the HGVS expressions and generate three dicts:
    # alleles[allele_id] ⇒ allele object
    # rs_names[allele_id] ⇒ rs label
    # hgvs_name[allele_id] ⇒ original hgvs expression
    
    # For convenience, also build
    # rs_to_id[rs_name] ⇒ allele_id
    
    alleles = {}
    rs_names = {}
    hgvs_names = collections.defaultdict(lambda: dict())
    for rs, hgvs_expr in data:
        allele = tlr.from_hgvs(hgvs_expr)
        allele_id = ga4gh_identify(allele)
        alleles[allele_id] = allele
        hgvs_names[allele_id] = hgvs_expr
        rs_names[allele_id] = rs
    
    rs_to_id = {r: i for i, r in rs_names.items()}

.. code:: ipython3

    # Now, build a new set of annotations: allele frequencies
    # This is more complicated because it maps to a map of frequences
    # It should be clear that other frequencies could be easily added here
    # or as a separate data source
    freqs = {
        "gnomad": {
            "global": {
                rs_to_id["rs7412C"]: 0.9385,
                rs_to_id["rs7412T"]: 0.0615,
                rs_to_id["rs429358C"]: 0.1385,
                rs_to_id["rs429358T"]: 0.8615,
            }
        }
    }

.. code:: ipython3

    # It might be convenient to save these data
    # A saved document might have structure like this:
    doc = {
        "alleles": alleles,
        "hgvs_names": hgvs_names,
        "rs_names": rs_names,
        "freqs": freqs
    }

.. code:: ipython3

    # For the benefit of pretty printing, let's replace the allele objects with their dict representations
    doc["alleles"] = {i: a.as_dict() for i, a in doc["alleles"].items()}
    import json
    print(json.dumps(doc, indent=2))


.. parsed-literal::

    {
      "alleles": {
        "ga4gh:VA.UUvQpMYU5x8XXBS-RhBhmipTWe2AALzj": {
          "location": {
            "interval": {
              "end": 44908822,
              "start": 44908821,
              "type": "SimpleInterval"
            },
            "sequence_id": "ga4gh:SQ.IIB53T8CNeJJdUqzn9V_JnRtQadwWCbl",
            "type": "SequenceLocation"
          },
          "state": {
            "sequence": "C",
            "type": "SequenceState"
          },
          "type": "Allele"
        },
        "ga4gh:VA.EgHPXXhULTwoP4-ACfs-YCXaeUQJBjH\_": {
          "location": {
            "interval": {
              "end": 44908822,
              "start": 44908821,
              "type": "SimpleInterval"
            },
            "sequence_id": "ga4gh:SQ.IIB53T8CNeJJdUqzn9V_JnRtQadwWCbl",
            "type": "SequenceLocation"
          },
          "state": {
            "sequence": "T",
            "type": "SequenceState"
          },
          "type": "Allele"
        },
        "ga4gh:VA.LQrGFIOAP8wEAybwNBo8pJ3yIG7tXWoh": {
          "location": {
            "interval": {
              "end": 44908684,
              "start": 44908683,
              "type": "SimpleInterval"
            },
            "sequence_id": "ga4gh:SQ.IIB53T8CNeJJdUqzn9V_JnRtQadwWCbl",
            "type": "SequenceLocation"
          },
          "state": {
            "sequence": "T",
            "type": "SequenceState"
          },
          "type": "Allele"
        },
        "ga4gh:VA.iXjilHZiyCEoD3wVMPMXG3B8BtYfL88H": {
          "location": {
            "interval": {
              "end": 44908684,
              "start": 44908683,
              "type": "SimpleInterval"
            },
            "sequence_id": "ga4gh:SQ.IIB53T8CNeJJdUqzn9V_JnRtQadwWCbl",
            "type": "SequenceLocation"
          },
          "state": {
            "sequence": "C",
            "type": "SequenceState"
          },
          "type": "Allele"
        }
      },
      "hgvs_names": {
        "ga4gh:VA.UUvQpMYU5x8XXBS-RhBhmipTWe2AALzj": "NC_000019.10:g.44908822=",
        "ga4gh:VA.EgHPXXhULTwoP4-ACfs-YCXaeUQJBjH\_": "NC_000019.10:g.44908822C>T",
        "ga4gh:VA.LQrGFIOAP8wEAybwNBo8pJ3yIG7tXWoh": "NC_000019.10:g.44908684=",
        "ga4gh:VA.iXjilHZiyCEoD3wVMPMXG3B8BtYfL88H": "NC_000019.10:g.44908684T>C"
      },
      "rs_names": {
        "ga4gh:VA.UUvQpMYU5x8XXBS-RhBhmipTWe2AALzj": "rs7412C",
        "ga4gh:VA.EgHPXXhULTwoP4-ACfs-YCXaeUQJBjH\_": "rs7412T",
        "ga4gh:VA.LQrGFIOAP8wEAybwNBo8pJ3yIG7tXWoh": "rs429358C",
        "ga4gh:VA.iXjilHZiyCEoD3wVMPMXG3B8BtYfL88H": "rs429358T"
      },
      "freqs": {
        "gnomad": {
          "global": {
            "ga4gh:VA.UUvQpMYU5x8XXBS-RhBhmipTWe2AALzj": 0.9385,
            "ga4gh:VA.EgHPXXhULTwoP4-ACfs-YCXaeUQJBjH\_": 0.0615,
            "ga4gh:VA.LQrGFIOAP8wEAybwNBo8pJ3yIG7tXWoh": 0.1385,
            "ga4gh:VA.iXjilHZiyCEoD3wVMPMXG3B8BtYfL88H": 0.8615
          }
        }
      }
    }

