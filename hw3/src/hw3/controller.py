#! /usr/bin/python2

import math
import rospy
import time
from rospy import Publisher, Subscriber
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

DIST_THRESHOLD = 0.1
VELOCITY = 1


def get_angle(pos1, pos2):
    return math.atan2(pos2.y - pos1.y, pos2.x - pos1.x)
    
def get_dist(pos1, pos2):
    return ((pos2.x - pos1.x) ** 2 + (pos2.y - pos1.y) ** 2) ** 0.5


class Controller:
    def __init__(self):
        self.subscriber_turtle1 = Subscriber('/turtle1/pose', Pose, self.update_pos1)
        self.pos1 = Pose()
        self.subscriber_turtle2 = Subscriber('/turtle2/pose', Pose, self.update_pos2)
        self.pos2 = Pose()
        self.publisher = Publisher('/turtle2/cmd_vel', Twist, queue_size=10)
        
    def update_pos1(self, pos):
    	self.pos1 = pos
    	self.move_turtle2()
    	
    def update_pos2(self, pos):
    	self.pos2 = pos
        
    def move_turtle2(self):
        dist  =  get_dist(self.pos2, self.pos1)
        angle = get_angle(self.pos2, self.pos1) - self.pos2.theta
        
        while angle > math.pi:
            angle -= 2. * math.pi
        while angle < - math.pi:
            angle += 2. * math.pi
            
        twist = Twist()
        twist.linear.x = 0
        twist.angular.z = 0
        
        if dist > DIST_THRESHOLD:
            twist.linear.x = min(dist, VELOCITY)
            twist.angular.z = angle
        self.publisher.publish(twist)
      
        
if __name__ == '__main__':
    rospy.init_node("controller")
    Controller()
    rospy.spin()
