cd /home/yang/
cd inference_test
make -j8
cd intel64/Release

./crossroad_camera_demo -i1 /home/yang/Documents/Dataset/Image_subsets/input -i /home/yang/Documents/Dataset/Image_subsets/input2 -m /home/yang/intel/computer_vision_sdk_2018.4.420/deployment_tools/intel_models/person-vehicle-bike-detection-crossroad-0078/FP32/person-vehicle-bike-detection-crossroad-0078.xml -m_pa /home/yang/intel/computer_vision_sdk_2018.4.420/deployment_tools/intel_models/person-attributes-recognition-crossroad-0031/FP32/person-attributes-recognition-crossroad-0031.xml -m_reid /home/yang/intel/computer_vision_sdk_2018.4.420/deployment_tools/intel_models/person-reidentification-retail-0079/FP32/person-reidentification-retail-0079.xml -d CPU -o1 /home/yang/Documents/crossroad_camera/Result -o2 /home/yang/Documents/crossroad_camera/Result
