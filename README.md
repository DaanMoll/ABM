# ABM - the performance of traffic flow with MESA

This agent based traffic model is built using the MESA package in python. We simulate the movement of cars on a road network using a grid model. Cars drive random optimal paths, stopping when they are too close to other cars or when they encounter a red traffic light. Traffic lights were placed at each intersection. Aditionally, when a car experiences a high level of congestion (calculated as the ratio of its cumulative speed and maximum speed) it enters a *hasty* state, causing the agent to driver over the speed limit. The model output measured is the average congestion experienced by agents.

## How to use:

All simulation files are under the ```abm_project``` folder.

There are four parameters in our model that can be adjusted: 
- maximum number of cars
- traffic light duration
- maximum speed
- haste tolerance level

Executing ```run.py``` will open the simulation as a browser window, where the model parameters can be tweaked using sliders.

## What to expect:

The simulation shows the average congestion level and the haste level, the more cars being put into the simulation, the likely it will get a high congestion. This may cause a gridlock, where the cars are not able to move anymore.


## References:
MESA: Grimm, Volker, Eloy Revilla, Uta Berger, Florian Jeltsch, Wolf M. Mooij, Steven F. Railsback, Hans-Hermann Thulke, Jacob Weiner, Thorsten Wiegand, and Donald L. DeAngelis. 2005. “Pattern-Oriented Modeling of Agent Based Complex Systems: Lessons from Ecology.” American Association for the Advancement of Science 310 (5750): 987–91. doi:10.1126/science.1116681.

Hunt, Andrew, and David Thomas. 2010. The Pragmatic Progammer: From Journeyman to Master. Reading, Massachusetts: Addison-Wesley.

Leek, Jeffrey T., and Roger D. Peng. 2015. “Reproducible Research Can Still Be Wrong: Adopting a Prevention Approach.” Proceedings of the National Academy of Sciences 112 (6): 1645–46. doi:10.1073/pnas.1421412111.
