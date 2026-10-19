/**
 * MNIST Handwritten Digit Recognition - Frontend Application Logic
 * Nhóm 03 - Môn Nhận dạng mẫu
 * Art Direction: Premium Soft Glass + Editorial Minimalism + Interactive Creative Workspace
 */

document.addEventListener("DOMContentLoaded", () => {
    // Canvas & Workspace Elements
    const canvas = document.getElementById("digitCanvas");
    const ctx = canvas.getContext("2d", { willReadFrequently: true });
    const canvasHint = document.getElementById("canvasHint");
    const brushSizeSlider = document.getElementById("brushSize");
    const strokePresetBtns = document.querySelectorAll(".stroke-preset-btn");
    const btnClear = document.getElementById("btnClear");
    const btnPredict = document.getElementById("btnPredict");
    const imageUpload = document.getElementById("imageUpload");
    const samplesPalette = document.getElementById("samplesPalette");
    const modelSelect = document.getElementById("modelSelect");

    // Model Metadata Elements
    const modelFeatureVal = document.getElementById("modelFeatureVal");
    const modelTrainVal = document.getElementById("modelTrainVal");
    const modelAccVal = document.getElementById("modelAccVal");
    const modelTypeTag = document.getElementById("modelTypeTag");

    // Results Elements
    const predictedDigitEl = document.getElementById("predictedDigit");
    const confidenceBadgeEl = document.getElementById("confidenceBadge");
    const prepImgEl = document.getElementById("prepImg");
    const latencyDisplayEl = document.getElementById("latencyDisplay");
    const probBarsContainer = document.getElementById("probBarsContainer");

    // Benchmark Navigation
    const btnToggleBenchmark = document.getElementById("btnToggleBenchmark");
    const benchmarkDrawer = document.getElementById("benchmarkDrawer");

    // State
    let isDrawing = false;
    let hasDrawn = false;
    let lastX = 0;
    let lastY = 0;
    let strokeTimer = null;
    let modelsRegistry = {};

    // 1. Initialize Canvas Background
    function initCanvas() {
        ctx.fillStyle = "#000000";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.lineCap = "round";
        ctx.lineJoin = "round";
        ctx.strokeStyle = "#ffffff";
        ctx.lineWidth = parseInt(brushSizeSlider ? brushSizeSlider.value : 20, 10);
        hasDrawn = false;
        if (canvasHint) {
            canvasHint.style.opacity = "1";
            canvasHint.style.pointerEvents = "none";
        }
    }

    initCanvas();

    // 2. Stroke Preset Buttons & Slider Synchronization
    function setActivePreset(size) {
        strokePresetBtns.forEach(btn => {
            const btnSize = parseInt(btn.getAttribute("data-size"), 10);
            if (btnSize === size) {
                btn.classList.add("active");
            } else {
                btn.classList.remove("active");
            }
        });
    }

    strokePresetBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            const size = parseInt(btn.getAttribute("data-size"), 10);
            if (brushSizeSlider) brushSizeSlider.value = size;
            ctx.lineWidth = size;
            setActivePreset(size);
        });
    });

    if (brushSizeSlider) {
        brushSizeSlider.addEventListener("input", (e) => {
            const size = parseInt(e.target.value, 10);
            ctx.lineWidth = size;
            setActivePreset(size);
        });
    }

    // 3. Initialize Empty Probability Bars
    function initProbBars() {
        if (!probBarsContainer) return;
        probBarsContainer.innerHTML = "";
        for (let i = 0; i < 10; i++) {
            const row = document.createElement("div");
            row.className = "prob-row";
            row.id = `prob-row-${i}`;
            row.innerHTML = `
                <div class="prob-digit-num">${i}</div>
                <div class="prob-track">
                    <div class="prob-fill" id="prob-fill-${i}"></div>
                </div>
                <div class="prob-pct-val" id="prob-val-${i}">0.0%</div>
            `;
            probBarsContainer.appendChild(row);
        }
    }

    initProbBars();

    // 4. Drawing Coordinates Helper
    function getCanvasCoordinates(e) {
        const rect = canvas.getBoundingClientRect();
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const clientY = e.touches ? e.touches[0].clientY : e.clientY;
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        return {
            x: (clientX - rect.left) * scaleX,
            y: (clientY - rect.top) * scaleY,
        };
    }

    // 5. Drawing Event Handlers
    function startDrawing(e) {
        e.preventDefault();
        isDrawing = true;
        const pos = getCanvasCoordinates(e);
        lastX = pos.x;
        lastY = pos.y;
        hasDrawn = true;
        if (canvasHint) canvasHint.style.opacity = "0";

        // Dot for single tap/click
        ctx.beginPath();
        ctx.arc(lastX, lastY, ctx.lineWidth / 2, 0, Math.PI * 2);
        ctx.fillStyle = "#ffffff";
        ctx.fill();
    }

    function draw(e) {
        if (!isDrawing) return;
        e.preventDefault();
        const pos = getCanvasCoordinates(e);

        ctx.beginPath();
        ctx.moveTo(lastX, lastY);
        ctx.lineTo(pos.x, pos.y);
        ctx.stroke();

        lastX = pos.x;
        lastY = pos.y;
    }

    function stopDrawing() {
        if (!isDrawing) return;
        isDrawing = false;

        // Auto predict with smooth debounce
        clearTimeout(strokeTimer);
        strokeTimer = setTimeout(() => {
            if (hasDrawn) {
                predictCurrentDigit();
            }
        }, 280);
    }

    // Attach listeners with passive: false for touch precision
    canvas.addEventListener("mousedown", startDrawing);
    canvas.addEventListener("mousemove", draw);
    window.addEventListener("mouseup", stopDrawing);

    canvas.addEventListener("touchstart", startDrawing, { passive: false });
    canvas.addEventListener("touchmove", draw, { passive: false });
    window.addEventListener("touchend", stopDrawing);

    // 6. Clear Canvas Action
    btnClear.addEventListener("click", () => {
        // Subtle ripple feedback
        canvas.style.transform = "scale(0.995)";
        setTimeout(() => { canvas.style.transform = "scale(1)"; }, 120);
        initCanvas();
        resetResults();
    });

    // 7. Predict Action
    btnPredict.addEventListener("click", () => {
        if (!hasDrawn) {
            // Visual subtle alert
            if (canvasHint) {
                canvasHint.style.color = "var(--color-error)";
                canvasHint.textContent = "Vui lòng vẽ chữ số lên bảng trước";
                setTimeout(() => {
                    canvasHint.style.color = "";
                    canvasHint.textContent = "Vẽ chữ số 0 – 9 tại đây";
                }, 2000);
            }
            return;
        }
        predictCurrentDigit();
    });

    // 8. Model Selection Handler
    modelSelect.addEventListener("change", () => {
        const selectedId = modelSelect.value;
        updateModelMetaDisplay(selectedId);
        if (hasDrawn) {
            predictCurrentDigit();
        }
    });

    function updateModelMetaDisplay(modelId) {
        const meta = modelsRegistry[modelId];
        if (!meta) return;

        if (modelFeatureVal) modelFeatureVal.textContent = meta.feature || "Trực tiếp 28×28";
        if (modelTrainVal) modelTrainVal.textContent = meta.train_samples ? `${meta.train_samples} mẫu` : "60,000";
        if (modelAccVal) modelAccVal.textContent = meta.accuracy || "--%";
        if (modelTypeTag) {
            if (meta.is_official) {
                modelTypeTag.textContent = "VERIFIED BENCHMARK";
                modelTypeTag.style.background = "var(--color-accent-subtle)";
                modelTypeTag.style.color = "var(--color-accent)";
            } else {
                modelTypeTag.textContent = "LEGACY COMPARISON";
                modelTypeTag.style.background = "rgba(100, 116, 139, 0.12)";
                modelTypeTag.style.color = "var(--color-text-muted)";
            }
        }
    }

    // 9. Reset Results Display
    function resetResults() {
        predictedDigitEl.textContent = "-";
        predictedDigitEl.classList.remove("updated");
        confidenceBadgeEl.textContent = "Độ tin cậy: --%";
        confidenceBadgeEl.style.color = "var(--color-text-muted)";
        confidenceBadgeEl.style.borderColor = "var(--color-border-glass)";
        latencyDisplayEl.textContent = "Độ trễ: 0 ms";
        prepImgEl.src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=";

        for (let i = 0; i < 10; i++) {
            const row = document.getElementById(`prob-row-${i}`);
            const fill = document.getElementById(`prob-fill-${i}`);
            const val = document.getElementById(`prob-val-${i}`);
            if (row) row.classList.remove("winner");
            if (fill) {
                fill.style.width = "0%";
                fill.classList.remove("winner");
            }
            if (val) val.textContent = "0.0%";
        }
    }

    // 10. Predict via Backend API
    async function predictCurrentDigit() {
        const dataUrl = canvas.toDataURL("image/png");
        const modelName = modelSelect.value;

        // Subtle loading indicator on predict button
        btnPredict.disabled = true;
        btnPredict.style.opacity = "0.85";

        try {
            const res = await fetch("/api/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    image_base64: dataUrl,
                    model_name: modelName,
                }),
            });

            if (!res.ok) {
                throw new Error(`Server returned ${res.status}`);
            }

            const data = await res.json();
            displayResults(data);
        } catch (err) {
            console.error("Lỗi dự đoán:", err);
            confidenceBadgeEl.textContent = "Lỗi kết nối API";
            confidenceBadgeEl.style.color = "var(--color-error)";
        } finally {
            btnPredict.disabled = false;
            btnPredict.style.opacity = "1";
        }
    }

    // 11. Display Prediction Result
    function displayResults(data) {
        const { predicted_digit, confidence, confidence_type, is_calibrated, probabilities, latency_ms, processed_image, message, model_used } = data;

        if (predicted_digit === -1) {
            predictedDigitEl.textContent = "-";
            predictedDigitEl.classList.remove("updated");
            confidenceBadgeEl.textContent = message || "Bảng vẽ trống";
            confidenceBadgeEl.style.color = "var(--color-error)";
            confidenceBadgeEl.style.borderColor = "rgba(180, 83, 9, 0.3)";
            latencyDisplayEl.textContent = `Độ trễ: ${latency_ms} ms`;
            if (processed_image) prepImgEl.src = processed_image;
            resetProbBars();
            return;
        }

        // Animate digit transition
        predictedDigitEl.textContent = predicted_digit;
        predictedDigitEl.classList.remove("updated");
        void predictedDigitEl.offsetWidth; // Force reflow
        predictedDigitEl.classList.add("updated");

        const pct = (confidence * 100).toFixed(1);
        const scoreType = confidence_type ? `${confidence_type}` : "Độ tin cậy";
        const calTag = is_calibrated ? " (Calibrated)" : " (Chưa hiệu chuẩn)";
        confidenceBadgeEl.textContent = `${scoreType}: ${pct}%${calTag}`;
        confidenceBadgeEl.title = `Loại độ đo: ${confidence_type}. Trạng thái: ${is_calibrated ? 'Đã hiệu chuẩn' : 'Chưa hiệu chuẩn'}. Mô hình: ${model_used}`;

        if (confidence > 0.8) {
            confidenceBadgeEl.style.color = "var(--color-success)";
            confidenceBadgeEl.style.borderColor = "rgba(45, 106, 79, 0.35)";
        } else if (confidence > 0.5) {
            confidenceBadgeEl.style.color = "var(--color-warning)";
            confidenceBadgeEl.style.borderColor = "rgba(180, 83, 9, 0.35)";
        } else {
            confidenceBadgeEl.style.color = "var(--color-error)";
            confidenceBadgeEl.style.borderColor = "rgba(185, 28, 28, 0.35)";
        }

        latencyDisplayEl.textContent = `Độ trễ: ${latency_ms} ms`;
        if (processed_image) {
            prepImgEl.src = processed_image;
        }

        // Update probability horizontal bars
        probabilities.forEach((p, idx) => {
            const row = document.getElementById(`prob-row-${idx}`);
            const fill = document.getElementById(`prob-fill-${idx}`);
            const val = document.getElementById(`prob-val-${idx}`);

            const barPct = (p * 100).toFixed(1);
            if (val) val.textContent = `${barPct}%`;
            if (fill) fill.style.width = `${Math.min(100, Math.max(0, barPct))}%`;

            if (idx === predicted_digit) {
                if (row) row.classList.add("winner");
                if (fill) fill.classList.add("winner");
            } else {
                if (row) row.classList.remove("winner");
                if (fill) fill.classList.remove("winner");
            }
        });
    }

    function resetProbBars() {
        for (let i = 0; i < 10; i++) {
            const row = document.getElementById(`prob-row-${i}`);
            const fill = document.getElementById(`prob-fill-${i}`);
            const val = document.getElementById(`prob-val-${i}`);
            if (row) row.classList.remove("winner");
            if (fill) {
                fill.style.width = "0%";
                fill.classList.remove("winner");
            }
            if (val) val.textContent = "0.0%";
        }
    }

    // 12. Load MNIST Test Samples
    async function loadTestSamples() {
        try {
            const res = await fetch("/api/samples");
            if (!res.ok) return;
            const data = await res.json();
            if (!data.samples || data.samples.length === 0) return;

            samplesPalette.innerHTML = "";
            data.samples.forEach((sample) => {
                const tile = document.createElement("button");
                tile.type = "button";
                tile.className = "sample-tile";
                tile.title = `Chữ số mẫu chuẩn NIST: ${sample.digit}`;
                tile.setAttribute("aria-label", `Chữ số mẫu ${sample.digit}`);
                tile.innerHTML = `
                    <img src="${sample.image_base64}" alt="Mẫu ${sample.digit}">
                    <span class="sample-tile-badge">${sample.digit}</span>
                `;

                tile.addEventListener("click", () => {
                    loadSampleIntoCanvas(sample.image_base64);
                });

                samplesPalette.appendChild(tile);
            });
        } catch (err) {
            console.warn("Không thể nạp samples:", err);
        }
    }

    function loadSampleIntoCanvas(b64) {
        const img = new Image();
        img.onload = () => {
            ctx.fillStyle = "#000000";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            // Draw scaled to canvas
            ctx.imageSmoothingEnabled = false;
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            hasDrawn = true;
            if (canvasHint) canvasHint.style.opacity = "0";
            predictCurrentDigit();
        };
        img.src = b64;
    }

    // 13. Image Upload Support
    if (imageUpload) {
        imageUpload.addEventListener("change", (e) => {
            const file = e.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = (event) => {
                const img = new Image();
                img.onload = () => {
                    ctx.fillStyle = "#000000";
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    
                    // Maintain aspect ratio inside canvas
                    const hRatio = canvas.width / img.width;
                    const vRatio = canvas.height / img.height;
                    const ratio = Math.min(hRatio, vRatio) * 0.8;
                    const centerShiftX = (canvas.width - img.width * ratio) / 2;
                    const centerShiftY = (canvas.height - img.height * ratio) / 2;
                    
                    ctx.drawImage(img, 0, 0, img.width, img.height,
                                      centerShiftX, centerShiftY, img.width * ratio, img.height * ratio);
                    hasDrawn = true;
                    if (canvasHint) canvasHint.style.opacity = "0";
                    predictCurrentDigit();
                };
                img.src = event.target.result;
            };
            reader.readAsDataURL(file);
        });
    }

    // 14. Dynamically Load Models & Metadata
    async function loadAvailableModels() {
        try {
            const res = await fetch("/api/models");
            if (!res.ok) return;
            const data = await res.json();
            if (!data.models || data.models.length === 0) return;

            modelsRegistry = {};
            modelSelect.innerHTML = "";
            const officialGroup = document.createElement("optgroup");
            officialGroup.label = "--- CÁC MÔ HÌNH CHÍNH THỨC (VERIFIED) ---";
            const legacyGroup = document.createElement("optgroup");
            legacyGroup.label = "--- CẤU HÌNH SO SÁNH / LEGACY ---";

            data.models.forEach((m) => {
                modelsRegistry[m.id] = m;
                const opt = document.createElement("option");
                opt.value = m.id;
                opt.textContent = `${m.name} [Test Acc: ${m.accuracy}]`;
                if (m.id === "cnn") opt.selected = true;

                if (m.is_official) {
                    officialGroup.appendChild(opt);
                } else {
                    legacyGroup.appendChild(opt);
                }
            });

            modelSelect.appendChild(officialGroup);
            if (legacyGroup.children.length > 0) {
                modelSelect.appendChild(legacyGroup);
            }

            // Populate initial model meta
            const initialId = modelSelect.value || "cnn";
            updateModelMetaDisplay(initialId);
        } catch (err) {
            console.warn("Không thể nạp danh sách mô hình:", err);
        }
    }

    // 15. Benchmark Navigation Scroll
    if (btnToggleBenchmark && benchmarkDrawer) {
        btnToggleBenchmark.addEventListener("click", () => {
            benchmarkDrawer.scrollIntoView({ behavior: "smooth", block: "start" });
        });
    }

    // Launch initial data fetches
    loadAvailableModels();
    loadTestSamples();
});
