build:
	gcc -I../../nginx-link-function/src -c -pedantic -mno-sse2 -mno-avx -mno-avx2 -mno-avx512f -fno-unroll-loops -fno-tree-vectorize -O2 -ggdb -fPIC -Wall -Wextra -pedantic main.c -o main.o -lm $(CFLAGS)
	gcc -shared -ggdb -o libmain.so main.o -lm

clean:
	rm -f *.o *.so

run: build
	echo "Application is running..."
	../../nginx/install/sbin/nginx -c ../../project/nginx-conf/project.conf -g "daemon off;"

run_debug: build
	echo "Application is running..."
	../../nginx/install/sbin/nginx -c ../../project/nginx-conf/project.conf -g "error_log /dev/stdout error; daemon off;"

run_inginious: build
	echo "Application is running..."
	../../nginx/install/sbin/nginx -c ../../project/nginx-conf/INGInious.conf -g "daemon off;"

run_cuda_checks: build_cuda
	nvcc -Xcompiler -ggdb,-fPIC -O1 -g test.c -o test accelerated.o -lm
	./test

build_cuda:
	nvcc -c -DCUDA_BLOCK_SIZE=16 -std=c++11 -O1 -Xcompiler -fPIC accelerated.cu -o accelerated.o -lm -lcuda
	gcc -DSIMT -std=c++11 -c -ggdb -fPIC -Wall -Wextra -pedantic -mno-sse2 -mno-avx -mno-avx2 -mno-avx512f -fno-unroll-loops -fno-tree-vectorize -O1 -g  main.c -o main.o -lm
	nvcc -O1 -std=c++11 -shared -Xcompiler -mno-sse2,-mno-avx,-mno-avx2,-mno-avx512f,-fno-unroll-loops,-fno-tree-vectorize,-O1,-ggdb -o libmain.so accelerated.o main.o -lm -lcuda

build_avx128:
	gcc -I../../nginx-link-function/src -c -DSIMD128 -pedantic -mno-sse2 -mno-avx -mno-avx2 -mno-avx512f -fno-unroll-loops -fno-tree-vectorize -O2 -ggdb -fPIC -Wall -Wextra -pedantic main.c -o main.o -lm $(CFLAGS)
	gcc -shared -ggdb -o libmain.so main.o -lm

build_avx256:
	gcc -I../../nginx-link-function/src -c -DSIMD256 -pedantic -mno-sse2 -mno-avx -mno-avx2 -mno-avx512f -fno-unroll-loops -fno-tree-vectorize -O2 -ggdb -fPIC -Wall -Wextra -pedantic main.c -o main.o -lm $(CFLAGS)
	gcc -shared -ggdb -o libmain.so main.o -lm

build_avx512:
	gcc -I../../nginx-link-function/src -c -DSIMD512 -pedantic -mno-sse2 -mno-avx -mno-avx2 -mno-avx512f -fno-unroll-loops -fno-tree-vectorize -O2 -ggdb -fPIC -Wall -Wextra -pedantic main.c -o main.o -lm $(CFLAGS)
	gcc -shared -ggdb -o libmain.so main.o -lm

build_avx_best:
	gcc -I../../nginx-link-function/src -c -DSIMD -pedantic -mno-sse2 -mno-avx -mno-avx2 -mno-avx512f -fno-unroll-loops -fno-tree-vectorize -O2 -ggdb -fPIC -Wall -Wextra -pedantic main.c -o main.o -lm $(CFLAGS)
	gcc -shared -ggdb -o libmain.so main.o -lm

run_simd128: build_avx128
	echo "Application is running..."
	../../nginx/install/sbin/nginx -c ../../project/nginx-conf/project.conf -g "daemon off;"

run_simd256: build_avx256
	echo "Application is running..."
	../../nginx/install/sbin/nginx -c ../../project/nginx-conf/project.conf -g "daemon off;"

run_simd512: build_avx512
	echo "Application is running..."
	../../nginx/install/sbin/nginx -c ../../project/nginx-conf/project.conf -g "daemon off;"

run_simd_best: build_avx_best
	echo "Application is running..."
	../../nginx/install/sbin/nginx -c ../../project/nginx-conf/project.conf -g "daemon off;"

run_simd128_debug: build_avx128
	echo "Application is running..."
	../../nginx/install/sbin/nginx -c ../../project/nginx-conf/project.conf -g "error_log /dev/stdout error; daemon off;"
run_simd256_debug: build_avx256
	echo "Application is running..."
	../../nginx/install/sbin/nginx -c ../../project/nginx-conf/project.conf -g "error_log /dev/stdout error; daemon off;"
run_simd512_debug: build_avx512
	echo "Application is running..."
	../../nginx/install/sbin/nginx -c ../../project/nginx-conf/project.conf -g "error_log /dev/stdout error; daemon off;"
run_simt_inginious_debug: build_cuda
	echo "Application is running..."
	../../nginx/install/sbin/nginx -c ../../project/nginx-conf/project.conf -g "error_log /dev/stdout error; daemon off;"

run_simd128_inginious: build_avx128
	echo "Application is running..."
	../../nginx/install/sbin/nginx -c ../../project/nginx-conf/INGInious.conf -g "daemon off;"

run_simd256_inginious: build_avx256
	echo "Application is running..."
	../../nginx/install/sbin/nginx -c ../../project/nginx-conf/INGInious.conf -g "daemon off;"

run_simd512_inginious: build_avx512
	echo "Application is running..."
	../../nginx/install/sbin/nginx -c ../../project/nginx-conf/INGInious.conf -g "daemon off;"
run_simt_inginious: build_cuda
	echo "Application is running..."
	../../nginx/install/sbin/nginx -c ../../project/nginx-conf/INGInious.conf -g "daemon off;"
