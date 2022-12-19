#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MIN(a, b) (((a) < (b)) ? (a) : (b))
#define ADD(a, b) (a + b)


int check_password(char *p, int p_size, char *i, int i_size)
{
    char p_guess[16] = "\0";
    int k = 0;
    int is_valid = 0;

    if (i_size > 14 || i_size < 0){
        return 0;
    }
    
    is_valid = is_pwd_safe(p_guess, i, i_size);

    for (k = 0; k < 15; k++){
        is_valid |= (p[k] != p_guess[k]);
    }

    return !is_valid;
}

int is_pwd_safe(char *p_guess, char *i, int i_size)
{
    int j = 0;
    int k = 0;
    int is_safe = 0;
    int end_j = (15 - i_size);
    for (j = 0; j < end_j; j++){
        p_guess[j] = '$';
    }
    for (k = 0; (j + k) < 15; k++){
        p_guess[j + k] = i[k];
        is_safe = is_safe | (i[k] == '$');
    }
    return is_safe;
}

// assumptions: password only has small characters [a, z], maximum length is 15 characters
int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        fprintf(stderr, "Usage: %s <password guess> <output_file>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    FILE *password_file;
    char password[16] = "\0";

    size_t len = 0;
    char *line;
    password_file = fopen("/home/isl/t2_3/password.txt", "r");

    if (password_file == NULL)
    {
        perror("cannot open password file\n");
        exit(EXIT_FAILURE);
    }

    fread(password, 1, 15, password_file);

    int is_match = 0;
    is_match = check_password(password, 15, argv[1], strlen(argv[1]));

    FILE *output_file;
    output_file = fopen(argv[2], "wb");
    fputc(is_match, output_file);
    fclose(output_file);

    fclose(password_file);
    return 0;
}
