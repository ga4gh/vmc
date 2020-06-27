.. _normalization:

Normalization
!!!!!!!!!!!!!

Certain insertion or deletion alleles may be represented ambiguously
when using conventional sequence normalization, resulting in
significant challenges when comparing such alleles.

VRS describes a "fully-justified" normalization algorithm
inspired by NCBI's Variant Overprecision Correction Algorithm [1]_.
Fully-justified normalization expands such ambiguous representation
over the entire region of ambiguity, resulting in an *unambiguous*
representation that may be readily compared with other alleles.

VRS RECOMMENDS that Alleles at precise locations are
normalized to a fully justified form unless there is a compelling
reason to do otherwise.

The process for fully justifying two alleles (reference sequence and
alternate sequence) at an interval is outlined below.

1. Trim sequences:

   * Remove suffixes common to all alleles, if any. Decrement
     the interval end position by the length of the trimmed suffix.
   * Remove prefixes common to all alleles, if any. Increment
     the interval start position by the length of the trimmed prefix.
   * If neither allele is empty, the allele pairs represent a alleles
     that do not have common prefixes or suffixes.  Normalization is not
     applicable and the trimmed alleles are returned.

2. Determine bounds of ambiguity:

   * Left roll: While the terminal base of all non-empty alleles is
     equal to the base *prior* to the current position, circularly
     permute all alleles *rightward* and move the current position
     *leftward*. When terminating, return `left_roll`, the number
     of steps rolled leftward.
   * Right roll: Symmetric case of left roll, returning `right_roll`,
     the number of steps rolled rightward.

3. Update position and alleles:

   * To each trimmed allele, prepend the `left_roll` bases prior to the
     trimmed allele position and append the `right_roll` bases after
     the trimmed allele position.
   * Expand the trimmed allele position by decrementing the start by
     `left_roll` and incrementing the end by `right_roll`.


.. _normalization-diagram:

.. list-table::
     **VRS Justified Normalization** A demonstration of fully justifying an insertion allele.
   :class: reece-wrap
   :header-rows: 1
   :widths: 40 15 20
   :align: left

   *  -  Steps
      -  | Interbase Position
         | and Alleles
      -  | Resulting Allele Set
         | (All alleles in this column result
	 | in the same empirical sequence change.)
   *  -  0. Given allele ``S:g.5_6delinsCAGCA`` defined on reference sequence S=TCAGCAGCT
      -  | (4,6)
         | (“CA”, “CAGCA”)
      -  .. math:: TCAG \Bigl[ \frac{CA}{CAGCA} \Bigr] GCT

   *  -  1. Trimming

            Remove prefix common to all alleles, if any, and update start position. Remove suffix common to all alleles, if any, and update end position.

            **Note:**  This example shows removing C prefix and A suffix.
            Equivalently in this case, CA prefix or CA suffix could be removed.
      -  | (5,5)
         | (“”, “AGC”)
      -  .. math:: TCAGC \Bigl[ \frac{}{AGC} \Bigr] AGCT  ①
   *  -  2. Condition: One allele must be empty.

            If the reference allele is empty, the allele set represents an insertion in the reference.

            If the alternate allele is empty, the allele set represents a deletion in the reference.

            If neither is true, the allele set represents a substitution, which is not subject to further normalization.
      -
      -
   *  -  3. Roll Left

            Begin with trimmed alleles ①.

            While the terminal base of all non-empty alleles equals the base
            prior to the current position, circularly permute all alleles right
            one step and move the start left one position.

            Shown: The 4 incremental steps of rolling left.
      -  | (1,1)
         | (“”, “CAG”)
      -  .. math::
            TCAGC \Bigl[ \frac{}{AGC} \Bigr] AGCT ①\\
            TCAG \Bigl[ \frac{}{CAG} \Bigr] CAGCT   \\
            TCA \Bigl[ \frac{}{GCA} \Bigr] GCAGCT   \\
            TC \Bigl[ \frac{}{AGC} \Bigr] AGCAGCT   \\
            T \Bigl[ \frac{}{CAG} \Bigr] CAGCAGCT   \\
            \Rightarrow left\_roll = 4
   *  -  4. Roll Right

            Symmetric case of step 3.
      -  | (8,8)
         | (“”, “AGC”)
      -  .. math::
            TCAGC \Bigl[ \frac{}{AGC} \Bigr] AGCT ①\\
            TCAGCA \Bigl[ \frac{}{GCA} \Bigr] GCT   \\
            TCAGCAG \Bigl[ \frac{}{CAG} \Bigr] CT   \\
            TCAGCAGC \Bigl[ \frac{}{AGC} \Bigr] T   \\
            \Rightarrow right\_roll = 3
   *  -  5. Update position and alleles to fully justify within region of ambiguity.

            To each trimmed allele (①), prepend the *left_roll* preceding reference
            bases and append the *right_roll* following reference bases
            (corresponding to the interbase reference spans (1,5) and (5,8) respectively).

            Decrement the start position by *left_roll*, and increment the end
            position by *right_roll*.
      -  | (1,8)
         | (“CAGCAGC”,
         | “CAGCAGCAGC”)
      -  .. math::
            TCAGC \Bigl[ \frac{}{AGC} \Bigr] AGCT ①\\
            T \Bigl[ \frac{CAGCAGC}{CAGCAGCAGC} \Bigr] T

**References**

.. [1] Holmes, J. B., Moyer, E., Phan, L., Maglott, D. &
       Kattman, B. L. *SPDI: Data Model for Variants and Applications
       at NCBI.* Bioinformatics (2020 March 15). `doi:10.1093/bioinformatics/btz856`_

.. _doi:10.1093/bioinformatics/btz856: https://doi.org/10.1093/bioinformatics/btz856
