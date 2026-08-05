cmake_minimum_required(VERSION 3.11)
project(husarion_navigation)

find_package(ament_cmake REQUIRED)

install(DIRECTORY config launch maps rviz DESTINATION share/${PROJECT_NAME})

ament_package()
