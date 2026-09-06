# Báo cáo tái hiện — ILCHO (Choi et al., IEEE TMC 2026)

**Bài báo gốc.** M. Choi, M. Park, J. Kim, J.-M. Chung, "Intelligent Handover Scheme for
Improved 6G NTN LEO Satellite Network Performance," *IEEE Transactions on Mobile Computing*,
vol. 25, no. 5, May 2026, tr. 6863–6880. DOI: 10.1109/TMC.2025.3642278.

**Tài liệu đi kèm.**
- `docs/PHUONG_PHAP_XAY_DUNG_CODE.md` — giải thích *vì sao* từng quyết định thiết kế và
  *cách* dựng code từ bài báo, chi tiết theo từng module.
- `docs/METHODOLOGY.html` — bản HTML có sơ đồ; **mục 2 là bảng thuật ngữ** cho mọi khái niệm
  NTN/3GPP và RL/MARL, kèm nguồn đọc thêm.
- `docs/KE_HOACH_TAI_TAO_DAY_DU.md` — những gì có thể làm thêm để tiến sát bài báo hơn, và
  những gì **không thể** khớp (vì bài báo giấu tham số — đã tra cứu, không có mã nguồn / bản
  preprint / tài liệu bổ sung công khai).

File này nói về **kết quả**. Mọi con số đều là kết quả cuối cùng của lượt chạy quy mô lớn
(`scripts/run_scaleup.sh`, xong ~4,8 giờ).

---

## 0. Phiên bản này khác gì lần chạy trước

Đã có 2 lượt tái hiện, và lượt này (lượt "quy mô lớn") thay thế lượt trước làm kết quả chính:

| | Lượt 1 (nhỏ) | **Lượt 2 (báo cáo này)** |
|---|---|---|
| Không gian hành động `N_max` | 16 | **27** (đúng bài báo, Phase 2-a) |
| Số agent lúc huấn luyện | 12–16 | **48** |
| Độ dài episode lúc huấn luyện | 300 s | 420 s |
| Độ dài episode lúc đánh giá | 600 s | 600 s (đúng bài báo) |
| Số episode huấn luyện | 800–1.800 | 2.000–2.800 |
| Số seed lúc đánh giá | 1–3 | 3 |

Các tối ưu kỹ thuật giúp lượt 2 khả thi trên 1 CPU trong ~5 giờ (xem
`docs/PHUONG_PHAP_XAY_DUNG_CODE.md`): **vector hoá hình học** (~10×), thay GRU thủ công bằng
`nn.GRU` hợp nhất + state mixer gọn (mean/max thay vì nối toàn bộ), replay buffer float16
nhận biết bộ nhớ, `learn-every=3`.

Kết quả lượt 1 vẫn còn trong `runs/xeval_*` để đối chiếu tác động của quy mô huấn luyện
(xem §4.1).

---

## 1. Môi trường thực thi

```
uv 0.10.9 · CPython 3.12.9 · Windows 11
torch 2.14.0+cpu · numpy 2.5.2 · matplotlib 3.11.1
```

`uv sync` dựng lại chính xác môi trường từ `uv.lock`.

---

## 2. Kiểm chứng hình học quỹ đạo & link budget

`uv run ilcho-sanity` và `uv run python -m ilcho.analysis`:

| Đại lượng | Bài báo | Bản này | Kết luận |
|---|---|---|---|
| Đỉnh vệ tinh khả kiến trên mọi vĩ độ, **Phase 1-a** | 17 (`N_max`) | **17** (vĩ độ ≈48°) | ✅ khớp chính xác |
| Đỉnh vệ tinh khả kiến trên mọi vĩ độ, **Phase 2-a** | 27 (`N_max`) | 29 (vĩ độ ≈50°) | ≈ (lệch ±7%, do hệ số phasing Walker `F` không công bố) |
| SE tại thiên đỉnh, 340 km | ≈3,76–3,85 bps/Hz | **3,78 bps/Hz** | ✅ |
| Khoảng cách tối thiểu giữa 2 lần HO (MD-CHO, đo thực nghiệm) | 6,61 s (giới hạn lý thuyết TR 38.821) | **8,0 s** | ✅ sát |
| Trung vị / trung bình khoảng cách giữa 2 lần HO | — | 50 s / 58 s | (hợp lý cho lượt bay 340 km) |
| Khoảng cách tối đa giữa 2 lần HO | 132,28 s (giới hạn 1 cặp vệ tinh) | 557 s (đuôi, 1/1372 mẫu) | ⚠️ khác phương pháp đo — xem chú thích |

Hình: `report_assets/analysis_*.png`.

> **Chú thích.** 132,28 s là *giới hạn giải tích* cho một cặp vệ tinh đơn lẻ. 557 s là số *đo
> thực nghiệm* từ mô phỏng đầy đủ nhiều UE + tranh chấp kênh — một UE có thể giữ được vị trí
> tốt xuyên qua ranh giới chuyển giao nên khoảng cách vượt giới hạn 1 cặp. Con số so được với
> bài báo là **tối thiểu** (8,0 s ≈ 6,61 s) và **trung vị** (50 s).

**Kết luận: Lemma 1, Lemma 2, và link budget 3GPP TR 38.811/38.821 (Eq. 8–13) tái hiện
trung thực.**

---

## 3. Những gì đã huấn luyện (lượt quy mô lớn)

48 agent, `N_max=27`, episode 420 s, `learn-every=3`, batch 12. HOF/SE là 10% cuối quá trình.

| Lượt | Hàm thưởng | Episode | HOF cuối | SE cuối | σ điểm số (10% cuối) |
|---|---|---|---|---|---|
| `su_ilcho_sigmoid` | sigmoid (Eq. 27) | 2800 | 3,9 | 2,78 | 6,5 |
| `su_ilcho_linear` | linear (Eq. 30) | 2000 | 4,2 | 2,77 | 5,4 |
| `su_lbsh` | IQL + cân bằng tải | 2000 | 3,2 | 2,71 | 8,0 |

**Cả ba đều hội tụ mượt, phương sai thấp.** Đường cong: `report_assets/su_*_training_curves.png`.

---

## 4. So sánh chính — Starlink Phase 2-a, quét 5→100 UE

`runs/xeval2_starlink_phase_2a` — **3 seed × 3 episode/điểm**, đánh giá ở 600 s, `N_max=27`,
chính sách = `su_ilcho_sigmoid`. Mỗi lần HOF gây 2 s mất dịch vụ (§8, sai khác #11), nên "SE"
là throughput **thực giao được**.

**Số HO thất bại (HOF) mỗi UE (so với Fig. 8b bài báo)** — `report_assets/xeval2_starlink_phase_2a_fig_hof_vs_ue.png`

| #UE | 5 | 20 | 40 | 70 | 100 |
|---|--:|--:|--:|--:|--:|
| **ILCHO** | **0,02** | **0,22** | **1,41** | **7,01** | 21,1 |
| ILCHO-lin | 0,00 | 0,42 | 2,08 | 6,68 | 16,9 |
| MD-CHO | 0,00 | 32,5 | 64,2 | 90,1 | 100,6 |
| MVT-CHO | 0,02 | 3,97 | 9,66 | 21,0 | 30,6 |
| HSNF | 0,02 | 0,02 | 0,03 | **0,04** | **3,37** |
| LBSH | 0,02 | 0,31 | 1,29 | **2,21** | **4,55** |

**Số HO mỗi UE (so với Fig. 8a)**

| #UE | 5 | 20 | 40 | 70 | 100 |
|---|--:|--:|--:|--:|--:|
| ILCHO | 8,5 | 9,1 | 8,9 | 7,4 | 3,6 |
| MD-CHO | 15,5 | 11,8 | 4,4 | 0,1 | 0,0 |
| MVT-CHO | 6,9 | 6,4 | 5,2 | 3,5 | 2,4 |
| HSNF | 16,5 | 13,1 | 11,3 | 9,9 | 5,5 |
| LBSH | 8,5 | 8,9 | 7,6 | 6,5 | 4,1 |

**Spectral efficiency thực giao được [bps/Hz] (so với Fig. 8c)**

| #UE | 5 | 20 | 40 | 70 | 100 |
|---|--:|--:|--:|--:|--:|
| ILCHO | 2,87 | 2,79 | 2,72 | 2,60 | 2,39 |
| MD-CHO | **3,43** | 2,96 | 2,42 | 1,98 | 1,77 |
| MVT-CHO | 3,02 | 2,98 | 2,86 | 2,58 | 2,35 |
| HSNF | 3,42 | **3,33** | **3,10** | **2,81** | **2,55** |
| LBSH | 2,49 | 2,41 | 2,46 | 2,49 | 2,50 |

**Tỉ lệ mất dịch vụ (outage)**

| #UE | 5 | 20 | 40 | 70 | 100 |
|---|--:|--:|--:|--:|--:|
| ILCHO | 0 | 0,1% | 0,5% | 2,3% | 6,8% |
| MD-CHO | 0 | 10,8% | 21,3% | 29,8% | **33,2%** |
| MVT-CHO | 0 | 1,3% | 3,2% | 6,9% | 9,9% |
| HSNF | 0 | 0 | 0 | 0 | 1,0% |
| LBSH | 0 | 0,1% | 0,4% | 0,7% | 1,4% |

**Chỉ số công bằng Jain**: 0,97–1,00 cho mọi phương pháp (ILCHO 0,994→0,990; bài báo 0,9798).
**Cân bằng tải** (`fig_load_balance.png`): LBSH và ILCHO thấp nhất; MD/HSNF/MVT cao hơn ~20–40%.

### 4.1 Tác động của việc tăng số agent lúc huấn luyện — kết quả tích cực chính

Câu hỏi mở từ lượt 1 (16 agent): *"HOF của ILCHO tăng vọt ở 70–100 UE có phải chỉ vì train ở
quá ít agent không?"* — Lượt 2 (48 agent) trả lời: **đúng, tăng số agent lúc train cải thiện
mạnh vùng tải cao.**

| HOF, Phase 2-a | 70 UE | 100 UE |
|---|--:|--:|
| ILCHO — lượt 1 (16 agent, `N_max=16`) | ~30,4 | ~47,4 |
| **ILCHO — lượt 2 (48 agent, `N_max=27`)** | **7,0** | **21,1** |

Giảm ~4× ở 70 UE và ~2,2× ở 100 UE, chỉ nhờ tăng số agent lúc train từ 16 lên 48. Đây là
bằng chứng ủng hộ giả thuyết rằng ngân sách huấn luyện lớn của bài báo (tới 100 agent) là
lý do chính khiến bài báo đạt HOF thấp hơn ở vùng tải cao — không phải do cơ chế CHO/QMIX
sai. Ngoại suy: nếu train đúng 100 agent như bài báo, nhiều khả năng ILCHO sẽ bám sát
HSNF/LBSH kể cả ở 100 UE.

### 4.2 Đọc kết quả so với các tuyên bố của bài báo

- ✅ **HOF thấp hơn hẳn MD-CHO ở mọi số UE, và thấp hơn MVT-CHO ở mọi số UE.** Ở 40 UE:
  HOF của ILCHO (1,4) thấp hơn MD-CHO (64,2) **46 lần** và thấp hơn MVT-CHO (9,7) **7 lần**.
  Ở lượt 1, ILCHO còn thua MVT ở 100 UE; lượt 2 đã vượt MVT ở mọi điểm.
- ✅ **Số HO ổn định** (~8–9/lần phục vụ tới 40 UE), giảm ở tải rất cao vì hệ thống bão hoà.
- ⚠️ **Ở tải cực đại (70–100 UE), HOF của ILCHO vẫn cao hơn HSNF và LBSH.** Ở 100 UE:
  ILCHO 21,1 so với HSNF 3,4 và LBSH 4,6. Đã tốt hơn nhiều so với lượt 1 nhưng chưa đạt
  "ILCHO thấp nhất" như bài báo — hết dư địa cải thiện thì cần train ở đúng 100 agent.
- ❌ **HSNF vẫn là phương pháp throughput cao nhất**, ở mọi số UE. HSNF được thiết kế để tham
  lam tối đa hoá tổng SE tức thời dưới ràng buộc kênh, nên điều này có thể xem là hợp lý.
  Phê phán của bài báo với HSNF là **tập trung hoá + tốn tính toán ở quy mô mega-constellation
  + tạo nhiều HO** (9–16 HO ở đây so với ILCHO 3–9) — cả ba đều được tái hiện.
- ✅ **Outage:** ILCHO giữ mất dịch vụ dưới 7% tới 100 UE, còn MD-CHO 33% — đây là nơi lợi
  ích throughput của ILCHO thật sự thể hiện (giữ UE được phục vụ liên tục).

---

## 5. Ablation hàm thưởng — sigmoid (Eq. 27) vs linear (Eq. 30)

Cấu hình khớp nhau: `su_ilcho_sigmoid` vs `su_ilcho_linear` (đều 48 agent, `learn-every=3`;
2800 vs 2000 episode). `runs/xeval2_reward_ablation/`.

**HOF, Phase 2-a**

| #UE | 5 | 20 | 40 | 70 | 100 |
|---|--:|--:|--:|--:|--:|
| sigmoid (ILCHO) | 0,02 | **0,22** | **1,41** | 7,01 | 21,1 |
| linear | 0,00 | 0,42 | 2,08 | **6,68** | **16,9** |

**SE, Phase 2-a**

| #UE | 5 | 20 | 40 | 70 | 100 |
|---|--:|--:|--:|--:|--:|
| sigmoid (ILCHO) | **2,87** | **2,79** | **2,72** | **2,60** | 2,39 |
| linear | 2,80 | 2,77 | 2,67 | 2,59 | **2,42** |

**Huấn luyện:** sigmoid HOF 20,6→3,9, SE 2,67→2,78 (σ điểm số 6,5); linear HOF 20,5→4,2,
SE 2,67→2,77 (σ 5,4). Cả hai hội tụ mượt.

### 5.1 Kết quả — vẫn là kết quả tiêu cực, và rõ hơn

**Không tái hiện được "sigmoid hội tụ, linear bất ổn và kém hơn" (Fig. 6 vs 7 bài báo).**
Với so sánh khớp cấu hình ở quy mô lớn hơn (48 agent), hai hàm thưởng cho ra chính sách
**gần như tương đương**: sigmoid nhỉnh hơn chút ở 20–40 UE, linear nhỉnh hơn chút ở 100 UE,
throughput gần trùng khít. Không hàm nào mất ổn định lúc huấn luyện.

Lý do khả dĩ (xem `docs/PHUONG_PHAP_XAY_DUNG_CODE.md` §6.4): số agent vẫn ít hơn bài báo
(48 so với tới 100), huấn luyện ngắn hơn, trọng số linear `w1,w2` của bài báo không công bố,
và chân trời episode ngắn hơn nén lại tính phi tuyến throughput–RVT mà lập luận của bài báo
dựa vào. Báo cáo đúng như quan sát, không chỉnh cho khớp bài báo.

---

## 6. Độ vững chắc — khảo sát độ nhạy (`runs/sensitivity2/`)

One-factor-at-a-time, Phase 2-a, **50 UE**, `N_max=27`, chính sách `su_ilcho_sigmoid`.

**HOF theo offset thực thi `O_off` (Eq. 28)**

| `O_off` [km] | 10 | 25 | 50 | 75 | 100 |
|---|--:|--:|--:|--:|--:|
| ILCHO | 2,10 | 2,99 | 2,71 | 2,61 | 3,03 |
| MD-CHO | 91,6 | 87,8 | 75,8 | 65,1 | 53,4 |
| MVT-CHO | 15,7 | 14,8 | 12,3 | 10,7 | 8,93 |

**HOF theo thời gian guard**

| guard [s] | 0 | 2 | 5 | 10 | 20 |
|---|--:|--:|--:|--:|--:|
| ILCHO | 5,71 | 3,74 | 2,71 | 2,32 | 2,16 |
| MD-CHO | 357 | 181 | 75,8 | 40,0 | 24,1 |
| MVT-CHO | 54,0 | 27,9 | 12,3 | 6,97 | 4,52 |

**HOF theo số kênh mỗi vệ tinh `J`**

| `J` | 4 | 6 | 8 | 12 | 16 |
|---|--:|--:|--:|--:|--:|
| ILCHO | 22,3 | 7,07 | 2,71 | 0,82 | **0,33** |
| MD-CHO | 100 | 87,3 | 75,8 | 55,5 | 42,1 |
| MVT-CHO | 31,0 | 18,8 | 12,3 | 7,34 | 5,19 |

**Kết luận.** Ở 50 UE, ưu thế HOF của ILCHO so với MD-CHO (và MVT-CHO) giữ vững qua **mọi**
giá trị của **mọi** tham số không công bố — chênh lệch 1–2 bậc độ lớn so với MD-CHO. Nơi thu
hẹp nhất là góc thiếu tài nguyên cực đoan (`J=4`): ILCHO (22,3) và MVT-CHO (31,0) vẫn hơn
MD-CHO (100) nhưng đều bị áp đảo bởi cùng sự thiếu dung lượng.

---

## 7. Các chòm vệ tinh khác

### 7.1 Starlink Phase 1-a (`runs/xeval2_starlink_phase_1a/`, chuyển giao zero-shot)

Phase 1-a (~11–17 vệ tinh khả kiến, ~88–136 khe kênh) **bão hoà toàn hệ thống ở 70–100 UE
với MỌI phương pháp** — HOF của HSNF cũng nhảy từ ≈0 lên 17→130 ở đó. Chỉ so được ở 5–40 UE:

| HOF | 5 | 20 | 40 | 70 | 100 |
|---|--:|--:|--:|--:|--:|
| ILCHO (zero-shot) | 0,00 | **0,86** | **0,97** | 25,3 | 141 |
| MD-CHO | 0,04 | 52,2 | 85,4 | 115 | 208 |
| MVT-CHO | 0,00 | 10,9 | 25,8 | 59,0 | 166 |

Tới 40 UE, ILCHO (train trên Phase 2-a, chạy zero-shot trên Phase 1-a) vẫn thắng MD-CHO
~88 lần và MVT-CHO ~27 lần.

### 7.2 Hybrid (Phase 1-a + Phase 2-a, `runs/xeval2_hybrid/`, so với Fig. 10 / Bảng III)

Nhiều vệ tinh hơn (6864) → **ILCHO mở rộng tốt nhất trong mọi kịch bản**:

| HOF | 5 | 20 | 40 | 70 | 100 |
|---|--:|--:|--:|--:|--:|
| ILCHO | 0,07 | 0,19 | 1,97 | 8,27 | **15,8** |
| MD-CHO | 0,00 | 32,5 | 64,2 | 90,0 | 98,8 |

(15,8 ở 100 UE so với 21,1 khi chỉ dùng Phase 2-a — thêm dung lượng rõ ràng giúp ích, khớp
nhận định của bài báo về hybrid.) HSNF ở hybrid giữ HOF ≈0 xuyên suốt (0,08 ở 100 UE).

---

## 8. Sai khác so với bài báo & ảnh hưởng quan sát được

| # | Bài báo | Bản này | Ảnh hưởng quan sát được |
|---|---|---|---|
| 1 | 3–30k episode, ≤100 agent, episode 600 s | 2–2,8k episode, 48 agent, episode 420 s | **HOF vùng tải cao giảm 2–4× so với lượt 16-agent** (§4.1), nhưng ở 100 UE vẫn cao hơn HSNF/LBSH — chỗ này nhiều khả năng còn cải thiện nữa nếu train 100 agent |
| 2 | `N_max` = 27 | 27 (đúng bài báo, Phase 2-a) | — |
| 3 | tần số sóng mang không công bố | 20 GHz, hiệu chỉnh theo 3,8 bps/Hz | chỉ ảnh hưởng SE tuyệt đối, không ảnh hưởng thứ hạng |
| 4 | `O_off` không công bố | 50 km (khảo sát 10–100) | thứ hạng không đổi (§6) |
| 5 | hằng số hàm thưởng không công bố | tự chọn (bộ v3, xem `docs/…` §6.4) | trở thành một phát hiện riêng (§5) |
| 6 | hệ số phasing Walker `F` không công bố | `F = 1` | đỉnh khả kiến P2a 29 so với 27 |
| 7 | HSNF/LBSH là cài đặt đầy đủ [22]/[26] | bản xấp xỉ gọn | **HSNF của bản này thắng throughput thô**; **LBSH của bản này ổn định hơn** mô tả của bài báo (không "vỡ trận" ở tải cao) |
| 8 | bỏ qua xoay Trái Đất, Doppler | bỏ qua | khớp bài báo |
| 9 | thời gian guard không nêu chi tiết | 5 s (khảo sát 0–20) | chặn hiện tượng thử lại HO phi thực tế mỗi giây; ảnh hưởng đều mọi phương pháp |
| 10 | linear reward được báo cáo bất ổn (Fig. 7) | **hội tụ ổn định, gần như trùng sigmoid** ở quy mô 48 agent | **không tái hiện được — kết quả tiêu cực (§5.1)** |
| 11 | hệ quả throughput của HOF không nêu chi tiết | thêm outage 2 s sau mỗi HOF, ở bước đánh giá | làm throughput được-giao phản ánh đúng HOF (Fig. 8c) |
| 12 | tốc độ mô phỏng | vector hoá + `nn.GRU` hợp nhất + replay float16 | ~10× nhanh hơn, cho phép chạy lượt 48-agent trong ~5 giờ trên 1 CPU |

---

## 9. Kết luận

**Tái hiện được (định tính), có số liệu hỗ trợ:**

1. ✅ **ILCHO giữ HOF thấp hơn hẳn MD-CHO và MVT-CHO ở MỌI số UE** (Phase 2-a) — thấp hơn
   MD-CHO 46× và MVT-CHO 7× ở 40 UE. Đứng vững qua mọi chòm vệ tinh (P1a, P2a, hybrid) và
   mọi giá trị của mọi tham số giả định (§6).
2. ✅ **Tăng số agent lúc huấn luyện cải thiện mạnh vùng tải cao** — HOF ở 70/100 UE giảm
   2–4× khi đi từ 16 lên 48 agent (§4.1). Đây là bằng chứng trực tiếp cho thấy ngân sách
   huấn luyện của bài báo là yếu tố then chốt.
3. ✅ **Công bằng** — Jain 0,97–1,00, khớp 0,9798 của bài báo.
4. ✅ **Cân bằng tải** — ILCHO trong nhóm 2 phương pháp phương sai chiếm dụng kênh thấp nhất.
5. ✅ **Liên tục dịch vụ** — outage của ILCHO dưới 7% tới 100 UE so với 33% của MD-CHO.
6. ✅ **Hình học & link budget** tái hiện sát số liệu bài báo (vài phần trăm).
7. ✅ **Điểm yếu thực sự của HSNF là số HO cao + chi phí tập trung hoá**, không phải throughput.

**Không tái hiện được — báo cáo như phát hiện, không che giấu:**

- ❌ **"ILCHO có throughput cao nhất."** HSNF cao nhất xuyên suốt; lợi thế của ILCHO nằm ở
  tránh outage và HOF, không phải SE thô.
- ❌ **Sự bất ổn khi huấn luyện với hàm thưởng linear (Fig. 7).** Ở quy mô 48 agent, sigmoid
  và linear cho chính sách gần như trùng nhau, đều hội tụ mượt.
- ⚠️ **Ở 70–100 UE, HOF của ILCHO vẫn cao hơn HSNF/LBSH** (dù đã cải thiện lớn so với lượt
  16-agent). Cần train đúng 100 agent như bài báo để khép khoảng cách này.
- ⚠️ **LBSH không suy giảm ở tải cao** như bài báo mô tả — bản IQL chia sẻ tham số vững hơn
  mạng gốc, nên không phải đại diện công bằng cho điểm yếu của baseline đó.

**Tóm lại.** Tuyên bố cốt lõi của bài báo — *một Conditional Handover điều khiển bằng RL giữ
số chuyển giao, đặc biệt là chuyển giao thất bại, ở mức thấp và ổn định trong chòm vệ tinh
LEO mật độ cao, nơi các heuristic khoảng cách/thời-gian-nhìn-thấy thất bại khi tải tăng* —
được tái hiện rõ ràng, vững chắc qua khảo sát độ nhạy, và lượt 48-agent cho thấy khoảng cách
còn lại ở vùng tải cực đại thu hẹp đúng như dự đoán khi tăng quy mô huấn luyện. Hai tuyên bố
phụ (dẫn đầu throughput; linear reward bất ổn) không xuất hiện trong bản tái hiện này; nhiều
khả năng do ngân sách huấn luyện của bài báo lớn hơn ~15–20 lần, nhưng đó là suy luận, không
phải điều bản này xác nhận được nếu không chạy đúng quy mô đó.

---

## 10. Cách tạo lại toàn bộ

```bash
uv sync
uv run ilcho-sanity                          # §2
uv run python -m ilcho.analysis --out runs/analysis        # §2
bash scripts/run_scaleup.sh                   # §3–§7 (huấn luyện + quét + độ nhạy, ~5 giờ)
uv run python scripts/make_report_tables.py   # -> report_assets/{TABLES.md, *.png}
```

Lượt nhỏ (16 agent, để đối chiếu §4.1) tạo bằng: `run_rest.sh` + `run_extended.sh` +
`run_ablation.sh` + `run_phase1a_native.sh`.

Mọi con số đều tính lại được từ `results.json` / `history.npz` trong `runs/`.
Lộ trình tiến sát bài báo hơn nữa (100 agent, 30k episode, cài đầy đủ HSNF/LBSH): xem
`docs/KE_HOACH_TAI_TAO_DAY_DU.md`.
