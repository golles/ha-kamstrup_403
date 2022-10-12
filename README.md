# Kamstrup 403

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

Kamstrup 403 custom component for Home Assistant.

<img width="663" alt="info" src="https://user-images.githubusercontent.com/2211503/173236049-10647d83-9be6-49a6-a90b-671a8860c743.png">

## Requirements

To use this component, you'll need a cable with an IR read/write head and connect your machine running Home Assistant directly to the IR sensor of the Kamstrup meter.
The one from [Volkszaehler.org](https://wiki.volkszaehler.org/hardware/controllers/ir-schreib-lesekopf) seems to work fine, but might be hard to get.  
The read/write head looks like this:  
![cable](https://user-images.githubusercontent.com/2211503/136630069-9da49f09-6f9c-4618-8255-40195405f21a.jpg)


### Supported devices

This component is created to only support the Kamstrup 403 meter. This is a conscious decision because I do own this device and I can only offer support for that. There are some similar devices that work with the same communication protocol. If it does work for a meter that isn't listed below, please create a [feature request](https://github.com/golles/ha-kamstrup_403/issues/new?template=supported_device.yaml) so I can update the table.
Meter | Supported | Description
-- | -- | --
Kamstrup 403 | Yes | 
Kamstrup 601 | Yes | Confirmed in [#14](https://github.com/golles/ha-kamstrup_403/issues/14)
Kamstrup 602 | Yes | Confirmed in [#10](https://github.com/golles/ha-kamstrup_403/issues/10)
Kamstrup 603 | Yes | Confirmed in [#18](https://github.com/golles/ha-kamstrup_403/issues/18)
Kamstrup 402 | Maybe | [Mentioned here](https://github.com/golles/ha-kamstrup_403/blob/main/custom_components/kamstrup_403/kamstrup.py#L12)
Kamstrup MC66C | No | Supported in my [old component](https://github.com/golles/Home-Assistant-Sensor-MC66C)


## Installation

### HACS

This component can be installed in your Home Assistant with HACS.


### Manual

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

It's recommended to use devices as `/dev/serial/by-id` and not `/dev/ttyUSB1` as the port. This because the first example is a stable identifier, while the second one can change when USB devices are added or removed, or even when you perform a system reboot.  
The port will be like: `/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_D307PBVY-if00-port0`.

Some meters contain a battery, and communicating with the meter does impact battery life. By default, this component updates every 60 seconds. From version `1.2.0`, you can configure the update interval on the Integrations page:

<img width="290" alt="opt1" src="https://user-images.githubusercontent.com/2211503/173235828-fd130b51-99b0-4522-b697-4d69df51925d.png"> <img width="392" alt="opt2" src="https://user-images.githubusercontent.com/2211503/173235826-ffd79769-cc2c-4404-9b79-d233aef8587e.png">

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
