#!/usr/bin/env python3

import rospy
#from turtle_sim_proj.srv import *
from geometry_msgs.msg import Twist
import sys

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


def turtle_circle():
	rospy.init_node('turtlesim', anonymous=True)
	pub = rospy.Publisher('/turtle1/cmd_vel',
						Twist, queue_size=10)
	rate = rospy.Rate(10)
	vel = Twist()
	while not rospy.is_shutdown():
		vel.linear.x = 4
		vel.linear.y = 0
		vel.linear.z = 0
		vel.angular.x = 0
		vel.angular.y = 0
		vel.angular.z = 2
		#rospy.loginfo("Radius = %f",
		#			radius)
		pub.publish(vel)
		rate.sleep()

side_length=3
rotations=2
# Callback will create a publisher that publishes to the turtlesim
def handle_move_square():
	#print "I shall do your bidding"
	pub = rospy.Publisher('/turtle1/cmd_vel',Twist, queue_size = 10)
	vel_msg = Twist()


	current_rotation = 0
	while current_rotation < rotations:
		move_in_line(side_length,vel_msg,pub)
		rotate(vel_msg,pub)
		current_rotation+=0.25

def move_square_server():
	rospy.init_node('move_square_server',anonymous = True)
	s = rospy.Service( 'move_square', MoveSquare, handle_move_square )
	rospy.spin()


def move_in_line(side_length,vel_msg,pub):

	vel_msg.linear.x = 3
	vel_msg.linear.y = 0
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = 0

	t0 = rospy.Time.now().to_sec()
	distance_travelled = 0

	while distance_travelled < side_length:
		pub.publish(vel_msg)
		t1 = rospy.Time.now().to_sec()
		distance_travelled = speed*(t1-t0)

	vel_msg.linear.x = 0
	pub.publish(vel_msg)

def rotate(vel_msg,pub):
	angular_speed = 2
	vel_msg.angular.z = angular_speed
	t0	= rospy.Time.now().to_sec()
	angle_travelled = 0

	while ( angle_travelled < PI/2.0 ):
		pub.publish(vel_msg)
		t1 = rospy.Time.now().to_sec()
		angle_travelled = angular_speed*(t1-t0)

	vel_msg.angular.z = 0
	pub.publish(vel_msg)	


if __name__ == '__main__':
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connect((HOST,PORT))
			data = s.recv(1024)
			if (data == b'circle'):
				turtle_circle()
		#move_square_server()
	except rospy.ROSInterruptException:
		pass

