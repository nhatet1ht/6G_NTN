# Nền tảng NTN & vệ tinh LEO

> 🟢 = khảo sát ngoài (nguồn cuối file). 🔵 = cách bài ILCHO dùng.

---

## 1. NTN là gì

**NTN — Non-Terrestrial Network** (mạng phi mặt đất): mạng truy nhập vô tuyến dùng nút bay/vũ trụ
làm trạm phát — vệ tinh (LEO/MEO/GEO/HEO), HAPS (khí cầu tầng bình lưu), UAV. 3GPP tích hợp NTN vào
5G NR để phủ sóng nơi hạ tầng mặt đất không tới: đại dương, sa mạc, vùng núi, vùng thiên tai, IoT
mật độ cao, hàng không/hàng hải. 🟢

**Hai vai trò NTN:**
- **Access** — vệ tinh là trạm gốc phục vụ UE trực tiếp (direct-to-device / direct-to-cell). ILCHO thuộc nhóm này.
- **Backhaul** — vệ tinh nối các trạm mặt đất về lõi.

---

## 2. Phân tầng quỹ đạo 🟢🔵

| Loại | Độ cao | Chu kỳ quỹ đạo | Trễ 1 chiều (tới UE) | Đặc điểm |
|------|--------|----------------|----------------------|----------|
| **LEO** | 300–2 000 km | ~90–120 phút | **~1–7 ms** (≈5 ms ở 550 km) 🔵 | Vùng phủ nhỏ, bay nhanh (**7,59 km/s @550 km** 🔵), cần **hàng nghìn** vệ tinh, HO liên tục |
| **MEO** | 2 000 km – < GEO | ~2–12 h | ~27–50 ms | Cân bằng; VD O3b |
| **GEO** | 35 786 km | 24 h (đứng yên so với mặt đất) | **~119–270 ms** 🔵 (RTT ~477–540 ms) | 3 vệ tinh phủ gần toàn cầu; trễ lớn, không hợp thoại/real-time |
| **HEO** | quỹ đạo elip cao | biến thiên | lớn | Phủ vùng vĩ độ cao (Molniya, Tundra) |

🔵 Bài ILCHO: trễ truyền **tối đa** LEO = **12,89 ms**, GEO = **270,73 ms** (trích TR 38.821).
LEO có **link budget tốt hơn** GEO (gần hơn ⇒ ít suy hao) nhưng **thời gian phủ ngắn**.

**Mega-constellation** = chòm sao hàng nghìn–chục nghìn LEO: Starlink, OneWeb, Amazon Kuiper,
Telesat Lightspeed, Guowang (TQ). 🟢

---

## 3. Lộ trình chuẩn hoá 3GPP NTN 🟢

| Release | Năm (freeze) | NTN có gì |
|---------|--------------|-----------|
| **Rel-15** | 2019 | Đặt **mục tiêu & kịch bản** NTN (TR 38.811 – study; TR 38.821 – solutions). Chưa có spec chuẩn. |
| **Rel-16** | 2020 | Nghiên cứu giải pháp NR-NTN (TR 38.821). **CHO** & **DAPS** được chuẩn hoá (cho TN, nhưng CHO chọn làm study item của NTN). |
| **Rel-17** | 2022 | **Spec NR-NTN đầu tiên**: payload **trong suốt (bent-pipe)**, UE power class 3 (≤23 dBm), FDD FR1 (n255/n256/n257), **GNSS bắt buộc** ở UE để pre-compensate **Timing Advance & Doppler**, PRACH mở rộng, mô hình kênh LEO/MEO/GEO. NB-IoT/eMTC over NTN (IoT-NTN). |
| **Rel-18** | 2024 | 5G-Advanced: mở rộng **FR2 (Ku/Ka-band)** cho VSAT trên máy bay/tàu, cải thiện **HO TN↔NTN**, tiết kiệm năng lượng IoT ở vùng phủ gián đoạn, hỗ trợ di động của UE. |
| **Rel-19** | 12/2025 | **Payload tái sinh (regenerative / full gNB on-board)**, **inter-satellite links (ISL)**, **inter-satellite mobility**, **store-and-forward** cho liên lạc trễ-chịu-được, RedCap over NTN, liên lạc UE↔UE dưới 1 vệ tinh không qua mặt đất. |

🔵 **ILCHO giả định payload tái sinh** (`s_m` "equipped with a regenerative payload that can support
base station functions on-board") → mỗi vệ tinh là một gNB thực sự → HO giữa các vệ tinh = HO
inter-gNB. Đây là kịch bản **Rel-19 trở đi**.

**Transparent vs Regenerative payload** 🟢:
- *Transparent (bent-pipe)*: vệ tinh chỉ khuếch đại & dịch tần; gNB nằm ở gateway mặt đất. HO vệ tinh
  ≈ đổi "sóng mang" nhưng cùng gNB.
- *Regenerative*: vệ tinh giải điều chế/xử lý băng gốc, chạy (một phần hoặc toàn bộ) gNB. Cho phép
  ISL, định tuyến trên không, giảm phụ thuộc gateway.

---

## 4. Cơ học quỹ đạo tối thiểu cần cho bài báo 🟢

### 4.1. Sáu phần tử Kepler (Keplerian orbital elements)
Xác định duy nhất một quỹ đạo + vị trí vật thể trên đó:

| Ký hiệu | Tên | Ý nghĩa |
|---------|-----|---------|
| `a` | **semi-major axis** (bán trục lớn) | Kích thước quỹ đạo. `a = R_E + H` cho quỹ đạo tròn. 🔵 `a_s` |
| `e` (ε) | **eccentricity** (độ lệch tâm) | Hình dạng: 0 = tròn, <1 = elip. 🔵 Starlink ε = 0,0001379 ≈ 0 |
| `i` (α) | **inclination** (góc nghiêng) | Góc giữa mặt phẳng quỹ đạo và mặt phẳng xích đạo. 🔵 `α` |
| `Ω` | **RAAN** (right ascension of ascending node) | "Xoay" mặt phẳng quỹ đạo quanh trục Trái Đất; nơi quỹ đạo cắt xích đạo đi lên. 🔵 `Ω_m` |
| `ω` | **argument of perigee** | Góc từ nút lên tới điểm cận địa. 🔵 `w_perigee` |
| `ν` (μ, θ, f) | **true anomaly** | Vị trí góc **tức thời** của vệ tinh trên quỹ đạo (đo từ tâm, từ điểm cận địa). 🔵 `μ^t_m` |

**Ba loại "anomaly"** (đều là góc chỉ vị trí, quy đổi qua nhau):
- **Mean anomaly** `M`: tăng **tuyến tính theo thời gian** (`M = M_0 + n·t`, `n` = mean motion).
- **Eccentric anomaly** `E`: qua **phương trình Kepler** `M = E − e·sin E` (giải lặp).
- **True anomaly** `ν`: góc hình học thật; `cos ν = (cos E − e)/(1 − e·cos E)`.
- Khi `e → 0`: `M ≈ E ≈ ν` (bài ILCHO dùng xấp xỉ này 🔵).

**Mean motion** (tốc độ góc trung bình): `n = sqrt(μ_grav / a³)`, `μ_grav = G·M_E ≈ 3,986·10¹⁴ m³/s²`
(định luật Kepler 3). 🔵 Bài ký hiệu là `ω = sqrt(GM_E/a_s³)`.

**Khoảng cách vệ tinh–tâm Trái Đất:** `r = a(1 − e²)/(1 + e·cos ν)`. 🔵 eq trong chứng minh Lemma 1.

### 4.2. Ephemeris & TLE 🟢
- **Ephemeris**: bộ tham số cho phép tính vị trí + vận tốc vệ tinh tại thời điểm bất kỳ. 3GPP NTN
  truyền ephemeris cho UE qua **SIB19** (System Information Block 19). 🔵 bài dùng "7 giá trị
  ephemeris" (6 Kepler + `t_0e` thời điểm tham chiếu).
- **TLE — Two-Line Element set**: định dạng ephemeris phổ biến của NORAD, dùng với bộ lan truyền
  **SGP4**. 🔵 bài nhắc "leveraging the TLE data (distance and elevation angle)".
- **T430 timer / `ntn-UlSyncValidityDuration`** (TS 38.331): thời hạn UE được coi ephemeris còn hợp
  lệ — **s5 … min20** (5 giây – 20 phút). 🔵 bài dùng để biện minh bỏ qua signaling delay.

### 4.3. Chòm sao Walker 🟢
Cách rải đều N vệ tinh để phủ toàn cầu với số vệ tinh tối thiểu.

- **Walker-Delta** `i : T/P/F`:
  - `i` = góc nghiêng chung mọi mặt phẳng (< 90° → phủ mạnh vĩ độ thấp–trung, yếu ở cực).
  - `T` = tổng số vệ tinh; `P` = số mặt phẳng; `T/P` = vệ tinh mỗi mặt phẳng.
  - `F` = **phasing factor** (0…P−1): độ lệch pha giữa vệ tinh của 2 mặt phẳng kề = `2πF/T`.
  - RAAN các mặt phẳng cách đều `360°/P` **trên toàn 360°** (Delta). 🔵 bài: `ΔΩ = 2π/N_p`.
- **Walker-Star**: RAAN rải trên **180°**, các mặt phẳng gần như cực (`i ≈ 90°`) → phủ tốt vùng cực
  (VD Iridium, OneWeb). Có "seam" (đường nối) nơi 2 mặt phẳng ngược chiều gặp nhau.
- 🔵 ILCHO: `α : N_total/N_p/F`, `ΔΦ = 2π/N_L` trong mặt phẳng, `Δf = 2πF/N_total` giữa mặt phẳng kề.

**Starlink shells** (bài trích FCC — Bảng I): mỗi "shell" là một chòm Walker riêng (độ cao + nghiêng
+ số vệ tinh khác nhau). "Phase 1-a", "Phase 2-a" trong bài = các shell cụ thể.

---

## 5. Mô hình kênh NTN (TR 38.811 / TR 38.821) 🟢🔵

### 5.1. Thành phần suy hao (bài eq 8–11)
```
P_loss = P_loss,b (cơ bản) + P_loss,g (khí quyển/mưa) + P_loss,s (scintillation) + P_loss,e (xuyên tường)
P_loss,b = FSPL(d,f_c) + Shadow Fading + Clutter Loss
FSPL(dB) = 32,45 + 20log₁₀(f_c[GHz]) + 20log₁₀(d[m])
```
- **Shadow fading (SF)** ~ `N(0, σ²)`: dao động chậm do che chắn địa hình/công trình.
- **Clutter loss (CL)**: suy hao do vật cản quanh UE (cây, nhà) khi góc ngẩng thấp.
- SF, CL tra **Bảng 6.6.2 TR 38.811** theo *scenario* (dense urban / urban / suburban / **rural** 🔵)
  và *LoS/NLoS*.
- **Atmospheric**: `P_loss,g = L_zenith(f_c)/sin ψ` — góc ngẩng ψ thấp ⇒ đường truyền qua khí quyển
  dài hơn ⇒ suy hao lớn hơn.
- **Scintillation**: nhấp nháy pha/biên độ do tầng điện ly (vĩ độ thấp/cực) hoặc đối lưu. 🔵 bài đặt
  `= 0` cho vĩ độ ±20°…±60° (khu vực [39–41°] nằm trong khoảng bỏ qua).
- **Building entry loss** `P_loss,e`: 🔵 bỏ qua vì UE ngoài trời, có LoS.

### 5.2. LoS probability
Xác suất có đường nhìn thẳng, phụ thuộc góc ngẩng + scenario (Bảng 6.6.1 TR 38.811). Góc ngẩng cao
⇒ P_LoS cao. 🔵 eq (11) trộn LoS/NLoS.

### 5.3. SNR & throughput
```
γ[dB] = EIRP + G/T − k_B − P_loss − 10log₁₀(BW)      (bài eq 12)
R = BW·log₂(1 + γ)                                   (Shannon, bài eq 13)
```
`G/T` = figure of merit của anten thu; `k_B` = −228,6 dBW/K/Hz.

### 5.4. Doppler shift 🟢
- Vệ tinh LEO tiến/lùi so với UE với vận tốc xuyên tâm lớn ⇒ dịch tần **`f_d = (v_r/c)·f_c`**, có thể
  tới **±480 kHz ở S-band**, hơn **±billion** ở Ka... (thực tế hàng trăm kHz–vài MHz), **thay đổi
  nhanh** khi vệ tinh bay qua đỉnh đầu (Doppler rate).
- Xử lý: **pre-compensation** ở UE (biết ephemeris + vị trí GNSS của mình) + **post-compensation** ở
  mạng; NR cho phép **subcarrier spacing** lớn, cấu hình DMRS dày.
- 🔵 ILCHO **bỏ qua Doppler**, viện dẫn 3GPP + [39–41] rằng bù được. Đây là **giả định đơn giản hoá**
  — xem file 08.

---

## 6. Vì sao HO trong NTN/LEO là bài toán khó & khác biệt 🔵🟢

1. **Nguồn di động đảo ngược**: cell (vệ tinh) bay, UE đứng yên → toàn bộ UE trong một vùng **cùng
   lúc** cần HO khi một vệ tinh khuất → **tương quan cao giữa các UE** → nếu ai cũng chọn "vệ tinh
   tốt nhất" theo một tiêu chí đơn → **nghẽn tập thể** (đây là lý do MD/MVT/LBSH của ILCHO tệ khi
   đông UE).
2. **Nhịp HO rất nhanh** (6–130 s) → cửa sổ quyết định hẹp → cần **chuẩn bị sớm** (CHO).
3. **Đo tín hiệu kém giá trị**: khoảng cách lớn → RSRP các cell na ná nhau, biến thiên khó lường →
   A3-RSRP không phân biệt được cell tốt.
4. **MR dễ lỗi thời**: trễ lan truyền + vệ tinh dịch nhanh → giá trị đo lúc tới gNB đã cũ.
5. **Nhưng có "quà"**: quỹ đạo **tất định** → biết trước cell nào phủ, khi nào, RVT bao lâu → thay
   "đo" bằng "tính". ILCHO khai thác điểm này (Lemma 1, 2).
6. **Nhiều lớp HO**: spot-beam HO (đổi beam trong 1 vệ tinh), satellite HO (đổi vệ tinh — ILCHO),
   ISL HO (đổi liên kết liên vệ tinh), gateway/feeder-link HO.
7. **Tài nguyên on-board hữu hạn**: số kênh/beam/công suất/năng lượng giới hạn → ràng buộc `J` kênh
   mỗi vệ tinh trong ILCHO (eq 15b).

---

## 7. Từ khoá tra cứu thêm
`3GPP NR-NTN Release 17 18 19`, `transparent vs regenerative payload`, `SIB19 ephemeris NTN`,
`Walker-Delta Walker-Star constellation`, `Keplerian elements true mean eccentric anomaly`,
`TR 38.811 channel model`, `TR 38.821 NTN solutions`, `Doppler pre-compensation LEO`,
`spot beam handover vs satellite handover`, `inter-satellite link ISL`.

---

## Nguồn tham khảo (ngoài bài báo)
- 3GPP, *Non-Terrestrial Networks (NTN) overview* — https://www.3gpp.org/technologies/ntn-overview
- Private LTE & 5G, *3GPP NTN: What's Standardized and What's Next* — https://www.privatelteand5g.com/3gpp-ntn-whats-standardized-and-whats-next/
- Ericsson, *5G Non-Terrestrial Networks in 3GPP Rel-19 (payload architecture)* — https://www.ericsson.com/en/blog/2024/10/ntn-payload-architecture
- Ericsson Technology Review, *Promising new 3GPP technology for satellite communication* — https://www.ericsson.com/en/reports-and-papers/ericsson-technology-review/articles/3gpp-satellite-communication
- Hubble, *3GPP Release 17 NTN Explained* — https://hubble.com/community/guides/3gpp-release-17-ntn-explained-what-non-terrestrial-networks-mean-for-iot-devices/
- MathWorks, *walkerDelta – Create Walker-Delta constellation* — https://www.mathworks.com/help/aerotbx/ug/satellitescenario.walkerdelta.html
- MathWorks, *Modeling Satellite Constellations Using Ephemeris Data* — https://www.mathworks.com/help/aerotbx/ug/modeling-satellite-constellations-using-ephemeris-data.html
- AGI/Ansys STK, *Walker (Satellites)* — https://help.agi.com/stk/Subsystems/connectCmds/Content/cmd_WalkerSatellites.htm
- arXiv 2412.00820, *Non-Terrestrial Networking for 6G: Evolution, Opportunities, and Future Directions* — https://arxiv.org/pdf/2412.00820
- arXiv 2407.02184, *Non-Terrestrial Networks for 6G: Integrated, Intelligent and Ubiquitous Connectivity* — https://arxiv.org/pdf/2407.02184
- 3GPP TR 38.811, TR 38.821 (channel models & NTN solutions) — https://www.3gpp.org
