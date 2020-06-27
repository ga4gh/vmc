.. _future-plans:

Future Plans
!!!!!!!!!!!!

Overview
@@@@@@@@

VRS covers a fundamental subset of data types to represent
variation, thus far predominantly related to the replacement of a
subsequence in a reference sequence. Increasing its applicability will
require supporting more complex types of variation, including:

* alternative coordinate types such as nested ranges
* feature-based coordinates such as genes, cytogenetic bands, and exons
* copy number variation
* structural variation
* mosaicism and chimerism
* rule-based variation

.. figure:: ../images/schema-future.png

   An illustration of planned components for the VRS Schema.

   Version 1.0 components are colored green. Components that are
   undergoing testing and evaluation and are candidates for the next
   release cycle are colored yellow. Components that are planned but
   still undergoing requirement gathering and initial development are
   colored red. The VRS Schema requires the use of multiple composite
   objects, which are grouped under four abstract classes:
   :ref:`Variation`, :ref:`Location`, :ref:`State`, and
   :ref:`Interval`. These classes and their relationships to the
   representation of Variation are illustrated here. All classes have
   a string type. Dashed borders denote abstract classes. Abstract
   classes are not instantiated. Thin solid borders denote classes
   that may be instantiated but are not identifiable. Bold borders
   denote identifiable objects (i.e., may be serialized and identified
   by computed identifier). Solid arrow lines denoted
   inheritance. Subclasses inherit all attributes from their
   parent. Inherited attributes are not shown.

The following sections provide a preview of planned concepts under way
to address a broader representation of variation.


.. _planned-locations:

Intervals and Locations
@@@@@@@@@@@@@@@@@@@@@@@

VRS uses :ref:`Interval` and :ref:`Location` subclasses to define
where variation occurs.  The schema is designed to be extensible to
new kinds of Intervals and Locations in order to support, for example,
fuzzy coordinates or feature-based locations.


NestedInterval
##############

**Biological definition**

None

**Computational definition**

An :ref:`Interval` comprised of an *inner* and *outer*
:ref:`SimpleInterval`. The *NestedInterval* allows for the definition
of "fuzzy" range endpoints by designating a potentially included
region (the *outer* SimpleInterval) and required included region (the
*inner* SimpleInterval).

**Information model**

.. list-table::
   :class: reece-wrap
   :header-rows: 1
   :align: left
   :widths: auto

   * - Field
     - Type
     - Limits
     - Description
   * - type
     - string
     - 1..1
     - Interval type; MUST be set to '**NestedInterval**'
   * - inner
     - :ref:`SimpleInterval`
     - 1..1
     - known interval
   * - outer
     - :ref:`SimpleInterval`
     - 1..1
     - potential interval

**Implementation guidance**

* Implementations MUST enforce values `0 ≤ outer.start ≤ inner.start ≤
  inner.end ≤ outer.end`. In the case of double-stranded DNA, this
  constraint holds even when a feature is on the complementary strand.



ComplexInterval
###############

**Biological definition**

Representation of complex coordinates based on relative locations or
offsets from a known location. Examples include "left of" a given
position and intronic positions measured from intron-exon junctions.

**Computational definition**

Under development.

**Information model**

Under development.


CytobandLocation
################

**Biological definition**

Imprecise chromosomal locations based on chromosomal staining.

**Computational definition**

Cytogenetic bands are defined by a chromosome name, band, and
sub-band. In VRS, a cytogenetic location is an interval on a
single chromsome with a start and end band and subband.

**Information model**

Under development.


GeneLocation
############

**Biological definition**

The symbolic location of a gene.

**Computational definition**

A gene location is made by reference to a gene identifier from NCBI,
Ensembl, HGNC, or other public trusted authority.

**Information model**

.. list-table::
   :class: reece-wrap
   :header-rows: 1
   :align: left
   :widths: auto

   * - Field
     - Type
     - Limits
     - Description
   * - _id
     - :ref:`CURIE`
     - 0..1
     - Location Id; MUST be unique within document
   * - type
     - string
     - 1..1
     - Location type; MUST be set to '**GeneLocation**'
   * - gene_id
     - :ref:`CURIE`
     - 1..1
     - CURIE-formatted gene identifier using NCBI numeric gene id.

**Notes**

* `gene_id` MUST be specified as a CURIE, using a CURIE prefix of
  `"NCBI"` and CURIE reference with the numeric gene id. Other trusted
  authorities MAY be permitted in future releases.

**Implementation guidance**

* GeneLocations MAY be converted to :ref:`sequence-location` using
  external data. The source of such data and mechanism for
  implementation is not defined by this specification.


.. _planned-states:

State Classes
@@@@@@@@@@@@@

Additional :ref:`State` concepts that are being planned for future
consideration in the specification.


.. _planned-cnvstate:

CNVState
########

.. note:: This concept is being refined. Please comment at https://github.com/ga4gh/vr-spec/issues/46.

**Biological definition**

Variations in the number of copies of a segment of DNA.  Copy number
variations cover copy losses or gains and at known or unknown
locations (including tandem repeats).  Variations MAY occur at precise
SequenceLocations, within nested intervals, or at GeneLocations.
There is no lower or upper bound on CNV sizes.

**Computational definition**

Under development.

**Information model**

.. list-table::
   :class: reece-wrap
   :header-rows: 1
   :align: left
   :widths: auto

   * - Field
     - Type
     - Limits
     - Description
   * - type
     - string
     - 1..1
     - State type; MUST be set to '**CNVState**'
   * - location
     - :ref:`Location`
     - 1..1
     - the Location of the copy ('**null**' if unknown)
   * - min_copies
     - int
     - 1..1
     - The minimum number of copies
   * - max_copies
     - int
     - 1..1
     - The maximum number of copies


.. _planned-variation:

Variation Classes
@@@@@@@@@@@@@@@@@

Additional :ref:`Variation` concepts that are being planned for future
consideration in the specification. See :ref:`Variation` for more
information.


Translocations
##############

.. note:: This concept is being refined. Please comment at https://github.com/ga4gh/vr-spec/issues/103

**Biological definition**

The aberrant joining of two segments of DNA that are not typically
contiguous.  In the context of joining two distinct coding sequences,
translocations result in a gene fusion, which is also covered by this
VRS definition.

**Computational definition**

A joining of two sequences is defined by two :ref:`Location` objects
and an indication of the join "pattern" (advice needed on conventional
terminology, if any).

**Information model**

Under consideration. See https://github.com/ga4gh/vr-spec/issues/28.

**Examples**

t(9;22)(q34;q11) in BCR-ABL


.. _planned-variation-sets:

Rule-based Variation
@@@@@@@@@@@@@@@@@@@@

Some variations are defined by categorical concepts, rather than specific
locations and states. These variations go by many terms, including
*categorical variants*, *bucket variants*, *container variants*, or
*variant classes*. These forms of variation are not described by any
broadly-recognized variation format, but modeling them is a key requirement
for the representation of aggregate variation descriptions as commonly
found in biomedical literature. Our future work will focus on the formal
specification for representing these variations with sets of rules, which
we currently call *Rule-based Variation*.

RuleLocation
############

RuleLocation is a subclass of :ref:`location` intended to capture locations
defined by rules instead of specific contiguous sequences. This includes
locations defined by sequence characteristics, e.g. *microsatellite
regions*.

RuleState
#########

RuleState is a subclass of :ref:`state` intended to capture states defined
by categorical rules instead of sequence states. This includes *gain- /
loss-of-function*, *oncogenic*, and *truncating* variation.

