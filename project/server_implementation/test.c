#include <stdint.h>
#include "accelerated.h"
#include <math.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#define N_TEST 3
#define MAX_KEY_SIZE 32
#define MIN_KEY_SIZE 16
#define MAX_FILE_SIZE 32
#define MIN_FILE_SIZE 16
#define MAX_NB_ROUNDS 1
#define MIN_NB_ROUNDS 1
#define rand_ab(a, b) (int)((a) + ((float)rand()/(float)RAND_MAX) * ((b) - (a)))


char *randomizator = "itfgiohtgiozerhjiopgzhrjioptgjheziopzioprgoipzerjutgiopuj"
                     "ruzropiziozrrjgpiozrhjego";
const uint64_t mutliplication_seed = 0x5bd8e995;
const uint8_t padding_batch = 4;
unsigned int gen_seed = 0xC0FFEE;

void printSquareMatrix(int *matrix, int size) {

    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            printf("%d\t", matrix[i * size + j]);
        }
        printf("\n");
    }
}
void printHexComparison(char *array1, char *array2, int N) {

    for (int i = 0; i < N; ++i) {
        printf("cpu_res[%d]=%d (0x%x) vs cuda_res[%d]=%d (0x%x)\n",
               i, array1[i], array1[i], i, array2[i], array2[i]);
    }
}


struct parsed_request {
    // The size of the key
    uint32_t key_size;
    // The size of the file
    uint32_t file_size;
    // The number of rounds to apply
    uint16_t nb_rounds;
    // A pointer to the start of the key
    int *key;
    // A pointer to the start of a file
    int *file;
};

inline int same_files(char * file1, char *file2, size_t sz) {
    return memcmp(file1, file2, sz) == 0;
}

inline void free_parsed_request(struct parsed_request * req) {
    free(req->key);
    free(req->file);
    free(req);
}

struct parsed_request * gen_random_request() {
    uint32_t key_size = rand_ab(MIN_KEY_SIZE, MAX_KEY_SIZE);
    uint32_t file_size = rand_ab(MIN_FILE_SIZE, MAX_FILE_SIZE);
    uint16_t nb_rounds = rand_ab(MIN_NB_ROUNDS, MAX_NB_ROUNDS);

    int * key = (int *) malloc(sizeof(int) * key_size);
    if (!key) {
        fprintf(stderr, "Could not allocate key!\n");
        return NULL;
    }
    int * file = (int *) malloc(sizeof(int) * file_size);
    if (!file) {
        fprintf(stderr, "Could not allocate file!\n");
        free(key);
        return NULL;
    }
    struct parsed_request * ret = malloc(sizeof(struct parsed_request));
    if (!ret) {
        fprintf(stderr, "Could not allocate struct parsed_request!\n");
        free(key);
        free(file);
        return NULL;
    }

    for (int i = 0; i < key_size; i++) {
        key[i] = rand_ab(0, INT8_MAX);
    }
    for (int i = 0; i < file_size; i++) {
        file[i] = rand_ab(0, INT8_MAX);
    }

    ret->key_size = key_size;
    ret->file_size = file_size;
    ret->nb_rounds = nb_rounds;
    ret->file = file;
    ret->key = key;
    return ret;
}



void multiply_matrix(int *matrix1, int *matrix2, int *result, uint32_t K) {
    for (uint32_t i = 0; i < K; i++) {
        for (uint32_t j = 0; j < K; j++) {
            result[i * K + j] = 0;

            for (uint32_t k = 0; k < K; k++) {
                result[i * K + j] += matrix1[i * K + k] * matrix2[k * K + j];
            }
        }
    }
}

int * get_multiplication_matrix(uint32_t K) {
    uint32_t pos = 0;
    int * multiplication_matrix = (int *) malloc(K * K * sizeof(int));
    for (size_t i = 0; i < K * K; i++) {
        multiplication_matrix[i] = *(int *)(randomizator + pos * sizeof(int));
        pos = (pos + 1) % ((strlen(randomizator) / sizeof(int)) - 1);
    }
    return multiplication_matrix;
}



inline uint32_t get_K(struct parsed_request * req) {return floor(sqrt((double)req->file_size / sizeof(int)));}

static char * mock_body_processing(struct parsed_request * parsed, bool use_cuda) {

    struct parsed_request req = *parsed;
    uint32_t K = get_K(parsed);

    int * product = (int *) malloc(K * K * sizeof(int));
    int * multiplication_matrix = get_multiplication_matrix(K);
    int * file_cpy = (int *) malloc(sizeof(int) * req.file_size);
    if (!file_cpy) {
        fprintf(stderr, "Could not allocate file copy !\n");
        free(multiplication_matrix);
        free(product);
        return NULL;
    }
    memcpy(file_cpy, req.file, req.file_size);

    int * key_cpy = (int *) malloc(sizeof(int) * req.key_size);
    if (!key_cpy) {
        fprintf(stderr, "Could not allocate key copy !\n");
        free(multiplication_matrix);
        free(product);
        free(file_cpy);
        return NULL;
    }
    memcpy(key_cpy, req.key, req.key_size);

    for (size_t i = 0; i < req.nb_rounds; i++) {

        if (use_cuda) {
            cu_matrix_mul(file_cpy, multiplication_matrix, product, K);
        } else {
            multiply_matrix(file_cpy, multiplication_matrix, product, K);
        }

    }
    free(multiplication_matrix);
    free(product);
    free(key_cpy);

    return (char *)file_cpy;
}

int main(int argc, const char* argv[]) {
    srand(gen_seed);
    for (int i = 0; i < N_TEST; i++) {
        fprintf(stdout, "Performing test #%d\n", i);
        struct parsed_request * generated = gen_random_request();
        uint32_t K = get_K(generated);
        char * res_cpu = mock_body_processing(generated, false);
        char * res_cuda = mock_body_processing(generated, true);

        if (!same_files(res_cpu, res_cuda, K)) {
            fprintf(stderr, "Files were different during testing !!! \n");
            fprintf(stdout, "result file is:\n");
            printHexComparison(res_cpu, res_cuda, K);
        } else {
            fprintf(stdout, "Passed test #%d \n", i);
        }

        free(res_cpu);
        free(res_cuda);
        free_parsed_request(generated);
    }


}