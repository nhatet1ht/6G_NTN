# Phân tích chi tiết bài báo ILCHO

> M. Choi, M. Park, J. Kim, J.-M. Chung, **"Intelligent Handover Scheme for Improved 6G NTN LEO
> Satellite Network Performance,"** *IEEE Transactions on Mobile Computing*, vol. 25, no. 5,
> pp. 6863–6880, May 2026. DOI [10.1109/TMC.2025.3642278](https://doi.org/10.1109/TMC.2025.3642278).
> Nhận 23/3/2025 · sửa 1/11/2025 · chấp nhận 1/12/2025 · xuất bản online 10/12/2025.
> Tài trợ: KAIA / Bộ Đất đai, Hạ tầng & Giao thông Hàn Quốc, Grant RS-2022-00143782.

Ký hiệu 🔵 = nội dung của bài báo. Các nhận xét/đối chiếu thêm được đánh dấu *(nhận xét)*.

---

## 0. Bản đồ bài báo

| Mục | Nội dung | Đóng góp nằm ở đâu |
|-----|----------|--------------------|
| I | Giới thiệu, bối cảnh 6G/NTN, Starlink, nêu 4 đóng góp | — |
| II | Công trình liên quan (game theory, network-flow, RL/DQN, IQL) | Xác định khoảng trống |
| III | Mô hình chòm sao Walker-Delta + mô hình kênh LEO + **Lemma 1, 2, 3** + bài toán (P) | Nền tảng giải tích |
| IV | Quy trình CHO 3 pha; nền tảng RL (MDP, Q-learning, DQN); **QMIX** | Chuẩn bị công cụ |
| V | Khung MARL của ILCHO: state/action/reward, **Algorithm 1**, độ phức tạp | Thuật toán chính |
| VI | Mô phỏng Starlink Phase 1-a / 2-a / hybrid; sigmoid vs linear; so 4 baseline; fairness & load balance | Bằng chứng thực nghiệm |
| VII | Kết luận + hướng phát triển | — |

---

## 1. Bối cảnh & động lực (Mục I) 🔵

### 1.1. Vì sao NTN, vì sao LEO
- 6G cần **phủ sóng toàn cầu** + ứng dụng thời gian thực (xe tự hành, robot, XR). 5G tập trung small-cell vùng đông dân; TN 3G/4G/5G dễ sập khi thiên tai. NTN (3GPP Rel-15) sinh ra để phủ vùng thưa dân, IoT mật độ cao, hành khách trên máy bay/tàu.
- Phân tầng quỹ đạo: **LEO 300–2 000 km**, **MEO >2 000 km & < GEO**, **GEO 35 786 km**, HEO, và mạng drone.
- Trễ truyền tối đa: **LEO 12,89 ms** vs **GEO 270,73 ms**. LEO có link budget tốt hơn nhưng **vùng phủ nhỏ, thời gian phủ ngắn** ⇒ phải "siêu dày" (ultra-dense).

### 1.2. Con số Starlink (bài báo trích hồ sơ FCC)
| Lớp | Số vệ tinh (kế hoạch) | Độ cao | Trạng thái |
|-----|----------------------|--------|-----------|
| Phase 1 | 4 408 | 540–570 km | đang vận hành |
| Phase 1 VLEO | 7 518 | 330–340 km | — |
| Phase 2 | 29 998 | 340–614 km | đang quy hoạch |

Tính đến 2/2025: ~8 000 vệ tinh đã phóng, ~6 100 đang cung cấp dịch vụ.

### 1.3. Vấn đề handover trong NTN
- Theo **3GPP TR 38.821 §7.3.2.1**: HO của LEO phải thực hiện **mỗi 6,61–132,28 s** tuỳ vị trí UE so với đường kính cell.
- Đo RSRP/RSSI **kém tin cậy** trong NTN: các cell vệ tinh ở xa, chồng lấn, tín hiệu dao động khó lường ⇒ UE khó chọn cell.
- Các khó khăn khác: kết nối chập chờn, xử lý on-board hạn chế, năng lượng on-board hạn chế (bài dẫn [14–16] về SAGIN).
- 3GPP kết luận: **không nên bê nguyên thuật toán HO của TN vào NTN**, và đề xuất **CHO** (Rel-16) làm giải pháp. Trigger MR có thể theo 4 tiêu chí: **đo đạc**, **vị trí**, **timing-advance**, **góc elevation** (giữa cell nguồn và đích).
- **HOF** (handover failure) xảy ra chủ yếu ở **pha chuẩn bị**; CHO giảm HOF bằng cách **quyết định chuẩn bị sớm hơn** so với BHO (baseline HO).

### 1.4. Bốn đóng góp được tuyên bố 🔵
1. **Nền tảng giải tích**: 3 Lemma. Lemma 1 → trạng thái (vị trí, quỹ đạo) vệ tinh; Lemma 2 → điều kiện "khả kiến" (accessible); Lemma 3 → ước lượng độ phức tạp/khả mở rộng (NP-hard).
2. **Môi trường chòm sao thực tế**: dùng Starlink Phase 1-a và Phase 2-a (đã/sắp triển khai thương mại) làm system model, thay vì mô hình < 100 vệ tinh giả định.
3. **Công thức MARL khả mở rộng**: không gian hành động = **số vệ tinh khả kiến tối đa** (qua Lemma 2), không phải = chỉ số của toàn bộ vệ tinh ⇒ tránh bùng nổ hành động, hội tụ ổn định.
4. **Kiểm chứng CHO dựa trên RL**: *"theo hiểu biết của nhóm tác giả, đây là nghiên cứu đầu tiên validate RL-based CHO trong một mega-constellation LEO NTN thực thụ"*, cho số HO trung bình ổn định bất kể số UE.

*(Nhận xét: đóng góp #3 là điểm kỹ thuật thực sự mới và đáng giá nhất — nó biến bài toán từ "không học nổi" thành "học được ở quy mô Starlink". Đóng góp #1 chủ yếu là tái trình bày cơ học quỹ đạo cổ điển dưới dạng Lemma.)*

---

## 2. Công trình liên quan (Mục II) 🔵

Bốn tiêu chí HO trong NTN mà văn liệu quan tâm: **visible time, cường độ tín hiệu, vị trí, cân bằng tải** [19,20].

| Nhóm | Công trình | Ý tưởng | Hạn chế (theo bài báo) |
|------|-----------|---------|------------------------|
| Game theory | [21] | Tối đa lợi ích UE bằng potential game | — |
| Network-flow | [22] = **HSNF** | Đồ thị luồng, ma trận chi phí (throughput + băng thông còn lại) tối ưu QoE đa UE | Tính chi phí mọi cặp UE–vệ tinh theo thời gian thực **bất khả thi** ở quy mô mega |
| Tunnel theo cụm | [23] | Rút ngắn thời gian thủ tục HO | — |
| RL không DNN | [24] | RL cải thiện QoE | Không dùng deep network |
| Multi-agent Q-learning | [25], [26] = **LBSH** | Giảm số HO, không vượt ngân sách kênh; reward = RVT + tải + phạt HO | Không phân tích QoE theo UE; **action space nổ** khi ghép vào Starlink |
| DQN + OneWeb | [27] | Tối đa throughput trên chòm OneWeb | Bỏ qua overhead báo hiệu do HO thừa |
| DRL, vệ tinh tự quyết | [28] | S-LEO tự chạy DRL chọn T-LEO, UE không gửi MR | Chỉ 3 mặt phẳng quỹ đạo, tối đa 3 hành động → "curse of dimensionality" khi lên chòm thật |
| CHO trong NTN | [30] | Đánh giá CHO 5G NR trên LEO | Chỉ ra CHO gây overhead báo hiệu do HO thừa → cần cải tiến |
| CHO + service continuity | [31] | Đồ thị hiệu năng liên tục dịch vụ + chọn target tối ưu | — |

**Về hướng RL đa tác tử**: các bài [25–28] đều dựa **DQN**, mở rộng đa tác tử bằng **IQL** (independent Q-learning) — mỗi agent học độc lập, coi agent khác là môi trường ⇒ **non-stationarity**, không đảm bảo hội tụ khi state space lớn. (Xem file 05 để hiểu IQL/non-stationarity.)

**Khoảng trống**: chưa có bài nào validate **RL-based CHO** trên **mega-constellation LEO thương mại**. ILCHO lấp chỗ này.

*(Nhận xét: bài báo hơi "gộp" [32] = QMIX vào chỗ trích IQL — thực ra IQL kinh điển là Tan 1993. Đây là lỗi trích dẫn nhỏ.)*

---

## 3. Mô hình chòm sao & kênh (Mục III) 🔵

### 3.1. Ký hiệu hệ thống
- `M` vệ tinh LEO: `S = {s_m | m ∈ [1,M]}`, mỗi vệ tinh có **regenerative payload** (làm được chức năng base station on-board).
- `K` UE: `U = {u_k | k ∈ [1,K]}`.
- `L = {l_{m,k}}`, `l_{m,k} ∈ {0,1}`; `l_{m,k}=1` ⇔ UE `u_k` đang được vệ tinh `m` phục vụ.

### 3.2. Mô hình Walker-Delta (III-A)
- Mọi quỹ đạo cùng **góc nghiêng** `α`.
- `N_p` mặt phẳng quỹ đạo, mỗi mặt phẳng `N_L` vệ tinh ⇒ `N_total = N_p · N_L`.
- Mặt phẳng cách đều: **RAAN** `ΔΩ = 2π/N_p`.
- Vệ tinh trong 1 mặt phẳng cách đều pha: `ΔΦ = 2π/N_L`.
- Pha lệch giữa vệ tinh của 2 mặt phẳng kề: `Δf = 2πF/N_total`, `F` = **phasing factor**.
- Ký hiệu chuẩn: `α : N_total / N_p / F`. (Hình 2 dùng ví dụ `α : 18/3/F`.)
- Chỉ số logic: vệ tinh `m` ↔ (mặt phẳng `v`, vị trí `h`), `m = (v−1)N_L + h`.
- **7 tham số ephemeris** (theo TR 38.821): góc nghiêng `α`, RAAN, độ lệch tâm `ε`, bán trục lớn `a_s`, argument of perigee `w_perigee`, mean anomaly `A`, thời điểm tham chiếu `t_0e`.
- `a_s = R_E + H_L` (bán kính Trái Đất + độ cao). SIB19 cung cấp `t_0e`; true anomaly tính từ tham số pha.
- Với Starlink, `ε = 0,0001379 ≈ 0` ⇒ quỹ đạo ~tròn ⇒ **true anomaly ≈ mean anomaly**.

### 3.3. LEMMA 1 — trạng thái vị trí vệ tinh 🔵

**Phát biểu.** Toạ độ Descartes của vệ tinh `m` tại thời điểm `t`:

```
s^t_m = a_s · [ cos ψ^t_m cos Ω_m − sin ψ^t_m sin Ω_m cos α
                cos ψ^t_m sin Ω_m + sin ψ^t_m cos Ω_m cos α
                sin ψ^t_m sin α ]                                (1)

với  ψ^t_m = Φ_m + ω t + f_0
```

- `ω = sqrt(G·M_E / a_s³)` — **mean motion** (tốc độ góc quỹ đạo) theo định luật Kepler 3; `G` hằng số hấp dẫn, `M_E` khối lượng Trái Đất.
  *(Lưu ý: bản OCR in ra "a_s²" ở một chỗ; công thức đúng là `a_s³`.)*
- `Φ_m = ΔΦ·h = 2πh/N_L` là pha ban đầu trong mặt phẳng; `f_0` pha khởi tạo chung; `Ω_m` là RAAN của mặt phẳng chứa `m`.

**Chứng minh (tóm tắt).**
1. Vệ tinh trong mặt phẳng nghiêng 0°: `P_j = (r_j cos μ_j, r_j sin μ_j, 0)`.
2. Xoay quanh trục x một góc `α` (ma trận `R_x(α)`) rồi xoay quanh trục z một góc RAAN `Ω_v` (`R_z(Ω_v)`):
   `s^0_m = R_z(Ω_v) R_x(α) P_h`.
3. Nhân 2 ma trận xoay → ra dạng (1) ở `t=0`.
4. Thêm phụ thuộc thời gian qua `μ^t_m`. Quan hệ mean/eccentric/true anomaly:
   ```
   A^t_m = Φ_h + ω t                     (mean anomaly tuyến tính theo t)
   A^t_m = E^t_m − ε sin E^t_m           (phương trình Kepler)
   cos μ^t_m = (cos E^t_m − ε)/(1 − ε cos E^t_m)
   r^t_m = a_s(1 − ε²)/(1 + ε cos μ^t_m) (khoảng cách vệ tinh–tâm Trái Đất)
   ```
5. Cho `ε → 0`: `μ ≈ A`, `r^t_m ≈ a_s`, thu được (1). ∎

**Ý nghĩa cốt lõi.** Vị trí vệ tinh là **hàm tường minh, tất định của thời gian** — biết ephemeris là **tính trước được mọi thứ**, **không cần đo**. Đây là nền để ILCHO "biết trước" trạng thái vệ tinh thay vì đo RSRP.

### 3.4. Vị trí UE & hình học liên kết (III-B) 🔵

UE là **VSAT cố định** (không di chuyển). Lý do: vệ tinh 550 km bay **7,59 km/s**, áp đảo hoàn toàn độ di động của UE ⇒ bỏ qua UE mobility (giả định phổ biến [19,20,22,25–28,30,31,37]).

```
u_k = R_E · (cos φ_k cos δ_k,  cos φ_k sin δ_k,  sin φ_k)         (2)
```
`φ_k` vĩ độ, `δ_k` kinh độ của UE `k`.

**Khoảng cách UE–vệ tinh** (định lý cosin trên tam giác tâm-Trái-Đất / UE / vệ tinh):
```
d_{m,k} = ‖s_m − u_k‖
        = sqrt( R_E² sin²ψ_{m,k} + H_L² + 2 H_L R_E ) − R_E sin ψ_{m,k}      (3)
```

**Góc ngẩng (elevation)** giữa UE `k` và vệ tinh `m`:
```
ψ_{m,k} = π/2 − arccos( u_k·(s_m − u_k) / (‖u_k‖ ‖s_m − u_k‖) )              (4)
```

### 3.5. LEMMA 2 — điều kiện "khả kiến" (accessible) 🔵

**Phát biểu.** UE `u_k` **accessible** với vệ tinh `s_m` ⇔
```
c_1 cos μ_m + c_2 sin μ_m  ≥  d_{m,k} · sin ψ_min / (R_E + H_L)              (5)

c_1 = cos φ_k · cos(Ω − δ_k)
c_2 = sin α · sin φ_k − cos α · cos φ_k · sin(Ω − δ_k)
```
`ψ_min` = góc ngẩng tối thiểu để có dịch vụ (bài dùng 30°).

**Chứng minh (tóm tắt).**
- "Accessible" ⇔ `ψ_{m,k} ≥ ψ_min` ⇔ (từ (4)) `u_k·(s_m−u_k) / (‖u_k‖‖s_m−u_k‖) ≥ sin ψ_min`  (6).
- Tử số: `u_k·(s_m−u_k) = u_k·s_m − R_E²`.
- Khai triển `u_k·s_m` bằng (1),(2) và rút gọn lượng giác ⇒ `u_k·s_m = R_E(R_E+H_L)·(c_1 cos μ_m + c_2 sin μ_m)`.
- Thay vào (6), với `‖u_k‖ = R_E`, `‖s_m−u_k‖ = d_{m,k}` ⇒ (7):
  `R_E(R_E+H_L)(c_1 cos μ_m + c_2 sin μ_m) / (‖u_k‖ d_{m,k}) ≥ sin ψ_min` ⇒ rút gọn thành (5). ∎

**Ý nghĩa.** `μ_m` biến thiên tất định theo `t` ⇒ **tập vệ tinh khả kiến của mỗi UE tính trước được toàn bộ** chỉ từ ephemeris + vĩ độ/kinh độ UE. Không phải "quét" mọi cặp UE–vệ tinh theo thời gian thực ⇒ **giảm mạnh chi phí tính toán**. Con số `N_max` (số vệ tinh khả kiến tối đa) suy ra từ đây → dùng làm kích thước không gian hành động.

### 3.6. Mô hình kênh LEO (III-B) 🔵

Path loss tổng (theo **3GPP TR 38.811 / TR 38.821**):
```
P_loss = P_loss,b + P_loss,g + P_loss,s + P_loss,e                          (8)
```
| Thành phần | Ý nghĩa | Xử lý trong bài |
|-----------|---------|-----------------|
| `P_loss,b` | Path loss cơ bản | `= F_loss(d,f_c) + SF + CL(α_CL, f_c)`  (9) |
| `P_loss,g` | Suy hao khí quyển + mưa | `= L_zenith(f_c) / sin ψ` (chia theo góc ngẩng) |
| `P_loss,s` | Nhấp nháy (scintillation) | `= 0` với vĩ độ ngoài dải ±20°…±60° |
| `P_loss,e` | Xuyên tường (building entry) | Bỏ qua vì UE ngoài trời có LoS |

- `F_loss(d,f_c) = 32,45 + 20 log₁₀(f_c) + 20 log₁₀(d)`  (10) — **free-space path loss** (`d` tính bằng m, `f_c` bằng GHz).
- `SF` = shadow fading ~ `N(0, σ²_SF)`; `CL` = clutter loss. `SF`, `CL` lấy từ **Bảng 6.6.2 của TR 38.811** theo kịch bản (bài dùng *rural*) và điều kiện LoS.
- **Doppler shift KHÔNG được xét.** Lý do bài đưa ra: 3GPP xác nhận Doppler bù được hiệu quả bằng pre/post-processing (biết quỹ đạo + vị trí UE), lớp vật lý NR thích ứng subcarrier spacing/DMRS; nhiều bài [39–41] đã chứng minh bù được bằng phần cứng/phần mềm.
- Path loss cuối = tổ hợp có trọng số LoS/NLoS theo xác suất LoS:
  ```
  P_loss,m,k = P_LoS · P_loss + (1 − P_LoS) · P_loss,NLoS                    (11)
  ```
- **SNR** (dB):
  ```
  γ_{m,k} = E_EIRP + G_T − K_B − P_loss,m,k − BW                            (12)
  ```
  `E_EIRP` công suất bức xạ đẳng hướng tương đương, `G_T` tỷ số gain/nhiệt tạp, `K_B` hằng số Boltzmann, `BW` băng thông.
- **Throughput (Shannon)**:
  ```
  R_{m,k} = BW_m · log₂(1 + γ_{m,k})   nếu l_{m,k}=1;   = 0 nếu l_{m,k}=0    (13)
  ```
- **Hàm mục tiêu dịch vụ NTN** = trung bình throughput theo thời gian và theo UE:
  ```
  R_NTN = ( Σ_{t∈T} Σ_{s_m∈S} Σ_{u_k∈U} R_{m,k} ) / K                       (14)
  ```

### 3.7. Bài toán tối ưu (P) & LEMMA 3 (III-C) 🔵

```
(P)   max  R_NTN
      s.t. (5)                     — ràng buộc phủ sóng (Lemma 2)
           Σ_{m=1}^M l_{m,k} ≤ 1,  ∀k     (15a)  — mỗi UE nối tối đa 1 vệ tinh
           Σ_{k=1}^K l_{m,k} ≤ J,  ∀m     (15b)  — mỗi vệ tinh phục vụ tối đa J kênh
```

**LEMMA 3.** Với `t = t_0` cố định và tập khả kiến cho trước, `(P)` tương đương một **generalized assignment problem (GAP)** ⇒ **NP-hard**.

**Chứng minh.** Bản tĩnh `(P')` tại `t_0`: tìm `l_{m,k} ∈ {0,1}` tối đa `Σ Σ R_{m,k}` với (15a),(15b). Đây đúng là một GAP (bài toán gán tổng quát, NP-hard kinh điển). Bài toán động `(P)` chứa `(P')` ở **mọi lát thời gian** ⇒ `(P)` cũng NP-hard. ∎

⇒ **Không giải chính xác được** ở quy mô lớn ⇒ chuyển sang **MARL** để tìm lời giải xấp xỉ tốt.

*(Nhận xét về 3 Lemma: Lemma 1–2 là biến đổi hình học/cơ học quỹ đạo, "đóng gói" lại cho gọn — giá trị nằm ở việc chỉ ra tính tất định để cắt action space. Lemma 3 là lập luận rút gọn (reduction) tiêu chuẩn, khá hiển nhiên với ai biết GAP; nó biện minh cho việc dùng học máy chứ không phải một kết quả độ phức tạp sâu sắc.)*

---

## 4. Quy trình CHO & nền tảng RL (Mục IV) 🔵

### 4.1. Quy trình ILCHO — 3 pha (IV-A)

CHO (3GPP Rel-16, TS 38.300) tách **2 sự kiện độc lập**: *preparation event* và *execution event*. BHO thì mạng quyết định thời điểm HO một cách **phản ứng (reactive)** ⇒ dễ HOF. CHO **chủ động (proactive)**: UE tự thực thi khi điều kiện thoả.

| Pha | Diễn biến trong ILCHO |
|-----|----------------------|
| **Preparation** | Sự kiện chuẩn bị thoả → UE gửi **MR** tới **S-LEO**. **T-LEO tối ưu chọn bằng MARL (Algorithm 1)** dựa trên ephemeris (Lemma 1,2) + trạng thái. S-LEO cấu hình các T-LEO ứng viên, gửi *CHO request* → nhận *ACK* → gửi *CHO command* cho UE kèm **hold-off time**; T-LEO **giữ trước tài nguyên vô tuyến**. |
| **Execution** | Khi **sự kiện dựa trên khoảng cách (28)** thoả → UE gửi *HO inform* cho S-LEO; S-LEO forward DL data cho T-LEO; T-LEO đồng bộ với UE, cấp phát UL + random access; UE gửi *CHO confirm* cho T-LEO. |
| **Completion** | Giống BHO: core network đổi bearer, chuyển path; T-LEO gửi *HO complete* cho S-LEO → xong. |

Tức: **DRL chỉ chạy ở pha chuẩn bị** để chọn T-LEO; pha thực thi vẫn dùng **sự kiện A3 kiểu khoảng cách** (28).

### 4.2. Nền tảng RL (IV-B) — xem file 05 để hiểu sâu

- **MDP**: agent thấy `s_t`, chọn `a_t` theo `π`, nhận `r_t`, sang `s_{t+1}`. Mục tiêu: tối đa **return chiết khấu** `R_t = Σ_{i=t}^{T_final} σ^{i−t} r_i`, `σ ∈ (0,1]`.
- **Hàm giá trị hành động** `Q(s,a) = E[R | s,a]`. **Bellman optimality**:
  ```
  Q*(s,a) = E[ r + σ max_{a'} Q*(s',a') | s,a ]                             (17)
  ```
- **Q-learning** (TD, learning rate `β`):
  ```
  Q(s,a) ← Q(s,a) + β [ r + σ max_{a'} Q*(s',a') − Q(s,a) ]                 (18)
  ```
- **DQN**: xấp xỉ `Q(·)` bằng DNN tham số `θ`, loss `L = E[(y − Q(s,a|θ))²]`, `y = r + σ max_{a'} Q(s',a'|θ)`.
  Ổn định nhờ **experience replay** (buffer `D` lưu `(s,a,r,s')`, lấy minibatch ngẫu nhiên → giảm tương quan) và **target network** cập nhật mềm:
  ```
  θ' ← η θ + (1 − η) θ'                                                     (19)
  ```
  *(bản in eq (19) bị lỗi typo cả 2 vế là θ'; ý là soft update như trên.)*

### 4.3. QMIX (IV-C) — xem file 05

- Chọn **QMIX** (value-based). **MADDPG** loại vì kém trong kịch bản hợp tác & khó scale; **MAPPO** mạnh nhưng QMIX **học hiệu quả & hội tụ nhanh hơn** trong bài toán này [43].
- Mỗi UE = 1 agent, **thông tin không đầy đủ** (không thấy quan sát của UE khác).
- **CTDE** (centralized training, decentralized execution): huấn luyện tập trung dùng thông tin toàn cục; thực thi thì mỗi agent chỉ dùng quan sát cục bộ `o_k`.
- **Tính đơn điệu (monotonicity)**: thay vì `Q_tot = Σ_k Q_k` (như VDN [46]), QMIX trộn `Q_k` thành `Q_tot` qua **mixing network** với ràng buộc
  ```
  arg max_a Q_tot(τ,a) = [ arg max_{a1} Q_1(τ_1,a_1), …, arg max_{aK} Q_K(τ_K,a_K) ]   (20)
  Q_tot = f_mix(Q_1,…,Q_K)                                                            (21)
  ∂Q_tot / ∂Q_k ≥ 0,  ∀k                                                              (22)
  ```
  ⇒ hành động tham lam cục bộ ⇒ tăng `Q_tot` toàn cục ⇒ **tín hiệu học nhất quán & ổn định** dù chính sách agent khác đang thay đổi ⇒ khắc phục **non-stationarity** của IQL.
- **3 mạng**: *agent network* (ra `Q_k`, kiến trúc **DRQN** — có GRU để nhớ lịch sử quan sát), *mixing network* (trộn `Q_k → Q_tot`), *hypernetwork* (sinh trọng số **không âm** cho mixing network từ trạng thái toàn cục → đảm bảo (22)).
- **Loss & target**:
  ```
  L_QMIX(θ) = Σ_b [ y_QMIX − Q_tot(τ,a,s; θ) ]²                             (23)
  y_QMIX = r + σ max_{a'} Q_tot(τ⁻,a⁻,s⁻; θ⁻)                               (24)
  θ⁻ ← η_QMIX θ + (1 − η_QMIX) θ⁻   (mỗi T_t bước)                          (25)
  ```
- **Nơi huấn luyện**: **near-RT RIC** (bộ điều khiển RAN thông minh gần thời gian thực, O-RAN [44]) gom quan sát + ephemeris. On-board chỉ chạy **inference** (phát lệnh CHO). Trễ 1 chiều LEO 550 km ≈ **5 ms**.
- **Hiệu lực ephemeris**: timer **T430** / tham số `ntn-UlSyncValidityDuration` (TS 38.331) nhận giá trị **s5 … min20** (5 s – 20 phút) ⇒ lớn hơn nhiều so với trễ tín hiệu ⇒ bỏ qua signaling delay.

---

## 5. Khung MARL của ILCHO (Mục V) 🔵

`(P)` là **general-sum game** (UE vừa hợp tác vừa cạnh tranh tài nguyên vệ tinh hữu hạn) + NP-hard ⇒ mô hình hoá thành **stochastic game**, giải bằng QMIX.

### 5.1. Mô hình MDP

| Thành phần | Định nghĩa |
|-----------|-----------|
| **Agent** | Mỗi UE `k` là 1 agent; môi trường **partially observable**. |
| **State / quan sát cục bộ** | `o^t_k = { (I^t_{k,n}, D^t_{k,n}, L^t_{k,n}, V^t_{k,n}) : n = 1…N_max }`  (26) |
| | `I` = chỉ số logic vệ tinh khả kiến thứ `n`; `D` = khoảng cách tới nó; `L` = số kênh nó đang dùng; `V` = **RVT** (remaining visible time). |
| **Action** | `a^t_k ∈ {1,…,N_max}` — chọn vệ tinh khả kiến thứ mấy làm T-LEO. VD `a_k = 2` ⇒ HO tới vệ tinh `I_{k,2}`. |
| **Reward** | công thức (27) — xem dưới. |

### 5.2. Hàm thưởng (27) — chi tiết & lý do thiết kế

```
        ⎧ −p_1                    nếu HO thành công
r^t_k = ⎨ −p_2                    nếu HOF
        ⎩ −U^t_{k,R} + U^t_{k,RVT}   ngược lại

U_k(x) = c_3 / (1 + e^{ c_1 (x − c_2) })          (hàm dạng sigmoid)
```
- `U_{k,R}` = hàm chi phí **throughput**: `(c_1, c_2, c_3)` = **(âm, dương, dương)** ⇒ throughput cao → reward cao.
- `U_{k,RVT}` = hàm chi phí **RVT**: `(c_1, c_2, c_3)` = **(dương, dương, âm)** ⇒ RVT thấp → bị phạt.
- **Không có số hạng cân bằng tải tường minh.** Nhưng HOF bị phạt nặng (`−p_2`), mà HOF hay xảy ra do vệ tinh quá tải ⇒ agent **tự học** né vệ tinh đông (reward shaping [47]).

**Vì sao sigmoid mà không tuyến tính?** (bài dành hẳn 1 phân tích + thí nghiệm)
- Khi vệ tinh vừa khả kiến: **RVT cao, throughput thấp**. Theo thời gian: **RVT giảm đơn điệu**; **throughput tăng rồi giảm** (vệ tinh tiến tới điểm gần nhất rồi ra xa) ⇒ quan hệ throughput–RVT **phi tuyến, phi đơn điệu**.
- Hàm tuyến tính (30) không tìm được "điểm ngọt": dễ **định giá thấp** vệ tinh còn tốt chỉ vì RVT đang giảm, hoặc **định giá cao** vệ tinh sắp rời vùng phủ.
- Sigmoid tạo **sweet spot**: thưởng cao khi cả throughput lẫn RVT thuận lợi, phạt hai cực ⇒ chính sách HO **bền & nhìn xa** hơn.

**Hàm tuyến tính đối chứng (30):**
```
        ⎧ −p_1 / −p_2                (như trên)
r^t_k = ⎨ w_1 R_NTN + w_2 T_RVT      ngược lại
```
`T_RVT` = RVT của vệ tinh đang phục vụ; `w_1, w_2` trọng số.

### 5.3. Sự kiện thực thi (28) & sự kiện đối chứng (31)

```
Execution (ILCHO):   d_{k,tar} < d_{k,serv} − O_off                        (28)
```
`d_{k,tar}` khoảng cách UE–T-LEO (do action đề xuất), `d_{k,serv}` UE–S-LEO, `O_off` offset. Đây là biến thể **A3 theo khoảng cách** (thay vì A3 theo RSRP).

```
Benchmark A2 (cho MD/MVT):   d_{serving} + O_off < ζ                       (31)
```
`ζ` = ngưỡng khoảng cách mà vượt qua thì S-LEO hết khả kiến.

### 5.4. Algorithm 1 — ILCHO 🔵

```
Khởi tạo: eval net θ_QMIX, target net θ⁻_QMIX, mixing net, hypernetworks
Inputs:   M, K, tham số chòm sao (N_total, N_p, F, α, H_L, t_0e, μ),
          N_max, ψ_min, L, siêu tham số (β, σ, ε, b, N_epi, T_t, η_QMIX)

for n = 1 … N_epi:                                  # mỗi episode
    khởi tạo môi trường LEO (u_k, s_m)
    for t = 1 … T_serv:                             # mỗi bước thời gian (1 s)
        lấy quan sát o^t_k của mọi agent
        for mỗi agent k = 1 … K:
            lấy o^t_k
            chọn a^t_k theo ε-greedy
            chọn T-LEO tối ưu ở pha Preparation
            if T-LEO thoả (28):                     # sự kiện thực thi
                thực hiện HO
                nhận r^t_k, o^{t+1}_k
                lưu (o^t, τ^t, a^t, r^t, o^{t+1}, τ^{t+1}) vào replay buffer D
        lấy minibatch b từ D
        tính â qua (21); tính target (24) & loss (23)
        cập nhật mạng bằng minimize (23)
        if (t mod T_t == 0): cập nhật target net (25)
```

### 5.5. Độ phức tạp

```
Training:  O( b·N_epi·T_s · [ K(P_a + N_max) + (P_m + P_h)/T_update + P_t/T_t ] )   (29)
```
`P_a, P_m, P_h, P_t` = số tham số agent/mixing/hyper/… net. Vì `N_max` = hằng (từ Lemma 2) và kích thước mạng cố định ⇒ **Training = O(K)**; **Inference = O(K(P_a+N_max)+P_m+P_h) = O(K)**.
⇒ **tuyến tính theo số UE**, KHÔNG phụ thuộc `N_total` (tổng số vệ tinh). Đây là lợi thế scale then chốt.

---

## 6. Mô phỏng & kết quả (Mục VI) 🔵

### 6.1. Thiết lập

| Tham số | Giá trị |
|---------|---------|
| Chòm sao thử | Starlink **Phase 1-a** (≈550 km) & **Phase 2-a** (≈340–370 km); + **hybrid** |
| `N_total` | 1 584 (Phase 1-a) / 5 280 (Phase 2-a) *(theo bản dịch Bảng II)* |
| Khu vực dịch vụ | [39–41° N] × [39–41° E], UE đặt ngẫu nhiên |
| Số UE | 5 → 100 |
| Kịch bản | Rural; LoS prob theo Bảng 6.6.2-1 của TR 38.821 |
| Băng tần | Ka-band, kênh 250 MHz *(bản dịch)* |
| `ψ_min` | 30° |
| `J` (kênh/vệ tinh) | 8 *(bản dịch)* |
| Thời lượng dịch vụ `T_s` | 10 phút, slot 1 s |
| `N_max` (max accessible links) | **17** (Phase 1-a) / **27** (Phase 2-a) — từ Lemma 2, Hình 5 |
| ε-greedy | 0,9 → 0,1 |
| Learning rate `β` | 1e−4 |
| Discount `σ` | 0,99 |
| Số episode | 3 000 → 30 000 (tăng theo số UE) |
| Cài đặt | Python 3.11 + PyTorch 2.1.0 |

**HOF được định nghĩa** (bài): HO tới T-LEO (1) thiếu tài nguyên, hoặc (2) đã hết RVT, hoặc (3) không còn accessible.

### 6.2. Hội tụ & sigmoid vs linear (Hình 6, 7)

- **Sigmoid** (Hình 6, 30 agents, Phase 2-a): tổng score hội tụ mượt; số HO & HOF **giảm dần**, throughput **tăng dần** theo episode ⇒ học hiệu quả.
- **Linear** (Hình 7, cùng điều kiện): tổng reward có xu hướng hội tụ, **nhưng HOF và throughput dao động mạnh, không hội tụ** ⇒ minh chứng thực nghiệm cho lập luận phi tuyến throughput–RVT.

### 6.3. So sánh 4 baseline trên Phase 2-a (Hình 8)

| Baseline | Cơ chế | Trigger thực thi |
|----------|--------|------------------|
| **MD-CHO** | HO tới vệ tinh khả kiến **gần nhất** | A2 theo khoảng cách (31) |
| **MVT-CHO** | HO tới vệ tinh **RVT dài nhất** | A2 (31) |
| **HSNF** [22] | Network-flow trên đồ thị, ma trận chi phí (throughput + băng thông còn lại) | — |
| **LBSH** [26] | Multi-agent Q-learning; reward = RVT + tải thấp + phạt HO lớn | — |

**Kết quả (đọc từ Hình 8, 5→100 UE):**

| Chỉ số | ILCHO | HSNF | MVT-CHO | MD-CHO | LBSH |
|--------|-------|------|---------|--------|------|
| Số HO / service duration | **10,8 → 12,95** (≈ ổn định) | ≈ 10 (ổn định) | 10 → ~24 | 10 → ~38 | 33 → ~65 |
| Số HOF / service duration | **0,48 (≤50 UE) → 1,38 (100 UE)** | ≈ 10 (không giảm) | 0 → ~20 | 0 → ~25 | ~4 → ~30 |
| Throughput (bps/Hz) | **3,85 (5) / 3,79 (50) / 3,76 (100)** | ~3,65–3,70 | ~3,5–3,6 | ~3,55–3,6 | 3,4–3,6 |

- Với 5 UE: ILCHO HO ~ mỗi **55,56 s**; với 100 UE: ~ mỗi **46,32 s** → gần như không đổi dù tải ×20.
- MD/MVT/LBSH tăng vọt HO & HOF khi UE tăng: **tương quan cao giữa các UE** (khoảng cách giữa các UE nhỏ so với khoảng cách tới vệ tinh) ⇒ nhiều UE cùng chọn "vệ tinh tốt nhất" theo một tiêu chí đơn ⇒ nghẽn.
- HSNF ổn định về số HO nhưng **HOF ~10 không giảm**: tính chi phí mọi cặp UE–vệ tinh theo thời gian thực bất khả thi ở quy mô mega.

### 6.4. Phase 1-a (Hình 9)

- Độ cao 550 km ⇒ **RVT dài hơn**, số vệ tinh khả kiến **ít hơn** (max 17).
- ILCHO & HSNF: số HO ổn định theo số UE. ILCHO: **8 → 9,17 HO / service duration** (HO mỗi 65–75 s).
- MVT bất ổn từ ≥ 15 UE (ít vệ tinh khả kiến); MD tụt ổn định mạnh (tương quan UE cao khi ít vệ tinh).
- ILCHO giữ **HOF < 0,98**, throughput cao nhất ⇒ tận dụng tốt **TLE** (khoảng cách, elevation) thay vì trigger theo đo đạc.

### 6.5. Chòm sao hybrid (Bảng III, Hình 10)

| Chỉ số | Phase 1-a (TB / min / max) | Phase 2-a | Hybrid |
|--------|---------------------------|-----------|--------|
| Số HO | 8,64 / 8,00 / 9,20 | 12,67 / 10,80 / 13,42 | 12,24 / 9,00 / 13,16 |
| HOF | 0,53 / 0,00 / 0,97 | 0,67 / 0,00 / 1,50 | 0,97 / 0,53 / 1,47 |
| Throughput (bps/Hz) | 3,375 / 3,325 / 3,474 | 3,788 / 3,754 / 3,846 | 3,647 / 3,572 / 3,748 |

Hybrid kế thừa: **số HO thấp** như Phase 1-a + **throughput cao** như Phase 2-a. HOF không khác biệt lớn giữa 3 kịch bản.

### 6.6. Fairness & Load balance (VI-A)

- **Jain's Fairness Index**: `J_JFI = (Σ_k R_k)² / (K · Σ_k R_k²)`  (32), càng gần 1 càng công bằng.
- Với 100 agents, Phase 2-a (Hình 11): **JFI = 0,9798**; throughput bách phân vị 10 = **3,50 bps/Hz**, median = 3,846, trung bình = 3,757 ⇒ **không có UE biên bị "đói"**.
- **Cân bằng tải** = phương sai của **channel occupancy** `O_{m,t} = L_{m,t}/J`. Với 50 agents, Phase 2-a (Bảng IV):

  | ILCHO | MD-CHO | MVT-CHO | LBSH | HSNF |
  |-------|--------|---------|------|------|
  | **0,072** | 0,372 | 0,400 | 0,077 | 0,089 |

  ILCHO phân bổ đều nhất — **hệ quả gián tiếp** của phạt HOF (né vệ tinh quá tải), dù reward không có số hạng tải.

---

## 7. Kết luận & hướng phát triển của bài (Mục VII) 🔵

- ILCHO hỗ trợ quyết định HO trong NTN nhiều LEO. Vì LEO nhanh + trễ dài, không dùng được trigger theo đo đạc của TN.
- ILCHO suy trạng thái vệ tinh (vị trí, quỹ đạo) → điều kiện khả kiến → chọn T-LEO tối ưu (throughput cao, ít HO).
- Dùng **"LEO satellite movement predictions" của MARL** + sự kiện thực thi theo khoảng cách ở pha chuẩn bị CHO.
- Kết quả: số HO ổn định hơn, throughput cao hơn các sơ đồ HO NTN khác.
- **Hướng tương lai (bài nêu):** xét thêm các yếu tố suy giảm hiệu năng khác trong NTN LEO; bài toán điều khiển sẽ phức tạp hơn, tối ưu khả mở rộng khó hơn.

---

## 8. Điểm mạnh & hạn chế (tổng hợp — xem file 08 để phản biện sâu)

**Điểm mạnh**
- Cơ sở toán chặt (3 Lemma), mô hình từ tham số Starlink thật (Bảng I).
- Thiết kế action space theo `N_max` → **giải quyết được vấn đề scale** mà các bài RL trước vấp.
- So sánh công bằng, nhiều baseline (MD/MVT/HSNF/LBSH), nhiều kịch bản (Phase 1-a/2-a/hybrid).
- **Ablation reward** (sigmoid vs linear) có lý do vật lý rõ ràng + bằng chứng.
- Bàn đủ về fairness (JFI) và load balance (phương sai occupancy).

**Hạn chế**
1. **Không phải "prediction" theo nghĩa ML.** Vị trí vệ tinh **tất định** từ ephemeris (Lemma 1). "Trí tuệ" nằm ở **ra quyết định** (RL action), không ở dự đoán đại lượng bất định (RSRP tương lai, thời điểm suy giảm link, tải tương lai...). Câu "movement predictions" ở Mục VII dễ gây hiểu nhầm.
2. **UE cố định (fixed VSAT)** — không có UE mobility (handheld/IoT di động, tàu, máy bay).
3. **Bỏ qua Doppler** — chỉ giả định đã bù ở lớp vật lý.
4. **Huấn luyện tốn** (3 000–30 000 episodes) — chưa phân tích khả thi online/real-time learning trên near-RT RIC thật; chưa nói thời gian tường (wall-clock).
5. **Chưa xét multi-connectivity**, chưa dự đoán tải tương lai của vệ tinh lân cận.
6. **Một khu vực địa lý hẹp** ([39–41°N/E]) — chưa quét theo vĩ độ cao/thấp, chưa vùng cực.
7. **Reward có `p_1` phạt cả HO thành công** — hợp lý để giảm số HO, nhưng đánh đổi với việc bám vệ tinh sắp khuất; chưa có sensitivity analysis theo `p_1, p_2, c_1, c_2, c_3, O_off`.
8. **Thiếu chi tiết tái lập**: kiến trúc mạng (số lớp/nơ-ron GRU), giá trị `p_1,p_2,c_i`, `O_off`, `ζ`, `T_t`, batch size, số seed/độ lệch chuẩn của kết quả — phần lớn không cho.

---

## 9. Danh mục tham chiếu quan trọng trong bài (để đọc tiếp cho survey)

| Ref | Nội dung | Vì sao nên đọc |
|-----|----------|----------------|
| [7] 3GPP TR 38.821 | Solutions for NR to support NTN | Nguồn gốc mọi con số HO, kênh, CHO trong NTN |
| [6] 3GPP TR 38.811 | Study on NR to support NTN | Mô hình kênh, path loss, Bảng 6.6.2 |
| [34] 3GPP TS 38.300 | NR & NG-RAN Stage-2 (Rel-16) | Định nghĩa CHO |
| [45] 3GPP TS 38.331 | RRC protocol | `ntn-UlSyncValidityDuration`, T430, SIB19 |
| [17] 3GPP R2-1700544 | Conditional handover | Đề xuất CHO gốc |
| [32] Rashid et al., **QMIX**, ICML 2018 ([arXiv:1803.11485](https://arxiv.org/abs/1803.11485)) | Thuật toán MARL dùng trong bài | Bắt buộc cho file 05 |
| [46] Sunehag et al., **VDN**, 2017 ([arXiv:1706.05296](https://arxiv.org/abs/1706.05296)) | `Q_tot = Σ Q_k` — baseline của QMIX | Hiểu vì sao cần mixing net |
| [42] Mnih et al., **DQN**, *Nature* 2015 | Nền tảng deep RL | — |
| [47] Sutton & Barto, *RL: An Introduction*, 2nd ed., 2018 | Sách gối đầu RL | reward shaping, TD, Q-learning |
| [22] Zhang et al., network-flow HO (**HSNF**), IEEE WCL 2021 | Baseline | — |
| [26] Badini et al., RL load-balancing HO trên NS-3 (**LBSH**), IEEE ICC 2023 | Baseline | — |
| [28] Lee et al., HO protocol learning cho LEO, IEEE TWC 2024 | DRL, vệ tinh tự quyết | So sánh cách đặt bài toán |
| [30] Juan et al., đánh giá CHO 5G NR trên LEO NTN, WCNC 2022 | CHO + overhead | — |
| [31] Wang et al., seamless HO trong LEO NTN, IEEE TC 2023 | CHO + service continuity | — |
| [44] Mahboob et al., O-RAN cho NTN, IEEE ComMag 2025 | near-RT RIC | Kiến trúc triển khai |

---

### Nguồn tham khảo (ngoài bài báo)
- 3GPP, *Non-Terrestrial Networks (NTN) overview* — https://www.3gpp.org/technologies/ntn-overview
- T. Rashid et al., "QMIX: Monotonic Value Function Factorisation for Deep MARL," — https://arxiv.org/abs/1803.11485 ; bản mở rộng JMLR https://arxiv.org/abs/2003.08839
- P. Sunehag et al., "Value-Decomposition Networks..." — https://arxiv.org/abs/1706.05296
- Handover Technique in LEO Satellite Networks: A Review (IEEE) — https://ieeexplore.ieee.org/document/10652688
