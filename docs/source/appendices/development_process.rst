Development Process
@@@@@@@@@@@@@@@@@@@

Versioning
##########

VRS will follow GA4GH `recommendation for semantic versioning`_
with semver 2.0. The VRS GitHub repository will maintain the
latest development code on the master branch for community review (see
:ref:`Release Cycle <release-cycle>`).

.. _release-cycle:

Release Cycle
#############

Planned Features
$$$$$$$$$$$$$$$$
Feature requests from the community are made through the generation of
`GitHub issues on the VRS repository`_, which are open for
public review and discussion. Feature requests identified to support
an unmet need are scheduled for discussion
in our weekly VR calls. These discussions are used to inform whether
or not a feature will be planned for development. The :ref:`Project
Leadership <project-leadership>` is responsible for making the final
determination on whether a feature is to be added to VRS.

Requirements Gathering
$$$$$$$$$$$$$$$$$$$$$$
Once a feature is planned for production, an issue requesting
community feedback on use cases and technical requirements will be
constructed (see `example requirement issues`_).

Feature Development
$$$$$$$$$$$$$$$$$$$
Features will be developed to meet gathered requirements. Features
ready for public review MAY be merged into the master branch by pull
request through review and approval by at least one (non-authoring)
:ref:`Project Maintainer <project-maintainers>`. Merged commits MAY be
tagged as alpha releases when needed.

Version Review and Release
$$$$$$$$$$$$$$$$$$$$$$$$$$

After completion of all planned features for a new minor or major
version, a request for community review will be indicated by a beta
release of the new version. Community stakeholders involved in the
feature requests and requirements gathering for the included features
are notified by Project Maintainers for review and approval of the
release. After a community review period of at least two weeks, the
Project Leadership will review and address any raised concerns for the
reviewed version.

After passing review, new minor versions are released to
production. If any features in the reviewed version are deemed to be
significant additions to the specification by the Project Leadership, or if
it is a major version change, instead a release candidate version will
be released and submitted for GA4GH product approval. After approval,
the new version is released to production.

Leadership
##########

.. _project-leadership:

Project Leadership
$$$$$$$$$$$$$$$$$$
As a product of the Genomic Knowledge Standards (GKS) Work Stream,
project leadership is comprised of the `Work Stream leadership`_:

* Alex Wagner (`@ahwagner <https://github.com/ahwagner>`__)
* Andy Yates (`@andrewyatz <https://github.com/andrewyatz>`__)
* Bob Freimuth (`@rrfreimuth <https://github.com/rrfreimuth>`__)
* Javier Lopez (`@javild <https://github.com/javild>`__)
* Larry Babb (`@larrybabb <https://github.com/larrybabb>`__)
* Matt Brush (`@mbrush <https://github.com/mbrush>`__)
* Melissa Konopko (`@MKonopko <https://github.com/MKonopko>`__)
* Reece Hart (`@reece <https://github.com/reece>`__)

.. _project-maintainers:

Project Maintainers
$$$$$$$$$$$$$$$$$$$
Project maintainers are the leads of the GKS Variation Representation working group:

* Alex Wagner (`@ahwagner <https://github.com/ahwagner>`__)
* Larry Babb (`@larrybabb <https://github.com/larrybabb>`__)
* Reece Hart (`@reece <https://github.com/reece>`__)


.. _recommendation for semantic versioning: https://docs.google.com/document/d/1UUJSnsPw32W5r1jaJ0vI11X0LLLygpAC9TNosjSge_w/edit#heading=h.h5gpuoaxcrgy
.. _GitHub issues on the VRS repository: https://github.com/ga4gh/vr-spec/issues
.. _example requirement issues: https://github.com/ga4gh/vr-spec/labels/requirements
.. _Work Stream leadership: https://ga4gh-gks.github.io/
