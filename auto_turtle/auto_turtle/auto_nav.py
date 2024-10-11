import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class AutoNav(Node):

    def __init__(self):
        super().__init__('auto_navigation')
        self.pose_sub=self.create_subscription(Pose,'/turtle1/pose',self.pose_teller,1)
        self.velo_publisher= self.create_publisher(Twist, '/turtle1/cmd_vel', 1)
        self.timer = self.create_timer(0.1, self.velo_calc)
        self.get_logger().info("Autonomous Navigation Node is Started")
        
        self.flag=True
        self.curr_x=Pose().x
        self.curr_y=Pose().y
        self.curr_ang=Pose().theta
        self.fin_x=self.curr_x
        self.fin_y=self.curr_y

    def pose_teller(self,msg: Pose):
        self.curr_x=msg.x
        self.curr_y=msg.y
        self.curr_ang=msg.theta
        print("Current X",self.curr_x)
        print("Current Y",self.curr_y)
        # if self.curr_ang<0:
        #     self.curr_ang=(2*math.pi)+self.curr_ang
        if(self.flag):
            self.fin_x=self.curr_x
            self.fin_y=self.curr_y
            self.flag=False
        
    def velo_calc(self):
        vel=Twist()
        dist=math.sqrt(((self.curr_x-float(self.fin_x))**2) + ((self.curr_y-float(self.fin_y))**2))
        print("Distance from goal",dist)
        if ((self.fin_x==self.curr_x and self.fin_y==self.curr_y) or dist<0.08):
            if(dist>0):
                self.get_logger().info("TURTLE REACHED GOAL POSE")
            key1=input("Enter x value ")
            key2=input("Enter y value ")
            if key1 in '0123456789.':
                self.fin_x=key1
            else:
                self.fin_x=self.curr_x
                self.get_logger().error("Entered value is not valid")

            if key2 in '1234567890.':
                self.fin_y=key2
            else:
                self.fin_y=self.curr_y
                self.get_logger().error("Entered value is not valid")
            
        dist=math.sqrt(((self.curr_x-float(self.fin_x))**2) + ((self.curr_y-float(self.fin_y))**2))
        # print("2nd",dist)
        fin_ang=math.atan2((int(self.fin_y)-self.curr_y),(int(self.fin_x)-self.curr_x))
        # if fin_ang<0:
        #     fin_ang=(2*math.pi) + fin_ang
        angle=fin_ang-self.curr_ang

        if angle>0.2:
            vel.angular.z=1.0
        elif angle<-0.2:
            vel.angular.z=-1.0
        else:
            vel.angular.z=0.0
            # print(dist)
            if dist<0.08:
                vel.linear.x=0.0
            elif dist>0.08:
                vel.linear.x=1.0
        # print(dist)
        self.velo_publisher.publish(vel)

def main(args=None):
    rclpy.init(args=args)
    auto_nav = AutoNav()
    rclpy.spin(auto_nav)
    rclpy.shutdown()


if __name__ == '__main__':
    main()