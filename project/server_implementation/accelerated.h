#include <cstdint>
#include <stdint.h>
/*
* Multiplies matrix1 with matrix2 of size KxK, stores the result in result
*
* Accelerating this part is a good starting point, given the fact 
*/
void cu_matrix_mul(int *matrix1, int *matrix2, int *result, uint32_t K);
/*
* Performs the encryption algorithm with the following parameters
*   n_rounds, the number of rounds 
*   key_size, the size of the key
*   key, pointing to an int array containing the key
*   K, the square size of the matrix representing the file
*   matrix, a pointer to the int array representing the matrix representing the file 
*   mult_mat, a pointer to the int array representing the multiplication matrix 
*/
void cu_encrypt(int n_rounds, int key_size, int * key, uint32_t K, int * matrix, int * mult_mat);

/*
* Initializes CUDA, returns the initialization's success code.
* This is separated from the rest of the server's code in order to still be able to compile the server directly with gcc separately
*/
int cu_init();
/*
* Resets the cuda device before exiting.
* This is separated from the rest of the server's code in order to still be able to compile the server directly with gcc separately
*/
int cu_exit();