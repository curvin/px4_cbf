import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry


if __name__ == "__main__":
    #2.初始化 ROS 节点:命名(唯一)
    rospy.init_node("vins_extrinsic_sim")
    #3.实例化 发布者 对象
    pub = rospy.Publisher("/vins_fusion/extrinsic",Odometry,queue_size=10)
    #4.组织被发布的数据，并编写逻辑发布数据
    vins_extrinsic = Odometry()
    vins_extrinsic.header.frame_id = "world"
    
    vins_extrinsic.header.seq=1
    # 设置循环频率
    rate = rospy.Rate(15)
    while not rospy.is_shutdown():
        
        vins_extrinsic.header.stamp=rospy.Time.now()
        
        vins_extrinsic.pose.pose.position.x = 0
        vins_extrinsic.pose.pose.position.y = 0
        vins_extrinsic.pose.pose.position.z = 0

        vins_extrinsic.pose.pose.orientation.w = -0.5
        vins_extrinsic.pose.pose.orientation.x =  0.5
        vins_extrinsic.pose.pose.orientation.y = -0.5
        vins_extrinsic.pose.pose.orientation.z =  0.5

        pub.publish(vins_extrinsic)
        rate.sleep()
   
       
