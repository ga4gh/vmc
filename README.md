[![DOI](https://zenodo.org/badge/67005248.svg)](https://zenodo.org/badge/latestdoi/67005248)
[![Read the Docs](https://img.shields.io/readthedocs/vr-spec/1.1)](https://vrs.ga4gh.org/)

The [GA4GH](https://www.ga4gh.org/) [Variation Representation
Specification](https://vrs.ga4gh.org/) provides a
comprehensive framework for the computational representation of
biological sequence variation.  VRS is the result of a
collaboration among [contributors](CONTRIBUTORS.md) representing
national information resource providers, major international public
initiatives, and diagnostic testing laboratories.

VRS is licensed under the [Apache License 2.0](LICENSE).


> **NOTE:** VRS is under active development.  See [VR 
> Project Roadmap](https://github.com/orgs/ga4gh/projects/5).


# Specific goals:

* Develop common language- and protocol-neutral information models and
  nomenclature for biological sequence variation.
* From the information models, develop data schemas.  The current
  schema is defined in JSON Schema, but other formats are expected.
* Provide algorithmic guidance and conventions to minimize
  representational ambiguity.
* Define a globally unique *computed identifier* for covered data
  classes.
* Develop [validation
  tests](https://github.com/ga4gh/vrs/tests/validation) to ensure
  consistency of implementations.

The VRS model is the product of the [GA4GH Variation Representation
group](https://ga4gh-gks.github.io/variant_representation.html).


> **SEE ALSO**: See [vrs-python](https://github.com/ga4gh/vrs-python)
> for an implementation and Jupyter notebooks.


# Using the schema

The schema is available in the `schema/` directory, in both yaml and
json versions.  It conforms to JSON Schema draft-07.  For a list of
libraries that support JSON schema, see [JSON
Schema>Implementations](https://json-schema.org/implementations.html).



# Contributing to the schema

VRS uses yaml as the source document for JSON Schema

To convert vrs.yaml to vrs.json:

    make vrs.json

You'll probably have to `pip install pyyaml` first.

To watch for changes and update automatically:

    make -C schema watch &


# Contributing docs

The VR specification documentation is written in reStructuredText and
located in `docs/source/`.  Commits to this repo are built
automatically at `vrs.ga4gh.org`. 

To build documentation locally, type:

    make -C docs clean watch &
	
Then, open `docs/build/html/index.html`.  The above make command
should build docs when source changes. (Some types of changes require
recleaning and building.)
