.. _example:

Example
!!!!!!!

This section provides a complete, language-neutral example of
essential features of VR.  In this example, we will translate an
HGVS-formatted variant, ``NC_000013.11:g.32936732G>C``, into its VR
format and assign a globally unique identifier.

Translate HGVS to VR
@@@@@@@@@@@@@@@@@@@@@

.. sidebar:: **Polymorphism in VR**

   VRS uses polymorphism extensively in order to provide a coherent
   top-down structure for variation while enabling precise models for
   variation data.

   For example, Allele is a kind of Variation, SequenceLocation is a
   kind of Location, and SequenceState is a kind of State.  See
   :ref:`future-plans` for the roadmap of VRS data classes and
   relationships.

   All VRS objects contain a ``type`` attribute, which is used to
   discriminate polymorphic objects.


The `hgvs`_ string ``NC_000013.11:g.32936732G>C`` represents a single
base substitution on the reference sequence `NC_000013.11
<https://www.ncbi.nlm.nih.gov/nuccore/NC_000013.11>`_ (human
chromosome 13, assembly GRCh38) at position 32936732 from the
reference nucleotide ``G`` to ``C``.

In VRS, a contiguous change is represented using an :ref:`allele`
object, which is composed of a :ref:`Location <location>` and of the
:ref:`State <state>` at that location.  Location and State are
abstract concepts: VRS is designed to accommodate many kinds of
Locations based on sequence position, gene names, cytogentic bands, or
other ways of describing locations. Similarly, State may refer to a
specific sequence change, copy number change, or complex sequence
event.

In this example, we will use a :ref:`SequenceLocation`, which is
composed of a sequence identifier and a :ref:`SimpleInterval`.

In VRS, all identifiers are a |CURIE|.  Therefore, NC_000013.11 MUST be
written as the string ``refseq:NC_000013.11`` to make explicit that
this sequence is from `RefSeq
<https://www.ncbi.nlm.nih.gov/refseq/>`__ .  VRS does not restrict
which data sources may be used, but does recommend using prefixes from
`identifiers.org <http://identifiers.org>`_.

VRS uses :ref:`inter-residue-coordinates-design`.  Inter-residue
coordinates *always* use intervals to refer to sequence spans.  For
the purposes of this example, inter-residue coordinates *look* like the
more familiar 0-based, right-open numbering system.  (Please read
about :ref:`inter-residue-coordinates-design` if you are interested in
the significant advantages of this design choice over other coordinate
systems.)

The :ref:`SimpleInterval` for the position ``32936732`` is

.. code-block:: json

    {
      "end": 32936732,
      "start": 32936731,
      "type": "SimpleInterval"
    }

The interval is then 'placed' on a sequence to create the
:ref:`SequenceLocation`:

.. code-block:: json

    {
      "interval": {
        "end": 32936732,
        "start": 32936731,
        "type": "SimpleInterval"
      },
      "sequence_id": "refseq:NC_000013.11",
      "type": "SequenceLocation"
    }

A :ref:`LiteralSequenceExpression` object consists simply of the replacement sequence, as follows:

.. code-block:: json

    {
      "sequence": "C",
      "type": "LiteralSequenceExprssion"
    }

We are now in a position to construct an :ref:`allele` object using
the objects defined above:

.. code-block:: json

    {
      "location": {
        "interval": {
          "end": 32936732,
          "start": 32936731,
          "type": "SimpleInterval"
        },
        "sequence_id": "refseq:NC_000013.11",
        "type": "SequenceLocation"
      },
      "state": {
        "sequence": "C",
        "type": "LiteralSequenceExpression"
      },
      "type": "Allele"
    }


This Allele is a fully-compliant VRS object that is parsable using the
VRS JSON Schema.

.. note:: VRS is verbose! The goal of VRS is to provide a extensible
          framework for representation of sequence variation in
          computers.  VRS objects are readily parsable and have precise
          meaning, but are often larger than other representations and
          are typically less readable by humans.  This tradeoff is
          intentional!



Generate a computed identifer
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

A key feature of VRS is an easily-implemented algorithm to
generate computed, digest-based identifiers for variation objects.
This algorithm permits organizations to generate the same identifier
for the same allele without prior coordination, which in turn
facilitates sharing, obviates centralized registration services, and
enables identifiers to be used in secure settings (such as diagnostic
labs).

Generating a computed identifier requires that all nested objects also
use computed identifiers.  In this example, the sequence identifier
MUST be transformed into a digest-based identifer as described in
:ref:`computed-identifiers`.  In practice, implmentations SHOULD
precompute sequence digests or SHOULD use an existing service that
does so. (See :ref:`required-data` for a description of data that are
needed to implement VR.)  In this case, ``refseq:NC_000013.11`` maps
to ``ga4gh:SQ._0wi-qoDrvram155UmcSC-zA5ZK4fpLT``. All VRS computed
identifiers begin with the ``ga4gh`` prefix and use a type prefix
(``SQ``, here) to denote the type of object.  The VRS sequence
identifier is then substituted directly into the Allele's location
object:

.. code-block:: json

    {
      "location": {
        "interval": {
          "end": 32936732,
          "start": 32936731,
          "type": "SimpleInterval"
        },
        "sequence_id": "ga4gh:SQ._0wi-qoDrvram155UmcSC-zA5ZK4fpLT",
        "type": "SequenceLocation"
      },
      "state": {
        "sequence": "C",
        "type": "SequenceState"
      },
      "type": "Allele"
    }

This, too, is a valid VRS Allele.

.. note:: Using VRS sequence identifiers collapses differences between
	  alleles due to trivial differences in reference naming.  The
	  same variation reported on NC_000013.11, CM000675.2,
	  GRCh38:13, GRCh38.p13:13 would appear to be distinct
	  variation; using a digest identifer will ensure that
	  variation is reported on a single sequence identifier.
	  Furthermore, using digest-based sequence identifiers enables
	  the use of custom reference sequences.


The first step in constructing a computed identifier is to create a
binary digest serialization of the Allele.  Details are provided in
:ref:`computed-identifiers`.  For this example the binary object looks
like:

.. code-block:: python3
		
   '{"location":"v9K0mcjQVugxTDIcdi7GBJ_R6fZ1lsYq","state":{"sequence":"C","type":"SequenceState"},"type":"Allele"}'
   (UTF-8 encoded)

.. important:: The binary serialization is governed by constraints
               that guarantee that different implementations will
               generate the same binary "blob".  Do not confuse binary
               digest serialization with JSON serialization, which is
               used elsewhere with VRS schema.

The GA4GH digest for the above blob is computed using the first 192
bits (24 bytes) of the `SHA-512`_ digest, `base64url`_ encoded.
Conceptually, the function is::

  base64url( sha512( blob )[:24] )

In this example, the value returned is
``n9ax-9x6gOC0OEt73VMYqCBfqfxG1XUH``.

A GA4GH Computed Identifier has the form::

  "ga4gh" ":" <type_prefix> "." <digest>

The ``type_prefix`` for a VRS Allele is ``VA``, which results in the
following computed identifier for our example::

  ga4gh:VA.n9ax-9x6gOC0OEt73VMYqCBfqfxG1XUH


Variation and Location objects contain an OPTIONAL ``_id`` attribute
which implementations may use to store any CURIE-formatted identifier.
*If* an implementation returns a computed identifier with objects, the
object might look like the following:

.. code-block:: json

  {
    "_id": "ga4gh:VA.n9ax-9x6gOC0OEt73VMYqCBfqfxG1XUH",
    "location": {
      "interval": {
        "end": 32936732,
        "start": 32936731,
        "type": "SimpleInterval"
      },
      "sequence_id": "ga4gh:SQ._0wi-qoDrvram155UmcSC-zA5ZK4fpLT",
      "type": "SequenceLocation"
    },
    "state": {
      "sequence": "C",
      "type": "SequenceState"
    },
    "type": "Allele"
  }

This example provides a full VR-compliant Allele with a computed identifier.

.. note:: The ``_id`` attribute is optional.  If it is used, the value
          MUST be a CURIE, but it does NOT need to be a GA4GH Computed
          Identifier.  Applications MAY choose to implement their own
          identifier scheme for private or public use.  For example,
          the above ``_id`` could be a serial number assigned by an
          application, such as ``acmecorp:v0000123``.


What's Next?
@@@@@@@@@@@@

This example has shown a full example for a relatively simple case.
VRS provides a framework that will enable much more complex variation.
Please see :ref:`future-plans` for a discussion of variation classes
that are intened in the near future.

The :ref:`implementations` section lists libraries and packages that
implement VRS.

VRS objects are `value objects
<https://en.wikipedia.org/wiki/Value_object>`__.  An important
consequence of this design choice is that data should be associated
*with* VRS objects via their identifiers rather than embedded *within*
those objects.  The appendix contains an example of :ref:`associating
annotations with variation <associating-annotations>`.
