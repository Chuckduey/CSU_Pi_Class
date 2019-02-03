#include <Python.h>
#include "mraa_raspberry_pi_pinmap.h"


mraa_gpio_context MCP3208_DIN;
mraa_gpio_context MCP3208_DOUT;
mraa_gpio_context MCP3208_CLK;
mraa_gpio_context MCP3208_CS;
/*
 *  * Function to be called from Python
 *   */
static PyObject* py_myFunction(PyObject* self, PyObject* args)
{
	  char *s = "Hello from C!";
	    return Py_BuildValue("s", s);
}

/*
 *  * Another function to be called from Python
 *   */
static PyObject* py_adcRead(PyObject* self, PyObject* args)
{
	int ch, i,val;
	PyArg_ParseTuple(args, "i", &ch);
	mraa_gpio_write (MCP3208_DIN, 0);
	mraa_gpio_write (MCP3208_CLK, 0);
	mraa_gpio_write (MCP3208_CS, 0);

	ch = ch | 0x18;
	for (i = 0; i < 5; i ++)
	{
		if (ch & 0x10)
		{
			mraa_gpio_write (MCP3208_DIN, 1);
		}
		else
		{
			mraa_gpio_write (MCP3208_DIN, 0);
		}
		ch <<= 1;

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
		
		val = (val << 1) | ((int) mraa_gpio_read (MCP3208_DOUT));	
	}
	
	mraa_gpio_write (MCP3208_CS, 1);
	mraa_gpio_write (MCP3208_DIN, 0);
	mraa_gpio_write (MCP3208_CLK, 0);
	return Py_BuildValue("i", val);
}

/*
 *  * Bind Python function names to our C functions
 *   */
static PyMethodDef adcPythonC_methods[] = {
	  {"myFunction", py_myFunction, METH_VARARGS},
	    {"adcRead", py_adcRead, METH_VARARGS},
	      {NULL, NULL}
};

/*
 *  * Python calls this to let us initialize our module
 *   */
void initadcPythonC()
{
	(void) Py_InitModule("adcPythonC", adcPythonC_methods);
	MCP3208_DIN = mraa_gpio_init (SPI_MOSI_PIN);
	MCP3208_DOUT = mraa_gpio_init (SPI_MISO_PIN);
	MCP3208_CLK = mraa_gpio_init (SPI_CLK_PIN);
	MCP3208_CS = mraa_gpio_init (SPI_CS0_PIN);
        sleep(1); // Need a delay before setting the direction.	
	mraa_gpio_dir(MCP3208_DIN, MRAA_GPIO_OUT_HIGH);
	mraa_gpio_dir(MCP3208_DOUT, MRAA_GPIO_IN);
	mraa_gpio_dir(MCP3208_CLK, MRAA_GPIO_OUT);
	mraa_gpio_dir(MCP3208_CS, MRAA_GPIO_OUT);

}
