#include <stdio.h>

int main() {
    int* p_wr;
    p_wr = 0x50000;
    printf("MAP Test");

    (*p_wr) = 25;

    printf("Pointer Write Data[%d] Addr[%ls]\n",(*p_wr),p_wr);

}
