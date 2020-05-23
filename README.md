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
  <a href="https://github.com/kuosi/108_dbc_data_generator">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">DBC Data Generator</h3>

  <p align="center">
    A CAN Data generator based on a CAN-Matrix described with a Vector .dbc format.
    <br />
    <a href="https://github.com/kuosi/108_dbc_data_generator"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/kuosi/108_dbc_data_generator">View Demo</a>
    ·
    <a href="https://github.com/kuosi/108_dbc_data_generator/issues">Report Bug</a>
    ·
    <a href="https://github.com/kuosi/108_dbc_data_generator/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
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

* [Snapcraft](https://snapcraft.io/)
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

### Installation

The software is installed as a snap package which starts a service.

```snap install 108_dbc_data_generator --dangerous --devmode
```

<!-- USAGE EXAMPLES -->
## Usage

* set the can interface
```
snap set 108_dbc_data_generator can.interface=vcan0
```

* set the frequency for generating can data (hz)
```
snap set 108_dbc_data_generator can.frequency=vcan0
```

* set the dbc file
```
snap set 108_dbc_data_generator dbc.file=full_path_to_dbc_file
```

* set the text file containing the list of message name that shall be considerd during the generation of data
```
snap set 108_dbc_data_generator dbc.messages=full_path_to_messages_file
```

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/kuosi/108_dbc_data_generator/issues) for a list of proposed features (and known issues).


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Winnie Pobouh - [www.winniepobouh.com](https://winniepobouh.com)

Project Link: [https://github.com/kuosi/108_dbc_data_generator](https://github.com/kuosi/108_dbc_data_generator)


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [Source for dbc file samples](http://hackage.haskell.org/package/ecu)
* [Numpy](https://pypi.org/project/numpy/)
* [Python CAN](https://pypi.org/project/python-can/)
* [README-Template](https://github.com/othneildrew/Best-README-Template)