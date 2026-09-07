# Conditional Handover (CHO) — chi tiết

> 🟢 = khảo sát ngoài. 🔵 = cách ILCHO dùng. CHO là **khung** mà ILCHO cắm bộ điều khiển MARL vào.

---

## 1. Vấn đề CHO giải quyết 🟢

Trong **BHO** (baseline HO, xem file 02 §2), gNB nguồn nhận MR → **quyết định ngay** → gửi HO command
qua chính liên kết đang yếu dần. Nếu liên kết nguồn tụt quá nhanh (UE tốc độ cao, mmWave chặn tia,
**vệ tinh LEO khuất nhanh**), HO command **không tới được UE** hoặc UE **không kịp** truy nhập cell
đích → **RLF / HOF**. HOF tập trung ở **pha chuẩn bị**.

**Ý tưởng CHO (3GPP Rel-16, TS 38.300 / R2-1700544):** 🟢
1. **Chuẩn bị sớm**, khi liên kết nguồn **còn tốt**: gNB nguồn chuẩn bị HO tới **nhiều cell ứng viên**
   cùng lúc, đẩy sẵn cấu hình RRC cho UE.
2. **Hoãn thực thi**: UE **giữ** cấu hình CHO, tự **giám sát điều kiện thực thi**; khi một cell ứng
   viên thoả điều kiện, UE **tự chuyển ngay** — không cần hỏi lại gNB nguồn.

⇒ Tách **"preparation event"** khỏi **"execution event"**. Quyết định "sẽ đi đâu" làm sớm; "đi lúc
nào" để UE tự chốt theo điều kiện. Kết quả: **HOF giảm mạnh**, robust hơn với biến động nhanh.
Interruption time vẫn ~ như hard HO (~30–60 ms) — CHO **không** giảm HIT (đó là việc của DAPS).

---

## 2. Hai sự kiện của CHO 🔵🟢

### 2.1. Preparation event (sự kiện chuẩn bị)
- Kích hoạt việc gNB nguồn bắt đầu chuẩn bị các cell ứng viên.
- Trong TN thường là **A3 với offset lớn hơn** ngưỡng thực thi (chuẩn bị trước khi thật sự cần đi).
- 🔵 **ILCHO:** khi preparation event thoả → UE gửi MR → **bộ MARL/QMIX chọn T-LEO tối ưu** trong tập
  vệ tinh accessible (Lemma 2) dựa trên state `(I, D, L, RVT)`. S-LEO gửi *CHO request* tới các T-LEO
  ứng viên, nhận *ACK*, gửi *CHO command* + **hold-off time** cho UE; T-LEO **giữ trước tài nguyên**.

### 2.2. Execution event (sự kiện thực thi)
- UE giám sát; khi thoả với một cell đã chuẩn bị → UE thực thi HO ngay.
- Trong TN thường là **A3** (neighbor hơn serving một offset) — nhưng offset/ngưỡng **chặt hơn**
  preparation event.
- 🔵 **ILCHO:** dùng **sự kiện dựa trên khoảng cách** thay cho A3-RSRP:
  ```
  d_{k,tar} < d_{k,serv} − O_off        (eq 28)
  ```
  UE HO khi T-LEO đã gần hơn S-LEO một biên `O_off`. (Baseline MD/MVT dùng **A2 theo khoảng cách**:
  `d_serv + O_off < ζ` — chỉ đi khi S-LEO **sắp hết** accessible.)

---

## 3. CHO cho NTN: các trigger đặc thù 🟢

3GPP mở rộng điều kiện kích hoạt CHO cho NTN (TR 38.821, TS 38.331) vì đo RSRP không đủ tin:

| Trigger | Cơ sở | Ghi chú |
|---------|-------|---------|
| **Measurement-based** | RSRP/RSRQ (sự kiện A3/A4/A5) | Kém tin trong NTN (cell ở xa, RSRP na ná) |
| **Time-based** (điều kiện T1) | "từ thời điểm t_start đến t_stop" | Vì quỹ đạo tất định → biết trước cửa sổ phục vụ |
| **Location-based** | Khoảng cách UE↔điểm tham chiếu cell, hoặc UE↔vệ tinh | 🔵 ILCHO dùng biến thể này (khoảng cách) |
| **Elevation-angle-based** | Góc ngẩng tới vệ tinh nguồn/đích so với ψ_min | Gắn trực tiếp với điều kiện "accessible" (Lemma 2) |
| **Timing-Advance-based** | Giá trị TA (tỉ lệ khoảng cách) | Tương đương location-based |

UE cần **ephemeris (SIB19)** + **vị trí bản thân (GNSS)** để đánh giá các trigger time/location/
elevation. 🔵 ILCHO giả định UE có "prior knowledge of the ephemeris data".

**"Location-based CHO"** là hướng được ưa chuộng cho NTN: dùng **thông tin chuyển động vệ tinh
(ephemeris)** làm điều kiện đo → không phụ thuộc chất lượng tín hiệu tức thời.

---

## 4. So sánh BHO / CHO / DAPS / CHO+DAPS 🟢

| | BHO | **CHO** | DAPS | CHO+DAPS |
|--|-----|---------|------|----------|
| 3GPP | ≤Rel-15 | Rel-16 | Rel-16 | Rel-17+ |
| Chuẩn bị | 1 cell, muộn | **nhiều cell, sớm** | 1 cell | nhiều cell, sớm |
| Ai chốt thời điểm | gNB nguồn (reactive) | **UE (proactive)** | gNB nguồn | UE |
| Mục tiêu chính | — | **↓ HOF** (robustness) | **↓ HIT ≈ 0 ms** | cả hai |
| HIT | 30–60 ms | 30–60 ms | ~0 ms | ~0 ms |
| Chi phí | thấp | tài nguyên giữ trước ở nhiều cell; báo hiệu chuẩn bị dư | UE phải thu/phát 2 cell đồng thời | cao nhất |
| Hợp với NTN? | không | **có** (3GPP chọn cho NTN) | khó (2 vệ tinh xa nhau, Doppler khác) | nghiên cứu |

🔵 **ILCHO chọn CHO** vì bài toán NTN là **robustness/HOF & số HO**, không phải HIT. Phần "trí tuệ"
được cắm vào **chỗ chọn cell ứng viên ở pha chuẩn bị**.

---

## 5. Overhead & nhược điểm của CHO 🟢

- **Giữ tài nguyên trước ở nhiều cell ứng viên** → lãng phí nếu chuẩn bị thừa.
- **Báo hiệu chuẩn bị dư** khi UE cuối cùng không HO tới cell đã chuẩn bị (ref [30] của bài chỉ ra:
  CHO "brings mobility enhancement but can cause excessive signaling overhead due to unnecessary
  HOs").
- Cần thuật toán **chọn đúng & đủ** cell ứng viên → đây chính là chỗ ML/RL có giá trị.
- 🔵 ILCHO gián tiếp giảm overhead này bằng cách: (a) chọn T-LEO tối ưu (ít HO hơn), (b) phạt `p_1`
  cho **mọi** HO (kể cả thành công) trong reward → agent học tiết chế số HO.

---

## 6. CHO trong bức tranh "AI cho HO" 🟢

Nhiều bài "AI cho HO trong NTN" thực chất = **học bộ chọn cell ứng viên / tham số trigger cho CHO**:
- Học **cell đích tối ưu** (ILCHO, [28], [31]).
- Học **offset/hysteresis/TTT** thích nghi (MRO bằng RL — chủ yếu ở TN).
- Học **thời điểm** kích hoạt preparation (dự đoán khi nào link suy giảm).
- Học **số lượng** cell ứng viên cần chuẩn bị (đánh đổi robustness ↔ overhead).

🔵 ILCHO nằm ở nhánh **"học cell đích tối ưu"**, với đầu vào là **trạng thái hình học tất định**
(khoảng cách, RVT, tải, chỉ số vệ tinh) chứ không phải chuỗi đo tín hiệu.

---

## 7. Từ khoá tra cứu thêm
`conditional handover CHO 3GPP TS 38.300`, `CHO execution condition CondEvent A3 A4 A5`,
`CHO NTN time-based location-based trigger`, `CHO candidate cell preparation`,
`CHO signaling overhead NTN`, `location-based handover LEO ephemeris`.

---

## Nguồn tham khảo (ngoài bài báo)
- arXiv 2204.01283, *Conditional Handover in 5G – Principles, Future Use Cases and FR2 Performance* — https://arxiv.org/pdf/2204.01283
- IEEE Xplore 10322919, *Conditional Handover for Non-Terrestrial Networks* — https://ieeexplore.ieee.org/document/10322919/
- IEEE Xplore 9771987 (= ref [30] của bài), *Performance Evaluation of the 5G NR Conditional Handover in LEO-based NTN* — https://ieeexplore.ieee.org/document/9771987/
- Amarisoft Tech Academy, *NR SA CHO (Conditional Handover)* — https://tech-academy.amarisoft.com/NR_SA_CHO.html
- arXiv 2507.07581, *Conditional Handovers via Meta-Learning (CHOMET)* — https://arxiv.org/pdf/2507.07581
- The 3G4G Blog, *DAPS Handover* — https://blog.3g4g.co.uk/2020/10/understanding-daps-handover.html
- 3GPP TS 38.300, TS 38.331, TR 38.821 — https://www.3gpp.org
