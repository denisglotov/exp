Convert hexadecimal string into binary file.

* Even longer string than 4096 bytes (PIPE_BUF size on linux).
* Even containing LF characters in the middle.

Usage example:

    cat >/tmp/input.txt
    # Paste you data here, then press Enter and Ctrl-D

    python hex-to-bin.sh /tmp/input.txt /tmp/output.bin

    od --width=32 -A x -t x1z -v /tmp/output.bin
