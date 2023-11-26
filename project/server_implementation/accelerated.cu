extern "C" {

#include <cuda_runtime.h>
#include <cuda_profiler_api.h>
#include <cuda.h>
#include <stdint.h>
#include <stdio.h>
#define CHECK_CUDA_INIT(err) if ((err)) {fprintf(stderr, "Could not initialize CUDA ! cudaError=%d\n", (err)); return err;}
#ifndef CUDA_BLOCK_SIZE
#define CUDA_BLOCK_SIZE 16
#endif
    __global__ void cudaKernel_matrixMul(int *A, int *B, int *C, int N) {
        //TODO perform matrix multiplication on the CUDA executor
        //This is a good validation step to ensure you are on the right track for the project
    }
    __global__ void cudaKernel_encrypt() {
        //TODO perform the GPU computation for the full encryption algorithm
        //You are free to change the parameters as you see fit. Or even split the work in multiple kernels.
    }
    void cu_matrix_mul(int *matrix1, int *matrix2, int *result, uint32_t K) {
        int *dev_A, *dev_B, *dev_res;
        cudaMalloc((void **)&dev_A, K * K * sizeof(int));
        cudaMalloc((void **)&dev_B, K * K * sizeof(int));
        cudaMalloc((void **)&dev_res, K * K * sizeof(int));

        // Copy matrices A and B from host to device
        cudaMemcpy(dev_A, matrix1, K * K * sizeof(int), cudaMemcpyHostToDevice);
        cudaMemcpy(dev_B, matrix2, K * K * sizeof(int), cudaMemcpyHostToDevice);

        // Define grid and block dimensions
        dim3 blockSize(CUDA_BLOCK_SIZE, CUDA_BLOCK_SIZE); // Define the block size (e.g., 16x16 threads per block)
        dim3 gridSize((K + blockSize.x - 1) / blockSize.x, (K + blockSize.y - 1) / blockSize.y);

        // Launch the kernel
        cudaKernel_matrixMul<<<gridSize, blockSize>>>(dev_A, dev_B, dev_res, K);

        // Copy the result matrix C from device to host
        cudaMemcpy(result, dev_res, K * K * sizeof(int), cudaMemcpyDeviceToHost);

        // Free device memory
        cudaFree(dev_A);
        cudaFree(dev_B);
        cudaFree(dev_res);
    }

    void cu_encrypt(int n_rounds, int key_size, int * key, uint32_t K, int * matrix, int * mult_mat) {
        //TODO perform CUDA allocations, kernel invocation, etc for the 
        //full encryption algorithm    
    }

    int cu_init() {
        cudaError_t err = cudaInitDevice(0, 0, 0);
        CHECK_CUDA_INIT(err)
        err = cudaSetDevice(0);
        CHECK_CUDA_INIT(err)
        err = cudaFree(0);
        CHECK_CUDA_INIT(err)
        return err;
    }
    
    int cu_exit() {
        return 0;
    }

}
