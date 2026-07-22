from ament_index_python.resources import has_resource

from launch.actions import DeclareLaunchArgument
from launch.launch_description import LaunchDescription
from launch.substitutions import LaunchConfiguration, PythonExpression

from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode


def generate_launch_description() -> LaunchDescription:
    """
    Generate a launch description with a camera node and visualiser.

    Returns
    -------
        LaunchDescription: the launch description

    """
    # parameters
    camera_param_name = "camera"
    camera_param_default = str(0)
    camera_param = LaunchConfiguration(
        camera_param_name,
        default=camera_param_default,
    )
    camera_launch_arg = DeclareLaunchArgument(
        camera_param_name,
        default_value=camera_param_default,
        description="camera ID or name"
    )

    role_param_name = "role"
    role_param_default = "raw"
    role_param = LaunchConfiguration(
        role_param_name,
        default=role_param_default,
    )
    role_launch_arg = DeclareLaunchArgument(
        role_param_name,
        default_value=role_param_default,
        description="stream role"
    )

    format_param_name = "format"
    format_param_default = str()
    format_param = LaunchConfiguration(
        format_param_name,
        default=format_param_default,
    )
    format_launch_arg = DeclareLaunchArgument(
        format_param_name,
        default_value=format_param_default,
        description="pixel format"
    )

    cam_info_url_param_name = "cam_info_url"
    cam_info_url_param_default = str()
    cam_info_url_param = LaunchConfiguration(
        cam_info_url_param_name,
        default=cam_info_url_param_default,
    )
    cam_info_url_launch_arg = DeclareLaunchArgument(
        cam_info_url_param_name,
        default_value=cam_info_url_param_default,
        description="Camera info URL"
    )

    frame_id_param_name = "frame_id"
    frame_id_param_default = str("raspi_camera")
    frame_id_param = LaunchConfiguration(
        frame_id_param_name,
        default=frame_id_param_default,
    )
    frame_id_launch_arg = DeclareLaunchArgument(
        frame_id_param_name,
        default_value=frame_id_param_default,
        description="frame ID for camera image"
    )

    swap_channels_param_name = "swap_red_blue"
    swap_channels_param_default = str(False)
    swap_channels_param = LaunchConfiguration(
        swap_channels_param_name,
        default=swap_channels_param_default,
    )
    swap_channels_launch_arg = DeclareLaunchArgument(
        swap_channels_param_name,
        default_value=swap_channels_param_default,
        description="swap red and blue channels"
    )

    software_rotation_param_name = "software_rotation"
    software_rotation_param_default = str(0)
    software_rotation_param = LaunchConfiguration(
        software_rotation_param_name,
        default=software_rotation_param_default,
    )
    software_rotation_launch_arg = DeclareLaunchArgument(
        software_rotation_param_name,
        default_value=software_rotation_param_default,
        description="software rotation angle"
    )

    # camera node
    FPS = 30
    fdl = int(1e6 / FPS)
    composable_nodes = [
        ComposableNode(
            package='camera_ros',
            plugin='camera::CameraNode',
            parameters=[{
                "camera": camera_param,
                "role": role_param,
                "width": 1280,
                "height": 1080,
                "format": format_param,
                "orientation": 0,
                "camera_info_url": cam_info_url_param,
                "frame_id": frame_id_param,
                "swap_red_blue": swap_channels_param,
                "software_rotation": software_rotation_param,
                "FrameDurationLimits": [fdl,fdl],
            }],
            extra_arguments=[{'use_intra_process_comms': True}],
            remappings=[
                ('/camera/image_raw', '/raspi_gscam/image_raw'),
                ('/camera/image_raw/compressed', '/raspi_gscam/image_raw/compressed'),
                ('/camera/camera_info', '/raspi_gscam/camera_info'),
            ],
        ),
    ]

    # optionally add ImageViewNode to show camera image
    # if has_resource("packages", "image_view"):
    #     composable_nodes += [
    #         ComposableNode(
    #             package='image_view',
    #             plugin='image_view::ImageViewNode',
    #             remappings=[('/image', '/camera/image_raw')],
    #             extra_arguments=[{'use_intra_process_comms': True}],
    #         ),
    #     ]

    # composable nodes in single container
    container = ComposableNodeContainer(
        name='camera_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=composable_nodes,
        arguments=['--ros-args', '--log-level', 'camera:=info'],
    )

    return LaunchDescription([
        container,
        camera_launch_arg,
        role_launch_arg,
        format_launch_arg,
        frame_id_launch_arg,
        swap_channels_launch_arg,
        software_rotation_launch_arg,
    ])
