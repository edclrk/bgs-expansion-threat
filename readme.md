A little requirements gathering if we wanted a process to check our "expansion threat"
For a given system (i.e. Negrito)
Get All Systems within designated LY from the designated system
For each  of those systems, check all factions
If a faction is above X INF (e.g. 50%), report them as a threat...

That's all that's really needed right?
Ed LaveYesterday at 1:06 AM
If a faction is above ‘x’ % AND the first system they would expand to is Negrito. 

If the ly range is now 30ly that’s a huge number of systems to check (50+) and they’d all need to be checked every couple of days. Plus Inara only goes up to 22 ish ly. Even then that’s a lot of systems and all to easy to say ‘i’ll check tomorrow’.
KamogYesterday at 6:50 AM
good point on the 1st system, could be some edge cases.  Looking at EDSM API, looks pretty straightforward, so I figure I'll see if I can put that together, then maybe figure out discord bots...




Getting systems within cube of named system:
https://www.edsm.net/api-v1/cube-systems?systemName=exioce&size=30&showInformation=1&showCoordinates=1&showId=1

Getting factions within system:
https://www.edsm.net/api-system-v1/factions?systemName=Exioce



Requests library:
http://docs.python-requests.org/en/latest/
