#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <numpy/arrayobject.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Struktura pro výsledky detekce okrajů
typedef struct {
    int left;
    int top;
    int right;
    int bottom;
    double area_reduction;
} BorderResult;

// Funkce pro kontrolu, zda je pixel bílý nebo průhledný
static int is_white_or_transparent_rgba(unsigned char r, unsigned char g, unsigned char b, unsigned char a, int tolerance) {
    // Kontrola průhlednosti
    if (a < tolerance) {
        return 1;
    }
    // Kontrola bílé barvy
    return (r >= 255 - tolerance && g >= 255 - tolerance && b >= 255 - tolerance);
}

static int is_white_or_transparent_rgb(unsigned char r, unsigned char g, unsigned char b, int tolerance) {
    return (r >= 255 - tolerance && g >= 255 - tolerance && b >= 255 - tolerance);
}

// Funkce pro výpočet průměrné světlosti řádku (RGBA)
static double calculate_row_brightness_rgba(unsigned char* data, int width, int y, int channels) {
    double sum = 0.0;
    int count = 0;
    
    for (int x = 0; x < width; x++) {
        int idx = (y * width + x) * channels;
        unsigned char r = data[idx];
        unsigned char g = data[idx + 1];
        unsigned char b = data[idx + 2];
        unsigned char a = data[idx + 3];
        
        // Pokud je pixel průhledný, přeskočíme ho
        if (a < 10) {
            continue;
        }
        
        // Průměrná hodnota RGB
        sum += (r + g + b) / 3.0;
        count++;
    }
    
    return count > 0 ? sum / count : 255.0;
}

// Funkce pro výpočet průměrné světlosti sloupce (RGBA)
static double calculate_col_brightness_rgba(unsigned char* data, int width, int height, int x, int channels) {
    double sum = 0.0;
    int count = 0;
    
    for (int y = 0; y < height; y++) {
        int idx = (y * width + x) * channels;
        unsigned char r = data[idx];
        unsigned char g = data[idx + 1];
        unsigned char b = data[idx + 2];
        unsigned char a = data[idx + 3];
        
        // Pokud je pixel průhledný, přeskočíme ho
        if (a < 10) {
            continue;
        }
        
        // Průměrná hodnota RGB
        sum += (r + g + b) / 3.0;
        count++;
    }
    
    return count > 0 ? sum / count : 255.0;
}

// Funkce pro výpočet průměrné světlosti řádku (RGB)
static double calculate_row_brightness_rgb(unsigned char* data, int width, int y, int channels) {
    double sum = 0.0;
    
    for (int x = 0; x < width; x++) {
        int idx = (y * width + x) * channels;
        unsigned char r = data[idx];
        unsigned char g = data[idx + 1];
        unsigned char b = data[idx + 2];
        
        // Průměrná hodnota RGB
        sum += (r + g + b) / 3.0;
    }
    
    return sum / width;
}

// Funkce pro výpočet průměrné světlosti sloupce (RGB)
static double calculate_col_brightness_rgb(unsigned char* data, int width, int height, int x, int channels) {
    double sum = 0.0;
    
    for (int y = 0; y < height; y++) {
        int idx = (y * width + x) * channels;
        unsigned char r = data[idx];
        unsigned char g = data[idx + 1];
        unsigned char b = data[idx + 2];
        
        // Průměrná hodnota RGB
        sum += (r + g + b) / 3.0;
    }
    
    return sum / height;
}

// Hlavní funkce pro detekci bílých okrajů
static BorderResult detect_white_borders_c(unsigned char* data, int width, int height, int channels, int tolerance, int extra_crop) {
    BorderResult result = {0, 0, width, height, 0.0};
    
    int max_scan = 100; // Maximální počet pixelů ke skenování z každé strany
    
    if (channels == 4) { // RGBA
        // Detekce horního okraje
        for (int y = 0; y < min(max_scan, height); y++) {
            double brightness = calculate_row_brightness_rgba(data, width, y, channels);
            if (brightness < 245) {
                result.top = y;
                break;
            }
        }
        
        // Detekce spodního okraje
        for (int y = height - 1; y >= max(height - max_scan, 0); y--) {
            double brightness = calculate_row_brightness_rgba(data, width, y, channels);
            if (brightness < 245) {
                result.bottom = y + 1;
                break;
            }
        }
        
        // Detekce levého okraje
        for (int x = 0; x < min(max_scan, width); x++) {
            double brightness = calculate_col_brightness_rgba(data, width, height, x, channels);
            if (brightness < 245) {
                result.left = x;
                break;
            }
        }
        
        // Detekce pravého okraje
        for (int x = width - 1; x >= max(width - max_scan, 0); x--) {
            double brightness = calculate_col_brightness_rgba(data, width, height, x, channels);
            if (brightness < 245) {
                result.right = x + 1;
                break;
            }
        }
    } else { // RGB
        // Detekce horního okraje
        for (int y = 0; y < min(max_scan, height); y++) {
            double brightness = calculate_row_brightness_rgb(data, width, y, channels);
            if (brightness < 245) {
                result.top = y;
                break;
            }
        }
        
        // Detekce spodního okraje
        for (int y = height - 1; y >= max(height - max_scan, 0); y--) {
            double brightness = calculate_row_brightness_rgb(data, width, y, channels);
            if (brightness < 245) {
                result.bottom = y + 1;
                break;
            }
        }
        
        // Detekce levého okraje
        for (int x = 0; x < min(max_scan, width); x++) {
            double brightness = calculate_col_brightness_rgb(data, width, height, x, channels);
            if (brightness < 245) {
                result.left = x;
                break;
            }
        }
        
        // Detekce pravého okraje
        for (int x = width - 1; x >= max(width - max_scan, 0); x--) {
            double brightness = calculate_col_brightness_rgb(data, width, height, x, channels);
            if (brightness < 245) {
                result.right = x + 1;
                break;
            }
        }
    }
    
    // Výpočet snížení plochy
    int original_area = width * height;
    int cropped_area = (result.right - result.left) * (result.bottom - result.top);
    result.area_reduction = ((double)(original_area - cropped_area) / original_area) * 100.0;
    
    // Aplikace extra ořezu
    result.left = max(0, result.left + extra_crop);
    result.top = max(0, result.top + extra_crop);
    result.right = min(width, result.right - extra_crop);
    result.bottom = min(height, result.bottom - extra_crop);
    
    // Zajištění minimálních rozměrů
    if (result.right <= result.left) result.right = result.left + 1;
    if (result.bottom <= result.top) result.bottom = result.top + 1;
    
    return result;
}

// Python wrapper funkce
static PyObject* detect_white_borders_wrapper(PyObject* self, PyObject* args) {
    PyArrayObject* array;
    int tolerance = 10;
    int extra_crop = 2;
    
    if (!PyArg_ParseTuple(args, "O!|ii", &PyArray_Type, &array, &tolerance, &extra_crop)) {
        return NULL;
    }
    
    // Kontrola dimenzí
    if (PyArray_NDIM(array) != 3) {
        PyErr_SetString(PyExc_ValueError, "Očekáván 3D numpy array (height, width, channels)");
        return NULL;
    }
    
    npy_intp* dims = PyArray_DIMS(array);
    int height = dims[0];
    int width = dims[1];
    int channels = dims[2];
    
    if (channels != 3 && channels != 4) {
        PyErr_SetString(PyExc_ValueError, "Očekáván RGB (3) nebo RGBA (4) formát");
        return NULL;
    }
    
    // Získání dat
    unsigned char* data = (unsigned char*)PyArray_DATA(array);
    
    // Detekce okrajů
    BorderResult result = detect_white_borders_c(data, width, height, channels, tolerance, extra_crop);
    
    // Vrácení výsledku jako tuple
    return Py_BuildValue("(iiii)d", 
                        result.left, result.top, result.right, result.bottom, 
                        result.area_reduction);
}

// Definice metod modulu
static PyMethodDef EdgeDetectionMethods[] = {
    {"detect_white_borders", detect_white_borders_wrapper, METH_VARARGS, 
     "Detekuje bílé okraje v obrázku a vrátí souřadnice ořezu"},
    {NULL, NULL, 0, NULL}
};

// Definice modulu
static struct PyModuleDef edge_detection_module = {
    PyModuleDef_HEAD_INIT,
    "edge_detection",
    "Rychlá detekce okrajů v C",
    -1,
    EdgeDetectionMethods
};

// Inicializační funkce modulu
PyMODINIT_FUNC PyInit_edge_detection(void) {
    import_array(); // Inicializace numpy
    return PyModule_Create(&edge_detection_module);
} 