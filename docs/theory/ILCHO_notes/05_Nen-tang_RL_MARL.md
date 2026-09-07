# Nền tảng Reinforcement Learning & Multi-Agent RL

> Đủ để đọc Mục IV–V của ILCHO và viết phần "phương pháp học" trong survey.
> 🟢 = kiến thức nền (nguồn cuối file). 🔵 = ánh xạ sang ILCHO.

---

## PHẦN A — Reinforcement Learning một tác tử

### A.1. MDP — Markov Decision Process 🟢
Bộ 5 `(S, A, P, R, γ)`:
- `S` — không gian trạng thái; `A` — không gian hành động.
- `P(s' | s, a)` — xác suất chuyển trạng thái (động lực môi trường).
- `R(s, a)` — phần thưởng tức thời.
- `γ ∈ [0,1)` — hệ số chiết khấu (bài ký hiệu `σ`, dùng 0,99).
- **Tính Markov**: `s_{t+1}` chỉ phụ thuộc `(s_t, a_t)`, không phụ thuộc quá khứ xa hơn.

Tác tử hành xử theo **chính sách** `π(a|s)`. Mục tiêu: tối đa **return** kỳ vọng
`G_t = Σ_{k≥0} γ^k r_{t+k}`. 🔵 bài eq: `R_t = Σ_{i=t}^{T_final} σ^{i−t} r_i`.

### A.2. Hàm giá trị & phương trình Bellman 🟢
- **State value**: `V^π(s) = E_π[G_t | s_t = s]`.
- **Action value (Q)**: `Q^π(s,a) = E_π[G_t | s_t=s, a_t=a]`.
- **Bellman expectation**: `Q^π(s,a) = E[r + γ Σ_{a'} π(a'|s') Q^π(s',a')]`.
- **Bellman optimality** (bài eq 17): `Q*(s,a) = E[ r + γ max_{a'} Q*(s',a') ]`.
- Chính sách tối ưu: `π*(s) = arg max_a Q*(s,a)`.

### A.3. Q-learning (off-policy, tabular) 🟢
Cập nhật TD (bài eq 18):
```
Q(s,a) ← Q(s,a) + β [ r + γ max_{a'} Q(s',a') − Q(s,a) ]
```
`β` = learning rate; `[ ... ]` = **TD error**. Hội tụ về `Q*` nếu mọi cặp `(s,a)` được thăm vô hạn lần
và `β` giảm hợp lý.

**Khám phá vs khai thác**: **ε-greedy** — xác suất `ε` chọn hành động ngẫu nhiên, `1−ε` chọn tham lam.
🔵 ILCHO: `ε` giảm dần **0,9 → 0,1** theo episode.

### A.4. DQN — Deep Q-Network (Mnih et al., *Nature* 2015) 🟢
Khi `S` quá lớn (liên tục/nhiều chiều) → xấp xỉ `Q(s,a) ≈ Q(s,a; θ)` bằng mạng nơ-ron.
Loss: `L(θ) = E[(y − Q(s,a;θ))²]`, `y = r + γ max_{a'} Q(s',a'; θ⁻)`.

Hai mẹo ổn định (bài IV-B nhắc cả hai):
1. **Experience replay**: lưu `(s,a,r,s')` vào buffer `D`, lấy **minibatch ngẫu nhiên** để học →
   phá tương quan thời gian giữa các mẫu liên tiếp.
2. **Target network** `θ⁻`: bản sao "đóng băng"/cập nhật chậm của `θ`, dùng để tính `y` → tránh mục
   tiêu chạy theo tham số → dao động. Cập nhật:
   - *hard*: `θ⁻ ← θ` mỗi `C` bước; hoặc
   - *soft*: `θ⁻ ← η θ + (1−η) θ⁻` (bài eq 19, 25).

**Biến thể quan trọng** 🟢: Double DQN (giảm overestimate), Dueling DQN (tách V và advantage),
Prioritized Experience Replay, **DRQN** (thêm RNN/GRU/LSTM để xử lý **partial observability** — nhớ
lịch sử quan sát). 🔵 QMIX trong ILCHO dùng **agent network kiểu DRQN (GRU)**.

### A.5. Hai họ thuật toán RL 🟢
| Họ | Học cái gì | Đại diện | Hợp với |
|----|-----------|----------|---------|
| **Value-based** | `Q(s,a)` → chính sách = argmax | Q-learning, DQN, **QMIX** | hành động **rời rạc** |
| **Policy-based / Actor-Critic** | trực tiếp `π_θ(a|s)` (+ critic `V`) | REINFORCE, A2C/A3C, DDPG, PPO, SAC, **MAPPO/MADDPG** | hành động liên tục, không gian lớn |

🔵 ILCHO chọn **value-based (QMIX)** vì action rời rạc (`1…N_max`) và (theo [43]) hội tụ nhanh hơn
MAPPO/MADDPG trong lớp bài toán này.

---

## PHẦN B — Multi-Agent RL (MARL)

### B.1. Vì sao MARL khó hơn RL 🟢
Nhiều tác tử cùng học trong **một** môi trường:
- **Non-stationarity**: từ góc nhìn của tác tử `i`, môi trường "trôi" vì các tác tử khác **đang thay
  đổi chính sách** → vi phạm giả định MDP dừng → Q-learning mất bảo đảm hội tụ.
- **Không gian chung nổ tổ hợp**: joint action `= |A|^K`.
- **Credit assignment**: phần thưởng chung → tác tử nào đã đóng góp (tốt/xấu)?
- **Partial observability**: mỗi tác tử chỉ thấy một phần trạng thái → **Dec-POMDP**
  (Decentralized Partially Observable MDP).

### B.2. Ba mô hình huấn luyện/thực thi 🟢
| Sơ đồ | Huấn luyện | Thực thi | Ghi chú |
|-------|-----------|----------|---------|
| **Centralized** | 1 policy chung thấy mọi thứ | tập trung | không scale, không thực tế |
| **Decentralized (IQL)** | mỗi tác tử học độc lập | phân tán | đơn giản, **non-stationarity** |
| **CTDE** (Centralized Training, Decentralized Execution) | dùng thông tin toàn cục **khi học** | mỗi tác tử chỉ dùng quan sát cục bộ **khi chạy** | **tiêu chuẩn hiện nay**; QMIX, MADDPG, MAPPO đều CTDE |

🔵 ILCHO = **CTDE**: near-RT RIC huấn luyện tập trung (gom quan sát + ephemeris); vệ tinh chạy
inference cục bộ.

### B.3. IQL — Independent Q-Learning (Tan, 1993) 🟢
Mỗi tác tử chạy DQN riêng, coi tác tử khác là môi trường. Ưu: cực đơn giản, scale tốt. Nhược:
**non-stationarity**, không hội tụ đảm bảo, hay dao động. 🔵 Bài phê phán [25–28] dùng IQL/multi-agent
DQN nên **không ổn định khi state space lớn**.

### B.4. Value Factorization — xương sống của ILCHO 🟢

Ý tưởng: học **một** `Q_tot` chung (để credit assignment đúng khi huấn luyện tập trung) nhưng **phân
rã** được thành các `Q_k` cục bộ (để mỗi tác tử tự chọn hành động khi thực thi). Điều kiện cần:

> **IGM (Individual-Global-Max)**: `arg max_a Q_tot(τ, a) = ( arg max_{a_1} Q_1, …, arg max_{a_K} Q_K )`

(bài eq 20). Nghĩa là "tối ưu cục bộ đồng thời = tối ưu toàn cục".

| Thuật toán | Cách phân rã | Biểu diễn được | Ghi chú |
|-----------|--------------|----------------|---------|
| **VDN** (Sunehag 2017) | `Q_tot = Σ_k Q_k` (cộng tuyến tính) | hẹp | bài eq: "as in [46]" — QMIX thay thế cái này |
| **QMIX** (Rashid 2018) | `Q_tot = f_mix(Q_1,…,Q_K)` với `∂Q_tot/∂Q_k ≥ 0` | rộng hơn VDN | **ILCHO dùng** |
| QTRAN (Son 2019) | bỏ ràng buộc đơn điệu, thêm ràng buộc mềm | rộng | khó tối ưu thực tế |
| QPLEX (Wang 2020) | dueling + advantage-based IGM | đầy đủ IGM | phức tạp hơn |
| Weighted QMIX | trọng số hoá để vượt giới hạn đơn điệu | rộng hơn | — |

### B.5. QMIX — chi tiết (Rashid et al., ICML 2018, [arXiv:1803.11485]) 🟢🔵

**Ràng buộc đơn điệu**: `∂Q_tot / ∂Q_k ≥ 0 ∀k` (bài eq 22). Đủ (không cần thiết) để thoả IGM.
Trực giác: nếu `Q_k` của một tác tử tăng (giữ nguyên các tác tử khác) thì `Q_tot` **không giảm** →
hành động tham lam cục bộ luôn kéo `Q_tot` lên → **tín hiệu học nhất quán** dù chính sách tác tử khác
đang đổi → **giảm non-stationarity**.

**Kiến trúc 3 mạng** (bài IV-C, Hình 4):
1. **Agent network** (một cho mỗi tác tử, chia sẻ tham số): đầu vào `(o^t_k, a^{t−1}_k)` → `Q_k(τ_k, ·)`.
   Kiến trúc **DRQN** (GRU) để nhớ lịch sử `τ_k = (o^1_k, …, o^t_k)` — xử lý partial observability.
2. **Mixing network**: nhận các `Q_k` → xuất `Q_tot`. Là mạng feed-forward với **trọng số không âm**
   (⇒ đơn điệu). Trọng số **không** học trực tiếp mà do…
3. **Hypernetwork**: nhận **trạng thái toàn cục** `s` → sinh ra (trọng số, bias) cho mixing network.
   Trọng số qua hàm `|·|`/ReLU để đảm bảo ≥ 0. Bias thì không cần ≥ 0. → `Q_tot` phụ thuộc `s` theo
   cách **phi tuyến bất kỳ**, chỉ **đơn điệu theo `Q_k`**.

**Huấn luyện** (bài eq 23–25):
```
L(θ) = Σ_batch [ y − Q_tot(τ, a, s; θ) ]²
y     = r + γ max_{a'} Q_tot(τ⁻, a⁻, s⁻; θ⁻)
θ⁻    ← η θ + (1−η) θ⁻   (soft update mỗi T_t bước)
```
Chạy end-to-end: gradient chảy từ `L` qua mixing net + hypernet về từng agent net.

**Giới hạn của QMIX** 🟢: ràng buộc đơn điệu **không biểu diễn được** các bài mà thứ tự ưu tiên hành
động của một tác tử **phụ thuộc hành động tác tử khác** (non-monotonic payoff, ví dụ trò chơi phối
hợp có "miscoordination penalty"). → sinh ra QTRAN, QPLEX, Weighted QMIX. *(Với ILCHO, phần thưởng
gần như phân tách được theo UE nên đơn điệu là đủ.)*

### B.6. Actor-critic đa tác tử (để so sánh) 🟢
- **MADDPG** (Lowe 2017): mỗi tác tử có actor cục bộ + **critic tập trung** thấy joint action. Hành
  động liên tục. 🔵 bài loại vì "kém trong kịch bản hợp tác + khó scale".
- **MAPPO** (Yu 2021): PPO + critic tập trung chia sẻ. Rất mạnh trên SMAC/MPE. 🔵 bài công nhận "mạnh"
  nhưng chọn QMIX vì "học hiệu quả & hội tụ nhanh hơn" [43] cho bài toán này.
- **COMA** (Foerster 2018): critic phản thực (counterfactual) để credit assignment.

### B.7. Ánh xạ ILCHO ↔ khái niệm MARL 🔵

| Khái niệm MARL | Trong ILCHO |
|----------------|-------------|
| Agent | mỗi UE `k` |
| Quan sát cục bộ `o_k` | `{(I, D, L, RVT) cho N_max vệ tinh khả kiến}` (eq 26) |
| Hành động `a_k` | chọn 1 trong `N_max` vệ tinh làm T-LEO (eq: `a_k ∈ {1..N_max}`) |
| Trạng thái toàn cục `s` | hợp quan sát mọi UE + ephemeris (dùng ở hypernetwork) |
| Reward | sigmoid throughput/RVT + phạt `p_1` (HO), `p_2` (HOF) (eq 27) |
| Môi trường | mô phỏng chòm Starlink, bước 1 s, 10 phút/episode |
| Non-stationarity | nhiều UE cùng học chọn vệ tinh → QMIX đơn điệu để ổn định |
| Partial observability | UE không thấy quan sát UE khác → DRQN/GRU |
| Credit assignment | mixing network tách đóng góp từng UE vào `Q_tot` |
| CTDE | train ở near-RT RIC, execute on-board |
| Giảm không gian hành động | `N_max` (từ Lemma 2) thay cho `M` (tổng vệ tinh) → **O(K)** |

### B.8. Vì sao thiết kế action-space của ILCHO là mấu chốt 🔵
- Nếu action = "chọn vệ tinh theo chỉ số toàn cục" → `|A| = M` (Starlink: 1 584–5 280, tương lai
  ~30 000). Q-network có `M` đầu ra, phần lớn tương ứng vệ tinh **không thể tới** → gradient loãng,
  thăm dò kém, **không hội tụ** (đúng như [27], [28] gặp).
- ILCHO: action = "chọn vệ tinh khả kiến **thứ n**", `n ∈ {1…N_max}`, `N_max` ≈ 17–27 và **hằng số**
  (Lemma 2). Mapping `n → chỉ số thật I_{k,n}` làm bên ngoài mạng. → `|A|` nhỏ, cố định → hội tụ
  ổn định, độ phức tạp **O(K)** không phụ thuộc `M`.
- Đây là một dạng **action masking / action abstraction** dựa trên tri thức miền (quỹ đạo tất định).

---

## PHẦN C — Bảng thuật ngữ RL/MARL nhanh

| Viết tắt | Nghĩa |
|----------|-------|
| MDP / POMDP / Dec-POMDP | Markov Decision Process / Partially Observable / Decentralized POMDP |
| TD | Temporal Difference |
| DQN / DDQN / DRQN | Deep / Double / Deep Recurrent Q-Network |
| CTDE | Centralized Training, Decentralized Execution |
| IQL | Independent Q-Learning |
| IGM | Individual-Global-Max (điều kiện phân rã giá trị) |
| VDN / QMIX / QTRAN / QPLEX | các thuật toán value factorization |
| MADDPG / MAPPO / COMA | actor-critic đa tác tử |
| GAE | Generalized Advantage Estimation |
| SMAC / MPE | StarCraft Multi-Agent Challenge / Multi-agent Particle Env (benchmark) |

---

## Nguồn tham khảo (ngoài bài báo)
- R. Sutton, A. Barto, *Reinforcement Learning: An Introduction*, 2nd ed., MIT Press, 2018 — http://incompleteideas.net/book/the-book-2nd.html
- V. Mnih et al., *Human-level control through deep reinforcement learning*, Nature 518, 2015 — https://www.nature.com/articles/nature14236
- T. Rashid et al., *QMIX: Monotonic Value Function Factorisation for Deep MARL*, ICML 2018 — https://arxiv.org/abs/1803.11485 ; bản JMLR mở rộng — https://arxiv.org/abs/2003.08839
- P. Sunehag et al., *Value-Decomposition Networks For Cooperative Multi-Agent Learning*, 2017 — https://arxiv.org/abs/1706.05296
- R. Lowe et al., *Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments (MADDPG)*, NeurIPS 2017 — https://arxiv.org/abs/1706.02275
- C. Yu et al., *The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games (MAPPO)*, 2021 — https://arxiv.org/abs/2103.01955
- G. Papoudakis et al., *Benchmarking Multi-Agent Deep RL Algorithms in Cooperative Tasks* (= ref [43] của bài), NeurIPS D&B 2021 — https://openreview.net/forum?id=cIrPX-Sn5n
- *Beyond Monotonicity: Revisiting Factorization Principles in Multi-Agent Q-Learning*, 2025 — https://arxiv.org/pdf/2511.09792
