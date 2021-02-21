Sample crash
------------

    gcc -s segfault.c
    ulimit -c unlimited
    ./a.out
    gdb a.out core

    
