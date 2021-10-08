# Kamstrup 403

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

**This component will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Show info from the meter.

## Requirements

To use this component, you'll need a cable with an IR read/write head and connect your machine running Home Assistant directly to the IR sensor of the Kamstrup meter.
For me, this USB-cable from [Ebay](https://www.ebay.nl/itm/USB-IR-Infrarot-Lese-Schreibkopf-f%C3%BCr-Stromz%C3%A4hler-Smart-Meter/274095213723) worked perfectly. The one from [Volkszaehler.org](https://wiki.volkszaehler.org/hardware/controllers/ir-schreib-lesekopf) seems to work fine as well, but might be harder to get.
![cable](https://user-images.githubusercontent.com/2211503/136630069-9da49f09-6f9c-4618-8255-40195405f21a.jpg)


## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `kamstrup_403`.
4. Download _all_ the files from the `custom_components/kamstrup_403/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Kamstrup 403"

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/kamstrup_403/translations/en.json
custom_components/kamstrup_403/translations/nl.json
custom_components/kamstrup_403/__init__.py
custom_components/kamstrup_403/config_flow.py
custom_components/kamstrup_403/const.py
custom_components/kamstrup_403/entity.py
custom_components/kamstrup_403/kamstrup.py
custom_components/kamstrup_403/manifest.json
custom_components/kamstrup_403/sensor.py
```

## Configuration is done in the UI

It's recommended to use devices as `/dev/serial/by-id` and not `/dev/ttyUSB1` as the port, as the first one should be stable, while the second one can change when you add/remove usb (serial) adapters, or even when you perform a system reboot.  
The port will become something like: `/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_D307PBVY-if00-port0`.

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[knmi]: https://github.com/golles/ha-kamstrup_403
[buymecoffee]: https://www.buymeacoffee.com/golles
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/golles/ha-kamstrup_403.svg?style=for-the-badge
[commits]: https://github.com/golles/ha-kamstrup_403/commits/main
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/golles/ha-kamstrup_403.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-golles-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/golles/ha-kamstrup_403.svg?style=for-the-badge
[releases]: https://github.com/golles/ha-kamstrup_403/releases
