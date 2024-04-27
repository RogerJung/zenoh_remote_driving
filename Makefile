build_project:
	colcon build --symlink-install --packages-select \
		remote_control \
		remote_lidar \
		g923_control
