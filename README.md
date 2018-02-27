# RedTools-Rig-Light

Light version of python script for monitoring Claymore's Dual Ethereum miner via API. 

The script wait request to Telegram bot and sends cumulative information about:
  1. Uptime of Claymore
  2. Current total hashrate of Rig
  3. Hashrate of each GPU
  4. Temperature of each GPU
  5. Fan speed of each GPU
  6. Number of accepted shares
  7. Number of invalid shares

## Screenshot
![Alt text](https://github.com/pistonov/RedTools-Rig-Light/raw/master/screen.jpg "Optional Title")

## Dependencies:
Telegram bot. 

### Installation:

#### In linux:
   *Install Python telepot package:*
   *```pip install telepot```*

#### In Windows:
   *Install Python 2.x.*
   
   *Install Python telepot package: ```C:\Python27\Tools\Scripts\pip.exe install telepot```*
  
## Setup:
  Set all necessary parameters at config section & add scrypt to startup

All comments and additions are welcome.
  
