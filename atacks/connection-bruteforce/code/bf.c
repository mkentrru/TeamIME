#include "stdio.h"
#include "stdlib.h"
#include "string.h"

struct passwd_t{
    unsigned char *s;
    int len;
    unsigned char min;
    unsigned char max;
};

int passwd_init (
    struct passwd_t *p,
    int len, 
    unsigned char min, 
    unsigned char max
){
        if (p == NULL)
            return EXIT_FAILURE;
        p->s = (unsigned char*) 
        malloc ((len + 1) * sizeof(char));
        if (p->s == NULL)
            return EXIT_FAILURE;
        memset (p->s, min, sizeof(char) * len);
        p->len = len;
        p->min = min;
        p->max = max;
        p->s[len] = '\0';
    }

int passwd_inc (
    struct passwd_t *p
){
    for (int i = 0; i < p->len; i++){      
        p->s[i]++;
        if ( p->s[i] > p->max){
            p->s[i] = p->min;
            if( i == p->len - 1)
                return EXIT_FAILURE;
        }
        else
            return EXIT_SUCCESS;
    }
    return EXIT_SUCCESS;
}

int main(int argc, char* argv[]){
    struct passwd_t p; 
    passwd_init(&p, 4, '1', '9');

    do{
        printf("%s\n", p.s);
    } while (passwd_inc(&p) == EXIT_SUCCESS);
        
}
