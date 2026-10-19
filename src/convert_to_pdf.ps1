$ErrorActionPreference = "Stop"
$docPath = "D:\Thuy_Loi\Nam_4\nhan_dang_mau\ChuSoVietTay\reports\Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.docx"
$pdfPath = "D:\Thuy_Loi\Nam_4\nhan_dang_mau\ChuSoVietTay\reports\Bao_Cao_Bai_Tap_Lon_Nhan_Dang_Mau_Nhom_03.pdf"

Write-Host "Connecting to Word Application COM..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open($docPath)
    $pageCount = $doc.ComputeStatistics(2)
    Write-Host "Computed Page Count: $pageCount"
    # 17 represents wdExportFormatPDF
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close()
    Write-Host "Successfully exported PDF with $pageCount pages to: $pdfPath"
} finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}
