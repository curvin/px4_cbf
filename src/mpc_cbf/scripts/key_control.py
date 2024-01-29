"""
 * File: offb_node.py
 * Stack and tested in Gazebo Classic 9 SITL
"""

#! /usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, CommandBoolRequest, SetMode, SetModeRequest

import tty #导入tty模块,用于设置终端模式
import sys #导入系统模块
import termios #导入termios模块,用于保存和恢复终端属性
import select #导入select模块,用于实现输入监听

settings = termios.tcgetattr(sys.stdin) #获取标准输入终端属性

current_state = State()

def state_cb(msg):
    global current_state
    current_state = msg

def getKey():
    
    tty.setraw(sys.stdin.fileno()) #设置终端为原始模式
    
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1) 
    #监听标准输入,超时0.1秒  
    
    if rlist: #若监听到输入
        
        key = sys.stdin.read(1) 
        #读取一个字符
        
    else:
        
        key = '' #否则设置为空字符
        
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings) 
    #恢复标准输入终端属性
    
    return key #返回键盘输入内容


if __name__ == "__main__":
    rospy.init_node("offb_node_py")

    state_sub = rospy.Subscriber("mavros/state", State, callback = state_cb)

    local_pos_pub = rospy.Publisher("mavros/setpoint_position/local", PoseStamped, queue_size=10)

    rospy.wait_for_service("/mavros/cmd/arming")
    arming_client = rospy.ServiceProxy("mavros/cmd/arming", CommandBool)

    rospy.wait_for_service("/mavros/set_mode")
    set_mode_client = rospy.ServiceProxy("mavros/set_mode", SetMode)


    # Setpoint publishing MUST be faster than 2Hz
    rate = rospy.Rate(20)

    # Wait for Flight Controller connection
    while(not rospy.is_shutdown() and not current_state.connected):
        rate.sleep()

    pose = PoseStamped()

    pose.pose.position.x = 0
    pose.pose.position.y = 0
    pose.pose.position.z = 2

    # Send a few setpoints before starting
    for i in range(100):
        if(rospy.is_shutdown()):
            break

        local_pos_pub.publish(pose)
        rate.sleep()

    offb_set_mode = SetModeRequest()
    offb_set_mode.custom_mode = 'OFFBOARD'

    arm_cmd = CommandBoolRequest()
    arm_cmd.value = True

    last_req = rospy.Time.now()

    while(not rospy.is_shutdown()):
        if(current_state.mode != "OFFBOARD" and (rospy.Time.now() - last_req) > rospy.Duration(5.0)):
            if(set_mode_client.call(offb_set_mode).mode_sent == True):
                rospy.loginfo("OFFBOARD enabled")

            last_req = rospy.Time.now()
        else:
            if(not current_state.armed and (rospy.Time.now() - last_req) > rospy.Duration(5.0)):
                if(arming_client.call(arm_cmd).success == True):
                    rospy.loginfo("Vehicle armed")

                last_req = rospy.Time.now()
        key=0
        key = getKey()
        if(key == 'w'):
            pose.pose.position.x = pose.pose.position.x + 0.1
        if(key == 's'):
            pose.pose.position.x = pose.pose.position.x - 0.1
        if(key == 'a'):
            pose.pose.position.y = pose.pose.position.y + 0.1
        if(key == 'd'):
            pose.pose.position.y = pose.pose.position.y - 0.1
        if(key == 'j'):
            pose.pose.position.z = pose.pose.position.z + 0.1
        if(key == 'l'):
            pose.pose.position.z = pose.pose.position.z - 0.1
        if key == 'q':
            break
            

        local_pos_pub.publish(pose)

        rate.sleep()
