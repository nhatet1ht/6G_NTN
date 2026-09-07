# Phân tích bài báo: ILCHO — Intelligent Handover Scheme for 6G NTN LEO Satellite Networks

## 1. Thông tin chung
- **Tên bài:** Intelligent Handover Scheme for Improved 6G NTN LEO Satellite Network Performance
- **Tác giả:** Minsu Choi, Minseung Park, Junwon Kim, Jong-Moon Chung (Yonsei University, Hàn Quốc)
- **Nguồn:** IEEE Transactions on Mobile Computing, Vol. 25, No. 5, May 2026

## 2. Vấn đề & động lực nghiên cứu
- 6G NTN dùng vệ tinh LEO (300–2000 km) để phủ sóng toàn cầu, độ trễ thấp hơn MEO/GEO nhưng do di chuyển rất nhanh (~7.59 km/s) và vùng phủ nhỏ nên **handover (HO) xảy ra liên tục** (mỗi 6.61–132.28 s).
- Các thuật toán HO truyền thống của mạng mặt đất (dựa trên đo RSRP/RSSI theo sự kiện A3) **không phù hợp với NTN** vì tín hiệu giữa các cell vệ tinh dao động và không ổn định (do khoảng cách xa, cell chồng lấn).
- 3GPP đề xuất **Conditional Handover (CHO)** ở Release 16 để giảm HO Failure (HOF) bằng cách quyết định sớm hơn (preparation event tách khỏi execution event), nhưng **chưa có nghiên cứu nào validate CHO bằng RL trong một mega-constellation LEO thực tế** (Starlink, OneWeb) — đây là khoảng trống mà bài báo lấp vào.

## 3. Đóng góp chính
1. **Nền tảng giải tích (3 Lemma):**
   - *Lemma 1:* công thức xác định vị trí (tọa độ Cartesian) của vệ tinh LEO tại thời điểm t dựa trên tham số quỹ đạo Walker-Delta (ephemeris).
   - *Lemma 2:* điều kiện để một vệ tinh LEO "accessible" (nằm trong vùng phủ) đối với một UE, dựa trên góc elevation ψ_min.
   - *Lemma 3:* chứng minh bài toán tối ưu chọn target-LEO là **NP-hard** (dạng generalized assignment problem theo thời gian) → cần một phương pháp học (RL) thay vì tối ưu chính xác.
2. **Mô hình constellation thực tế:** dùng thông số triển khai/dự kiến triển khai thật của Starlink Phase 1-a, Phase 2-a, OneWeb (Bảng I) thay vì mô hình < 100 vệ tinh giả định như các bài trước.
3. **MARL có khả năng scale:** action space được giới hạn bằng N_max (số vệ tinh accessible tối đa, suy ra từ Lemma 2) thay vì bằng toàn bộ chỉ số vệ tinh trong constellation → tránh bùng nổ không gian hành động khi số vệ tinh tăng lên hàng nghìn.
4. Đề xuất **ILCHO** = CHO + MARL (QMIX), là bài đầu tiên validate RL-based CHO trên mega-constellation LEO.

## 4. Phương pháp

### 4.1 Mô hình hệ thống
- M vệ tinh LEO, K UE (VSAT cố định — **giả định UE không di chuyển**, vì tốc độ vệ tinh vượt trội hẳn tốc độ UE).
- Path loss theo 3GPP TR 38.811/38.821 (free-space loss + shadow fading + clutter loss + atmospheric attenuation), **bỏ qua Doppler shift** (giả định đã được bù ở lớp vật lý).
- Bài toán tối ưu (P): tối đa hóa tổng throughput toàn mạng R_NTN, ràng buộc mỗi UE chỉ nối 1 vệ tinh tại 1 thời điểm và mỗi vệ tinh phục vụ tối đa J kênh → NP-hard (Lemma 3).

### 4.2 Quy trình CHO (3 pha)
- **Preparation:** UE gửi Measurement Report → bộ điều khiển trung tâm (near-RT RIC) dùng **ILCHO/QMIX** để chọn target-LEO tối ưu cho từng UE dựa trên state (vị trí, khoảng cách, số kênh đang dùng, RVT — remaining visible time).
- **Execution:** Kích hoạt bằng **sự kiện dựa trên khoảng cách** (distance-based event, công thức 28: d_target < d_serving − offset), thay vì đo RSRP như A3 truyền thống.
- **Completion:** chuyển bearer, giải phóng context ở S-LEO (giống BHO chuẩn).

### 4.3 MARL / QMIX
- Mỗi UE = 1 agent, quan sát cục bộ (partially observable), huấn luyện **CTDE** (centralized training, decentralized execution).
- Action: chọn 1 trong N_max vệ tinh accessible.
- **Reward dạng sigmoid** (công thức 27) cân bằng giữa throughput và RVT (không phải hàm tuyến tính) — đây là một đóng góp kỹ thuật quan trọng: bài báo **chứng minh bằng thực nghiệm** rằng reward tuyến tính (công thức 30) không hội tụ ổn định vì mối quan hệ throughput–RVT là phi tuyến (throughput tăng rồi giảm, RVT giảm đơn điệu).
- So sánh với 4 baseline: MD-CHO (chọn khoảng cách gần nhất), MVT-CHO (chọn thời gian nhìn thấy dài nhất), HSNF (network-flow based), LBSH (multi-agent Q-learning + load balancing).

## 5. Kết quả chính
- ILCHO **giảm mạnh số lần HO và HOF**, giữ ổn định khi số UE tăng (5→100 UE): ví dụ ở Starlink Phase 2-a, HOF chỉ 0.48/service duration với 50 UE và 1.38 với 100 UE (so với LBSH có thể >20).
- **Throughput cao hơn** tất cả baseline (~3.76–3.85 bps/Hz tùy số UE).
- **Fairness tốt:** Jain's Fairness Index = 0.9798 (gần 1.0 — phân bổ tài nguyên công bằng).
- **Load balancing tốt hơn:** phương sai channel occupancy thấp nhất trong các phương pháp so sánh (0.072 so với 0.372–0.400 của MD/MVT).
- Kết quả nhất quán trên cả Phase 1-a, Phase 2-a, và hybrid constellation.

## 6. Nhận xét — điểm mạnh & hạn chế

**Điểm mạnh:**
- Cơ sở toán học chặt chẽ (3 Lemma), mô hình hóa dựa trên tham số constellation thương mại thật.
- So sánh công bằng, nhiều baseline, nhiều kịch bản constellation.
- Reward function được thiết kế có lý do vật lý rõ ràng (không phải chọn tùy tiện), có thực nghiệm ablation (sigmoid vs linear).

**Hạn chế / khoảng trống — hướng tiềm năng cho luận văn:**
1. **Đây không phải mô hình "dự đoán" (prediction) theo nghĩa ML cổ điển.** Vị trí vệ tinh là **hoàn toàn xác định** (deterministic, tính từ ephemeris/Kepler orbit — Lemma 1), nên "trí tuệ" ở đây nằm ở **quyết định tối ưu** (RL action selection), không phải ở việc dự đoán một đại lượng bất định trong tương lai (VD: dự đoán RSRP, dự đoán thời điểm suy giảm liên kết, dự đoán trước khi đo được). Nếu đề tài của bạn là "dự đoán Handover bằng AI", đây là điểm mấu chốt cần làm rõ với cô — ILCHO tối ưu hóa lựa chọn target dựa trên thông tin đã biết trước (ephemeris), chứ **không dự đoán điều kiện kênh bất định** (fading, nghẽn tải tương lai, hành vi UE...).
2. UE được giả định **đứng yên (fixed VSAT)** — không có UE mobility, nên chưa phản ánh trường hợp handheld/IoT di động.
3. **Doppler shift bị bỏ qua**, chỉ giả định đã bù ở lớp vật lý — đơn giản hóa so với thực tế.
4. Thời gian huấn luyện QMIX khá lớn (3.000–30.000 episodes) — chưa phân tích rõ độ khả thi triển khai real-time/online learning trên near-RT RIC thực tế.
5. Chưa xét đa kết nối (multi-connectivity) hay dự đoán tải tương lai của các vệ tinh lân cận.

## 7. Việc cần làm để chuẩn bị báo cáo với cô
1. Viết một bản tóm tắt ngắn (1 trang) theo cấu trúc: Vấn đề → Phương pháp (CHO + MARL/QMIX) → Kết quả → Nhận xét cá nhân (mục 6).
2. Chuẩn bị sẵn phần **"khoảng trống nghiên cứu"** — vì đây thường là phần cô quan tâm nhất để định hướng luận văn.
3. Chuẩn bị các câu hỏi cụ thể để hỏi lại cô (danh sách bên dưới) thay vì tự đoán.

## 8. Câu hỏi nên hỏi lại cô
- Đề tài của em là "dự đoán Handover" — cô muốn em đi theo hướng: (a) xây mô hình **dự đoán** một đại lượng (VD: thời điểm HO, RSRP tương lai, xác suất HOF) để **bổ sung/thay thế** phần ra quyết định CHO trong ILCHO, hay (b) tái hiện/mở rộng chính cơ chế RL-based selection như bài này?
- Em có cần **cài đặt lại (reproduce)** mô phỏng ILCHO (Python/PyTorch, QMIX) để làm baseline so sánh không, hay chỉ cần đọc hiểu và viết review?
- Nếu hướng đi là dự đoán: cô có định hướng cụ thể về input/output của mô hình dự đoán không (VD: dự đoán RVT, dự đoán suy giảm SNR trước N bước thời gian)?
- Deadline nộp báo cáo phân tích này là khi nào, và cô muốn độ sâu ở mức tổng quan hay phản biện kỹ thuật chi tiết (toán học, thực nghiệm)?
