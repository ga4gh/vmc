.. _truncated-digest-collision-analysis:

Truncated Digest Timing and Collision Analysis
==============================================

The GA4GH Digest uses a truncated SHA-512 digest in order to generate a
unique identifier based on data that defines the object. This notebook
discusses the choice of SHA-512 over other digest methods and the choice
of truncation length.

.. note:: Please see `this Jupyter notebook
  <https://github.com/biocommons/biocommons.seqrepo/blob/master/docs/Truncated%20Digest%20Collision%20Analysis.ipynb>`__
  in `Python SeqRepo library
  <https://github.com/biocommons/biocommons.seqrepo>`__ for code and
  updates.  A fuller explanation is given in [Hart2020]_.


Conclusions
-----------

-  The computational time for SHA-512 is similar to that of other digest
   methods. Given that it is believed to distribute input bits more
   uniformly with no increased computational cost, it should be
   preferred for our use (and likely most uses).
-  24 bytes (192 bits) of digest is *ample* for VRS uses. Arguably, we
   could choose much smaller without significant risk of collision.

.. code:: ipython3

    import hashlib
    import math
    import timeit
    
    from IPython.display import display, Markdown
    
    from ga4gh.vrs.extras.utils import _format_time
    
    algorithms = {'sha512', 'sha1', 'sha256', 'md5', 'sha224', 'sha384'}


Digest Timing
-------------

This section provides a rationale for the selection of SHA-512 as the
basis for the Truncated Digest.

.. code:: ipython3

    def blob(l):
        """return binary blob of length l (POSIX only)"""
        return open("/dev/urandom", "rb").read(l)
    
    def digest(alg, blob):
        md = hashlib.new(alg)
        md.update(blob)
        return md.digest()
    
    def magic_run1(alg, blob):
        t = %timeit -o digest(alg, blob)
        return t
    
    def magic_tfmt(t):
        """format TimeitResult for table"""
        return "{a} ± {s} ([{b}, {w}])".format(
            a = _format_time(t.average),
            s = _format_time(t.stdev),
            b = _format_time(t.best),
            w = _format_time(t.worst),
        )

.. code:: ipython3

    blob_lengths = [100, 1000, 10000, 100000, 1000000]
    blobs = [blob(l) for l in blob_lengths]

.. code:: ipython3

    table_rows = []
    table_rows += [["algorithm"] + list(map(str,blob_lengths))]
    table_rows += [["-"] * len(table_rows[0])]
    for alg in sorted(algorithms):
        r = [alg]
        for i in range(len(blobs)):
            blob = blobs[i]
            t = timeit.timeit(stmt='digest(alg, blob)', setup='from __main__ import alg, blob, digest', number=1000)
            r += [_format_time(t)]
        table_rows += [r]
    table = "\n".join(["|".join(map(str,row)) for row in table_rows])
    display(Markdown(table))



========= ======= ======= ======= ====== =======
algorithm 100     1000    10000   100000 1000000
========= ======= ======= ======= ====== =======
md5       1.02 ms 2.51 ms 23.4 ms 145 ms 1.44 s
sha1      1.02 ms 1.91 ms 11.3 ms 101 ms 1 s
sha224    1.21 ms 3.16 ms 23.1 ms 224 ms 2.2 s
sha256    1.18 ms 3.29 ms 23.3 ms 223 ms 2.2 s
sha384    1.17 ms 2.54 ms 16 ms   150 ms 1.47 s
sha512    1.2 ms  2.55 ms 16.1 ms 148 ms 1.47 s
========= ======= ======= ======= ====== =======


**Conclusion: SHA-512 computational time is comparable to that of other
digest methods.**

This is result was not expected initially. On further research, there is
a clear explanation: The SHA-2 series of digests (which includes
SHA-224, SHA-256, SHA-384, and SHA-512) is defined using 64-bit
operations. When an implementation is optimized for 64-bit systems (as
used for these timings), the number of cycles is essentially halved when
compared to 32-bit systems and digests that use 32-bit operations. SHA-2
digests are indeed much slower than SHA-1 and MD5 on 32-bit systems, but
such legacy platforms is not relevant to the Truncated Digest.


Collision Analysis
------------------

Our question: **For a hash function that generates digests of length b
(bits) and a corpus of m messages, what is the probability p that there
exists at least one collision?** This is the so-called Birthday Problem
[6].

Because analyzing digest collision probabilities typically involve
choices of mathematical approximations, multiple “answers” appear
online. This section provides a quick review of prior work and extends
these discussions by focusing the choice of digest length for a desired
collision probability and corpus size.

Throughout the following, we’ll use these variables:

-  :math:`P` = Probability of collision
-  :math:`P'` = Probability of no collision
-  :math:`b` = digest size, in bits
-  :math:`s` = digest space size, :math:`s = 2^b`
-  :math:`m` = number of messages in corpus

The length of individual messages is irrelevant.

References
~~~~~~~~~~

-  [1] http://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf
-  [2] https://tools.ietf.org/html/rfc3548#section-4
-  [3] http://stackoverflow.com/a/4014407/342839
-  [4] http://stackoverflow.com/a/22029380/342839
-  [5] http://preshing.com/20110504/hash-collision-probabilities/
-  [6] https://en.wikipedia.org/wiki/Birthday_problem
-  [7] https://en.wikipedia.org/wiki/Birthday_attack

Background: The Birthday Problem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Directly computing the probability of one or more collisions, :math:`P`,
in a corpus is difficult. Instead, we first seek to solve for
:math:`P'`, the probability that a collision does not exist (i.e., that
the digests are unique). Because are only two outcomes,
:math:`P + P' = 1` or, equivalently, :math:`P = 1 - P'`.

For a corpus of size :math:`m=1`, the probabability that the digests of
all :math:`m=1` messages are unique is (trivially) 1:

.. math:: P' = s/s = 1

because there are :math:`s` ways to choose the first digest from among
:math:`s` possible values without a collision.

For a corpus of size :math:`m=2`, the probabability that the digests of
all :math:`m=2` messages are unique is:

.. math:: P' = 1 \times (\frac{s-1}{s})

because there are :math:`s-1` ways to choose the second digest from
among :math:`s` possible values without a collision.

Continuing this logic, we have:

.. math:: P' = \prod\nolimits_{i=0}^{m-1} \frac{(s-i)}{s}

or, equivalently,

.. math:: P' = \frac{s!}{s^m \cdot (s-m)!}

When the size of the corpus becomes greater than the size of the digest
space, the probability of uniques is zero by the pigeonhole principle.
Formally, the above equation becomes:

.. math::


   P' = \left\{
           \begin{array}{ll}
               1    &    \text{if }m = 0 \\
               \prod\nolimits_{i=0}^{m-1} \frac{(s-i)}{s}    &    \text{if }1 \le m\le s\\
               0    &    \text{if }m \gt s
           \end{array}
        \right.

For the remainder of this section, we’ll focus on the case where
:math:`1 \le m \ll s`. In addition, notice that the brute force
computation is not feasible in practice because :math:`m` and :math:`s`
will be very large (both :math:`\gg 2^9`).

Approximation #1: Taylor approximation of terms of P’
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Taylor series expansion of the exponential function is

.. math:: e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + ...

For :math:`|x| \ll 1`, the expansion is dominated by the first terms and
therecore :math:`e^x \approx 1 + x`.

In the above expression for :math:`P'`, note that the product term
:math:`(s-i)/s` is equivalent to :math:`1-i/s`. Combining this with the
Taylor expansion, where :math:`x = -i/s` (⇒ :math:`m \ll s`):

.. math::


   \begin{split}
   P' & \approx \prod\nolimits_{i=0}^{m-1} e^{-i/s} \\
      & = e^{-m(m-1)/2s}
   \end{split}

(The latter equivalence comes from converting the product of exponents
to a single exponent of a summation of :math:`-i/s` terms, factoring out
:math:`1/s`, and using the series sum equivalence
:math:`\sum\nolimits_{j=0}^{n} j = n(n+1)/2` for :math:`n\ge0`.)

Approximation #2: Taylor approximation of P’
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The above result for :math:`P'` is also amenable to Taylor
approximation. Setting :math:`x = -m(m-1)/2s`, we continue from the
previous derivation:

.. math::


   \begin{split}
   P' & \approx e^{-(m(m-1)/2s} \\
      & \approx 1 + \frac{-m(m-1)}{2s}
   \end{split}

Approximation #3: Square approximation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For large :math:`m`, we can approximate :math:`m(m-1)` as :math:`m^2` to
yield

.. math:: P' \approx 1-m^2/2s


Summary of equations
~~~~~~~~~~~~~~~~~~~~

We may now summarize equations to approximate the probability of digest
collisions.

.. list-table:: Summary of Equations
   :header-rows: 1
   :widths: 15 30 20 20 15

   * - Method
     - Probability of uniqueness(:math:`P'`)
     - Probability of collision(:math:`P=1-P'`)
     - Assumptions
     - Source/Comparison
   * - exact
     - :math:`\prod_\nolimits{i=0}^{m-1} \frac{(s-i)}{s}`     
     - :math:`1-P'`
     - :math:`1 \le m\le s`
     - [1]
   * - Taylor approximation on #1
     - :math:`e^{-m(m-1)/2s}`
     - :math:`1-P'` 
     - :math:`m \ll s`
     - [1]
   * - Taylor approximation on #2
     - :math:`1 - \frac{m(m-1)}{2s}`
     - :math:`\frac{m(m-1)}{2s}`
     - (same)
     - [1]
   * - Large square approximation
     - :math:`1 - \frac{m^2}{2s}`
     - :math:`\frac{m^2}{2s}` 
     - (same)
     - [2] (where :math:`s=2^n`)

-  [1] https://en.wikipedia.org/wiki/Birthday_problem
-  [2] http://preshing.com/20110504/hash-collision-probabilities/


Choosing a digest size
----------------------

Now, we turn the problem around:

   **What digest length :math:`b` is required to achieve a collision
   probability less than :math:`P` for :math:`m` messages?**

From the above summary, we have :math:`P = m^2 / 2s` for
:math:`m \ll s`. Rewriting with :math:`s=2^b`, we have the probability
of a collision using :math:`b` bits with :math:`m` messages (sequences)
is:

.. math:: P(b, m) = m^2 / 2^{b+1}

Note that the collision probability depends on the number of messages,
but not their size.

Solving for the minimum number of *bits* :math:`b` as a function of an
expected number of sequences :math:`m` and a desired tolerance for
collisions of :math:`P`:

.. math:: b(m, P) = \log_2{\left(\frac{m^2}{P}\right)} - 1

This equation is derived from equations that assume that
:math:`m \ll s`, where :math:`s = 2^b`. When computing :math:`b(m,P)`,
we’ll require that :math:`m/s \le 10^{-3}` as follows:

.. math:: m/s \le 10^{-3}

is approximately equivalent to:

.. math:: m/2^b \le 2^{-5}

.. math:: m \le 2^{b-5}

.. math:: log_2 m \le b-5

.. math:: b \ge 5 + log_2 m

For completeness:
~~~~~~~~~~~~~~~~~

Solving for the number of messages:

.. math:: m(b, P) = \sqrt{P * 2^{b+1}}

This equation is not used further in this analysis.

.. code:: ipython3

    def b2B3(b):
        """Convert bits b to Bytes, rounded up modulo 3
    
        We report modulo 3 because the intent will be to use Base64 encoding, which is
        most efficient when inputs have a byte length modulo 3. (Otherwise, the resulting
        string is padded with characters that provide no information.)
        
        """
        return math.ceil(b/8/3) * 3
        
    def B(P, m):
        """return the number of bits needed to achieve a collision probability
        P for m messages
    
        Assumes m << 2^b.
        
        """
        b = math.log2(m**2 / P) - 1
        if b < 5 + math.log2(m):
            return "-"
        return b2B3(b)

.. code:: ipython3

    m_bins = [1E6, 1E9, 1E12, 1E15, 1E18, 1E21, 1E24, 1E30]
    P_bins = [1E-30, 1E-27, 1E-24, 1E-21, 1E-18, 1E-15, 1E-12, 1E-9, 1E-6, 1E-3, 0.5]

.. code:: ipython3

    table_rows = []
    table_rows += [["#m"] + ["P<={P}".format(P=P) for P in P_bins]]
    table_rows += [["-"] * len(table_rows[0])]
    for n_m in m_bins:
        table_rows += [["{:g}".format(n_m)] + [B(P, n_m) for P in P_bins]]
    table = "\n".join(["|".join(map(str,row)) for row in table_rows])
    table_header = "### digest length (bytes) required for expected collision probability $P$ over $m$ messages \n"
    display(Markdown(table_header +  table))



digest length (bytes) required for expected collision probability :math:`P` over :math:`m` messages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| #m  | P<= | P<= | P<= | P<= | P<= | P<= | P<= | P<= | P<= | P<= | P<= |
|     | 1e- | 1e- | 1e- | 1e- | 1e- | 1e- | 1e- | 1e- | 1e- | 0.0 | 0.5 |
|     | 30  | 27  | 24  | 21  | 18  | 15  | 12  | 09  | 06  | 01  |     |
+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+=====+
| 1e+ | 18  | 18  | 15  | 15  | 15  | 12  | 12  | 9   | 9   | 9   | 6   |
| 06  |     |     |     |     |     |     |     |     |     |     |     |
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 1e+ | 21  | 21  | 18  | 18  | 15  | 15  | 15  | 12  | 12  | 9   | 9   |
| 09  |     |     |     |     |     |     |     |     |     |     |     |
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 1e+ | 24  | 24  | 21  | 21  | 18  | 18  | 15  | 15  | 15  | 12  | 12  |
| 12  |     |     |     |     |     |     |     |     |     |     |     |
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 1e+ | 27  | 24  | 24  | 24  | 21  | 21  | 18  | 18  | 15  | 15  | 15  |
| 15  |     |     |     |     |     |     |     |     |     |     |     |
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 1e+ | 30  | 27  | 27  | 24  | 24  | 24  | 21  | 21  | 18  | 18  | 15  |
| 18  |     |     |     |     |     |     |     |     |     |     |     |
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 1e+ | 30  | 30  | 30  | 27  | 27  | 24  | 24  | 24  | 21  | 21  | 18  |
| 21  |     |     |     |     |     |     |     |     |     |     |     |
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 1e+ | 33  | 33  | 30  | 30  | 30  | 27  | 27  | 24  | 24  | 24  | 21  |
| 24  |     |     |     |     |     |     |     |     |     |     |     |
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+
| 1e+ | 39  | 39  | 36  | 36  | 33  | 33  | 30  | 30  | 30  | 27  | 27  |
| 30  |     |     |     |     |     |     |     |     |     |     |     |
+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+

