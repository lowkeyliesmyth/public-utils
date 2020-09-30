### Goals
* Parse yaml and split on `---`
* Output each stanza as lower {metadata.name}-{kind}.yml
* Accept remote url as input
* Optionally accept local file as input
* Deal with any name conflicts by appending increasing int to metadata.name
* Optionally accept output dir, otherwise just output to PWD
