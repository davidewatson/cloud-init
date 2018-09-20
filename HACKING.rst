*********************
Hacking on cloud-init
*********************

This document describes how to contribute changes to cloud-init.
It assumes you have a `Launchpad`_ account, and refers to your launchpad user
as ``LP_USER`` throughout.

Do these things once
====================

* To contribute, you must sign the Canonical `contributor license agreement`_

  If you have already signed it as an individual, your Launchpad user will be listed in the `contributor-agreement-canonical`_ group.  Unfortunately there is no easy way to check if an organization or company you are doing work for has signed.  If you are unsure or have questions, email `Scott Moser <mailto:scott.moser@canonical.com>`_ or ping smoser in ``#cloud-init`` channel via freenode.

  When prompted for 'Project contact' or 'Canonical Project Manager' enter
  'Scott Moser'.

* Configure git with your email and name for commit messages.

  Your name will appear in commit messages and will also be used in
  changelogs or release notes.  Give yourself credit!::

    git config user.name "Your Name"
    git config user.email "Your Email"

* Clone the upstream `repository`_ on Launchpad::

    git clone https://git.launchpad.net/cloud-init
    cd cloud-init

  There is more information on Launchpad as a git hosting site in
  `Launchpad git documentation`_.

* Create a new remote pointing to your personal Launchpad repository.
  This is equivalent to 'fork' on github.

  .. code:: sh

    git remote add LP_USER ssh://LP_USER@git.launchpad.net/~LP_USER/cloud-init
    git push LP_USER master

.. _repository: https://git.launchpad.net/cloud-init
.. _contributor license agreement: http://www.canonical.com/contributors
.. _contributor-agreement-canonical: https://launchpad.net/%7Econtributor-agreement-canonical/+members
.. _Launchpad git documentation: https://help.launchpad.net/Code/Git

Do these things for each feature or bug
=======================================

* Create a new topic branch for your work::

    git checkout -b my-topic-branch

* Make and commit your changes (note, you can make multiple commits,
  fixes, more commits.)::

    git commit

* Run unit tests and lint/formatting checks with `tox`_::

    tox

* Push your changes to your personal Launchpad repository::

    git push -u LP_USER my-topic-branch

* Use your browser to create a merge request:

  - Open the branch on Launchpad.

    - You can see a web view of your repository and navigate to the branch at:

      ``https://code.launchpad.net/~LP_USER/cloud-init/``

    - It will typically be at:

      ``https://code.launchpad.net/~LP_USER/cloud-init/+git/cloud-init/+ref/BRANCHNAME``

      for example, here is larsks move-to-git branch: https://code.launchpad.net/~larsks/cloud-init/+git/cloud-init/+ref/feature/move-to-git

  - Click 'Propose for merging'
  - Select 'lp:cloud-init' as the target repository
  - Type '``master``' as the Target reference path
  - Click 'Propose Merge'
  - On the next page, hit 'Set commit message' and type a git combined git style commit message like::

      Activate the frobnicator.

      The frobnicator was previously inactive and now runs by default.
      This may save the world some day.  Then, list the bugs you fixed
      as footers with syntax as shown here.

      The commit message should be one summary line of less than
      74 characters followed by a blank line, and then one or more
      paragraphs describing the change and why it was needed.

      This is the message that will be used on the commit when it
      is sqaushed and merged into trunk.

      LP: #1

Then, someone in the `cloud-init-dev`_ group will review your changes and
follow up in the merge request.

Feel free to ping and/or join ``#cloud-init`` on freenode irc if you
have any questions.

.. _tox: https://tox.readthedocs.io/en/latest/
.. _Launchpad: https://launchpad.net
.. _cloud-init-dev: https://launchpad.net/~cloud-init-dev/+members#active

Building source packages for PPA
================================

* Creating a Docker-based env for Building

    docker run --rm -it -v ~/src:/src -v ~/.gnupg:/root/.gnupg ubuntu:xenial /bin/bash
    apt-get update
    apt-get install -y git make devscripts debhelper dh-systemd python3-yaml python3-requests python3-setuptools
    cd /src/cloud-init/cloud-init/

* For Xenial:

    ./packages/bddeb -S -d --sign --release xenial

* For Bionic:

    ./packages/bddeb -S -d --sign --release bionic

Building source packages for COPR
=================================

* Creating a Docker-based env for Building

    docker run --rm -it -v ~/src:/src centos:7 /bin/bash
    yum install -y python-six python-yaml python-requests python-jinja2 git rpm-build make
    cd /src/cloud-init/cloud-init/

* For EL7:

    ./packages/brpm --srpm --distro=redhat --boot=systemd