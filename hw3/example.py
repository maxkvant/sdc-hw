#! /usr/bin/python
import rospy
from turtlesim.msg import Color rospy.init_node('turtle_color_blue') pub=rospy.Publisher('/turtle1/color_sensor',
Color,
queue_size=10) msg=Color(r=0,g=0,b=255)
rospy.loginfo(“published message %s”, msg) pub.publish(msg)
