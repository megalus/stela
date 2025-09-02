# CHANGELOG


## v8.1.0 (2025-09-02)

### Documentation

* docs: clarify env precedence in dev.to article and README; add in-memory os.environ priority and fix examples ([`139080d`](https://github.com/megalus/stela/commit/139080de3bf6a4c13ff7ead5d834bdadf1b97016))

### Features

* feat: add type inference tests and improve parser to support JSON booleans/objects first with json.loads, fallback to literal_eval ([`b5e7ab0`](https://github.com/megalus/stela/commit/b5e7ab0a52f930b9ea7db0ed350dd25353add5cd))

### Unknown

* tests: enable logging in type inference tests for better debugging ([`b68db7b`](https://github.com/megalus/stela/commit/b68db7beae807d54c8a4cd5810f1947ed27012a6))


## v8.0.10 (2025-09-02)

### Documentation

* docs: clarify installation and initialization instructions in README ([`fe6b514`](https://github.com/megalus/stela/commit/fe6b5145e7217902a9b918dddcdb97ecdebca378))

### Fixes

* fix: update dotenv handling to prevent overwriting existing environment variables and improve documentation ([`a991485`](https://github.com/megalus/stela/commit/a991485fd1036b5f98c8978860bcc5e8a7f8d8d3))


## v8.0.9 (2025-09-02)

### Fixes

* fix: improve documentation clarity and update initialization command options ([`338d22c`](https://github.com/megalus/stela/commit/338d22cbaf034c6266370b7f02baf86357e04f0b))


## v8.0.8 (2025-09-02)

### Fixes

* fix: update Python version requirement to support up to 4.0 ([`9073047`](https://github.com/megalus/stela/commit/90730474ad342de2a00a6954ffe0ccef4d361e40))


## v8.0.7 (2025-09-02)

### Fixes

* fix: update project configuration and dependencies in pyproject.toml ([`4c01620`](https://github.com/megalus/stela/commit/4c01620ee8d9961bfeac35b043a5c0b2b42fd9e1))


## v8.0.6 (2025-09-02)

### Documentation

* docs: add coding guidelines and project documentation ([`35b7955`](https://github.com/megalus/stela/commit/35b7955c8a2db9dd82e5ce3da4fec1e960208f6b))

### Fixes

* fix: update dotenv configuration and logging options ([`09f8ddd`](https://github.com/megalus/stela/commit/09f8ddd94ca40b7974209a32bd2c0f576ed1e285))


## v8.0.5 (2024-10-09)

### Fixes

* fix: github actions ([`b3a6ced`](https://github.com/megalus/stela/commit/b3a6ced71cfdd678045419a833c22709a6c571ee))


## v8.0.4 (2024-10-09)

### Fixes

* fix: github actions ([`2d2d4c3`](https://github.com/megalus/stela/commit/2d2d4c373e9b0548324a1fa9c6543f23b878c953))


## v8.0.3 (2024-10-09)

### Fixes

* fix: github actions ([`6065f96`](https://github.com/megalus/stela/commit/6065f960f5363d5fcfd59ea4fe463c1caa20ff45))


## v8.0.2 (2024-10-09)

### Fixes

* fix: github actions ([`f30b7af`](https://github.com/megalus/stela/commit/f30b7af116ff9ddd9945836322ecfa32ddb5694f))


## v8.0.1 (2024-10-09)

### Fixes

* fix: github actions ([`0ef22bd`](https://github.com/megalus/stela/commit/0ef22bd62986a2510d97d8b7e711f83599288814))


## v8.0.0 (2024-10-09)

### Breaking

* feat!: bump version

BREAKING CHANGE ([`08fbf80`](https://github.com/megalus/stela/commit/08fbf80213001ec73f40e663d0af2ad311db062a))

### Unknown

* Add support to Python 3.13 (#11)

* feat!: Add support to Python 3.13

This is a BREAKING CHANGE commit. Changes:

* Add support to 3.13
* Remove support to 3.10
* Update GitHub Actions

* ci: fix pre-commit ([`1277fbc`](https://github.com/megalus/stela/commit/1277fbcd19eee581d344f342adfbd6de58374b35))


## v7.1.0 (2024-03-14)

### Features

* feat: add `no_name_env` option.

Default value: GLOBAL

Also fix unit tests with Pytest 8.x ([`d3c235c`](https://github.com/megalus/stela/commit/d3c235c1eca3ce8a63fc124ff254d44f9e9fc593))


## v7.0.4 (2024-02-09)

### Fixes

* fix: error when stela did not find STELA_xxx environment variables in dotenv file. ([`df54c1c`](https://github.com/megalus/stela/commit/df54c1c89fd2139f556fa9851ccd111731063ac7))


## v7.0.3 (2024-02-08)

### Fixes

* fix: error when stela did not find any dotenv file. ([`8ab3313`](https://github.com/megalus/stela/commit/8ab3313d3127651f1e08cab21d8539cb462766ab))


## v7.0.2 (2024-02-05)

### Fixes

* fix: StelaValueError during initialization ([`4c9dfac`](https://github.com/megalus/stela/commit/4c9dfac1227c8f2c019a0d7047be7f0b9a48ce23))


## v7.0.1 (2024-02-05)

### Fixes

* fix: fix error when variable exists on memory but not on dotenv files ([`00b65d0`](https://github.com/megalus/stela/commit/00b65d0eb0a35cd1ec06176197e363eba920184a))


## v7.0.0 (2024-02-05)

### Breaking

* fix!: remove `dotenv_overwrites_memory`. This option gives a lot of headaches for custom final loaders.

For now on, Stela will always overwrite the `os.environ` values with the ones found in the dotenv files.

This is a BREAKING CHANGE. ([`abcb68c`](https://github.com/megalus/stela/commit/abcb68c0bcd50b6085fda3a55ffd8c3e77e53069))

### Documentation

* docs: Update README.md ([`0213495`](https://github.com/megalus/stela/commit/02134952300979d6c8ab87b13b9d11e07080e231))


## v6.0.0 (2023-12-27)

### Breaking

* feat!: New Version 6.0

BREAKING CHANGE: Changes for this commit:
* Drop Python 3.9 support
* Add Python 3.12 support
* Remove `Stela.settings` object and deprecated code. If you're still using the old API, please use version 5.x
* Update documentation ([`4563314`](https://github.com/megalus/stela/commit/4563314626b17a1918c1d1cde9313ed2956dee2c))

### Chores

* chore: add missing code ([`b290042`](https://github.com/megalus/stela/commit/b290042f33198b0c659668b251a35f4de22fb1cf))


## v5.2.0 (2023-08-15)

### Features

* feat: Added recursion to dotenv file search to improve file detection.

In the previous implementation, there was a chance of not finding the .env file if it was nested in the subdirectories. Added a recursive approach to solve this problem: the function `look_for_file` is now called recursively until the .env file is found or till it hits the root directory. This change ensures that the .env file will be accurately detected regardless of its location relative to the directory from which the script is run. Now, users can be more flexible in their directory structure. ([`9b99a80`](https://github.com/megalus/stela/commit/9b99a808a219b6149db4b28b2170d7f7f6bb33e0))


## v5.1.9 (2023-08-15)

### Fixes

* fix: Added recursion to dotenv file search to improve file detection.

In the previous implementation, there was a chance of not finding the .env file if it was nested in the subdirectories. Added a recursive approach to solve this problem: the function `look_for_file` is now called recursively until the .env file is found or till it hits the root directory. This change ensures that the .env file will be accurately detected regardless of its location relative to the directory from which the script is run. Now, users can be more flexible in their directory structure. ([`08d0e03`](https://github.com/megalus/stela/commit/08d0e031094947eb8c5f08bb0a263cbd8094ea4f))


## v5.1.8 (2023-08-15)

### Fixes

* fix: recursion for search dotenv files ([`d084242`](https://github.com/megalus/stela/commit/d084242260e63b25b22b7a89cf82b7e9b0b39897))


## v5.1.7 (2023-08-15)

### Fixes

* fix: Refactor file searching in config by using utility function ([`0a28113`](https://github.com/megalus/stela/commit/0a28113fe241f5123b40265872045fa9ae96cf62))


## v5.1.6 (2023-08-15)

### Fixes

* fix: Use absolute path for config file search in stela

The 'get_settings' function in stela config has been updated to use 'Path.cwd()' instead of 'Path(".")' when defining the paths for 'pyproject.toml' and '.stela'. This change shifts the configuration file search from a relative path to the current working directory, thus enhancing the consistency and reliability of the configuration loading process. ([`d2afdbe`](https://github.com/megalus/stela/commit/d2afdbeee6acde3c19d968b46b4e512a24d0ac66))


## v5.1.5 (2023-08-15)

### Fixes

* fix: Add recursive file search to stela configuration

Introduced a recursive file search in stela configuration's `get_settings` method. The change added a helper method `recurse_find_file`, which looks up for configuration files from the current directory up to the root one. This change helps to locate the 'pyproject.toml' and '.stela' configuration files, improving application stability and user experience. ([`16d2629`](https://github.com/megalus/stela/commit/16d26296a3af00708d581362249a2fdbe7eaf97b))


## v5.1.4 (2023-08-15)

### Fixes

* fix: Add logging for stela settings and update troubleshooting docs

This commit adds logging in the configuration init file to log the stela settings being used and updates the troubleshooting docs to include information on how to handle Errors related to Stela not finding values for variables in the .env file. This was done to provide users with better troubleshooting abilities and improve user experience. ([`302b6bd`](https://github.com/megalus/stela/commit/302b6bd634743ef0a30a45b34c2b986a27a88e2d))


## v5.1.3 (2023-08-15)

### Fixes

* fix: error in stela init command ([`2722a3d`](https://github.com/megalus/stela/commit/2722a3d94991c350f112c0eeb338eee541e3f999))


## v5.1.2 (2023-08-14)

### Fixes

* fix: fix versions ([`b692461`](https://github.com/megalus/stela/commit/b692461e3712a39b0d21c144f5364a156224c1cf))

* fix: use version 7.34.6 ([`6bbf2bc`](https://github.com/megalus/stela/commit/6bbf2bcda8c16b87efd4dee49f56b07ddfaeeebf))

* fix: use version 7 ([`95db837`](https://github.com/megalus/stela/commit/95db837fd2bfeada324e6e6bbea0f885af2edfe7))

* fix: use version 7.33.5 ([`fe3b081`](https://github.com/megalus/stela/commit/fe3b081fe45680e813355bd9b8286acdd98da64f))


## v5.1.1 (2023-08-14)

### Fixes

* fix: add missing configuration in github actions ([`c75d97b`](https://github.com/megalus/stela/commit/c75d97b2e33bd866f7897b96f67284f4b52dbcc1))

* fix: add missing configuration in github actions ([`280e1eb`](https://github.com/megalus/stela/commit/280e1ebc9c6e9bfedf1e7165f5088c40e0ad8dbf))

* fix: fix github actions with new distribution packages ([`2889dd8`](https://github.com/megalus/stela/commit/2889dd841e91c063d02504103b85c215bdbfcd48))


## v5.1.0 (2023-08-14)

### Features

* feat: Add support to Pydantic v2.x

* Support for Pydantic v1 is now deprecated and will be removed on 6.0.
* Updated Stela's initialization flag from `--use-default` to `--default`. ([`5165d3c`](https://github.com/megalus/stela/commit/5165d3cec4ef3a0f8e5f397123569194ff13ccf1))


## v5.0.4 (2023-04-05)

### Fixes

* fix: reduce logger messages from old settings ([`de565ef`](https://github.com/megalus/stela/commit/de565efdefd5191552a927cef926c6209b0796bd))


## v5.0.3 (2023-04-05)

### Fixes

* fix: move the default value from missing env to another function.

* Use the `env.get()` to return var value or `None`.
* Use the `env.get_or_default()` to return var value or default value ([`e69f680`](https://github.com/megalus/stela/commit/e69f6803e4be90097499a255aae2923b92551634))


## v5.0.2 (2023-04-04)

### Fixes

* fix: stela error when no .env file exists ([`c38715e`](https://github.com/megalus/stela/commit/c38715e4ece0060fea93ff55d5cef0a3d87f93b6))


## v5.0.1 (2023-04-03)

### Documentation

* docs: fix typo ([`d91a7b7`](https://github.com/megalus/stela/commit/d91a7b7992d1e632eeb8744a64709ede8b257469))

* docs: Update legacy loader example ([`5d7674b`](https://github.com/megalus/stela/commit/5d7674b10d284fde626d0817b7c30ca2bca54a74))

### Fixes

* fix: Fix stela init toml parse and save data. ([`96a7a9a`](https://github.com/megalus/stela/commit/96a7a9afdfb58c7d5980c99e7b429a869b2e50b1))


## v5.0.0 (2023-04-03)

### Breaking

* feat!: Bump version 5.0

This is a BREAKING CHANGE. ([`6838206`](https://github.com/megalus/stela/commit/6838206359d5323da34cd5fe404d91c6ed607059))

### Chores

* chore: remove author file ([`180b136`](https://github.com/megalus/stela/commit/180b136530ce7dd3895ba9a74dc83c4cdc4c2db4))

### Continuous Integration

* ci: fix publish action ([`18d5c76`](https://github.com/megalus/stela/commit/18d5c76f8d92421580f78dc1942267754c316d46))

* ci: add sonar commands ([`5b41a65`](https://github.com/megalus/stela/commit/5b41a65f1731a13a987ee580e67e6f80cc5a6c63))

* ci: update dependencies in action ([`a8480d2`](https://github.com/megalus/stela/commit/a8480d2b474d1becb88f4744f11e2bd13a5d6c95))

### Documentation

* docs: [skip-ci] Update README.md ([`02ef602`](https://github.com/megalus/stela/commit/02ef602d0f5a690e56acac8666c1f79f69130d8e))

### Unknown

* New Release: Stela 5.0 (#10)

* feat!: Stela 5.0

* Drop support to Python 3.8
* BREAKING CHANGE. This is a complete rework, please check /docs/update.md
* Update Github Actions workflows
* Move Documentation to MKDocs

Resolves ST-2

* ci: add missing files

* tests: fix unit tests

* ci: fix setup python action

* ci: fix missing setup python action

* ci: fix all action versions

* ci: fix pre-commit action

* ci: fix unit tests ([`281e76a`](https://github.com/megalus/stela/commit/281e76a0dcdc094373604a5b2d10026878fcff43))


## v4.0.2 (2022-02-01)

### Fixes

* fix: change licence to MIT ([`61536f8`](https://github.com/megalus/stela/commit/61536f893260df8235015dd0a836f8c1bfb9c705))


## v4.0.1 (2022-02-01)

### Continuous Integration

* ci: fix github actions yaml files ([`3505fa5`](https://github.com/megalus/stela/commit/3505fa57d37bedc424bbc02c164e21e9a1805014))

### Fixes

* fix: change licence to AGPL-3.0 ([`06c69d4`](https://github.com/megalus/stela/commit/06c69d4bd11214512131d4de02bdbb83068215f4))


## v4.0.0 (2022-01-18)

### Breaking

* feat!: Add Pydantic support

Bump commit, please check https://github.com/chrismaille/stela/pull/9 for changes

BREAKING CHANGE: dropped python 3.7 support ([`c1bc903`](https://github.com/megalus/stela/commit/c1bc9031736cfc50308eb7a369802d012bfa0d5d))

### Documentation

* docs: Update README.md ([`ddb834b`](https://github.com/megalus/stela/commit/ddb834babdb19f576146acb45809ac48c4162385))

### Unknown

* Release 4.0 (#9)

* feat!: Add Pydantic support

BREAKING CHANGE: dropped python 3.7 support ([`b7fcd09`](https://github.com/megalus/stela/commit/b7fcd0998d92f697906773d2e3f2eae00b96c2f6))


## v3.0.2 (2021-08-25)

### Documentation

* docs: fixing README index. ([`5b6b2bf`](https://github.com/megalus/stela/commit/5b6b2bf1a3463324edcc3403ee510e79bd53a6df))

* docs: Update README.md ([`575ee4a`](https://github.com/megalus/stela/commit/575ee4a9cdd0964b3a56e382a23c46f6d2f5c0e0))

### Fixes

* fix: Make circular import errors explicity with stela.settings ([`2a56b7c`](https://github.com/megalus/stela/commit/2a56b7c4af65470005c4b7b1274ec002dd750cb3))


## v3.0.1 (2021-08-25)

### Fixes

* fix: do not show logs when no loaders exist ([`41da0cf`](https://github.com/megalus/stela/commit/41da0cf49ddcf17c60a44b84d034e03660baf24a))


## v3.0.0 (2021-08-25)

### Breaking

* feat!: Improve logging and refactor decorators logic.

Stela logs will now show key/values retrieved during his lifecycle. All values will show filtered.

BREAKING CHANGE: Logs now will be disabled, by default. ([`6886c74`](https://github.com/megalus/stela/commit/6886c749f82af50b00da19b9e750b09eb14cd2e3))

### Chores

* chore: Avoid multiple decorators strange behavior. ([`874ad25`](https://github.com/megalus/stela/commit/874ad255cf19faa84fc6d830b4f33c016767544b))

### Features

* feat: Add log decorators ([`fb5b926`](https://github.com/megalus/stela/commit/fb5b9263add8141cd7ba5ac38a12a5943e98f5a3))

### Testing

* test: small typo ([`bffb78c`](https://github.com/megalus/stela/commit/bffb78cb983a2d548eb26b1911d6c52b7a0242b1))

### Unknown

* Merge pull request #8 from chrismaille/3.0

Release 3.0 ([`36b5210`](https://github.com/megalus/stela/commit/36b52103a36641374355dc915a016459dde15e72))


## v2.0.9 (2021-05-28)

### Fixes

* fix: Permit access the Environment Variable Name, when use the `do_not_read_environment` option ([`61e4efb`](https://github.com/megalus/stela/commit/61e4efb53c752e355398f0f093981345275e1eae))


## v2.0.8 (2021-03-30)

### Unknown

* Merge remote-tracking branch 'origin/main' ([`8eba440`](https://github.com/megalus/stela/commit/8eba4404d45b632eba76e9aba96796023e23b5d8))


## v2.0.7 (2021-03-30)

### Fixes

* fix: merge dicts between phases error ([`8d79bb8`](https://github.com/megalus/stela/commit/8d79bb81962ed255ebcbab7aaaaa42b61f397c7a))

### Unknown

* Merge remote-tracking branch 'origin/main' ([`8201236`](https://github.com/megalus/stela/commit/820123640870c9a9a0ea531467da4c4aa30e74a0))


## v2.0.6 (2021-03-30)

### Fixes

* fix: error when subtable overwrites main table ([`7801f6f`](https://github.com/megalus/stela/commit/7801f6f687cb383111e1d0267d8c20c6b70f83df))

### Unknown

* Merge remote-tracking branch 'origin/main' ([`6af877e`](https://github.com/megalus/stela/commit/6af877e2d732d9e97592281b1dc2dd705e43eae1))


## v2.0.5 (2021-03-29)

### Fixes

* fix: add sub-dictionaries inside environment tables on pyproject.toml ([`3340bec`](https://github.com/megalus/stela/commit/3340bec762198d0fb69d536ed9134a92e7fca54e))

* fix: dotnet logic ([`fcc14c1`](https://github.com/megalus/stela/commit/fcc14c1c74e8c7ece41c1a01ea87a881f6f7a9b7))


## v2.0.4 (2021-03-27)

### Fixes

* fix: Fix error when function decorated are not called. ([`bd115b3`](https://github.com/megalus/stela/commit/bd115b328fa0c64175ce2de92cc0907c7b077466))


## v2.0.3 (2021-03-27)

### Fixes

* fix: build configuration during publish ([`4e6c6c4`](https://github.com/megalus/stela/commit/4e6c6c48d54df1cc8c4e032518b309259e4f115e))


## v2.0.2 (2021-03-27)

### Unknown

* Merge remote-tracking branch 'origin/main' ([`12a89dc`](https://github.com/megalus/stela/commit/12a89dce0a01fb94aa081af51c31e04ef92c04b4))


## v2.0.1 (2021-03-27)

### Fixes

* fix: build configuration during publish ([`0c83367`](https://github.com/megalus/stela/commit/0c83367a8522ab7e51e0a91c00f0922eaf8b871e))

* fix: missing command during publish ([`93602b1`](https://github.com/megalus/stela/commit/93602b12630c9193e07b54112f34f1743e0043f0))


## v2.0.0 (2021-03-27)

### Breaking

* feat: Bump version

BREAKING CHANGE: new version ([`fdede7e`](https://github.com/megalus/stela/commit/fdede7e1135077a847130f774fe872cf11c4b662))

### Build System

* build: remove rootpath library

This lib not work when dependencies are generated for AWS Lambda Layers (in dependencies/python folder). Current logic actually delete lib code inside this folder ([`6f22c42`](https://github.com/megalus/stela/commit/6f22c42c6d6ce4914b59ed7a4bd17f6789f23ecf))

* build: fix python version during publish ([`025e02b`](https://github.com/megalus/stela/commit/025e02b35bfbccdf02ce90413300c78a5e3738cb))

* build: Remove 3.8 from Actions

Until issue is resolved:
https://github.community/t5/GitHub-Actions/Seg-Faults-with-Python-in-Linux-while-Running-Pytest/td-p/39912 ([`92faaa1`](https://github.com/megalus/stela/commit/92faaa124d56ea9af95fd5d9fffce04644b38947))

* build: add credential in git checkout ([`2b2d886`](https://github.com/megalus/stela/commit/2b2d8863e92781ce7d75b217fe5931640a7c45c3))

* build: remove git pull in script ([`99d81fd`](https://github.com/megalus/stela/commit/99d81fdbe57d5dc8b516277676b7c9e8caacf40b))

* build: fix branch name ([`6f1d306`](https://github.com/megalus/stela/commit/6f1d306a30584df336a94703a3c398dc9815fb70))

* build: remove branch prefix ([`4b3949d`](https://github.com/megalus/stela/commit/4b3949d830360ae4ffaed6c7b69aad77fdf2c40d))

* build: add git pull ([`d5e6990`](https://github.com/megalus/stela/commit/d5e6990e0429ab27904c122caf6285a08fd57b28))

* build: bump version ([`effd3ef`](https://github.com/megalus/stela/commit/effd3ef72f2761e1d93ca2cebcafd5a1c533e61c))

* build: bump ([`7038c7f`](https://github.com/megalus/stela/commit/7038c7f32683fd1f381c03cdf2a541604c6fa6ef))

* build: bump version ([`fc392c7`](https://github.com/megalus/stela/commit/fc392c7876f2e5b9d98f4a21261469a9ce84c2ac))

* build: add git token ([`0388275`](https://github.com/megalus/stela/commit/0388275a0cb7822ae3dc5de1ebeba2cd2ad57416))

* build: fix missing push ([`7b84151`](https://github.com/megalus/stela/commit/7b84151f632b0b6b82f62ca26bcb253e58dbe7c8))

* build: bump version ([`f2e4206`](https://github.com/megalus/stela/commit/f2e42063bcb4eb5f8e206c045a0cb5ca5c6da2ee))

* build: fix missing push ([`c09c9f8`](https://github.com/megalus/stela/commit/c09c9f8e01d1cedbc4cdaf08d529048ce94cfe9b))

* build: fix python version in pyproject.toml ([`57f3148`](https://github.com/megalus/stela/commit/57f3148e0a045dddfd9dade3d1197f6c84a4252a))

* build: fix dependencies ([`a300021`](https://github.com/megalus/stela/commit/a300021319b9dba5ec8536a38b0e6896ab8bef19))

* build: test with sudo ([`58e1a5d`](https://github.com/megalus/stela/commit/58e1a5d826b31ee3f95c5b37375348e951e7632e))

* build: test with sudo ([`be68eee`](https://github.com/megalus/stela/commit/be68eeec665cabd4ac8f8b0e3e8d48feb948614a))

* build: fix tests.yml error ([`d6d48a5`](https://github.com/megalus/stela/commit/d6d48a51fb778725f6cfa594f9ea1538706926e4))

* build: fix tests.yml format ([`77bc2c4`](https://github.com/megalus/stela/commit/77bc2c47cf8d6f65f59d87159921332376ddcaa6))

* build: fix conditional in tests.yml ([`2956296`](https://github.com/megalus/stela/commit/2956296c22292d0fdfd5c18213b54b3542dcea7e))

* build: fix tests.yml ([`cc8e208`](https://github.com/megalus/stela/commit/cc8e20805abb235b2648e9c5c175b734caf207cf))

* build: Publish packages via Github Actions

* Add auto-changelog
* Improve tests in Windows/Mac ([`08ef0b2`](https://github.com/megalus/stela/commit/08ef0b2231019957c8ee9ddb142f8cf76f3a73e5))

* build: add dataclasses backport to 3.6 ([`e25c447`](https://github.com/megalus/stela/commit/e25c447ec11e8041a02bbb52dbc2fc4567cd77a3))

* build: remove python 3.8 support

* Build issues on regex in windows ([`b811f18`](https://github.com/megalus/stela/commit/b811f1873f9b0067e5b9fd0b64f12d4695e38ec8))

### Continuous Integration

* ci: Fix missing poetry during publish. BREAKING CHANGE: new version ([`2f722b1`](https://github.com/megalus/stela/commit/2f722b16aa5ba40293415c2c50d9fcb2d3a72526))

* ci: fix wrong publishing branch (also BREAKING CHANGE) ([`770a705`](https://github.com/megalus/stela/commit/770a7054bbe36b4d05da24e40388a3c15da715cf))

* ci: add missing option in publish step ([`dc2b90a`](https://github.com/megalus/stela/commit/dc2b90a3804541925dff5283f85657ebd78070af))

* ci: remove old changelog script ([`3084c79`](https://github.com/megalus/stela/commit/3084c79b1e90416e920cb1999f1372d457421266))

* ci: fix make ci command ([`84cc4a7`](https://github.com/megalus/stela/commit/84cc4a7020fe2fdf7beef3eedcd9f82a67f2934a))

* ci: fix missing yamllint error ([`f8775d4`](https://github.com/megalus/stela/commit/f8775d4cdca05effffccc1db7cf025580013c5d4))

* ci: update make install command ([`6c2432c`](https://github.com/megalus/stela/commit/6c2432c82ec3627c518c4db847315ee119ac9721))

* ci: remove make pre-ci command ([`9420cd7`](https://github.com/megalus/stela/commit/9420cd78e416a08e47ec81193bcc87e4a54b628c))

* ci: fix python version in  pyproject.toml ([`72efc26`](https://github.com/megalus/stela/commit/72efc26d1f454a0a1c837fb4fd28d38cd62279ec))

* ci: fix python version in  pyproject.toml ([`a22b525`](https://github.com/megalus/stela/commit/a22b525ebd9d02664934f37cab801630de4afca9))

* ci: fix python version in  pyproject.toml ([`23bb386`](https://github.com/megalus/stela/commit/23bb3868bbf4ffdeb1f17d3379a5cd6cb58063f7))

* ci: fix make pre-ci error ([`ced90cc`](https://github.com/megalus/stela/commit/ced90cc8870659d9c2465243e8df7093ebd2846f))

* ci: Remove ssh manual upload ([`2215107`](https://github.com/megalus/stela/commit/221510767553b42bf7c83a8f895f490e0a1764b0))

* ci: Add github actions

Changes:
* Add mypy support
* Fix PEP 527 errors
* Add github test workflow ([`b9da377`](https://github.com/megalus/stela/commit/b9da3776816ec4f8065915719928f3c2246bbf96))

### Documentation

* docs: Update README.md ([`4407cb2`](https://github.com/megalus/stela/commit/4407cb2471101d199d7ac1a255795ef3c5ffd8f7))

* docs: Add pypi badge ([`301bf51`](https://github.com/megalus/stela/commit/301bf515ad4c031a4e01acdd139e86d31fd7aba6))

* docs: Update Pypi docs ([`ac109d5`](https://github.com/megalus/stela/commit/ac109d5761028e5d3eb8c76feb52e183a5859dc9))

* docs: Update README.md ([`80cf466`](https://github.com/megalus/stela/commit/80cf466a02df094d4d7012ae3521f5cfe68a1e64))

### Features

* feat: Update for scalpl 0.4.0 ([`c59b3c2`](https://github.com/megalus/stela/commit/c59b3c2906b67bd696b6aa5cbca493489ab3cc99))

* feat: Better lifecycle and dotenv support.

This is a BREAKING VERSION

### Changes
* Add dotenv support. Stela now will check for `dotenv` files after checking memory, but before return value from dictionary. This can be customized in `[tool.stela]` settings
* Add more steps in Stela Lifecycle. Now, we have:  `pre_load, embed, file, custom, pre_load` steps. To recreate old behavior define `load_order = [""pre_load", "file", "post_load"]` in `[tool.stela]` settings
* Add environment variables direct in `pyproject.toml`. You can use this file directly instead creating one for each environment layer.
* Update documentation and CI process ([`2a99dfc`](https://github.com/megalus/stela/commit/2a99dfcf805411d3bef85f20ea12800a15f594d0))

* feat: Add `do_not_read_environment` option.

This options will set Stela to always use the value from configuration files, instead replace him for the correspondent environment variable. ([`18bce3c`](https://github.com/megalus/stela/commit/18bce3c2b5768313712dd41684210763a4d6a4b0))

* feat: Make logs optional ([`0945c62`](https://github.com/megalus/stela/commit/0945c6220adb1363adfb37dcd1bfdfe14dc4d49a))

* feat: First Commit

Changes:
* Add main logic
* Fixes errors in scalpl get/pop operations ([`27280d7`](https://github.com/megalus/stela/commit/27280d7ba5a8dece51043de352b2494609a5ee38))

### Fixes

* fix: coverage level for new scalpl code ([`01ef4c0`](https://github.com/megalus/stela/commit/01ef4c070bf058e861bafb4bcd3511dbdc4942a8))

* fix: small fixes in deploy process ([`76b967b`](https://github.com/megalus/stela/commit/76b967b6ea5a985bbc19df3e6f99a57ede3efcec))

* fix: linter errors ([`a970635`](https://github.com/megalus/stela/commit/a97063542f6dc7b73bb91d95f5edece2b9ba4982))

* fix: install dataclasses backport in python 3.7+ ([`144a2df`](https://github.com/megalus/stela/commit/144a2df17dba9190967d12d16c61e68e0b89837c))

* fix: remove backmerge from script ([`46fcfd1`](https://github.com/megalus/stela/commit/46fcfd151049c2d60829f874a5f48d231d0a895c))

* fix: fix allow unrelated histories ([`03a6096`](https://github.com/megalus/stela/commit/03a609633a00c7d7e5d7645bdf40a4a3df925951))

* fix: fix ci script error in poetry version ([`90faf3e`](https://github.com/megalus/stela/commit/90faf3ec34802555ec0fb75e771a175161a14e0f))

* fix: fix ci script error in git checkout command ([`082ca19`](https://github.com/megalus/stela/commit/082ca19acac690eca11f2501df61d2b058f5fd91))

### Refactoring

* refactor: get pyproject.toml folder ([`81f1ab4`](https://github.com/megalus/stela/commit/81f1ab4f13292306e3ea92a09cea5ecf392c1c6b))

### Unknown

* Merge remote-tracking branch 'origin/main' ([`be3a18d`](https://github.com/megalus/stela/commit/be3a18d9202739e0615098f9a7e95f7c5695773b))

* Merge pull request #7 from chrismaille/develop

feat: Better lifecycle and dotenv support. ([`45a7ab7`](https://github.com/megalus/stela/commit/45a7ab79e97ee7d955fc7eb06ef2ec4ce51fe8fb))

* Merge remote-tracking branch 'origin/main' into develop

# Conflicts:
#	.github/workflows/tests.yml
#	CHANGELOG.md
#	stela/stela_cut.py
#	update_changelog.sh ([`fce3bff`](https://github.com/megalus/stela/commit/fce3bffb54354f5bb013c3253d7677e0946469ad))

* [skip-ci] auto-bump version 1.0.12 ([`f8dccff`](https://github.com/megalus/stela/commit/f8dccff3c94769c6245f7ae4187215e35b3ede64))

* [skip-ci] auto-bump version 1.0.11 ([`34a111c`](https://github.com/megalus/stela/commit/34a111cd932d71854d41df214d55ca0731532052))

* [skip-ci] auto-bump version 1.0.10 ([`80f86e3`](https://github.com/megalus/stela/commit/80f86e3428d7ab0029ba2875cae41051af7dd0a5))

* [skip-ci] auto-bump version 1.0.9 ([`f89e7f2`](https://github.com/megalus/stela/commit/f89e7f200582bf99f7c79c41cd674ff64ce18b1d))

* hotfix: remove logs ([`b8f4aa3`](https://github.com/megalus/stela/commit/b8f4aa38d1e5da8bcec843a14a984b8b317416ed))

* [skip-ci] auto-bump version 1.0.8 ([`fd72349`](https://github.com/megalus/stela/commit/fd72349cacca94f65aae221338413d59514dda8d))

* hotfix: find root folder running WSL ([`9a71ef3`](https://github.com/megalus/stela/commit/9a71ef389d932b2f9135ada3f271e73d2c8c598c))

* [skip-ci] auto-bump version 1.0.7 ([`9887ca3`](https://github.com/megalus/stela/commit/9887ca3a5e58a035d45e205a610b7b49f5c7df43))

* Merge pull request #6 from chrismaille/develop

Refactor: Find pyproject.toml code ([`112bbd8`](https://github.com/megalus/stela/commit/112bbd82e7ada8187d35644e25c842cbe34343ef))

* Merge pull request #5 from chrismaille/master

Backmerge ([`cfcc0f0`](https://github.com/megalus/stela/commit/cfcc0f0c99ce186d2fa4b784be612b3298bafe8b))

* [skip-ci] auto-bump version 1.0.6 ([`166cf9a`](https://github.com/megalus/stela/commit/166cf9a4ecd170c116eae86a979efbbaee84eb99))

* Merge pull request #4 from chrismaille/develop

Remove rootpath from dependencies ([`dadb2a9`](https://github.com/megalus/stela/commit/dadb2a9f87f5d94b0ff53b422620f54bd1b85e19))

* [skip-ci] auto-bump version 1.0.5 ([`53dd2b5`](https://github.com/megalus/stela/commit/53dd2b53310d9b75e3f257ef641266a21b324149))

* Merge pull request #3 from chrismaille/develop

fix: remove dataclass backport when using Python 3.7+ ([`caef46f`](https://github.com/megalus/stela/commit/caef46fd8bbfb4fc14ef9ee5fef21f9014922d6d))

* chord: Add python 3.8 support ([`0225ad3`](https://github.com/megalus/stela/commit/0225ad3b888c8cfd4478a71a3249db2755745966))

* [skip-ci] auto-bump version 1.0.4 ([`94cf876`](https://github.com/megalus/stela/commit/94cf8766fb9100128896e95d040a6b98838630ff))

* Merge pull request #2 from chrismaille/develop

feat: Add `do_not_read_environment` option. ([`ce13cf8`](https://github.com/megalus/stela/commit/ce13cf8d19a912e008570939b4f12dcfa50be168))

* Update issue templates ([`d90491c`](https://github.com/megalus/stela/commit/d90491c5c6612018f838f68b01eb1f8a4c1757a3))

* [skip-ci] auto-bump version 1.0.3 ([`787d480`](https://github.com/megalus/stela/commit/787d4803b99e908676abd6205e468bcefec56f79))

* [skip-ci] auto-bump version 1.0.2 ([`4bd9d4d`](https://github.com/megalus/stela/commit/4bd9d4de9984d1c116d9c5a7837e4e8a907b3020))

* bump version ([`6e07092`](https://github.com/megalus/stela/commit/6e07092e6a48959361c51d9be8b93c3e9b15ede7))

* [skip-ci] auto-bump version 1.0.3 ([`4d0a69c`](https://github.com/megalus/stela/commit/4d0a69c54916780d2cf8c136b6db4400869cefa0))

* [skip-ci] auto-bump version 1.0.2 ([`3176314`](https://github.com/megalus/stela/commit/31763141cc3c10b585dbc982350d9e6240922764))

* [skip-ci] auto-bump version 1.0.1 ([`8ee852a`](https://github.com/megalus/stela/commit/8ee852aae588ad719d234d216ac2c4475c222153))

* [skip-ci] auto-bump version 1.0.0 ([`82eed12`](https://github.com/megalus/stela/commit/82eed12afadd1667b8c7d2f495855844ad9c9a55))

* Merge pull request #1 from chrismaille/release/1.0.0

Release/1.0.0 ([`8f0f67d`](https://github.com/megalus/stela/commit/8f0f67d2bd659b65767d71ab1134650892ae1631))

* [skip-ci] auto-bump version 1.0.0-alpha.10 ([`b4eb07c`](https://github.com/megalus/stela/commit/b4eb07cfefdc67e7ec9c0e2212db021f97b1fa74))

* [skip-ci] auto-bump version 1.0.0-alpha.10 ([`f28cb36`](https://github.com/megalus/stela/commit/f28cb364df78f4829dea283c0bad44daabc7531a))

* [skip-ci] auto-bump version 1.0.0-alpha.9 ([`76cc782`](https://github.com/megalus/stela/commit/76cc78267ba4b698a20d25007906d53d72b6e654))

* Merge remote-tracking branch 'origin/release/1.0.0' into release/1.0.0 ([`d4c9d37`](https://github.com/megalus/stela/commit/d4c9d37d833c3abc5d78f2f2db8f2ea9061458a8))

* [skip-ci] auto-bump version 1.0.0-alpha.8 ([`e2fcc33`](https://github.com/megalus/stela/commit/e2fcc33aea86cfd6ca4d1cda14effd39c78db60e))

* chord: fix python versions ([`5b09017`](https://github.com/megalus/stela/commit/5b090175276d5e1a5faf0d8e3e38ce5c81ec2a6d))

* chord: bump version ([`3fcf945`](https://github.com/megalus/stela/commit/3fcf945fbd92bf7922c58d570cbe9256c94d2a05))

* chord: remove classifiers ([`22004c5`](https://github.com/megalus/stela/commit/22004c5f0362bfb89cda52e59ab82a13eeec3635))

* chord: fix prerelease bug ([`653df2e`](https://github.com/megalus/stela/commit/653df2ee1335b645259da9f12c0c90d753afd6d8))

* [skip-ci] Auto-bump version 1.0.0-alpha.0 ([`8315b4e`](https://github.com/megalus/stela/commit/8315b4e2ef8ae6b6b1c4dbc625756cdc9490d735))

* chord: bump version ([`442a2f1`](https://github.com/megalus/stela/commit/442a2f110bc7fce4167472e8ba8fdaba4d3c3d13))

* chord: fix git config error ([`5c4d9c6`](https://github.com/megalus/stela/commit/5c4d9c694b2ca7f31b8422a761a03ff4dac4e34c))

* chord: change script permission ([`3921906`](https://github.com/megalus/stela/commit/39219066a077d7f4d4c181310a7dddfbad228b54))

* Initial commit ([`c86616e`](https://github.com/megalus/stela/commit/c86616ecf027b80e093aa9ad26e98f92b779cf89))
