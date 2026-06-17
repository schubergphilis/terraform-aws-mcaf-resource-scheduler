# Changelog

All notable changes to this project will automatically be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v1.0.1 - 2026-06-17

### What's Changed

#### 🐛 Bug Fixes

* fix: updates for downtime windows that go past midnight (#12) @rguha-sbp

**Full Changelog**: https://github.com/schubergphilis/terraform-aws-mcaf-resource-scheduler/compare/v1.0.0...v1.0.1

## v1.0.0 - 2026-03-20

### What's Changed

#### 🚀 Features

* security!: upgrade dependencies (#11) @wvanheerde

**Full Changelog**: https://github.com/schubergphilis/terraform-aws-mcaf-resource-scheduler/compare/v0.4.0...v1.0.0

## v0.4.0 - 2025-01-02

### What's Changed

#### 🚀 Features

* test: implement more complete tests

#### 🐛 Bug Fixes

* fix: bug in ECS module that failed on finding the right filesystem

#### 📖 Documentation

* docs: add output descriptions
* ci: add linting, formatting and unit tests to CI

**Full Changelog**: https://github.com/schubergphilis/terraform-aws-mcaf-resource-scheduler/compare/v0.3.0...v0.4.0

## v0.3.0 - 2024-12-25

### What's Changed

#### 🚀 Features

* feature: add support for managing EFS provisioned throughput (#9) @wvanheerde
* enhancement: Improve docs and validations (#8) @wvanheerde

#### 📖 Documentation

* enhancement: Improve docs and validations (#8) @wvanheerde

**Full Changelog**: https://github.com/schubergphilis/terraform-aws-mcaf-resource-scheduler/compare/v0.2.1...v0.3.0

## v0.2.1 - 2024-11-29

### What's Changed

#### 🐛 Bug Fixes

* fix: use correct resource arn for FSx file systems (#7) @wvanheerde

**Full Changelog**: https://github.com/schubergphilis/terraform-aws-mcaf-resource-scheduler/compare/v0.2.0...v0.2.1

## v0.2.0 - 2024-11-28

### What's Changed

#### 🚀 Features

* feat: add support for scheduling FSx Windows File System throughput capacity (#6) @wvanheerde

**Full Changelog**: https://github.com/schubergphilis/terraform-aws-mcaf-resource-scheduler/compare/v0.1.4...v0.2.0

## v0.1.4 - 2024-09-11

### What's Changed

#### 🐛 Bug Fixes

* docs: Add docs to examples, fix README image (#5) @wvanheerde

#### 📖 Documentation

* docs: Add docs to examples, fix README image (#5) @wvanheerde

**Full Changelog**: https://github.com/schubergphilis/terraform-aws-mcaf-resource-scheduler/compare/v0.1.3...v0.1.4

## v0.1.3 - 2024-09-11

### What's Changed

#### 🐛 Bug Fixes

* fix: remove SFN logging (#4) @wvanheerde

**Full Changelog**: https://github.com/schubergphilis/terraform-aws-mcaf-resource-scheduler/compare/v0.1.2...v0.1.3

## v0.1.2 - 2024-09-11

### What's Changed

#### 🐛 Bug Fixes

* fix: log group for state machines (#3) @wvanheerde

**Full Changelog**: https://github.com/schubergphilis/terraform-aws-mcaf-resource-scheduler/compare/v0.1.1...v0.1.2

## v0.1.1 - 2024-09-11

### What's Changed

#### 🐛 Bug Fixes

* fix: pre-commit check failures (#2) @wvanheerde

**Full Changelog**: https://github.com/schubergphilis/terraform-aws-mcaf-resource-scheduler/compare/v0.1.0...v0.1.1
