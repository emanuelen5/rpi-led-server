#define PY_SSIZE_T_CLEAN
#include <Python.h>
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>
#include "ssd1331.h"

static PyObject *take_array(PyObject *self, PyObject *args) {
    PyObject *arg1 = NULL;
    PyArrayObject *arr = NULL;

    /* Parse arguments */
    printf("Parsing tuple\n");
    if(!PyArg_ParseTuple(args, "O", &arg1)) {
        return NULL;
    }

    printf("Getting array\n");
    arr = (PyArrayObject*) PyArray_FROM_OTF(arg1, NPY_DOUBLE, NPY_ARRAY_IN_ARRAY);
    if (arr == NULL) return NULL;

    int N = (int)PyArray_DIM(arr, 0);
    int dims = PyArray_NDIM(arr);
    npy_intp *shape = PyArray_SHAPE(arr);
    for (int i=0; i<dims; i++) {
    	printf("Array->shape[%d]=%d\n", i, shape[i]);
    }

    printf("Ensuring array\n");
    // arr = PyArray_FromAny(obj, );

    return arr;
}

static PyMethodDef methods[] = {
    {"take_array", take_array, METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "liboled",
    "Python interface for the OLED C library function",
    -1,
    methods
};

PyMODINIT_FUNC PyInit_liboled(void) {
    import_array();
    return PyModule_Create(&module);
}
