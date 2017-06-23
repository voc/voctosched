# schedule-ng
Scripts for converting various formats to frab-style https://github.com/frab/frab fahrplan XML.
This also my or maynot be usefull for users of pentabarf.

This repository implements a object representation of the frab export data model.
This can be used to build different in-/exporter or manipulators for the frab schedule export.

There is also a number of application which can display the schedule on mobile devices or infoscreens.
Some example are:

* https://infobeamer.com
* https://github.com/tuxmobil/CampFahrplan
* https://github.com/Wilm0r/giggity

# currently supported Inputs
* CSV

# validator
The generated XML can be validated with the c3voc validator
which can be found here https://github.com/voc/schedule/tree/master/validator
