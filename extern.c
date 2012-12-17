#include <stdio.h>

void print_int(long long var) {
    printf("%lld", var);
}

void print_str(char *var) {
    printf("%s", var);
}

void print_char(long long var) {
    printf("%c", (char)var);
}

int read_int() {
    int var; scanf("%d", &var); return var;
}

int comp_less(int a, int b) {
    printf("comp %d < %d\n", a, b);
    return a < b ? 1 : 0;
}

int read_char() {
    char var; scanf(" %c", &var); return var;
}
