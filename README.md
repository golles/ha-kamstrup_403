# Kamstrup 403

[![GitHub Release][releases-shield]][releases]
[![GitHub Repo stars][stars-shield]][stars]
[![License][license-shield]](LICENSE)
[![GitHub Activity][commits-shield]][commits]
[![Code coverage][codecov-shield]][codecov]
[![hacs][hacs-shield]][hacs]
[![installs][hacs-installs-shield]][ha-active-installation-badges]
[![Project Maintenance][maintenance-shield]][maintainer]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

Kamstrup 403 custom component for Home Assistant.

<img width="660" alt="info" src="https://user-images.githubusercontent.com/2211503/200671065-201f84bc-0d01-4a87-8fd9-3da3beedfb5d.png">

## Requirements

To use this custom component, you'll need an optical eye and connect your machine running Home Assistant directly with the optical eye to the Kamstrup meter.
The optical eye looks like this:<br>
![cable](https://user-images.githubusercontent.com/2211503/136630069-9da49f09-6f9c-4618-8255-40195405f21a.jpg)

### Placing the optical eye

There is not a lot of tolerance for placing the optical eye on the meter, it can be very tedious to get this right. The best way is to fix the optical eye to the meter. I suggest this 3D-printed holder from [Thingiverse](https://www.thingiverse.com/thing:5615493).<br>
![647d4ce9-4e72-4c54-95e6-d4caf720a79b](https://user-images.githubusercontent.com/2211503/200637881-19fd9166-ea5c-4805-a127-4b9be87f2de5.jpeg)

### Supported devices

This component is created to only support the Kamstrup 403 meter. This is a conscious decision because I do own this device and I can only offer support for that. There are some similar devices that work with the same communication protocol. If it does work for a meter that isn't listed below, please create a [feature request](https://github.com/golles/ha-kamstrup_403/issues/new?template=supported_device.yaml) so I can update the table.
Meter | Supported | Description
-- | -- | --
Kamstrup 403 | Yes |
Kamstrup 302 | Yes | Confirmed by email
Kamstrup 402 | Yes | Confirmed in [#14](https://github.com/golles/ha-kamstrup_403/issues/27)
Kamstrup 601 | Yes | Confirmed in [#14](https://github.com/golles/ha-kamstrup_403/issues/14)
Kamstrup 602 | Yes | Confirmed in [#10](https://github.com/golles/ha-kamstrup_403/issues/10)
Kamstrup 603 | Yes | Confirmed in [#18](https://github.com/golles/ha-kamstrup_403/issues/18)
Kamstrup MC66C | No | Supported in my [old component](https://github.com/golles/Home-Assistant-Sensor-MC66C)

## Installation

### HACS

This component can easily be installed in your Home Assistant using HACS.

### Manual

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `kamstrup_403`.
4. Download _all_ the files from the `custom_components/kamstrup_403/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Kamstrup 403"

Using your HA configuration directory (folder) as a starting point you should now also have these files:

```text
custom_components/kamstrup_403/pykamstrup/__init__.py
custom_components/kamstrup_403/pykamstrup/const.py
custom_components/kamstrup_403/pykamstrup/kamstrup.py
custom_components/kamstrup_403/translations/en.json
custom_components/kamstrup_403/translations/nl.json
custom_components/kamstrup_403/__init__.py
custom_components/kamstrup_403/config_flow.py
custom_components/kamstrup_403/const.py
custom_components/kamstrup_403/coordinator.py
custom_components/kamstrup_403/diagnostics.py
custom_components/kamstrup_403/manifest.json
custom_components/kamstrup_403/sensor.py
```

## Configuration

Configuration is done in the UI. It's recommended to use devices as `/dev/serial/by-id` and not `/dev/ttyUSB1` as the port. This is because the first example is a stable identifier, while the second can change when USB devices are added or removed, or even when you perform a system reboot.<br>
The port should look like this: `/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_D307PBVY-if00-port0`. If the port is a remote port (e.g. by using ser2net) it's possible to use a socket connection too, by using something similar to `socket://192.168.1.101:20019`.

Some meters contain a battery, and communicating with the meter does impact battery life. By default, this component updates every `3600` seconds (1 hour). This is configurable. Also, since version `2.0.1` you can also configure the serial timeout. The default value is `1.0` seconds, if you get the error `Finished update, No readings from the meter. Please check the IR connection` you can try to increase this value. Fractional numbers are allowed (eg. `0.5`).
You can do this by pressing `configure` on the Integrations page:

<img width="300" alt="integration" src="https://user-images.githubusercontent.com/2211503/200671075-39c7a812-42a2-4a4d-8934-6ea37517a400.png"> <img width="300" alt="configure" src="https://user-images.githubusercontent.com/2211503/201747344-b019693a-1d88-4ca1-9a28-87fa24992e13.png">

### Sensors

This component comes with many sensors, and most of the sensors are disabled by default. This is to preserve the battery life of the meter, reading data uses an internal battery, so it's advisable to not read too much data too often. If you like, you can enable as many sensors as you want, it's good to keep a good balance between the number of sensors you enable and the configured `Scan interval`.
Next to that, the component will read up to 8 sensors in one interaction with the meter.

## Integration in the energy dashboard

This component does support integration into the Home Assitant's energy dashboard.

### Heat Energy (E1)

This sensor, with unit `GJ`, can since Home Assistant release 2022.11 directly be added to the energy dashboard. It's important to understand that you need to add this in the individual devices section. So not in the electricity or gas section. The devices here will be added on the bottom of your energy dashboard in a horizontal bar graph showing all your devices in `kWh`. This is by design and can't be changed by this component.

### Heat Energy to Gas

From version `2.0.0` of this component, there is `Heat Energy to Gas` sensor, this is disabled by default and needs to be manually enabled. It's also required to have the `Heat Energy (E1)` sensor enabled for this to work.
This sensor acts as a `gas` sensor with the `m³` unit and has the same value as `Heat Energy (E1)`. This sensor can be added to the energy dashboard in the gas section. The added value for this is, that you get a better visual representation in the energy dashboard, eg hourly graphs.

## Collect logs

When you want to report an issue, please add logs from this component. You can enable logging for this component by configuring the logger in Home Assistant as follows:

```yaml
logger:
  default: warn
  logs:
    custom_components.kamstrup_403: debug
```

More info can be found on the [Home Assistant logger integration page](https://www.home-assistant.io/integrations/logger)

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

[buymecoffee]: https://www.buymeacoffee.com/golles
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/golles/ha-kamstrup_403.svg?style=for-the-badge
[codecov]: https://app.codecov.io/gh/golles/ha-kamstrup_403
[codecov-shield]: https://img.shields.io/codecov/c/github/golles/ha-kamstrup_403?style=for-the-badge
[commits]: https://github.com/golles/ha-kamstrup_403/commits/main
[hacs]: https://github.com/hacs/integration
[hacs-shield]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[ha-active-installation-badges]: https://github.com/golles/ha-active-installation-badges
[hacs-installs-shield]: https://raw.githubusercontent.com/golles/ha-active-installation-badges/main/badges/kamstrup_403.svg
[license-shield]: https://img.shields.io/github/license/golles/ha-kamstrup_403.svg?style=for-the-badge
[maintainer]: https://github.com/golles
[maintenance-shield]: https://img.shields.io/badge/maintainer-golles-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/golles/ha-kamstrup_403.svg?style=for-the-badge
[releases]: https://github.com/golles/ha-kamstrup_403/releases
[stars-shield]: https://img.shields.io/github/stars/golles/ha-kamstrup_403?style=for-the-badge
[stars]: https://github.com/golles/ha-kamstrup_403/stargazers
