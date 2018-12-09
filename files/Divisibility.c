#include <stdio.h>

int main() {
setbuf(stdout, NULL);
    int a, b;
    printf("Enter A value: "); printf("\n"); fflush(stdout); /**/
    scanf("%d", &a);

    printf("Enter B value: "); printf("\n"); fflush(stdout); /**/
    scanf("%d", &b);

    if (a % b == 0) {
        printf("divisible"); printf("\n"); fflush(stdout); /**/
    } else {
        printf("not divisible"); printf("\n"); fflush(stdout); /**/
    }
}


