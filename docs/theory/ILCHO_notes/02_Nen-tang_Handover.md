# Nền tảng Handover (chuyển giao)

> Mục tiêu: nắm chắc HO trong mạng di động mặt đất (TN) trước khi hiểu vì sao NTN cần cơ chế khác.
> 🟢 = kiến thức nền khảo sát ngoài; nguồn ở cuối file. 🔵 = cách bài ILCHO dùng khái niệm đó.

---

## 1. Handover là gì

**Handover (HO)** / handoff = quá trình chuyển kết nối vô tuyến đang hoạt động của một UE
(user equipment) từ một cell/beam/tần số/công nghệ này sang một cái khác **mà không ngắt dịch vụ**
(lý tưởng). Mục đích: giữ liên tục phiên khi UE di chuyển, cân bằng tải, tránh rớt cuộc gọi. 🟢

**Vì sao cần:** khi UE rời xa base station (BS) phục vụ, tín hiệu yếu dần; một BS lân cận mạnh lên.
Nếu không chuyển kịp → **rớt liên kết**. 🟢

### 1.1. Phân loại theo cơ chế vô tuyến 🟢
| Loại | Mô tả | Ghi chú |
|------|-------|---------|
| **Hard HO** ("break-before-make") | Ngắt kết nối cũ **trước** khi nối cái mới | Có **khoảng gián đoạn** (interruption time). LTE/NR dùng mặc định. |
| **Soft HO** ("make-before-break") | Giữ đồng thời ≥2 kết nối rồi mới bỏ cái cũ | Đặc trưng CDMA/3G. Tốn tài nguyên. |
| **Softer HO** | Soft HO giữa các sector cùng một BS | 3G |

### 1.2. Phân loại theo phạm vi 🟢
- **Intra-frequency / inter-frequency**: cùng hay khác tần số sóng mang.
- **Intra-RAT / inter-RAT**: cùng hay khác công nghệ truy nhập (VD LTE ↔ NR).
- **Intra-gNB / inter-gNB**: trong cùng trạm hay khác trạm (khác → cần báo hiệu qua Xn/NG core).
- **Xn-based vs N2(S1)-based**: đường báo hiệu giữa 2 gNB hay qua lõi.
- **Beam-level mobility** (NR FR2/mmWave): chuyển giữa các beam trong cùng cell — xử lý ở lớp vật lý/MAC, không phải HO lớp RRC.

---

## 2. Quy trình HO cơ bản trong 5G NR (network-controlled, UE-assisted) 🟢

Đây là **BHO — baseline handover** mà bài ILCHO đối chiếu.

```
1. Measurement configuration:  gNB nguồn gửi UE danh sách cần đo (RRCReconfiguration),
                               kèm ngưỡng/ offset / TTT của các "sự kiện" A1–A6.
2. Measurement & evaluation:   UE đo RSRP/RSRQ/SINR các cell lân cận (từ SSB/CSI-RS).
3. Measurement Report (MR):    khi một sự kiện thoả trong suốt Time-To-Trigger (TTT),
                               UE gửi MR lên gNB nguồn.
4. HO decision:                gNB nguồn quyết định HO và chọn cell đích.
5. HO preparation:             gNB nguồn → gNB đích: "Handover Request";
                               gNB đích cấp phát tài nguyên (admission control) → "Handover Request ACK"
                               (chứa cấu hình RRC cho UE).
6. HO execution / command:     gNB nguồn gửi "RRCReconfiguration" (HO command) cho UE.
                               UE tách khỏi cell nguồn, đồng bộ cell đích, làm Random Access (RACH).
                               >>> Đây là lúc có HANDOVER INTERRUPTION TIME (HIT), ~30–60 ms.
7. HO completion:              UE gửi "RRCReconfigurationComplete" cho gNB đích.
                               Path switch ở core (UPF/AMF), release tài nguyên ở gNB nguồn.
```

**Điểm yếu của BHO:** quyết định HO (bước 4) và thực thi (bước 6) **gắn liền nhau, phản ứng (reactive)**.
Nếu tín hiệu tụt quá nhanh (UE tốc độ cao, mmWave, hoặc **vệ tinh LEO bay 7,59 km/s**), MR/HO command
có thể tới **quá muộn** → **HOF**. 🔵 *ILCHO thay bước 4 bằng bộ chọn T-LEO học bằng MARL, và tách
hẳn bước 6 thành một "execution event" độc lập theo khoảng cách (CHO — xem file 04).*

---

## 3. Các sự kiện đo (measurement events) A1–A6 🟢

3GPP (TS 36.331 cho LTE, TS 38.331 cho NR) định nghĩa các sự kiện kích hoạt MR. Metric thường là
**RSRP** (Reference Signal Received Power), RSRQ, hoặc SINR của SpCell (serving) và các cell lân cận.

| Sự kiện | Điều kiện kích hoạt | Dùng cho |
|---------|--------------------|----------|
| **A1** | Serving **tốt hơn** ngưỡng | Huỷ đo inter-freq / dừng HO |
| **A2** | Serving **xấu hơn** ngưỡng | Bắt đầu đo để chuẩn bị HO; **trigger "phòng hờ"** |
| **A3** | Neighbor **hơn** SpCell một **offset** (`Mn + Ofn + Ocn − Hys > Mp + Ofp + Ocp + Off`) | **HO phổ biến nhất** (intra/inter-freq) |
| **A4** | Neighbor **tốt hơn** ngưỡng (tuyệt đối, không so serving) | HO theo tải, HO khi serving vẫn ổn |
| **A5** | SpCell **xấu hơn** ngưỡng1 **VÀ** neighbor **tốt hơn** ngưỡng2 | HO khi serving đã kém (kết hợp A2+A4) |
| **A6** | Neighbor hơn **SCell** một offset | Carrier Aggregation (đổi SCell), thường không phải HO |
| B1/B2 | Tương tự A4/A5 nhưng cho **inter-RAT** (cell công nghệ khác) | HO liên RAT |

**Tham số điều chỉnh:** `Offset` (Ofn/Ocn), `Hysteresis` (Hys), `Time-To-Trigger` (TTT).
- Offset/Hys/TTT **lớn** → ít HO hơn, ít **ping-pong**, nhưng **HOF cao** (chuyển muộn).
- Offset/Hys/TTT **nhỏ** → HO sớm, ít HOF, nhưng nhiều **ping-pong**. → đây là **đánh đổi cốt lõi**. 🟢

🔵 **Trong ILCHO:** A3 kinh điển dùng **RSRP** không đáng tin trong NTN (cell vệ tinh ở xa, RSRP gần
giống nhau, biến thiên khó lường — TR 38.821). Nên:
- Pha thực thi ILCHO: **A3 theo khoảng cách** — `d_{k,tar} < d_{k,serv} − O_off`  (eq 28).
- Baseline MD/MVT: **A2 theo khoảng cách** — `d_serving + O_off < ζ`  (eq 31).

---

## 4. Các chỉ số hỏng & KPI của HO 🟢

| Thuật ngữ | Định nghĩa |
|-----------|-----------|
| **HOF — Handover Failure** | HO khởi động nhưng không hoàn tất: RACH tới cell đích thất bại, T304 hết hạn, hoặc cell đích từ chối. Liên kết vô tuyến vốn còn tốt nhưng **báo hiệu HO hỏng**. |
| **RLF — Radio Link Failure** | Mất đồng bộ vô tuyến (out-of-sync liên tục / hết T310 / RACH hỏng tối đa). Thường vì HO **quá muộn** hoặc tới **nhầm cell**. |
| **Too-late HO** | RLF xảy ra ở cell nguồn **trước khi** HO kịp kích hoạt. |
| **Too-early HO** | HO xong thì lập tức RLF ở cell đích, hoặc quay lại cell nguồn ngay. |
| **HO to wrong cell** | RLF ở cell đích ngay sau HO, rồi UE nối sang cell thứ ba. |
| **Ping-pong HO** | UE bị đẩy qua lại A→B→A trong khoảng thời gian rất ngắn (dwell time nhỏ). Tốn báo hiệu, hao pin. |
| **HIT — HO Interruption Time** | Thời gian UE không thu/phát được dữ liệu người dùng trong lúc HO (~30–60 ms với hard HO; ~0 ms với DAPS). |
| **HOPP rate** | Số ping-pong / đơn vị thời gian. |
| **HOFP** | HOF trên mỗi HO (xác suất). |

🔵 **ILCHO định nghĩa HOF hẹp hơn** (đặc thù mô phỏng vệ tinh): HO tới T-LEO mà (1) thiếu tài nguyên
kênh, (2) đã hết RVT, hoặc (3) không còn accessible. Không mô phỏng RACH/T304.

**MRO — Mobility Robustness Optimization** 🟢: nhánh SON (Self-Organizing Networks) tự động chỉnh
Offset/Hys/TTT để giảm HOF + RLF + ping-pong. Bản chất cũng là **đánh đổi HOF ↔ ping-pong**. Nhiều
bài "AI cho HO" trong TN thực chất là MRO bằng ML.

---

## 5. Các kiểu HO nâng cao (bối cảnh để đặt CHO) 🟢

| Cơ chế | 3GPP | Ý tưởng | Interruption |
|--------|------|---------|--------------|
| **BHO** (baseline) | ≤ Rel-15 | Quyết định + thực thi gắn liền, network-controlled | ~30–60 ms |
| **CHO** (Conditional HO) | **Rel-16** | Chuẩn bị **sớm** nhiều cell đích; UE tự thực thi khi điều kiện thoả | ~30–60 ms nhưng **HOF ↓ mạnh** |
| **DAPS** (Dual Active Protocol Stack) | **Rel-16** | Make-before-break: giữ song song stack nguồn + đích | **~0 ms** HIT, đổi lại UE phức tạp (thu/phát 2 cell) |
| **CHO + DAPS** | Rel-17+ | Kết hợp | ~0 ms + robust |
| **L1/L2-Triggered Mobility (LTM)** | **Rel-18** | HO điều khiển ở lớp 1/2, giảm trễ báo hiệu RRC | rất thấp |

🔵 **ILCHO xây trên CHO** (không phải DAPS). Xem file 04 cho CHO chi tiết.

---

## 6. Vì sao HO của TN không bê thẳng sang NTN được 🔵🟢

| Khía cạnh | TN | NTN / LEO |
|-----------|----|-----------|
| Ai di chuyển | UE di chuyển, BS đứng yên | **Vệ tinh (cell) bay ~7,5 km/s**, UE gần như đứng yên |
| Nhịp HO | phút–giờ | **mỗi 6,61–132,28 s** (TR 38.821) |
| Cơ sở quyết định | RSRP/RSRQ đo được, tương phản rõ giữa các cell | RSRP các cell vệ tinh **gần giống nhau & khó lường** (khoảng cách lớn) → đo không phân biệt được |
| Trễ | ms | 1 chiều ~ 5 ms (LEO 550 km) → ~25–270 ms (GEO); MR có thể **lỗi thời** khi tới nơi |
| Tính dự đoán | quỹ đạo UE ngẫu nhiên | **quỹ đạo vệ tinh tất định** từ ephemeris → biết trước cell nào sẽ phủ, khi nào |
| Doppler | nhỏ | lớn (vài trăm kHz), cần bù |

⇒ Hệ quả thiết kế: NTN nên dùng **thông tin quỹ đạo/ vị trí/ elevation/ thời gian** (deterministic)
thay cho đo tín hiệu; và nên **chuẩn bị sớm** (CHO) vì cửa sổ quyết định rất hẹp. Đây chính là
triết lý của ILCHO.

---

## 7. Từ khoá để tra cứu thêm
`handover LTE NR procedure`, `A3 event offset hysteresis time-to-trigger`, `mobility robustness
optimization`, `conditional handover CHO`, `DAPS handover`, `RLF radio link failure T310 T304`,
`ping-pong handover rate`, `LTM L1/L2 triggered mobility Rel-18`, `beam management NR`.

---

## Nguồn tham khảo (ngoài bài báo)
- devopedia, *5G UE Measurements and Reporting* — https://devopedia.org/5g-ue-measurements-and-reporting
- RF Wireless World, *5G NR Event Reporting: A1–A6 Measurement Triggers* — https://www.rfwireless-world.com/articles/5g-nr-event-reporting
- ShareTechnote, *LTE MultiCell Measurement / Events* — https://www.sharetechnote.com/html/Handbook_LTE_MultiCell_Measurement_LTE.html
- The 3G4G Blog, *Understanding the Dual Active Protocol Stack (DAPS) Handover in 5G* — https://blog.3g4g.co.uk/2020/10/understanding-daps-handover.html
- Ericsson, *Reducing mobility interruption time in 5G networks* — https://www.ericsson.com/en/blog/2020/4/reducing-mobility-interruption-time-5g-networks
- TechPlayon, *5G NR DAPS Handover – 3GPP Release 16* — https://www.techplayon.com/5g-nr-dual-active-protocol-stack-daps-handover-3gpp-release-16/
- ResearchGate, *Mobility Robustness Optimization for Handover Failure Reduction in LTE Small-Cell Networks* — https://www.researchgate.net/publication/322091106
- arXiv 2204.01283, *Conditional Handover in 5G – Principles, Future Use Cases and FR2 Performance* — https://arxiv.org/pdf/2204.01283
- 3GPP TS 38.331 (RRC), TS 38.300 (NR & NG-RAN Stage-2), TR 38.821 (Solutions for NR to support NTN) — https://www.3gpp.org
