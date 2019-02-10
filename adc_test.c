#include "mraa_raspberry_pi_pinmap.h"
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#define LCD_ADDR 0x3e
#define MAX7500_I2C_ADDR 0x48
#pragma GCC diagnostic ignored "-Wwrite-strings"


mraa_i2c_context i2cp;
mraa_gpio_context MCP3208_DIN;
mraa_gpio_context MCP3208_DOUT;
mraa_gpio_context MCP3208_CLK;
mraa_gpio_context MCP3208_CS;
mraa_gpio_context MCP3208_CS1;


int GetMCP3208 (int Channel)
{
        int i;
        int val;

        mraa_gpio_write (MCP3208_DIN, 0);
        mraa_gpio_write (MCP3208_CLK, 0);
        mraa_gpio_write (MCP3208_CS, 0);

        Channel = Channel | 0x18;
        for (i = 0; i < 5; i ++)
        {
                if (Channel & 0x10)
                {
                        mraa_gpio_write (MCP3208_DIN, 1);
                }
                else
                {
                        mraa_gpio_write (MCP3208_DIN, 0);
                }
                Channel <<= 1;

                mraa_gpio_write (MCP3208_CLK, 0);
                mraa_gpio_write (MCP3208_CLK, 1);
        }

        mraa_gpio_write (MCP3208_CLK, 0);
        mraa_gpio_write (MCP3208_CLK, 1);

        mraa_gpio_write (MCP3208_CLK, 0);
        mraa_gpio_write (MCP3208_CLK, 1);

        val = 0;
        for (i = 0; i < 12; i ++)
        {
                mraa_gpio_write (MCP3208_CLK, 0);
                mraa_gpio_write (MCP3208_CLK, 1);

                val = (val << 1) | (mraa_gpio_read (MCP3208_DOUT));
        }

        mraa_gpio_write (MCP3208_CS, 1);
        mraa_gpio_write (MCP3208_DIN, 0);
        mraa_gpio_write (MCP3208_CLK, 0);

        return val;
}


void delay_time (unsigned int time_end)
{
        unsigned int index;
        for (index = 0; index < time_end; index++);
}

void home_LCD (void)
{
        uint8_t buf[] = {0x00,0x02};
        mraa_i2c_write(i2cp, buf, 2);  //Set to Home
}

void home2_LCD (void)
{
        uint8_t buf[] = {0x00,0x02,0xC0};
        mraa_i2c_write(i2cp, buf, 3);  //Set to Start of 2nd line 0X40 
}


void LCD_Print (char* str)
{
        uint8_t buf[80];
        int i = 0, strl;
        home_LCD ();
        buf[i] = 0x40;  //register for display
        i++;
        strl = strlen(str);
        for (int j = 0; j < strl; j++)
        {
                buf[i] = str[j];
                i++;
        }
        mraa_i2c_write(i2cp, buf, i);
}

void LCD_Print2 (char* str)
{
        uint8_t buf[80];
        int i = 0, strl;
        home2_LCD ();
        buf[i] = 0x40;  //register for display
        strl = strlen(str);
        for (int j = 0; j < strl; j++)
        {
                i++;
                buf[i] = str[j];
        }
        mraa_i2c_write(i2cp, buf, i);
}

void LCD_init (void)
{
   uint8_t init1[] = {0x00,0x38};
   uint8_t init2[] = {0x00, 0x39, 0x14,0x74,0x54,0x6f,0x0c,0x01};
        // 2 lines 8 bit 3.3V Version
    mraa_i2c_write(i2cp, init1, 2);
    mraa_i2c_write(i2cp, init2,8);  //Function Set
}

void clear_LCD (void)
{
        uint8_t buf[] = {0x00,0x01};
        mraa_i2c_write(i2cp, buf, 2);  //Clear Display
}

#define SENSOR_BUF 120
int main(int argc, char** argv)
{
        char buffer[40]; // One line of display
        int adc_chan = 6;
        mraa_init();
        int rcount=0;
        int res;
        float sum=0;
        float volts;
        float tempc,tempf;
        i2cp = mraa_i2c_init_raw (I2CP_BUS);
        mraa_i2c_frequency (i2cp, MRAA_I2C_STD);
        mraa_i2c_address(i2cp, LCD_ADDR);
        MCP3208_DIN = mraa_gpio_init (SPI_MOSI_PIN);
        MCP3208_DOUT = mraa_gpio_init (SPI_MISO_PIN);
        MCP3208_CLK = mraa_gpio_init (SPI_CLK_PIN);
        MCP3208_CS = mraa_gpio_init (SPI_CS0_PIN);
        MCP3208_CS1 = mraa_gpio_init (SPI_CS1_PIN);

        mraa_gpio_dir(MCP3208_DIN, MRAA_GPIO_OUT);
        mraa_gpio_dir(MCP3208_DOUT, MRAA_GPIO_IN);
        mraa_gpio_dir(MCP3208_CLK, MRAA_GPIO_OUT);
        mraa_gpio_dir(MCP3208_CS, MRAA_GPIO_OUT);
        mraa_gpio_dir(MCP3208_CS1, MRAA_GPIO_OUT);
        mraa_gpio_write (MCP3208_CS1, 1);
        LCD_init();
        clear_LCD();
        LCD_Print ("ADC Code Test\n");

        res = GetMCP3208(adc_chan);
        usleep(500000);
        while (1)
        {
                usleep(200000);
                res = GetMCP3208(adc_chan);
                volts = (float) res *3.3 / 4096;   // 3.3V = full scale 4096 = numper of steps
                tempc = (volts - .5) / .01;        // Temperature = volts - 500mv 10mV / step
                tempf = tempc * 9 / 5 + 32;
                printf("Volts = %4.2f Temp C = %4.1f  Temp F = %4.1f\n",volts,tempc,tempf);
                sprintf(buffer, "TTemp=%4.1f%cF\n", tempf, 0xDF);
                sum += tempf;
                if(rcount>=10)   // Display data value every 1s
                {
                        clear_LCD();
                        LCD_Print(buffer);
                        sprintf(buffer, "Ave Temp=%4.1f%cF\n", sum/rcount,0xDF);
                        LCD_Print2(buffer);
                        rcount=0;
                        sum = 0;
                }

                rcount++;
        }
}
