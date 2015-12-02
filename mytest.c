#include <stdio.h>
#include <stdlib.h>
int mysize = 10000;
int readcsv(double* leftchannel, double* rightchannel){
	char file_name[25];
   	FILE *fp;
   	printf("Enter the name of file\n");
   	gets(file_name);
   	int temp = 1, num = 0;
   	fp = fopen(file_name,"r"); // read mode
 
	if( fp == NULL ){
	printf("The file does not exist!\n");
   	}
   	
   	printf("The contents of %s file are :\n", file_name);
   	
	while(1){
		temp = fscanf(fp,"%lf,%lf",leftchannel+num,rightchannel+num);
		if(temp<0)
			break;   // End reading when fscanf cannot match any data
		
		printf("%lf %lf\n",*(leftchannel+num),*(rightchannel+num));
		num++;
		// num recourd the number of sets of data
		// Extent the arrays if the size is not big enough
		if(num >= mysize){
			mysize += 10000;
			leftchannel = realloc(leftchannel, mysize*sizeof(double));
			rightchannel = realloc(rightchannel, mysize*sizeof(double));
		}
	}
	printf("Finish reading! The number of rows: %d.\n", num);
			
   	fclose(fp);
   	return num; 
}

int main(){
	double *leftchannel = (double*)malloc(sizeof(double)*mysize); 
	double *rightchannel = (double*)malloc(sizeof(double)*mysize);
	readcsv(leftchannel, rightchannel);
	int i = 0;
	for(;i < 1000; i++){
		printf("%lf, ",leftchannel[i]);
	}
   	return 0; 
}
