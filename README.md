# 🤖 고인돌 유적지 자율 순찰 로봇

전북 팀지컬 AI 기반 고창 고인돌 유적지 무인 순찰 시스템

## 🎯 프로젝트 개요

- **목적**: 고인돌 유적지 24시간 무인 순찰
- **기술**: ROS2 Humble, Gazebo, Navigation2, SLAM, YOLOv8
- **로봇**: TurtleBot3 Waffle (2배 확대)

## 📌 주요 기능

### Phase 1: 수동 탐색
- 키보드로 로봇 조종
- 's' 키로 waypoint 저장
- JSON 파일 생성

### Phase 2: 자동 순찰
- JSON 파일 로드
- Navigation2로 자동 주행
- 장애물 회피

### Phase 3: 객체 인식
- YOLOv8 기반 탐지
- VLM 자연어 처리
- 실시간 모니터링

## 🛠️ 시스템 구성
```
센서:
- 2D/3D LiDAR
- RGB + Depth 카메라
- IMU, Odometry

소프트웨어:
- SLAM Toolbox
- Navigation2
- RViz2 시각화
```

## 🚀 실행 방법

### 1. 환경 설정
```bash
cd ~/my_robot_lim_last
colcon build --packages-select my_robot
source install/setup.bash
```

### 2. Gazebo 실행
```bash
ros2 launch my_robot gazebo_with_robot.launch.py \
  world:=$HOME/my_robot_lim_last/src/my_robot/worlds/gochang_dolmen_park.world
```

### 3. SLAM 실행
```bash
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
```

### 4. 수동 탐색 (Phase 1)
```bash
# 터미널 1: 키보드 조종
ros2 run teleop_twist_keyboard teleop_twist_keyboard

# 터미널 2: waypoint 저장
ros2 run my_robot manual_exploration.py
```

### 5. 자동 순찰 (Phase 2)
```bash
ros2 run my_robot auto_patrol.py \
  --waypoints-file path/to/waypoints.json
```

### 6. KITTI 스타일 시각화
```bash
ros2 launch my_robot kitti_visualization.launch.py
```

## 📁 폴더 구조
```
my_robot_lim_last/
├── src/
│   └── my_robot/
│       ├── launch/          # Launch 파일
│       ├── config/          # 설정 파일
│       ├── worlds/          # Gazebo world
│       ├── models/          # 3D 모델
│       └── scripts/         # Python 스크립트
└── data/                    # 실험 데이터
```

## 💡 기술적 특징

- ✅ Waypoint 기반 자율 순찰
- ✅ KITTI 스타일 포인트 클라우드 시각화
- ✅ VLM 자연어 명령 처리
- ✅ 실시간 객체 인식 및 추적
- ✅ 장애물 회피 및 경로 재계획

## 🔮 향후 계획

1. 실제 로봇 하드웨어 이식
2. VLM 기반 자연어 제어 강화
3. 다양한 환경으로 확장 (공장, 창고, 공원 등)

## 📝 개발 환경

- Ubuntu 22.04 LTS
- ROS2 Humble
- Gazebo Classic
- Python 3.10
