#include <stdio.h>

int main() {
    int n, y;

    printf("Enter N value: "); printf("\n"); fflush(stdout); /**/
    scanf("%d", &n);
    
    for(int i=1; i<=n; i+=1) {
        printf("%d\n", i); fflush(stdout); /**/
    }

    return 0;
}







