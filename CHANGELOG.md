# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2023-10-10

### Fixed

- Set field [GitRepository.URL] unique. Fix issue [issue #5].

### Changed

- Upgrade dependencies: Django-CMS 3.11, etc.

## [1.0.2] - 2022-03-28

### Added

- Write a guide into the README.md

### Fixed

- Fix setup to install templates and translations.

## [1.0.1] - 2021-06-18

### Added

- Add repository check to the signal handler.
- Add branch name into repository str method.
- Use repository branch for cloning.
- Add GitRepositoryForm and avoid raising exceptions.

### Fixed

- Fix FileNotFoundError and add fenced_code extension.

## [1.0.0] - 2021-05-27


[unreleased]: https://github.com/CZ-NIC/djangocms-git-md-page/compare/2.0.0...main
[2.0.0]: https://github.com/CZ-NIC/djangocms-git-md-page/compare/1.0.2...2.0.0
[1.0.2]: https://github.com/CZ-NIC/djangocms-git-md-page/compare/1.0.1...1.0.2
[1.0.1]: https://github.com/CZ-NIC/djangocms-git-md-page/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/CZ-NIC/djangocms-git-md-page/releases/tag/1.0.0

[issue #5]: https://github.com/CZ-NIC/djangocms-git-md-page/issues/5
[GitRepository.URL]: https://github.com/CZ-NIC/djangocms-git-md-page/blob/main/git_md_page/models/git_plugins.py#L11
