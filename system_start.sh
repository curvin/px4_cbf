#!/bin/bash

# 启动px4仿真
gnome-terminal --title="PX4_Sim" -- bash -c 'source ~/.bashrc; roslaunch mpc_cbf uav_sim.launch; $SHELL'
sleep 5s

# 启动egp planner
gnome-terminal --title="egp_planner" -- bash -c 'source ~/.bashrc;cd ~/Fast-Drone-250/; source ./devel/setup.bash; roslaunch ego_planner single_run_in_exp.launch;$SHELL'
sleep 3s

# 启动egp planner rviz
gnome-terminal --title="egp_rviz" -- bash -c 'source ~/.bashrc;cd ~/Fast-Drone-250/; source ./devel/setup.bash; roslaunch ego_planner rviz.launch;$SHELL'
sleep 3s

# 新建空闲窗口
gnome-terminal --title="egp_rviz" -- bash -c 'source ~/.bashrc;$SHELL'
sleep 3s
