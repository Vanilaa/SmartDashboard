# Smart Dashboard

This project is a interactive dashboard built on a Raspberry Pi. It integrates a 64x32 RGB LED Matrix and a PiTFT touchscreen to create a smart display that allows you to control Spotify, check the weather, and draw pixel art in real-time.

## Features

The system features a main **Home Screen** that displays the date, time, and a greeting, along with a menu to navigate between three main applications:

1.  **🎵 Spotify Player**
    * **Control:** Play, Pause, Skip, and Previous tracks directly from the touchscreen.
    * **Display:** Shows the current track name, artist, and album art on the LED matrix.
    * **Backend:** Uses the Spotify API to fetch real-time playback data.

2.  **🎨 Scribble**
    * **Interactive Drawing:** Draw on the PiTFT touchscreen using a color palette.
    * **Real-time Sync:** Your drawing is instantly mapped and displayed on the 64x32 LED Matrix.
    * **Save:** Ability to save your creations.

3.  **☁️ Weather Station**
    * **Live Data:** Displays current weather conditions, temperature, and humidity.
    * **Visuals:** Animated GIFs (sun, rain, snow, clouds) on the LED matrix representing the current weather.
    * **Sun Cycle:** Shows Sunrise or Sunset times based on the time of day.

## 🛠️ Hardware Requirements

* **Raspberry Pi** (3B+ or 4 recommended)
* **RGB LED Matrix** (64x32) & Bonnet/HAT
* **PiTFT Touchscreen** (320x240)
* **Power Supply** (Adequate power for both Pi and Matrix)

## 📦 Software Dependencies

This project relies on several Python libraries. You can install them using pip:

```bash
sudo pip3 install spotipy pygame pillow RPi.GPIO requests
