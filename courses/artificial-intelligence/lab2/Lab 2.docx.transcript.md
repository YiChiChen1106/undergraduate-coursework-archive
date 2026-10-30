# Lab 2

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

Lab 2 Programming GA Based on a Toolbox

Task: 

There exists a GA toolbox including various GA operators as functions. Your task is to understand them and use these operator functions to build a functional GA. You can choose either binary or real-coded GA.

Link to obtain the GA toolbox: GA Toolbox.zip

You will test your GA by minimizing the following function. This is called G9 function for constrained optimization and the code can be downloaded from http://www-optima.amp.i.kyoto-u.ac.jp/member/student/hedar/Hedar_files/TestGO_files/Page898.htm  

x is the decision variable, which has 7 dimensions. The search range is [-10,10]7. 

Note that you are required to carry out vector programming (i.e., the population as a whole should be considered as the input). Hence, the downloaded functions need to be modified to generate a vector output. Your code needs to be submitted as attachments for the GTAs to test. You only need to submit the code that you generated to finish the task. You do not need to submit the code of G9 function.

Please show the performance of your algorithm using 20 runs (not 20 generations). In each run, save the current best objective function value in each generation. Plot the convergence trend of your algorithm using the median value of the above data in each generation. List the best, worst, mean, and median values of your 20 final results. Each final result is the best objective function value that is obtained in each of the 20 runs. 

Explain how you select the GA parameters (e.g., population size, number of function evaluations, crossover rate, etc) and the penalty coefficients. Note that the GA crossover and mutation operators from this toolbox are different from those in MATLAB's built-in GA function.  

Marking criterion: 

Your program obtains a median result near the global optimum. 

Your plot correctly shows the convergence trend. 

Your table contains the correct statistical values. 

Criterion

Description

Partial Score

Total Score: 100

Objective

Function

The correctness of the penalized objective function 

0~15

15

Result

The program cannot run. 

0~20

50

The program can run but not all of the constraints are satisfied. For each constraint, a violation of 0.1 or smaller can be neglected.

21~30

The program can run and all the constraints are satisfied. The median of the objective function values of the obtained optimal solutions has a distance larger than or equal to 4 compared to the global optimum, 680.63. 

31~45

The program can run and all the constraints are satisfied. The median of the objective function values of the obtained optimal solutions has a distance smaller than 4 compared to the global optimum, 680.63.

46~50

Plot

According to the correctness of the plot. 

0~10

10

Table

According to the correctness of the statistical values.

0~10

10

Explanation 

According to the correctness of the GA settings and the reason.

0~15

15