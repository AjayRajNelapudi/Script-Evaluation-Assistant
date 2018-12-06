#include <stdio.h>

int main() {
setbuf(stdout, NULL);
    int a, b;
    printf("Enter A value: ");
    scanf("%d", &a);

    printf("Enter B value: ");
    scanf("%d", &b);

    if (a % b == 0) {
        printf("divisible");
    } else {
        printf("not divisible");
    }
}


