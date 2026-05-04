# BACHELOR-PROJECT
This repository contains the code in python and C++ for my bachelor's project (grade: 10/B) titled: "Automated Disassembly: Design and Development of a Bearing Puller Mechanism".  My work in this project can be roughly be divided in 3:

First part: Development of a Python Application to
- visualise sensordata (Distance and force measurement during extraction) in real-time
- storing the data (in normal folder structure).
- Visualise stored data
- Provide an interface for controlling the gripper

Second part: Firmnware coding in C++ on ESP32 to
- Integrate ST3020 Servo Motors in Mechanical design to control the gripper diameter and height
- Measure Force during extraction with load cell
- Measure distance (through rotary encoder in ST3020) during extraction

Third part: Having the python application communicate with the ESP32 through serial commanication to 
- Control the gripper (Python interface -> ESP32)
- Visualize real-time data (ESP32 -> Python interface)

OVERALL: This was a bachelor's project with as much focus on innovation and iterative design processes as on the technical part. A very "loose" defined project: "Smart Remanufacturing of products", my bachelor partner and I were required to provide an in-depth research and be creative early on to actually find the problem we wanted to solve.

