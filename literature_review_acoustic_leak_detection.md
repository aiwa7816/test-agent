# 基于声像仪图像的智能漏气异常检测——文献检索、分类与聚类

## 研究背景与目标

**应用场景**：地铁车辆车底管道漏气检测  
**工作压力**：0.6 MPa  
**阵列频率响应**：20–60 kHz（超声频段）  
**泄漏部位**：制动管路软管、空气管路连接部分  
**泄漏孔径**：0.5–2 mm  
**核心科学问题**：声像仪（波束形成）已完成声源定位，需判别"亮斑是否为泄漏"——即在声源定位图像层面实现泄漏/非泄漏的智能异常检测。

---

## 一、文献分类体系

根据检索结果，将相关研究按**技术路线**分为以下六大类：

| 类别编号 | 技术路线 | 核心思路 | 代表性工作数量 |
|:---:|:---|:---|:---:|
| I | 声学成像硬件与波束形成算法 | 阵列设计、波束形成优化、声源可视化 | 6 |
| II | 泄漏声发射物理机理研究 | 湍流射流噪声、孔径-频率-压力关系 | 3 |
| III | 传统机器学习分类方法 | 手工特征提取 + SVM/RF/XGBoost | 5 |
| IV | 深度学习信号处理方法 | CNN/LSTM/Transformer处理1D声学信号 | 6 |
| V | 图像级异常检测方法 | 声像图/频谱图 + 视觉异常检测模型 | 5 |
| VI | 多模态融合与系统集成 | 声学-视觉融合、AI辅助决策系统 | 5 |

---

## 二、各类文献详细分析

### 第I类：声学成像硬件与波束形成算法

本类研究聚焦于"如何获得高质量的声源定位图像"，是后续异常检测的数据基础。

| # | 文献 | 年份 | 核心贡献 | 关键技术指标 |
|:---:|:---|:---:|:---|:---|
| 1 | Ultrasonic Beamforming-Based Visual Localisation of Minor and Multiple Gas Leaks Using a MEMS Microphone Array [Sensors, 25(10), 3190] | 2025 | 基于MEMS数字麦克风阵列的超声波束形成气体泄漏定位成像；用Hilbert变换替代FFT节省计算资源 | 检测距离0.6–3m；最小泄漏24 mL/min；实时嵌入式实现 |
| 2 | Acoustic Imaging Method for Gas Leak Detection and Localization Using Virtual Ultrasonic Sensor Array [Sensors, 24, 1366] | 2024 | 仅用2个超声传感器构建虚拟阵列，通过扫描+交叉功率谱实现泄漏成像定位 | 大幅降低硬件成本；阵列孔径不受物理限制 |
| 3 | Enhanced acoustic monitoring using semi-coprime microphone array and joint spatial-frequency filtering [EURASIP J. Audio Speech Music Process.] | 2025 | 半互质阵列(SCA)设计，13个麦克风实现2.2°波束宽度和-12.4 dB旁瓣 | 高分辨率+有效旁瓣抑制 |
| 4 | Fluke SV600 Fixed Acoustic Imager for railway leak detection [TRB IDEA Safety-48] | 2021 | 固定式声学成像仪用于铁路制动管路漏气；确定30–45 kHz频段、45 dB最低检测阈值 | 铁路场景实证；频段/阈值优化 |
| 5 | FLIR Si1-LD handheld acoustic camera [商业产品/应用报告] | 2024 | 96元MEMS阵列，2–100 kHz，用于铁路制动空气泄漏检测与量化 | 2.5m距离检测0.01 L/min泄漏；带通滤波背景噪声抑制 |
| 6 | GB/T 45348-2025 声源定位成像系统技术规范 | 2025 | 中国国家标准，规定声源定位成像系统架构、功能/性能要求和测试方法 | 标准化参考 |

**研究现状总结**：波束形成声学成像技术已较成熟，MEMS阵列使硬件趋于小型化和低成本化。但现有系统**仅完成"定位"**，即输出亮斑位置，尚未系统解决"亮斑语义判别"问题。

---

### 第II类：泄漏声发射物理机理研究

本类研究为异常检测提供物理先验知识，揭示泄漏声学信号的产生机制。

| # | 文献 | 年份 | 核心贡献 | 关键发现 |
|:---:|:---|:---:|:---|:---|
| 1 | The Characteristics of Acoustic Emissions Due to Gas Leaks in Circular Cylinders [Applied Sciences, 13(17), 9814] | 2023 | 理论建模+实验：泄漏声发射由孔口湍流的波动雷诺应力(FRS)作为集中力源激励圆柱壳振动产生 | 0.2mm孔@2bar峰值频率173.4 kHz；1.2mm孔@4bar峰值频率108.1 kHz；频率随孔径增大而降低 |
| 2 | All-Optical, Air-Coupled Ultrasonic Detection of Low-Pressure Gas Leaks and Observation of Jet Tones in the MHz Range [Sensors, 23(12), 5665] | 2023 | 光机超声传感器检测小孔径气体泄漏；揭示低Re下的射流音调(jet tones)和高Re下的宽带超声噪声 | 30-gauge针头(~0.16mm)射流音调间隔~60 kHz；孔径越小，谐波间隔越大、频率越高 |
| 3 | Acoustic impedance of orifices: measurements and CFD predictions [J. Sound Vib.] | 经典 | 孔口声学阻抗建模；URANS仿真验证不同L/D比孔口的声学响应 | 提供孔口声学放大效应的理论基础 |

**研究现状总结**：0.5–2 mm孔径在0.6 MPa压力下的泄漏属于高Re湍流射流，声学特征为宽带超声噪声（覆盖20–60 kHz频段）。这意味着泄漏在声像仪上的表现为**宽带高能亮斑**，与窄带机械噪声或电气噪声在频谱分布上存在可区分性。

---

### 第III类：传统机器学习分类方法

本类研究从声学信号中提取手工特征，用传统分类器判别泄漏状态。

| # | 文献 | 年份 | 核心贡献 | 方法/精度 |
|:---:|:---|:---:|:---|:---|
| 1 | Machine learning-based platform for leakage detection using AE sensor [Sensors, 23, 3226] | 2023 | 提取11个时域+14个频域特征；评估NN/DT/RF/KNN分类器 | Random Forest最佳；多压力多尺寸泄漏检测 |
| 2 | Leak State Detection and Size Identification with Novel AE Intensity Index and Random Forest [Sensors, 23, 9087] | 2023 | 提出AE活动强度指数曲线(AIIC)；贝叶斯集成变点检测+RF泄漏尺寸分类 | 高精度多工况泄漏状态和尺寸识别 |
| 3 | Latent Leakage Fault Identification for Key Pneumatic Units in EMU Braking System [Applied Sciences, 9(2), 300] | 2019 | Kalman滤波+序贯概率比检验(SPRT)+SVM用于动车组制动继动阀潜隐泄漏诊断 | SVM小样本条件100%故障识别率；内外泄漏分类 |
| 4 | Compressed air leak detection using ML classifiers for ultrasonic microphone arrays [IEEE, 10950451] | 2025 | 在超声麦克风阵列自动化泄漏检测中，训练ML分类器抑制假阳性 | 大幅减少假阳性，不影响真阳性检测 |
| 5 | Early detection of air leakage in IoT-connected compressors (benchmark) [Scientific Reports] | 2025 | 对比SVM/RF/XGBoost/DT/KNN在压缩空气泄漏检测中的性能 | XGBoost/SVM+UEDSM采样最优；F1>80%提前数分钟预警 |

**研究现状总结**：传统ML在**信号级**泄漏判别上已证明有效，尤其RF和SVM在小样本工况下表现良好。但这些方法处理的是**原始时域/频域信号特征**，而非声像仪输出的**二维空间图像**。

---

### 第IV类：深度学习信号处理方法

本类研究将声学信号转化为时频表示后用深度网络直接学习。

| # | 文献 | 年份 | 核心贡献 | 方法/精度 |
|:---:|:---|:---:|:---|:---|
| 1 | Multi-Fluid Pipeline Leak Detection Using Savitzky–Golay Scalograms and Lightweight Vision Transformer [PMC, 2025] | 2025 | SG滤波CWT时频图 + ResNet18局部特征 + 轻量ViT全局特征 + ANN分类 | 98.60%精度，100%召回率；0.3/0.5/1mm泄漏分类 |
| 2 | Multi-Scale Frequency-Aware Transformer (MSFAT) for Pipeline Leak Detection [Sensors, 25(20), 6390] | 2025 | 频率感知嵌入层+多头频率注意力+自适应噪声滤波(ANF)+多尺度特征聚合 | 端到端；多SNR条件下稳定检测；无ANF时精度降至93.1% |
| 3 | AE-Based Pipeline Leak Detection Using Customized 1D-DenseNet [Sensors, 25(4), 1112] | 2025 | EWT自适应频率分解+自适应阈值去噪+1D-DenseNet密集连接 | 检测精度99.76% |
| 4 | Spatio-Temporal Feature Extraction Using 1D-CNN-LSTM [Applied Sciences, 14(22), 10339] | 2024 | 一维CNN提取空间特征 + LSTM建模时间依赖 | 端到端，无需传统特征提取 |
| 5 | Pipeline Leak Detection Using CWT Image + DBN-GA-LSSVM [Sensors, 24(12), 4009] | 2024 | CWT时频图 + 深度置信网络 + 遗传算法优化LSSVM | 在噪声环境区分泄漏/背景 |
| 6 | Multi-source deep evidence fusion (CNN-LSTM-DS) for natural gas pipeline [Eng. Res. Express, 2026] | 2026 | 分布式光纤+次声传感器多源信号；自适应VMD + CNN-LSTM并行特征提取 + D-S证据融合 | F1=97.09%；≤6mm泄漏@5MPa |

**研究现状总结**：深度学习方法在声学信号处理上已达到极高精度（>97%），但主要处理的是**一维信号或其时频变换图**。**直接处理声像仪输出的二维声源定位图像（空间声功率谱叠加可见光图像）作为检测输入**的研究尚为空白。

---

### 第V类：图像级异常检测方法

本类研究将声学信息转化为图像后用视觉异常检测框架处理，与本课题直接相关。

| # | 文献 | 年份 | 核心贡献 | 方法 |
|:---:|:---|:---:|:---|:---|
| 1 | From Vision to Sound: Advancing Audio Anomaly Detection with Vision-Based Algorithms [arXiv:2502.18328] | 2025 | 将视觉异常检测(VAD)算法迁移到音频异常检测；利用预训练特征提取器在频谱图上逐patch计算异常分数 | PatchCore/EfficientAD等VAD方法→频谱图；像素级异常定位 |
| 2 | EfficientAD: Accurate Visual Anomaly Detection at Millisecond-Level Latencies [WACV 2024, arXiv:2303.14535] | 2024 | Student-Teacher模型检测局部异常 + 自编码器检测全局异常；毫秒级推理 | MVTec AD上99.1% image AUROC；可直接用于频谱图/声像图 |
| 3 | Identify Defects in Air Compressors Using Spectrogram Images [MATLAB/EfficientAD示例] | 2024 | 将EfficientAD直接应用于空压机声学频谱图异常检测；仅需正常样本训练 | 频谱图→异常热图；假阳性/假阴性可视化分析 |
| 4 | PatchCore: Towards Total Recall in Industrial Anomaly Detection [CVPR 2022] | 2022 | 预训练CNN骨干网特征 + coreset子采样记忆库 + 最近邻异常评分 | 99.6% image AUROC; 98.4% pixel AUROC (MVTec AD) |
| 5 | DCASE 2025 Challenge Task 2: First-Shot Unsupervised Anomalous Sound Detection [arXiv:2506.10097] | 2025 | 机器状态监测的无监督异常声音检测；自编码器基线+自监督分类+对比学习 | 域泛化；首次遇见机器类型的快速部署 |

**研究现状总结**：视觉异常检测（EfficientAD、PatchCore等）已被成功迁移到声学频谱图/音频异常检测领域，核心优势是**仅需正常样本训练（单分类/无监督）**。但目前应用对象是频谱图（时频图），**尚未有研究直接将这些方法应用于波束形成输出的空间声功率谱图像（声像仪输出图像）**。

---

### 第VI类：多模态融合与系统集成

本类研究关注声学信息与其他模态的融合以及面向应用的完整系统。

| # | 文献 | 年份 | 核心贡献 | 融合策略 |
|:---:|:---|:---:|:---|:---|
| 1 | AI-based image/ultrasonic convergence camera for gas leak detection in petrochemical plants [PMC, 11002273] | 2024 | 超声相机+YOLO管道目标检测；将声学定位输出与视觉管道检测对齐以消除假阳性 | 决策级融合：YOLO定位管件区域→超声确认泄漏；mAP50=0.45 |
| 2 | Unified AI Framework: Acoustic-Vision Leak Detection (MPSF) [Buildings, 16(9), 1698] | 2026 | FLUKE ii910超声相机；概率多阶段融合算法(MPSF)将声学亮斑像素面积转化为物理泄漏量 | 像素级声学-视觉融合→泄漏功率量化(11.0 kW) |
| 3 | Micro-Leakage Image Recognition for Buried Gas Pipelines [Sensors, 23, 3956] | 2023 | 管道机器人内窥图像；YOLOv5+BiFPN+小目标检测层 | 视觉目标检测；mAP=96.31%；最小可识别1mm泄漏 |
| 4 | Recurrent Autoencoder Ensembles for Brake Operating Unit Anomaly Detection on Metro Vehicles [CMC, 73(1)] | 2022 | 循环自编码器集成用于地铁制动操作单元异常检测 | 时序压力信号→LSTM-AE异常评分 |
| 5 | Multi-track Intelligent Inspection Robot for Urban Rail Vehicles [中车时代电气] | 2022 | 地铁车底智能巡检机器人；SLAM+多自由度机械臂+高清光学+AI异常预警 | 视觉检测变形/松动/缺失 |

**研究现状总结**：已有将超声相机与视觉目标检测融合来抑制假阳性的尝试，也有面向地铁车底的智能巡检机器人平台。但**声像仪图像智能判别+车底移动平台实时检测**的完整方案尚未形成。

---

## 三、文献聚类分析

按照研究的**核心技术维度**，对上述文献进行聚类：

### 聚类1：声学信号获取与预处理
```
├── 阵列设计优化（互质阵列、MEMS阵列小型化）
├── 波束形成算法改进（Hilbert变换替代FFT、MVDR/DAS）
├── 频段选择与带通滤波（30-45 kHz优选频段）
└── 降噪预处理（VMD、EWT、SG滤波、CEEMDAN）
```

### 聚类2：泄漏物理特征建模
```
├── 湍流射流噪声机理（FRS、集中力模型）
├── 孔径-压力-频率映射关系
├── 射流音调(jet tones)与宽带噪声的雷诺数转变
└── 声发射传播与衰减特性
```

### 聚类3：分类/识别算法
```
├── 一维信号分类
│   ├── 传统ML（RF、SVM、XGBoost + 手工特征）
│   └── 深度学习（1D-CNN、LSTM、DenseNet、Transformer）
├── 二维图像分类
│   ├── 时频图（CWT/STFT频谱图）+ CNN/ViT
│   └── 声源图像 + 目标检测（YOLO）← 新兴方向
└── 异常检测（单分类/无监督）
    ├── 自编码器重构误差
    ├── Student-Teacher（EfficientAD）
    └── 记忆库匹配（PatchCore）
```

### 聚类4：应用系统集成
```
├── 手持式巡检（FLIR Si1-LD、SUTO S532）
├── 固定式监测（Fluke SV600 + 铁路自动化）
├── 移动机器人平台（地铁车底巡检机器人）
└── 多模态融合系统（声学+视觉+AI决策）
```

---

## 四、国内外研究进展对比

| 维度 | 国际研究进展 | 国内研究进展 |
|:---|:---|:---|
| 声学成像硬件 | FLIR(96元阵列)、Fluke(SV600)、SONOTEC成熟商业产品；学术界MEMS阵列小型化研究活跃 | SUTO(希尔思)代理64元MEMS阵列产品；GB/T 45348-2025发布声源定位成像标准 |
| 泄漏物理机理 | 系统性地建立了FRS理论模型、射流音调规律 | 偏重工程应用验证，理论建模较少 |
| AI泄漏判别 | IEEE 2025发表超声阵列ML分类器抑制假阳性；EfficientAD/PatchCore迁移至声学频谱图 | 深度学习管道泄漏检测（AE+DL）研究较多；声像仪图像智能判别研究极少 |
| 轨道交通应用 | TRB IDEA项目实证铁路制动管路声学成像检漏；FLIR Si1-LD定位铁路应用 | 中车开发车底巡检机器人（视觉为主）；EMU制动阀泄漏诊断（压力信号+SVM） |
| 系统集成 | 超声相机+YOLO视觉融合（石化场景）；声学-视觉概率融合量化框架 | 巡检机器人+SLAM+AI异常预警（仅视觉） |

---

## 五、关键科学问题与技术瓶颈

基于文献分析，识别出以下关键科学问题：

### 问题1：声像仪输出图像中"亮斑"的语义判别

**现状**：波束形成算法输出的是空间声功率谱，任何超声频段的声源都会产生亮斑——包括泄漏、机械摩擦、电气放电、反射/绕射伪影等。目前**无系统性研究**直接在声像仪图像层面建立泄漏亮斑的判别模型。

**机理分析**：
- 泄漏亮斑特征：宽带能量分布、空间位置与管路高度相关、形状近似圆形/椭圆形、强度随压力变化
- 干扰亮斑特征：窄带（机械噪声）、空间分布规律性强（旁瓣伪影）、强度不随充压变化

### 问题2：单分类/少样本条件下的异常检测

**现状**：实际工况中泄漏样本稀少且类型多样，传统监督学习需要大量标注数据。无监督/单分类方法（如PatchCore、EfficientAD）仅需正常样本训练，但**尚未在声像仪图像上验证可行性**。

### 问题3：实时性与移动检测的约束

**现状**：车底移动检测要求算法在有限计算资源下实时运行。EfficientAD已证明毫秒级推理可行，但声像仪数据的帧率、分辨率与计算负载的平衡需要专门研究。

### 问题4：多源干扰下的鲁棒性

**现状**：车底环境存在多种超声干扰源（电气设备、HVAC系统、金属碰撞等）。IEEE 2025的研究证明ML分类器可以有效抑制假阳性，但其方法基于原始信号特征，而非图像特征。

---

## 六、研究机遇与建议的技术路线

基于文献缺口分析，提出以下值得探索的方向：

### 方向A：视觉异常检测方法迁移到声像仪图像

**原理**：将声像仪输出的声源定位图像视为"工业视觉检测"任务，利用PatchCore/EfficientAD等SOTA方法，仅用正常状态（无泄漏）的声像仪图像训练模型，检测时输出异常热图定位泄漏亮斑。

**优势**：
- 无需泄漏标注样本
- 利用成熟的预训练视觉特征(ImageNet backbone)
- 毫秒级推理满足实时性
- 可解释性强（异常热图）

### 方向B：声学-空间特征联合判别

**原理**：不仅利用声像图的二维空间信息，还提取波束形成输出的频谱分布、时间稳定性等特征，构建多维度判别框架。

**可用特征**：
- 空间特征：亮斑形状、面积、位置、与管路的空间关系
- 频谱特征：宽带/窄带比、频谱平坦度、频谱质心
- 时域特征：时间稳定性（泄漏持续存在 vs 瞬态噪声）
- 压力响应：充压/泄压过程中亮斑强度变化

### 方向C：物理信息引导的深度学习

**原理**：将泄漏声学机理（射流噪声的宽带特性、孔径-频率关系等物理先验）嵌入到网络设计中（如频率感知注意力模块、物理约束损失函数），提升模型的泛化能力和可解释性。

### 方向D：声学-视觉融合的轨道交通应用

**原理**：参考已有石化场景的超声相机+YOLO融合方案，针对地铁车底场景，将声像仪输出与可见光图像中的管路/接头目标检测结合，实现"先定位管件→再判别该处是否泄漏"的层级决策。

---

## 七、核心参考文献列表

### 声学成像与波束形成
1. MDPI Sensors 2025, 25(10), 3190 — MEMS阵列超声波束形成泄漏成像
2. MDPI Sensors 2024, 24, 1366 — 虚拟超声传感器阵列泄漏成像
3. EURASIP J. Audio Speech Music Process. 2025 — 半互质麦克风阵列空间滤波
4. TRB IDEA Safety-48, 2021 — 铁路固定声学成像仪压缩空气泄漏检测
5. GB/T 45348-2025 — 声源定位成像系统技术规范

### 泄漏声学机理
6. MDPI Applied Sciences 2023, 13(17), 9814 — 圆柱孔口气体泄漏声发射特性
7. MDPI Sensors 2023, 23(12), 5665 — 小孔径气体泄漏超声射流音调
8. J. Sound Vib. — 孔口声学阻抗测量与CFD预测

### 传统机器学习方法
9. MDPI Sensors 2023, 23, 3226 — AE多特征+RF/KNN泄漏检测平台
10. MDPI Sensors 2023, 23, 9087 — AE强度指数+RF泄漏尺寸分类
11. MDPI Applied Sciences 2019, 9(2), 300 — EMU制动阀Kalman+SPRT+SVM诊断
12. IEEE 2025 (10950451) — 超声阵列ML分类器假阳性抑制
13. Scientific Reports 2025 — IoT压缩机ALDNet+UEDSM泄漏检测

### 深度学习信号处理
14. PMC 2025 (12656461) — SG-CWT时频图+ResNet+轻量ViT
15. MDPI Sensors 2025, 25(20), 6390 — 多尺度频率感知Transformer(MSFAT)
16. MDPI Sensors 2025, 25(4), 1112 — EWT+1D-DenseNet泄漏检测与尺寸分类
17. MDPI Applied Sciences 2024, 14(22), 10339 — 1D-CNN-LSTM时空特征提取
18. IOP Eng. Res. Express 2026, 8, 095404 — CNN-LSTM-DS多源证据融合

### 图像级异常检测
19. arXiv:2502.18328, 2025 — 视觉异常检测算法迁移到音频异常检测
20. arXiv:2303.14535 (WACV 2024) — EfficientAD毫秒级视觉异常检测
21. MATLAB示例 2024 — EfficientAD应用于空压机频谱图异常检测
22. arXiv:2106.08265 (CVPR 2022) — PatchCore工业异常检测
23. DCASE 2025 Task 2 — 首次遇见类型的无监督异常声音检测

### 多模态融合与系统集成
24. PMC 2024 (11002273) — 超声相机+YOLO视觉融合石化泄漏检测
25. MDPI Buildings 2026, 16(9), 1698 — 声学-视觉概率融合泄漏量化(MPSF)
26. MDPI Sensors 2023, 23, 3956 — 管道机器人YOLOv5+BiFPN微泄漏识别
27. CMC 2022, 73(1) — 循环自编码器集成地铁制动单元异常检测
28. 中车时代电气 2022 — 城轨车辆多股道智能巡检机器人
29. Springer CIRAC 2022, vol.1770 — 地铁车底智能巡检机器人设计与控制

### Fraunhofer公开数据集
30. IDMT-ISA-Compressed-Air Dataset (Fraunhofer IDMT) — 压缩空气泄漏声学数据集（多泄漏类型+工业背景噪声；5592个音频文件）

---

## 八、结论与展望

综上所述，当前研究呈现以下格局：

1. **声学成像硬件与算法已成熟**——波束形成定位不再是瓶颈
2. **信号级泄漏检测方法丰富**——但局限于一维信号或时频图处理
3. **视觉异常检测方法已证明可迁移至声学域**——但尚未直接应用于声像仪空间图像
4. **轨道交通场景应用碎片化**——硬件巡检机器人与声学泄漏检测分离发展

**核心创新点**在于：将视觉异常检测方法（EfficientAD/PatchCore等）**直接应用于声像仪输出的声源定位图像**，结合泄漏声学物理先验知识，建立面向地铁车底管道的"亮斑语义判别"方法。这一方向目前在国内外文献中尚属空白，具有明确的学术贡献和工程应用价值。

---

## 九、关键实践问题：声压值提取的OCR困境与解决方案

### 9.1 问题描述

当前声像仪仅输出声源定位图像（含伪彩色热图叠加可见光背景+色标+数值标注），未提供原始频谱及原始声压数据的API接口或文件导出。为获取声压峰值等定量信息，目前采用OCR图像识别方式提取图中标注的dB数值。但面临以下问题：

| 误差来源 | 具体表现 |
|:---|:---|
| 文字密集重叠 | 多个标注值在图像中相互遮挡，OCR无法正确分割 |
| 标注角度倾斜 | 文字非水平排列，常规OCR识别率显著下降 |
| 色标自动缩放 | 不同帧/工况下色标范围(dB_min~dB_max)动态变化，同一颜色对应不同物理值 |
| 截图分辨率有限 | 压缩/降分辨率后数字细节丢失，OCR误读率升高 |
| 结果异常 | 部分工况下出现明显不符合声学规律的峰值读数 |

### 9.2 解决方案体系

#### 方案一（推荐）：色标反向映射法——完全绕过OCR

**核心思路**：不读取图中的数字文本，而是通过图像中伪彩色像素的颜色值，反向查找对应的物理量(dB)。

**实现步骤**：

```
步骤1：色标区域提取
  ├── 从图像中裁剪色标条(colorbar)区域
  ├── 沿色标条采样每个像素的RGB/HSV值
  └── 建立颜色→归一化位置(0~1)的映射表(LUT)

步骤2：色标端值校准
  ├── 方案A：对色标两端的数值做一次性OCR（仅2个数字，精度要求低）
  ├── 方案B：如果色标范围固定/已知，直接手动设定dB_min和dB_max
  └── 方案C：利用物理约束（如环境背景噪声下限、仪器量程上限）约束范围

步骤3：逐像素反向映射
  ├── 对声源热图区域每个像素的RGB值
  ├── 在色标LUT中查找最近邻（欧氏距离最小）
  ├── 获得归一化位置 p ∈ [0,1]
  └── 计算物理值：dB = dB_min + p × (dB_max - dB_min)

步骤4：峰值提取
  └── 在反向映射得到的2D dB矩阵中直接求最大值/局部极值
```

**关键Python工具**：
- `unmap` 库（scienxlab/unmap）：专门从伪彩色图像恢复标量数据，支持自动colormap猜测
- OpenCV FLANN反向查找：构建256色LUT后用FLANN最近邻匹配
- matplotlib colormap逆映射：已知colormap类型时直接计算

**误差分析**：
- 典型误差 < 色标分辨率的1/256（即当色标范围60 dB时，分辨率约0.23 dB）
- 远优于OCR的多dB级误差
- 对JPEG压缩伪影敏感，建议使用PNG无损格式

#### 方案二：数据源头获取——联系厂商获取原始数据接口

**核心思路**：从硬件/软件层面获取波束形成算法的原始输出数值数据，绕过图像层面的间接提取。

**可行路径**：

| 路径 | 具体方案 | 可行性 |
|:---|:---|:---|
| A. 厂商API/SDK | 联系声像仪厂商获取数据导出接口（如CRY8500提供208通道原始波形API） | 取决于具体设备型号 |
| B. 软件数据导出 | 查看声像仪配套软件是否支持导出csv/mat/h5格式的波束形成结果 | 多数专业级软件支持 |
| C. 屏幕录制+帧同步 | 将仪器屏幕以无损格式录制，保证色标信息完整 | 次优方案 |
| D. Acoular开源重建 | 如能获取多通道原始音频(.wav)，用Acoular开源库重新进行波束形成 | 需要原始麦克风信号 |

**参考**：
- CRYSOUND CRY8500声像派：明确提供"实时阵列信号波形数据输出API"，支持.wav/.cdat数据导出
- Acoular (Python开源库, v26.04)：`BeamformerBase.synthetic(freq)` 直接返回各网格点的声压平方值(Pa²)
- GFAi NoiseImage软件：显示色标最大值Lp(dB)、鼠标悬停点声压级，数据可导出

#### 方案三：物理约束后处理——异常值剔除与校正

**核心思路**：在OCR识别结果的基础上，利用声学物理规律对异常值进行检测和校正。

**物理约束规则**：

```
规则1：量程约束
  └── 声压级必须在仪器量程内（如 0 ≤ Lp ≤ 120 dB）

规则2：空间连续性
  └── 相邻帧/相邻位置的声压峰值变化不应超过物理合理范围
      （如移动速度v下，Δt时间内声压变化 ≤ 预期衰减量）

规则3：距离衰减律
  └── 自由声场点源：ΔLp ≈ 20·lg(r1/r2) 
      如检测距离恒定，同一泄漏源的声压峰值应稳定

规则4：频率-压力关联
  └── 在固定工作压力(0.6 MPa)下，泄漏声压水平应与孔径正相关
      0.5mm孔 < 1mm孔 < 2mm孔（给定距离）

规则5：时间稳定性
  └── 真实泄漏声压应稳定持续，瞬态尖峰（单帧出现）大概率为OCR误读
```

**异常检测算法**：
- 中值滤波：对时间序列的声压读数做中值滤波，剔除离群值
- 3σ准则：基于滑动窗口统计，超出3倍标准差的读数标记为异常
- 物理模型校核：用泄漏声压的理论预估值作为参考，偏差超阈值则触发重新提取

#### 方案四（推荐的最终方案）：绕过声压值提取——直接图像异常检测

**核心思路**：重新审视研究目标——判别"亮斑是否为泄漏"**不一定需要精确的dB数值**。可直接在图像层面建立判别模型，完全跳过声压值提取环节。

**论证**：

| 传统思路（需要dB值） | 新思路（直接图像判别） |
|:---|:---|
| 声像仪图像 → OCR提取dB值 → 阈值/规则判断 | 声像仪图像 → 视觉特征提取 → 异常/正常分类 |
| 精度受OCR限制 | 精度由模型能力决定 |
| 需要建立dB阈值规则 | 自动学习判别边界 |
| 丢失空间分布信息 | 充分利用空间形态信息 |

**为什么可行**：
1. 泄漏亮斑与非泄漏亮斑在图像上的**视觉模式不同**（形状、颜色分布、空间位置、面积）
2. PatchCore/EfficientAD等方法**仅需正常样本**训练，检测时输出像素级异常热图
3. 无需OCR、无需精确dB值、无需色标校准——直接端到端处理
4. 已有成功先例：EfficientAD应用于空压机声学频谱图异常检测（MATLAB官方示例，2024）

**实施路径**：
```
阶段1：数据收集
  ├── 收集正常状态（无泄漏）下车底各位置的声像仪截图（越多越好，覆盖不同背景）
  └── 保证图像格式统一（分辨率、色标范围固定或归一化）

阶段2：模型训练（仅需正常样本）
  ├── 方案A：PatchCore —— 预训练CNN提取patch特征 → 记忆库存储 → KNN异常评分
  └── 方案B：EfficientAD —— Student-Teacher + 自编码器 → 毫秒级推理

阶段3：在线推理
  ├── 输入：实时声像仪截图
  ├── 输出：(1)异常/正常判定 (2)异常热图（定位可疑泄漏区域）
  └── 阈值：基于验证集ROC曲线确定最优分类阈值

阶段4：验证
  ├── 人工标注泄漏/非泄漏样本进行评估
  └── 计算AUROC、精确率、召回率
```

### 9.3 建议的优先级

| 优先级 | 方案 | 理由 |
|:---:|:---|:---|
| ★★★ | 方案四：直接图像异常检测 | 从根本上绕过OCR问题；与研究目标最契合；方法创新性强 |
| ★★☆ | 方案一：色标反向映射 | 如确实需要定量dB值（如论文中对比分析），此法精度高且实现简单 |
| ★★☆ | 方案二：获取原始数据 | 彻底解决问题但受硬件厂商限制 |
| ★☆☆ | 方案三：物理约束后处理 | 作为OCR结果的补充校验有价值，但不解决根本问题 |

### 9.4 色标反向映射的参考代码框架

```python
import numpy as np
import cv2
from scipy.spatial import cKDTree

class ColorbarInverseMapper:
    """从声像仪伪彩色图像中反向提取声压级数值"""
    
    def __init__(self, colorbar_img, db_min, db_max):
        """
        参数:
            colorbar_img: 裁剪后的色标条图像 (H, W, 3) BGR
            db_min: 色标下限 (dB)
            db_max: 色标上限 (dB)
        """
        self.db_min = db_min
        self.db_max = db_max
        
        # 沿色标条采样颜色，建立查找表
        h = colorbar_img.shape[0]
        mid_col = colorbar_img.shape[1] // 2
        self.lut_colors = colorbar_img[:, mid_col, :].astype(np.float32)
        
        # 归一化位置：顶部=1(最大值)，底部=0(最小值)
        self.lut_values = np.linspace(db_max, db_min, h)
        
        # 建立KD-Tree加速最近邻搜索
        self.tree = cKDTree(self.lut_colors)
    
    def inverse_map(self, heatmap_img):
        """
        将伪彩色热图区域反向映射为dB矩阵
        
        参数:
            heatmap_img: 声源热图区域 (H, W, 3) BGR
        返回:
            db_map: 声压级矩阵 (H, W)
        """
        h, w = heatmap_img.shape[:2]
        pixels = heatmap_img.reshape(-1, 3).astype(np.float32)
        
        # KD-Tree最近邻查找
        _, indices = self.tree.query(pixels)
        
        # 映射为dB值
        db_map = self.lut_values[indices].reshape(h, w)
        return db_map
    
    def get_peak(self, heatmap_img):
        """提取声压峰值及其位置"""
        db_map = self.inverse_map(heatmap_img)
        peak_val = np.max(db_map)
        peak_pos = np.unravel_index(np.argmax(db_map), db_map.shape)
        return peak_val, peak_pos
```
