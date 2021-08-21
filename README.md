# AI-Scheduler
<h2>Final Project Computer Science - Ariel University</h2><br>
<h3>Team members: Amit Bibi 203262647, Moran Oshia 313292633, Alex Chagan 206262123</h3><br>

![alt text](https://github.com/amitbb93/AI-Scheduler/blob/main/Documents/AI-Scheduler.jpg)


## Contribution/project goal

Our AI Scheduler will provide an easy way to create a shifts board for the managers and the workers. 

## Introduction

Nowadays, most of the process of creating shifts schedules is a tedious process for employers and employees.
In a world where procedures become automated, we are replacing manual shift creation with automation and fairness.
Even better, we make the submission of the shifts easier and more automated for the employees themselves, not only the employers.


## Selected Approach & Infrastructure

We created a Linux virtual machine in Azure portal with a network security group that regulates the inbound and outbound traffic. In the VM we have a docker container that keeps our web application running.
We use a Machine Learning - Logistic Regression algorithm with the Sklearn package to extract data of previous preferences of workers and creates a recommendation system for each worker.
We use HTML web to offer and submit shifts to users, than we extract data into Excel files, execute a heuristic algorithm and returns output in csv format that keep all the information 
and display it to the users. 

## Our Solution

We decided to build a website application that will satisfy the goals of our project. The part which is responsible for the creation of the shifts board  will use linear programing, that will schedule workers to shifts by their preferences and restrictions. In addition, the worker will get suggestions of schedule shift offers based on previous preferences, the machine will recognize the most frequent shifts the worker chose every week from our DB and create a suggested shifts board. Our product allows users to maximize efficiency of creating adapted work schedules with a click of button and offers a user friendly interface for both managers and workers.


