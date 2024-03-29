[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

_Component to integrate with [kamstrup_403][kamstrup_403]._

**This component will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Show info from the meter.

{% if not installed %}
## Installation

1. Click install.
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Kamstrup 403".

{% endif %}


## Configuration is done in the UI

It's recommended to use devices as `/dev/serial/by-id` and not `/dev/ttyUSB1` as the port, as the first one should be stable, while the second one can change when you add/remove usb (serial) adapters, or even when you perform a system reboot.
The port will become something like: `/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_D307PBVY-if00-port0`.

***

[kamstrup_403]: https://github.com/golles/ha-kamstrup_403
[buymecoffee]: https://www.buymeacoffee.com/golles
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/golles/ha-kamstrup_403.svg?style=for-the-badge
[commits]: https://github.com/golles/ha-kamstrup_403/commits/main
[hacs]: https://hacs.xyz
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license]: https://github.com/golles/ha-kamstrup_403/blob/main/LICENSE
[license-shield]: https://img.shields.io/github/license/golles/ha-kamstrup_403.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-golles-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/golles/ha-kamstrup_403.svg?style=for-the-badge
[releases]: https://github.com/golles/ha-kamstrup_403/releases
[user_profile]: https://github.com/golles
