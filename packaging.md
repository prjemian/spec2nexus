# Release Packaging

Packages for upload to [PyPI](https://pypi.org/project/spec2nexus/) and
[conda-forge](https://anaconda.org/conda-forge/spec2nexus) are built by GitHub
Actions workflows with every push to the GitHub repository.

Uploads to the PyPI & conda-forge package providers are limiited in each
workflow to new repository tags.

## Define Release

Once all [issues](https://github.com/prjemian/spec2nexus/issues) and [pull
requests](https://github.com/prjemian/spec2nexus/pulls) have been completed for
a particular [release
milestone](https://github.com/prjemian/spec2nexus/milestones) and there are no
failures noted in any of the [workflow
actions](https://github.com/prjemian/spec2nexus/actions), then a new release may
be created.

To create a new tag and release, [draft a new
release](https://github.com/prjemian/spec2nexus/releases/new) (use the option to create the new tag at the same time) on the GitHub web
site rather than pushing a new tag.  (When pushing a new tag from the remote
clone, the [publishing workflow
fails](https://github.com/prjemian/spec2nexus/runs/5324908848?check_suite_focus=true)
due to a race condition, as demonstrated with releases
[2021.1.9](https://github.com/prjemian/spec2nexus/releases/tag/2021.1.9) and
[2021.1.10](https://github.com/prjemian/spec2nexus/releases/tag/2021.1.10).)

## legacy Conda channels

These channels are used for older releases, prior to the 2021.1.11 release.

*   `prjemian` personal channel
*   `aps-anl-tag` production releases
*   `aps-anl-dev` anything else, such as: pre-release, release candidates, or testing purposes
