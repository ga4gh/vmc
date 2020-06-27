.. _required-data:

Required External Data
!!!!!!!!!!!!!!!!!!!!!!

All VRS implementations will require external data regarding
sequences and sequence metadata.  The choices of data sources and
access methods are left to implementations.  This section provides
guidance about how to implement required data and helps implementers
estimate effort.  This section is descriptive only: it is not intended
to impose requirements on interface to, or sources of, external data.
For clarity and completeness, this section also describes the contexts
in which external data are used.


Contexts
@@@@@@@@

* **Conversion from other variant formats** When converting from other
  variation formats, implementations MUST translate primary database
  accessions or identifiers (|eg| ``NM_000551.3`` or
  ``refseq:NM_000551.3``) to a GA4GH VRS sequence identifier (
  ``ga4gh:SQ.v_QTc1p-MUYdgrRv4LMT6ByXIOsdw3C_``)

* **Conversion to other variant formats** When converting to other
  variation formats, implementations SHOULD translate GA4GH VR
  sequence identifier ( ``ga4gh:SQ.v_QTc1p-MUYdgrRv4LMT6ByXIOsdw3C_``)
  to primary database identifiers (``refseq:NM_000551.3``) that will
  be more readily recognized by users.

* **Normalization** During :ref:`normalization`, implementations will
  need access to sequence length and sequence contexts. 



Data Services
@@@@@@@@@@@@@

The following tables summarizes data required in the above contexts:

.. list-table:: Data Service Desciptions
   :class: reece-wrap
   :widths: auto
   :header-rows: 1

   * - Data Service
     - Description
     - Contexts
   * - sequence
     - For a given sequence identifier and range, return the
       corresponding subsequence.
     - normalization
   * - sequence length
     - For a given sequence identifier, return the length of the
       sequence
     - normalization
   * - identifier translation
     - For a given sequence identifier and target namespace, return
       all identifiers in the target namespace that are equivelent to
       the given identifier.
     - Conversion to/from other formats


.. note:: Construction of the GA4GH computed identifier for a sequence
          is described in :ref:`computed-identifiers`.



Suggested Implementation
@@@@@@@@@@@@@@@@@@@@@@@@

In order to maximize portability and to insulate implementations from
decisions about external data sources, implementers should consider
writing an abstract data proxy interface that to define a service, and
then implement this interface for each data backend to be
supported. The :ref:`impl-vr-python` `DataProxy class
<https://github.com/ga4gh/vr-python/blob/master/src/ga4gh/vr/extras/dataproxy.py>`__
provides an example of this design pattern and sample replies.

The DataProxy interface defines three methods:

* ``get_sequence(identifier, start, end)``: Given a sequence
  identifier and start and end coordinates, return the corresponding
  sequence segment.
* ``get_metadata(identifier)``: Given a sequence identifier, return a
  dictionary of length, alphabet, and known aliases.
* ``translate_sequence_identifier(identifier, namespace)``: Given a
  sequence identifier, return all aliases in the specified
  namespace. Zero or more aliases may be returned.

|vr-python| implements the DataProxy interface using a local |seqrepo|
instance backend and using a |seqrepo_rs| backend.  A GA4GH refget
implementation has been started, but is pending interface changes to
support lookup using primary database accesssions.

Examples
########

The following examples are taken from |notebooks|:

.. code:: ipython3

    from ga4gh.vr.extras.dataproxy import SeqRepoRESTDataProxy
    seqrepo_rest_service_url = "http://localhost:5000/seqrepo"
    dp = SeqRepoRESTDataProxy(base_url=seqrepo_rest_service_url)

    def get_sequence(identifier, start=None, end=None):
        """returns sequence for given identifier, optionally limited
        to interbase <start, end> interval"""
        return dp.get_sequence(identifier, start, end)
    def get_sequence_length(identifier):
        """return length of given sequence identifier"""
        return dp.get_metadata(identifier)["length"]
    def translate_sequence_identifier(identifier, namespace):
        """return for given identifier, return *list* of equivalent identifiers in given namespace"""
        return dp.translate_sequence_identifier(identifier, namespace)

.. code:: ipython3

    get_sequence_length("ga4gh:SQ.IIB53T8CNeJJdUqzn9V_JnRtQadwWCbl")
    58617616

.. code:: ipython3

    start, end = 44908821-25, 44908822+25
    get_sequence("ga4gh:SQ.IIB53T8CNeJJdUqzn9V_JnRtQadwWCbl", start, end)
    'CCGCGATGCCGATGACCTGCAGAAGCGCCTGGCAGTGTACCAGGCCGGGGC'

.. code:: ipython3

    translate_sequence_identifier("GRCh38:19", "ga4gh")
    ['ga4gh:SQ.IIB53T8CNeJJdUqzn9V_JnRtQadwWCbl']

.. code:: ipython3

    translate_sequence_identifier("ga4gh:SQ.IIB53T8CNeJJdUqzn9V_JnRtQadwWCbl", "GRCh38")
    ['GRCh38:19', 'GRCh38:chr19']
