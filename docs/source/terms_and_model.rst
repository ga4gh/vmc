Terminology & Information Model
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

When biologists define terms in order to describe phenomena and
observations, they rely on a background of human experience and
intelligence for interpretation. Definitions may be abstract, perhaps
correctly reflecting uncertainty of our understanding at the
time. Unfortunately, such terms are not readily translatable into an
unambiguous representation of knowledge.

For example, "allele" might refer to "an alternative form of a gene or
locus" [`Wikipedia`_], "one of two or more forms of the DNA sequence
of a particular gene" [`ISOGG`_], or "one of a set of coexisting
sequence alleles of a gene" [`Sequence Ontology`_]. Even for human
interpretation, these definitions are inconsistent: does the
definition precisely describe a specific change on a specific
sequence, or, rather, a more general change on an undefined sequence?
In addition, all three definitions are inconsistent with the practical
need for a way to describe sequence changes outside regions associated
with genes.

**The computational representation of biological concepts requires
translating precise biological definitions into data structures that
can be used by implementers.** This translation should result in a
representation of information that is consistent with conventional
biological understanding and, ideally, be able to accommodate future
data as well. The resulting *computational representation* of
information should also be cognizant of computational performance, the
minimization of opportunities for misunderstanding, and ease of
manipulating and transforming data.

Accordingly, for each term we define below, we begin by describing the
term as used by biologists (**biological definition**) as
available. When a term has multiple biological definitions, we
explicitly choose one of them for the purposes of this
specification. We then provide a computer modelling definition
(**computational definition**) that reformulates the biological
definition in terms of information content. We then translate each of
these computational definitions into precise specifications for the
(**logical model**). Terms are ordered "bottom-up" so that definitions
depend only on previously-defined terms.

.. note:: The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL
          NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and
          "OPTIONAL" in this document are to be interpreted as
          described in `RFC 2119`_.


Data Model Notes and Principles
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

* VRS uses `snake_case
  <https://simple.wikipedia.org/wiki/Snake_case>`__ to represent
  compound words.  Although the schema is currently JSON-based (which
  would typically use camelCase), VRS itself is intended to be neutral
  with respect to languages and database.

* VRS objects are `value objects
  <https://en.wikipedia.org/wiki/Value_object>`__.  Two objects are
  considered equal if and only if their respective attributes are
  equal.  As value objects, VRS objects are used as primitive types and
  SHOULD NOT be used as containers for related data.  Instead, related
  data should be associated with VRS objects through identifiers.  See
  :ref:`computed-identifiers`.

* Error handling is intentionally unspecified and delegated to
  implementation.  VRS provides foundational data types that
  enable significant flexibility.  Except where required by this
  specification, implementations may choose whether and how to
  validate data.  For example, implementations MAY choose to validate
  that particular combinations of objects are compatible, but such
  validation is not required.

* We recognize that a common desire may be to have human-readable
  identifiers associated with VRS objects. We recommend using the _id
  field (see :ref:`optional-attributes` below) to create a lookup for
  any such identifiers (see :ref:`example usage
  <associating-annotations>`), and provide reference methods for
  creating VRS identifiers from other common variant formats (see the
  :ref:`HGVS translation example <example>`).


.. _optional-attributes:

Optional Attributes
@@@@@@@@@@@@@@@@@@@

* VRS attributes use a leading underscore to represent optional
  attributes that are not part of the value object.  Such attributes
  are not considered when evaluating equality or creating computed
  identifiers. Currently, the only such attribute in the specification
  is the `_id` attribute.

* The `_id` attribute is available to identifiable objects, and MAY be
  used by an implementation to store the identifier for a VRS object.
  If used, the stored `_id` element MUST be a :ref:`curie`. If used for
  creating a :ref:`truncated-digest` for parent objects, the stored
  element must be a :ref:`GA4GH Computed Identifier <identify>`.


Primitive Concepts
@@@@@@@@@@@@@@@@@@


.. _curie:

CURIE
#####

**Biological definition**

None.

**Computational definition**

A `CURIE <https://www.w3.org/TR/curie/>`__ formatted string.  A CURIE
string has the structure ``prefix``:``reference`` (W3C Terminology).
 
**Implementation guidance**

* All identifiers in VRS MUST be a valid |curie|, regardless of
  whether the identifier refers to GA4GH VRS objects or external data.
* For GA4GH VRS objects, this specification RECOMMENDS using globally
  unique :ref:`computed-identifiers` for use within *and* between
  systems.
* For external data, CURIE-formatted identifiers MUST be used.  When
  an appropriate namespace exists at `identifiers.org
  <http://identifiers.org/>`__, that namespace MUST be used.  When an
  appropriate namespace does not exist at `identifiers.org
  <http://identifiers.org/>`__, support is implementation-dependent.
  That is, implementations MAY choose whether and how to support
  informal or local namespaces.
* Implemantions MUST use CURIE identifiers verbatim and MUST NOT be
  modified in any way (e.g., case-folding).  Implementations MUST NOT
  expose partial (parsed) identifiers to any client.

**Example**

Identifiers for GRCh38 chromosome 19::

    ga4gh:SQ.IIB53T8CNeJJdUqzn9V_JnRtQadwWCbl
    refseq:NC_000019.10
    grch38:19

See :ref:`identify` for examples of CURIE-based identifiers for VR
objects.


.. _residue:

Residue
#######

**Biological definition**

A residue refers to a specific `monomer`_ within the `polymeric
chain`_ of a `protein`_ or `nucleic acid`_ (Source: `Wikipedia Residue
page`_).

**Computational definition**

A character representing a specific residue (i.e., molecular species)
or groupings of these ("ambiguity codes"), using `one-letter IUPAC
abbreviations <https://www.genome.jp/kegg/catalog/codes1.html>`_ for
nucleic acids and amino acids.


.. _sequence:

Sequence
########

**Biological definition**

A contiguous, linear polymer of nucleic acid or amino acid residues.

**Computational definition**

A character string of :ref:`Residues <Residue>` that represents a
biological sequence using the conventional sequence order (5'-to-3'
for nucleic acid sequences, and amino-to-carboxyl for amino acid
sequences). IUPAC ambiguity codes are permitted in Sequences.

**Information model**

A Sequence is a string, constrained to contain only characters representing IUPAC nucleic acid or
amino acid codes.

**Implementation guidance**

* Sequences MAY be empty (zero-length) strings. Empty sequences are used as the
  replacement Sequence for deletion Alleles.
* Sequences MUST consist of only uppercase IUPAC abbreviations, including ambiguity codes.
* A Sequence provides a stable coordinate system by which an :ref:`Allele` MAY be located and
  interpreted.
* A Sequence MAY have several roles. A “reference sequence” is any Sequence used
  to define an :ref:`Allele`. A Sequence that replaces another Sequence is
  called a “replacement sequence”.
* In some contexts outside VRS, “reference sequence” may refer
  to a member of set of sequences that comprise a genome assembly. In the VR
  specification, any sequence may be a “reference sequence”, including those in
  a genome assembly.
* For the purposes of representing sequence variation, it is not
  necessary that Sequences be explicitly “typed” (i.e., DNA, RNA, or
  AA).



Non-variation classes
@@@@@@@@@@@@@@@@@@@@@@

.. _interval:

Interval (Abstract Class)
#########################

**Biological definition**

None.

**Computational definition**

The *Interval* abstract class defines a range on a :ref:`sequence`,
possibly with length zero, and specified using
:ref:`interbase-coordinates-design`. An Interval MAY be a
:ref:`SimpleInterval` with a single start and end coordinate.
:ref:`Future Location and Interval types <planned-locations>` will
enable other methods for describing where :ref:`variation` occurs. Any
of these MAY be used as the Interval for Location.

.. sidebar:: VRS Uses Interbase Coordinates

   **GA4GH VRS uses interbase coordinates when referring to spans of
   sequence.**

   Interbase coordinates refer to the zero-width points before and
   after :ref:`residues <Residue>`. An interval of interbase
   coordinates permits referring to any span, including an empty span,
   before, within, or after a sequence. See
   :ref:`interbase-coordinates-design` for more details on this design
   choice.  Interbase coordinates are always zero-based.


.. _SimpleInterval:

SimpleInterval
$$$$$$$$$$$$$$

**Computational definition**

An :ref:`Interval` with a single start and end coordinate.

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
     - Interval type; MUST be set to '**SimpleInterval**'
   * - start
     - uint64
     - 1..1
     - start position
   * - end
     - uint64
     - 1..1
     - end position

**Implementation guidance**

* Implementations MUST enforce values 0 ≤ start ≤ end. In the case of
  double-stranded DNA, this constraint holds even when a feature is on
  the complementary strand.
* VRS uses Interbase coordinates because they provide conceptual
  consistency that is not possible with residue-based systems (see
  :ref:`rationale <interbase-coordinates-design>`). Implementations
  will need to convert between interbase and 1-based inclusive
  residue coordinates familiar to most human users.
* Interbase coordinates start at 0 (zero).
* The length of an interval is *end - start*.
* An interval in which start == end is a zero width point between two residues.
* An interval of length == 1 MAY be colloquially referred to as a position.
* Two intervals are *equal* if the their start and end coordinates are equal.
* Two intervals *intersect* if the start or end coordinate of one is
  strictly between the start and end coordinates of the other. That
  is, if:

   * b.start < a.start < b.end OR
   * b.start < a.end < b.end OR
   * a.start < b.start < a.end OR
   * a.start < b.end < a.end
* Two intervals a and b *coincide* if they intersect or if they are
  equal (the equality condition is REQUIRED to handle the case of two
  identical zero-width Intervals).
* <start, end>=<*0,0*> refers to the point with width zero before the first residue.
* <start, end>=<*i,i+1*> refers to the *i+1th* (1-based) residue.
* <start, end>=<*N,N*> refers to the position after the last residue for Sequence of length *N*.
* See example notebooks in |vr-python|.

**Example**

.. parsed-literal::

    {
      "end": 44908822,
      "start": 44908821,
      "type": "SimpleInterval"
    }

.. _location:

Location (Abstract Class)
#########################

**Biological definition**

As used by biologists, the precision of “location” (or “locus”) varies
widely, ranging from precise start and end numerical coordinates
defining a Location, to bounded regions of a sequence, to conceptual
references to named genomic features (e.g., chromosomal bands, genes,
exons) as proxies for the Locations on an implied reference sequence.

**Computational definition**

The `Location` abstract class refers to position of a contiguous
segment of a biological sequence.  The most common and concrete
Location is a :ref:`sequence-location`, i.e., a Location based on a
named sequence and an Interval on that sequence. Additional
:ref:`planned-locations` may also be conceptual or symbolic locations,
such as a cytoband region or a gene. Any of these may be used as the
Location for Variation.

**Implementation Guidance**

* Location refers to a position.  Although it MAY imply a sequence,
  the two concepts are not interchangable, especially when the
  location is non-specific (e.g., a range) or symbolic (a gene).


.. _cytoband_location:

CytobandLocation
$$$$$$$$$$$$$$$$

**Biological definition**

Cytobands (cytological bands) are patterns observed on metahphase
chromosomes after staining with dye. 

**Computational definition**

A CytobandLocation is a :ref:`Location` that is defined by a named
chromosomal band within a species.  Conceptually, a CytobandLocation
represents a family of :ref:`SequenceLocations` within a species.

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
     - Location type; MUST be set to **'CytobandLocation'**
   * - species
     - :ref:`CURIE`
     - 1..1
     - An external reference to a species taxonomy.  See Implementation Guidance, below.
   * - chromsome
     - string
     - 1..1
     - The symbolic chromosome name
   * - start
     - string
     - 1..1
     - The chromosmal band name of the start
   * - end
     - string
     - 0..1
     - The end chromosomal band name; if null, end is presumed to equal `start`.


**Implementation guidance**

* CytobandLocation is intended to enable the representation of
  cytogenetic results from karyotyping or low-resolution molecular
  methods.  Precise :ref:`SequenceLocations` should be preferred when
  known.
* `species` is specified using the NCBI taxonomy.  The CURIE prefix
  MUST be `taxonomy`, corresponding to the `NCBI taxonomy prefix at
  identifiers.org
  <https://registry.identifiers.org/registry/taxonomy>`__.
* Valid values for, and syntactic structure of, `chromosome`, `start`,
  and `end` depend on the species.  Therefore, VRS does not constrain
  these values in the model, except for the guidelines below.
* `chromosome` MUST be an official primary name from `NCBI Assembly
  <https://www.ncbi.nlm.nih.gov/assembly>`__.  For Humans, valid
  chromosome names are 1..22, X, Y.
* `start` and `end` SHOULD be values that are conventional for the
  species. For Humans, bands are denoted by the arm (`p` or `q`) and
  position (e.g., `22` or `22.3`). See example.
* When `end` is provided, `CytobandLocation` is effectively a
  contiguous interval of cytobands. There is no distinct class for
  cytoband intervals.
* Prescribing the conversion of CytobandLocations to SequenceLocations
  is out-of-scope for VRS.  Recommended data for this operation are
  available at `https://ftp.ncbi.nlm.nih.gov/pub/gdp/`__ and
  `genome.ucsc.edu`__.


**Example**

.. parsed-literal::

   {
     'chr': '11',
     'end': 'q22.3',
     'species': 'taxonomy:9606',
     'start': 'q22.2',
     'type': 'CytobandLocation'
   }


.. _gene_location:

GeneLocation
$$$$$$$$$$$$$$$$

**Biological definition**

A gene is a conceptual chromosomal region that is associated with 
a biological function or trait. A GeneLocation is a Location within a gene,
defined by regions such as a functional domain or exons, up to and
including the entire gene.

**Computational definition**

GeneLocation is a proxy for a reference to a gene feature defined by
an external organization.

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
     - Location type; MUST be set to **`GeneLocation`**
   * - gene
     - :ref:`CURIE`
     - 1..1
     - An id mapping to the :ref:`computed-identifiers` of the
       external database Sequence containing the sequence to be
       located.

**Implementation guidance**

* The intention of GeneLocation is to represent the conceptual
  location of a named gene.  A GeneLocation may be thought of as
  representing a family of precise :ref:`SequenceLocations` on
  distinct sequences.
* Implements MUST NOT use a gene symbol (e.g., "BRCA1") to define a
  GeneLocation.
* Implementations SHOULD use one of the following namespaces:
  `ncbigene <https://registry.identifiers.org/registry/ncbigene>`__,
  `hgnc <https://registry.identifiers.org/registry/hgnc>`__,
  `vgnc <https://registry.identifiers.org/registry/vgnc>`__,
  `mgi <https://registry.identifiers.org/registry/mgi>`__,  
  `ensembl <https://registry.identifiers.org/registry/ensembl>`__.
  Other namespaces may be used as necessary.
* A gene is specific to a species.  Gene orthologs have distinct
  records in the recommended databases.  For example, the BRCA1 gene
  in humans and the Brca1 gene in mouse are orthologs and have
  distinct records in the previously recommended gene databases.


**Example**

The following examples all refer to the Human BRCA1 gene:

.. parsed-literal::

   {
     'gene': 'ncbigene:672',
     'type': 'GeneLocation'
   }

   {
     'gene': 'hgnc:1100',
     'type': 'GeneLocation'
   }

   {
     'gene': 'ensembl:ENSG00000012048',
     'type': 'GeneLocation'
   }

   
.. _sequence-location:

SequenceLocation
$$$$$$$$$$$$$$$$

**Biological definition**

A specified subsequence within another sequence that is used as a reference sequence.

**Computational definition**

A Location subclass for describing a defined :ref:`Interval` on a
named :ref:`Sequence`.

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
     - Location type; MUST be set to '**SequenceLocation**'
   * - sequence_id
     - :ref:`CURIE`
     - 1..1
     - An id mapping to the :ref:`computed-identifiers` of the external database Sequence containing the sequence to be located.
   * - interval
     - :ref:`Interval`
     - 1..1
     - Position of feature on reference sequence specified by sequence_id.

**Implementation guidance**

* For a :ref:`Sequence` of length *n*:
   * 0 ≤ *interval.start* ≤ *interval.end* ≤ *n*
   * interbase coordinate 0 refers to the point before the start of the Sequence
   * interbase coordinate n refers to the point after the end of the Sequence.
* Coordinates MUST refer to a valid Sequence. VRS does not support
  referring to intronic positions within a transcript sequence,
  extrapolations beyond the ends of sequences, or other implied
  sequence.

.. important:: HGVS permits variants that refer to non-existent
               sequence. Examples include coordinates extrapolated
               beyond the bounds of a transcript and intronic
               sequence. Such variants are not representable using VR
               and MUST be projected to a genomic reference in order
               to be represented.

**Example**

.. parsed-literal::

    {
      "interval": {
        "end": 44908822,
        "start": 44908821,
        "type": "SimpleInterval"
      },
      "sequence_id": "ga4gh:SQ.IIB53T8CNeJJdUqzn9V_JnRtQadwWCbl",
      "type": "SequenceLocation"
    }




.. _state:

State (Abstract Class)
######################

**Biological definition**

None.

**Computational definition**

*State* objects are one of two primary components specifying a VR
:ref:`Allele` (in addition to :ref:`Location`), and the designated
components for representing change (or non-change) of the features
indicated by the Allele Location. As an abstract class, State currently
encompasses single and contiguous :ref:`sequence` changes (see :ref:`SequenceState
<sequence-state>`), with additional types under consideration (see
:ref:`planned-states`).

.. _sequence-state:

SequenceState
$$$$$$$$$$$$$

**Biological definition**

None.

**Computational definition**

The *SequenceState* class specifically captures a :ref:`sequence` as a
:ref:`State`. This is the State class to use for representing
"ref-alt" style variation, including SNVs, MNVs, del, ins, and delins.

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
     - State type; MUST be set to '**SequenceState**'
   * - sequence
     - string
     - 1..1
     - The string of sequence residues that is to be used as the state for other types.

**Example**

.. parsed-literal::

    {
      "sequence": "T",
      "type": "SequenceState"
    }


.. _variation:

Variation
@@@@@@@@@

The Variation class is the conceptual root of all types of variation,
both current and future.  Variation subclasses are:

**Biological definition**

In biology, variation is often used to mean `genetic variation`_,
describing the differences observed in DNA among individuals.

**Computational definition**

The *Variation* abstract class is the top-level object in the
:ref:`vr-schema-diagram` and represents the concept of a molecular
state. The representation and types of molecular states are widely
varied, and there are several :ref:`planned-variation` currently under
consideration to capture this diversity. The primary Variation
subclass defined by the VRS |version| specification is the
:ref:`Allele`, with the :ref:`text` subclass for capturing other
Variations that are not yet covered.


.. _allele:

Allele
######

**Biological definition**

One of a number of alternative forms of the same gene or same genetic
locus. In the context of biological sequences, “allele” refers to one
of a set of specific changes within a :ref:`Sequence`. In the context
of VR, Allele refers to a Sequence or Sequence change with respect to
a reference sequence, without regard to genes or other features.

**Computational definition**

An Allele is an assertion of the :ref:`State <State>` of a biological
sequence at a :ref:`Location <Location>`.

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
     - Variation Id; MUST be unique within document
   * - type
     - string
     - 1..1
     - Variation type; MUST be set to '**Allele**'
   * - location
     - :ref:`Location`
     - 1..1
     - Where Allele is located
   * - state
     - :ref:`State`
     - 1..1
     - State at location

**Implementation guidance**

* The :ref:`State <State>` and :ref:`Location <Location>` subclasses
  respectively represent diverse kinds of sequence changes and
  mechanisms for describing the locations of those changes, including
  varying levels of precision of sequence location and categories of
  sequence changes.
* Implementations MUST enforce values interval.end ≤ sequence_length
  when the Sequence length is known.
* Alleles are equal only if the component fields are equal: at the
  same location and with the same state.
* Alleles MAY have multiple related representations on the same
  Sequence type due to normalization differences.
* Implementations SHOULD normalize Alleles using :ref:`"justified"
  normalization <normalization>` whenever possible to facilitate
  comparisons of variation in regions of representational ambiguity.
* Implementations MUST normalize Alleles using :ref:`"justified"
  normalization <normalization>` when generating a
  :ref:`computed-identifiers`.
* When the alternate Sequence is the same length as the interval, the
  lengths of the reference Sequence and imputed Sequence are the
  same. (Here, imputed sequence means the sequence derived by applying
  the Allele to the reference sequence.) When the replacement Sequence
  is shorter than the length of the interval, the imputed Sequence is
  shorter than the reference Sequence, and conversely for replacements
  that are larger than the interval.
* When the replacement is “” (the empty string), the Allele refers to
  a deletion at this location.
* The Allele entity is based on Sequence and is intended to be used
  for intragenic and extragenic variation. Alleles are not explicitly
  associated with genes or other features.
* Biologically, referring to Alleles is typically meaningful only in
  the context of empirical alternatives. For modelling purposes,
  Alleles MAY exist as a result of biological observation or
  computational simulation, i.e., virtual Alleles.
* “Single, contiguous” refers the representation of the Allele, not
  the biological mechanism by which it was created. For instance, two
  non-adjacent single residue Alleles could be represented by a single
  contiguous multi-residue Allele.
* The terms "allele" and "variant" are often used interchangeably,
  although this use may mask subtle distinctions made by some users.

   * In the genetics community, "allele" may also refer to a
     haplotype.
   * "Allele" connotes a state whereas "variant" connotes a change
     between states. This distinction makes it awkward to use variant
     to refer to the concept of an unchanged position in a Sequence
     and was one of the factors that influenced the preference of
     “Allele” over “Variant” as the primary subject of annotations.
   * See :ref:`Use “Allele” rather than “Variant” <use-allele>` for
     further details.
* When a trait has a known genetic basis, it is typically represented
  computationally as an association with an Allele.
* This specification's definition of Allele applies to all Sequence
  types (DNA, RNA, AA).

**Example**

.. parsed-literal::

    {
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
    }


.. _text:

Text
####

**Biological definition**

None

**Computational definition**

The *Text* subclass of :ref:`Variation` is intended to capture textual
descriptions of variation that cannot be parsed by other Variation
subclasses, but are still treated as variation.

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
     - Variation Id; MUST be unique within document
   * - type
     - string
     - 1..1
     - Variation type; MUST be set to '**Text**'
   * - definition
     - string
     - 1..1
     - The textual variation representation not parsable by other subclasses of Variation.

**Implementation guidance**

* An implementation MUST represent Variation with subclasses other
  than Text if possible.
* An implementation SHOULD define or adopt conventions for defining
  the strings stored in Text.definition.
* If a future version of VRS is adopted by an implementation and
  the new version enables defining existing Text objects under a
  different Variation subclass, the implementation MUST construct a
  new object under the other Variation subclass. In such a case, an
  implementation SHOULD persist the original Text object and respond
  to queries matching the Text object with the new object.
* Additional Variation subclasses are continually under
  consideration. Please open a `GitHub issue`_ if you would like to
  propose a Variation subclass to cover a needed variation
  representation.

**Example**

.. parsed-literal::

    {
      "definition": "APOE loss",
      "type": "Text"
    }


.. _GitHub issue: https://github.com/ga4gh/vr-spec/issues
.. _genetic variation: https://en.wikipedia.org/wiki/Genetic_variation


VariationSet
############

**Biological definition**

Sets of variation are used widely, such as sets of variants in dbSNP
or ClinVar that might be related by function. 

**Computational definition**

An unconstrained set of Variation objects or references.

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
     - Identifier of the VariationSet.
   * - type
     - string
     - 1..1
     - Variation type; MUST be "VariationSet" (default)
   * - members
     - :ref:`Variation`\[] or :ref:`CURIE`\[]
     - 0..*
     - List of Variation objects or identifiers. Attribute is
       required, but MAY be empty.


**Implementation Guidance**

* The VariationSet identifier MAY be computed as described in
  :ref:`computed-identifiers`, in which case the identifier
  effectively refers to a static set because a different set of
  members would generate a different identifier.
* `members` may be specified as Variation objects or CURIE
  identifiers.
* CURIEs MAY refer to entities outside the `ga4gh` namespace.
  However, objects that use non-`ga4gh` identifiers MAY NOT use the
  :ref:`computed-identifiers` mechanism.
* VariationSet identifiers computed using the GA4GH
  :ref:`computed-identifiers` process do *not* depend on whether the
  Variation objects are inlined or referenced, and do *not* depend on
  the order of members.
* Elements of `members` must be subclasses of Variation, which permits
  sets to be nested.
* Recursive sets are not meaningful and are not supported.
* VariationSets may be empty.

**Example**

Inlined Variation objects:

.. parsed-literal::

  {
    "members": [
      {
        "location": {
          "interval": {
            "end": 11,
            "start": 10,
            "type": "SimpleInterval"
          },
          "sequence_id": "ga4gh:SQ.01234abcde",
          "type": "SequenceLocation"
        },
        "state": {
          "sequence": "C",
          "type": "SequenceState"
        },
        "type": "Allele"
      },
      {
        "location": {
          "interval": {
            "end": 21,
            "start": 20,
            "type": "SimpleInterval"
          },
          "sequence_id": "ga4gh:SQ.01234abcde",
          "type": "SequenceLocation"
        },
        "state": {
          "sequence": "C",
          "type": "SequenceState"
        },
        "type": "Allele"
      },
      {
        "location": {
          "interval": {
            "end": 31,
            "start": 30,
            "type": "SimpleInterval"
          },
          "sequence_id": "ga4gh:SQ.01234abcde",
          "type": "SequenceLocation"
        },
        "state": {
          "sequence": "C",
          "type": "SequenceState"
        },
        "type": "Allele"
      }
    ],
    "type": "VariationSet"
  }


Referenced Variation objects:

.. parsed-literal::

  {
    "members": [
      "ga4gh:VA.6xjH0Ikz88s7MhcyN5GJTa1p712-M10W",
      "ga4gh:VA.7k2lyIsIsoBgRFPlfnIOeCeEgj_2BO7F",
      "ga4gh:VA.ikcK330gH3bYO2sw9QcTsoptTFnk_Xjh"
    ],
    "type": "VariationSet"
  }

The GA4GH computed identifier for these sets is
`ga4gh:VS.WVC_R7OJ688EQX3NrgpJfsf_ctQUsVP3`, regardless of the whether
the Variation objects are inlined or referenced, and regardless of
order. See :ref:`computed-identifiers` for more information.
