build_project:
	colcon build --symlink-install --packages-select \
		remote_control \
		remote_lidar \
		g923_control


build_proxy:
	cd src/ffmpeg/ && g++ proxy.cpp -o proxy
