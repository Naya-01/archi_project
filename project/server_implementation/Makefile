build:
	gcc -I../../nginx-link-function/src -c -ggdb -fPIC -Wall -Wextra -pedantic main.c -o main.o -lm
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