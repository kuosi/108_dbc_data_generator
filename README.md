<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/kuosi/CAN-data-generator">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">DBC Data Generator</h3>

  <p align="center">
    A CAN Data generator based on a CAN-Matrix described with a Vector .dbc format.
    <br />
    <a href="https://github.com/kuosi/CAN-data-generator"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/kuosi/CAN-data-generator">View Demo</a>
    ·
    <a href="https://github.com/kuosi/CAN-data-generator/issues">Report Bug</a>
    ·
    <a href="https://github.com/kuosi/CAN-data-generator/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Usage](#usage)
  * [Configuration file](#configuration-file)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com)-->

If you are developing a software for a vehicle IoT device, but does not have the possibility to collect CAN data from a real vehicle, then this might be what you are looking for.

I'll be adding more features in the near future. You may also suggest changes by opening an issue.

A list of commonly used resources that I find helpful are listed in the acknowledgements.

### Built With

* [Docker](https://www.docker.com/) -- Optional
* [Python3](https://www.python.org/)


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

If you have a real can interface, turn it on as usual.

If you do not have real can interface, create a virtual can interface.

* vcan0
```
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0
```

### Usage

#### Python3

```
usage: main.py [-h] -d CONFIGDIR -c CONFIGFILE -b DBCFILE

optional arguments:
  -h, --help            show this help message and exit
  -d CONFIGDIR, --configdir CONFIGDIR
                        Directory containing the configuration and dbc files
  -c CONFIGFILE, --configfile CONFIGFILE
                        Configuration file
  -b DBCFILE, --dbcfile DBCFILE
                        DBC file
```

#### Docker

Adapt the file docker-compose.yml to match your own configuration.

```
docker-compose -up
```


### Configuration file

```
{
    "can": {
        "fd": <True if can message with size <= 64 Bytes shall be sent. Shall match with the CAN interface.>,
        "frequency": <Frequency between message.>,
        "interface": <Configured can interface where the generated can data shall be sent.>
    },
    "dbc": {
        "IDs": <Semi-column separated CAN IDs.>
    }
}
```

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/kuosi/CAN-data-generator/issues) for a list of proposed features (and known issues).


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact

Winnie Pobouh - [www.kuosi.io](https://kuosi.io)

Project Link: [https://github.com/kuosi/CAN-data-generator](https://github.com/kuosi/CAN-data-generator)


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Source for dbc file samples](http://hackage.haskell.org/package/ecu)
* [Cantools](https://pypi.org/project/cantools/)
* [Python CAN](https://pypi.org/project/python-can/)
* [README-Template](https://github.com/othneildrew/Best-README-Template)