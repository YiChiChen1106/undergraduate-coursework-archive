# Lab 1

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

Lab 1: Modeling EE problems and make use of MATLAB functions 

Task 1 (30’): 

Microwave diplexers are widely used in communication systems. The evolutionary optimization technique, which is a branch of AI, can be used to obtain the optimal coupling matrix of a target diplexer according to design specifications. In this process, there must be a function showing the performance of a certain diplexer response, which is shown in the following figure. The S11, S21, and S31 are responses. 

Figure 1 Responses of a diplexer.

S11, S21, and S31 responses need to be considered. Ideally, we expect a diplexer satisfying all the specifications for S11, S21, and S31. To evaluate how certain S11, S21, and S31 responses meet the S11, S21, and S31 specifications, we need to write such a function (i.e., objective function), which will be used for diplexer optimization in the future. In this task, you are asked to write a function evaluating whether the provided diplexer responses meet the specifications or not. If not, how large is the violation? 

The files:

“T_junctioni_best.mat” is the S-parameter magnitude data.

“plot_values” is the code for drawing the S-parameter responses.

https://gla-my.sharepoint.com/:u:/g/personal/bo_liu_glasgow_ac_uk/EQuNMWWeL1dOkoEtl29XBuABfc93FQBa3Ma_6obeHOIeaw?e=R8ud2M 

The specifications

S11_val≤-20 dB, 12.5~12.75 GHz and 13~13.25 GHz  // For example, in Fig. 1, the S11 curve is not under -20 dB at every frequency. Hence, there are violations of S11 specifications.  

S21_val≤-20 dB, 12~12.3 GHz; S21_val≤-55 dB, 13~13.25 GHz

S31_val≤-55 dB, 12.5~12.75 GHz; S31_val≤-20 dB, 13.4~13.75 GHz

Task:

1. Write a MATLAB function to represent the performance of the diplexer based on the design specifications. 

function perf = evaluate (f, S11_val, S21_val, S31_val) 

where f is the frequency variable, S11_val, S21_val, and S31_val are the magnitudes of S-parameters, which will be used for the comparison with the specifications. They can be found in the data file. It is a cell array and the variables can be extracted by: 

perf is a vector containing [E1,E2,E3,E4,E5,E6], corresponding to each frequency range. 

For example, E1 targets S11_val≤-20 dB, 12.5~12.75 GHz. E2 targets S11_val≤-20 dB, 13~13.25 GHz, … E means the violation of specifications in a certain frequency range. 

For example, the meaning of E1 is as follows: S11_val has certain values from 12.5~12.75 GHz. If all of them are smaller than or equal to -20 dB, then there is no violation of specification, and the violation is 0 (E1=0). 

Otherwise, if at some frequency points between 12.5~12.75 GHz, the values of S11_val are larger than -20 dB, then there are violations, and E1 should be the largest violation value among them. 

For example, between 12.5~12.75 GHz, at 12.65 GHz, S11_val=-18 dB, and at 12.70 GHz, S11_val=-17 dB, and in all other frequency points, S11_val≤-20 dB. 

Then E1=3 because the maximum violation of -20 dB between 12.5~12.75 GHz (E1 targets) is -17-(-20)=3. So do E2 to E6.

You need to submit a report with your code including function output and sufficient comments. 

Student files:

 https://gla-my.sharepoint.com/:u:/g/personal/bo_liu_glasgow_ac_uk/Edu2gMK5fZZMjlv1dWFNgpsBJT7hg-AucJQef8cnZnZdUg?e=FX9SEv 

Data: 

https://gla-my.sharepoint.com/:u:/g/personal/bo_liu_glasgow_ac_uk/EelsUNt6HENBpYNOy0DiEO4Bz0Wp2C88KQz4BxF8XPGDew?e=FF6cNj 

Marking criterion: 

The total mark is evenly distributed to each subtask (i.e., E1 to E6). 

Your program can obtain correct outputs: 70%. 

You provided sufficient comments to let other people understand your code: 20%.  

Your program is concise and runs fast (you are encouraged to use built-in functions that were not taught in class): 10%.

The above applies to each output value.

Criterion

Description

Partial Score

Total Score: 100

Correctness

The answer for E1 is correct. (10)

If incorrect. (0~5)

0~60

70

The answer for E2 is correct. (10)

If incorrect. (0~5)

The answer for E3 is correct. (10)

If incorrect. (0~5)

The answer for E4 is correct. (10)

If incorrect. (0~5)

The answer for E5 is correct. (10)

If incorrect. (0~5)

The answer for E6 is correct. (10)

If incorrect. (0~5)

Question: Which one satisfies the specifications?

0 or 3 or 6 or 10

Comment

No comments.

0

20

Simple comments. It may confuse others.

0~10

Sufficient comments. Understandable.

10~20

Conciseness

The program is redundant.

0~5

10

The program is concise.

5~8

If using built-in functions

+2

The total mark will be multiplied by 0.3 to match 30’ for this task. 

Task 2 (40’): 

Human activity recognition (HAR) is an important research topic, which has many applications, e.g., sport and health monitoring, assisted living, gaming, and human-computer interaction to name a few. The raw data can be collected from a Radar or Wifi. The data are then processed to extract useful information from radar signatures, which we call features. Features need to first be extracted prior to classification and a selection needs to be performed to retain only the salient features for the task at hand. Classification techniques for HAR, which is a branch of machine learning can be applied using statistical learning or deep learning methods.

You will work on a subset of the database provided by the university of Glasgow for human radar signatures – the full dataset and information related to it can be downloaded from this location. Figure 2 presents the 6 activities from the subset 1: walking, 2: sitting, 3 standing, 4 picking up an item, 5: drinking, 6: falling. Their corresponding radar signatures are in Figure 3. 

Figure 2: Human Activities contained in the subset of the database.

Figure 3: corresponding radar microDoppler signatures of activities 1 to 6.

In radar, classification work is still primarily performed on spectrograms, i.e., micro-Doppler signatures showing Doppler-time representations of the received signals based on Short-Time Fourier Transform. This approach offers simple and effective data representation for problems presenting large interclass variations Spectrogram generation is computationally efficient as it is Fourier-transform-based. To read all the basics about frequency modulated radar, you can refer to the page here. The raw data recorded by the radar is a beat frequency that is directly proportional to the delay stemming from the time of flight between the radar and the target under observation. After performing an FFT for each sweep duration (1ms or 128 samples), you will obtain the range information of all targets in the field of view of the radar. This will then be used across the slow-time domain (across range profiles or across a succession of sweeps) per range bin to extract the Doppler (speed information) using a short-time Fourier transform. This will be performed repeatedly for the duration of the recording over a predefined time window. This time window is sliding across the recording to produce the microDoppler signature. 

In this task, you are asked to support preparing the data for employing machine learning methods for classification in the future. The whole data processing procedure is complex. However, many works were finished by other engineers and the data provided to you include 6 activities with 359 data files. 

You will find a MATLAB function called spectrogramprops. By running this function, you will process all 359 files together. To run the program, make sure that the folder with the dataset is within the folder where you are running the MATLAB program. The location should be like the following figure. 

Figure 4: run the function 

[Spec_image,labels] = spectrogramprops(0,1,256,0.95,0,0.1,0,0,0,0,1,0);

Spec_image (352x92 matrix) and labels (359x1 vector) are the data for training and testing the classifier in the future.   

The spectrogramprops.m is incomplete, and you need to fill in the “?” according to the instructions in the comments, making it can be run without throwing out an error.

P.S. If you are not using the latest version of MATLAB, the function im2gray will not work. Please change all im2gray in the file division.m (Line 79, 108, 109, and 128) to rgb2gray.

Marking criterion: 

The total mark is evenly distributed to each subtask (i.e., each question). 

Your program can obtain correct outputs: 100%. For code whose output is incorrect, but some correct ideas are used, some marks can be provided, but not more than 50%.  

The above applies to each subtask.   

Description

Score

Run with error.

0~25

Run without error but the result is incorrect.

25~50

Perfect!

100

The total mark will be multiplied by 0.4 to match 40’ for this task. 

Task 3 (30’): 

There is a MATLAB built-in function called ‘ga’ which uses the genetic algorithm for optimization. There is a function called the Ackley function and the code can be downloaded from http://www-optima.amp.i.kyoto-u.ac.jp/member/student/hedar/Hedar_files/TestGO_files/Page295.htm 

x is the decision variable, which has 10 dimensions. The search range is [-15,30]10. Note that the above function uses 2 dimensions and you need to revise it to 10 dimensions. 

Please use the ‘ga’ function to optimize the 10d Ackley function. You need to submit a report with your code showing (1) your revised 10d Ackley function, (2) your use of the ga function, and (3) the result, including the obtained optimal values of the decision variables and the corresponding optimal objective function value.   

Marking criterion: 

Your revised Ackley function is correct: 20%

Your use of the ‘ga’ function is correct (no syntax error): 25%

Your program can obtain an optimal solution for the Ackley function: 25% 

You have displayed your result correctly: 20%

Your program has comments and is concise: 10%

Criterion

Description

Partial Score

Total Score: 100

Correctness

Revised Ackley function

0~20

20

 Use “ga” function

0~25

25

Obtain correct result

Your provided optimal objective function value has a distance compared to the global optimum. The distance is smaller than 10 and is larger than 0.01.  

0~20

25

Your provided optimal objective function value has a distance compared to the global optimum. The distance is smaller than 0.01.  

21~25

Display results (plot and value)

0~20

20

Comment

No comments.

0

5

Sufficient comments. Understandable.

1~5

Conciseness

The program is redundant.

0~2

5

The program is concise.

2~5

The total mark will be multiplied by 0.3 to match 30’ for this task.