# Dashboard Decor

This project is managed by Yaqi (yg298) and Alina (lw584) during Fall 2023 and demonstrate on 12/7/2023.
<center><img src="img/grouppic.jpg" width="300" height="400"></center>

## Objective
In this project, we want to make our home or study area more comfortable, creating this safe space where we would love to study or live in, therefore we came up with the idea of creating a desktop gadget. We envision this to be a versatile, fun, and aesthetic decor for someone who is into Pixel art. This dashboard will combine different functionalities like controlling Spotify song playback, playing drawing and guessing game, entering Zen mode with weather forecast, and displaying cute animations
<center><img src="img/welcome.png" width="400" height="320"></center>

## Introduction
We imagine this dashboard to be like a small widget where the user will be able to check for the current date, time, a short greeting based on the time of the day, current weather conditions, temperature/humidity, and sunrise/sunset time. For other interactive functions, we want it to be able to connect to the user’s Spotify account so it can control the playlist, skip back and forth in the playlist, and display the album cover. We also want to add a game to the dashboard, at first we wanted to implement Dianasour’s Jumping game in Google, but the LED panel’s pitch is too large and the animation on it doesn’t look very good, so we pivoted to a drawing game in which the player can either play with a friend, or it can be single player and just let the LED display the artwork user draws.

In terms of the technical components involved in implementation, we want to make use of the PyGame library and TFT screen as we have learned during this semester’s lab sections. Those hardware and software can be customized in so many different ways, giving us many options of how to use them. We also wanted to explore aspects of human-centered deisgn, since this is a highly interactive project. In addition, we want to try out some additional hardware like LED Panel and learn to access external APIs for real-time data and HTTP requests.


## Design and Testing

We followed modular design principles throughout the project. 
<center><img src="img/page.jpg" width="850" height="340"></center>

### LED Panel

#### Wiring

To wire up the LED panel to Raspberry Pi, we referenced the pinouts described in Adafruit's [RGB matrix bonnet tutorial](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/pinouts). 

| left               | right              |
| ------------------ | ------------------ |
| LED# - Func - GPIO | LED# - Func - GPIO |
| 1-R1-5             | 9-G1-13            |
| 2-B1-6             | 10-GND-GND         |
| 3-R2-12            | 11-G2-16           |
| 4-B2-23            | 12-E-24            |
| 5-A-22             | 13-B-26            |
| 6-C-27             | 14-D-20            |
| 7-CLK-17           | 15-LAT-21          |
| 8-OE-4             | 16-GND-GND         |

We also check to make sure that the GPIO pins used for the LED panel does not overlap pins used by TFT. It does turnout that the GPIO pins connected to the buttons on the TFT screen is used by the LED panel. Therefore we incorporated an external button to function as the quit button. 

#### Installing library and running provided examples

We took advantage of hzeller's [Raspberry Pi RGB matrix library](https://github.com/hzeller/rpi-rgb-led-matrix) to control the LED panel with Raspberry Pi. After installing the library, we tried running a few example, with flags `--led-cols=64 --led-rows=32`We observed some issues, where the bottom half of the panel does not light up at all, and we couldn't really tell what is on the top half, which looks like it is glitching. So we went back to double check our wiring and configuration. We found a misplaced wire for the matrix E pin. Plugging it in the right place gives us pixels lighting up on the bottom half. We then found suggestions in the tutorial that with Pi 4, the matrix control speed needs to be dialed back slightly. We changed the `--led-slowdown-gpio` setting to 4, which fixed the glitches. 

#### Creating views individually

We study the examples that came with the library to understand the flow of projecting an image to the LED panel. There are three steps in preparing an image: importing, resizing, and converting format to RGB. We also explored playing animations on the panel by importing gif, process each frame, adding all the frames to a list, loop over the frames and display them on the panel one after the other. We also discovered that the library came with an abundant set of fonts available for use, which allow us to display text on the LED panel.

To allow the user to create their own art piece with this panel, we mapped each pixel drawn on the piTFT screens to a position on the LED screen, store the RGB values in a 2D matrix, loop through the matrix and set each Pixel individually. 

##### Spotify
Upon entering music player mode, the album cover of the current track is downloaded and stored in `album_cover.jpg`. We were careful to make sure that we do not always have to download the cover at each update of the frame, since it takes some time for download to complete. The cover is then resized and displayed on the LED panel, along with name of the track and the artist. 
<center><img src="img/spotify.png" width="400" height="320"></center>

##### Drawing
To allow the user to create their own art piece with this panel, we mapped each pixel drawn on the piTFT screens to a position on the LED screen, store the RGB values in a 2D matrix, loop through the matrix and set each Pixel individually.
<center><img src="img/draw.JPG" width="300" height="420"></center>

##### Weather
The weather screen displays a weather animation which is done by isolating each frame of a weather gif and displaying them in a loop to create the animated effect. On top of the weather animation, we will display the weather information obtained by requesting from an Open API, described below.

#### Accessing real-time weather information with API

For real-time weather info, we decided to use Open Weather API which allows us to make HTTP requests hourly to get accurate weather information.

We store the weather info as a JSON file since it's long and detailed. We only needed a few information like weather condition, temperature, and humidity. Therefore, we can index into the JSON, pull the information out from the JSON file, and display it on top of the animation frames.
<center><img src="img/weather.png" width="400" height="320"></center>

### TFT Screen

#### Installing and testing Spotipy library
The [Spotipy](https://spotipy.readthedocs.io/en/2.22.1/) library is a lightweight python library for the [Spotify Web API](https://developer.spotify.com/documentation/web-api). It has the capability of accessing authorized user’s playlist, devices and controlling playback on the devices by sending http requests and receiving http responses. 
We followed the example on Spotipy documentation and first created and testsed a simple python script to control playback on our personal device through command line. We then organized the code into functions and created our own `my_spotify` library. The library has four functions: initialize, download album cover, add playlist to queue, and fetch current playback’s track title and artist. 


#### Creating user interfaces with Pygame

##### Home Screen

Three icons are centered on the TFT home page: spotify, draw, and weather. Each icon will direct the user to the corresponding page. For implementation, we created these Pygame rects and detected mouse collision with the rects. After switching to the other screen, we will use the pygame’s clear function to clean it.

##### Drawing

For the drawing screen, we want to have a color palette screen where the user can change the color of the paintbrush and a drawing area. Therefore we have 2 main Pygame screens, the color palette consists of the color circles which detects mouse collision to determine which color the user is trying to change to. The drawing screen will blit all the pixel user drawn on it and append the pixel’s coordinate to an RGB matrix which will be mapped to the LED screen at the same time. Therefore, both TFT and LED screens will be able to see the drawing live-time. 

### Other

#### Spotifyd

We also followed a Youtube tutorial on [how to turn Raspberry Pi device into a device on Spotify account](https://www.youtube.com/watch?v=GGXJuzSise4)

Mainly, we added a config file in which we specify the Spotify account logins and added the device we wanted to use to play music which is RPi. 



## Result
<iframe width="500" height="295" src="https://www.youtube.com/embed/SPaAW63JxDM?si=T1H66s3DqAr8YQQ0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>

## Conclusion

We successfully achieved 90% of the functionality we proposed in our proposal and substituted the 10% with functionalities we thought would be more fun to implement as we worked on it. We were able to solve most of the bugs and we pushed through the project even when we lost all of our files when crontab messed up. 
We found out that due to Spotify’s security policy, we won’t be able to use Crontab, since it requires Spotify authorization after each reboot or shutdown. We also learned more about how to restore files if Crontab didn’t function properly, and always backup or at least download our files before reboot. 


## Future Work
There are still a lot to do if we want to improve this project.
1. We can clean up the wires and build a display case for it
2. Add the functionality to save user's artwork
3. Scrolling song title and artist name when they are too long. 

## Budget

| Part         | Quantity          | Our Cost  | Actual Cost|
|:-------------|:------------------|:----------|:-----------|
| RPi          | 1                 | 0         | 45         |
| TFT screen   | 1                 | 0         | 45         |
| Button       | 1                 | 0         | 0.5        |
| LED Panel    | 2                 | 0         | 45         |
| 5V 4A adapter| 1                 | 0         | 0          |
| Jump wires   | a handful         | 0         | 0          |


Total: $135.5

## Reference

### Libraries

1. pygame
2. spotipy
3. spotifyd
4. rpi-rgb-led-marix

### Tutorials/Guides
These are linked though out the webpage for seamless reading.


### Code Appendix
Below is our master code where we integrated everything: [Master Code](code/dashboard.py)

Below is the Spotify API code where we defined our own functions to help us download album cover, switch between songs, and pulling song infos: [Spotify API Code](code/my_spotify.py)
