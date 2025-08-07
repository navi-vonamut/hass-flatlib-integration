# Flatlib Astrology Home Assistant Integration

**Flatlib Astrology** is a custom Home Assistant integration that connects to the **[Flatlib Astrology API Add-on](https://github.com/navi-vonamut/Flatlib-Natal-Chart-API)** to retrieve and expose astrological data as Home Assistant sensors. This allows for dynamic astrological insights within your smart home automations and for feeding data to Large Language Models (LLMs).

-----

## 🌟 Features (v0.2.0)

  * **Natal Chart Data:** Fetches comprehensive natal chart data (planets, houses, aspects, etc.) for configured users.
  * **Daily, Monthly, & Yearly Horoscopes:** New sensors to provide predictions for different time periods.
  * **Convenient UI Configuration:** Replaces plain text inputs with **SelectSelectors**, allowing you to choose from existing Home Assistant users and all available timezones, simplifying the setup process.
  * **LLM Ready:** Provides a structured JSON output, ideal for interpretation by LLMs.
  * **Config Flow:** Offers a simple and intuitive setup process directly through the Home Assistant UI.

-----

## ⚠️ Prerequisites

Before installing this integration, you **must** have the **[Flatlib Astrology API Add-on](https://github.com/navi-vonamut/Flatlib-Natal-Chart-API)** installed and running. This integration relies on that add-on for all astrological computations.

-----

## 🚀 Installation

### 1\. Install the Flatlib Astrology API Add-on (if not already installed)

Follow the installation instructions in the [Flatlib Astrology API Add-on repository](https://github.com/navi-vonamut/Flatlib-Natal-Chart-API#installation). **Ensure the add-on is running before you proceed.**

### 2\. Install this Custom Integration (Manual)

1.  **Create the `custom_components` folder:** If you don't already have one, create a `custom_components` folder in your Home Assistant configuration directory (typically `/config/`).
2.  **Download the integration files:**
      * Navigate to the [latest release](https://github.com/navi-vonamut/hass-flatlib-integration/releases) of this repository.
      * Download the source code archive (e.g., `Source code (zip)`).
3.  **Extract and copy files:**
      * Unzip the downloaded archive.
      * Copy the folder named `flatlib_astrology` into your Home Assistant `custom_components` directory.
      * Your directory structure should look like this:
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
4.  **Restart Home Assistant:** Go to **Settings** \> **System** \> **Restart**. This is crucial for Home Assistant to discover the new custom component.

-----

## ⚙️ Configuration

Once installed and Home Assistant has restarted:

1.  Go to **Settings** \> **Devices & Services**.
2.  Click the **"ADD INTEGRATION"** button in the bottom right corner.
3.  Search for "**Flatlib Astrology**" and select it.
4.  A configuration dialog will appear. Fill in the required details for the person's natal chart:
      * **User:** Select a Home Assistant user from the dropdown list. Their name will be used for the sensor entity IDs.
      * **Birth Date:** The date of birth.
      * **Birth Time:** The time of birth (local time).
      * **Location:** The place of birth.
      * **Time Zone:** Select the timezone from the dropdown list.
5.  Click **"SUBMIT"**.

This will create a new device for the user and a set of sensors for their natal chart data and daily, monthly, and yearly horoscopes.

-----

## 📊 Using the Sensor Data

Each sensor will have an entity ID based on the user's name (e.g., `sensor.<name>_natal_chart`, `sensor.<name>_daily_prediction`). The detailed data will be available in the sensor's **state attributes**.

### Example usage in a Home Assistant Template or for an LLM:

```yaml
# Example in a Home Assistant template to get daily horoscope data
service: llm_agent.process_text
data:
  text: |
    Analyze the following daily horoscope:
    {{ state_attr('sensor.ivan_daily_prediction', 'prediction_data') | to_json }}
  target_agent: "mentor_agent"
```

*Note: The exact attribute keys (`prediction_data`, `natal_chart_data`) may vary depending on how you've structured the JSON responses in your `api.py` and `sensor.py` files.*

-----

## 🔧 Troubleshooting

  * **Add-on not running:** Ensure the "Flatlib Astrology API" add-on is installed, started, and running without errors.
  * **Check Home Assistant Logs:** For any issues, check the Home Assistant logs (**Settings** \> **System** \> **Logs**) for messages related to `flatlib_astrology`.

-----

## 🤝 Contribution

Contributions are welcome\! If you have suggestions, find issues, or want to contribute code, please open an issue or submit a pull request on GitHub.

-----

## 📄 License

This project is licensed under the [MIT License](https://www.google.com/search?q=https://github.com/navi-vonamut/hass-flatlib-integration/blob/main/LICENSE).