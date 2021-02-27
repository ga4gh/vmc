.. _implementations:

Implementations
!!!!!!!!!!!!!!!

The libraries and applications listed below have implemented the GA4GH
Variation Representation Specification to store and exchange variation
data. They are listed here to demonstrate utility and as a resource
for those considering implementing VRS. These packages are not
supported by GA4GH.


Libraries
@@@@@@@@@

Libraries facilitate the use of the VRS, but do not implement a
particular use or application.  Although there is only one library
currently, it is expected that others will eventually appear as
VRS is adopted.


.. _impl-vrs-python:

vrs-python: GA4GH VRS Python Implementation
###########################################

The |vrs-python| is an implementation for the GA4GH VRS.  It
supports all types covered by the VRS, implements Allele
normalization and computed identifier generation, and provides "extra"
features such as translation from HGVS, SPDI, and VCF formats.

|VRS| MAY be used without using the Python implementation.


Applications and Web Services
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

Applications implement VRS to support specific use cases.
Projects known to implement VRS are listed below. Descriptions are
provided by the application authors.


.. _impl-allele-registry:

ClinGen Allele Registry
#######################

ClinGen Allele Registry [1]_ provides identifiers for more than 900
million variants. Each identifier (canonical allele identifiers:
CAIds) is an abstract concept which represents a group of identical
variants based on alignment. Identifiers are retrievable irrespective
of the reference sequence and normalization status.

As a Driver Project for GA4GH, `ClinGen Allele Registry
<https://reg.clinicalgenome.org>`__ implements two standards: RefGet
and VRS in the first implementation.

The API endpoints that support data retrieval in this two key
standards are summarized in the following table.

**HOST**: `https//reg.clinicalgenome.org/ <https://reg.clinicalgenome.org>`__

.. csv-table::
   :header: API Path, Parameters, Response Format, Example,
   :align: left

   **RefGet**,,,
   [GET] /sequence/service-info, \-, Refget v1.0.0, `/sequence/service-info <https://reg.clinicalgenome.org/sequence/service-info>`__
   [GET] /sequence/{id}, id => TRUNC512 digest for reference sequence, Refget v1.0.0, `/sequence/vYfm5TA_F-_BtIGjfzjGOj8b6IK5hCTx <https://reg.clinicalgenome.org/sequence/F-LrLMe1SRpfUZHkQmvkVKFEGaoDeHul?start=2232131&end=2232145>`__
   [GET] /sequence/{id}/metadata, id => TRUNC512 digest for reference sequence, Refget v1.0.0, `/sequence/vYfm5TA_F-_BtIGjfzjGOj8b6IK5hCTx/metadata <https://reg.clinicalgenome.org/sequence/F-LrLMe1SRpfUZHkQmvkVKFEGaoDeHul/metadata>`__
   **VRS**,,,
   [GET] /vrAllele?hgvs={hgvs}, hgvs => HGVS expression, VRS v1.0, `/vrAllele?hgvs=NC_000007.14:g.55181320A>T <https://reg.clinicalgenome.org/vrAllele?hgvs=NC_000007.14:g.55181320A%3ET>`__  `/vrAllele?hgvs=NC_000007.14:g.55181220del <https://reg.clinicalgenome.org/vrAllele?hgvs=NC_000007.14:g.55181220del>`__

Support for GA4GH refget and VRS provided in ClinGen Allele
Registry is independent from VRS-Python. Support for this community
standards is implemented in ClinGen Allele Registry through extension
of code written in C++.


.. _impl-brca-exchange:

BRCA Exchange
#############

The goal of BRCA Exchange (https://brcaexchange.org/) is to expand approaches to integrate and disseminate information on BRCA variants in Hereditary Breast and Ovarian Cancer (HBOC), as an exemplar for additional genes and additional heritable disorders [2]_.  The BRCA Exchange web portal provides information on the annotation and clinical interpretation of 40,000 variants to date.  As a GA4GH Driver Project, BRCA Exchange is contributing to and adopting the Variant Annotation (VA), Pedigree (Ped) and Variant Representation (VRS) standards.  BRCA Exchange displays the VRS identifiers of all variants, and provides an API endpoint for querying variants by VRS identifier.  With this endpoint, if BRCA Exchange contains a variant that matches the VRS identifier, it returns data on that variant.  Otherwise, it returns a Server 500 error.

Example query:
   * https://brcaexchange.org/backend/data/vrid?vr_id=ga4gh:VA.jgT2lU4y55WshIgcW__MVzHBnnga_iZL

.. _impl-vicc:

VICC Meta-knowledgebase
#######################

The Variant Interpretation for Cancer Consortium (VICC;
https://cancervariants.org) has a collection of ~20K clinical
interpretations associated with ~3,500 somatic variations and variation
classes in a harmonized meta-knowledgebase [3]_ (see documentation at
http://docs.cancervariants.org). Each interpretation is be linked to
one or more variations or a variation class.

As a Driver Project for GA4GH, VICC is contributing to and/or
adopting several GA4GH standards, including VRS, Variant Annotation (VA), 
and service_info. VICC supports queries on all VRS computed
identifiers at the searchAssociations endpoint (`vicc-docs`_).
Features associated with each interpretation are represented as VRS
objects.

Example queries:
  * **Allele:** https://search.cancervariants.org/api/v1/associations?size=10&from=1&q=ga4gh:VA.mJbjSsW541oOsOtBoX36Mppr6hMjbjFr
  * **SequenceLocation:** https://search.cancervariants.org/api/v1/associations?size=10&from=1&q=ga4gh:SL.gJeEs42k4qeXOKy9CJ515c0v2HTu8s4K
  * **Text:** https://search.cancervariants.org/api/v1/associations?size=10&from=1&q=ga4gh:VT.9Wer7KrxALcPRDRGVKOEzf9ZEKZpOKK0

**References:**

.. [1] Pawliczek P, Patel RY, et al. *ClinGen Allele Registry links
       information about genetic variants.* Hum Mutat 11
       (2018). `doi:10.1002/humu.23637`_
.. [2] Cline, M.S., et al.  *BRCA Challenge: BRCA Exchange as a global resource for
       variants in BRCA1 and BRCA2.* PLoS Genet. 2018 Dec 26;14(12):e1007752.
       `doi:10.1371/journal.pgen.1007752`_
.. [3] Wagner, A.H., et al. *A harmonized meta-knowledgebase of
       clinical interpretations of cancer genomic variants.* bioRxiv
       366856 (2018). `doi:10.1101/366856`_

.. _vicc-docs: https://search.cancervariants.org/api/v1/ui/#!/Associations/searchAssociations
.. _doi:10.1101/366856: https://doi.org/10.1101/366856
.. _doi:10.1002/humu.23637: https://onlinelibrary.wiley.com/doi/full/10.1002/humu.23637
.. _doi:10.1371/journal.pgen.1007752: https://www.doi.org/10.1371/journal.pgen.1007752
