/* Raspberry Pi Pin Mappings for NB Board LP 0 Only!!!!!
*
* revision 0.1 - Initial revision with proposed mappings
* revision 0.2 - Added raspberry Pi version and set I2CP bus for private bus (EEPROM and Display)
* revision 1.0 - New hardware has pin shift on SPI CE0 and CE1
*
* GP2 to GP9 go to Arduino Connector
* GP8 Connected to Button #1
* GP9 Connected to Button #2
* GP10 Connected to Button #3
* GP11 Connected to Button #4
*
* SPI_CS0 only goes to ADC 3208
* SPI control signals goto user connectors gated by SPI_CS0
*
* I2CP bus goes to EEPROM and Display - Consider as Private Bus
*
* I2C1 bus goes to Arduino Connector and user connectors
*/

#include <stdio.h>
#include "mraa.h"

#define HIGH  1
#define LOW   0

#define TRUE  1
#define FALSE 0


// mraa pin numbers
// Note for Raspberry Pi the MRAA GPIO are defined as the physical pin numbers

//  SPI Bus Controls
int SPI_MISO_PIN 	= 21;  //GPIO9
int SPI_MOSI_PIN 	= 19; //GPIO10
int SPI_CLK_PIN 	= 23; //GPIO11

int SPI_CS0_PIN	    = 24;  //GPIO25
int SPI_CS1_PIN     = 26;   //GPIO8

// I2C Bus Controls
int I2C1_BUS        = 1;   //I2C Bus # 
int I2C1_SCL_PIN    = 5;   //GPIO3
int I2C1_SDA_PIN    = 3;   //GPIO2

int I2CP_BUS        = 0;   //I2C Bus #  - Note we are faking this out for code consistancy
int I2C2_SCL_PIN    = 28;  //I2C0_SCL   Note no GPIO on these pins
int I2C2_SDA_PIN    = 27;  //I2C0_SDA - Note no GPIO on these pins

// GP - General Purpose io pins
int GP2             = 7;   //GPIO4
int GP3             = 15;  //GPIO22
int GP4             = 16;  //GPIO23
int GP5             = 26;  //GPIO7
int GP6             = 36;  //GPIO19
int GP7             = 18;  //GPIO24
int GP8             = 32;  //GPIO12
int GP9             = 33;  //GPIO13
int GP10            = 37;  //GPIO26
int GP11            = 36;  //GPIO16

// Serial bus Mux control pins
int UARTSEL0       =   29;  //GPIO5
int UARTSEL1       =   31;  //GPIO6
 
