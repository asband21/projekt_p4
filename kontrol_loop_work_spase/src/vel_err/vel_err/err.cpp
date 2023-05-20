#include <iostream>
#include <cmath>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include "std_msgs/msg/float32_multi_array.hpp"
#include "std_msgs/msg/header.hpp"
#include "tf2_msgs/msg/tf_message.hpp"
#include "tf2_ros/buffer.h"
#include "tf2_ros/transform_listener.h"
#include "custom_interface/msg/vicon_info.hpp"

class FrameListener : public rclcpp::Node
{
public:
	explicit FrameListener()
	: Node("oel")
	{
		subscription_ = this->create_subscription<tf2_msgs::msg::TFMessage>(
			"/tf", 10,
			std::bind(&FrameListener::on_timer, this, std::placeholders::_1));

		publisher_ = this->create_publisher<std_msgs::msg::Float32MultiArray>("drone_error", 10);
		pub_ = this->create_publisher<custom_interface::msg::ViconInfo>("vicon_info", 10);

		target_frame_ = this->declare_parameter("vicon", "Drone").get_value<std::string>();

		gammel_tf_ = nullptr;
		tf_buffer_ = std::make_shared<tf2_ros::Buffer>(this->get_clock());
		tf_listener_ = std::make_shared<tf2_ros::TransformListener>(*tf_buffer_, this);

		RCLCPP_INFO(this->get_logger(), "err node start");
	}

	double quat2yor(double x, double y, double z, double w)
	{
		return std::atan2(w * w + x * x - y * y - z * z, 2.0 * (x * y + w * z));
	}

	void on_timer(const tf2_msgs::msg::TFMessage::SharedPtr msg)
	{
		if (gammel_tf_ == nullptr)
		{
			gammel_tf_ = std::make_shared<tf2_msgs::msg::TFMessage>(*msg);
			for (auto& tra : gammel_tf_->transforms)
			{
				if (tra.child_frame_id == "Drone" || tra.child_frame_id == "drone")
				{
					tra.transform.translation.x += 1;
				}
			}
			return;
		}

		std::vector<float> vec(9, 0.0);
		rclcpp::Time del_tid;
		for (const auto& tra : msg->transforms)
		{
			if ((tra.child_frame_id == "Drone" || tra.child_frame_id == "drone") && tra.header.frame_id == "vicon")
			{
				vec[0] = tra.transform.translation.x;
				vec[1] = tra.transform.translation.y;
				vec[2] = tra.transform.translation.z;
				vec[3] = quat2yor(tra.transform.rotation.x, tra.transform.rotation.y, tra.transform.rotation.z, tra.transform.rotation.w);
				del_tid = tra.header.stamp;
				if (del_tid == rclcpp::Time(0, 0, RCL_ROS_TIME))
				{
					RCLCPP_INFO(this->get_logger(), "teamp = 0");
				}
			}
		}

		if (gammel_tf_ != nullptr)
		{
			for (const auto& tra : gammel_tf_->transforms)
			{
				if ((tra.child_frame_id == "Drone" || tra.child_frame_id == "drone") && tra.header.frame_id == "vicon")
				{
					if (del_tid != rclcpp::Time(0, 0, RCL_ROS_TIME))
					{
						rclcpp::Duration del_time = del_tid - tra.header.stamp;
						vec[4] = (vec[0] - tra.transform.translation.x) / del_time.seconds();
						vec[5] = (vec[1] - tra.transform.translation.y) / del_time.seconds();
						vec[6] = (vec[2] - tra.transform.translation.z) / del_time.seconds();
						vec[7] = (vec[3] - quat2yor(tra.transform.rotation.x, tra.transform.rotation.y, tra.transform.rotation.z, tra.transform.rotation.w)) / del_time.seconds();
						vec[8] = del_time.nanoseconds();
						for (size_t i = 0; i < 8; ++i)
						{
							if (vec[i] > 2)
							{
								vec[i] = 1;
							}
						}
						// formatted_vector = [f"{value:8.5f}" for value in vec]
						// self.get_logger().info(f"vec: {formatted_vector}")
						gammel_tf_ = std::make_shared<tf2_msgs::msg::TFMessage>(*msg);
						callback(vec);
					}
				}
			}
		}
	}

	void callback(const std::vector<float>& array)
	{
		std_msgs::msg::Float32MultiArray msg;
		msg.data = array;
		publisher_->publish(msg);
	}

private:
	rclcpp::Subscription<tf2_msgs::msg::TFMessage>::SharedPtr subscription_;
	rclcpp::Publisher<std_msgs::msg::Float32MultiArray>::SharedPtr publisher_;
	rclcpp::Publisher<custom_interface::msg::ViconInfo>::SharedPtr pub_;

	std::string target_frame_;
	std::shared_ptr<tf2_msgs::msg::TFMessage> gammel_tf_;
	std::shared_ptr<tf2_ros::Buffer> tf_buffer_;
	std::shared_ptr<tf2_ros::TransformListener> tf_listener_;
};

int main(int argc, char** argv)
{
	rclcpp::init(argc, argv);
	rclcpp::spin(std::make_shared<FrameListener>());
	rclcpp::shutdown();
	return 0;
}

