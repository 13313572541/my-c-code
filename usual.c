#define  _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main()
{
	// Your code here
	int p = 0;
	int b = 0;
	//shu ru
	printf("need\n");
	scanf("%d", &p);
	printf("u give\n:");
	scanf("%d", &b);

	if (b < p)
	{
		printf("need%d\n", p - b);
	}
	else if (b > p)
	{
		printf("u get%d元\n", b - p);
	}
	else
	{
		printf("OK\n");
	}

}