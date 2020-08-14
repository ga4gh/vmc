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
* Implementations MUST use CURIE identifiers verbatim and MUST NOT be
  modified in any way (e.g., case-folding).  Implementations MUST NOT
  expose partial (parsed) identifiers to any client.

**Example**

Identifiers for GRCh38 chromosome 19::

    ga4gh:SQ.IIB53T8CNeJJdUqzn9V_JnRtQadwWCbl
    refseq:NC_000019.10
    grch38:19

See :ref:`identify` for examples of CURIE-based identifiers for VRS
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
  to a member of set of sequences that comprise a genome assembly. In the VRS
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


.. _CytobandInterval:

CytobandInterval
$$$$$$$$$$$$$$

**Computational definition**

A contiguous region specified by named cytoband features.

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
     - Interval type; MUST be set to '**CytobandInterval**'
   * - start
     - string
     - 1..1
     - name of feature start
   * - end
     - string
     - 1..1
     - name of feature end

**Implementation guidance**

* `start` and `end` attributes of CytobandInterval are specified
  vaguely in order to enable the use of CytobandInterval in multiple
  species.  However, the primary use is for Human genetics.
* The valid values for, and the syntactic structure of, the `start`
  and `end` depend on the species.  When using :ref:`CytobandInterval`
  to refer to human cytogentic bands, ISCN conventions MUST be
  used. Bands are denoted by the arm ("p" or "q") and position (e.g.,
  "22", "22.3", or the symbolic values "cen", "tel", or "ter"). If
  `start` and `end` are on different arms, they SHOULD correspond to
  the p-arm and q-arm locations respectively. If `start` and `end` are
  on the same arm, `start` MUST be the more centromeric position
  (i.e., with lower band and sub-band numbers).

**Example**

.. parsed-literal::

   {
     'end': 'q22.3',
     'start': 'q22.2',
     'type': 'CytobandInterval'
   }

.. _TextInterval:

TextInterval
$$$$$$$$$$$$$$

**Computational definition**

A contiguous region specified by named features.

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
     - Interval type; MUST be set to '**TextInterval**'
   * - start
     - string
     - 1..1
     - name of feature start
   * - end
     - string
     - 1..1
     - name of feature end

**Implementation guidance**

* `start` and `end` attributes of TextInterval are intentionally
  specified vaguely in order to accommodate a wide variety of
  uses.

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
  the two concepts are not interchangeable, especially when the
  location is non-specific (e.g., a range) or symbolic (a gene).


.. _chromosomelocation:

ChromosomeLocation
$$$$$$$$$$$$$$$$$$

**Biological definition**

Chromosomal locations based on named landmarks.

**Computational definition**

A ChromosomeLocation is a :ref:`Location` that is defined by a named
chromosomal features.

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
     - Location id; MUST be unique within document
   * - type
     - string
     - 1..1
     - Location type; MUST be set to **'ChromosomeLocation'**
   * - species
     - :ref:`CURIE`
     - 1..1
     - An external reference to a species taxonomy.  See Implementation Guidance, below.
   * - chr
     - string
     - 1..1
     - The symbolic chromosome name
   * - interval
     - :ref:`CytobandInterval`
     - 1..1
     - The chromosome region based on feature names


**Implementation guidance**

* ChromosomeLocation is intended to enable the representation of
  cytogenetic results from karyotyping or low-resolution molecular
  methods, particularly those found in older scientific literature.
  Precise :ref:`SequenceLocation` should be preferred when
  nucleotide-scale location is known.
* `species` is specified using the NCBI taxonomy.  The CURIE prefix
  MUST be "taxonomy", corresponding to the `NCBI taxonomy prefix at
  identifiers.org
  <https://registry.identifiers.org/registry/taxonomy>`__, and the
  CURIE reference MUST be an NCBI taxonomy identifier (e.g., 9606 for
  Homo sapiens).
* `chromosome` is an archetypal chromosome name. Valid values for, and
  the syntactic structure of, `chromosome` depends on the species.
  `chromosome` MUST be an official sequence name from `NCBI Assembly
  <https://www.ncbi.nlm.nih.gov/assembly>`__.  For Humans, valid
  chromosome names are 1..22, X, Y (case-sensitive).
* `interval` refers to a contiguous region specified named markers,
  which are presumed to exist on the specified chromosome.  See
  :ref:`CytobandInterval` for additional information.
* The conversion of ChromosomeLocation instances to SequenceLocation
  instances is out-of-scope for VRS.  When converting `start` and
  `end` to SequenceLocations, the positions MUST be interpreted as
  inclusive ranges that cover the maximal extent of the region.
* Data for converting cytogenetic bands to precise sequence
  coordinates are available at `NCBI GDP
  <https://ftp.ncbi.nlm.nih.gov/pub/gdp/>`__, `UCSC GRCh37 (hg19)
  <http://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/cytoBand.txt.gz>`__,
  `UCSC GRCh38 (hg38)
  <http://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/cytoBand.txt.gz>`__,
  and `bioutils (Python)
  <https://bioutils.readthedocs.io/en/stable/reference/bioutils.cytobands.html>`__.
* See also the rationale
  for :ref:`dd-not-using-external-chromosome-declarations`.


**Example**

.. parsed-literal::

   {
     'chr': '11',
     'interval': {
       'end': 'q22.3',
       'start': 'q22.2',
       'type': 'CytobandInterval'
       },
     'species_id': 'taxonomy:9606',
     'type': 'ChromosomeLocation'
   }

.. _sequence-location:
.. _sequencelocation:

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
               sequence. Such variants are not representable using VRS
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

*State* objects are one of two primary components specifying a VRS
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
both current and future.

**Biological definition**

In biology, variation is often used to mean *sequence* variation,
describing the differences observed in DNA or AA bases among
individuals.

**Computational definition**

The *Variation* abstract class is the top-level object in the
:ref:`vr-schema-diagram` and represents the concept of a molecular
state. The representation and types of molecular states are widely
varied, and there are several :ref:`planned-variation` currently under
consideration to capture this diversity. The primary Variation
subclass defined by the VRS |version| specification is the
:ref:`Allele`, with the :ref:`textvariation` subclass for capturing other
Variations that are not yet covered.


.. _allele:

Allele
######

**Biological definition**

One of a number of alternative forms of the same gene or same genetic
locus. In the context of biological sequences, “allele” refers to one
of a set of specific changes within a :ref:`Sequence`. In the context
of VRS, Allele refers to a Sequence or Sequence change with respect to
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


.. _textvariation:

TextVariation
####

**Biological definition**

None

**Computational definition**

The *TextVariation* subclass of :ref:`Variation` is intended to capture textual
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
     - Variation type; MUST be set to '**TextVariation**'
   * - definition
     - string
     - 1..1
     - The textual variation representation not parsable by other subclasses of Variation.

**Implementation guidance**

* An implementation MUST represent Variation with subclasses other
  than TextVariation if possible.
* An implementation SHOULD define or adopt conventions for defining
  the strings stored in TextVariation.definition.
* If a future version of VRS is adopted by an implementation and
  the new version enables defining existing TextVariation objects under a
  different Variation subclass, the implementation MUST construct a
  new object under the other Variation subclass. In such a case, an
  implementation SHOULD persist the original TextVariation object and respond
  to queries matching the TextVariation object with the new object.
* Additional Variation subclasses are continually under
  consideration. Please open a `GitHub issue`_ if you
  would like to propose a Variation subclass to cover a needed
  variation representation.

**Example**

.. parsed-literal::

    {
      "definition": "APOE loss",
      "type": "TextVariation"
    }


.. _haplotype:

Haplotype
#########

**Biological definition**

A specific combination of Alleles that occur together on single
sequence in one or more individuals.

**Computational definition**

A specific combination of non-overlapping Alleles that co-occur on the
same reference sequence.

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
     - Variation type; MUST be "Haplotype"
   * - members
     - :ref:`Allele`\[] | :ref:`CURIE`\[]
     - 1..*
     - List of Alleles, or references to Alleles, that comprise this
       Haplotype



**Implementation Guidance**

* Haplotypes are an assertion of Alleles known to occur “in cis” or
  “in phase” with each other.
* All Alleles in a Haplotype MUST be defined on the same reference
  sequence.
* Alleles within a Haplotype MUST not overlap ("overlap" is defined in
  Interval).
* The locations of Alleles within the Haplotype MUST be interpreted
  independently.  Alleles that create a net insertion or deletion of
  sequence MUST NOT change the location of "downstream" Alleles.
* The `members` attribute is required and MUST contain at least one
  Allele.


**Sources**

* `ISOGG: Haplotype <https://isogg.org/wiki/Haplotype>`__ — A haplotype
  is a combination of alleles (DNA sequences) at different places
  (loci) on the chromosome that are transmitted together. A haplotype
  may be one locus, several loci, or an entire chromosome depending on
  the number of recombination events that have occurred between a
  given set of loci.
* `SO: haplotype (SO:0001024)
  <http://www.sequenceontology.org/browser/current_release/term/SO:0001024>`__
  — A haplotype is one of a set of coexisting sequence variants of a
  haplotype block.
* `GENO: Haplotype (GENO:0000871)
  <http://www.ontobee.org/ontology/GENO?iri=http://purl.obolibrary.org/obo/GENO_0000871>`__ -
  A set of two or more sequence alterations on the same chromosomal
  strand that tend to be transmitted together.

**Examples**

An APOE-ε1 Haplotype with inline Alleles::

    {
      "members": [
        {
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
        },
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
      ],
      "type": "Haplotype"
    }
    
The same APOE-ε1 Haplotype with referenced Alleles::
    
    {
      "members": [
        "ga4gh:VA.iXjilHZiyCEoD3wVMPMXG3B8BtYfL88H",
        "ga4gh:VA.EgHPXXhULTwoP4-ACfs-YCXaeUQJBjH_"
      ],
      "type": "Haplotype"
    }
    
The GA4GH computed identifier for these Haplotypes is
`ga4gh:VH.NAVnEuaP9gf41OxnPM56XxWQfdFNcUxJ`, regardless of the whether
the Variation objects are inlined or referenced, and regardless of
order. See :ref:`computed-identifiers` for more information.



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
     - Variation type; MUST be "VariationSet"
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
