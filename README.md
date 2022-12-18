# voctosched
Tool converting various formats to [frab](https://github.com/frab/frab)-style schedule XML and JSON as described by [in the c3voc wiki](https://c3voc.de/wiki/schedule). The format was initialy introduced by [pentabarf](https://github.com/nevs/pentabarf), got more popular with [frab](https://frab.github.io/frab/) and is also provided by [[https://pretalx.com/p/about/|pretalx]] – as it became the main interexchange format [between various systems](https://c3voc.de/wiki/api) recording and publishing talks of conferences and other events.


This repository implements an object representation of the frab data model and can be used to build different im-/exporters or manipulators.

There is also a number of application which can display the schedule on mobile devices or infoscreens.
Some examples are:

* https://infobeamer.com
* https://github.com/EventFahrplan/EventFahrplan
* https://github.com/Wilm0r/giggity

More information about the format, and other tools with different approaches can be found on https://c3voc.de/wiki/schedule#conversion_tools

# Usage
```
pip3 install --user -r requirements.txt
./schedule.py -vvd -c ./demo/gpn11.ini
```
For more information about the input parameters and the generated output
have a look at the `demo` directory, this should be a good starting point.

# Currently supported inputs
* [CSV](demo/gpn11.csv)
* schedule JSON
* [Proyektor](demo/fusion22.json)

# Currently supported outputs
* [schedule XML](https://github.com/voc/schedule/tree/master/validator/xsd)
    * extended schedule XML, with additional `video_download_url` in events
* [schedule JSON](https://github.com/voc/schedule/tree/master/validator/json)

# Validator
The generated schedule XML can be validated with the c3voc validator, which can be found at https://github.com/voc/schedule/tree/master/validator and https://c3voc.de/schedulexml/

A quick validation can also be done with:

```
xmllint --noout --schema https://raw.githubusercontent.com/voc/schedule/master/validator/xsd/schedule.xml.xsd schedule.xml
```
