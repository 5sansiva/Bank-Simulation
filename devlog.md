11:47 PM 4/6/2025
This is project 2 which will simulate a bank environemnt. There are three tellers and the bank opens when all are ready. This will simulate how an actual bank environemnt will be.
From my initial understanding, I can see that this project will consist of a single file but with multiple threads at work to represent each teller and the customer. The output should then consist of detailing a log of the interactions and such. For this project, I plan to use python3 and make sure my script also works on the cs1 servers in python3. I am still rather confused about this project but I feel it is to implement deadlock prevention along with mainly talk about concurrecy, or have multiple processes work at the same time but not necessarily at the same time, so like a bank for example. This initial commit just details my thoughts so far. I will start working on adding some initial methods and such to my project and such.

12:37 AM 4/7/2025
This session I did not do much but really understand what the project was about so I feel like I have a good starting point. Next session, I look to really start writing out the logic by expanding the given example file to really add in additional teller and customer threads and utilize semaphores to facilitate communication between them.

5:27 PM 4/10/2025
So far, I understand that this project one requires one file which stores the customer and teller threads along with using semaphores to control which customer would get access and such so that is what the project mainly consists of.
This session I plan to setup the overall program when it comes to flow and just start by setting up the customer and teller threads and just set the project up. So I will look at the example code and then look to adjust that and understand where semaphores come into the overall project and how it works with the threads.

6:31 PM 4/10/2025
During my session, I wrote down the inital program which initializes three teller threads and 10 customer threads and adjusted the output. I am mainly focusing on figuring out how the semaphores work with the threading module and figuring out the flow. I did not encounter any major problems during this session so it fine overall. I accomplished my goal of getting an initial understanding of the flow using threads and sempahores, now I need to add the additional features that were required on the project. Next session, I plan to add those features.

11:01 PM 4/11/2025
So far, I made an initial flow where there are three teller threads and ten customer threads just for a demo right now. This work session, I am going to focus on adding more functionality that fits the requirements on the pdf and see how much I can get done.

12:34 AM 4/12/2025
This past working session, I mainly focused on adjusting my code to have two classes, one for the customers and another for the tellers. This is because each one stores states so having them as classes instead of methods is easier. I didn't really encounter many problems this working session. Next session, I plan on going through the pdf more and seeing what else I need to add and just work through the project like normal.

11:38 AM 4/12/2025
I don't have any new thoughts that I haven't already written out in my previous session logs. This session, I plan to mainly finish up the teller classes along with maybe finishing up the customer class and further see how the flow is between the classes and such. That is what I plan on implementing in this session.

1:39 PM 4/12/2025
I was more productive this session. I was able to finish the teller class along with the customer class and adjust how the flow should be between the classes. I have to do some more testing to see if this is fine and I also have to test on the UTD servers to make sure this program runs on there. I did not encounter any major errors during this work session as the minute errors I had were more of how the teller messages were intertwined with the customer messages to start, like the customer enters before all three of the tellers were ready. I accomplished more this session because I initially only was going to finish the teller class but I ended up finishing both the teller and customer class for now. Next session is mainly testing, double checking with the pdf requirements and testing on the UTD servers.

10:37 PM 4/12/2025
From last session, I haven't had any new thoughts besides adjusting more of the outputs and such and make sure it flows properly. This session, I plan to do more testing and ensure my code outputs and runs properly and such. Beyond that, I do not have major confusions about the project because it is about the interaction between three threads for the tellers and 50 threads for the customers.

11:55 PM 4/12/2025
This session, I didn't really do much, I just reviewed my logic and made minor corrections to the output logic. Next session, I plan on testing on the cs1 server.

7:41PM 4/13/2025
I am going to finish working on the project during this session. I have already established the teller and customer classes so I will be testing on the cs1 server. Last project, I encountered issues on the server due to different versions of python so this time, I hope to ensure that those errors will not arise. I will do testing and ensure everything works smoothly, then I will upload to the server. I will document any errors that I have during my session.
