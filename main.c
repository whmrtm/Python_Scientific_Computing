
#include <stdio.h>
#include <stdlib.h>
#include <NIDAQmx.h>
#include <math.h>
#include <string.h>

#define DAQmxErrChk(functionCall) if( DAQmxFailed(error=(functionCall)) ) goto Error; else

int main(void)
{
	/* Initialize */
	int32  error=0;
	TaskHandle  taskHandle=0;
	double  data[1000];
	char  errBuff[2048]={'\0'};	
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

	/* DAQmx Configure Code */
	DAQmxErrChk (DAQmxCreateTask("",&taskHandle));
	printf("Create task ..... \n");
	DAQmxErrChk (DAQmxCreateAOVoltageChan(taskHandle,"myDAQ1/ao0","",-10.0,10.0,DAQmx_Val_Volts,NULL));
	DAQmxErrChk (DAQmxCfgSampClkTiming(taskHandle,"",10000.0,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,num));
	
	/* DAQmx Write Code */
	DAQmxErrChk (DAQmxWriteAnalogF64(taskHandle,num,0,10.0,DAQmx_Val_GroupByChannel,leftchannel,NULL,NULL));

	/* DAQmx Start Code */
	DAQmxErrChk (DAQmxStartTask(taskHandle));
	printf("Start task ..... \n");
	DAQmxErrChk (DAQmxWaitUntilTaskDone(taskHandle,20.0));



Error:
	if(DAQmxFailed(error))
		DAQmxGetExtendedErrorInfo(errBuff,2048);
	if(taskHandle!=0 ) {
		/* DAQmx Stop Code */
		DAQmxStopTask(taskHandle);
		printf("End task .... \n");
		DAQmxClearTask(taskHandle);
		printf("clear task .... \n");

		/* Clost file pointer and free memory space */
		fclose(fp);
		free(leftchannel);
		free(rightchannel);

	}
	if(DAQmxFailed(error))
		printf("DAQmx Error: %s\n",errBuff);
		
	printf("End of program, press Enter key to quit\n");
	getchar();
	return 0;
}

