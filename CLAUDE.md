# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Home Assistant custom integration for the Kamstrup 403 heating meter. Reads energy consumption, temperatures, flow rates, and other meter data via a serial connection using an optical IR eye, using the Kamstrup Meter Protocol (KMP).

## Commands

### Setup

```bash
./scripts/setup_env.sh    # Install deps via uv, npm, configure pre-commit hooks
```

### Development

```bash
./scripts/develop.sh      # Run Home Assistant locally with the integration loaded (config/ dir)
```

### Testing

```bash
uv run pytest                                     # Run all tests with coverage
uv run pytest tests/test_sensor.py                # Run a single test file
uv run pytest tests/test_sensor.py::test_state    # Run a single test
uv run pytest -k "test_state"                     # Run tests matching pattern
```

### Linting & Formatting

```bash
uv run mypy .                                              # Type checking
uv run ruff check --fix .                                  # Linter
uv run ruff format .                                       # Formatter
uv run pylint custom_components/kamstrup_403 tests         # Pylint
npm run prettier -- --write .                              # YAML/JSON/Markdown
uv run yamllint .                                          # YAML lint
uv run shellcheck scripts/*.sh                             # Shell scripts
./scripts/local_ci_checks.sh                               # Full CI suite locally
```

## Architecture

### Integration Layer (`custom_components/kamstrup_403/`)

The integration follows the standard Home Assistant coordinator pattern:

- **`__init__.py`** — Entry point. Calls `async_setup_entry` / `async_unload_entry`, creates the coordinator, and forwards setup to the sensor platform. The coordinator is stored in `config_entry.runtime_data`.
- **`coordinator.py`** — `KamstrupUpdateCoordinator` manages all meter communication. Sensors register their commands via `coordinator.register_command(command_id)`. On each update cycle, the coordinator fetches data for all registered commands in batches (max 8 per update, a protocol constraint). Stores results keyed by command ID as `{"value": ..., "unit": ...}`.
- **`sensor.py`** — Defines the sensor entity class hierarchy. Most sensors have `entity_registry_enabled_default = False` to avoid excessive polling (battery life concern).
- **`config_flow.py`** — UI flow for configuring the serial port (`ConfigFlow`) and options flow for scan interval and read timeout (`OptionsFlow`).
- **`diagnostics.py`** — HA diagnostics support; exposes `config_entry`, `data`, and `registered_commands` for debugging.
- **`const.py`** — Domain name, default values (scan interval: 3600s, timeout: 1.0s, baudrate: 1200 baud — fixed by KMP).

### Sensor Class Hierarchy

- **`KamstrupSensor`** — Base class. Reads `coordinator.data[data_key]`. Does not register commands.
- **`KamstrupMeterSensor`** — Extends base. Registers/unregisters command IDs with the coordinator via `async_added_to_hass` / `async_will_remove_from_hass`. Unit of measurement falls back to what the meter reports.
- **`KamstrupDateSensor`** — Extends `KamstrupMeterSensor`. Converts raw float values in `yymmdd.0` format to `datetime` objects in the local timezone.
- **`KamstrupGasSensor`** — Extends base (not `KamstrupMeterSensor`). Derives from heat energy (command 60) without registering its own command — it piggybacks on command 60 already registered by the Heat Energy sensor.

### Protocol Library (`custom_components/kamstrup_403/pykamstrup/`)

A standalone KMP serial protocol implementation (`kamstrup.py`). This was reverse-engineered and handles the low-level framing (escape sequences, 0x0D terminator), CRC-16/CCITT, and serial I/O via `serialx`. Sensor command IDs (e.g., 60 = Heat Energy, 68 = Volume) are defined in `pykamstrup/const.py`. The `get_values()` method supports batching up to 8 commands in a single request.

### Test Suite (`tests/`)

- **`conftest.py`** — Key fixtures: `mock_kamstrup` (patches `Kamstrup` class with `AsyncMock`), `enable_all_entities` (overrides `entity_registry_enabled_default` so all sensors are active in tests), `auto_enable_custom_integrations`.
- **`__init__.py`** — Helper `setup_integration(hass, config_entry)` used in most test files to bootstrap the integration.
- Tests are fully async (`asyncio_mode = "auto"` via pytest-asyncio). The `pytest-homeassistant-custom-component` package provides HA test infrastructure (`hass` fixture, etc.).

## Code Standards

- **Line length**: 150 characters
- **Docstring style**: Google
- **Type hints**: Required (enforced by mypy)
- **Async**: All integration I/O is async
- **Formatter**: Ruff (Black-compatible), Prettier for non-Python files
