#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct stack {
    char stk[500];
    int top;
};

typedef struct stack STACK;
STACK s;

char beginners[50] = "{[(";
char enders[50] = "}])";
char quotes[50] = "\"\'";
char notKeywords[50] = "{[(}])\'\" \EOF \n!=;,";
char token;

int b = 0;
int e = 0;
int q = 0;
int i = 0;

int checkIdentifiers(char t);
int checkBeginners(char t);
int checkEnders(char t);
void checkQuote(char t);
void pop();
void push(char t);

FILE *file;

int main(){


s.top = 0;


file = fopen("file.txt", "r");

do{
    token = fgetc(file);
    checkQuote(token);
    i = i + checkIdentifiers(token);
    b = b + checkBeginners(token);
    e = e + checkEnders(token);

} while (token != EOF);

    if(b == e){
        printf("Brackets are properly nested.\n");
    } else if (b > e) {
        int diff = b - e;
        printf("There are %d too many opening brackets.\n", diff);
    } else if (e > b) {
        int diff = e - b;
        printf("There are %d too many closing brackets.\n", diff);
    }

    printf("There are %d keywords and identifiers.\n", i);

return 0;

}

void checkQuote(char t){
    int preceeding;
    int stkT = s.stk[s.top];
    if(strchr(quotes,t)!=NULL){
        do{
            preceeding = t;
            t = fgetc(file);
            if(strchr(quotes,t) != NULL && preceeding != '\\'){
                break;
            }
        } while (t != EOF );
        if(t==EOF){
            printf("Reached the end of the file without an end quote. Check your quotes!\n");
        }
    }

}

int checkIdentifiers(char t){
    if(strchr(notKeywords, t) == NULL){
        do{
            token = fgetc(file);
            if (strchr(notKeywords, token) != NULL || token == EOF){
                return 1;
            }
        } while(token != EOF);

    } else {
    return 0;
    }

}

int checkBeginners(char t){
    if(strchr(beginners,t)!= NULL){
        push(t);
        return 1;
    } else {
    return 0;
    }
}

int checkEnders(char t){
    int stkT = s.stk[s.top];
    if(strchr(enders,t)!= NULL){
        if(s.top > 0){
            if(stkT=='{' && t == '}'){
            pop();
            return 1;
            } else if (stkT == '[' && t == ']'){
            pop();
            return 1;
            } else if (stkT == '(' && t == ')'){
            pop();
            return 1;
            }
    } else{
    return 1;
    }
    } else return 0;
}

void pop(){
    --s.top;
}

void push(char t){
    ++s.top;
    s.stk[s.top] = t;
}

