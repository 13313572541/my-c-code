#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main() {
    int a;

	scanf("%d", &a);

	for (int i = 2; i <a; i++) {
		if (a % i == 0) {
			printf("No");
			return 0;
		}
	}
	printf("Yes");
    return 0;
}
