#include <stdio.h>
#include <stdlib.h>

int main(){
	/* Initialize */
	int mysize = 10000;  // Initial size of the data
   	int temp = 1, num = 0, i = 0; // temp->stores the result of fscanf, num -> records the number of data
    double *leftchannel; 
	double *rightchannel;
	leftchannel = (double*)malloc(sizeof(double)*mysize);
	rightchannel = (double*)malloc(sizeof(double)*mysize);

	/* read the csv file */
	char file_name[25];
   	FILE *fp;
   	printf("Enter the name of file\n");
   	gets(file_name);
   	fp = fopen(file_name,"r");
	if( fp == NULL ){
		printf("The file does not exist!\n");
   	}
   	
   	/* Begin reading data */
	while(1){
		temp = fscanf(fp,"%lf,%lf", leftchannel+num, rightchannel+num);
		if(temp<0){
			break;   // End reading when fscanf cannot match any data
		}
		num++;       // Data number increment
		
		/* Extend the arrays if the size is not big enough */
		if(num >= mysize){
			mysize *= 2; // double the size			
			leftchannel = realloc(leftchannel, mysize*sizeof(double));
			rightchannel = realloc(rightchannel, mysize*sizeof(double));
		}
		
	}
	printf("Finish reading! The number of rows: %d.\n", num);


	
	/* Clost file pointer and free memory space */		
   	fclose(fp);
	free(leftchannel);
	free(rightchannel);
	
   	return 0; 
}
