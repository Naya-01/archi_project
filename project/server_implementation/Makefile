build:
	gcc -I../../nginx-link-function/src -c -pedantic -mno-sse2 -mno-avx -mno-avx2 -mno-avx512f -fno-unroll-loops -fno-tree-vectorize -O2 -ggdb -fPIC -Wall -Wextra -pedantic main.c -o main.o -lm $(CFLAGS)
	gcc -shared -ggdb -o libmain.so main.o -lm
clean:
	rm -f *.o *.so
run:
	echo "Application is running..."
	../../nginx/install/sbin/nginx -c ../../project/nginx-conf/project.conf -g "daemon off;worker_processes 8;"
run_debug: build
	echo "Application is running..."
	../../nginx/install/sbin/nginx -c ../../project/nginx-conf/project.conf -g "error_log /dev/stdout error; daemon off;"
run_inginious: build
	echo "Application is running..."
	../../nginx/install/sbin/nginx -c ../../project/nginx-conf/INGInious.conf -g "daemon off;worker_processes 8;"
