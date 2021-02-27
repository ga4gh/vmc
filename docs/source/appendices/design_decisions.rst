.. _design-decisions:

Design Decisions
!!!!!!!!!!!!!!!!

VRS contributors confronted numerous trade-offs in developing this
specification. As these trade-offs may not be apparent to outside
readers, this section highlights the most significant ones and the
rationale for our design decisions, including:

.. _variation-not-variant:

Variation Rather than Variant
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

The abstract :ref:`Variation` class is intentionally not labeled
"Variant", despite this being the primary term used in other molecular
variation exchange formats (e.g. Variant Call Format, HGVS Sequence
Variant Nomenclature). This is because the term "Variant" as used in
the Genetics community is intended to describe discrete changes in
nucleotide / amino acid sequence. "Variation", in contrast, captures
other classes of molecular variation, including epigenetic alteration
and transcript abundance. Capturing these other classes of variation
is a :doc:`future goal <future_plans>` of VRS, as there are many
annotations that will require these variation classes as the subject.

.. _allele-not-variant:

Allele Rather than Variant
@@@@@@@@@@@@@@@@@@@@@@@@@@

The most primitive sequence assertion in VRS is the :ref:`Allele`
entity. Colloquially, the words "allele" and "variant" have similar
meanings and they are often used interchangeably. However, the VR
contributors believe that it is essential to distinguish the state of
the sequence from the change between states of a sequence. It is
imperative that precise terms are used when modelling data. Therefore,
within VRS, Allele refers to a state and "variant" refers to the change
from one Allele to another.

The word "variant", which implies change, makes it awkward to refer to
the (unchanged) reference allele. Some systems will use an HGVS-like
syntax (e.g., NC_000019.10:g.44906586G>G or NC_000019.10:g.44906586=)
when referring to an unchanged residue. In some cases, such "variants"
are even associated with allele frequencies. Similarly, a predicted
consequence is better associated with an allele than with a variant.

.. _should-normalize:

Implementations should normalize
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

VRS STRONGLY RECOMMENDS that Alleles be :ref:`normalized
<normalization>` when generating :ref:`computed identifiers
<computed-identifiers>`. The rationale for recommending, rather than
requiring, normalization is grounded in dual views of Allele objects
with distinct interpretations:

* Allele as minimal representation of a change in sequence. In this
  view, normalization is a process that makes the representation
  minimal and unambiguous.

* Allele as an assertion of state. In this view, it is reasonable to
  want to assert state that may include (or be composed entirely of)
  reference bases, for which the normalization process would alter the
  intent.

Although this rationale applies only to Alleles, it may have have
parallels with other VRS types. In addition, it is desirable for all
VRS types to be treated similarly.

Furthermore, if normalization were required in order to generate
:ref:`computed-identifiers`, but did not apply to certain instances of
VRS Variation, implementations would likely require secondary
identifier mechanisms, which would undermine the intent of a global
computed identifier.

The primary downside of not requiring normalization is that Variation
objects might be written in non-canonical forms, thereby creating
unintended degeneracy.

Therefore, normalization of all VRS Variation classes is optional in
order to support the view of Allele as an assertion of state on a
sequence.



.. _fully-justified:

Alleles are Fully Justified
@@@@@@@@@@@@@@@@@@@@@@@@@@@

In order to standardize the representation of sequence variation,
Alleles SHOULD be fully justified from the description of the NCBI
`Variant Overprecision Correction Algorithm (VOCA)`_. Furthermore,
normalization rules are identical for all sequence types (DNA, RNA,
and protein). 

The choice of algorithm was relatively straightforward: VOCA is
published, easily understood, easily implemented, and
covers a wide range of cases.

The choice to fully justify is a departure from other common variation
formats. The HGVS nomenclature recommendations, originally published in
1998, require that alleles be right normalized `(3' rule)`_ on all sequence
types. The Variant Call Format (VCF), released as a PDF specification
in 2009, made the conflicting choice to write variants `left (5')
normalized`_ and anchored to the previous nucleotide.

Fully-justified alleles represent an alternate approach. A fully-justified
representation does not make an arbitrary choice of where a variant truly
occurs in a low-complexity region, but rather describes the final and
unambiguous state of the resultant sequence.


.. _inter-residue-coordinates-design:

Inter-residue Coordinates
@@@@@@@@@@@@@@@@@@@@@@@@@@@

Sequence ranges use an inter-residue coordinate system. Inter-residue
coordinate conventions are used in this terminology because they
provide conceptual consistency that is not possible with residue-based
systems.

.. important:: The choice of what to count — residue or inter-residue
               positions — has significant semantic implications for
               the interpretation of coordinates.  Although
               inter-residue coordinates and the "0-based" residue
               coordinates are often numerically identical, we favor
               "inter-residue" to emphasize the meaning of these
               coordinates.

When humans refer to a range of residues within a sequence, the most
common convention is to use an interval of ordinal residue positions
in the sequence. While natural for humans, this convention has several
shortcomings when dealing with sequence variation.

For example, interval coordinates are interpreted as exclusive
coordinates for insertions, but as inclusive coordinates for
substitutions and deletions; in effect, the interpretation of
coordinates depends on the variant type, which is an unfortunate
coupling of distinct concepts.

.. _modelling-language:

Modelling Language
@@@@@@@@@@@@@@@@@@

The VRS collaborators investigated numerous options for modelling data,
generating code, and writing the wire protocol. Required and desired
selection criteria included:

* language-neutral -- or at least C/C++, java, python
* high-quality tooling/libraries
* high-quality code generation
* documentation generation
* supported constructs and data types
   * typedefs/aliases
   * enums
   * lists, maps, and maps of lists/maps
   * nested objects
* protocol versioning (but not necessarily automatic adaptation)

Initial versions of the VRS logical model were implemented in UML,
protobuf, and swagger/OpenAPI, and JSON Schema. We have implemented
our schema in JSON Schema. Nonetheless, it is anticipated that some
adopters of the VRS logical model may implement the specification in
other protocols.

.. _dd-digest-serialization:

Serialization Strategy
@@@@@@@@@@@@@@@@@@@@@@

There are many packages and proposals that aspire to a canonical form
for json in many languages. Despite this, there are no ratified or *de
facto* winners. Many packages have similar names, which makes it
difficult to discern whether they are related or not (often
not). Although some packages look like good single-language
candidates, none are ready for multi-language use. Many seem
abandoned. The need for a canonical json form is evident, and there
was at least one proposal for an ECMA standard.

Therefore, we implemented our own :ref:`serialization format
<digest-serialization>`, which is very similar to `Gibson Canonical
JSON`_ (not to be confused with `OLPC Canonical JSON`_).

.. _Variant Overprecision Correction Algorithm (VOCA): https://www.biorxiv.org/content/10.1101/537449v3.full
.. _SPDI variant data model: https://www.biorxiv.org/content/10.1101/537449v3.full
.. _(3' rule): https://varnomen.hgvs.org/recommendations/general/
.. _left (5') normalized: https://genome.sph.umich.edu/wiki/Variant_Normalization#Definition
.. _Gibson Canonical JSON: http://gibson042.github.io/canonicaljson-spec/
.. _OLPC Canonical JSON: http://wiki.laptop.org/go/Canonical_JSON



.. _dd-not-using-external-chromosome-declarations:

Not using External Chromosome Declarations
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

In :ref:`ChromosomeLocation <chromosomelocation>`, the tuple <species,chromosome name>
refers an archetypal chromosome for the species.  `WikiData
<https://www.wikidata.org/>`_ and `MeSH
<https://www.ncbi.nlm.nih.gov/mesh/>`_ provide such definitions (e.g.,
Human Chr 1 at `WikiData <https://www.wikidata.org/wiki/Q430258>`__
and `MeSH <https://meshb.nlm.nih.gov/record/ui?ui=D002878>`__) and
were considered, and rejected, for use in VRS. Both ontologies were
anticipated to increase complexity that was not justified by the
benefit to VRS.  In addition, data in WikiData are crowd-sourced and
therefore potentially unstable, and the species coverage in MeSH was
insufficient for anticipated VRS uses.
