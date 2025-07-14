# Flatlib Astrology Home Assistant Integration

**Flatlib Astrology** is a custom Home Assistant integration that connects to the [Flatlib Natal Chart API Add-on](https://github.com/navi-vonamut/Flatlib-Natal-Chart-API) to retrieve and expose astrological natal chart and transit data as Home Assistant sensors. This allows for dynamic astrological insights within your smart home automations and for feeding data to Large Language Models (LLMs).

---

## 🌟 Features

* **Natal Chart Data:** Fetches comprehensive natal chart data (planets, houses, aspects, etc.) for configured individuals.
* **Transit Data:** Retrieves current transit positions and their aspects to natal chart placements.
* **Single Sensor Output:** All raw astrological data is available as attributes of a single, easy-to-use Home Assistant sensor (`sensor.<person_name>_natal_chart`).
* **LLM Ready:** Provides a structured JSON output of astrological data, ideal for interpretation by LLMs.
* **UI Configuration:** Simple setup and configuration through the Home Assistant UI via Config Flow.

---

## ⚠️ Prerequisites

Before installing this integration, you **must** have the [**Flatlib Natal Chart API Add-on**](https://github.com/navi-vonamut/Flatlib-Natal-Chart-API) installed and running in your Home Assistant instance. This integration relies on that add-on for all astrological computations.

---

## 🚀 Installation

### 1. Install the Flatlib Natal Chart API Add-on (if not already installed)

Follow the installation instructions in the [Flatlib Natal Chart API Add-on repository](https://github.com/navi-vonamut/Flatlib-Natal-Chart-API#installation). **Ensure the add-on is running before proceeding.**

### 2. Install this Custom Integration (Manual)

Currently, this integration is available via manual installation. Support for HACS (Home Assistant Community Store) is planned for the future.

1.  **Create the custom_components folder:** If you don't already have one, create a `custom_components` folder in your Home Assistant configuration directory.
    * Example path: `/config/custom_components/`
2.  **Download the integration files:**
    * Navigate to the [latest release](https://github.com/navi-vonamut/hass-flatlib-integration/releases) of this repository.
    * Download the source code archive (e.g., `Source code (zip)`).
3.  **Extract and copy files:**
    * Unzip the downloaded archive.
    * Copy the folder named `flatlib_astrology` (from inside the unzipped folder, it contains `__init__.py`, `manifest.json`, etc.) into your Home Assistant `custom_components` directory.
    * After copying, your directory structure should look like this:
        ```
        /config/custom_components/
        └── flatlib_astrology/
            ├── __init__.py
            ├── api.py
            ├── config_flow.py
            ├── const.py
            ├── manifest.json
            └── sensor.py
        ```
4.  **Restart Home Assistant:** Go to **Settings** > **System** > **Restart**. This is crucial for Home Assistant to discover the new custom component.

---

## 💡 Configuration

Once installed and Home Assistant restarted:

1.  Go to **Settings** > **Devices & Services**.
2.  Click the **"ADD INTEGRATION"** button in the bottom right corner.
3.  Search for "**Flatlib Astrology**" and select it.
4.  A configuration dialog will appear (thanks to `config_flow`). Fill in the required details for the person's natal chart:
    * **Name:** A unique name for this person (e.g., "Ivan", "My Natal Chart"). This will be used in the sensor entity ID.
    * **Birth Date:** Date of birth.
    * **Birth Time:** Time of birth (local time).
    * **Location:** Birth location (latitude and longitude will be automatically retrieved if you use the map).
    * **Time Zone:** Timezone offset from UTC (e.g., `+03:00` for Eastern European Summer Time, Moldova).

5.  Click **"SUBMIT"**.

If successful, a new device representing the person's astrological data will be created, and a sensor named `sensor.<name_you_entered>_natal_chart` (e.g., `sensor.ivan_natal_chart`) will appear.

---

## 📊 Using the Sensor Data

The `sensor.<person_name>_natal_chart` entity's state will indicate `loaded` if data was successfully retrieved. All the detailed natal chart and transit information from the Flatlib Add-on will be available in its **state attributes**.

### Example usage in a Home Assistant Template or LLM Prompt:

```yaml
# In a template sensor, script, or automation
# To get all natal chart data for 'Ivan'
service: llm_agent.process_text
data:
  text: |
    Анализируй следующую натальную карту:
    {{ state_attr('sensor.ivan_natal_chart', 'natal_chart_data') | to_json }}
    И текущие транзиты:
    {{ state_attr('sensor.ivan_natal_chart', 'transit_data') | to_json }}
  target_agent: "mentor_agent" # Или ваш LLM-ассистент
````

*Note: The exact attribute keys (`natal_chart_data`, `transit_data`) depend on how your `api.py` and the Flatlib Add-on structure their JSON response. Please verify the actual keys in the sensor's state attributes.*

-----

## 💡 Troubleshooting

  * **Add-on not running:** Ensure the "Flatlib Natal Chart API" add-on is installed, started, and running without errors in its logs. This integration cannot work without it.
  * **Incorrect `time_zone`:** Double-check the timezone offset from UTC (e.g., `+03:00`, `-05:00`). This is crucial for accurate calculations.
  * **Check Home Assistant Logs:** For any issues, check the Home Assistant logs (**Settings** \> **System** \> **Logs**) for errors related to `flatlib_astrology`.

-----

## 🤝 Contribution

Contributions are welcome\! If you have suggestions, find issues, or want to contribute code, please open an issue or submit a pull request on GitHub.

-----

## 📄 License

This project is licensed under the [MIT License](https://www.google.com/search?q=LICENSE).

