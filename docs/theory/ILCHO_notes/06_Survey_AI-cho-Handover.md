# Survey: AI/ML cho Handover (tập trung NTN/LEO)

> File này là **khung để bạn viết survey**: phân loại, bảng công trình tiêu biểu, phương pháp đánh
> giá, khoảng trống nghiên cứu, và cách định vị đề tài. 🟢 = khảo sát ngoài (nguồn cuối file).

---

## 1. Bức tranh vấn đề

Handover management có 4 câu hỏi con — AI có thể can thiệp vào bất kỳ câu nào:

| Câu hỏi | Quyết định gì | Kỹ thuật AI hay dùng |
|---------|---------------|----------------------|
| **WHEN** (khi nào chuẩn bị/thực thi HO) | thời điểm trigger | dự đoán chuỗi thời gian (LSTM/GRU), phân loại |
| **WHERE** (HO tới cell/vệ tinh/beam nào) | chọn target | RL/MARL, phân loại, tối ưu tổ hợp học |
| **HOW MANY** (chuẩn bị bao nhiêu cell ứng viên — CHO) | tập ứng viên | RL, học có giám sát, meta-learning |
| **PARAMETERS** (offset/hysteresis/TTT) | tinh chỉnh SON/MRO | RL (contextual bandit, DQN), Bayesian optimization |

🔵 **ILCHO trả lời câu WHERE** (chọn T-LEO), giữ WHEN ở mức luật cố định (sự kiện khoảng cách eq 28),
gộp HOW MANY vào "candidate T-LEO" nhưng không tối ưu số lượng.

---

## 2. Trục phân loại chính cho survey

### 2.1. Trục A — *Dự đoán* (prediction) vs *Ra quyết định* (decision/control) 🟢

Đây là trục **quan trọng nhất** để định vị đề tài "dự đoán handover" của bạn.

| | **Prediction-based** | **Decision/Control-based** |
|--|----------------------|----------------------------|
| Bài toán ML | hồi quy / phân loại / dự báo chuỗi | điều khiển tuần tự (RL) hoặc tối ưu |
| Output điển hình | RSRP/SINR tương lai; xác suất HOF; thời điểm HO tối ưu; cell sẽ mạnh nhất; RVT; thời điểm link suy giảm | hành động HO: đi/không, đi đâu, chuẩn bị cell nào |
| Nhãn/giám sát | cần dữ liệu có nhãn (đo lịch sử) | cần môi trường/simulator + hàm thưởng |
| Ví dụ TN | LSTM dự đoán RSRP → HO sớm; CNN dự đoán ping-pong | DQN chọn cell; bandit chỉnh offset |
| Ví dụ NTN | dự báo RSRP do UE+vệ tinh cùng chuyển động (CNN-LSTM encoder-decoder); dự đoán khả kiến | **ILCHO** (MARL chọn T-LEO); [28] DRL vệ tinh tự quyết |
| Thường ghép với | một bộ quyết định luật cứng phía sau (threshold on prediction) | có thể nuốt luôn phần dự đoán vào state |

> **Chỗ ILCHO gây nhầm lẫn** (xem file 08): Mục VII bài viết *"LEO satellite movement predictions made
> by its MARL system"*. Nhưng chuyển động vệ tinh là **tất định** (Lemma 1) — "dự đoán" ở đây chỉ là
> **lan truyền quỹ đạo Kepler**, không phải học một đại lượng bất định. ILCHO là **decision-based**
> thuần. Nếu đề tài của bạn là *prediction-based*, đây là điểm phân biệt phải nêu rõ.

### 2.2. Trục B — Kỹ thuật học 🟢
- **Supervised**: DNN, CNN, **LSTM/GRU**, Transformer, XGBoost → dự đoán RSRP/HOF/cell tốt nhất. Cần
  dataset nhãn; suy luận nhanh; không tự tối ưu mục tiêu dài hạn.
- **Unsupervised / clustering**: nhóm UE/cell, phát hiện bất thường mobility.
- **RL / DRL**: Q-learning, DQN, Double/Dueling/DRQN, PPO, SAC, Actor-Critic → tối ưu mục tiêu tích
  luỹ (throughput − #HO − #HOF). Cần simulator; khó hội tụ; sample-inefficient.
- **MARL**: IQL, **VDN, QMIX**, QTRAN, QPLEX, MADDPG, MAPPO, COMA → khi có **nhiều UE tương tác** &
  tài nguyên chia sẻ. 🔵 ILCHO = QMIX.
- **Federated Learning**: huấn luyện phân tán, không gom dữ liệu UE → riêng tư; ghép với LSTM cho HO
  prediction.
- **Meta-learning / Transfer**: thích nghi nhanh sang chòm sao/khu vực mới với ít dữ liệu (CHOMET).
- **Graph Neural Network**: topo vệ tinh–UE–ISL dạng đồ thị (HSNF baseline là network-flow, chưa GNN).

### 2.3. Trục C — Môi trường
TN macro / TN ultra-dense small cell / TN mmWave (FR2) / HetNet / **NTN LEO** / NTN MEO-GEO / tích hợp
TN-NTN / HAPS-UAV / high-speed rail.

### 2.4. Trục D — Nơi đặt "bộ não" 🟢
- **UE-centric**: UE tự quyết (cần thông tin & tính toán ở UE).
- **Network-centric / gNB**: gNB hoặc vệ tinh nguồn quyết (VD [28]).
- **Centralized controller / RIC**: near-RT RIC (O-RAN) học tập trung. 🔵 ILCHO.
- **Satellite on-board**: vệ tinh chạy inference (payload tái sinh). 🔵 ILCHO (inference).

### 2.5. Trục E — Tiêu chí tối ưu
số HO ↓ · HOF/RLF ↓ · ping-pong ↓ · throughput/SE ↑ · SNR/SINR ↑ · độ trễ HO ↓ · QoE ↑ ·
fairness (JFI) ↑ · load balance (variance occupancy) ↓ · signaling overhead ↓ · năng lượng ↓.

---

## 3. Bảng công trình tiêu biểu (mở rộng từ Mục II của ILCHO) 🟢🔵

| # | Công trình | Môi trường | Kỹ thuật | WHEN/WHERE/PARAM | Mục tiêu | Hạn chế nêu trong ILCHO / chung |
|---|-----------|-----------|----------|------------------|----------|-------------------------------|
| [21] | Potential-game HO | LEO | Game theory (không học) | WHERE | lợi ích UE | không AI, giả định lý tưởng |
| [22] **HSNF** | LEO | Network-flow / graph, cost matrix | WHERE | QoE đa UE | tính cost mọi cặp real-time bất khả thi ở mega-scale |
| [23] | Cluster tunnel | Satellite B5G | thủ tục (không học) | HOW | ↓ thời gian thủ tục HO | — |
| [24] | QoE-driven HO | Mobile satellite | RL **không DNN** | WHERE | QoE UE-centric | không deep, state nhỏ |
| [25] | Load-aware MARL HO | Satellite | Multi-agent Q-learning | WHERE | ↓#HO, ngân sách kênh | không phân tích QoE/UE |
| [26] **LBSH** | Satellite (NS-3) | Multi-agent Q-learning, reward = RVT+tải+phạt HO | WHERE | load balancing | action space nổ khi ghép Starlink |
| [27] | Successive DQN distributed HO | **OneWeb** | DQN đa tác tử | WHERE | ↑throughput | bỏ qua overhead HO thừa |
| [28] | HO protocol learning | LEO | **DRL, vệ tinh (S-LEO) tự quyết**, UE không gửi MR | WHERE + access delay/collision | ↓ trễ truy nhập, ↓ va chạm | chỉ 3 mặt phẳng, 3 action → curse of dimensionality |
| [30] | Đánh giá CHO 5G NR | LEO NTN | phân tích (không học) | — | chỉ ra CHO gây signaling overhead | động lực cho ILCHO |
| [31] | Seamless HO, service continuity | LEO NTN | đồ thị hiệu năng + chọn target tối ưu | WHERE + WHEN | ↑ thời gian liên tục dịch vụ | không RL |
| **ILCHO** | **Starlink Phase 1-a/2-a/hybrid** | **MARL / QMIX, CTDE, action = N_max** | **WHERE** (T-LEO) | ↑throughput, ↓#HO ổn định, fairness, load balance | *xem file 08* |

**Các nhóm ngoài ILCHO đáng đưa vào survey** 🟢:
- **HO prediction bằng LSTM/CNN** (TN & TN-NTN tích hợp): dự báo RSRP → HO chủ động; giảm ping-pong so
  với A3.
- **Federated + LSTM** cho HO prediction (bảo mật dữ liệu UE).
- **DRL cho MRO/tham số HO** trong TN ultra-dense (chỉnh offset/TTT).
- **Meta-learning cho CHO** (CHOMET) — thích nghi điều kiện thực thi.
- **MARL cho HO trong LEO–TN tích hợp, terminal tốc độ cao** (ví dụ ETRI Journal 2025 — proactive HO
  bằng multi-agent DRL).
- **Graph/GNN cho định tuyến + mobility trong mega-constellation**.
- **AI-native O-RAN cho NTN** (đặt bộ điều khiển HO ở near-RT RIC như ILCHO).

---

## 4. Bốn baseline của ILCHO — giải thích để trích dẫn trong survey 🔵

| Baseline | Thuộc nhóm | Luật chọn target | Trigger thực thi | Điểm yếu bộc lộ khi đông UE |
|----------|-----------|------------------|------------------|----------------------------|
| **MD-CHO** (Minimum Distance) | heuristic hình học | vệ tinh accessible **gần nhất** | A2 khoảng cách `d_serv + O_off < ζ` | mọi UE gần nhau → cùng chọn 1 vệ tinh → nghẽn → HOF ↑, #HO ↑ |
| **MVT-CHO** (Maximum Visible Time) | heuristic hình học | vệ tinh **RVT dài nhất** | A2 khoảng cách | tương tự MD; kém khi ít vệ tinh khả kiến (Phase 1) |
| **HSNF** [22] | tối ưu tổ hợp (không học) | network-flow, ma trận chi phí (throughput + băng thông còn lại) | — | tính cost real-time cho mọi cặp UE–vệ tinh bất khả thi ở mega-scale → HOF ~10 không giảm |
| **LBSH** [26] | MARL (Q-learning độc lập) | reward = RVT + tải thấp + phạt HO lớn | — | action = chỉ số vệ tinh → **không gian nổ** khi lên Starlink → không hội tụ tốt → #HO, HOF cao |

**Thông điệp so sánh của ILCHO**: heuristic đơn tiêu chí (MD/MVT) và MARL không cắt action space
(LBSH) đều **sụp khi số UE tăng** vì tương quan UE; ILCHO giữ ổn định nhờ (a) reward đa mục tiêu phi
tuyến, (b) action space = N_max, (c) QMIX xử lý tương tác đa UE.

---

## 5. Phương pháp đánh giá — checklist cho survey 🟢🔵

**Môi trường mô phỏng**: NS-3 (+ module NTN), Python custom (ILCHO: Python 3.11 + PyTorch 2.1.0),
MATLAB Satellite Toolbox, STK, Hypatia/StarPerf (mega-constellation), OMNeT++.

**Mô hình quỹ đạo**: Walker-Delta/Star; SGP4 + TLE thật; ephemeris 3GPP; tham số FCC (ILCHO dùng
Bảng I từ hồ sơ FCC Starlink).

**Mô hình kênh**: 3GPP TR 38.811 / 38.821 (path loss, SF, CL, LoS prob, atmospheric); có/không
Doppler; có/không fading nhanh.

**KPI chuẩn** (nên báo cáo đủ):
- Mobility: #HO/UE/đơn vị thời gian, #HOF, HOF rate, ping-pong rate, RLF, HO interruption time.
- Hiệu năng: throughput/SE trung bình & CDF, SNR/SINR, độ trễ.
- Công bằng & tải: **Jain's Fairness Index** (ILCHO: 0,9798), **variance of channel occupancy**
  (ILCHO Bảng IV), % UE bị "đói".
- Chi phí: signaling overhead, tài nguyên giữ trước (CHO), thời gian huấn luyện, độ phức tạp
  (ILCHO: O(K)).

**Điểm yếu đánh giá thường gặp** (nêu trong phần "limitations of the field"):
- Không có TLE/kênh thật → khó tái lập.
- Thiếu độ lệch chuẩn / số seed / khoảng tin cậy.
- Khu vực địa lý hẹp, không quét vĩ độ.
- Không so cùng một simulator giữa các bài → số liệu không so trực tiếp được.
- Bỏ qua Doppler, UE mobility, lỗi ephemeris, trễ báo hiệu thực.
- Không phân tích chi phí huấn luyện/hội tụ, không bàn online/continual learning.

---

## 6. Khoảng trống nghiên cứu (research gaps) — để đề xuất đề tài 🟢🔵

| # | Khoảng trống | Vì sao mở | Hướng đề tài khả thi |
|---|--------------|-----------|----------------------|
| G1 | **Dự đoán đại lượng bất định** (RSRP/SINR/HOF/tải tương lai) để nuôi CHO — ILCHO chỉ dùng hình học tất định | ILCHO & phần lớn bài NTN né phần "bất định" | LSTM/Transformer dự báo SINR hiệu dụng (gồm fading, tải) N bước tới → điều kiện thực thi CHO thông minh |
| G2 | **UE di động** (handheld, tàu, máy bay, HSR) | ILCHO giả định VSAT cố định | MARL/pred-HO có UE mobility + Doppler biến thiên |
| G3 | **Doppler & lỗi ephemeris** vào bài toán quyết định | ILCHO bỏ qua | robust HO khi ephemeris cũ (T430 hết hạn) / bù Doppler không hoàn hảo |
| G4 | **Online / continual / offline RL** trên near-RT RIC thật | ILCHO train offline 3k–30k episodes | offline RL từ log; continual learning khi chòm sao đổi |
| G5 | **Multi-connectivity / soft HO / make-before-break trong NTN** | ILCHO là hard-HO 1 kết nối | MARL chọn *tập* vệ tinh (DAPS-like) |
| G6 | **Dự đoán tải & phối hợp UE** để tránh nghẽn tập thể | ILCHO chỉ né gián tiếp qua phạt HOF | dự đoán occupancy vệ tinh + MARL có communication giữa agent |
| G7 | **Tối ưu số cell ứng viên CHO** (robustness ↔ overhead) | ILCHO không tối ưu HOW-MANY | RL chọn động số T-LEO chuẩn bị |
| G8 | **Khả mở rộng thực sự lên ~30 000 vệ tinh + ISL HO + beam HO** | ILCHO dừng ở satellite HO, 5 280 vệ tinh | phân cấp (hierarchical MARL), GNN state encoder |
| G9 | **Sinh dữ liệu & benchmark chuẩn** cho HO trong NTN | mỗi bài một simulator | bộ benchmark mở (TLE thật + kênh 38.811 + KPI thống nhất) |
| G10 | **Sim-to-real / kiểm chứng trên testbed / O-RAN** | tất cả đều mô phỏng | triển khai near-RT RIC xApp cho HO NTN |
| G11 | **Giải thích được (XAI) & an toàn** cho quyết định HO học máy | tin cậy vận hành | ràng buộc an toàn, verify chính sách |

---

## 7. Cách định vị đề tài "dự đoán Handover" của bạn 🔵

Ba kịch bản (nên hỏi cô để chốt — xem file 08 §4):

1. **Prediction làm module bổ trợ cho CHO** (khác biệt rõ với ILCHO):
   Xây mô hình dự đoán (LSTM/GRU/Transformer) một đại lượng bất định — ví dụ **SINR hiệu dụng tương
   lai** hoặc **xác suất HOF** hoặc **thời điểm link-degradation** — rồi dùng nó làm **điều kiện
   preparation/execution** của CHO. So sánh với ILCHO (decision thuần) và với A3/A2.
   → Đóng góp: lấp G1. Vẫn có thể tái dùng khung MARL của ILCHO cho phần WHERE.

2. **Prediction hợp nhất vào state của RL** (mở rộng ILCHO):
   Thêm đặc trưng **dự báo** (tải vệ tinh tương lai, SINR dự báo) vào `o_k` của QMIX; so hiệu năng
   với ILCHO gốc (chỉ hình học). → Đóng góp: lấp G1+G6, "ablation" giá trị của thông tin dự đoán.

3. **Tái hiện + mở rộng ILCHO** (ít yếu tố "prediction"):
   Reproduce QMIX-CHO, rồi thêm UE mobility / Doppler / multi-connectivity (G2/G3/G5).

**Lưu ý học thuật**: nếu gọi là "dự đoán handover" thì phải có **đại lượng bất định được học từ dữ
liệu** (nhãn), có **metric dự đoán** (RMSE, F1, AUC, lead-time), tách bạch với **metric hệ thống**
(#HO, HOF, throughput). Đừng để bị hiểu là "dự đoán = lan truyền quỹ đạo".

---

## 8. Cấu trúc survey đề xuất

1. Giới thiệu: 6G, NTN, vì sao HO là nút thắt.
2. Nền tảng: HO trong TN (events, KPI, BHO/CHO/DAPS) → HO trong NTN (đặc thù LEO).
3. Phân loại AI-cho-HO: các trục A–E ở §2.
4. Prediction-based approaches (supervised, FL, chuỗi thời gian).
5. Decision/Control-based approaches (RL, **MARL**, tối ưu học).
6. Case study sâu: **ILCHO** (dùng file 01) + so với [26],[28],[31].
7. Môi trường mô phỏng & KPI & khả tái lập (§5).
8. Thách thức mở & hướng tương lai (§6, G1–G11).
9. Kết luận.

---

## Nguồn tham khảo (ngoài bài báo)
- *A Survey of Machine Learning Applications to Handover Management in 5G and Beyond* — https://www.academia.edu/72940811/
- *A Comprehensive Survey on Machine Learning Methods for Handover Optimization in 5G Networks* — https://www.researchgate.net/publication/383140668
- *Reactive to Predictive Mobility Management: A Systematic Review of ML-Driven Handover Optimization in 5G and Beyond*, MAKE 2025 — https://doi.org/10.3390/make8050133
- *Handover Technique in LEO Satellite Networks: A Review*, IEEE 2024 — https://ieeexplore.ieee.org/document/10652688
- *Non-Terrestrial Networking for 6G: Evolution, Opportunities, and Future Directions*, ScienceDirect 2025 — https://www.sciencedirect.com/science/article/pii/S2095809925002917
- *AI-Native Open RAN for Non-Terrestrial Networks: An Overview*, arXiv 2507.11935 — https://arxiv.org/pdf/2507.11935
- Jang et al., *Proactive handover optimization via multi-agent deep RL in integrated LEO satellite–terrestrial networks for high-mobility terminals*, ETRI Journal 2025 — https://onlinelibrary.wiley.com/doi/full/10.4218/etrij.2025-0240
- *Intelligent Dynamic Handover via AI-assisted Signal Quality Prediction in 6G Multi-RAT Networks*, arXiv 2510.14832 — https://arxiv.org/pdf/2510.14832
- *Privacy-Preserving Handover Optimization Using Federated Learning and LSTM Networks*, Sensors 2024 — https://doi.org/10.3390/s24206685
- *Conditional Handovers via Meta-Learning (CHOMET)*, arXiv 2507.07581 — https://arxiv.org/pdf/2507.07581
- *Dual-Graph Multi-Agent Reinforcement Learning for Handover Optimization*, arXiv 2603.24634 — https://arxiv.org/pdf/2603.24634
- *A Deep Reinforcement Learning-based Approach for Adaptive Handover Protocols*, arXiv 2401.14823 — https://arxiv.org/pdf/2401.14823
