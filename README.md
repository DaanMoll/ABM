# ABM - The performance of traffic flow with MESA

This agent based traffic model is built using the MESA package in python. We simulate the movement of cars on a road network using a grid model. Cars drive random optimal paths, stopping when they are too close to other cars or when they encounter a red traffic light. Traffic lights were placed at each intersection. Aditionally, when a car experiences a high level of congestion (calculated as the ratio of its cumulative speed and maximum speed) it enters a *hasty* state, causing the agent to driver over the speed limit. The model output measured is the average congestion experienced by agents.

## How to use:

All simulation files are under the ```abm_project``` folder.

There are four parameters in our model that can be adjusted: 
- maximum number of cars
- traffic light duration
- maximum speed
- haste tolerance level

Executing ```run.py``` will open the simulation as a browser window, where the model parameters can be tweaked using sliders.

The ```sensitivity_analysis.ipynb``` is a Jupyter Notebook that does sensitivity analysis on the model with OFAT and Sobol decomposition. 

## What to expect:

The simulation shows the average congestion level and the haste level, the more cars being put into the simulation, the likely it will get a high congestion. This may cause a gridlock, where the cars are not able to move anymore.


## References:

"Mesa: Agent-based modeling in Python 3+ — Mesa .1 documentation", Mesa.readthedocs.io, 2021. [Online]. Available: https://mesa.readthedocs.io/en/stable/index.html. [Accessed: 03- Feb- 2021].
Copyright 2020 Core Mesa Team

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
