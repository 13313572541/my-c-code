#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

    int removeElement(int a[], int n, int val) {
        int j = 0;                      // j = 已留下的元素个数
        for (int i = 0; i < n; i++) {
            if (a[i] != val) {          // 不是要删的 → 留下
                a[j] = a[i];
                j++;
            }
            // 是要删的 → 跳过，什么都不做
        }
        return j;                       // j 就是新长度
    }

    int main() {
        int a[10];
        for (int i = 0; i < 10; i++) {
            scanf("%d", &a[i]);
        }
        int val;
        scanf("%d", &val);

        int newLen = removeElement(a, 10, val);

        for (int i = 0; i < newLen; i++) {
            printf("%d ", a[i]);
        }
        printf("\n%d\n", newLen);

        return 0;
    }