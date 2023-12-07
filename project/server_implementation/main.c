#include <math.h>
#include <ngx_link_func_module.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <immintrin.h>

int is_service_on = 0;
char *randomizator = "itfgiohtgiozerhjiopgzhrjioptgjheziopzioprgoipzerjutgiopuj"
                     "ruzropiziozrrjgpiozrhjego";
const uint64_t mutliplication_seed = 0x5bd8e995;
const uint8_t padding_batch = 4;

/**
 * @brief Returns the constant multiplication_matrix.
 *
 * @param ctx The context of the request, only used for logging and memory
 * allocation.
 * @param K dimension of the matrix
 *
 * @return a K*K matrix
 *
 * @note You should use this function only once, and store its result.
 */
int *get_multiplication_matrix(ngx_link_func_ctx_t *ctx, uint32_t K)
{
  uint32_t pos = 0;
  int *multiplication_matrix = ngx_link_func_palloc(ctx, K * K * sizeof(int));
  for (size_t i = 0; i < K * K; i++)
  {
    multiplication_matrix[i] = *(int *)(randomizator + pos * sizeof(int));
    pos = (pos + 1) % ((strlen(randomizator) / sizeof(int)) - 1);
  }
  return multiplication_matrix;
}

struct parsed_request
{
  // The size of the key
  uint32_t key_size;
  // The size of the file
  uint32_t file_size;
  // The number of rounds to apply
  uint16_t nb_rounds;
  // A pointer to the start of the key
  int *key;
  // A pointer to tjhe start of a file
  int *file;
};

/**
 * @brief Parse the a raw request into a nice struct
 *
 * @param raw_request : A big string containing the request as it is received by the server
 * @param raw_request_len : The size of the raw request
 * @param request : A struct that will contain the parsed request at the end of the function
 *
 * @note The variable `request` should be modified to store the parsed representation of the request
 */
void parse_request(char *raw_request, uint32_t raw_request_len, struct parsed_request *request)
{
  const char *comma = strchr(raw_request, ',');

  if (comma == NULL)
  {
    return;
  }

  request->key_size = atoi(raw_request);
  const char *key_start = comma + 1;
  comma = strchr(key_start, ',');

  if (comma == NULL)
  {
    return;
  }

  request->file_size = atoi(key_start);
  comma++;
  request->nb_rounds = atoi(comma);
  const char *key_end = strchr(comma, ',');

  if (key_end == NULL)
  {
    return;
  }
  key_end++;

  request->key = (int *)key_end;
  const char *file_start = key_end + request->key_size;
  request->file = (int *)file_start;
}

void multiply_matrix_optimized(int *matrix1, int *matrix2, int *result, uint32_t K)
{
  memset(result, 0, K * K * sizeof(int));

  // Boucle combinée qui utilise le 'loop unrolling' et l'optimisation 'cache-aware'
  for (uint32_t i = 0; i < K; i++)
  {
    uint32_t iK = i * K;
    for (uint32_t j = 0; j < K; j++)
    {
      int r = matrix1[iK + j];
      uint32_t jK = j * K;

      uint32_t k;
      for (k = 0; k + 7 < K; k += 8)
      {
        result[iK + k] += r * matrix2[j * K + k];
        result[iK + k + 1] += r * matrix2[jK + k + 1];
        result[iK + k + 2] += r * matrix2[jK + k + 2];
        result[iK + k + 3] += r * matrix2[jK + k + 3];
        result[iK + k + 4] += r * matrix2[jK + k + 4];
        result[iK + k + 5] += r * matrix2[jK + k + 5];
        result[iK + k + 6] += r * matrix2[jK + k + 6];
        result[iK + k + 7] += r * matrix2[jK + k + 7];
      }
      // Traitement des éléments restants
      for (; k < K; k++)
      {
        result[iK + k] += r * matrix2[jK + k];
      }
    }
  }
}

#ifdef SIMD128
void multiply_matrix_optimized_128(int *matrix1, int *matrix2, int *result, uint32_t K)
{
  memset(result, 0, K * K * sizeof(int));

  for (uint32_t i = 0; i < K; i++)
  {
    uint32_t iK = i * K;
    for (uint32_t j = 0; j < K; j++)
    {
      int r = matrix1[iK + j];
      __m128i r_vec = _mm_set1_epi32(r);
      uint32_t jK = j * K;

      uint32_t k;
      for (k = 0; k + 3 < K; k += 4)
      {
        __m128i res_vec = _mm_loadu_si128((__m128i *)&result[iK + k]);
        __m128i m2_vec = _mm_loadu_si128((__m128i *)&matrix2[jK + k]);
        __m128i prod_vec = _mm_mullo_epi32(r_vec, m2_vec);
        res_vec = _mm_add_epi32(res_vec, prod_vec);
        _mm_storeu_si128((__m128i *)&result[iK + k], res_vec);
      }

      for (; k < K; k++)
      {
        result[iK + k] += r * matrix2[jK + k];
      }
    }
  }
}
#endif

#ifdef SIMD256
void multiply_matrix_optimized_256(int *matrix1, int *matrix2, int *result, uint32_t K)
{
  memset(result, 0, K * K * sizeof(int));

  for (uint32_t i = 0; i < K; i++)
  {
    uint32_t iK = i * K;
    for (uint32_t j = 0; j < K; j++)
    {
      int r = matrix1[iK + j];
      __m256i r_vec = _mm256_set1_epi32(r);
      uint32_t jK = j * K;

      uint32_t k;
      for (k = 0; k + 7 < K; k += 8)
      {
        __m256i res_vec = _mm256_loadu_si256((__m256i *)&result[iK + k]);
        __m256i m2_vec = _mm256_loadu_si256((__m256i *)&matrix2[jK + k]);
        __m256i prod_vec = _mm256_mullo_epi32(r_vec, m2_vec);
        res_vec = _mm256_add_epi32(res_vec, prod_vec);
        _mm256_storeu_si256((__m256i *)&result[iK + k], res_vec);
      }

      for (; k < K; k++)
      {
        result[iK + k] += r * matrix2[jK + k];
      }
    }
  }
}
#endif

#ifdef SIMD512
void multiply_matrix_optimized_512(int *matrix1, int *matrix2, int *result, uint32_t K)
{
  memset(result, 0, K * K * sizeof(int));

  for (uint32_t i = 0; i < K; i++)
  {
    uint32_t iK = i * K;
    for (uint32_t j = 0; j < K; j++)
    {
      int r = matrix1[iK + j];
      __m512i r_vec = _mm512_set1_epi32(r);
      uint32_t jK = j * K;

      uint32_t k;
      for (k = 0; k + 15 < K; k += 16)
      {
        __m512i res_vec = _mm512_loadu_si512((__m512i *)&result[iK + k]);
        __m512i m2_vec = _mm512_loadu_si512((__m512i *)&matrix2[jK + k]);
        __m512i prod_vec = _mm512_mullo_epi32(r_vec, m2_vec);
        res_vec = _mm512_add_epi32(res_vec, prod_vec);
        _mm512_storeu_si512((__m512i *)&result[iK + k], res_vec);
      }

      for (; k < K; k++)
      {
        result[iK + k] += r * matrix2[jK + k];
      }
    }
  }
}
#endif

#ifdef SIMD
void multiply_matrix_optimized_SIMD(int *matrix1, int *matrix2, int *result, uint32_t K)
{
  memset(result, 0, K * K * sizeof(int));

  for (uint32_t i = 0; i < K; i++)
  {
    uint32_t iK = i * K;
    for (uint32_t j = 0; j < K; j++)
    {
      int r = matrix1[iK + j];
      __m512i r_vec = _mm512_set1_epi32(r);
      uint32_t jK = j * K;

      uint32_t k;
      for (k = 0; k + 63 < K; k += 64)
      {

        __m512i res_vec1 = _mm512_loadu_si512((__m512i *)&result[iK + k]);
        __m512i m2_vec1 = _mm512_loadu_si512((__m512i *)&matrix2[jK + k]);
        __m512i prod_vec1 = _mm512_mullo_epi32(r_vec, m2_vec1);
        res_vec1 = _mm512_add_epi32(res_vec1, prod_vec1);
        _mm512_storeu_si512((__m512i *)&result[iK + k], res_vec1);

        __m512i res_vec2 = _mm512_loadu_si512((__m512i *)&result[iK + k + 16]);
        __m512i m2_vec2 = _mm512_loadu_si512((__m512i *)&matrix2[jK + k + 16]);
        __m512i prod_vec2 = _mm512_mullo_epi32(r_vec, m2_vec2);
        res_vec2 = _mm512_add_epi32(res_vec2, prod_vec2);
        _mm512_storeu_si512((__m512i *)&result[iK + k + 16], res_vec2);

        __m512i res_vec3 = _mm512_loadu_si512((__m512i *)&result[iK + k + 32]);
        __m512i m2_vec3 = _mm512_loadu_si512((__m512i *)&matrix2[jK + k + 32]);
        __m512i prod_vec3 = _mm512_mullo_epi32(r_vec, m2_vec3);
        res_vec3 = _mm512_add_epi32(res_vec3, prod_vec3);
        _mm512_storeu_si512((__m512i *)&result[iK + k + 32], res_vec3);

        __m512i res_vec4 = _mm512_loadu_si512((__m512i *)&result[iK + k + 48]);
        __m512i m2_vec4 = _mm512_loadu_si512((__m512i *)&matrix2[jK + k + 48]);
        __m512i prod_vec4 = _mm512_mullo_epi32(r_vec, m2_vec4);
        res_vec4 = _mm512_add_epi32(res_vec4, prod_vec4);
        _mm512_storeu_si512((__m512i *)&result[iK + k + 48], res_vec4);
      }

      if (K - k >= 4)
      {
        __m128i r_vec_128 = _mm_set1_epi32(r);
        for (; k + 3 < K; k += 4)
        {
          __m128i res_vec = _mm_loadu_si128((__m128i *)&result[iK + k]);
          __m128i m2_vec = _mm_loadu_si128((__m128i *)&matrix2[jK + k]);
          __m128i prod_vec = _mm_mullo_epi32(r_vec_128, m2_vec);
          res_vec = _mm_add_epi32(res_vec, prod_vec);
          _mm_storeu_si128((__m128i *)&result[iK + k], res_vec);
        }
      }

      for (; k < K; k++)
      {
        result[iK + k] += r * matrix2[jK + k];
      }
    }
  }
}
#endif

/**
 * @brief Computes the product of two matrixes
 *
 * @param matrix1 : a K x K matrix
 * @param matrix2 : a K x K matrix
 * @param result : a K x K matrix that should contain the product of matrix1
 * and matrix2 at the end of the function
 *
 * @note result should be modified to contain the encrypted version of the file
 */
void multiply_matrix(int *matrix1, int *matrix2, int *result, uint32_t K)
{
  for (uint32_t i = 0; i < K; i++)
  {
    for (uint32_t j = 0; j < K; j++)
    {
      result[i * K + j] = 0;
      for (uint32_t k = 0; k < K; k++)
      {
        result[i * K + j] += matrix1[i * K + k] * matrix2[k * K + j];
      }
    }
  }
}

void cipher_optimized(int *file, int *key, uint32_t key_size, uint32_t K)
{
  for (uint32_t i = 0; i < K; i++)
  {
    for (uint32_t j = 0; j < K; j++)
    {
      uint32_t index = i * K + j;
      int character = file[index];
      int key_sum = 0;
      uint32_t i_j = i * j;

      uint32_t k = 0;

      for (; k + 7 < key_size; k += 8)
      {
        key_sum += key[k] + key[k + 1] + key[k + 2] + key[k + 3] + key[k + 4] + key[k + 5] + key[k + 6] + key[k + 7];
        key[k] ^= i_j;
        key[k + 1] ^= i_j;
        key[k + 2] ^= i_j;
        key[k + 3] ^= i_j;
        key[k + 4] ^= i_j;
        key[k + 5] ^= i_j;
        key[k + 6] ^= i_j;
        key[k + 7] ^= i_j;
      }

      for (; k < key_size; k++)
      {
        key_sum += key[k];
        key[k] ^= i_j;
      }

      character ^= key_sum;
      file[index] = character;
    }
  }
}

#ifdef SIMD128
void cipher_optimized_128(int *file, int *key, uint32_t key_size, uint32_t K)
{
  for (uint32_t i = 0; i < K; i++)
  {
    for (uint32_t j = 0; j < K; j++)
    {
      uint32_t index = i * K + j;
      int character = file[index];
      int key_sum = 0;
      uint32_t i_j = i * j;

      __m128i sum_vector = _mm_setzero_si128();
      __m128i i_j_vector = _mm_set1_epi32(i_j);

      uint32_t k = 0;
      for (; k + 3 < key_size; k += 4)
      {
        __m128i key_vector = _mm_loadu_si128((__m128i *)(key + k));
        sum_vector = _mm_add_epi32(sum_vector, key_vector);
        key_vector = _mm_xor_si128(key_vector, i_j_vector);
        _mm_storeu_si128((__m128i *)(key + k), key_vector);
      }

      key_sum += _mm_extract_epi32(sum_vector, 0);
      key_sum += _mm_extract_epi32(sum_vector, 1);
      key_sum += _mm_extract_epi32(sum_vector, 2);
      key_sum += _mm_extract_epi32(sum_vector, 3);

      for (; k < key_size; k++)
      {
        key_sum += key[k];
        key[k] ^= i_j;
      }

      character ^= key_sum;
      file[index] = character;
    }
  }
}
#endif

#ifdef SIMD256
void cipher_optimized_256(int *file, int *key, uint32_t key_size, uint32_t K)
{
  for (uint32_t i = 0; i < K; i++)
  {
    for (uint32_t j = 0; j < K; j++)
    {
      uint32_t index = i * K + j;
      int character = file[index];
      int key_sum = 0;
      uint32_t i_j = i * j;

      __m256i sum_vector = _mm256_setzero_si256();
      __m256i i_j_vector = _mm256_set1_epi32(i_j);

      uint32_t k = 0;
      for (; k + 7 < key_size; k += 8)
      {
        __m256i key_vector = _mm256_loadu_si256((__m256i *)(key + k));
        sum_vector = _mm256_add_epi32(sum_vector, key_vector);
        key_vector = _mm256_xor_si256(key_vector, i_j_vector);
        _mm256_storeu_si256((__m256i *)(key + k), key_vector);
      }

      key_sum += _mm256_extract_epi32(sum_vector, 0);
      key_sum += _mm256_extract_epi32(sum_vector, 1);
      key_sum += _mm256_extract_epi32(sum_vector, 2);
      key_sum += _mm256_extract_epi32(sum_vector, 3);
      key_sum += _mm256_extract_epi32(sum_vector, 4);
      key_sum += _mm256_extract_epi32(sum_vector, 5);
      key_sum += _mm256_extract_epi32(sum_vector, 6);
      key_sum += _mm256_extract_epi32(sum_vector, 7);

      for (; k < key_size; k++)
      {
        key_sum += key[k];
        key[k] ^= i_j;
      }

      character ^= key_sum;
      file[index] = character;
    }
  }
}
#endif

#ifdef SIMD512
void cipher_optimized_512(int *file, int *key, uint32_t key_size, uint32_t K)
{
  for (uint32_t i = 0; i < K; i++)
  {
    for (uint32_t j = 0; j < K; j++)
    {
      uint32_t index = i * K + j;
      int character = file[index];
      int key_sum = 0;
      uint32_t i_j = i * j;

      __m512i sum_vector = _mm512_setzero_si512();
      __m512i i_j_vector = _mm512_set1_epi32(i_j);

      uint32_t k = 0;
      for (; k + 15 < key_size; k += 16)
      {
        __m512i key_vector = _mm512_loadu_si512((__m512i *)(key + k));
        sum_vector = _mm512_add_epi32(sum_vector, key_vector);
        key_vector = _mm512_xor_si512(key_vector, i_j_vector);
        _mm512_storeu_si512((__m512i *)(key + k), key_vector);
      }

      int buffer[16];
      _mm512_storeu_si512((__m512i *)buffer, sum_vector);
      for (int i = 0; i < 16; i++)
      {
        key_sum += buffer[i];
      }

      for (; k < key_size; k++)
      {
        key_sum += key[k];
        key[k] ^= i_j;
      }

      character ^= key_sum;
      file[index] = character;
    }
  }
}
#endif

#ifdef SIMD
void cipher_optimized_SIMD(int *file, int *key, uint32_t key_size, uint32_t K)
{
  for (uint32_t i = 0; i < K; i++)
  {
    for (uint32_t j = 0; j < K; j++)
    {
      uint32_t index = i * K + j;
      int character = file[index];
      int key_sum = 0;
      uint32_t i_j = i * j;

      __m512i i_j_vector_512 = _mm512_set1_epi32(i_j);
      __m512i sum_vector_512 = _mm512_setzero_si512();
      uint32_t k = 0;
      for (; k + 15 < key_size; k += 16)
      {
        __m512i key_vector = _mm512_loadu_si512((__m512i *)(key + k));
        sum_vector_512 = _mm512_add_epi32(sum_vector_512, key_vector);
        key_vector = _mm512_xor_si512(key_vector, i_j_vector_512);
        _mm512_storeu_si512((__m512i *)(key + k), key_vector);
      }

      __m128i extract1 = _mm512_extracti32x4_epi32(sum_vector_512, 0);
      __m128i extract2 = _mm512_extracti32x4_epi32(sum_vector_512, 1);
      __m128i extract3 = _mm512_extracti32x4_epi32(sum_vector_512, 2);
      __m128i extract4 = _mm512_extracti32x4_epi32(sum_vector_512, 3);

      key_sum += _mm_extract_epi32(extract1, 0) + _mm_extract_epi32(extract1, 1) +
                 _mm_extract_epi32(extract1, 2) + _mm_extract_epi32(extract1, 3);
      key_sum += _mm_extract_epi32(extract2, 0) + _mm_extract_epi32(extract2, 1) +
                 _mm_extract_epi32(extract2, 2) + _mm_extract_epi32(extract2, 3);
      key_sum += _mm_extract_epi32(extract3, 0) + _mm_extract_epi32(extract3, 1) +
                 _mm_extract_epi32(extract3, 2) + _mm_extract_epi32(extract3, 3);
      key_sum += _mm_extract_epi32(extract4, 0) + _mm_extract_epi32(extract4, 1) +
                 _mm_extract_epi32(extract4, 2) + _mm_extract_epi32(extract4, 3);

      if (key_size - k >= 4)
      {
        __m128i i_j_vector_128 = _mm_set1_epi32(i_j);
        __m128i sum_vector_128 = _mm_setzero_si128();
        for (; k + 3 < key_size; k += 4)
        {
          __m128i key_vector_128 = _mm_loadu_si128((__m128i *)(key + k));
          sum_vector_128 = _mm_add_epi32(sum_vector_128, key_vector_128);
          key_vector_128 = _mm_xor_si128(key_vector_128, i_j_vector_128);
          _mm_storeu_si128((__m128i *)(key + k), key_vector_128);
        }

        key_sum += _mm_extract_epi32(sum_vector_128, 0);
        key_sum += _mm_extract_epi32(sum_vector_128, 1);
        key_sum += _mm_extract_epi32(sum_vector_128, 2);
        key_sum += _mm_extract_epi32(sum_vector_128, 3);
      }

      for (; k < key_size; k++)
      {
        key_sum += key[k];
        key[k] ^= i_j;
      }

      character ^= key_sum;
      file[index] = character;
    }
  }
}
#endif

/**
 * @brief Encrypts a file
 *
 * @param file : a K x K matrix containing the file
 * @param key : a `key_size` array containing the key
 * @param key_size : Length of the key
 * @param K : Dimension of the file matrix
 *
 * @note `file` should be modified to contain the encrypted file.
 */
void cipher(int *file, int *key, uint32_t key_size, uint32_t K)
{
  /** Example code that uses the available variables */
  for (uint32_t i = 0; i < K; i++)
  {
    for (uint32_t j = 0; j < K; j++)
    {
      int character = file[i * K + j];

      int key_sum = 0;
      for (uint32_t k = 0; k < key_size; k++)
      {
        key_sum += key[k];
        key[k] ^= i * j;
      }

      character ^= key_sum;
      file[i * K + j] = character;
    }
  }
}

struct encrypted_file
{
  // Pointer to the beginning of the encrypted file
  char *file;
  // Size of the encrypted file
  uint32_t file_size;
};

/**
 * @brief Process the request's body, and return a response. This is the
 * function you should implement.
 *
 * @param ctx The context of the request, only used for logging and memory
 * allocation.
 * @param body The request's body, as a string.
 * @param body_len The length of the request's body.
 * @param resp_len The length of the response.
 *
 * @note You will do the required operations based on the request's body, and
 * return a response. BE CAREFUL, you MUST store the length of your response in
 * `resp_len` before returning.
 *
 * @note Also, this environment keeps you from doing classical `malloc` to
 * allocate memory. Instead, use the function `ngx_link_func_palloc(ctx,
 * number_of_bytes)`. The advantage of this method is that your memory
 * allocation is linked to the request and everything is freed when the resquest
 * finished. No need to worry about freeing memory :)
 */
static char *body_processing(ngx_link_func_ctx_t *ctx, char *body,
                             size_t body_len, size_t *resp_len)
{
  /**
   * TODO: Replace the example code below with your own code.
   */
  struct encrypted_file encrypted_file;
  // complete_algorithm(body, body_len, mutiplication_matrix, &encrypted_file);

  struct parsed_request parsed_request;
  parse_request(body, body_len, &parsed_request);

  uint32_t K = floor(sqrt(parsed_request.file_size / sizeof(int))); // Ensure that your matrix is squared
  int *product = (int *)malloc(K * K * sizeof(int));                //  Do not worry about freeing memory

  int *mutiplication_matrix = get_multiplication_matrix(ctx, K);

  for (size_t i = 0; i < parsed_request.nb_rounds; i++)
  {

    multiply_matrix(parsed_request.file, mutiplication_matrix, product, K);
    cipher(product, parsed_request.key, parsed_request.key_size / sizeof(int), K);
    // Swap pointers for the next iteration
    int *tmp = parsed_request.file;
    parsed_request.file = product;
    product = tmp;
  }

  encrypted_file.file = (char *)parsed_request.file;
  encrypted_file.file_size = K * K * sizeof(int);

  *resp_len = encrypted_file.file_size;
  return encrypted_file.file;
}

/**
 * @brief Optimized version of boyd_processing.
 *
 * Process the request's body, and return a response. This is the
 * function you should implement.
 *
 * @param ctx The context of the request, only used for logging and memory
 * allocation.
 * @param body The request's body, as a string.
 * @param body_len The length of the request's body.
 * @param resp_len The length of the response.
 *
 * @note You will do the required operations based on the request's body, and
 * return a response. BE CAREFUL, you MUST store the length of your response in
 * `resp_len` before returning.
 *
 * @note Also, this environment keeps you from doing classical `malloc` to
 * allocate memory. Instead, use the function `ngx_link_func_palloc(ctx,
 * number_of_bytes)`. The advantage of this method is that your memory
 * allocation is linked to the request and everything is freed when the resquest
 * finished. No need to worry about freeing memory :)
 */
static char *body_processing_optimized(ngx_link_func_ctx_t *ctx, char *body,
                                       size_t body_len, size_t *resp_len)
{
  /**
   * TODO: Replace the example code below with your own code.
   */
  struct encrypted_file encrypted_file;
  // complete_algorithm(body, body_len, mutiplication_matrix, &encrypted_file);

  struct parsed_request parsed_request;
  parse_request(body, body_len, &parsed_request);

  uint32_t K = floor(sqrt(parsed_request.file_size / sizeof(int))); // Ensure that your matrix is squared
  int *product = (int *)malloc(K * K * sizeof(int));                //  Do not worry about freeing memory

  int *mutiplication_matrix = get_multiplication_matrix(ctx, K);

  for (size_t i = 0; i < parsed_request.nb_rounds; i++)
  {
#ifdef SIMD128
    multiply_matrix_optimized_128(parsed_request.file, mutiplication_matrix, product, K);
    cipher_optimized_128(product, parsed_request.key, parsed_request.key_size / sizeof(int), K);
#endif
#ifdef SIMD256
    multiply_matrix_optimized_256(parsed_request.file, mutiplication_matrix, product, K);
    cipher_optimized_256(product, parsed_request.key, parsed_request.key_size / sizeof(int), K);
#endif
#ifdef SIMD512
    multiply_matrix_optimized_512(parsed_request.file, mutiplication_matrix, product, K);
    cipher_optimized_512(product, parsed_request.key, parsed_request.key_size / sizeof(int), K);
#endif
#ifdef SIMD
    multiply_matrix_optimized_SIMD(parsed_request.file, mutiplication_matrix, product, K);
    cipher_optimized_SIMD(product, parsed_request.key, parsed_request.key_size / sizeof(int), K);
#endif

    // Swap pointers for the next iteration
    int *tmp = parsed_request.file;
    parsed_request.file = product;
    product = tmp;
  }

  encrypted_file.file = (char *)parsed_request.file;
  encrypted_file.file_size = K * K * sizeof(int);

  *resp_len = encrypted_file.file_size;
  return encrypted_file.file;
}

void main_function(ngx_link_func_ctx_t *ctx)
{

  // Retrieve request's body
  char *body = (char *)ctx->req_body;
  size_t body_len = ctx->req_body_len;

  // Process the request's body
  size_t resp_len = 0;
  char *resp;

  char *optimized = (char *)ngx_link_func_get_query_param(ctx, "optimized");
  if (optimized == 0x0)
  {
    ngx_link_func_write_resp(
        ctx, 400, "400 Bad Request", "text/plain",
        "No parameters were given. Ensure that your request looks like : "
        "http://localhost:8899?optimized=X, where X is either 1 or 0.\n",
        sizeof(
            "No parameters were given. Ensure that your request looks like : "
            "http://localhost:8899?optimized=X, where X is either 1 or 0.\n") -
            1);
    return;
  }
  else if (*optimized == '1' && strlen(optimized) == 1)
  {
    resp = body_processing_optimized(ctx, body, body_len, &resp_len);
  }
  else if (*optimized == '0' && strlen(optimized) == 1)
  {
    resp = body_processing(ctx, body, body_len, &resp_len);
  }
  else
  {
    ngx_link_func_write_resp(
        ctx, 400, "400 Bad Request", "text/plain",
        "Unknown parameter, your parameter is set to %s, but it should be "
        "either 1 or 0.\n",
        sizeof("Unknown parameter, your parameter is set to %s, but it should "
               "be either 1 or 0.\n") -
            1);
    return;
  }

  // Warn user in case of error during processing
  if (resp == NULL)
  {
    ngx_link_func_write_resp(ctx, 500, "500 Internal Server Error",
                             "text/plain", "Failed to parse request's body",
                             sizeof("Failed to parse request's body") - 1);
    return;
  }
  // War user if he forgot to set the response's length
  if (resp_len == 0)
  {
    ngx_link_func_write_resp(
        ctx, 500, "500 Internal Server Error", "text/plain",
        "You forgot to set the response's length ! :angry:",
        sizeof("You forgot to set the response's length ! :angry:") - 1);
    return;
  }
  // Return the response
  ngx_link_func_write_resp(ctx, 200, "200 OK", "text/plain", resp, resp_len);
}

/**
 * A function that is called when the application is started.
 *
 * You shouldn't do anything here
 */
void ngx_link_func_init_cycle(ngx_link_func_cycle_t *cycle)
{
  ngx_link_func_cyc_log(info, cycle, "%s", "Starting application, new logs !");
  is_service_on = 1;
}

/**
 * A function that is called when the application is stopped.
 *
 * You shouldn't do anything here
 */
void ngx_link_func_exit_cycle(ngx_link_func_cycle_t *cyc)
{
  ngx_link_func_cyc_log(info, cyc, "%s\n",
                        "Shutting down/reloading the Application");

  is_service_on = 0;
}
