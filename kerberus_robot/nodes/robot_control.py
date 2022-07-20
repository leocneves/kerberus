#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros
from std_msgs.msg import String
import time
from geometry_msgs.msg import Twist

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
            self.got = False

    def execute(self, data):
        global pub_sound
        rospy.loginfo('Executing state startTalk')
        t1 = time.time()
        while (time.time() - t1) <= 60 * 3:
            if self.got:
                self.got = False
                pub_sound.publish(", Yes")
                return 'finished'
        pub_sound.publish(", Is anyone there?")
        return 'failed'

# define state Bar
class Action(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['finished', 'failed'])
        self.got = False

        self.subscriber = rospy.Subscriber('/speech_recognition/final_result', String, self.callback)

        self.actions = ['walk forward', 'turn right', 'turn left', 'walk backwards']

    def execute(self, userdata):
        global pub_sound, velocity_publisher

        rospy.loginfo('Executing state Action')

        vel_msg = Twist()
        t1 = time.time()

        # Waiting for action up to
        while ((time.time() - t1) <= 10) or self.got:
            if self.got:
                ############## ACTIONS ##################
                pub_sound.publish(", ok")

                c = time.time()
                n = 3
                if self.data == 'walk forward':
                    vel_msg.linear.x = 1.0
                    vel_msg.angular.z = 0.0
                    while (time.time() - c) < n:
                        velocity_publisher.publish(vel)
                elif self.data == 'walk backwards':
                    vel_msg.linear.x = -1.0
                    vel_msg.angular.z = 0.0
                    while (time.time() - c) < n:
                        velocity_publisher.publish(vel)
                elif self.data == 'turn right':
                    vel_msg.linear.x = 0.0
                    vel_msg.angular.z = 1.0
                    while (time.time() - c) < n:
                        velocity_publisher.publish(vel)
                elif self.data == 'turn left':
                    vel_msg.linear.x = 0.0
                    vel_msg.angular.z = -1.0
                    while (time.time() - c) < n:
                        velocity_publisher.publish(vel)


                vel_msg.linear.x = 0.0
                vel_msg.angular.z = 0.0
                velocity_publisher.publish(vel)


                self.got = False
                return 'finished'
        pub_sound.publish(", Sorry, I don't understand")
        return 'failed'


    def callback(self, data):
        self.data = data.data
        if data.data in self.actions:
            self.got = True
        else:
            self.got = False


def main():
    global pub_sound, velocity_publisher
    rospy.init_node('control_state_machine')

    pub_sound = rospy.Publisher('/tts/phrase', String, queue_size=1)
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['outcome4'])

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('ROBOT', StartTalk(),
                               transitions={'finished':'ACTION', 'failed':'ROBOT'})
        smach.StateMachine.add('ACTION', Action(),
                               transitions={'finished':'ROBOT', 'failed':'ROBOT'})

    # Execute SMACH plan
    pub_sound.publish(", I am alive")
    outcome = sm.execute()



if __name__ == '__main__':
    main()
