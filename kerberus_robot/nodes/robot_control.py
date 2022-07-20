#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros
from std_msgs.msg import String
import time

# define state startTalk
class StartTalk(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['finished', 'failed'])
        self.got = False

        self.subscriber = rospy.Subscriber('/speech_recognition/final_result', String, self.callback)

    def callback(self, data):
        if data.data == 'robot':
            self.got = True
        else:
            self.got = True

    def execute(self, data):
        global pub_sound
        rospy.loginfo('Executing state startTalk')
        t1 = time.time()
        while (time.time() - t1) <= 60:
            if self.got:
                pub_sound.publish("Yes")
                return 'finished'
        return 'failed'

# define state Bar
class Test(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['finished'])

    def execute(self, userdata):
        global pub_sound
        rospy.loginfo('Executing state TEST')
        time.sleep(2)
        pub_sound.publish("Nice, I can hear you very well Leonardo")

        return 'finished'





def main():
    global pub_sound
    rospy.init_node('control_state_machine')

    pub_sound = rospy.Publisher('/tts/phrase', String, queue_size=10)

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['outcome4'])
    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('ROBOT', StartTalk(),
                               transitions={'finished':'TEST', 'failed':'ROBOT'})
        smach.StateMachine.add('TEST', Test(),
                               transitions={'finished':'ROBOT'})

    # Execute SMACH plan
    outcome = sm.execute()



if __name__ == '__main__':
    main()
