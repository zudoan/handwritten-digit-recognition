# TIẾN ĐỘ THỰC HIỆN SỬA ĐỔI TÍNH ĐÚNG ĐẮN (FINAL_CORRECTNESS_PROGRESS.md)
**Dự án: Nhận dạng chữ số viết tay MNIST — Môn Nhận dạng mẫu — Nhóm 03**

---

## BẢNG TIẾN ĐỘ TỪNG GIAI ĐOẠN (STEP 1 - STEP 8)

| Giai đoạn | Nhiệm vụ chính | Trạng thái | Bằng chứng kiểm chứng |
|---|---|:---:|---|
| **STEP 1: Kiểm tra & Tái hiện lỗi** | Tái hiện lỗi SVM Deskew + PCA không khớp giữa transformer và estimator; phát hiện lệch tập fit PCA (x_train_60k vs x_train_50k). | **DONE** | Log kiểm tra độc lập ghi nhận Accuracy cũ 89.54% do lệch cơ sở biến đổi PCA 112D. |
| **STEP 2: Sửa Pipeline SVM Deskew + PCA** | Refit PCA Deskew 112D trên tập con train 10k chuẩn, đóng gói unified `DeskewTransformer` + pipeline `saved_models/svm_rbf_deskew_pca_pipeline.joblib`. | **DONE** | Đo lại trên 10.000 test set: **97.97% Accuracy**, **97.96% Macro F1**, **203 lỗi / 10k**. Tái lập 100%. |
| **STEP 3: Tối ưu siêu tham số trên Validation** | Viết `src/tune_hyperparameters.py`, chia 50k train / 10k val (Stratified), dò tìm k-NN, Linear SVM, RBF SVM, Random Forest, lưu kết quả. | **DONE** | `results/hyperparameter_search_results.json` & `.csv`. k-NN k=3 distance (95.60%), RBF C=5 (97.09%), RF n=150 (95.07%). Khớp 100% checkpoint. |
| **STEP 4: Sửa Benchmark & Lưu kết quả** | Cập nhật `results/verified_experiments.json`, đồng bộ thời gian train, độ trễ suy luận, số ảnh sai của 10 mô hình thực nghiệm. | **DONE** | Tệp JSON chính thức chứa 12 bản ghi, bao gồm nhóm A, B, C độc lập và công bằng. |
| **STEP 5: Nâng cấp Test Suite** | Bổ sung lớp `TestAuditRegressionAndModelConsistency` vào `tests/test_pipeline.py` (22 tests), kiểm tra reload pipeline, CNN params (160,074), search results. | **DONE** | Chạy `python -m unittest -v tests/test_pipeline.py`: **22/22 PASS (100%)** trong 1.097s. |
| **STEP 6: Web Demo & Browser E2E** | Sửa `app/server.py` (nạp pipeline mới, bỏ fallback, trả HTTP 404), chạy browser automation kiểm thử trực tiếp trên Canvas, mẫu test, chuyển model. | **DONE** | Video ghi lại `mnist_web_demo_test_1792317191430.webp`, 3 ảnh chụp màn hình kiểm thử mẫu 0, 3, 7 và chuyển đổi model SVM Deskew + PCA thành công. |
| **STEP 7: Đồng bộ Báo cáo, Slide & Tài liệu** | Cập nhật kiến trúc CNN (3 conv blocks, 160,074 params), nạp động bảng tuning từ JSON, cập nhật Deskew+PCA 97.97% trên Word, PDF, PPTX, MD. | **DONE** | Render PDF 27 trang qua Word COM (`Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf`), xuất PPTX 10 slides (`Slide_Thuyet_Trinh_Nhom_03.pptx`). |
| **STEP 8: Kiểm tra Git & Nghiệm thu** | Kiểm tra `git status`, `.gitignore`, đảm bảo không commit rác lớn, hoàn thiện hồ sơ bàn giao và báo cáo nghiệm thu. | **DONE** | `FINAL_VERIFICATION_REPORT.md` hoàn thành với bảng nghiệm thu 12 tiêu chí PASS. |
