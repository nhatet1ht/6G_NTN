# Thuật ngữ & ký hiệu

---

## 1. Bảng ký hiệu toán học của bài ILCHO

### 1.1. Chòm sao & hình học
| Ký hiệu | Nghĩa | Ghi chú |
|---------|-------|---------|
| `M` | tổng số vệ tinh LEO trong mô hình | |
| `K` | số UE (= số agent) | 5–100 trong mô phỏng |
| `s_m` | vệ tinh LEO thứ `m` | có regenerative payload |
| `u_k` | UE thứ `k` | VSAT cố định |
| `l_{m,k}` ∈ {0,1} | chỉ báo phục vụ: 1 nếu `s_m` phục vụ `u_k` | |
| `N_p` | số mặt phẳng quỹ đạo | |
| `N_L` | số vệ tinh mỗi mặt phẳng | |
| `N_total` | `= N_p · N_L` | |
| `α` | góc nghiêng quỹ đạo (inclination) | chung mọi mặt phẳng (Walker-Delta) |
| `Ω_m` | RAAN của mặt phẳng chứa `s_m` | `ΔΩ = 2π/N_p` |
| `Φ_m` | pha ban đầu của `s_m` trong mặt phẳng | `ΔΦ = 2π/N_L` |
| `F` | phasing factor | `Δf = 2πF/N_total` |
| `f_0` | pha khởi tạo chung | |
| `ε` | độ lệch tâm (eccentricity) | Starlink 0,0001379 ≈ 0 |
| `a_s` | bán trục lớn `= R_E + H_L` | |
| `R_E` | bán kính Trái Đất | ~6 371 km |
| `H_L` | độ cao vệ tinh | 550 km (P1) / ~340 km (P2) |
| `w_perigee` | argument of perigee | |
| `A`, `A^t_m` | mean anomaly | `= Φ_h + ωt` |
| `E^t_m` | eccentric anomaly | `A = E − ε sin E` (pt Kepler) |
| `μ^t_m` (ν) | **true anomaly** tại `t` | `≈ A` khi ε≈0 |
| `ω` | mean motion (tốc độ góc) `= √(G M_E / a_s³)` | bản in OCR ghi nhầm `a_s²` |
| `t_0e` | thời điểm tham chiếu ephemeris | từ SIB19 |
| `s^t_m = (x,y,z)` | vị trí Descartes vệ tinh tại `t` | **Lemma 1**, eq (1) |
| `r^t_m` | khoảng cách vệ tinh–tâm Trái Đất | `= a_s(1−ε²)/(1+ε cos μ)` |
| `φ_k`, `δ_k` | vĩ độ, kinh độ UE `k` | |
| `ψ_{m,k}` | **góc ngẩng** (elevation) UE `k` → vệ tinh `m` | eq (4) |
| `ψ_min` | góc ngẩng tối thiểu để "accessible" | 30° |
| `d_{m,k}` | khoảng cách UE `k` – vệ tinh `m` | eq (3) |
| `c_1, c_2` | hệ số hình học trong **Lemma 2** | phụ thuộc `φ_k, δ_k, α, Ω` |
| `N_max` | số vệ tinh khả kiến **tối đa** cho 1 UE | 17 (P1-a) / 27 (P2-a); = kích thước action space |

### 1.2. Kênh & hiệu năng
| Ký hiệu | Nghĩa |
|---------|-------|
| `P_loss` | path loss tổng (eq 8) = `P_loss,b + P_loss,g + P_loss,s + P_loss,e` |
| `P_loss,b` | path loss cơ bản = FSPL + SF + CL (eq 9) |
| `F_loss(d,f_c)` | free-space path loss `= 32,45 + 20log₁₀f_c + 20log₁₀d` (eq 10), d[m], f_c[GHz] |
| `SF` | shadow fading ~ `N(0, σ²_SF)` |
| `CL` | clutter loss |
| `P_loss,g` | suy hao khí quyển/mưa `= L_zenith(f_c)/sin ψ` |
| `P_loss,s` | scintillation (= 0 với vĩ độ ±20°…±60°) |
| `P_loss,e` | building entry loss (bỏ qua, UE ngoài trời LoS) |
| `P_LoS` | xác suất line-of-sight |
| `γ_{m,k}` | SNR (dB) UE `k` – vệ tinh `m` (eq 12) |
| `E_EIRP` | equivalent isotropic radiated power |
| `G_T` | gain-to-noise-temperature ratio (G/T) anten thu |
| `K_B` | hằng số Boltzmann |
| `BW`, `BW_m` | băng thông (kênh) |
| `J` | số kênh tối đa mỗi vệ tinh (bài dùng 8) |
| `R_{m,k}` | throughput vệ tinh `m` cấp cho UE `k` (Shannon, eq 13) |
| `R_NTN` | hàm mục tiêu = throughput TB theo thời gian & theo UE (eq 14) |
| `O_{m,t}` | channel occupancy `= L_{m,t}/J` |
| `L_{m,t}` | số UE đang nối vệ tinh `m` tại `t` `= Σ_k l_{m,k}` |
| `J_JFI` | Jain's Fairness Index (eq 32) |

### 1.3. RL / QMIX
| Ký hiệu | Nghĩa |
|---------|-------|
| `s_t, a_t, r_t` | trạng thái / hành động / thưởng tại `t` |
| `π` | chính sách |
| `σ` | discount factor (= γ; bài dùng 0,99) |
| `R_t` | return chiết khấu `Σ σ^{i−t} r_i` |
| `Q(s,a)` | action-value function |
| `Q*` | Q tối ưu (Bellman, eq 17) |
| `β` | learning rate (1e−4) |
| `θ_QMIX`, `θ⁻_QMIX` | tham số mạng đánh giá / mạng đích |
| `η_QMIX` | hệ số soft update (eq 25) |
| `o^t_k` | quan sát cục bộ của agent `k` (eq 26) |
| `τ_k` | lịch sử quan sát–hành động của agent `k` |
| `I^t_{k,n}` | chỉ số logic vệ tinh khả kiến thứ `n` |
| `D^t_{k,n}` | khoảng cách tới vệ tinh khả kiến thứ `n` |
| `L^t_{k,n}` | số kênh vệ tinh khả kiến thứ `n` đang dùng |
| `V^t_{k,n}` | **RVT** — remaining visible time của vệ tinh khả kiến thứ `n` |
| `a^t_k ∈ {1..N_max}` | hành động: chọn vệ tinh khả kiến thứ mấy làm T-LEO |
| `Q_k` | action-value cục bộ của agent `k` |
| `Q_tot` | joint action-value (qua mixing network) |
| `f_mix` | mixing network (đơn điệu) |
| `U_k(x) = c_3/(1+e^{c_1(x−c_2)})` | hàm chi phí dạng sigmoid trong reward |
| `U_{k,R}`, `U_{k,RVT}` | hàm chi phí cho throughput / RVT |
| `p_1` | phạt khi HO thành công (giảm số HO) |
| `p_2` | phạt khi HOF |
| `w_1, w_2` | trọng số trong reward tuyến tính đối chứng (eq 30) |
| `T_RVT` | RVT của vệ tinh đang phục vụ (reward tuyến tính) |
| `O_off` | offset khoảng cách trong sự kiện thực thi (eq 28) |
| `ζ` | ngưỡng khoảng cách trong sự kiện A2 đối chứng (eq 31) |
| `d_{k,tar}, d_{k,serv}` | khoảng cách UE `k` tới T-LEO / S-LEO |
| `N_epi` | số episode huấn luyện (3 000–30 000) |
| `T_serv`, `T_s` | thời lượng dịch vụ (10 phút, slot 1 s) |
| `T_t` | chu kỳ cập nhật mạng đích |
| `b` | batch size replay buffer |
| `D` | replay buffer |
| `P_a, P_m, P_h, P_t` | số tham số agent / mixing / hyper / … network (eq 29) |

---

## 2. Từ điển viết tắt

### Mạng & chuẩn hoá
| Viết tắt | Đầy đủ | Ghi chú |
|----------|--------|---------|
| 3GPP | 3rd Generation Partnership Project | tổ chức chuẩn hoá di động |
| NTN | Non-Terrestrial Network | mạng phi mặt đất |
| TN | Terrestrial Network | mạng mặt đất |
| NR | New Radio | giao diện vô tuyến 5G |
| RAT | Radio Access Technology | |
| UE | User Equipment | thiết bị người dùng |
| gNB | next-generation NodeB | trạm gốc 5G |
| RAN | Radio Access Network | |
| RIC | RAN Intelligence Controller | O-RAN; near-RT RIC = gần thời gian thực |
| SAGIN | Space-Air-Ground Integrated Network | |
| SIB19 | System Information Block 19 | mang ephemeris NTN |
| RRC | Radio Resource Control | lớp báo hiệu |
| TR / TS | Technical Report / Technical Specification | tài liệu 3GPP |
| FCC | Federal Communications Commission | cơ quan Mỹ; nguồn tham số Starlink |

### Handover
| Viết tắt | Đầy đủ |
|----------|--------|
| HO | Handover (chuyển giao) |
| BHO | Baseline Handover |
| CHO | Conditional Handover (chuyển giao có điều kiện) |
| DAPS | Dual Active Protocol Stack |
| LTM | L1/L2-Triggered Mobility |
| HOF | Handover Failure |
| RLF | Radio Link Failure |
| HIT | Handover Interruption Time |
| MRO | Mobility Robustness Optimization |
| SON | Self-Organizing Network |
| MR | Measurement Report |
| TTT | Time-To-Trigger |
| RSRP / RSRQ / RSSI / SINR | Reference Signal Received Power / Quality / Received Signal Strength Indicator / Signal-to-Interference-plus-Noise Ratio |
| S-LEO / T-LEO | Source / Target LEO satellite |
| RVT | Remaining Visible Time (thời gian còn khả kiến) |
| MVT / MD | Maximum Visible Time / Minimum Distance (baseline) |
| HSNF | Handover Strategy based on Network Flows (baseline [22]) |
| LBSH | Load Balancing Satellite Handover (baseline [26]) |

### Quỹ đạo
| Viết tắt | Đầy đủ |
|----------|--------|
| LEO / MEO / GEO / HEO / VLEO | Low / Medium / Geostationary / Highly Elliptical / Very Low Earth Orbit |
| RAAN | Right Ascension of the Ascending Node |
| TLE | Two-Line Element set |
| SGP4 | Simplified General Perturbations 4 (bộ lan truyền quỹ đạo) |
| ISL | Inter-Satellite Link |
| VSAT | Very Small Aperture Terminal |
| EIRP | Equivalent Isotropic Radiated Power |
| G/T | Gain-to-noise-Temperature ratio |
| FSPL | Free-Space Path Loss |
| LoS / NLoS | Line-of-Sight / Non-Line-of-Sight |
| SF / CL | Shadow Fading / Clutter Loss |

### Học máy
| Viết tắt | Đầy đủ |
|----------|--------|
| RL / DRL | Reinforcement Learning / Deep RL |
| MARL | Multi-Agent RL |
| MDP / POMDP / Dec-POMDP | (Partially Observable / Decentralized) Markov Decision Process |
| TD | Temporal Difference |
| DQN / DDQN / DRQN | Deep / Double / Deep Recurrent Q-Network |
| DNN / CNN / RNN / GRU / LSTM | các kiến trúc mạng nơ-ron |
| CTDE | Centralized Training, Decentralized Execution |
| IQL | Independent Q-Learning |
| IGM | Individual-Global-Max |
| VDN / QMIX / QTRAN / QPLEX | value factorization algorithms |
| MADDPG / MAPPO / COMA / PPO / SAC / DDPG | actor-critic (đa tác tử) |
| FL | Federated Learning |
| JFI | Jain's Fairness Index |
| QoE / QoS | Quality of Experience / Service |
| SE | Spectral Efficiency (bps/Hz) |
| XAI | eXplainable AI |
