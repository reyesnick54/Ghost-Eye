# GhostEye WiFi Sensing Repo Capability Scan

Generated from local vendored repositories.

## Awesome-WiFi-CSI-Sensing

### Top-level files
```text
LICENSE
README.md
```

### README preview
```text
[![GitHub](https://img.shields.io/github/license/Marsrocky/Awesome-WiFi-CSI-Sensing?color=blue)](https://github.com/Marsrocky/Awesome-WiFi-CSI-Sensing/blob/main/LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-YES-green.svg)](https://github.com/Marsrocky/Awesome-WiFi-CSI-Sensing/graphs/commit-activity)
![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)
[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

# Awesome WiFi Sensing
A list of awesome papers and cool resources on WiFi CSI sensing. Link to the *Github* if available is also present. 

*You are very welcome to suggest resources via pull requests*.

# Table of Contents
- [Benchmark](#benchmark)
- [Papers](#papers)
  - [Methods](#methods)
  - [Surveys](#surveys)
  - [Applications](#applications)
    - [Occupancy Detection](#occupancy-detection)
    - [Human Activity Recognition](#human-activity-recognition)
    - [Human Identification](#human-identification)
    - [Crowd Counting](#crowd-counting)
    - [Gesture Recognition](#gesture-recognition)
    - [Fall Detection](#fall-detection)
    - [Vital Sign Detection & Healthcare](#vital-sign-detection--healthcare)
    - [In-Car Activity Recognition](#in-car-activity-recognition)
    - [Pose Estimation](#pose-estimation)
    - [Indoor Localization](#indoor-localization)
    - [LLM+WiFi-CSI Sensing](#llmwifi-csi-sensing)
  - [Challenges for Real-World Large-Scale WiFi Sensing](#challenges-for-real-world-large-scale-wifi-sensing)
    - [IoT System Design](#iot-system-design)
    - [Efficiency and Security](#efficiency-and-security)
    - [Cross-Environment WiFi Sensing](#cross-environment-wifi-sensing)
    - [Multi-modal Sensing (WiFi+CV/Radar)](#multi-modal-sensing-wificvradar)
- [Platforms](#platforms)
  - [CSI Tool](#csi-tool)
- [Datasets](#datasets)
- [Libraries & Codes](#libraries--codes)
  - [Libraries](#libraries)
  - [Github Repositories](#github-repositories)
    - [From Papers](#from-papers)
    - [From Developers](#from-developers)
- [Book Chapter](#book-chapter)

# Benchmark
* [SenseFi: A Library and Benchmark on Deep-Learning-Empowered WiFi Human Sensing](https://arxiv.org/abs/2207.07859) | [[Github]](https://github.com/xyanchen/WiFi-CSI-Sensing-Benchmark) 
  <br>A comprehensive benchmarking for deep learning models in WiFi sensing.
  <br>***Highly Recommended as a Tutorial with Codes**

<!-- *********************************************************************** -->

# Papers

Papers are ordered by theme and inside each theme by publication date (submission date for arXiv papers).

## Methods
WiFi CSI sensing methods have enabled many applications, which can be divided into three categories:
* **Learning-based methods** learn the mapping functions from CSI data to the corresponding labels by [machine learning]() and deep learning.
* **Modeling-based methods** are based on physical theories like the [Fresnel Zone model](https://ieeexplore.ieee.org/abstract/document/8067692), or statistical models like the [Rician fading model](https://ieeexplore.ieee.org/abstract/document/9385792).
* **Hybrid methods** derive the strengths from learning-based and modeling-based methods.

## Surveys
* [Toward Integrated Sensing and Communications in IEEE 802.11bf Wi-Fi Networks](https://ieeexplore.ieee.org/document/10192291) | [[Github](https://github.com/francescamen/SHARPax)] IEEE Communications Magazine (2023)
* [WiFi Sensing with Channel State Information: A Survey](https://www.cs.wm.edu/~yma/files/WiFiSensing_YongsenMa_authorversion.pdf) ACM Computing Surveys (2019)
* [Device-Free WiFi Human Sensing: From Pattern-Based to Model-Based Approaches](https://ieeexplore.ieee.org/abstract/document/8067692) IEEE Communications Magazine (2017)
* [From RSSI to CSI: Indoor Localization via Channel Response](https://dl.acm.org/doi/abs/10.1145/2543581.2543592) ACM Computing Surveys (2013)

## Applications
### Occupancy Detection
* [Robust In-Car Child Presence Detection using Commercial WiFi](https://dl.acm.org/doi/abs/10.1145/3636534.3698864) Proceedings of the 30th Annual International Conference on Mobile Computing and Networking (MobiCom) (2024)
* [Time-Selective RNN for Device-Free Multiroom Human Presence Detection Using WiFi CSI](https://ieeexplore.ieee.org/abstract/document/10379149) IEEE Transactions on Instrumentation and Measurement (2024)
* [WiFi-enabled occupancy monitoring in smart buildings with a Self-Adaptive mechanism](https://dl.acm.org/doi/pdf/10.1145/3555776.3577841?casa_token=teWjknE1Pp4AAAAA:pMnmB2p_G4C7mMn54rUpdWSjyobwCJBWPqkI5jedzXNSN5_w6PEaj2OhpJ9Ronb99eZb9FsZHhc9bw) Proceedings of the 38th ACM/SIGAPP symposium on applied computing (2023)
* [A Machine Learning Approach to Passive Human Motion Detection Using WiFi Measurements From Commodity IoT Devices](https://ieeexplore.ieee.org/abstract/document/10122883?casa_token=PyKcBvHN-h0AAAAA:Wx_8OUuR4Ztqz9BQeORKqu5jVOIIIB0edW1IKl5HtUg7D_WjLjWwqGpm4ksD5EcWybCov8gAOA) IEEE Transactions on Instrumentation and Measurement (2023)
* [Intelligent Wi-Fi Based Child Presence Detection System](https://ieeexplore.ieee.org/document/9747420) IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP) (2022)
* [Machine Learning empowered Occupancy Sensing for Smart Buildings](https://s3.us-east-1.amazonaws.com/climate-change-ai/papers/icml2019/3/paper.pdf) IEEE ICML Climate Change Workshop (2019)
* [FreeDetector: Device-Free Occupancy Detection with Commodity WiFi](https://ieeexplore.ieee.org/abstract/document/8011040) IEEE International Conference on Sensing, Communication and Networking (SECON Workshops) (2017)

### Human Activity Recognition
* [Vision Transformers for Human Activity Recognition Using WiFi Channel State Information](https://ieeexplore.ieee.org/document/10477406) IEEE Internet of Things Journal (2024)
* [Exposing Data Leakage in Wi-Fi CSI-Based Human Action Recognition: A Critical Analysis](https://www.mdpi.com/2411-5134/9/4/90) Inventions (2024)
* [Critical Analysis of Data Leakage in WiFi CSI-Based Human Action Recognition Using CNNs](https://www.mdpi.com/1424-8220/24/10/3159) Sensors (2024)
* [SHARP: Environment and Person Independent Activity Recognition with Commodity IEEE 802.11 Access Points](https://ieeexplore.ieee.org/document/9804861) | [[Github](https://github.com/francescamen/SHARP)] IEEE Transactions on Mobile Computing (2023)
* [SiMWiSense: Simultaneous Multi-Subject Activity Classification Through Wi-Fi Signals](https://ieeexplore.ieee.org/document/10195411) (2023) | [[Github](https://github.com/kfoysalhaque/SiMWiSense)] IEEE 24th International Symposium on a World of Wireless, Mobile and Multimedia Networks (WoWMoM)
* [CSI-based location-independent Human Activity Recognition with parallel convolutional networks](https://www.sciencedirect.com/science/article/pii/S0140366422004157) Computer Communications (2023)
* [CSI-Based Location-Independent Human Activity Recognition Using Feature Fusion](https://ieeexplore.ieee.org/document/9926206) IEEE Transactions on Instrumentation and Measurement (2022)
* [Wi-Fi-Based Location-Independent Human Activity Recognition with Attention Mechanism Enhanced Method](https://www.mdpi.com/2079-9292/11/4/642/pdf) Electronics (2022)
* [Multimodal CSI-based Human Activity Recognition using GANs](https://ieeexplore.ieee.org/document/9431203) IEEE Internet of Things Journal (2021)
* [Two-Stream Convolution Augmented Transformer for Human Activity Recognition](https://ojs.aaai.org/index.php/AAAI/article/view/16103) | [[Github](https://github.com/windofshadow/THAT)] AAAI Conference on Artificial Intelligence (AAAI) (2021)
* [Improving WiFi-based Human Activity Recognition with Adaptive Initial State via One-shot Learning](https://ieeexplore.ieee.org/abstract/document/9417590) IEEE Wireless Communications and Networking Conference (2021)
* [Data Augmentation and Dense-LSTM for Human Activity Recognition Using WiFi Signal](https://ieeexplore.ieee.org/abstract/document/9205901) IEEE Internet of Things Journal (2021)
* [DeepSeg: Deep-Learning-Based Activity Segmentation Framework for Activity Recognition Using WiFi](https://ieeexplore.ieee.org/document/9235578) | [[Github]](https://github.com/ChunjingXiao/DeepSeg) IEEE Internet of Things Journal (2021)
* [Robust CSI-based Human Activity Recognition using Roaming Generator](https://ieeexplore.ieee.org/abstract/document/9305332) IEEE International Conference on Control and Automation (ICCA) (2020)
* [CsiGAN: Robust Channel State Information-Based Activity Recognition With GANs](https://ieeexplore.ieee.org/document/8808929) | [[Github]](https://github.com/ChunjingXiao/CsiGAN) IEEE Internet of Things Journal (2019)
* [BeSense: Leveraging WiFi Channel Data and Computational Intelligence for Behavior Analysis](https://ieeexplore.ieee.org/abstract/document/8870275) IEEE Computational Intelligence Magazine (2019)
* [WiFi CSI Based Passive Human Activity Recognition Using Attention Based BLSTM](https://ieeexplore.ieee.org/abstract/document/8514811) IEEE Transactions on Mobile Computing (2019)
* [Deep Learning Networks for Human Activity Recognition with CSI Correlation Feature Extraction](https://ieeexplore.ieee.org/abstract/document/8761445) IEEE International Conference on Communications (ICC) (2019)
* [Device-free Occupancy Sensing Platform using WiFi-enabled IoT Devices for Smart Homes](https://ieeexplore.ieee.org/abstract/document/8391737) IEEE Internet of Things Journal (2018)
* [DeepSense: Device-Free Human Activity Recognition via Autoencoder Long-Term Recurrent Convolutional Network](https://ieeexplore.ieee.org/abstract/document/8422895) IEEE International Conference on Communications (ICC) (2018)
* [CareFi: Sedentary Behavior Monitoring System via Commodity WiFi Infrastructures](https://ieeexplore.ieee.org/document/8354831) IEEE Transactions on Vehicular Technology (2018)
* [Towards Occupant Activity Driven Smart Buildings via WiFi-enabled IoT Devices and Deep Learning](https://www.sciencedirect.com/science/article/abs/pii/S037877881831329X) Energy and Building (2018)
* [Poster:WiFi-based Device-free Human Activity Recognition via Automatic Representation Learning](https://www.researchgate.net/publication/320222015_Poster_WiFi-based_Device-Free_Human_Activity_Recognition_via_Automatic_Representation_Learning) Annual International Conference on Mobile Computing, MOBICOM-17 (2017)
* [Understanding and Modeling of WiFi Signal Based Human Activity Recognition](https://dl.acm.org/doi/abs/10.1145/2789168.2790093) Annual International Conference on Mobile Computing (MOBICOM) (2017) 

### Human Identification
* [A Survey on WiFi-based Human Identification: Scenarios, Challenges, and Current Solutions](https://dl.acm.org/doi/abs/10.1145/3708323) ACM Transactions on Sensor Networks (2025)
* [A contactless authentication system based on WiFi CSI](https://dl.acm.org/doi/full/10.1145/3532095) ACM Transactions on Sensor Networks (2023) 
* [CAUTION: A Robust WiFi-based Human Authentication System via Few-shot Open-set Gait Recognition](https://ieeexplore.ieee.org/abstract/document/9726794/) IEEE Internet of Things Journal (2022)
* [WiONE: One-Shot Learning for Environment-Robust Device-Free User Authentication via Commodity Wi-Fi in Man–Machine System](https://ieeexplore.ieee.org/abstract/document/9385792) IEEE Transactions on Computational Social Systems (2021)
* [Gate-ID: WiFi-based human identification irrespective of walking directions in smart home](https://ieeexplore.ieee.org/abstract/document/9272621) IEEE Internet of Things Journal (2020)
* [Wifi-based Human Identification via Convex Tensor Shapelet Learning](https://ojs.aaai.org/index.php/AAAI/article/view/11497) AAAI Conference on Artificial Intelligence AAAI-18 (2018)
* [NeuralWave: Gait-Based User Identification Through Commodity WiFi and Deep Learning](https://ieeexplore.ieee.org/document/8591820) | [[Github]](https://github.com/kdkalvik/WiFi-user-recognition) Annual Conference of the IEEE Industrial Electronics Society (IECON) (2018)
* [Non-Intrusive Biometric Identification for Personalized Computing Using Wireless Big Data](https://ieeexplore.ieee.org/document/8560141) | [[Github]](https://github.com/mobinets/wifiwalker) IEEE SmartWorld, Ubiquitous Intelligence & Computing, Advanced & Trusted Computing, Scalable Computing & Communications, Cloud & Big Data Computing, Internet of People and Smart City Innovation (2018)
* [WFID: Passive Device-free Human Identification Using WiFi Signal](https://dl.acm.org/doi/abs/10.1145/2994374.2994377) International Conference on Mobile and Ubiquitous Systems: Computing, Networking and Services (MOBIQUITOUS) (2016)
* [WiWho: WiFi-Based Person Identification in Smart Spaces](https://ieeexplore.ieee.org/abstract/document/7460727) ACM/IEEE International Conference on Information Processing in Sensor Networks (IPSN) (2016)
* [WiFi-ID: Human Identification Using WiFi Signal](https://ieeexplore.ieee.org/abstract/document/7536315) International Conference on Distributed Computing in Sensor Systems (DCOSS) (2016)
 
### Crowd Counting
* [BeamCount: Indoor Crowd Counting Using Wi-Fi Beamforming Feedback Information](https://dl.acm.org/doi/abs/10.1145/3641512.3686361) Proceedings of the Twenty-fifth International Symposium on Theory, Algorithmic Foundations, and Protocol Design for Mobile Networks and Mobile Computing (MobiHoc) (2024)
* [CSI-based Passenger Counting on Public Transport Vehicles with Multiple Transceivers](https://ieeexplore.ieee.org/abstract/document/10571130) IEEE Wireless Communications and Networking Conference (WCNC) (2024)
* [Pa-count: passenger counting in vehicles using wi-fi signals](https://ieeexplore.ieee.org/abstract/document/10089148) IEEE Transactions on Mobile Computing (2023)
* [Passive People Counting using Commodity WiFi](https://ieeexplore.ieee.org/document/9221456) IEEE 6th World Forum on Internet of Things (WF-IoT) (2020)
* [Device-free Occupancy Detection and Crowd Counting in Smart Buildings with WiFi-enabled IoT](https://www.sciencedirect.com/science/article/abs/pii/S0378778817339336) Energy and Building (2018)
```

### Dependency indicators
```text
```

### Capability keyword hits
```text
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:1:[![GitHub](https://img.shields.io/github/license/Marsrocky/Awesome-WiFi-CSI-Sensing?color=blue)](https://github.com/Marsrocky/Awesome-WiFi-CSI-Sensing/blob/main/LICENSE)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:2:[![Maintenance](https://img.shields.io/badge/Maintained%3F-YES-green.svg)](https://github.com/Marsrocky/Awesome-WiFi-CSI-Sensing/graphs/commit-activity)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:7:A list of awesome papers and cool resources on WiFi CSI sensing. Link to the *Github* if available is also present. 
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:22:    - [Fall Detection](#fall-detection)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:25:    - [Pose Estimation](#pose-estimation)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:27:    - [LLM+WiFi-CSI Sensing](#llmwifi-csi-sensing)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:32:    - [Multi-modal Sensing (WiFi+CV/Radar)](#multi-modal-sensing-wificvradar)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:34:  - [CSI Tool](#csi-tool)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:35:- [Datasets](#datasets)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:44:* [SenseFi: A Library and Benchmark on Deep-Learning-Empowered WiFi Human Sensing](https://arxiv.org/abs/2207.07859) | [[Github]](https://github.com/xyanchen/WiFi-CSI-Sensing-Benchmark) 
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:45:  <br>A comprehensive benchmarking for deep learning models in WiFi sensing.
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:55:WiFi CSI sensing methods have enabled many applications, which can be divided into three categories:
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:56:* **Learning-based methods** learn the mapping functions from CSI data to the corresponding labels by [machine learning]() and deep learning.
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:57:* **Modeling-based methods** are based on physical theories like the [Fresnel Zone model](https://ieeexplore.ieee.org/abstract/document/8067692), or statistical models like the [Rician fading model](https://ieeexplore.ieee.org/abstract/document/9385792).
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:58:* **Hybrid methods** derive the strengths from learning-based and modeling-based methods.
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:64:* [From RSSI to CSI: Indoor Localization via Channel Response](https://dl.acm.org/doi/abs/10.1145/2543581.2543592) ACM Computing Surveys (2013)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:69:* [Time-Selective RNN for Device-Free Multiroom Human Presence Detection Using WiFi CSI](https://ieeexplore.ieee.org/abstract/document/10379149) IEEE Transactions on Instrumentation and Measurement (2024)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:78:* [Exposing Data Leakage in Wi-Fi CSI-Based Human Action Recognition: A Critical Analysis](https://www.mdpi.com/2411-5134/9/4/90) Inventions (2024)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:79:* [Critical Analysis of Data Leakage in WiFi CSI-Based Human Action Recognition Using CNNs](https://www.mdpi.com/1424-8220/24/10/3159) Sensors (2024)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:82:* [CSI-based location-independent Human Activity Recognition with parallel convolutional networks](https://www.sciencedirect.com/science/article/pii/S0140366422004157) Computer Communications (2023)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:83:* [CSI-Based Location-Independent Human Activity Recognition Using Feature Fusion](https://ieeexplore.ieee.org/document/9926206) IEEE Transactions on Instrumentation and Measurement (2022)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:85:* [Multimodal CSI-based Human Activity Recognition using GANs](https://ieeexplore.ieee.org/document/9431203) IEEE Internet of Things Journal (2021)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:90:* [Robust CSI-based Human Activity Recognition using Roaming Generator](https://ieeexplore.ieee.org/abstract/document/9305332) IEEE International Conference on Control and Automation (ICCA) (2020)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:93:* [WiFi CSI Based Passive Human Activity Recognition Using Attention Based BLSTM](https://ieeexplore.ieee.org/abstract/document/8514811) IEEE Transactions on Mobile Computing (2019)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:94:* [Deep Learning Networks for Human Activity Recognition with CSI Correlation Feature Extraction](https://ieeexplore.ieee.org/abstract/document/8761445) IEEE International Conference on Communications (ICC) (2019)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:104:* [A contactless authentication system based on WiFi CSI](https://dl.acm.org/doi/full/10.1145/3532095) ACM Transactions on Sensor Networks (2023) 
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:117:* [CSI-based Passenger Counting on Public Transport Vehicles with Multiple Transceivers](https://ieeexplore.ieee.org/abstract/document/10571130) IEEE Wireless Communications and Networking Conference (WCNC) (2024)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:139:* [TCS-Fall: Cross-individual fall detection system based on channel state information and time-continuous stack method](https://journals.sagepub.com/doi/full/10.1177/20552076241259047) | [[Github]](https://github.com/zhouziyu2050/pyQT-CSITool) Digital Health (2024)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:158:* [CARIN: Wireless CSI-based Driver Activity Recognition under the Interference of Passengers](https://dl.acm.org/doi/abs/10.1145/3380992) ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies (2020)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:160:* [WiDriver: Driver Activity Recognition System Based on WiFi CSI](https://link.springer.com/article/10.1007/s10776-018-0389-0) International Journal of Wireless Information Networks (2018)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:164:* [Adapose: Towards cross-site device-free human pose estimation with commodity wifi](https://arxiv.org/pdf/2309.16964) IEEE Internet of Things Journal (2024)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:168:* [Towards 3D human pose construction using wifi](https://dl.acm.org/doi/abs/10.1145/3372224.3380900) Annual International Conference on Mobile Computing and Networking (MOBICOM) (2020)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:173:* [Passive Indoor Localization Based on CSI and Naive Bayes Classification](https://ieeexplore.ieee.org/abstract/document/7902212) IEEE Transactions on Systems, Man, and Cybernetics: Systems (2018)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:174:* [CSI-Based Fingerprinting for Indoor Localization: A Deep Learning Approach](https://ieeexplore.ieee.org/abstract/document/7438932) IEEE Transactions on Vehicular Technology (2017)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:175:* [CSI-Based Indoor Localization](https://ieeexplore.ieee.org/abstract/document/6244790) IEEE Transactions on Parallel and Distributed Systems (2013)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:177:### LLM+WiFi-CSI Sensing
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:187:* [EfficientFi: Towards Large-Scale Lightweight WiFi Sensing via CSI Compression](https://ieeexplore.ieee.org/abstract/document/9667414) | [[Github]](https://github.com/Marsrocky/EfficientFi) IEEE Internet of Things Journal (2022) 
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:190:* [CSITime: Privacy-preserving human activity recognition using WiFi channel state information](https://www.sciencedirect.com/science/article/abs/pii/S0893608021004391) Neural Networks, (2022)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:193:* [An Experimental Study of CSI Management to Preserve Location Privacy](https://dl.acm.org/doi/10.1145/3411276.3412187) | [[Github]](https://github.com/seemoo-lab/csicloak) ACM International Workshop on Wireless Network Testbeds, Experimental evaluation & Characterization (WiNTECH) (2020)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:205:* [WiFE: WiFi and Vision based Intelligent Facial-Gesture Emotion Recognition](https://www.researchgate.net/profile/Xiang-Zhang-54/publication/340826489_WiFE_WiFi_and_Vision_based_Intelligent_Facial-Gesture_Emotion_Recognition/links/5ec72a1192851c11a87da07b/WiFE-WiFi-and-Vision-based-Intelligent-Facial-Gesture-Emotion-Recognition.pdf) arXiv:2004.09889 (2020)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:209:* [CSI-Net: Unified Human Body Characterization and Pose Recognition](https://arxiv.org/pdf/1810.03064.pdf) | [[Github]](https://github.com/geekfeiw/CSI-Net) arXiv:1810.03064 (2018)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:215:## CSI Tool
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:216:* [[Intel 5300 NIC]](https://dhalperi.github.io/linux-80211n-csitool/) Pioneered CSI tool enables Intel 5300 NIC to extract CSI data. It supports 30 subcarriers for a pair of antennas running on 20MHz.
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:217:* [[Atheros CSI Tool]](https://wands.sg/research/wifi/AtherosCSI/) Revamped CSI tool enables various Qualcomm Atheros NIC to extract CSI data. It supports 114 subcarriers for a pair of antennas running on 40MHz.
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:218:* [[Nexmon CSI Tool]](https://github.com/seemoo-lab/nexmon_csi) Mobile CSI Tool enables mobile phone and embedded device (RasPi) to extract CSI data of up to 256 subcarriers for a pair of antennas running on 80MHz.
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:219:* [[ESP32 CSI Tool]](https://stevenmhernandez.github.io/ESP32-CSI-Tool/) The ESP32 CSI Toolkit provides researchers access to Channel State Information (CSI) directly from the ESP32 microcontroller. 
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:220:* [[Software Defined Radio (SDR)]](https://www.ettus.com/) platforms, such as [Universal Software Radio Peripheral (USRP)](https://www.ettus.com/) and [Wireless Open Access Research Platform (WARP)](https://warpproject.org/trac), provide CSI measurements at 2.4GHz, 5GHz, and 60GHz.
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:223:* [[MM-Fi]](https://github.com/ybhbingo/MMFi_dataset) The MM-Fi dataset is a large-scale multimodal dataset including CSI, RGB-D, LiDAR, mmwave Radar. It consists of 40 human subjects across 4 different scenarios, with over 20 categories of actions.
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:224:* [[NTU-Fi]](https://github.com/xyanchen/WiFi-CSI-Sensing-Benchmark) The NTU-Fi dataset is the only CSI dataset with 114 subcarriers per pair of antennas, collected using Atheros CSI tool. It consists of 6 human activities and 14 human gait patterns.
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:226:IEEE 802.11ac routers with 256 subcarriers (practically 242 available). It includes 10 subjects and 3 applications.
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:227:* [[Widar 3.0]](https://ieee-dataport.org/open-access/widar-30-wifi-based-activity-recognition-dataset) The Widar 3.0 project is a large dataset designed for use in WiFi-based hand gesture recognition, collected using Intel 5300 NIC (30 subcarriers). The dataset consists of 258K instances of hand gestures with a duration of totally 8,620 minutes and from 75 domains.
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:228:* [[WiAR]](https://github.com/linteresa/WiAR) The WiAR dataset contains sixteen activities including coarse-grained activity and gestures performed by ten volunteers with 30 times every volunteer.
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:229:* [[UT-HAR]](https://github.com/ermongroup/Wifi_Activity_Recognition) The dataset is collected in ''A Survey on Behaviour Recognition Using WiFi Channel State Information''. It consists of continuous CSI data for 6 activities without golden segmentation timestamp for each sample.
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:230:* [[SignFi]](https://github.com/yongsen/SignFi) Channel State Information (CSI) traces for sign language recognition using WiFi.
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:237:* [[SenseFi]](https://github.com/xyanchen/WiFi-CSI-Sensing-Benchmark) Deep learning libraries for WiFi CSI sensing  (PyTorch) (Model Zoo)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:241:* [MM-Fi: Multi-Modal Non-Intrusive 4D Human Dataset for Versatile Wireless Sensing](https://arxiv.org/abs/2305.10345) | [[Github]](https://github.com/ybhbingo/MMFi_dataset) (Python) (2023)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:242:* [EfficientFi: Towards Large-Scale Lightweight WiFi Sensing via CSI Compression](https://ieeexplore.ieee.org/abstract/document/9667414) | [[Github]](https://github.com/Marsrocky/EfficientFi) (Python) (2022) 
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:245:* [An Experimental Study of CSI Management to Preserve Location Privacy](https://dl.acm.org/doi/10.1145/3411276.3412187) | [[Github]](https://github.com/seemoo-lab/csicloak) (Python) (2020)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:248:* [CSI-Net: Unified Human Body Characterization and Pose Recognition](https://arxiv.org/pdf/1810.03064.pdf) | [[Github]](https://github.com/geekfeiw/CSI-Net)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:256:* [Gait Recognition by SVM](https://github.com/thinszx/WiFi-CSI-gait-recognition) (MATLAB)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:257:* [BiLSTM for Human Activity Recognition](https://github.com/ludlows/CSI-Activity-Recognition) (Tensorflow 2.0)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:258:* [LSTM for Human Activity Recognition](https://github.com/Retsediv/WIFI_CSI_based_HAR) (Pytorch)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:259:* [SVM for Human Activity Recognition](https://github.com/noahcroit/HumanActivityDetection_using_CSI_MATLAB) (MATLAB)
third_party/wifi-sensing/vendor/Awesome-WiFi-CSI-Sensing/README.md:260:* [Gesture Data Collection Tool for Nexmon CSI Tool](https://github.com/dingyiyi0226/gesture-recognition-csi) (Python)
```

## esp-csi

### Top-level files
```text
.gitignore
.gitlab-ci.yml
.pre-commit-config.yaml
examples/README_cn.md
examples/README.md
LICENSE
README_cn.md
README.md
tools/check_idf_version.sh
tools/format.sh
```

### README preview
```text
# ESP-CSI [[中文]](./README_cn.md)

## Introduction to CSI

Channel State Information (CSI) is an important parameter that describes the characteristics of a wireless channel, including indicators such as signal amplitude, phase, and signal delay. In Wi-Fi communication, CSI is used to measure the state of the wireless network channel. By analyzing and studying changes in CSI, one can infer physical environmental changes that cause channel state changes, achieving non-contact intelligent sensing. CSI is very sensitive to environmental changes. It can sense not only large movements such as people or animals walking and running but also subtle actions in a static environment, such as breathing and chewing. These capabilities make CSI widely applicable in smart environment monitoring, human activity monitoring, wireless positioning, and other applications.

## Basic Knowledge

To better understand CSI technology, we provide some related basic knowledge documents (to be updated gradually):

- [Signal Processing Fundamentals](./docs/en/Signal-Processing-Fundamentals.md)
- [OFDM Introduction](./docs/en/OFDM-introduction.md)
- [Wireless Channel Fundamentals](./docs/en/Wireless-Channel-Fundamentals.md)
- [Introduction to Wireless Location](./docs/en/Introduction-to-Wireless-Location.md)
- [Wireless Indicators CSI and RSSI](./docs/en/Wireless-indicators-CSI-and-RSSI.md)
- [CSI Applications](./docs/en/CSI-Applications.md)

## Advantages of Espressif CSI

- **Full series support:** All ESP32 series support CSI, including ESP32 / ESP32-S2 / ESP32-C3 / ESP32-S3 / ESP32-C5 / ESP32-C6 / ESP32-C61.
- **Strong ecosystem:** Espressif is a global leader in the Wi-Fi MCU field, perfectly integrating CSI with existing IoT devices.
- **More information:** ESP32 provides rich channel information, including RSSI, RF noise floor, reception time, and the 'rx_ctrl' field of the antenna.
- **Bluetooth assistance:** ESP32 also supports BLE, for example, it can scan surrounding devices to assist detection.
- **Powerful processing capability:** The ESP32 CPU is dual-core 240MHz, supporting AI instruction sets, capable of running machine learning and neural networks.
- **OTA upgrade:** Existing projects can upgrade to new CSI features through software OTA without additional hardware costs.

## Example Introduction

### [get-started](./examples/get-started)

Helps users quickly get started with CSI functionality, demonstrating the acquisition and initial analysis of CSI data through basic examples. For details, see [README](./examples/get-started/README.md).

- [csi_recv](./examples/get-started/csi_recv) demonstrates the ESP32 as a receiver example.
- [csi_send](./examples/get-started/csi_send) demonstrates the ESP32 as a sender example.
- [csi_recv_router](./examples/get-started/csi_recv_router) demonstrates using a router as the sender, with the ESP32 triggering the router to send CSI packets via Ping.
- [tools](./examples/get-started/tools) provides scripts for assisting CSI data analysis, such as csi_data_read_parse.py.

### [esp-radar](./examples/esp-radar)

Provides some applications using CSI data, including RainMaker cloud reporting and human activity detection.

- [connect_rainmaker](./examples/esp-radar/connect_rainmaker) demonstrates capturing CSI data and uploading it to Espressif's RainMaker cloud platform.
- [console_test](./examples/esp-radar/console_test) demonstrates an interactive console that allows dynamic configuration and capture of CSI data, with applications for human activity detection algorithms.
- [wifi_sensing_demo](./examples/esp-radar/wifi_sensing_demo) demonstrates motion and human presence detection on top of the `esp_wifi_sensing` component, with on-site training, LED feedback, and a browser-based Web Serial monitor for live diagnostics and tuning.

## How to get CSI

### 4.1 Get router CSI

<img src="docs/_static/get_router_csi.png" width="550">

- **How ​​to implement:** ESP32 sends a Ping packet to the router, and receives the CSI information carried in the Ping Replay returned by the router.
- **Advantage:** Only one ESP32 plus router can be completed.
- **Disadvantages:** Depends on the router, such as the location of the router, the supported Wi-Fi protocol, etc.
- **Applicable scenario:** There is only one ESP32 in the environment, and there is a router in the detection environment.

### 4.2 Get CSI between devices

<img src="docs/_static/get_device_csi.png" width="550">

- **How ​​to implement:** ESP32 A and B both send Ping packets to the router, and ESP32 A receives the CSI information carried in the Ping sent by ESP32 B, which is a supplement to the first detection scenario.
- **Advantage:** Does not depend on the location of the router, and is not affected by other devices connected under the router.
- **Disadvantage:** Depends on the Wi-Fi protocol supported by the router, environment.
- **Applicable scenario:** There must be more than two ESP32s in the environment.

### 4.3 Get CSI specific devices

<img src="docs/_static/get_broadcast_csi.png" width="550">

- **How ​​to implement:** The packet sending device continuously switches channels to send out packets. ESP32 A, B, and C all obtain the CSI information carried in the broadcast packet of the packet sending device. This method has the highest detection accuracy and reliability.
- **Advantages:** The completion is not affected by the router, and the detection accuracy is high. When there are multiple devices in the environment, only one packet sending device will cause little interference to the network environment.
- **Disadvantages:** In addition to the ordinary ESP32, it is also necessary to add a special package issuing equipment, the cost is the same and higher.
- **Applicable scenarios:** Suitable for scenarios that require high accuracy and multi-device cluster positioning.

## 5 Note

1. The effect of external IPEX antenna is better than PCB antenna, PCB antenna has directivity.
2. Test in an unmanned environment. Avoid the influence of other people's activities on test results.

## 6 Related resources

- [ESP-IDF Programming Guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/index.html) is the documentation for the Espressif IoT development framework.
- [ESP-WIFI-CSI Guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/wifi.html#wi-fi-channel-state-information) is the use of ESP-WIFI-CSI Description.
- Community project recommendation: [ESPectre](https://github.com/francescopace/espectre), a motion detection system based on Wi-Fi CSI spectrum analysis with Home Assistant integration. It can be used as a reference implementation for bringing CSI research into real smart-home scenarios.
- If you find a bug or have a feature request, you can submit it on [Issues](https://github.com/espressif/esp-csi/issues) on GitHub. Please check to see if your question already exists in the existing Issues before submitting it.

## Reference

1. [Through-Wall Human Pose Estimation Using Radio Signals](http://rfpose.csail.mit.edu/)
2. [A list of awesome papers and cool resources on WiFi CSI sensing](https://github.com/Marsrocky/Awesome-WiFi-CSI-Sensing#awesome-wifi-sensing)
```

### Dependency indicators
```text
examples/esp-crab/master_recv/CMakeLists.txt
examples/esp-crab/slave_recv/CMakeLists.txt
examples/esp-crab/slave_send/CMakeLists.txt
examples/esp-radar/connect_rainmaker/CMakeLists.txt
examples/esp-radar/console_test/CMakeLists.txt
examples/esp-radar/wifi_sensing_demo/CMakeLists.txt
examples/get-started/csi_recv_router/CMakeLists.txt
examples/get-started/csi_recv/CMakeLists.txt
examples/get-started/csi_send/CMakeLists.txt
examples/get-started/tools/requirements.txt
```

### Capability keyword hits
```text
third_party/wifi-sensing/vendor/esp-csi/tools/ci/astyle-rules.yml:10:#   #    Add special rules for upstream source files, if necessary.
third_party/wifi-sensing/vendor/esp-csi/tools/ci/astyle-rules.yml:20:#   # Files which are not supposed to be formatted.
third_party/wifi-sensing/vendor/esp-csi/tools/ci/astyle-rules.yml:22:#   # - Upstream source code we don't want to modify
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Signal-Processing-Fundamentals.md:23:## CSI 子载波的利用
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Signal-Processing-Fundamentals.md:25:CSI通过子载波获取信道信息的能力源于正交频分复用（Orthogonal Frequency Division Multiplexing，OFDM）和正交频分复用多输入多输出（Orthogonal Frequency Division Multiplexing Multiple Input Multiple Output，OFDM-MIMO）等技术。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Signal-Processing-Fundamentals.md:28:因此，CSI能够通过子载波获取信道信息是基于OFDM技术和MIMO技术的特性，利用多个子载波和多个天线之间的信号差异来推断信道状态信息。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/CSI-Applications.md:1:# CSI的应用与案例分析[[English]](./docs/en/CSI-Applications.md)
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/CSI-Applications.md:3:本章介绍信道状态信息（CSI）在各种实际场景中的应用，主要内容包括：
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/CSI-Applications.md:5:## CSI在无线通信中的应用
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/CSI-Applications.md:7:- **频谱感知**：利用CSI检测和感知信道状态，进行频谱管理，优化频谱利用率。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/CSI-Applications.md:8:- **干扰管理**：使用CSI识别和抑制干扰源，提高通信质量和系统稳定性。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/CSI-Applications.md:9:- **资源分配**：基于CSI进行动态资源分配，优化系统性能和通信效率。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/CSI-Applications.md:11:## CSI在无线定位中的应用
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/CSI-Applications.md:13:- **精确定位**：利用CSI的高精度特性，实现厘米级定位，适用于需要高精度定位的场景。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/CSI-Applications.md:14:- **姿态估计**：通过CSI信息估计设备的姿态和方向，提高定位和导航的精度。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/CSI-Applications.md:18:- **CSI的获取与精度**：如何提高CSI获取的精度和效率，是未来研究的一个重要方向。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/CSI-Applications.md:19:- **大规模MIMO系统中的CSI**：处理大规模天线系统中的CSI问题，推动大规模MIMO技术的发展。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/CSI-Applications.md:20:- **机器学习与CSI**：利用机器学习技术优化CSI的应用和处理，提高CSI在复杂环境中的适应能力。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/CSI-Applications.md:24:- **案例1：定位和测距**：可以学习RSSI方法，并使用CSI作为更有信息的指纹（包括多个子载波上的信号幅度和相位信息），或依赖频率选择衰减模型来获得更准确的测距。CSI在定位和测距中的高精度特性使其成为比传统RSSI更优越的选择。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/CSI-Applications.md:25:通过CSI实现高精度室内定位，克服了传统定位技术的局限性。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/CSI-Applications.md:26:- **案例2：智能家居**：利用CSI信息提供个性化智能家居服务，提高用户体验和家庭安全。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/CSI-Applications.md:27:- **案例3：工业物联网**：基于CSI优化工业设备的监控和管理，提升工业自动化和智能化水平。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/CSI-Applications.md:29:- **案例5：人类活动检测和识别**：利用CSI对环境变化的高灵敏度来识别人体动作、手势、呼吸等细小动作和日常活动。CSI的高精度和高灵敏度使其在健康监测、智能家居和人机交互等领域有广泛的应用前景。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-Channel-Fundamentals.md:21:## CSI与无线信道特性的关系
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-Channel-Fundamentals.md:23:CSI通过详细的信道信息，帮助理解和利用无线信道的各种特性，从而优化无线通信系统的性能和可靠性。在无线通信中，特别是在使用多径效应和信道状态信息（CSI）时，有几种重要的应用：
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-Channel-Fundamentals.md:29:- **波束跟踪**：利用CSI信息跟踪多径传播信道的变化，以优化波束形状，从而最大化接收信号强度。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-Channel-Fundamentals.md:30:- **干扰抑制**：通过准确测量并分析多径信道的CSI，可以实现对干扰源的空间抑制，提高通信系统的信号干扰比（SIR）和系统的容量。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-Channel-Fundamentals.md:34:多径效应对于实现精确的位置定位和移动跟踪至关重要。CSI可以通过以下方式应用于定位与跟踪：
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-Channel-Fundamentals.md:36:- **多径成像**：通过分析CSI数据，可以构建物体周围的多径成像，从而实现高分辨率的位置估计。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-Channel-Fundamentals.md:41:在多用户MIMO系统中，CSI与多径效应的结合有以下应用：
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-Channel-Fundamentals.md:43:- **多用户分集**：通过利用多径传播的CSI，可以在不同路径上接收用户的数据流，从而提高系统的频谱效率和容量。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-Channel-Fundamentals.md:44:- **空间多用户调度**：基于多径信道的CSI信息，可以实现空间上的多用户调度，最大化系统的吞吐量和资源利用率。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-Channel-Fundamentals.md:48:多径效应和CSI对于动态频谱访问（DSA）和频谱感知（Spectrum Sensing）也有应用：
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-Channel-Fundamentals.md:50:- **频谱利用率优化**：通过分析多径信道的CSI，可以准确地评估和优化频谱资源的利用率，包括在频谱空白中实现动态频谱访问。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-Channel-Fundamentals.md:51:- **频谱干扰检测**：利用多径效应和CSI信息，可以实现对频谱干扰源的快速检测和定位，提高系统的抗干扰能力。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-Channel-Fundamentals.md:55:在高速移动通信环境下，多径效应和CSI的应用有助于：
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-Channel-Fundamentals.md:57:- **移动信道建模**：分析多径效应和CSI，可以建立准确的移动信道模型，为高速移动通信提供支持。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-Channel-Fundamentals.md:58:- **移动用户跟踪**：通过多径效应和CSI信息，可以实现对高速移动用户的快速跟踪和定位，提高通信系统的稳定性和可靠性。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-indicators-CSI-and-RSSI.md:1:# 无线通信指标 CSI 与 RSSI[[English]](./docs/en/Wireless-indicators-CSI-and-RSSI.md)
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-indicators-CSI-and-RSSI.md:3:无线通信中的 CSI（Channel State Information，信道状态信息）和 RSSI（Received Signal Strength Indicator，接收信号强度指示）是两个重要的指标，用于评估无线信号的质量和特性。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-indicators-CSI-and-RSSI.md:5:## CSI（Channel State Information）
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-indicators-CSI-and-RSSI.md:7:CSI 是指在无线通信系统中描述信道特性的详细信息。它包括了信道的幅度和相位信息，并通常在频域上表示为一个复数向量。CSI 提供了有关信道状态的非常详细的描述，通常用于 MIMO（多输入多输出）系统和 OFDM（正交频分复用）系统。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-indicators-CSI-and-RSSI.md:11:1. **精确性高**：CSI 提供了关于信道的非常详细的信息，包括信号的振幅和相位，因此可以精确地描述信道的状态。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-indicators-CSI-and-RSSI.md:12:2. **支持高级信号处理技术**：由于其详细性，CSI 支持高级的信号处理技术，如波束赋形、预编码和 MIMO 通信，能够显著提高系统的性能。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-indicators-CSI-and-RSSI.md:13:3. **动态调整**：可以根据实时的 CSI 信息动态调整发送策略和参数，提高通信的可靠性和效率。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-indicators-CSI-and-RSSI.md:17:1. **复杂性高**：获取和处理 CSI 信息需要较高的计算资源和复杂的硬件支持。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-indicators-CSI-and-RSSI.md:18:2. **时变性**：CSI 受信道变化影响较大，需要频繁更新，以保持信息的准确性。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-indicators-CSI-and-RSSI.md:19:3. **开销大**：获取和传输 CSI 信息会增加系统的开销，特别是在高速移动环境中。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-indicators-CSI-and-RSSI.md:39:**详细程度:** CSI 提供有关无线信道的更详细的信息，包括幅度、相位和频率响应。另一方面，RSSI 仅提供信号强度的一般测量。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-indicators-CSI-and-RSSI.md:41:**应用:** Wi-Fi CSI 对于需要对无线信道进行细粒度分析的高级应用特别有用，例如室内定位，手势识别和活动检测。RSSI 通常用于基本任务，如信号强度估计和基本的基于近似的应用程序。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-indicators-CSI-and-RSSI.md:43:**精度:** CSI 在某些应用中可以提供比 RSSI 更高的精度。它允许更精确的定位和跟踪，以及更好地区分不同的动作或手势。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-indicators-CSI-and-RSSI.md:45:**硬件支持:** CSI 和 RSSI 都可以从标准的 Wi-Fi 接收器获得，但 CSI 需要更先进的硬件能力来捕获和处理详细的信道信息。RSSI 是一种更简单的测量方法，大多数 Wi-Fi 接收器都可以获得。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-indicators-CSI-and-RSSI.md:47:||**CSI**|**RSSI**|
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/Wireless-indicators-CSI-and-RSSI.md:56:在实际应用中，CSI 和 RSSI 各有其适用场景。CSI 适合用于需要精确信道信息和高级信号处理的系统，而 RSSI 则适用于对资源要求较低的简单应用场景。
third_party/wifi-sensing/vendor/esp-csi/docs/zh_CN/OFDM-introduction.md:3:要理解 CSI 的原理，首先要了解 Wi-Fi 传输的物理层基本知识。OFDM 的"O"代表着"正交"，那么先从正交的定义说起。
third_party/wifi-sensing/vendor/esp-csi/docs/en/Signal-Processing-Fundamentals.md:23:## Utilization of CSI Subcarriers
third_party/wifi-sensing/vendor/esp-csi/docs/en/Signal-Processing-Fundamentals.md:25:The ability of CSI to obtain channel information through subcarriers is derived from technologies such as Orthogonal Frequency Division Multiplexing (OFDM) and Orthogonal Frequency Division Multiplexing Multiple Input Multiple Output (OFDM-MIMO).
third_party/wifi-sensing/vendor/esp-csi/docs/en/Signal-Processing-Fundamentals.md:27:In an OFDM-MIMO system, multiple antennas simultaneously transmit different data streams. These data streams are transmitted through the channel to the receiving end and are affected by channel effects such as multipath propagation and fading. Since the channel affects different subcarriers differently, the characteristics of signals on these subcarriers can be used to obtain channel information. By observing the differences between transmitted and received signals, one can infer channel state information, including channel fading, phase shifts, etc.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Signal-Processing-Fundamentals.md:28:Therefore, the ability of CSI to obtain channel information through subcarriers is based on the characteristics of OFDM and MIMO technologies, utilizing the signal differences between multiple subcarriers and multiple antennas to infer channel state information.
third_party/wifi-sensing/vendor/esp-csi/docs/en/CSI-Applications.md:1:# Application and Case Analysis of CSI[[中文]](docs/zh_CN/CSI-Applications.md)
third_party/wifi-sensing/vendor/esp-csi/docs/en/CSI-Applications.md:3:This chapter explores the application of Channel State Information (CSI) in various practical scenarios. The main content includes:
third_party/wifi-sensing/vendor/esp-csi/docs/en/CSI-Applications.md:5:## Applications of CSI in Wireless Communication
third_party/wifi-sensing/vendor/esp-csi/docs/en/CSI-Applications.md:7:- **Spectrum Sensing**: Using CSI to detect and sense channel states for spectrum management, optimizing spectrum utilization.
third_party/wifi-sensing/vendor/esp-csi/docs/en/CSI-Applications.md:8:- **Interference Management**: Using CSI to identify and suppress interference sources, improving communication quality and system stability.
third_party/wifi-sensing/vendor/esp-csi/docs/en/CSI-Applications.md:9:- **Resource Allocation**: Dynamically allocating resources based on CSI to optimize system performance and communication efficiency.
third_party/wifi-sensing/vendor/esp-csi/docs/en/CSI-Applications.md:11:## Applications of CSI in Wireless Positioning
third_party/wifi-sensing/vendor/esp-csi/docs/en/CSI-Applications.md:13:- **Precise Positioning**: Utilizing the high precision characteristics of CSI to achieve centimeter-level positioning, suitable for scenarios requiring high accuracy.
third_party/wifi-sensing/vendor/esp-csi/docs/en/CSI-Applications.md:14:- **Attitude Estimation**: Estimating the device's posture and orientation through CSI information, enhancing the accuracy of positioning and navigation.
third_party/wifi-sensing/vendor/esp-csi/docs/en/CSI-Applications.md:18:- **CSI Acquisition and Accuracy**: Improving the accuracy and efficiency of CSI acquisition is a crucial direction for future research.
third_party/wifi-sensing/vendor/esp-csi/docs/en/CSI-Applications.md:19:- **CSI in Large-scale MIMO Systems**: Addressing CSI issues in large-scale antenna systems to promote the development of large-scale MIMO technology.
third_party/wifi-sensing/vendor/esp-csi/docs/en/CSI-Applications.md:20:- **Machine Learning and CSI**: Leveraging machine learning techniques to optimize the application and processing of CSI, enhancing its adaptability in complex environments.
third_party/wifi-sensing/vendor/esp-csi/docs/en/CSI-Applications.md:24:- **Case 1: Positioning and Ranging**: Learning the RSSI method and using CSI as a more informative fingerprint (including signal amplitude and phase information across multiple subcarriers), or relying on frequency-selective fading models to achieve more accurate ranging. The high precision of CSI in positioning and ranging makes it a superior choice compared to traditional RSSI.
third_party/wifi-sensing/vendor/esp-csi/docs/en/CSI-Applications.md:25:Achieving high-precision indoor positioning with CSI overcomes the limitations of traditional positioning technologies.
third_party/wifi-sensing/vendor/esp-csi/docs/en/CSI-Applications.md:26:- **Case 2: Smart Home**: Utilizing CSI information to provide personalized smart home services, enhancing user experience and home security.
third_party/wifi-sensing/vendor/esp-csi/docs/en/CSI-Applications.md:27:- **Case 3: Industrial IoT**: Optimizing the monitoring and management of industrial equipment based on CSI, improving the level of industrial automation and intelligence.
third_party/wifi-sensing/vendor/esp-csi/docs/en/CSI-Applications.md:29:- **Case 5: Human Activity Detection and Recognition**: Using CSI's high sensitivity to environmental changes to recognize human movements, gestures, breathing, and other subtle actions and daily activities. The high precision and sensitivity of CSI make it widely applicable in health monitoring, smart homes, and human-computer interaction fields.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-Channel-Fundamentals.md:20:## Relationship Between CSI and Wireless Channel Characteristics
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-Channel-Fundamentals.md:22:Channel State Information (CSI) provides detailed channel information, aiding in understanding and utilizing various wireless channel characteristics to optimize the performance and reliability of wireless communication systems. Several important applications in wireless communication, especially involving multipath effects and Channel State Information (CSI), include:
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-Channel-Fundamentals.md:28:- **Beam Tracking:** Using CSI information to track changes in multipath propagation channels to optimize beam shapes and maximize received signal strength.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-Channel-Fundamentals.md:29:- **Interference Suppression:** Accurately measuring and analyzing CSI of multipath channels enables spatial suppression of interference sources, improving Signal-to-Interference Ratio (SIR) and system capacity.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-Channel-Fundamentals.md:32:Multipath effects are crucial for precise localization and mobile tracking. CSI can be applied in localization and tracking as follows:
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-Channel-Fundamentals.md:34:- **Multipath Imaging:** Analyzing CSI data to construct multipath images around objects, enabling high-resolution position estimation.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-Channel-Fundamentals.md:38:In multi-user MIMO systems, combining CSI with multipath effects has the following applications:
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-Channel-Fundamentals.md:40:- **Multi-User Diversity:** Utilizing CSI of multipath propagation to receive users' data streams on different paths, improving system spectral efficiency and capacity.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-Channel-Fundamentals.md:41:- **Spatial Multi-User Scheduling:** Using CSI information of multipath channels to achieve spatial multi-user scheduling, maximizing system throughput and resource utilization.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-Channel-Fundamentals.md:44:Multipath effects and CSI are also applied in dynamic spectrum access (DSA) and spectrum sensing:
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-Channel-Fundamentals.md:46:- **Optimizing Spectrum Utilization:** Analyzing CSI of multipath channels to accurately evaluate and optimize spectrum resource utilization, including achieving dynamic spectrum access in spectrum blanks.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-Channel-Fundamentals.md:47:- **Spectrum Interference Detection:** Using multipath effects and CSI information for rapid detection and localization of spectrum interference sources, enhancing system interference resistance.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-Channel-Fundamentals.md:50:In high-speed mobile communication environments, applications of multipath effects and CSI include:
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-Channel-Fundamentals.md:52:- **Mobile Channel Modeling:** Analyzing multipath effects and CSI to establish accurate mobile channel models, supporting high-speed mobile communications.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-Channel-Fundamentals.md:53:- **Mobile User Tracking:** Using multipath effects and CSI information for rapid tracking and localization of high-speed mobile users, improving communication system stability and reliability.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-Channel-Fundamentals.md:54:This translation captures the essential details and applications of wireless channel fundamentals and their relationship with CSI in optimizing wireless communication systems.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-indicators-CSI-and-RSSI.md:1:# Wireless Indicators: CSI and RSSI[[中文]](docs/zh_CN/Wireless-indicators-CSI-and-RSSI.md)
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-indicators-CSI-and-RSSI.md:3:In wireless communication, Channel State Information (CSI) and Received Signal Strength Indicator (RSSI) are two important metrics used to evaluate the quality and characteristics of wireless signals.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-indicators-CSI-and-RSSI.md:5:## CSI (Channel State Information)
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-indicators-CSI-and-RSSI.md:7:CSI is a detailed description of channel characteristics in a wireless communication system. It includes amplitude and phase information of the channel, typically represented as a complex vector in the frequency domain. CSI provides a very detailed description of the channel state, commonly used in Multiple Input Multiple Output (MIMO) and Orthogonal Frequency Division Multiplexing (OFDM) systems.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-indicators-CSI-and-RSSI.md:11:1. **High Precision**: CSI provides detailed information about the channel, including signal amplitude and phase, allowing for an accurate description of the channel state.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-indicators-CSI-and-RSSI.md:12:2. **Supports Advanced Signal Processing Techniques**: Due to its detailed nature, CSI supports advanced signal processing techniques such as beamforming, precoding, and MIMO communication, significantly enhancing system performance.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-indicators-CSI-and-RSSI.md:13:3. **Dynamic Adjustment**: Real-time CSI information enables dynamic adjustment of transmission strategies and parameters, improving communication reliability and efficiency.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-indicators-CSI-and-RSSI.md:16:1. **High Complexity**: Obtaining and processing CSI information requires significant computational resources and complex hardware support.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-indicators-CSI-and-RSSI.md:17:2. **Time-Varying Nature**: CSI is heavily influenced by changes in the channel and needs frequent updates to maintain accuracy.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-indicators-CSI-and-RSSI.md:18:3. **High Overhead**: Acquiring and transmitting CSI information increases system overhead, especially in high-speed mobile environments.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-indicators-CSI-and-RSSI.md:35:- **Detail Level**: CSI provides more detailed information about wireless channels, including amplitude, phase, and frequency response. In contrast, RSSI only provides a general measurement of signal strength.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-indicators-CSI-and-RSSI.md:36:- **Applications**: Wi-Fi CSI is particularly useful for advanced applications requiring fine-grained analysis of wireless channels, such as indoor positioning, gesture recognition, and activity detection. RSSI is typically used for basic tasks like signal strength estimation and simple applications.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-indicators-CSI-and-RSSI.md:37:- **Accuracy**: CSI can offer higher accuracy than RSSI in some applications, allowing for more precise localization, tracking, and differentiation of different actions or gestures.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-indicators-CSI-and-RSSI.md:38:- **Hardware Support**: Both CSI and RSSI can be obtained from standard Wi-Fi receivers, but CSI requires more advanced hardware capabilities to capture and process detailed channel information. RSSI is a simpler measurement method, accessible on most Wi-Fi receivers.
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-indicators-CSI-and-RSSI.md:39:|  | **CSI** | **RSSI** |
third_party/wifi-sensing/vendor/esp-csi/docs/en/Wireless-indicators-CSI-and-RSSI.md:48:In practical applications, CSI and RSSI each have their appropriate use cases. CSI is suitable for systems requiring precise channel information and advanced signal processing, while RSSI is suitable for simple applications with low resource requirements.
third_party/wifi-sensing/vendor/esp-csi/docs/en/OFDM-introduction.md:3:To understand the principles of CSI, one must first grasp the basics of the physical layer in Wi-Fi transmission. The "O" in OFDM stands for "Orthogonal," so let's start with the definition of orthogonality.
third_party/wifi-sensing/vendor/esp-csi/docs/en/OFDM-introduction.md:14:Let's start with the simplest model: for any $\omega_1 \ne \omega_2$, $\sin(\omega_1 t)$ and $\sin(\omega_2 t)$ are orthogonal over one period.
third_party/wifi-sensing/vendor/esp-csi/docs/en/OFDM-introduction.md:28:In a simple model, $\sin(\omega_1 t)$ and $\sin(\omega_2 t)$ are orthogonal. Over the duration $[0, T]$, the easiest way to transmit signals is through amplitude modulation: $\sin(\omega_1 t)$ transmits signal $a$, thus sending $a \cdot \sin(\omega_1 t)$, and $\sin(\omega_2 t)$ transmits signal $b$, thus sending $b \cdot \sin(\omega_2 t)$. The sine waves $\sin(\omega_1 t)$ and $\sin(\omega_2 t)$ serve as carriers and are predetermined information between the transmitter and receiver, called subcarriers. **The amplitude signals $a$ and $b$ modulated onto the subcarriers are the actual information to be transmitted.** The signal transmitted through the channel is $a \cdot \sin(\omega_1 t) + b \cdot \sin(\omega_2 t)$. At the receiver end, the signals are detected by integrating the received signal with respect to $\sin(\omega_1 t)$ and $\sin(\omega_2 t)$, thus retrieving $a$ and $b$. Below is the mathematical explanation of orthogonality applied to OFDM:
third_party/wifi-sensing/vendor/esp-csi/docs/en/OFDM-introduction.md:51:Taking $\sin(\omega_1 t)$ and $\sin(\omega_2 t)$ as examples, we demonstrate the transition from intuitive to abstract. The simple orthogonal model is the foundation of all complex theories.
third_party/wifi-sensing/vendor/esp-csi/docs/en/OFDM-introduction.md:53:Next, expand the model of $\sin(t)$ and $\sin(2t)$ to more subcarrier sequences $\{ \sin(2T \Delta f \cdot t), \sin(2T \Delta f \cdot 2t), \sin(2T \Delta f \cdot 3t), \ldots, \sin(2T \Delta f \cdot kt) \} $ (e.g., $k=16, 256, 1024$), where $2\pi$ is a constant, $\Delta f $ is the preselected carrier frequency interval, $T$ is the period, and $k$ is the maximum index of the sequence.
third_party/wifi-sensing/vendor/esp-csi/docs/en/OFDM-introduction.md:63:Thus, the sequence model extends to $\{\sin(2T \Delta f t), \sin(2T \Delta f \cdot 2t), \ldots, \sin(2T \Delta f kt), \cos(2T \Delta f t), \cos(2T \Delta f \cdot 2t), \ldots, \cos(2T \Delta f kt)\}$.
third_party/wifi-sensing/vendor/esp-csi/docs/en/OFDM-introduction.md:76:Therefore, the principle of OFDM is to decompose the time signal into different frequency sub-signals through Fourier transform, achieve parallel transmission through orthogonality, and then recover the original signal at the receiving end through inverse Fourier transform. This greatly improves spectral efficiency and interference resistance.
third_party/wifi-sensing/vendor/esp-csi/docs/en/OFDM-introduction.md:82:1. **Resistance to Multipath Interference**: Since OFDM decomposes the signal into multiple sub-signals transmitted on different frequencies, multipath interference only affects part of the sub-signals. The receiver can use equalization algorithms to reduce interference.
third_party/wifi-sensing/vendor/esp-csi/README.md:1:# ESP-CSI [[中文]](./README_cn.md)
third_party/wifi-sensing/vendor/esp-csi/README.md:3:## Introduction to CSI
third_party/wifi-sensing/vendor/esp-csi/README.md:5:Channel State Information (CSI) is an important parameter that describes the characteristics of a wireless channel, including indicators such as signal amplitude, phase, and signal delay. In Wi-Fi communication, CSI is used to measure the state of the wireless network channel. By analyzing and studying changes in CSI, one can infer physical environmental changes that cause channel state changes, achieving non-contact intelligent sensing. CSI is very sensitive to environmental changes. It can sense not only large movements such as people or animals walking and running but also subtle actions in a static environment, such as breathing and chewing. These capabilities make CSI widely applicable in smart environment monitoring, human activity monitoring, wireless positioning, and other applications.
third_party/wifi-sensing/vendor/esp-csi/README.md:9:To better understand CSI technology, we provide some related basic knowledge documents (to be updated gradually):
```

## RuView

### Top-level files
```text
.claude-flow/.gitignore
.claude-flow/.trend-cache.json
.claude-flow/CAPABILITIES.md
.claude-flow/config.yaml
.claude-flow/daemon-state.json
.claude-plugin/marketplace.json
.claude/memory.db
.claude/scheduled_tasks.lock
.claude/settings.json
.claude/settings.local.json
.dockerignore
.github/dependabot.yml
.gitignore
.gitmodules
.mcp.json
.swarm/schema.sql
.swarm/state.json
.vscode/launch.json
aether-arena/README.md
aether-arena/STATUS.md
aether-arena/VERIFY.md
archive/README.md
assets/exported-assets.zip
assets/NVsim Dashboard.zip
assets/README.txt
assets/ruview-seed.png
assets/ruview-small-gemini.jpg
assets/ruview-small.jpg
assets/screen.png
assets/screenshot.png
assets/seed.png
assets/v2-screen.png
assets/wifi-densepose-demo.zip
assets/wifi-mat.zip
benchmark_baseline.json
CHANGELOG.md
CLAUDE.md
dashboard/.gitignore
dashboard/index.html
dashboard/package-lock.json
dashboard/package.json
dashboard/playwright.config.ts
dashboard/tsconfig.json
dashboard/vite.config.ts
data/clone-data.rvf
deploy.sh
docker/.dockerignore
docker/docker-compose.yml
docker/docker-entrypoint.sh
docker/Dockerfile.python
docker/Dockerfile.rust
docker/wifi-densepose-v1.rvf
docs/ADR-110-BRANCH-STATE.md
docs/ADR-110-REVIEW-GUIDE.md
docs/build-guide.md
docs/proof-of-capabilities.md
docs/readme-details.md
docs/RELEASE-streaming-engine-v0.3.0.md
docs/security-audit-wasm-edge-vendor.md
docs/TROUBLESHOOTING.md
docs/user-guide-apple-homepod.md
docs/user-guide.md
docs/wifi-mat-user-guide.md
docs/WITNESS-LOG-028.md
docs/WITNESS-LOG-110.md
example.env
examples/README.md
examples/ruview_live.py
install.sh
LICENSE
logging/fluentd-config.yml
Makefile
monitoring/alerting-rules.yml
monitoring/grafana-dashboard.json
monitoring/prometheus-config.yml
plans/overview.md
plans/ui-pose-detection-rebuild.md
PROOF.md
pyproject.toml
python/.gitignore
```

### README preview
```text
# WiFi DensePose UI

A modular, modern web interface for the WiFi DensePose human tracking system. Provides real-time monitoring, WiFi sensing visualization, and pose estimation from CSI (Channel State Information).

## Architecture

The UI follows a modular architecture with clear separation of concerns:

```
ui/
├── app.js                    # Main application entry point
├── index.html                # HTML shell with tab structure
├── style.css                 # Complete CSS design system
├── config/
│   └── api.config.js         # API endpoints and configuration
├── services/
│   ├── api.service.js        # HTTP API client
│   ├── websocket.service.js  # WebSocket connection manager
│   ├── websocket-client.js   # Low-level WebSocket client
│   ├── pose.service.js       # Pose estimation API wrapper
│   ├── sensing.service.js    # WiFi sensing data service (live + simulation fallback)
│   ├── health.service.js     # Health monitoring API wrapper
│   ├── stream.service.js     # Streaming API wrapper
│   └── data-processor.js     # Signal data processing utilities
├── components/
│   ├── TabManager.js         # Tab navigation component
│   ├── DashboardTab.js       # Dashboard with live system metrics
│   ├── SensingTab.js         # WiFi sensing visualization (3D signal field, metrics)
│   ├── LiveDemoTab.js        # Live pose detection with setup guide
│   ├── HardwareTab.js        # Hardware configuration
│   ├── SettingsPanel.js      # Settings panel
│   ├── PoseDetectionCanvas.js # Canvas-based pose skeleton renderer
│   ├── gaussian-splats.js    # 3D Gaussian splat signal field renderer (Three.js)
│   ├── body-model.js         # 3D body model
│   ├── scene.js              # Three.js scene management
│   ├── signal-viz.js         # Signal visualization utilities
│   ├── environment.js        # Environment/room visualization
│   └── dashboard-hud.js      # Dashboard heads-up display
├── utils/
│   ├── backend-detector.js   # Auto-detect backend availability
│   ├── mock-server.js        # Mock server for testing
│   └── pose-renderer.js      # Pose rendering utilities
└── tests/
    ├── test-runner.html       # Test runner UI
    ├── test-runner.js         # Test framework and cases
    └── integration-test.html  # Integration testing page
```

## Features

### WiFi Sensing Tab
- 3D Gaussian-splat signal field visualization (Three.js)
- Real-time RSSI, variance, motion band, breathing band metrics
- Presence/motion classification with confidence scores
- **Data source banner**: green "LIVE - ESP32", yellow "RECONNECTING...", or red "SIMULATED DATA"
- Sparkline RSSI history graph
- "About This Data" card explaining CSI capabilities per sensor count

### Live Demo Tab
- WebSocket-based real-time pose skeleton rendering
- **Estimation Mode badge**: green "Signal-Derived" or blue "Model Inference"
- **Setup Guide panel** showing what each ESP32 count provides:
  - 1 ESP32: presence, breathing, gross motion
  - 2-3 ESP32s: body localization, motion direction
  - 4+ ESP32s + trained model: individual limb tracking, full pose
- Debug mode with log export
- Zone selection and force-reconnect controls
- Performance metrics sidebar (frames, uptime, errors)

### Dashboard
- Live system health monitoring
- Real-time pose detection statistics
- Zone occupancy tracking
- System metrics (CPU, memory, disk)
- API status indicators

### Hardware Configuration
- Interactive antenna array visualization
- Real-time CSI data display
- Configuration panels
- Hardware status monitoring

## Data Sources

The sensing service (`sensing.service.js`) supports three connection states:

| State | Banner Color | Description |
|-------|-------------|-------------|
| **LIVE - ESP32** | Green | Connected to the Rust sensing server receiving real CSI data |
| **RECONNECTING** | Yellow (pulsing) | WebSocket disconnected, retrying (up to 20 attempts) |
| **SIMULATED DATA** | Red | Fallback to client-side simulation after 5+ failed reconnects |

Simulated frames include a `_simulated: true` marker so code can detect synthetic data.

## Backends

### Rust Sensing Server (primary)
The Rust-based `wifi-densepose-sensing-server` serves the UI and provides:
- `GET /health` — server health
- `GET /api/v1/sensing/latest` — latest sensing features
- `GET /api/v1/vital-signs` — vital sign estimates (HR/RR)
- `GET /api/v1/model/info` — RVF model container info
- `WS /ws/sensing` — real-time sensing data stream
- `WS /api/v1/stream/pose` — real-time pose keypoint stream

### Python FastAPI (legacy)
The original Python backend on port 8000 is still supported. The UI auto-detects which backend is available via `backend-detector.js`.

## Quick Start

### With Docker (recommended)
```bash
cd docker/

# Default: auto-detects ESP32 on UDP 5005, falls back to simulation
docker-compose up

# Force real ESP32 data
CSI_SOURCE=esp32 docker-compose up

```

### Dependency indicators
```text
aether-arena/space/requirements.txt
archive/v1/requirements-lock.txt
archive/v1/setup.py
dashboard/package.json
examples/frontend/package.json
firmware/esp32-csi-node/CMakeLists.txt
firmware/esp32-csi-node/main/CMakeLists.txt
firmware/esp32-csi-node/main/idf_component.yml
firmware/esp32-hello-world/CMakeLists.txt
firmware/esp32-hello-world/main/CMakeLists.txt
harness/ruview/package.json
pyproject.toml
python/pyproject.toml
python/ruview-meta/pyproject.toml
python/tombstone/pyproject.toml
requirements-dev.txt
requirements.txt
tools/ruview-cli/package.json
tools/ruview-mcp/package.json
ui/mobile/package.json
```

### Capability keyword hits
```text
third_party/wifi-sensing/vendor/RuView/ui/README.md:3:A modular, modern web interface for the WiFi DensePose human tracking system. Provides real-time monitoring, WiFi sensing visualization, and pose estimation from CSI (Channel State Information).
third_party/wifi-sensing/vendor/RuView/ui/README.md:15:│   └── api.config.js         # API endpoints and configuration
third_party/wifi-sensing/vendor/RuView/ui/README.md:17:│   ├── api.service.js        # HTTP API client
third_party/wifi-sensing/vendor/RuView/ui/README.md:18:│   ├── websocket.service.js  # WebSocket connection manager
third_party/wifi-sensing/vendor/RuView/ui/README.md:19:│   ├── websocket-client.js   # Low-level WebSocket client
third_party/wifi-sensing/vendor/RuView/ui/README.md:20:│   ├── pose.service.js       # Pose estimation API wrapper
third_party/wifi-sensing/vendor/RuView/ui/README.md:21:│   ├── sensing.service.js    # WiFi sensing data service (live + simulation fallback)
third_party/wifi-sensing/vendor/RuView/ui/README.md:23:│   ├── stream.service.js     # Streaming API wrapper
third_party/wifi-sensing/vendor/RuView/ui/README.md:29:│   ├── LiveDemoTab.js        # Live pose detection with setup guide
third_party/wifi-sensing/vendor/RuView/ui/README.md:32:│   ├── PoseDetectionCanvas.js # Canvas-based pose skeleton renderer
third_party/wifi-sensing/vendor/RuView/ui/README.md:34:│   ├── body-model.js         # 3D body model
third_party/wifi-sensing/vendor/RuView/ui/README.md:42:│   └── pose-renderer.js      # Pose rendering utilities
third_party/wifi-sensing/vendor/RuView/ui/README.md:53:- Real-time RSSI, variance, motion band, breathing band metrics
third_party/wifi-sensing/vendor/RuView/ui/README.md:54:- Presence/motion classification with confidence scores
third_party/wifi-sensing/vendor/RuView/ui/README.md:55:- **Data source banner**: green "LIVE - ESP32", yellow "RECONNECTING...", or red "SIMULATED DATA"
third_party/wifi-sensing/vendor/RuView/ui/README.md:57:- "About This Data" card explaining CSI capabilities per sensor count
third_party/wifi-sensing/vendor/RuView/ui/README.md:60:- WebSocket-based real-time pose skeleton rendering
third_party/wifi-sensing/vendor/RuView/ui/README.md:62:- **Setup Guide panel** showing what each ESP32 count provides:
third_party/wifi-sensing/vendor/RuView/ui/README.md:63:  - 1 ESP32: presence, breathing, gross motion
third_party/wifi-sensing/vendor/RuView/ui/README.md:64:  - 2-3 ESP32s: body localization, motion direction
third_party/wifi-sensing/vendor/RuView/ui/README.md:65:  - 4+ ESP32s + trained model: individual limb tracking, full pose
third_party/wifi-sensing/vendor/RuView/ui/README.md:72:- Real-time pose detection statistics
third_party/wifi-sensing/vendor/RuView/ui/README.md:79:- Real-time CSI data display
third_party/wifi-sensing/vendor/RuView/ui/README.md:89:| **LIVE - ESP32** | Green | Connected to the Rust sensing server receiving real CSI data |
third_party/wifi-sensing/vendor/RuView/ui/README.md:98:The Rust-based `wifi-densepose-sensing-server` serves the UI and provides:
third_party/wifi-sensing/vendor/RuView/ui/README.md:100:- `GET /api/v1/sensing/latest` — latest sensing features
third_party/wifi-sensing/vendor/RuView/ui/README.md:101:- `GET /api/v1/vital-signs` — vital sign estimates (HR/RR)
third_party/wifi-sensing/vendor/RuView/ui/README.md:102:- `GET /api/v1/model/info` — RVF model container info
third_party/wifi-sensing/vendor/RuView/ui/README.md:103:- `WS /ws/sensing` — real-time sensing data stream
third_party/wifi-sensing/vendor/RuView/ui/README.md:104:- `WS /api/v1/stream/pose` — real-time pose keypoint stream
third_party/wifi-sensing/vendor/RuView/ui/README.md:115:# Default: auto-detects ESP32 on UDP 5005, falls back to simulation
third_party/wifi-sensing/vendor/RuView/ui/README.md:116:docker-compose up
third_party/wifi-sensing/vendor/RuView/ui/README.md:118:# Force real ESP32 data
third_party/wifi-sensing/vendor/RuView/ui/README.md:119:CSI_SOURCE=esp32 docker-compose up
third_party/wifi-sensing/vendor/RuView/ui/README.md:122:CSI_SOURCE=simulated docker-compose up
third_party/wifi-sensing/vendor/RuView/ui/README.md:129:cargo build -p wifi-densepose-sensing-server --no-default-features
third_party/wifi-sensing/vendor/RuView/ui/README.md:134:# Run with real ESP32
third_party/wifi-sensing/vendor/RuView/ui/README.md:142:wifi-densepose start
third_party/wifi-sensing/vendor/RuView/ui/README.md:154:| **Signal-Derived** | Green | 1+ ESP32, no model needed | Presence, breathing, gross motion |
third_party/wifi-sensing/vendor/RuView/ui/README.md:155:| **Model Inference** | Blue | 4+ ESP32s + trained `.rvf` model | Full 17-keypoint COCO pose |
third_party/wifi-sensing/vendor/RuView/ui/README.md:157:To use model inference, start the server with a trained model:
third_party/wifi-sensing/vendor/RuView/ui/README.md:159:sensing-server --source esp32 --model path/to/model.rvf --ui-path ./ui
third_party/wifi-sensing/vendor/RuView/ui/README.md:165:Edit `config/api.config.js`:
third_party/wifi-sensing/vendor/RuView/ui/README.md:170:  API_VERSION: '/api/v1',
third_party/wifi-sensing/vendor/RuView/ui/README.md:189:Test categories: API configuration, API service, WebSocket, pose service, health service, UI components, integration.
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:5:WiFi-DensePose Mobile is a React Native / Expo companion app for the [WiFi-DensePose](../../README.md) sensing platform. It connects to a WiFi sensing server over WebSocket, renders live 3D Gaussian splat visualizations of detected humans, displays breathing and heart rate in real time, and provides a full WiFi-MAT disaster triage dashboard — all from a single codebase that runs on iOS, Android, and Web.
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:10:> | **Vitals** | Breathing rate (6-30 BPM) and heart rate (40-120 BPM) arc gauges with sparkline history |
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:11:> | **Zones** | SVG floor plan with occupancy grid, zone legend, presence heatmap |
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:31:| **3D Live View** | Gaussian splat rendering | Three.js via WebView (native) or iframe (web), real-time pose overlay |
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:32:| **Vital Signs** | Breathing + heart rate | Arc gauge components with sparkline 60-sample history, confidence indicators |
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:34:| **Floor Plan** | SVG occupancy grid | Zone-level presence visualization, color-coded density, interactive legend |
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:36:| **Offline Capable** | Automatic simulation fallback | When the sensing server is unreachable, generates synthetic data so the UI stays functional |
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:37:| **RSSI Mode** | No CSI hardware needed | Toggle RSSI-only scanning for coarse presence detection on consumer WiFi devices |
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:53:| WiFi-DensePose Server | Any | Optional — app falls back to simulated data without a server |
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:67:Open `http://localhost:8081` in your browser. The app starts in simulation mode with synthetic pose and vital sign data.
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:99:| ESP32 mesh | `http://<esp32-ip>:3000` | Direct connection to ESP32 aggregator |
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:102:When the server is unreachable, the app automatically falls back to **simulation mode** after exhausting reconnect attempts (exponential backoff). A yellow `SIM` badge appears in the connection banner. Reconnection resumes automatically when the server becomes available.
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:119:      ErrorBoundary.tsx            Crash boundary with fallback UI
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:131:      api.ts                       REST API path constants
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:133:      websocket.ts                 WS path, reconnect delays, max attempts
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:152:        index.tsx                  Breathing + heart rate dashboard
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:153:        BreathingGauge.tsx         Arc gauge for breathing BPM
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:154:        HeartRateGauge.tsx         Arc gauge for heart rate BPM
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:174:      ws.service.ts               WebSocket client with auto-reconnect + simulation fallback
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:175:      api.service.ts              REST client (Axios) with retry logic
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:182:      poseStore.ts                Pose frames, connection status, frame history (Zustand)
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:194:      api.ts                      PoseStatus, ZoneConfig, HistoricalFrames, ApiError
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:216:  poseStore.ts          simulation.service.ts
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:223:       +---> VitalsScreen (breathing + heart rate gauges)
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:226:  api.service.ts -----> REST API (GET /api/pose/status, /zones, /frames)
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:246:The primary visualization screen. Renders a 3D Gaussian splat representation of detected humans using Three.js. On native platforms, the renderer runs inside a WebView; on web, it uses an iframe. A heads-up display overlays connection status, FPS, RSSI signal strength, detection confidence, and person count. Supports three modes: **LIVE** (connected to server), **SIM** (simulation fallback), and **RSSI** (RSSI-only scanning).
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:250:Displays real-time breathing rate and heart rate extracted from CSI signal processing. Each vital sign is shown as an animated arc gauge (`GaugeArc` component) with the current BPM value, a 60-sample sparkline history (`SparklineChart`), and a confidence percentage. Normal ranges: breathing 6-30 BPM, heart rate 40-120 BPM.
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:279:The app connects to the sensing server's WebSocket endpoint for real-time data streaming.
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:292:  features: FeatureSet;      // mean_rssi, variance, motion_band_power, etc.
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:293:  classification: Classification; // motion_level, presence, confidence
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:295:  vital_signs?: VitalsData;  // breathing_bpm, hr_proxy_bpm, confidence
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:307:The REST client (`api.service.ts`) provides:
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:311:| `GET` | `/api/pose/status` | `PoseStatus` — server health and capabilities |
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:312:| `GET` | `/api/pose/zones` | `ZoneConfig[]` — configured sensing zones |
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:313:| `GET` | `/api/pose/frames?limit=N` | `HistoricalFrames` — recent frame history |
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:336:| Services | 4 | `ws.service`, `api.service`, `rssi.service`, `simulation.service` |
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:337:| Stores | 3 | `poseStore`, `matStore`, `settingsStore` |
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:356:| `vitals_screen.yaml` | Breathing and heart rate gauges render with values |
third_party/wifi-sensing/vendor/RuView/ui/mobile/README.md:360:| `offline_fallback.yaml` | App transitions to SIM mode when server unreachable |
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:1506:    "node_modules/@dimforge/rapier3d-compat": {
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:1508:      "resolved": "https://registry.npmjs.org/@dimforge/rapier3d-compat/-/rapier3d-compat-0.12.0.tgz",
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:1524:    "node_modules/@emnapi/core": {
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:1526:      "resolved": "https://registry.npmjs.org/@emnapi/core/-/core-1.8.1.tgz",
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:1532:        "@emnapi/wasi-threads": "1.1.0",
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:1536:    "node_modules/@emnapi/runtime": {
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:1538:      "resolved": "https://registry.npmjs.org/@emnapi/runtime/-/runtime-1.8.1.tgz",
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:1547:    "node_modules/@emnapi/wasi-threads": {
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:1549:      "resolved": "https://registry.npmjs.org/@emnapi/wasi-threads/-/wasi-threads-1.1.0.tgz",
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:2598:        "merge-stream": "^2.0.0",
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:3276:        "merge-stream": "^2.0.0",
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:3652:        "merge-stream": "^2.0.0",
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:3774:    "node_modules/@napi-rs/wasm-runtime": {
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:3776:      "resolved": "https://registry.npmjs.org/@napi-rs/wasm-runtime/-/wasm-runtime-0.2.12.tgz",
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:3782:        "@emnapi/core": "^1.4.3",
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:3783:        "@emnapi/runtime": "^1.4.3",
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:4499:        "@react-navigation/routers": "^7.5.3",
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:4558:    "node_modules/@react-navigation/routers": {
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:4560:      "resolved": "https://registry.npmjs.org/@react-navigation/routers/-/routers-7.5.3.tgz",
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:4998:        "@dimforge/rapier3d-compat": "~0.12.0",
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:5049:        "ts-api-utils": "^2.5.0"
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:5167:        "ts-api-utils": "^2.5.0"
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:5210:        "ts-api-utils": "^2.5.0"
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:5505:        "@napi-rs/wasm-runtime": "^0.2.11"
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:6102:        "stream-buffers": "2.2.x"
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:6440:    "node_modules/combined-stream": {
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:6442:      "resolved": "https://registry.npmjs.org/combined-stream/-/combined-stream-1.0.8.tgz",
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:6446:        "delayed-stream": "~1.0.0"
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:6972:    "node_modules/delayed-stream": {
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:6974:      "resolved": "https://registry.npmjs.org/delayed-stream/-/delayed-stream-1.0.0.tgz",
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:7591:        "get-stream": "^6.0.0",
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:7593:        "is-stream": "^2.0.0",
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:7594:        "merge-stream": "^2.0.0",
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:7969:        "@expo/router-server": "^55.0.9",
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:8017:        "expo-router": "*",
third_party/wifi-sensing/vendor/RuView/ui/mobile/package-lock.json:8021:        "expo-router": {
```

## Wi-PoseDataset

### Top-level files
```text
Matrix.png
README.md
```

### README preview
```text
# Wi-Pose-Dataset
## Introduction
To further promote the research on WiFi-based human pose estimation, we construct the new dataset Wi-Pose by a camera, a 5 GHz wireless router, and a WiFi receiving host. Wi-Pose consists of 166,600 packets of .mat format. These packets contain pose annotations and WiFi channel state information (CSI) of 12 different actions performed by 12 volunteers. The pose annotations are generated by [Alphapose](https://openaccess.thecvf.com/content_ICCV_2017/papers/Fang_RMPE_Regional_Multi-Person_ICCV_2017_paper.pdf) [1] based on the pose images captured by the camera. The annotation of each pose image includes the coordinates of 18 skeleton points including the nose, neck, right shoulder, right elbow, right wrist, left shoulder, left elbow, left wrist, right hip, right knee, right ankle, left hip, left knee, left ankle, right eye, left eye, right ear, and left ear. The 12 actions include wave, walk, throw, run, push, pull, jump, crouch, circle, sit down, stand up, and bend. 

To make Wi-Pose more challenging and more adaptable to real scenarios, we invited 12 volunteers of different heights and weights and asked them to repeat each action 10 times. Each volunteer has about 13,200 corresponding packets of .mat format. Each packet contains 3 variable includes 'csi_serial', 'jointsVector', and 'jointsMatrix'. The 'csi_serial' stores the CSI with the size of 5×30×3×3, where 5 represents the 5 CSI data corresponding to the 1 image, 30 represents the 30 sub-carries, and 3×3 represents the 3 WiFi transmitting antennas and receiving antennas. The 'jointsVector' stores the pose annotations with the format of (x, y, c, c), where (x, y) represents the coordinate of each skeleton point, and c represents the confidence of the coordinate. Moreover, the 'jointsMatrix' stores the extended pose annotation matrix generated according to the following formula:
![Dataset](https://github.com/NjtechCVLab/Wi-PoseDataset/blob/main/Matrix.png)
The matrix makes the relative displacement between each skeleton point the regular term to enhance the robustness of the training model. Because of personal privacy and portrait rights, the public Wi-Pose does not include pose images of volunteers. Fortunately, it won't affect Wi-Pose-based model training. For data division, 132,847 and 33,753 packets are utilized for training, and testing, respectively.

## Dataset Access

### Google Drive
Link: [https://drive.google.com/file/d/1WL6bJ-rSVdsclRt9RFc0l5hhtXYmfNg9/view?usp=sharing](https://drive.google.com/file/d/1WL6bJ-rSVdsclRt9RFc0l5hhtXYmfNg9/view?usp=sharing)

### Baidu Netdisk
Link: [https://pan.baidu.com/s/14TbkIRPQN1DktDir9N2Y3A](https://pan.baidu.com/s/14TbkIRPQN1DktDir9N2Y3A)  
Password: wqeq 

## Reference
[1] Fang H S, Xie S, Tai Y W, et al. Rmpe: Regional multi-person pose estimation[C]//Proceedings of the IEEE international conference on computer vision. 2017: 2334-2343.
```

### Dependency indicators
```text
```

### Capability keyword hits
```text
third_party/wifi-sensing/vendor/Wi-PoseDataset/README.md:3:To further promote the research on WiFi-based human pose estimation, we construct the new dataset Wi-Pose by a camera, a 5 GHz wireless router, and a WiFi receiving host. Wi-Pose consists of 166,600 packets of .mat format. These packets contain pose annotations and WiFi channel state information (CSI) of 12 different actions performed by 12 volunteers. The pose annotations are generated by [Alphapose](https://openaccess.thecvf.com/content_ICCV_2017/papers/Fang_RMPE_Regional_Multi-Person_ICCV_2017_paper.pdf) [1] based on the pose images captured by the camera. The annotation of each pose image includes the coordinates of 18 skeleton points including the nose, neck, right shoulder, right elbow, right wrist, left shoulder, left elbow, left wrist, right hip, right knee, right ankle, left hip, left knee, left ankle, right eye, left eye, right ear, and left ear. The 12 actions include wave, walk, throw, run, push, pull, jump, crouch, circle, sit down, stand up, and bend. 
third_party/wifi-sensing/vendor/Wi-PoseDataset/README.md:5:To make Wi-Pose more challenging and more adaptable to real scenarios, we invited 12 volunteers of different heights and weights and asked them to repeat each action 10 times. Each volunteer has about 13,200 corresponding packets of .mat format. Each packet contains 3 variable includes 'csi_serial', 'jointsVector', and 'jointsMatrix'. The 'csi_serial' stores the CSI with the size of 5×30×3×3, where 5 represents the 5 CSI data corresponding to the 1 image, 30 represents the 30 sub-carries, and 3×3 represents the 3 WiFi transmitting antennas and receiving antennas. The 'jointsVector' stores the pose annotations with the format of (x, y, c, c), where (x, y) represents the coordinate of each skeleton point, and c represents the confidence of the coordinate. Moreover, the 'jointsMatrix' stores the extended pose annotation matrix generated according to the following formula:
third_party/wifi-sensing/vendor/Wi-PoseDataset/README.md:7:The matrix makes the relative displacement between each skeleton point the regular term to enhance the robustness of the training model. Because of personal privacy and portrait rights, the public Wi-Pose does not include pose images of volunteers. Fortunately, it won't affect Wi-Pose-based model training. For data division, 132,847 and 33,753 packets are utilized for training, and testing, respectively.
third_party/wifi-sensing/vendor/Wi-PoseDataset/README.md:19:[1] Fang H S, Xie S, Tai Y W, et al. Rmpe: Regional multi-person pose estimation[C]//Proceedings of the IEEE international conference on computer vision. 2017: 2334-2343.
```

## WiFi-CSI-Sensing-Benchmark

### Top-level files
```text
dataset.py
img/CSI_samples.jpg
img/Models.jpg
img/readme.md
img/transformer_block.jpg
img/Widar_classes.jpg
LICENSE
NTU_Fi_model.py
README.md
requirements.txt
run.py
self_supervised_model.py
self_supervised.py
UT_HAR_model.py
util.py
widar_model.py
```

### README preview
```text
[![GitHub](https://img.shields.io/github/license/Marsrocky/Awesome-WiFi-CSI-Sensing?color=blue)](https://github.com/Marsrocky/Awesome-WiFi-CSI-Sensing/blob/main/LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-YES-green.svg)](https://github.com/Marsrocky/Awesome-WiFi-CSI-Sensing/graphs/commit-activity)
![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)
[![DOI](https://zenodo.org/badge/511110383.svg)](https://zenodo.org/badge/latestdoi/511110383)
# SenseFi: A Benchmark for WiFi CSI Sensing
## Introduction
SenseFi is the first open-source benchmark and library for WiFi CSI human sensing, implemented by PyTorch. The state-of-the-art networks, including MLP, CNN, RNN, Transformers, etc, are evaluated on four public datasets across different WiFi CSI platforms. The details are illustrated in our paper [*SenseFi: A Library and Benchmark on Deep-Learning-Empowered WiFi Human Sensing*](https://arxiv.org/abs/2207.07859) that has been accepted by Patterns, Cell Press.

```
@article{yang2023benchmark,
  title={SenseFi: A Library and Benchmark on Deep-Learning-Empowered WiFi Human Sensing},
  author={Yang, Jianfei and Chen, Xinyan and Wang, Dazhuo and Zou, Han and Lu, Chris Xiaoxuan and Sun, Sumei and Xie, Lihua},
  journal={Patterns},
  volume={4},
  number={3},
  publisher={Elsevier},
  year={2023}
}
```

## Requirements

1. Install `pytorch` and `torchvision` (we use `pytorch==1.12.0` and `torchvision==0.13.0`).
2. `pip install -r requirements.txt`

**Note that the project runs perfectly in Linux OS (`Ubuntu`). If you plan to use `Windows` to run the codes, you need to modify the all the `/` to `\\` in the code regarding the dataset directory for the CSI data loading.**

## Run
### Download Processed Data
Please download and organize the [processed datasets](https://drive.google.com/drive/folders/1R0R8SlVbLI1iUFQCzh_mH90H_4CW2iwt?usp=sharing) in this structure:
```
Benchmark
├── Data
    ├── NTU-Fi_HAR
    │   ├── test_amp
    │   ├── train_amp
    ├── NTU-Fi-HumanID
    │   ├── test_amp
    │   ├── train_amp
    ├── UT_HAR
    │   ├── data
    │   ├── label
    ├── Widardata
    │   ├── test
    │   ├── train
```
We also offer [pre-trained weights](https://drive.google.com/drive/folders/1NBVe9za8ntFnkE9B1vhv4gD6eM88P1KI?usp=sharing) for all models


### Supervised Learning
To run models with supervised learning (train & test):  
Run: `python run.py --model [model name] --dataset [dataset name]`  

You can choose [model name] from the model list below
- MLP
- LeNet
- ResNet18
- ResNet50
- ResNet101
- RNN
- GRU
- LSTM
- BiLSTM
- CNN+GRU
- ViT

You can choose [dataset name] from the dataset list below
- UT_HAR_data
- NTU-Fi-HumanID
- NTU-Fi_HAR
- Widar

*Example: `python run.py --model ResNet18 --dataset NTU-Fi_HAR`*
### Unsupervised Learning
To run models with unsupervised (self-supervised) learning (train on **NTU-Fi HAR** & test on **NTU-Fi HumanID**):  
Run: `python self_supervised.py --model [model name] ` 

You can choose [model name] from the model list below
- MLP
- LeNet
- ResNet18
- ResNet50
- ResNet101
- RNN
- GRU
- LSTM
- BiLSTM
- CNN+GRU
- ViT

*Example: `python self_supervised.py --model MLP`*  
Method: [*AutoFi: Towards Automatic WiFi Human Sensing via Geometric Self-Supervised Learning*](https://doi.org/10.48550/arXiv.2205.01629)  


## Model Zoo
### MLP
- It consists of 3 fully-connected layers followed by activation functions 
### LeNet
- **self.encoder** : It consists of 3 convolutional layers followed by activation functions and Maxpooling layers to learn features
- **self.fc** : It consists of 2 fully-connected layers followed by activation functions for classification
### ResNet
- ***class*** **Bottleneck** : Each bottleneck consists of 3 convolutional layers followed by batch normalization operation and activation functions. And adds resudual connection within the bottleneck
- ***class*** **Block** : Each block consists of 2 convolutional layers followed by batch normalization operation and activation functions. And adds resudual connection within the block
- **self.reshape** : Reshape the input size into the size of 3 x 32 x 32
- **self.fc** : It consists of a fully-connected layer
### RNN
- **self.rnn** : A one-layer RNN structure with a hidden dimension of 64
- **self.fc** : It consists of a fully-connected layer
### GRU
- **self.gru** : A one-layer GRU structure with a hidden dimension of 64
- **self.fc** : It consists of a fully-connected layer
### LSTM
- **self.lstm** : A one-layer LSTM structure with a hidden dimension of 64
- **self.fc** : It consists of a fully-connected layer
### BiLSTM
- **self.lstm** : A one-layer bidirectional LSTM structure with a hidden dimension of 64
- **self.fc** : It consists of a fully-connected layer
### CNN+GRU
- **self.encoder** : It consists of 3 convolutional layers followed by activation functions
- **self.gru** : A one-layer GRU structure with a hidden dimension of 64
```

### Dependency indicators
```text
requirements.txt
```

### Capability keyword hits
```text
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/run.py:5:from util import load_data_n_model
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/run.py:7:def train(model, tensor_loader, num_epochs, learning_rate, criterion, device):
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/run.py:8:    model = model.to(device)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/run.py:9:    optimizer = torch.optim.Adam(model.parameters(), lr = learning_rate)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/run.py:11:        model.train()
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/run.py:21:            outputs = model(inputs)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/run.py:31:        epoch_loss = epoch_loss/len(tensor_loader.dataset)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/run.py:37:def test(model, tensor_loader, criterion, device):
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/run.py:38:    model.eval()
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/run.py:47:        outputs = model(inputs)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/run.py:57:    test_loss = test_loss/len(tensor_loader.dataset)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/run.py:65:    parser.add_argument('--dataset', choices = ['UT_HAR_data','NTU-Fi-HumanID','NTU-Fi_HAR','Widar'])
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/run.py:66:    parser.add_argument('--model', choices = ['MLP','LeNet','ResNet18','ResNet50','ResNet101','RNN','GRU','LSTM','BiLSTM', 'CNN+GRU','ViT'])
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/run.py:69:    train_loader, test_loader, model, train_epoch = load_data_n_model(args.dataset, args.model, root)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/run.py:72:    model.to(device)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/run.py:75:        model=model,
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/run.py:83:        model=model,
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/widar_model.py:116:            nn.ConvTranspose2d(22,3,7,stride=1),
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/widar_model.py:118:            nn.ConvTranspose2d(3,3,kernel_size=7,stride=1),
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:1:from dataset import *
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:2:from UT_HAR_model import *
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:3:from NTU_Fi_model import *
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:4:from widar_model import *
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:5:from self_supervised_model import *
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:8:def load_data_n_model(dataset_name, model_name, root):
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:10:    if dataset_name == 'UT_HAR_data':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:11:        print('using dataset: UT-HAR DATA')
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:12:        data = UT_HAR_dataset(root)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:17:        if model_name == 'MLP':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:18:            print("using model: MLP")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:19:            model = UT_HAR_MLP()
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:21:        elif model_name == 'LeNet':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:22:            print("using model: LeNet")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:23:            model = UT_HAR_LeNet()
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:25:        elif model_name == 'ResNet18':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:26:            print("using model: ResNet18")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:27:            model = UT_HAR_ResNet18()
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:29:        elif model_name == 'ResNet50':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:30:            print("using model: ResNet50")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:31:            model = UT_HAR_ResNet50()
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:33:        elif model_name == 'ResNet101':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:34:            print("using model: ResNet101")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:35:            model = UT_HAR_ResNet101()
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:37:        elif model_name == 'RNN':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:38:            print("using model: RNN")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:39:            model = UT_HAR_RNN()
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:41:        elif model_name == 'GRU':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:42:            print("using model: GRU")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:43:            model = UT_HAR_GRU()
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:45:        elif model_name == 'LSTM':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:46:            print("using model: LSTM")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:47:            model = UT_HAR_LSTM()
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:49:        elif model_name == 'BiLSTM':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:50:            print("using model: BiLSTM")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:51:            model = UT_HAR_BiLSTM()
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:53:        elif model_name == 'CNN+GRU':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:54:            print("using model: CNN+GRU")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:55:            model = UT_HAR_CNN_GRU()
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:57:        elif model_name == 'ViT':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:58:            print("using model: ViT")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:59:            model = UT_HAR_ViT()
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:61:        return train_loader, test_loader, model, train_epoch
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:64:    elif dataset_name == 'NTU-Fi-HumanID':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:65:        print('using dataset: NTU-Fi-HumanID')
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:67:        train_loader = torch.utils.data.DataLoader(dataset=CSI_Dataset(root + 'NTU-Fi-HumanID/test_amp/'), batch_size=64, shuffle=True)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:68:        test_loader = torch.utils.data.DataLoader(dataset=CSI_Dataset(root + 'NTU-Fi-HumanID/train_amp/'), batch_size=64, shuffle=False)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:69:        if model_name == 'MLP':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:70:            print("using model: MLP")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:71:            model = NTU_Fi_MLP(num_classes)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:73:        elif model_name == 'LeNet':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:74:            print("using model: LeNet")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:75:            model = NTU_Fi_LeNet(num_classes)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:77:        elif model_name == 'ResNet18':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:78:            print("using model: ResNet18")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:79:            model = NTU_Fi_ResNet18(num_classes)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:81:        elif model_name == 'ResNet50':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:82:            print("using model: ResNet50")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:83:            model = NTU_Fi_ResNet50(num_classes)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:85:        elif model_name == 'ResNet101':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:86:            print("using model: ResNet101")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:87:            model = NTU_Fi_ResNet101(num_classes)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:89:        elif model_name == 'RNN':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:90:            print("using model: RNN")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:91:            model = NTU_Fi_RNN(num_classes)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:93:        elif model_name == 'GRU':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:94:            print("using model: GRU")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:95:            model = NTU_Fi_GRU(num_classes)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:97:        elif model_name == 'LSTM':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:98:            print("using model: LSTM")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:99:            model = NTU_Fi_LSTM(num_classes)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:101:        elif model_name == 'BiLSTM':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:102:            print("using model: BiLSTM")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:103:            model = NTU_Fi_BiLSTM(num_classes)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:105:        elif model_name == 'CNN+GRU':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:106:            print("using model: CNN+GRU")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:107:            model = NTU_Fi_CNN_GRU(num_classes)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:109:        elif model_name == 'ViT':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:110:            print("using model: ViT")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:111:            model = NTU_Fi_ViT(num_classes=num_classes)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:113:        return train_loader, test_loader, model, train_epoch
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:116:    elif dataset_name == 'NTU-Fi_HAR':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:117:        print('using dataset: NTU-Fi_HAR')
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:119:        train_loader = torch.utils.data.DataLoader(dataset=CSI_Dataset(root + 'NTU-Fi_HAR/train_amp/'), batch_size=64, shuffle=True)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:120:        test_loader = torch.utils.data.DataLoader(dataset=CSI_Dataset(root + 'NTU-Fi_HAR/test_amp/'), batch_size=64, shuffle=False)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:121:        if model_name == 'MLP':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:122:            print("using model: MLP")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:123:            model = NTU_Fi_MLP(num_classes)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:125:        elif model_name == 'LeNet':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:126:            print("using model: LeNet")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:127:            model = NTU_Fi_LeNet(num_classes)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:129:        elif model_name == 'ResNet18':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:130:            print("using model: ResNet18")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:131:            model = NTU_Fi_ResNet18(num_classes)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:133:        elif model_name == 'ResNet50':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:134:            print("using model: ResNet50")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:135:            model = NTU_Fi_ResNet50(num_classes)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:137:        elif model_name == 'ResNet101':
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:138:            print("using model: ResNet101")
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:139:            model = NTU_Fi_ResNet101(num_classes)
third_party/wifi-sensing/vendor/WiFi-CSI-Sensing-Benchmark/util.py:141:        elif model_name == 'RNN':
```

## wifi-densepose

### Top-level files
```text
.claude-flow/.gitignore
.claude-flow/CAPABILITIES.md
.claude-flow/config.yaml
.claude-flow/daemon-state.json
.claude-flow/daemon.pid
.claude/memory.db
.claude/settings.json
.dockerignore
.gitignore
.mcp.json
.swarm/memory.db
.swarm/schema.sql
.swarm/state.json
assets/exported-assets.zip
assets/README.txt
assets/screen.png
assets/screenshot.png
assets/wifi-densepose-demo.zip
assets/wifi-mat.zip
CHANGELOG.md
CLAUDE.md
deploy.sh
docker/.dockerignore
docker/docker-compose.yml
docker/Dockerfile.python
docker/Dockerfile.rust
docker/wifi-densepose-v1.rvf
docs/build-guide.md
docs/user-guide.md
docs/wifi-mat-user-guide.md
docs/WITNESS-LOG-028.md
example.env
install.sh
LICENSE
logging/fluentd-config.yml
Makefile
monitoring/alerting-rules.yml
monitoring/grafana-dashboard.json
monitoring/prometheus-config.yml
plans/overview.md
plans/ui-pose-detection-rebuild.md
pyproject.toml
README.md
references/app.js
references/chart_script.py
references/densepose_performance_chart.png
references/generated_image_1.png
references/generated_image.png
references/index.html
references/LICENSE
references/README.md
references/script_1.py
references/script_2.py
references/script_3.py
references/script_4.py
references/script_5.py
references/script_6.py
references/script_7.py
references/script_8.py
references/script.py
references/style.css
references/wifi_densepose_pytorch.py
references/wifi_densepose_results.csv
references/wifi-densepose-arch.png
references/WiFi-DensePose-README.md
requirements.txt
scripts/generate-witness-bundle.sh
scripts/provision.py
ui/app.js
ui/index.html
ui/README.md
ui/start-ui.sh
ui/style.css
ui/TEST_REPORT.md
ui/viz.html
v1/__init__.py
v1/README.md
v1/requirements-lock.txt
v1/setup.py
v1/test_application.py
```

### README preview
```text
# WiFi-DensePose v1 (Python Implementation)

This directory contains the original Python implementation of WiFi-DensePose.

## Structure

```
v1/
├── src/                    # Python source code
│   ├── api/               # REST API endpoints
│   ├── config/            # Configuration management
│   ├── core/              # Core processing logic
│   ├── database/          # Database models and migrations
│   ├── hardware/          # Hardware interfaces
│   ├── middleware/        # API middleware
│   ├── models/            # Neural network models
│   ├── services/          # Business logic services
│   └── tasks/             # Background tasks
├── tests/                  # Test suite
├── docs/                   # Documentation
├── scripts/               # Utility scripts
├── data/                  # Data files
├── setup.py               # Package setup
├── test_application.py    # Application tests
└── test_auth_rate_limit.py # Auth/rate limit tests
```

## Requirements

- Python 3.10+
- PyTorch 2.0+
- FastAPI
- PostgreSQL/SQLite

## Installation

```bash
cd v1
pip install -e .
```

## Usage

```bash
# Start API server
python -m src.main

# Run tests
pytest tests/
```

## Note

This is the legacy Python implementation. For the new Rust implementation with improved performance, see `/rust-port/wifi-densepose-rs/`.
```

### Dependency indicators
```text
firmware/esp32-csi-node/CMakeLists.txt
firmware/esp32-csi-node/main/CMakeLists.txt
pyproject.toml
requirements.txt
ui/mobile/package.json
v1/requirements-lock.txt
v1/setup.py
vendor/ruvector/benchmarks/package.json
vendor/ruvector/npm/package.json
vendor/ruvector/package.json
```

### Capability keyword hits
```text
third_party/wifi-sensing/vendor/wifi-densepose/v1/test_auth_rate_limit.py:17:API_PREFIX = "/api/v1"
third_party/wifi-sensing/vendor/wifi-densepose/v1/test_auth_rate_limit.py:75:            f"{API_PREFIX}/pose/current"
third_party/wifi-sensing/vendor/wifi-densepose/v1/test_auth_rate_limit.py:99:            (f"{API_PREFIX}/pose/analyze", "POST"),
third_party/wifi-sensing/vendor/wifi-densepose/v1/test_auth_rate_limit.py:100:            (f"{API_PREFIX}/pose/calibrate", "POST"),
third_party/wifi-sensing/vendor/wifi-densepose/v1/test_auth_rate_limit.py:101:            (f"{API_PREFIX}/stream/start", "POST"),
third_party/wifi-sensing/vendor/wifi-densepose/v1/test_auth_rate_limit.py:102:            (f"{API_PREFIX}/stream/stop", "POST")
third_party/wifi-sensing/vendor/wifi-densepose/v1/test_auth_rate_limit.py:131:        endpoint = f"{self.base_url}{API_PREFIX}/pose/analyze"
third_party/wifi-sensing/vendor/wifi-densepose/v1/test_auth_rate_limit.py:171:                "endpoint": f"{API_PREFIX}/pose/current",
third_party/wifi-sensing/vendor/wifi-densepose/v1/test_auth_rate_limit.py:175:                "description": "Current pose endpoint (60/min)"
third_party/wifi-sensing/vendor/wifi-densepose/v1/test_auth_rate_limit.py:178:                "endpoint": f"{API_PREFIX}/pose/analyze",
third_party/wifi-sensing/vendor/wifi-densepose/v1/test_auth_rate_limit.py:257:        endpoint = f"{self.base_url}{API_PREFIX}/pose/current"
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:4:Provides realistic hardware behavior simulation for routers and sensors.
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:38:    router_id: str
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:49:    """Mock WiFi router with CSI capabilities."""
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:55:        self.is_streaming = False
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:63:        self.last_heartbeat = None
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:69:        self._streaming_task = None
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:70:        self._heartbeat_task = None
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:73:        """Connect to router."""
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:90:        self.last_heartbeat = datetime.utcnow()
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:93:        # Start heartbeat
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:94:        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:99:        """Disconnect from router."""
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:103:        # Stop streaming if active
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:104:        if self.is_streaming:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:105:            await self.stop_csi_streaming()
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:107:        # Stop heartbeat
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:108:        if self._heartbeat_task:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:109:            self._heartbeat_task.cancel()
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:111:                await self._heartbeat_task
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:118:    async def start_csi_streaming(self, sample_rate: int = 1000) -> bool:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:119:        """Start CSI data streaming."""
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:123:        if self.is_streaming:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:126:        self.is_streaming = True
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:127:        self._streaming_task = asyncio.create_task(self._csi_streaming_loop(sample_rate))
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:131:    async def stop_csi_streaming(self):
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:132:        """Stop CSI data streaming."""
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:133:        if not self.is_streaming:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:136:        self.is_streaming = False
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:138:        if self._streaming_task:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:139:            self._streaming_task.cancel()
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:141:                await self._streaming_task
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:145:    async def _csi_streaming_loop(self, sample_rate: int):
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:146:        """CSI data streaming loop."""
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:150:            while self.is_streaming:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:151:                # Generate CSI data
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:171:    async def _heartbeat_loop(self):
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:175:                self.last_heartbeat = datetime.utcnow()
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:193:        """Generate realistic CSI sample."""
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:225:            "router_id": self.config.router_id,
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:260:        """Notify CSI data callbacks."""
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:282:        """Get router status information."""
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:284:            "router_id": self.config.router_id,
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:287:            "is_streaming": self.is_streaming,
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:291:            "last_heartbeat": self.last_heartbeat.isoformat() if self.last_heartbeat else None,
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:318:        """Get CSI data buffer."""
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:322:        """Clear CSI data buffer."""
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:327:    """Mock network of WiFi routers."""
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:330:        self.routers = {}
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:334:            "on_router_added": [],
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:335:            "on_router_removed": [],
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:339:    def add_router(self, config: RouterConfig) -> MockWiFiRouter:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:340:        """Add router to network."""
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:341:        if config.router_id in self.routers:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:342:            raise ValueError(f"Router {config.router_id} already exists")
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:344:        router = MockWiFiRouter(config)
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:345:        self.routers[config.router_id] = router
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:347:        # Register for router events
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:348:        router.register_callback("on_status_change", self._on_router_status_change)
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:349:        router.register_callback("on_error", self._on_router_error)
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:352:        for callback in self.global_callbacks["on_router_added"]:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:353:            callback(router)
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:355:        return router
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:357:    def remove_router(self, router_id: str) -> bool:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:358:        """Remove router from network."""
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:359:        if router_id not in self.routers:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:362:        router = self.routers[router_id]
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:365:        if router.status != RouterStatus.OFFLINE:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:366:            asyncio.create_task(router.disconnect())
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:368:        del self.routers[router_id]
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:371:        for callback in self.global_callbacks["on_router_removed"]:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:372:            callback(router_id)
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:376:    def get_router(self, router_id: str) -> Optional[MockWiFiRouter]:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:377:        """Get router by ID."""
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:378:        return self.routers.get(router_id)
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:380:    def get_all_routers(self) -> Dict[str, MockWiFiRouter]:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:381:        """Get all routers."""
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:382:        return self.routers.copy()
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:384:    async def connect_all_routers(self) -> Dict[str, bool]:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:385:        """Connect all routers."""
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:389:        for router_id, router in self.routers.items():
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:390:            task = asyncio.create_task(router.connect())
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:391:            tasks.append((router_id, task))
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:393:        for router_id, task in tasks:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:396:                results[router_id] = result
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:398:                results[router_id] = False
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:402:    async def disconnect_all_routers(self):
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:403:        """Disconnect all routers."""
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:406:        for router in self.routers.values():
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:407:            if router.status != RouterStatus.OFFLINE:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:408:                task = asyncio.create_task(router.disconnect())
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:414:    async def start_all_streaming(self, sample_rate: int = 1000) -> Dict[str, bool]:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:415:        """Start CSI streaming on all routers."""
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:418:        for router_id, router in self.routers.items():
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:419:            if router.status == RouterStatus.ONLINE:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:420:                result = await router.start_csi_streaming(sample_rate)
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:421:                results[router_id] = result
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:423:                results[router_id] = False
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:427:    async def stop_all_streaming(self):
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:428:        """Stop CSI streaming on all routers."""
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:431:        for router in self.routers.values():
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:432:            if router.is_streaming:
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:433:                task = asyncio.create_task(router.stop_csi_streaming())
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:441:        total_routers = len(self.routers)
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:442:        online_routers = sum(1 for r in self.routers.values() if r.status == RouterStatus.ONLINE)
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:443:        streaming_routers = sum(1 for r in self.routers.values() if r.is_streaming)
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:446:            "total_routers": total_routers,
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:447:            "online_routers": online_routers,
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:448:            "streaming_routers": streaming_routers,
third_party/wifi-sensing/vendor/wifi-densepose/v1/tests/mocks/hardware_mocks.py:449:            "network_health": online_routers / max(total_routers, 1),
```

## wifi-radar

### Top-level files
```text
.github/CONTRIBUTING.md
.gitignore
.pre-commit-config.yaml
docker/docker-compose.yml
docker/Dockerfile
docker/nginx-rtmp.conf
docs/# WiFi-Radar Setup Guide.md
docs/recent_research_2026.md
docs/reference.md
docs/system_overview.md
main.py
pyproject.toml
README.md
requirements-dev.txt
requirements.txt
scripts/__init__.py
scripts/check_code.sh
scripts/export_onnx.py
scripts/export_tensorrt.py
scripts/README.md
scripts/setup_venv.sh
scripts/train_simulation_baseline.py
scripts/train_transfer_learning.py
scripts/validate_live_capture.py
setup.cfg
tests/__init__.py
tests/conftest.py
tests/README.md
tests/test_api.py
tests/test_csi_parser.py
tests/test_dashboard_streaming.py
tests/test_gait_anomaly_detector.py
tests/test_hybrid_activity_fusion.py
tests/test_live_capture_validation.py
weights/.gitkeep
```

### README preview
```text
# Tests

This directory contains tests for the WiFi-Radar system:

- Unit tests for individual components
- Integration tests for system functionality
- Test data and utilities

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=wifi_radar

# Run specific test file
pytest tests/test_csi_collector.py

# Run tests matching a pattern
pytest -k "collector"
```

## Test Organization

- `test_data/`: Test data files and fixtures
- `test_*.py`: Individual test files for each module
- `conftest.py`: Shared pytest fixtures```

### Dependency indicators
```text
pyproject.toml
requirements-dev.txt
requirements.txt
```

### Capability keyword hits
```text
third_party/wifi-sensing/vendor/wifi-radar/docker/docker-compose.yml:4:# Start:    docker compose -f docker/docker-compose.yml up --build
third_party/wifi-sensing/vendor/wifi-radar/docker/docker-compose.yml:5:# Detached: docker compose -f docker/docker-compose.yml up -d --build
third_party/wifi-sensing/vendor/wifi-radar/docker/docker-compose.yml:7:# Ports exposed to host:
third_party/wifi-sensing/vendor/wifi-radar/docker/docker-compose.yml:8:#   1935  — RTMP ingest   (push from wifi-radar app)
third_party/wifi-sensing/vendor/wifi-radar/docker/docker-compose.yml:9:#   8080  — HLS playback  + nginx stats  (http://localhost:8080/hls/wifi_radar.m3u8)
third_party/wifi-sensing/vendor/wifi-radar/docker/docker-compose.yml:19:    container_name: wifi-radar-rtmp
third_party/wifi-sensing/vendor/wifi-radar/docker/docker-compose.yml:32:  # ── wifi-radar app ─────────────────────────────────────────────────────────
third_party/wifi-sensing/vendor/wifi-radar/docker/docker-compose.yml:33:  wifi-radar:
third_party/wifi-sensing/vendor/wifi-radar/docker/docker-compose.yml:37:    container_name: wifi-radar-app
third_party/wifi-sensing/vendor/wifi-radar/docker/docker-compose.yml:41:      - RTMP_URL=rtmp://nginx-rtmp/live/wifi_radar
third_party/wifi-sensing/vendor/wifi-radar/docker/docker-compose.yml:44:      - wifi_radar_config:/root/.wifi_radar
third_party/wifi-sensing/vendor/wifi-radar/docker/docker-compose.yml:45:      - wifi_radar_weights:/app/weights
third_party/wifi-sensing/vendor/wifi-radar/docker/docker-compose.yml:52:      --rtmp-url rtmp://nginx-rtmp/live/wifi_radar
third_party/wifi-sensing/vendor/wifi-radar/docker/docker-compose.yml:56:  wifi_radar_config:
third_party/wifi-sensing/vendor/wifi-radar/docker/docker-compose.yml:58:  wifi_radar_weights:
third_party/wifi-sensing/vendor/wifi-radar/requirements.txt:12:websockets>=12.0
third_party/wifi-sensing/vendor/wifi-radar/requirements.txt:14:fastapi>=0.115
third_party/wifi-sensing/vendor/wifi-radar/tests/__init__.py:4:Purpose: Enable pytest to find and execute integration and system-level tests
third_party/wifi-sensing/vendor/wifi-radar/tests/__init__.py:5:         that span multiple wifi_radar submodules.
third_party/wifi-sensing/vendor/wifi-radar/tests/README.md:16:pytest --cov=wifi_radar
third_party/wifi-sensing/vendor/wifi-radar/tests/test_live_capture_validation.py:3:from wifi_radar.data.csi_collector import CSICollector
third_party/wifi-sensing/vendor/wifi-radar/tests/test_live_capture_validation.py:4:from wifi_radar.utils.live_capture_validation import validate_capture_file
third_party/wifi-sensing/vendor/wifi-radar/tests/test_live_capture_validation.py:26:    collector = CSICollector(buffer_size=8)
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:3:from wifi_radar.analysis.gait_analyzer import GaitMetrics
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:4:from wifi_radar.analysis.hybrid_activity_fusion import HybridActivityFusion
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:16:            pose_confidence=np.ones(17, dtype=np.float32) * 0.95,
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:21:    assert result["motion_score"] < 0.05
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:30:            pose_confidence=np.ones(17, dtype=np.float32) * 0.9,
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:41:    assert moving["activity_label"] in {"walking", "high_motion"}
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:42:    assert moving["motion_score"] > 0.05
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:45:def test_hybrid_activity_fusion_escalates_possible_fall():
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:53:        pose_confidence=np.ones(17, dtype=np.float32) * 0.4,
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:62:        fall_severity=2,
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:65:    assert result["activity_label"] == "possible_fall"
third_party/wifi-sensing/vendor/wifi-radar/tests/test_hybrid_activity_fusion.py:66:    assert result["fall_risk"] >= 0.8
third_party/wifi-sensing/vendor/wifi-radar/tests/test_gait_anomaly_detector.py:3:from wifi_radar.analysis.gait_analyzer import GaitMetrics
third_party/wifi-sensing/vendor/wifi-radar/tests/test_gait_anomaly_detector.py:4:from wifi_radar.analysis.gait_anomaly_detector import GaitAnomalyDetector
third_party/wifi-sensing/vendor/wifi-radar/tests/test_api.py:1:from fastapi.testclient import TestClient
third_party/wifi-sensing/vendor/wifi-radar/tests/test_api.py:3:from wifi_radar.api.app import AppState, create_app
third_party/wifi-sensing/vendor/wifi-radar/tests/test_api.py:6:def test_api_health_and_config_roundtrip():
third_party/wifi-sensing/vendor/wifi-radar/tests/test_api.py:24:def test_api_ingest_and_status():
third_party/wifi-sensing/vendor/wifi-radar/tests/test_api.py:34:            "events": [{"message": "fall alert", "severity": 2}],
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:3:from wifi_radar.streaming.rtmp_streamer import RTMPStreamer
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:4:from wifi_radar.visualization.dashboard import Dashboard
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:7:def _sample_pose():
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:19:    pose = _sample_pose()
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:25:        pose_data=pose,
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:26:        confidence_data=pose["confidence"],
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:28:        tracked_people=[{"person_id": 1, **pose}],
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:31:        fall_events=[{"message": "fall alert", "severity": 2, "timestamp": 123.0}],
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:35:    dashboard.confidence_history.append(float(np.mean(pose["confidence"])))
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:36:    pose_fig = dashboard._update_pose_figure(pose)
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:40:    assert len(pose_fig.data) > 0
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:45:def test_rtmp_streamer_renders_frame():
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:46:    streamer = RTMPStreamer(width=320, height=240, fps=10)
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:47:    pose = _sample_pose()
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:48:    streamer.update_frame(pose_data=pose, confidence_data=pose["confidence"])
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:49:    assert streamer.latest_frame is not None
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:50:    assert streamer.latest_frame.shape == (240, 320, 3)
third_party/wifi-sensing/vendor/wifi-radar/tests/test_dashboard_streaming.py:51:    assert streamer.latest_frame.sum() > 0
third_party/wifi-sensing/vendor/wifi-radar/tests/test_csi_parser.py:4:from wifi_radar.data.csi_collector import CSICollector
third_party/wifi-sensing/vendor/wifi-radar/tests/test_csi_parser.py:8:    collector = CSICollector()
third_party/wifi-sensing/vendor/wifi-radar/tests/test_csi_parser.py:12:    raw = b"CSI0" + struct.pack("<III", 3, 3, 64) + amp.tobytes() + phase.tobytes()
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:3:The WiFi-Radar system is based on research in the field of RF-based human sensing, particularly focusing on WiFi signals for pose estimation. This document provides key references that form the theoretical foundation of this project.
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:11:   - Summary: Presents a system for human pose estimation using WiFi signals, without requiring cameras or specialized hardware.
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:17:   - Summary: Demonstrates human pose estimation through walls using specialized RF devices.
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:25:4. **CSI-Based Human Activity Recognition Using Channel State Information**
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:29:   - Summary: Presents techniques for extracting and processing CSI data for human activity recognition.
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:33:### Channel State Information (CSI)
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:35:CSI data represents the channel properties of a communication link, containing information about:
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:42:In 802.11n/ac WiFi systems, CSI is collected for each subcarrier and for each transmitter-receiver antenna pair in MIMO systems.
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:53:These interactions create measurable changes in the CSI, which can be analyzed to infer human presence, movement, and posture.
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:57:Modern pose estimation from WiFi signals uses deep learning techniques including:
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:66:1. [Linux CSI Tool](https://github.com/spanev/linux-80211n-csitool): Tool for collecting CSI measurements from WiFi devices
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:67:2. [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose): Popular framework for pose estimation
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:68:3. [DensePose](https://github.com/facebookresearch/DensePose): Research framework for dense human pose estimation
third_party/wifi-sensing/vendor/wifi-radar/docs/reference.md:74:3. **Health monitoring**: Using WiFi-based pose for fall detection and gait analysis
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:5:WiFi-Radar consists of several interconnected components that work together to transform WiFi signals into human pose estimations:
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:8:CSI Data Acquisition → Signal Processing → Neural Network Processing → Pose Estimation → Visualization/Streaming
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:11:### 1. CSI Data Acquisition
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:13:The system captures Channel State Information (CSI) from WiFi signals using a commodity router with 3×3 MIMO capability. CSI data contains:
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:21:Raw CSI data undergoes several preprocessing steps:
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:29:A dual-branch encoder processes the prepared CSI data:
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:47:- RTMP streaming for external broadcasting
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:51:### WiFi CSI Extraction
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:53:We use the Linux CSI Tool or similar to extract CSI data from the WiFi router. This requires:
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:54:- Modified router firmware
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:55:- Driver modifications for CSI extraction
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:56:- Network configuration for real-time data streaming
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:67:The pose estimation system uses:
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:84:- RTMP protocol for streaming
third_party/wifi-sensing/vendor/wifi-radar/docs/system_overview.md:85:- Custom frame generation from pose data
third_party/wifi-sensing/vendor/wifi-radar/docs/recent_research_2026.md:7:| 2026-01-18 | PerceptAlign / geometry-aware cross-layout pose estimation | Explicitly conditions the model on transceiver geometry to reduce layout overfitting | Strong fit for real-hardware deployment and replay validation |
third_party/wifi-sensing/vendor/wifi-radar/docs/recent_research_2026.md:8:| 2026-02-09 | WiFlow | Lightweight spatio-temporal decoupling for continuous WiFi pose estimation | Strong fit for low-latency and edge inference |
third_party/wifi-sensing/vendor/wifi-radar/docs/recent_research_2026.md:9:| 2026-02-26 | WiPowerSys | ESP32-based CSI capture with skeleton supervision | Strong fit for commodity deployment workflows |
third_party/wifi-sensing/vendor/wifi-radar/docs/recent_research_2026.md:10:| 2026-04-01 | MKFi | Multi-window fusion for temporally robust WiFi activity recognition under limited data | Strong fit for fall and gait robustness |
third_party/wifi-sensing/vendor/wifi-radar/docs/recent_research_2026.md:16:1. keep the existing CSI-to-pose backbone,
third_party/wifi-sensing/vendor/wifi-radar/docs/recent_research_2026.md:18:3. fuse short-window and long-window CSI motion evidence with pose confidence and gait metrics.
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:3:This guide will help you set up and run the WiFi-Radar system for human pose estimation through WiFi signals.
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:7:- A WiFi router capable of providing CSI (Channel State Information) data
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:8:  - Recommended: Nighthawk mesh router or similar devices
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:9:  - The router should support 3×3 MIMO capabilities
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:15:### Enabling CSI Collection
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:17:To collect CSI data from your router, you'll need to:
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:19:1. Install custom firmware on your router that enables CSI extraction
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:20:   - For Nighthawk routers: Follow the manufacturer's instructions for firmware updates
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:21:   - For TP-Link Archer series: Install OpenWrt and the `atheros-csi-tool` package
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:22:   - For ASUS routers: Use the Merlin firmware with CSI extraction patches
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:23:   - You may need to install OpenWrt or similar open-source firmware
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:25:2. Configure the router to stream CSI data
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:27:   # SSH into your router
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:30:   # Enable CSI tool (Nighthawk method)
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:33:   # Configure CSI streaming
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:34:   csi-tool stream --port 5500 --format binary
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:36:   # Alternative for OpenWrt-based routers
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:39:   # Alternative for ASUS routers
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:43:3. Verify that CSI data is being streamed
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:49:   python scripts/test_csi_connection.py --router-ip <YOUR_ROUTER_IP> --port 5500
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:51:   You should see continuous data streaming from the router.
third_party/wifi-sensing/vendor/wifi-radar/docs/# WiFi-Radar Setup Guide.md:53:4. Troubleshooting CSI collection:
```

## WiROS

### Top-level files
```text
README.md
```

### README preview
```text
# WiROS: WiFi sensing toolbox for robotics

WiROS is a plug-and-play WiFi sensing toolbox allowing researchers to access coarse grained WiFi signal strength (RSSI), fine grained WiFi channel state information (CSI), and other MAC-layer information (device address, packet id’s or frequency-channel information). Additionally, WiROS open-sources state of-art algorithms to calibration and process WiFi measurements to furnish accurate bearing information for received WiFi signals. 

This is an index repository to access the following components of WiROS
1. [**CSI Node**](https://github.com/ucsdwcsng/wiros_csi_node) - Extends the Nexmon CSI toolkit[1] to provide a ROS overlay. 
2. [**Processing Node**](https://github.com/ucsdwcsng/wiros_processing_node) - Provide calibration and post-processing of WiFi CSI measurments. Open-sources mulitple state-of-art bearing extraction algorithms to measure both the angle of arrival (at the receiver) and angle of departure (from the transmitter) of the WiFi signal.
3. [**RF Messages format**](https://github.com/ucsdwcsng/rf_msgs) - Custom ROS messages to structure WiFi measurements information. 

## Overview of Features

1. Easily integrate WiFi channel state measurements, received signal strength and other WiFi MAC-layer information into your robot sensor stack. 
2. Exposes all relevant measurements as accessible ROS topics. See [`rf_msgs`](https://github.com/ucsdwcsng/rf_msgs) for more details.  
3. Builds a framework for hassle-free [wireless calibration](https://github.com/ucsdwcsng/wiros_processing_node/blob/main/README.md#dynamic-compensation) of wireless sensors.
4. Provides visualizations for WiFi signals which are helpful for algorithm paramter tuning and debugging 
5. Open-sources implementation of various state-of-art WiFi processing algorithms[2, 3, 4]. 

## Getting Started

To get started with WiROS, clone these repositories into the `src` folder of your catkin workspace, and follow the [README](https://github.com/ucsdwcsng/wiros_csi_node/blob/main/README.md) in the [CSI Node](https://github.com/ucsdwcsng/wiros_csi_node) to configure your hardware.   

## Example usage of WiROS 

WiROS can be easily leveraged to incorporate WiFi sensors to solve many applicable problems in robotics. We provide the following sample use-cases:

1. **Kidnapped Robot Problem**: A lost robot in an indoor envrionment can be conveniently localized using WiROS. Given a prior map of the existing Access points and additional details of their antenna geometry, the robot's location can be triangulated in a space. 
2. **Correct for Robot Location Drift**: WiFi measurements can be additionally fused with Camera and odometry measurements to more accurately correct for sensor drifts and resolve ambiguities arising from perceptual aliasing in indoor environment[3]. 
3. **IoT device localiztion**: Often IoT devices are hard to localize visually. However, we can leverage WiFi-based bearing measurements to trinagulate their position in the envrionment. This can be useful for both IoT device management or to ensure security/privacy of users in a space. 

### Citations

1. Blanco, Alejandro, et al. "Accurate ubiquitous localization with off-the-shelf ieee 802.11 ac devices." The 19th Annual International Conference on Mobile Systems, Applications, and Services (MobiSys 2021). 2021.
2. Kotaru, Manikanta, et al. "Spotfi: Decimeter level localization using wifi." Proceedings of the 2015 ACM Conference on Special Interest Group on Data Communication. 2015.
3. Arun, Aditya, et al. "ViWiD: Leveraging WiFi for Robust and Resource-Efficient SLAM." arXiv preprint arXiv:2209.08091 (2022).
4. Schmidt, Ralph. "Multiple emitter location and signal parameter estimation." IEEE transactions on antennas and propagation 34.3 (1986): 276-280.
    




```

### Dependency indicators
```text
```

### Capability keyword hits
```text
third_party/wifi-sensing/vendor/WiROS/README.md:1:# WiROS: WiFi sensing toolbox for robotics
third_party/wifi-sensing/vendor/WiROS/README.md:3:WiROS is a plug-and-play WiFi sensing toolbox allowing researchers to access coarse grained WiFi signal strength (RSSI), fine grained WiFi channel state information (CSI), and other MAC-layer information (device address, packet id’s or frequency-channel information). Additionally, WiROS open-sources state of-art algorithms to calibration and process WiFi measurements to furnish accurate bearing information for received WiFi signals. 
third_party/wifi-sensing/vendor/WiROS/README.md:5:This is an index repository to access the following components of WiROS
third_party/wifi-sensing/vendor/WiROS/README.md:6:1. [**CSI Node**](https://github.com/ucsdwcsng/wiros_csi_node) - Extends the Nexmon CSI toolkit[1] to provide a ROS overlay. 
third_party/wifi-sensing/vendor/WiROS/README.md:7:2. [**Processing Node**](https://github.com/ucsdwcsng/wiros_processing_node) - Provide calibration and post-processing of WiFi CSI measurments. Open-sources mulitple state-of-art bearing extraction algorithms to measure both the angle of arrival (at the receiver) and angle of departure (from the transmitter) of the WiFi signal.
third_party/wifi-sensing/vendor/WiROS/README.md:8:3. [**RF Messages format**](https://github.com/ucsdwcsng/rf_msgs) - Custom ROS messages to structure WiFi measurements information. 
third_party/wifi-sensing/vendor/WiROS/README.md:12:1. Easily integrate WiFi channel state measurements, received signal strength and other WiFi MAC-layer information into your robot sensor stack. 
third_party/wifi-sensing/vendor/WiROS/README.md:13:2. Exposes all relevant measurements as accessible ROS topics. See [`rf_msgs`](https://github.com/ucsdwcsng/rf_msgs) for more details.  
third_party/wifi-sensing/vendor/WiROS/README.md:20:To get started with WiROS, clone these repositories into the `src` folder of your catkin workspace, and follow the [README](https://github.com/ucsdwcsng/wiros_csi_node/blob/main/README.md) in the [CSI Node](https://github.com/ucsdwcsng/wiros_csi_node) to configure your hardware.   
third_party/wifi-sensing/vendor/WiROS/README.md:22:## Example usage of WiROS 
third_party/wifi-sensing/vendor/WiROS/README.md:24:WiROS can be easily leveraged to incorporate WiFi sensors to solve many applicable problems in robotics. We provide the following sample use-cases:
third_party/wifi-sensing/vendor/WiROS/README.md:26:1. **Kidnapped Robot Problem**: A lost robot in an indoor envrionment can be conveniently localized using WiROS. Given a prior map of the existing Access points and additional details of their antenna geometry, the robot's location can be triangulated in a space. 
```

