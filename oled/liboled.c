#define PY_SSIZE_T_CLEAN
#include <Python.h>
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>
#include <stdbool.h>
#include <arpa/inet.h>
#include "ssd1331.h"

bool is_initialized = false;
uint16_t display_buffer[OLED_WIDTH * OLED_HEIGHT];
#define PACK_RGB(R,G,B)  ((((uint16_t) R >> 3) << 11) | (((uint16_t) G >> 2) << 5) | ((uint16_t) B >> 3))
#define UNPACK_R(rgb)  ((uint8_t)((rgb >> 8) & 0xF8))
#define UNPACK_G(rgb)  ((uint8_t)((rgb >> 3) & 0xFC))
#define UNPACK_B(rgb)  ((uint8_t)((rgb << 3) & 0xF8))

static bool check_initialization(void) {
	if (!is_initialized)
		PyErr_SetString(PyExc_RuntimeError, "The module has not been initialized");
	return is_initialized;
}

static PyObject *init(PyObject *self, PyObject *args) {
	if (is_initialized) {
		PyErr_SetString(PyExc_RuntimeError, "The module has already been initialized");
		return NULL;
	}
	is_initialized = true;
	SSD1331_begin();

	Py_RETURN_NONE;
}

static PyObject *display(PyObject *self, PyObject *args) {
	if (!check_initialization())
		return NULL;

	PyArrayObject *frame_buffer;

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
		Py_DECREF(frame_buffer);
		return NULL;
	}

	if (shape[0] != OLED_HEIGHT || shape[1] != OLED_WIDTH || shape[2] != 3) {
		PyErr_SetString(PyExc_ValueError, "Wrong shape of array.");
		Py_DECREF(frame_buffer);
		return NULL;
	}

	uint8_t r, g, b;
	for (int y=0; y < OLED_HEIGHT; y++) {
		for (int x=0; x < OLED_WIDTH; x++) {
			r = 255.0 * *(npy_double*)PyArray_GETPTR3(frame_buffer, y, x, 0) + 0.5;
			g = 255.0 * *(npy_double*)PyArray_GETPTR3(frame_buffer, y, x, 1) + 0.5;
			b = 255.0 * *(npy_double*)PyArray_GETPTR3(frame_buffer, y, x, 2) + 0.5;
			display_buffer[y * OLED_WIDTH + x] = htons(PACK_RGB(r, b, g));
		}
	}

	SSD1331_display(display_buffer);

	Py_DECREF(frame_buffer);
	Py_RETURN_NONE;
}

static PyObject *deinit(PyObject *self, PyObject *args) {
	if (is_initialized)
		SSD1331_end();

	is_initialized = false;
	Py_RETURN_NONE;
}

static PyObject *get_buffer(PyObject *self, PyObject *args) {
	if (!check_initialization())
		return NULL;

	PyArrayObject *display_buffer_npy;
	PyArray_Descr* descr = PyArray_DescrFromType(NPY_UINT8);
	const npy_intp dims[] = {OLED_HEIGHT, OLED_WIDTH, 3};
	display_buffer_npy = (PyArrayObject*) PyArray_Zeros(3, dims, descr, 0);

	uint16_t rgb;
	for (int y=0; y < OLED_HEIGHT; y++) {
		for (int x=0; x < OLED_WIDTH; x++) {
			rgb = ntohs(display_buffer[y * OLED_WIDTH + x]);
			*(npy_uint8*)PyArray_GETPTR3(display_buffer_npy, y, x, 0) = UNPACK_R(rgb);
			*(npy_uint8*)PyArray_GETPTR3(display_buffer_npy, y, x, 1) = UNPACK_G(rgb);
			*(npy_uint8*)PyArray_GETPTR3(display_buffer_npy, y, x, 2) = UNPACK_B(rgb);
		}
	}

	return (PyObject*) display_buffer_npy;
}

static PyMethodDef methods[] = {
    {"init", init, METH_NOARGS, "Initializes memory and communication with the hardware"},
    {"deinit", deinit, METH_NOARGS, "Releases the hardware and memory"},
    {"display", display, METH_VARARGS, "Refresh the display with the current image data"},
    {"get_buffer", get_buffer, METH_NOARGS, "Get the currently displayed buffer"},
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
    is_initialized = false;
    return module;
}
