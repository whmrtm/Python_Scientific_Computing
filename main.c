
#include <stdio.h>
#include <stdlib.h>
#include <NIDAQmx.h>
#include <math.h>

#define DAQmxErrChk(functionCall) if( DAQmxFailed(error=(functionCall)) ) goto Error; else

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

int main(void)
{
	int32       error=0;
	TaskHandle  taskHandle=0;
	float64     data[1000];
	char        errBuff[2048]={'\0'};
	int         i, written, num=0;
	
	double *leftchannel = (double*)malloc(sizeof(double)*mysize); 
	double *rightchannel = (double*)malloc(sizeof(double)*mysize);

	num = readcsv(leftchannel, rightchannel);
//	
//	for(;i<1000;i++)
//		data[i] = 9.95*sin((double)i*2.0*3.14/1000.0);

	/*********************************************/
	// DAQmx Configure Code
	/*********************************************/
	DAQmxErrChk (DAQmxCreateTask("",&taskHandle));
	DAQmxErrChk (DAQmxCreateAOVoltageChan(taskHandle,"myDAQ1/ao0","",-10.0,10.0,DAQmx_Val_Volts,NULL));
	DAQmxErrChk (DAQmxCfgSampClkTiming(taskHandle,NULL,2000,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,num));

//	DAQmxErrChk (DAQmxRegisterDoneEvent(taskHandle,0,DoneCallback,NULL));

	/*********************************************/
	// DAQmx Write Code
	/*********************************************/
	DAQmxErrChk (written = DAQmxWriteAnalogF64(taskHandle,num,0,0,DAQmx_Val_GroupByChannel,leftchannel,NULL,NULL));

	/*********************************************/
	// DAQmx Start Code
	/*********************************************/
	DAQmxErrChk (DAQmxStartTask(taskHandle));
	printf("Start task!\n");
//	getchar();
	DAQmxErrChk(DAQmxWaitUntilTaskDone(taskHandle,10));
	
Error:
	if( DAQmxFailed(error) )
		DAQmxGetExtendedErrorInfo(errBuff,2048);
	if( taskHandle != 0 ) {
		/*********************************************/
		// DAQmx Stop Code
		/*********************************************/
		DAQmxStopTask(taskHandle);
		DAQmxClearTask(taskHandle);
		printf("Finish task!\n");
		printf("End of program, press Enter key to quit\n");
		getchar();
		return 0;
	}
	if( DAQmxFailed(error) )
		printf("DAQmx Error: %s\n",errBuff);
		
}

