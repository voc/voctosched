# voctosched
Scripts for converting various formats to [frab](https://github.com/frab/frab)-style fahrplan XML.
This also may or may not be useful for users of [pentabarf](https://github.com/nevs/pentabarf).

This repository implements an object representation of the frab export data model.
This can be used to build different im-/exporters or manipulators for the frab schedule export.

There is also a number of application which can display the schedule on mobile devices or infoscreens.
Some examples are:

* https://infobeamer.com
* https://github.com/EventFahrplan/EventFahrplan
* https://github.com/Wilm0r/giggity

# Usage
```
pip3 install --user translitcodec
./schedule.py -vvd -c ./demo/gpn11.ini
```
For more information about the input parameters and the generated output
have a look at the `demo` directory, this should be a good starting point.

# Currently supported inputs
* CSV

# Currently supported outputs
* basic XML, frab format
* extended XML, with additional `video_download_url` in events

# Validator
The generated XML can be validated with the c3voc validator, which can be found here https://github.com/voc/schedule/tree/master/validator

A quick validation can also be done with:

```
xmllint --noout --schema https://github.com/voc/voctosched/blob/master/schema/basic.xsd schedule.xml
```

For our extended format, use:

```
xmllint --noout --schema https://github.com/voc/voctosched/blob/master/schema/extended.xsd schedule.xml
```
