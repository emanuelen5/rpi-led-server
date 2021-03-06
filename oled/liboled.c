#define PY_SSIZE_T_CLEAN
#include <Python.h>
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>
#include "ssd1331.h"

uint16_t buffer[OLED_WIDTH * OLED_HEIGHT];
#define PACK_RGB(R,G,B)  ((((uint16_t) R >> 3) << 11) | (((uint16_t) G >> 2) << 5) | ((uint16_t) B >> 3))

static PyObject *take_array(PyObject *self, PyObject *args) {
    PyObject *arg1 = NULL;
    PyArrayObject *arr = NULL;

    if(!PyArg_ParseTuple(args, "O", &arg1)) {
        return NULL;
    }

    arr = (PyArrayObject*) PyArray_FROM_OTF(arg1, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
    if (arr == NULL) return NULL;

    int dims = PyArray_NDIM(arr);
    npy_intp *shape = PyArray_SHAPE(arr);
    for (int i=0; i<dims; i++) {
    	printf("Array->shape[%d]=%ld\n", i, shape[i]);
    }

    return (PyObject*) arr;
}

PyArrayObject *frame_buffer = NULL;
static PyObject *init(PyObject *self, PyObject *args) {
	if (frame_buffer != NULL) {
		PyErr_SetString(PyExc_RuntimeError, "The module has already been initialized");
		return NULL;
	}

	PyObject *arg1 = NULL;
	if (!PyArg_ParseTuple(args, "O", &arg1))
		return NULL;

	frame_buffer = (PyArrayObject*) PyArray_FROM_OTF(arg1, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
	if (frame_buffer == NULL) {
		PyErr_SetString(PyExc_RuntimeError, "Could not parse as array");
		return NULL;
	}

	int dims = PyArray_NDIM(frame_buffer);
	npy_intp *shape = PyArray_SHAPE(frame_buffer);

	if (dims != 3) {
		PyErr_SetString(PyExc_ValueError, "Wrong array dimensions. Expected a 3-dimensinoal array.");
		return NULL;
	}

	if (shape[0] != OLED_HEIGHT || shape[1] != OLED_WIDTH || shape[2] != 3) {
		PyErr_SetString(PyExc_ValueError, "Wrong shape of array.");
		return NULL;
	}

	Py_INCREF(frame_buffer);
	SSD1331_begin();

	Py_RETURN_NONE;
}

static PyObject *display(PyObject *self, PyObject *args) {
	if (frame_buffer == NULL) {
		PyErr_SetString(PyExc_RuntimeError, "The module has not been initialized");
		return NULL;
	}

	uint8_t r, g, b;
	for (int y=0; y < OLED_HEIGHT; y++) {
		for (int x=0; x < OLED_WIDTH; x++) {
			r = 256.0 * *(npy_double*)PyArray_GETPTR3(frame_buffer, y, x, 0);
			g = 256.0 * *(npy_double*)PyArray_GETPTR3(frame_buffer, y, x, 1);
			b = 256.0 * *(npy_double*)PyArray_GETPTR3(frame_buffer, y, x, 2);
			buffer[y * OLED_WIDTH + x] = PACK_RGB(r, g, b);
		}
	}
	SSD1331_display(buffer);

	Py_RETURN_NONE;
}

static PyObject *deinit(PyObject *self, PyObject *args) {
	if (frame_buffer == NULL) {
		PyErr_SetString(PyExc_RuntimeError, "The module has not been initialized");
		return NULL;
	}

	SSD1331_end();
	Py_XDECREF(frame_buffer);
	frame_buffer = NULL;

	Py_RETURN_NONE;
}

static PyObject *get_array(PyObject *self, PyObject *args) {
	if (frame_buffer == NULL) {
		PyErr_SetString(PyExc_RuntimeError, "The module has not been initialized");
		return NULL;
	}

	return (PyObject*) frame_buffer;
}

static PyMethodDef methods[] = {
    {"take_array", take_array, METH_VARARGS, "Test method for learning Numpy C API"},
    {"init", init, METH_VARARGS, "Initializes memory and communication with the hardware"},
    {"deinit", deinit, METH_NOARGS, "Releases the hardware and memory"},
    {"get_array", get_array, METH_NOARGS, "Gets the Numpy C array that is used for the display"},
    {"display", display, METH_NOARGS, "Refresh the display with the current image data"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef liboled_module = {
    PyModuleDef_HEAD_INIT,
    "liboled",
    "Python interface for the OLED C library function",
    -1,
    methods
};

PyMODINIT_FUNC PyInit_liboled(void) {
    import_array();
    PyObject *module = PyModule_Create(&liboled_module);
    PyModule_AddIntMacro(module, OLED_HEIGHT);
    PyModule_AddIntMacro(module, OLED_WIDTH);
    return module;
}
