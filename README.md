# Information cascade game in oTree

The experiment is designed along the same line as the classic infomration cascade
experiment by [Anderson and Holt (2008)](#myfootnote1).
See a general description of what the information cascade in [this wiki article](https://en.wikipedia.org/wiki/Information_cascade).

The main feature of any cascade game is that the decisions are taken sequentially.
The player takes the decision, and then the next one has in addition to other information
the information of the decision of a previous player (or all or some previuos players).

The main technical issue here is that only one person in a moment of time
should take the decision while the others should wait. As soon as s/he takes the decision,
and leaves the page where the decision is made, another player is allowed to access
the page, while all others are waiting for him. Etc.

The way we did it is by using channels and a custom-made Waiting Page.
The subsession-level field `room_busy` serves as a block to prevent access to `Choose.html`
(which is our decision page) by more than one player at a time.

As soon as a player accesses the page, the `subsession.room_busy` is set to `True`
and everyone else waits in a previous `WaitingRoom` page.

Right after the player takes the decision, in `before_next_page` method, we unblock
the `room_busy`. After than we collect all the channels of individual players who wait
in the `WaitingRoom` and we send a signal to **only one of them**. This player
is forwarded to the decision page, it blocks the room, and the cycle repeats.

## Technical issues to take into account before using in mTurk

This code is deliberately left as simple as possible. However if you'd like to
run a full-scale online experiment using it, you should have two things in mind.

1. The background logic of what's going now is the
following: the guy enters the Choose room and the room is blocked for new  arrivals until he leaves it. Everyone else waits in a Waiting Room. When he clicks 'Next' the room is unblocked, the code gathers all the channels of those waiting in the Waiting Room, and sends a signal to one of them forwarding him/her to the Choose room. The room is blocked again. And so on.

    However if in those milliseconds (or even seconds if connection is slow) between receiving a signal and being forwarded from the Waiting Room to the Choose room the guy leaves the experiment (or his connection is lost), then all the rest of those poor things waiting in the Waiting Room are stuck there for good. If you'd like to
    keep your mTurk reputation high, it is crucial to guarantee that this never happens.

    Thus, we need a background process that would check at the server side every n
    seconds that the Choose room is not empty, and if it is empty,
    it will pick someone from the waiting room and forward him there.
    One of the way to do it is by using any cronjob packages available for Django, like
    Celery or Huey. We personally used [Django-background-tasks](http://django-background-tasks.readthedocs.io/).

2. Second issue is really small and can be ignored, but still it's nice to have it in mind. If someone would really like to avoid waiting in the Waiting room, he or she can open now a Javascript console (available in most of modern browsers) and can type in there `$('.form').submit();`. and he will be forwarded to the decision page even if the Choose room is blocked. There will be many who would like to do it, but still it makes sense to block this kind of behaviour.




<a name="fn1">1</a>: Anderson, L. R.
and C. A. Holt (2008). "Information cascade experiments." Handbook of
Experimental Economics Results 1: 335-343.
