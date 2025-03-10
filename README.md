# Shop Drawing Package Version Update
In this project we aim to automate the version update / incrementation / date update in the shop drawing packages  which are in DEG / DXF format
AFC and AS BUILT Package Automation

Please follow the instructions to generate the AFC and AS BUILT Packages automatically and in a short time, rather than manually editing each drawing.
1.Clone the program onto your system
The first step is to clone the program onto your system using the SSH key or HTTPS patch:
SSH:
git@support.safetypower.ca:engineering/shop_drawing_version_control.git
HTTPS:
https://support.safetypower.ca/engineering/shop_drawing_version_control.git

Apply the following commands in your terminal to clone the program:
SSH:
•	cd path/to/your/folder
•	git clone git@support.safetypower.ca:engineering/shop_drawing_version_control.git
use the following link to learn about the SSH key:
•	  https://docs.github.com/en/authentication/connecting-to-github-with-ssh

HTTPS:
•	cd path/to/your/folder
•	git clone https://support.safetypower.ca/engineering/shop_drawing_version_control.git


2.	Download and Install the ODA file converter
The first step is to download and install the ODA file converter on your system. In order to convert the DWG files to editable DXF files.
 ![image](https://github.com/user-attachments/assets/1b381d33-2f4d-4af0-b14c-c394d52657a8)
![image](https://github.com/user-attachments/assets/b436328d-15e7-4f20-a191-a5621a78d983)
![image](https://github.com/user-attachments/assets/7906433a-84f0-4d29-9aa4-f86c2334e978)

 
3.	Add a virtual environment and install all the required packages
To make a virtual environment in your project directory, you need to follow the following steps:
-change the path to your project folder: 
  cd path/to/your/project
-make the virtual environment using the following command
  python -m venv myenv
-Activate your virtual environment using the following command
  myenv\Scripts\activate

Now you need to install the following packages using the following command:
  pip install (package name/library)
The following packages need to be installed:
 (os, ezdxf, re, datetime, shutil, subprocess, matplotlib)
 ![image](https://github.com/user-attachments/assets/e79b154e-80e0-43e3-ad5e-75e2166939a3)

4.	Add the input and output folders directory to the code
You need to add the input, output and pdf folders directory to your code. Please follow these steps:
-Go to the project folder>02 Shop Drawing Package>_Working> (project version: ex. 24153_Shop drawing package_Rev4A)
-Make the following folders (output folders) in the working project directory: dwg2, pdf2
-Add the directory of the output folders to the code; simply right click on the folder, select “copy path” and paste it to the code to make the following format:
r"\\192.168.2.11\SharedDocs\1. SPI Documents\projects\24153 - MSA2AZ1\02 Shop Drawing Package\_Working\MTU-RR Google Shop Drawing Package Rev5A_AS BUILT\dwg2"

Please note that your input folder is the dwg folder in your project directory, output folder is the dwg2 you created and the pdf2 is where the printed files are saved.
 ![image](https://github.com/user-attachments/assets/4c2af9ff-a3e6-4d38-b27a-49f83c857a7e)

5.	Run the program
In the next step you can run the program.
And answer the questions in the terminal
 ![image](https://github.com/user-attachments/assets/523006d1-298e-45eb-8a18-bf2c7483dd33)


To find the x1, y1, x2, y2, x3 , y3, simply open up a drawing (EX. 24153 PI-02), x1,y1 are the coordinates of the Rev number, x2, y2 are the coordinates of Rev and x3,y3 are the location of Date. As can be seen in the image below y1= y2 = y3, so you just need to add y1.
When you opened the drawing package, type “id” using this command you can locate all the coordinates. 
 ![image](https://github.com/user-attachments/assets/4e4031a5-adae-4db8-b63b-35c418662a6f)


In the next step the program asks about the Rev you need to apply:
Add “1” if you need to rev up from “FOR CUTOMER APPROVAL” to “APPROVED FOR CONSTRUCTION”
Add “2” if you need to rev up from “APPROVED FOR CONSTRUCTION” to “AS BUILT”
Add “3” if you need to rev up from “FOR CUTOMER APPROVAL” to “AS BUILT”
