# voctosched
Scripts for converting various formats to [frab](https://github.com/frab/frab)-style fahrplan XML.
This also may or may not be useful for users of [pentabarf](https://github.com/nevs/pentabarf).

This repository implements an object representation of the frab export data model.
This can be used to build different im-/exporters or manipulators for the frab schedule export.

There is also a number of application which can display the schedule on mobile devices or infoscreens.
Some examples are:

* https://infobeamer.com
* https://github.com/tuxmobil/CampFahrplan
* https://github.com/Wilm0r/giggity

# Currently supported inputs
* CSV

# Currently supported outputs
* basic XML, frab format
* extended XML, with additional `video_download_url` in events

# Validator
The generated XML can be validated with the c3voc validator, which can be found here https://github.com/voc/schedule/tree/master/validator

A quick validation can also be done with:

```
xmllint --noout --schema https://github.com/zuntrax/voctosched/blob/master/schema/basic.xsd schedule.xml
```

For our extended format, use:

```
xmllint --noout --schema https://github.com/zuntrax/voctosched/blob/master/schema/extended.xsd schedule.xml
```

# License
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/.

Full license text [here](LICENSE).
