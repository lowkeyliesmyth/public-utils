### Overview
This script will decompose local or remote concatenated YAML files into separate local files. Specifically used for splitting up upstream kubernetes project manifests into consumable, easily identified pieces.

### Goals
* Parse yaml and split on `---`
* Output each stanza as lower {metadata.name}-{kind}.yml
* Accept remote url as input
* Optionally accept local file as input
* Deal with any name conflicts by appending increasing int to metadata.name
* Optionally accept output dir, otherwise just output to PWD

### TODO
* When retrieving remote manifests verify HTTPResponse is `Content-Type: text/plain;` otherwise fail
* Maintain block scalar multiline string formatting 