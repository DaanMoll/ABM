## ABM - the performance of traffic flow with MESA

This traffic model is built with MESA package with python. We simulate the movement of cars on a road network in a grid model, traffic lights were placed at each intersection and the cars will stop when the traffic light turns red. The pathway is random. 

# How to use:

A simulation is under abm_project folder.

There are four parameters in our model that can be adjusted: 
- maximum number of cars
- traffic light duration
- maximum speed
- tolerance level 

# What to expect:

The simulation shows the average congestion level and the haste level, the more cars being put into the simulation, the likely it will get a high congestion. THis may cause a gridlock, where the cars are not able to move anymore.


# References:
MESA: Grimm, Volker, Eloy Revilla, Uta Berger, Florian Jeltsch, Wolf M. Mooij, Steven F. Railsback, Hans-Hermann Thulke, Jacob Weiner, Thorsten Wiegand, and Donald L. DeAngelis. 2005. “Pattern-Oriented Modeling of Agent Based Complex Systems: Lessons from Ecology.” American Association for the Advancement of Science 310 (5750): 987–91. doi:10.1126/science.1116681.

Hunt, Andrew, and David Thomas. 2010. The Pragmatic Progammer: From Journeyman to Master. Reading, Massachusetts: Addison-Wesley.

Leek, Jeffrey T., and Roger D. Peng. 2015. “Reproducible Research Can Still Be Wrong: Adopting a Prevention Approach.” Proceedings of the National Academy of Sciences 112 (6): 1645–46. doi:10.1073/pnas.1421412111.
