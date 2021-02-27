.. _ga4gh-identifiers:

Proposal for GA4GH-wide Computed Identifier Standard
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

This appendix describes a proposal for creating a GA4GH-wide standard
for serializing data, computing digests on serialized data, and
constructing CURIE identifiers from the digests.  Essentially, it is a
generalization of the :ref:`computed-identifiers` section.

This standard is proposed now because VRS needs a
well-defined mechanism for generating identifiers.  Changing the
identifier mechanism later will create significant issues for VR
adopters.


Background
@@@@@@@@@@

The GA4GH mission entails structuring, connecting, and sharing data
reliably. A key component of this effort is to be able to *identify*
entities, that is, to associate identifiers with entities. Ideally,
there will be exactly one identifier for each entity, and one entity
for each identifier.  Traditionally, identifiers are assigned to
entities, which means that disconnected groups must coordinate on
identifier assignment.

The computed identifier scheme proposed in VRS
computes identifiers from the data itself.  Because identifers depend
on the data, groups that independently generate the same variation
will generate the same computed identifier for that entity, thereby
obviating centralized identifier systems and enabling identifiers to
be used in isolated settings such as clinical labs. 

The computed identifier mechanism is broadly applicable and useful to
the entire GA4GH ecosystem.  Adopting a common identifier scheme will
make interoperability of GA4GH entities more obvious to consumers,
will enable the entire organization to share common entity definitions
(such as sequence identifiers), and will enable all GA4GH products to
share tooling that manipulate identified data.  In short, it provides
an important consistency within the GA4GH ecosystem.

As a result, we are proposing that the computed identifier scheme
described in VRS be considered for adoption as a
GA4GH-wide standard.  If the proposal is accepted by the GA4GH
executive committee, the current VRS proposal will stand as-is; if the
proposal is rejected, the VRS proposal will be modified to rescope the
computed identifier mechanism to VRS and under admininstration of the
VR team.



Proposal
@@@@@@@@

The following algorithmic processes, described in depth in the VRS
:ref:`computed-identifiers` proposal, are included in this proposal by
reference:

* **GA4GH Digest Serialization** is the process of converting an
  object to a canonical binary form based on JSON and inspired by
  similar (but unratified) JSON standards.  This serialization for is
  used only for the purposes of computing a digest.
* **GA4GH Truncated Digest** is a convention for using `SHA-512`_,
  truncated to 24 bytes, and encoding using `base64url`_.
* **GA4GH Identification** is the CURIE-based syntax for constructing
  a namespaced and typed identifier for an object.


Type Prefixes
@@@@@@@@@@@@@

A GA4GH identifier is proposed to be constructed according to this syntax::

  "ga4gh" ":" type_prefix "." digest

The `digest` is computed as described above. The type_prefix is a
short alphanumeric code that corresponds to the type of object being
represented.  If this propsal is accepted, this "type prefix map"
would be administered by GA4GH.  (Currently, this map is maintained in
a YAML file within the VRS repository, but it would be relocated
on approval of this proposal.)

We propose the following guidelines for type prefixes:

* Prefixes SHOULD be short, approximately 2-4 characters.
* Prefixes SHOULD be for concrete types, not polymorphic parent classes.
* A prefix MUST map 1:1 with a schema type.
* Variation Representation types SHOULD start with V.
* Variation Annotation types SHOULD start with A.


Administration
@@@@@@@@@@@@@@

If accepted, administration of these guidelines should be transferred
to a technical steering committee.  If not accepted, the VR team will
assume administration of the existing prefixes.

