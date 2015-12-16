
#include <stdio.h>
#include <stdlib.h>
#include <NIDAQmx.h>
#include <math.h>
#include <vector>
using namespace std;
#define DAQmxErrChk(functionCall) if( DAQmxFailed(error=(functionCall)) ) goto Error; else
int readcsv(vector<double> leftchannel, vector<double> rightchannel){
	char file_name[25];
   	FILE *fp;
   	printf("Enter the name of file\n");
   	gets(file_name);
   	int temp = 1;
	int num = 0;
	double left, right;
   	fp = fopen(file_name,"r"); // read mode
 
	if( fp == NULL ){
	printf("The file does not exist!\n");
   	}
   	   	
	while(1){
		temp = fscanf(fp,"%lf,%lf", &left, &right);
		if(temp<0)
			break;   // End reading when fscanf cannot match any data
		leftchannel.push_back(left);
		rightchannel.push_back(right);  
//		printf("%lf %lf\n",*(leftchannel+num),*(rightchannel+num));
		num++;
		// num recourd the number of sets of data
		// Extent the arrays if the size is not big enough
		if(num >= leftchannel.size()){
			leftchannel.resize(leftchannel.size() + 10000); 
			rightchannel.resize(leftchannel.size() + 10000); 
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
	double     data[1000];
	char        errBuff[2048]={'\0'};
	vector<double> leftchannel(10000);
	vector<double> rightchannel(10000);
	int i = 0;
	readcsv(leftchannel, rightchannel);
	int mysize = leftchannel.size();
	printf("%d\n",mysize);
	double* left = (double*)malloc(sizeof(double)*mysize);

	for(; i<mysize; i++){
		left[i] = leftchannel[i];		
	}  
	/*********************************************/
	// DAQmx Configure Code
	/*********************************************/
	DAQmxErrChk (DAQmxCreateTask("",&taskHandle));
	printf("Create task ..... \n");
	DAQmxErrChk (DAQmxCreateAOVoltageChan(taskHandle,"myDAQ1/ao0","",-10.0,10.0,DAQmx_Val_Volts,NULL));
	DAQmxErrChk (DAQmxCfgSampClkTiming(taskHandle,"",5000.0,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,mysize));
//	/*********************************************/
//	 DAQmx Write Code
	/*********************************************/
	DAQmxErrChk (DAQmxWriteAnalogF64(taskHandle,mysize,0,10.0,DAQmx_Val_GroupByChannel,left,NULL,NULL));
//
//	/*********************************************/
//	 DAQmx Start Code
//	/*********************************************/
	DAQmxErrChk (DAQmxStartTask(taskHandle));
	printf("Start task ..... \n");
	DAQmxErrChk (DAQmxWaitUntilTaskDone(taskHandle,20.0));



Error:
	if( DAQmxFailed(error) )
		DAQmxGetExtendedErrorInfo(errBuff,2048);
	if( taskHandle!=0 ) {
		/*********************************************/
		// DAQmx Stop Code
		/*********************************************/
		DAQmxStopTask(taskHandle);
		printf("End task .... \n");
		DAQmxClearTask(taskHandle);
		printf("clear task .... \n");
	}
	if( DAQmxFailed(error) )
		printf("DAQmx Error: %s\n",errBuff);
	printf("End of program, press Enter key to quit\n");
	getchar();
	return 0;

}


