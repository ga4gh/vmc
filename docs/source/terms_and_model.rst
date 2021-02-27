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
translating precise biological definitions into information models and
data structures that may be used in software.** This translation
should result in a representation of information that is consistent
with conventional biological understanding and, ideally, be able to
accommodate future data as well. The resulting *computational
representation* of information should also be cognizant of
computational performance, the minimization of opportunities for
misunderstanding, and ease of manipulating and transforming data.

Accordingly, for each term we define below, we begin by describing the
term as used by the genetics and/or bioinformatics communities as
available. When a term has multiple such definitions, we
explicitly choose one of them for the purposes of computational
modelling. We then define the **computational definition** that
reformulates the community definition in terms of information content.
Finally, we translate each of these computational definitions into precise
specifications for the (**information model**). Terms are ordered
"bottom-up" so that definitions depend only on previously-defined terms.

.. note:: The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL
          NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and
          "OPTIONAL" in this document are to be interpreted as
          described in `RFC 2119`_.


Information Model Principles
@@@@@@@@@@@@@@@@@@@@@@@@@@@@

* **VRS uses** `snake_case
  <https://simple.wikipedia.org/wiki/Snake_case>`__ **to represent
  compound words.** Although the schema is currently JSON-based (which
  would typically use camelCase), VRS itself is intended to be neutral
  with respect to languages and database.

* **VRS objects are minimal** `value objects
  <https://en.wikipedia.org/wiki/Value_object>`__. Two objects are
  considered equal if and only if their respective attributes are
  equal.  As value objects, VRS objects are used as primitive types
  and MUST NOT be used as containers for related data, such as primary
  database accessions, representations in particular formats, or links
  to external data.  Instead, related data should be associated with
  VRS objects through identifiers.  See :ref:`computed-identifiers`.

* **Error handling is intentionally unspecified and delegated to
  implementation.**  VRS provides foundational data types that
  enable significant flexibility.  Except where required by this
  specification, implementations may choose whether and how to
  validate data.  For example, implementations MAY choose to validate
  that particular combinations of objects are compatible, but such
  validation is not required.

* **Optional attributes start with an underscore.** Optional
  attributes are not part of the value object.  Such attributes are
  not considered when evaluating equality or creating computed
  identifiers.  The ``_id`` attribute is available to identifiable
  objects, and MAY be used by an implementation to store the
  identifier for a VRS object.  If used, the stored ``_id`` element
  MUST be a `CURIE`_. If used for creating a :ref:`truncated-digest`
  for parent objects, the stored element must be a :ref:`GA4GH
  Computed Identifier <identify>`.  Implementations MUST ignore
  attributes beginning with an underscore and they SHOULD NOT transmit
  objects containing them.



.. _Variation:

Variation
@@@@@@@@@

In the genetics community, variation is often used to mean *sequence*
variation, describing the differences observed in DNA or AA bases among
individuals, and typically with respect to a common reference sequence.

In VRS, the Variation class is the conceptual root of all types of
variation, and the *Variation* abstract class is the top-level object in
the :ref:`vr-schema-diagram`. Variation types are broadly categorized as
:ref:`MolecularVariation`, :ref:`SystemicVariation`, or a :ref:`utility
subclass <utilityvariation>`. Types of variation are widely varied, and
there are several :ref:`planned-variation` currently under consideration
to capture this diversity.

**Computational Definition**

A representation of the state of one or more molecules.

.. _MolecularVariation:

Molecular Variation
###################

A :ref:`variation` of a sequence that represents a portion of or an
entire contiguous molecule.

.. _Allele:

Allele
$$$$$$

.. note:: The terms *allele* and *variant* are often used interchangeably,
   although this use may mask subtle distinctions made by some users.
   Specifically, while *allele* connotes a specific sequence state,
   *variant* connotes a **change** between states.

   This distinction makes it awkward to use *variant* to represent an
   unchanged (refrence-agreement) state at a Sequence Location. This was
   a primary factor for choosing to use *allele* over *variant*
   when designing VRS. Read more about this design decision: Using
   :ref:`allele-not-variant`.

An allele may refer to a number of alternative forms of the same gene or same
genetic locus. In the genetics community, *allele* may also refer to a
specific haplotype. In the context of biological sequences, "allele" refers
to a distinct state of a molecule at a location.

**Computational Definition**

A state of a molecule at a :ref:`Location`.

**Information Model**

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
     - MUST be "Allele"
   * - location
     - :ref:`Location` | :ref:`CURIE`
     - 1..1
     - Where Allele is located
   * - state
     - :ref:`SequenceExpression` | :ref:`SequenceState` (deprecated)
     - 1..1
     - An expression of the sequence state

**Implementation Guidance**

* The :ref:`SequenceExpression` and :ref:`Location`
  subclasses respectively represent diverse kinds of
  sequence changes and mechanisms for describing the locations of
  those changes, including varying levels of precision of sequence
  location and categories of sequence changes.
* Implementations MUST enforce values interval.end ≤ sequence_length
  when the Sequence length is known.
* Alleles are equal only if the component fields are equal: at the
  same location and with the same state.
* Alleles MAY have multiple related representations on the same
  Sequence type due to normalization differences.
* Implementations SHOULD normalize Alleles using :ref:`fully-justified
  normalization <normalization>` whenever possible to facilitate
  comparisons of variation in regions of representational ambiguity.
* Implementations MUST normalize Alleles using :ref:`fully-justified
  normalization <normalization>` when generating
  :ref:`computed-identifiers`.
* When the alternate Sequence is the same length as the interval, the
  lengths of the reference Sequence and imputed Sequence are the
  same. (Here, imputed sequence means the sequence derived by applying
  the Allele to the reference sequence.) When the replacement Sequence
  is shorter than the length of the interval, the imputed Sequence is
  shorter than the reference Sequence, and conversely for replacements
  that are larger than the interval.
* When the state is a :ref:`LiteralSequenceExpression` of ``""`` (the empty
  string), the Allele refers to a deletion at this location.
* The Allele entity is based on Sequence and is intended to be used
  for intragenic and extragenic variation. Alleles are not explicitly
  associated with genes or other features.
* Biologically, referring to Alleles is typically meaningful only in
  the context of empirical alternatives. For modelling purposes,
  Alleles MAY exist as a result of biological observation or
  computational simulation, i.e., virtual Alleles.
* "Single, contiguous" refers the representation of the Allele, not
  the biological mechanism by which it was created. For instance, two
  non-adjacent single residue Alleles could be represented by a single
  contiguous multi-residue Allele.
* When a trait has a known genetic basis, it is typically represented
  computationally as an association with an Allele.
* This specification's definition of Allele applies to any
  :ref:`Location`, including locations on RNA or protein
  :ref:`Sequence`.

**Examples**

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
          "type": "LiteralSequenceExpression"
       },
       "type": "Allele"
    }


**Sources**

* `ISOGG: Allele <http://isogg.org/wiki/Allele>`__ — An allele is one
  of two or more forms of the DNA sequence of a particular gene.
* `SequenceOntology: allele (SO:0001023)
  <http://www.sequenceontology.org/browser/current_svn/term/SO:0001023>`__
  — An allele is one of a set of coexisting sequence variants of a
  gene.
* `SequenceOntology: sequence_alteration (SO:0001059)
  <http://www.sequenceontology.org/browser/current_svn/term/SO:0001059>`__
  — A sequence_alteration is a sequence_feature whose extent is the
  deviation from another sequence.
* `SequenceOntology: sequence_variant (SO:0001060)
  <http://www.sequenceontology.org/browser/current_svn/term/SO:0001060>`__
  — A sequence_variant is a non exact copy of a sequence_feature or
  genome exhibiting one or more sequence_alteration.
* `Wikipedia: Allele <https://en.wikipedia.org/wiki/Allele>`__ — One
  of a number of alternative forms of the same gene or same genetic
  locus.
* `GenotypeOntology: Allele (GENO:0000512)
  <http://purl.obolibrary.org/obo/GENO_0000512>`__ - A sequence
  feature representing one of a set of coexisting sequences at a
  particular genomic locus. An allele can represent a 'reference' or
  'variant' sequence at a locus.


.. _Haplotype:

Haplotype
$$$$$$$$$

Haplotypes are a specific combination of Alleles that are *in-cis*: occurring
on the same physical molecule. Haplotypes are commonly described with respect
to locations on a gene, a set of nearby genes, or other physically proximal
genetic markers that tend to be transmitted together.

**Computational Definition**

A set of non-overlapping :ref:`Allele` members that co-occur on the same
molecule.

**Information Model**

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
     - MUST be "Haplotype"
   * - members
     - :ref:`Allele`\[] | :ref:`CURIE`\[]
     - 1..*
     - List of Alleles, or references to Alleles, that comprise this
       Haplotype


**Implementation Guidance**

* Haplotypes are an assertion of Alleles known to occur "in cis" or
  "in phase" with each other.
* All Alleles in a Haplotype MUST be defined on the same reference
  sequence or chromosome.
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
* `SequenceOntology: haplotype (SO:0001024)
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
            "type": "LiteralSequenceExpression"
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
            "type": "LiteralSequenceExpression"
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
`ga4gh:VH.NAVnEuaP9gf41OxnPM56XxWQfdFNcUxJ`, regardless
of whether the Variation objects are inlined or
referenced, and regardless of order. See
:ref:`computed-identifiers` for more information.

.. _SystemicVariation:

Systemic Variation
##################

Systemic Variation is a :ref:`Variation` of multiple
molecules in the context of a system, e.g. a genome,
sample, or homologous chromosomes.

.. _Abundance:

Abundance
$$$$$$$$$

*Abundance* is the measure of a quantity of a molecule
in a system. :ref:`Copy Number <CopyNumber>` and
gene expression variants are two common types of
abundance variation, measuring the copies of a molecule
present in a genome or expressed in a sample, respectively.

.. _CopyNumber:

CopyNumber
##########

*Copy Number* captures the copies of a molecule within
a genome, and can be used to express concepts such as
amplification and copy loss.

**Computational Definition**

The count of copies of a :ref:`Feature` or
:ref:`MolecularVariation` subject within a genome.

**Information Model**

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
     - Computed Identifier
   * - type
     - string
     - 1..1
     - MUST be "CopyNumber"
   * - subject
     - :ref:`MolecularVariation` | :ref:`Feature`
     - 1..1
     - Subject of the abundance statement
   * - copies
     - :ref:`CopyCount`
     - 1..1
     - The integral number of copies of the subject in the genome

**Example**

Two, three, or four total copies of BRCA1:

.. parsed-literal::

    {
      "copies": {
        "absolute_measure": true,
        "max": 4,
        "min": 2,
        "type": "CopyCount"
      },
      "subject": {
        "gene_id": "ncbigene:672",
        "type": "Gene"
      },
      "type": "CopyCount"
    }


.. _UtilityVariation:

Utility Variation
#################

*Utility variation* is a collection of :ref:`Variation`
subclasses that cannot be constrained to a specific class of
biological variation, but are necessary for some technical
applications of VRS.

.. _Text:

Text
$$$$

Some forms of variation are described with text that is interpretable
only by humans.

**Computational Definition**

A free-text definition of variation.

**Information Model**

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
     - MUST be "Text"
   * - definition
     - string
     - 1..1
     - The textual variation representation not representable by
       other subclasses of Variation.

**Implementation Guidance**

* An implementation MUST represent Variation with subclasses other
  than Text if possible.
* Because the Text type can be easily abused, implementations are NOT
  REQUIRED to provide it.  If it is provided, implementations SHOULD
  consider applying access controls.
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

.. _GitHub issue: https://github.com/ga4gh/vrs/issues

**Examples**

.. parsed-literal::

    {
      "definition": "Microsatellite Instability High",
      "type": "Text"
    }


.. _VariationSet:

VariationSet
$$$$$$$$$$$$

Sets of variation are used widely, such as sets of variants in dbSNP
or ClinVar that might be related by function.

**Computational Definition**

An unconstrained set of Variation members.

**Information Model**

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
     - MUST be "VariationSet"
   * - members
     - :ref:`Variation`\[] | :ref:`CURIE`\[]
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

**Examples**

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


Locations and Intervals
@@@@@@@@@@@@@@@@@@@@@@@


.. _Location:

Location
########

As used by biologists, the precision of "location" (or "locus") varies
widely, ranging from precise start and end numerical coordinates
defining a Location, to bounded regions of a sequence, to conceptual
references to named genomic features (e.g., chromosomal bands, genes,
exons) as proxies for the Locations on an implied reference sequence.

The most common and concrete Location is a :ref:`SequenceLocation`, i.e.,
a Location based on a named sequence and an Interval on that sequence.
Another common Location is a :ref:`ChromosomeLocation`, specifying a
location from cytogenetic coordinates of stained metaphase chromosomes.
Additional :ref:`planned-locations` may also be conceptual or symbolic locations,
such as a cytoband region or a gene. Any of these may be used as the
Location for Variation.

**Computational Definition**

The position of a contiguous segment of a biological sequence.

**Implementation Guidance**

* Location refers to a position.  Although it MAY imply a sequence,
  the two concepts are not interchangeable, especially when the
  location is non-specific (e.g., specified by a
  :ref:`NestedInterval`).


.. _ChromosomeLocation:

ChromosomeLocation
$$$$$$$$$$$$$$$$$$

Chromosomal locations based on named features, including named landmarks,
cytobands, and regions observed from chromosomal staining techniques.

**Computational Definition**

A :ref:`Location`, on a chromosome defined by a species and chromosome name.

**Information Model**

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
     - MUST be "ChromosomeLocation"
   * - species
     - :ref:`CURIE`
     - 1..1
     - An external reference to a species taxonomy.  Default:
       "taxonomy:9606" (human).  See Implementation Guidance, below.
   * - chr
     - string
     - 1..1
     - The symbolic chromosome name
   * - interval
     - :ref:`CytobandInterval`
     - 1..1
     - The chromosome region based on feature names


**Implementation Guidance**

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
* ChromosomeLocation is intended primarily for human chromosomes.
  Support for other species is possible and will be considered based
  on community feedback.
* `chromosome` is an archetypal chromosome name. Valid values for, and
  the syntactic structure of, `chromosome` depends on the species.
  `chromosome` MUST be an official sequence name from `NCBI Assembly
  <https://www.ncbi.nlm.nih.gov/assembly>`__.  For humans, valid
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


**Examples**

.. parsed-literal::

   {
     "chr": "11",
     "interval": {
       "end": "q22.3",
       "start": "q22.2",
       "type": "CytobandInterval"
       },
     "species_id": "taxonomy:9606",
     "type": "ChromosomeLocation"
   }

.. _SequenceLocation:

SequenceLocation
$$$$$$$$$$$$$$$$

A *Sequence Location* is a specified subsequence of a reference :ref:`Sequence`.
The reference is typically a chromosome, transcript, or protein sequence.

**Computational Definition**

A :ref:`Location` defined by an interval on a referenced :ref:`Sequence`.

**Information Model**

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
     - MUST be "SequenceLocation"
   * - sequence_id
     - :ref:`CURIE`
     - 1..1
     - A VRS :ref:`Computed Identifier <computed-identifiers>`
       for the reference :ref:`Sequence`.
   * - interval
     - :ref:`SequenceInterval`
     - 1..1
     - Position of feature on reference sequence specified by sequence_id.

**Implementation Guidance**

* For a :ref:`Sequence` of length *n*:
   * 0 ≤ *interval.start* ≤ *interval.end* ≤ *n*
   * inter-residue coordinate 0 refers to the point before the start of the Sequence
   * inter-residue coordinate n refers to the point after the end of the Sequence.
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

**Examples**

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

.. _Interval:
.. _SequenceInterval:

SequenceInterval
################

**Computational Definition**

The *SequenceInterval* abstract class defines a range on a
:ref:`sequence`, possibly with length zero, and specified using
:ref:`inter-residue-coordinates-design`. An Interval MAY be a
:ref:`SimpleInterval` with a single start and end coordinate.
:ref:`Future Location and SequenceInterval types <planned-locations>`
will enable other methods for describing where :ref:`variation`
occurs. Any of these MAY be used as the SequenceInterval for Location.

.. sidebar:: VRS Uses Inter-residue Coordinates

   **GA4GH VRS uses inter-residue coordinates when referring to spans of
   sequence.**

   Inter-residue coordinates refer to the zero-width points before and
   after :ref:`residues <Residue>`. An interval of inter-residue
   coordinates permits referring to any span, including an empty span,
   before, within, or after a sequence. See
   :ref:`inter-residue-coordinates-design` for more details on this design
   choice.  Inter-residue coordinates are always zero-based.


**Sources**

* `Interbase Coordinates (Chado documentation) <http://gmod.org/wiki/Introduction_to_Chado#Interbase_Coordinates>`__
* `SequenceOntology: sequence_feature (SO:0000110) <http://www.sequenceontology.org/miso/current_svn/term/SO:0000110>`__ — Any extent of continuous biological sequence.
* `SequenceOntology: region (SO:0000001) <http://www.sequenceontology.org/miso/current_svn/term/SO:0000001>`__ — A sequence_feature with an extent greater than zero. A nucleotide region is composed of bases and a polypeptide region is composed of amino acids.


.. _SimpleInterval:

SimpleInterval
$$$$$$$$$$$$$$

**Computational Definition**

A :ref:`SequenceInterval` with a single start and end coordinate.

**Information Model**

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
     - MUST be "SimpleInterval"
   * - start
     - integer
     - 1..1
     - start position
   * - end
     - integer
     - 1..1
     - end position

**Implementation Guidance**

* Implementations MUST enforce values 0 ≤ start ≤ end. In the case of
  double-stranded DNA, this constraint holds even when a feature is on
  the complementary strand.
* VRS uses Inter-residue coordinates because they provide conceptual
  consistency that is not possible with residue-based systems (see
  :ref:`rationale <inter-residue-coordinates-design>`). Implementations
  will need to convert between inter-residue and 1-based inclusive
  residue coordinates familiar to most human users.
* Inter-residue coordinates start at 0 (zero).
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
  identical zero-width SimpleIntervals).
* <start, end>=<*0,0*> refers to the point with width zero before the first residue.
* <start, end>=<*i,i+1*> refers to the *i+1th* (1-based) residue.
* <start, end>=<*N,N*> refers to the position after the last residue for Sequence of length *N*.
* See example notebooks in |vrs-python|.

**Examples**

.. parsed-literal::

    {
      "end": 44908822,
      "start": 44908821,
      "type": "SimpleInterval"
    }


.. _NestedInterval:

NestedInterval
$$$$$$$$$$$$$$

For some assays, it is not possible to describe a
:ref:`SequenceLocation` with exact precision, but it is possible
to bound the region containing the Sequence Location. In those
cases, two sets of coordinates are used as a nested interval to
describe the inner and outer bounds.

**Computational Definition**

A :ref:`SequenceInterval` defined by nested inner and outer
:ref:`SimpleInterval` coordinates. Inner and outer coordinates
represent inner and outer bounds of ambiguity for the start and
end of the interval.

**Information Model**

.. list-table:: NestedInterval
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
     - MUST be "NestedInterval"
   * - inner
     - :ref:`SimpleInterval`
     - 1..1
     - inner interval
   * - outer
     - :ref:`SimpleInterval`
     - 1..1
     - outer interval

**Implementation Guidance**

* NestedInterval is intended to be used for variation where the start
  and end positions each occur within ranges.
* `inner` and `outer` must be defined, but the `start` and `end`
  within each may be null.
* If `start` and `end` attributes of `inner` and `outer` are defined,
  they MUST satisfy `outer.start <= inner.start <= inner.end <=
  outer.end`

**Examples**

.. parsed-literal::

   {
     "inner": {
       "end": 30,
       "start": 20,
       "type": "SimpleInterval"
     },
     "outer": {
       "end": 40,
       "start": 10,
       "type": "SimpleInterval"
     },
     "type": "NestedInterval"
   }


.. _CytobandInterval:

CytobandInterval
################

.. important:: VRS currently supports only human cytobands and
   cytoband intervals. Implementers wishing to use VRS for other
   cytogenetic systems are encouraged to open a `GitHub issue`_.

Cytobands refer to regions of chromosomes that are identified by
visible patterns on stained metaphase chromosomes.  They provide a
convenient, memorable, and low-resolution shorthand for chromosomal
segments.

**Computational Definition**

An interval on a stained metaphase chromosome, specified by cytobands.
CytobandIntervals include the regions described by the start and end
cytobands.

**Information Model**

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
     - MUST be "CytobandInterval"
   * - start
     - :ref:`HumanCytoband`
     - 1..1
     - name of Cytoband at the interval start (see below)
   * - end
     - :ref:`HumanCytoband`
     - 1..1
     - name of Cytoband at the interval end (see below)

**Implementation Guidance**

* When using :ref:`CytobandInterval` to refer to human cytogentic
  bands, the following conventions MUST be used. Bands are denoted by
  the arm ("p" or "q") and position (e.g., "22", "22.3", or the symbolic
  values "cen" or "ter") per ISCN conventions [1]_. These conventions
  identify cytobands in order from the centromere towards the telomeres.
  In VRS, we order cytoband coordinates in the p-ter → cen → q-ter
  orientation, analogous to sequence coordinates. This has the
  consequence that bands on the p-arm are represented in descending
  numerical order when selecting cytobands for `start` and `end`.

**Examples**

.. parsed-literal::

   {
     "end": "p22.1",
     "start": "p22.3",
     "type": "CytobandInterval"
   }

.. _SequenceExpression:

Sequence Expression
@@@@@@@@@@@@@@@@@@@

VRS provides several syntaxes for expressing a sequence,
collectively referred to as *Sequence Expressions*. They are:

* :ref:`LiteralSequenceExpression`: An explicit :ref:`Sequence`.
* :ref:`DerivedSequenceExpression`: A sequence that is derived from a
  :ref:`Sequencelocation`.
* :ref:`RepeatedSequenceExpression`: A description of a repeating :ref:`Sequence`.


.. _LiteralSequenceExpression:

LiteralSequenceExpression
#########################

A LiteralSequenceExpression "wraps" a string representation of a sequence for
parallelism with other SequenceExpressions.

**Computational Definition**

An explicit expression of a Sequence.

**Information Model**

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
     - MUST be "LiteralSequenceExpression"
   * - sequence
     - :ref:`Sequence`
     - 1..1
     - The sequence to express

**Example**

.. parsed-literal::

    {
      "sequence": "ACGT",
      "type": "LiteralSequenceExpression"
    }


.. _DerivedSequenceExpression:

DerivedSequenceExpression
#########################

Certain mechanisms of variation result from relocating and
transforming sequence from another location in the genome.
A *derived sequence* is a mechanism for expressing (typically
large) reference subsequences specified by a :ref:`SequenceLocation`.

**Computational Definition**

An expression of a sequence that is derived from a referenced
sequence location.

**Information Model**

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
     - MUST be "DerivedSequenceExpression"
   * - location
     - :ref:`SequenceLocation`
     - 1..1
     - The location describing the sequence

**Example**

.. parsed-literal::

     {
       "location": {
         "interval": {
           "end": 33,
           "start": 22,
           "type": "SimpleInterval"
         },
         "sequence_id": "ga4gh:SQ.0123abcd",
         "type": "SequenceLocation"
       },
       "type": "DerivedSequenceExpression"
     }


.. _RepeatedSequenceExpression:

RepeatedSequenceExpression
##########################

*Repeated Sequence* is a class of sequence expression where a specified
subsequence is repeated multiple times in tandem. Microsatellites are an
example of a common class of repeated sequence, but repeated sequence can
also be used to describe larger subsequence repeats, up to and including
large-scale tandem duplications.

**Computational Definition**

An expression of a sequence comprised of a tandem repeating subsequence.

**Information Model**

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
     - MUST be "RepeatedSequenceExpression"
   * - seq_expr
     - :ref:`SequenceExpression`
     - 1..1
     - an expression of the repeating subsequence
   * - count
     - :ref:`CopyCount`
     - 1..1
     - the inclusive range count of repeated units


**Example**

.. parsed-literal::

    {
      "count": {
        "max": 10,
        "min": 5,
        "type": "CopyCount"
      },
      "seq_expr": {
        "sequence": "CAG",
        "type": "LiteralSequenceExpression"
      },
      "type": "RepeatedSequenceExpression"
    }



.. _Feature:

Feature
@@@@@@@

A *Feature* is a named entity that can be mapped to a
:ref:`Location`. Genes, protein domains, exons, and chromosomes are
some examples of common biological entities that may be Features.

.. _Gene:

Gene
####

A gene is a basic and fundamental unit of heritability. Genes are
functional regions of heritable DNA or RNA that include transcript
coding regions, regulatory elements, and other functional sequence
domains. Because of the complex nature of these many components
comprising a gene, the interpretation of a gene is context dependent.

**Computational definition**

A gene is an authoritative representation of one or more heritable
:ref:`Locations <Location>` that includes all sequence elements
necessary to perform a biological function. A gene may include
regulatory, transcribed, and/or other functional Locations.

**Information Model**

.. list-table::
   :class: reece-wrap
   :header-rows: 1
   :align: left
   :widths: auto

   * - Field
     - Type
     - Limits
     - Description
   * - gene_id
     - :ref:`CURIE`
     - 1..1
     - Authoritative Gene ID (see guidance)
   * - type
     - string
     - 1..1
     - MUST be "Gene"

**Implementation guidance**

* Gene symbols (e.g., "BRCA1") are unreliable keys.  Implementations
  MUST NOT use a gene symbol to define a Gene.
* A gene is specific to a species.  Gene orthologs have distinct
  records in the recommended databases.  For example, the BRCA1 gene
  in humans and the Brca1 gene in mouse are orthologs and have
  distinct records in the recommended gene databases.
* Implementations MUST use authoritative gene namespaces available from
  identifiers.org whenever possible.  Examples include:

    * `hgnc <https://registry.identifiers.org/registry/hgnc>`__
    * `ncbigene <https://registry.identifiers.org/registry/ncbigene>`__
    * `ensembl <https://registry.identifiers.org/registry/ensembl>`__
    * `vgnc <https://registry.identifiers.org/registry/vgnc>`__
    * `mgi <https://registry.identifiers.org/registry/mgi>`__
* The `hgnc` namespace is RECOMMENDED for human
  variation in order to improve interoperability.
* Gene MAY be converted to one or more :ref:`Locations <Location>`
  using external data. The source of such data and mechanism for
  implementation is not defined by this specification.

**Example**

The following examples all refer to the human BRCA1 gene:

.. parsed-literal::

   {
     'gene_id': 'ncbigene:672',
     'type': 'Gene'
   }

Gene is intended to be used as a subject of gene-level annotations,
such as this statement of increased copy number of BRCA1:

.. parsed-literal::

    {
      "copies": {
        "absolute_measure": true,
        "min": 3,
        "type": "CopyCount"
      },
      "subject": {
        "gene_id": "ncbigene:672",
        "type": "Gene"
      },
      "type": "CopyCount"
    }



**Sources**

* `SequenceOntology: gene (SO:0000704)
  <http://www.sequenceontology.org/browser/current_release/term/SO:0000704>`__
  — A region (or regions) that includes all of the sequence elements
  necessary to encode a functional transcript. A gene may include
  regulatory regions, transcribed regions and/or other functional
  sequence regions.

.. _Quantity:

Quantity
@@@@@@@@

A value indicating a multitude or magnitude measure.

.. _CopyCount:

CopyCount
#########

**Computational Definition**

An integer count of copies. Counts are bounded ranges
denoted by minimum and maximum possible values.
Absolute copy number counts may not be smaller than zero.

**Information Model**

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
     - MUST be "CopyCount"
   * - absolute_measure
     - boolean
     - 1..1
     - specifies if the count is an absolute (True)
       or relative (False) measure
   * - min
     - integer
     - 0..1
     - minimum value; inclusive
   * - max
     - integer
     - 0..1
     - maximum value; inclusive

**Implementation Guidance**

* At least one of ``min`` or ``max`` must be specified.
* If both ``min`` and ``max`` are specified, they MUST satisfy ``min
  <= max``.
* If ``min == max``, then the range specifies a single numeric amount.


**Examples**

.. parsed-literal::

   {
     "absolute_measure": True,
     "max": 4,
     "min": 0,
     "type": "CopyCount",
   }


Primitive Concepts
@@@@@@@@@@@@@@@@@@


.. _CURIE:

CURIE
#####

**Computational Definition**

A `CURIE <https://www.w3.org/TR/curie/>`__ formatted string.  A CURIE
string has the structure ``prefix``:``reference`` (W3C Terminology).

**Implementation Guidance**

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
* Implementations MUST use CURIE identifiers verbatim. Implementations
  MAY NOT modify CURIEs in any way (e.g., case-folding).


**Examples**

Identifiers for GRCh38 chromosome 19::

    ga4gh:SQ.IIB53T8CNeJJdUqzn9V_JnRtQadwWCbl
    refseq:NC_000019.10
    grch38:19

See :ref:`identify` for examples of CURIE-based identifiers for VRS
objects.

.. _Residue:

Residue
#######

A residue refers to a specific `monomer`_ within the `polymeric
chain`_ of a `protein`_ or `nucleic acid`_ (Source: `Wikipedia
Residue page`_).

**Computational Definition**

A character representing a specific residue (i.e., molecular species)
or groupings of these ("ambiguity codes"), using `one-letter IUPAC
abbreviations`_ for nucleic acids and amino acids.

.. _one-letter IUPAC abbreviations:
     https://en.wikipedia.org/wiki/International_Union_of_Pure_and_Applied_Chemistry#Amino_acid_and_nucleotide_base_codes

.. _Sequence:

Sequence
########

A *sequence* is a character string representation of a contiguous,
linear polymer of nucleic acid or amino acid :ref:`Residues <Residue>`.
Sequences are the prevalent representation of these polymers,
particularly in the domain of variant representation.

**Computational Definition**

A character string representing :ref:`Residues <Residue>` using the
conventional sequence order (5'-to-3' for nucleic acid sequences, and
amino-to-carboxyl for amino acid sequences) and conforming to the
`one-letter IUPAC abbreviations`_ for sequence representation.

**Information Model**

A string constrained to match the regular expression ``^[A-Z*\-]*$``,
derived from the IUPAC one-letter nucleic acid and amino acid codes.

**Implementation Guidance**

* Sequences MAY be empty (zero-length) strings. Empty sequences are used as the
  replacement Sequence for deletion Alleles.
* Sequences MUST consist of only uppercase IUPAC abbreviations, including ambiguity codes.
* A Sequence provides a stable coordinate system by which an :ref:`Allele` MAY be located and
  interpreted.
* A Sequence MAY have several roles. A "reference sequence" is any Sequence used
  to define an :ref:`Allele`. A Sequence that replaces another Sequence is
  called a "replacement sequence".
* In some contexts outside VRS, "reference sequence" may refer
  to a member of set of sequences that comprise a genome assembly. In the VRS
  specification, any sequence may be a "reference sequence", including those in
  a genome assembly.
* For the purposes of representing sequence variation, it is not
  necessary that Sequences be explicitly "typed" (i.e., DNA, RNA, or
  AA).

.. _HumanCytoband:

HumanCytoband
#############

Cytobands are any of a pattern of stained bands, formed on chromosomes of
cells undergoing metaphase, that serve to identify particular chromosomes.
Human cytobands are predominantly specified by the *International System
for Human Cytogenomic Nomenclature* (ISCN) [1]_.

**Computational Definition**

A character string representing cytobands derived from the
*International System for Human Cytogenomic Nomenclature* (ISCN)
guidelines.

**Information Model**

A string constrained to match the regular expression
``^cen|[pq](ter|([1-9][0-9]*(\.[1-9][0-9]*)?))$``, derived from the
ISCN guidelines [1]_.

.. [1] McGowan-Jordan J (Ed.). *ISCN 2016: An international system
       for human cytogenomic nomenclature (2016).* Karger (2016).


.. _deprecations:

Deprecated and Obsolete Classes
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

.. _SequenceState:

SequenceState
#############

.. warning::

   DEPRECATED. SequenceState will be removed in VRS 2.0. Use
   :ref:`LiteralSequenceExpression` instead.

**Computational Definition**

A :ref:`sequence` as a :ref:`State`. This is the State class
to use for representing "ref-alt" style variation, including
SNVs, MNVs, del, ins, and delins.

**Information Model**

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
     - MUST be "SequenceState"
   * - sequence
     - :ref:`Sequence`
     - 1..1
     - The string of sequence residues that is to be used as the state for other types.

**Examples**

.. parsed-literal::

    {
      "sequence": "T",
      "type": "SequenceState"
    }


.. _State:

State
#####

.. Warning::

   OBSOLETE. State was an abstract class that was intended for future
   growth. It was replaced by SequenceExpressions, which subsumes the
   functionality envisioned for State.  Because State was abstract,
   and therefore purely an internal concept, it was made obsolete at
   the same time that SequenceState was deprecated.

**Computational Definition**

*State* objects are one of two primary components specifying a VRS
:ref:`Allele` (in addition to :ref:`Location`), and the designated
components for representing change (or non-change) of the features
indicated by the Allele Location. As an abstract class, State
currently encompasses single and contiguous :ref:`sequence` changes
(see :ref:`SequenceState`).
