import { useState } from 'react'
import { Download, Loader2 } from 'lucide-react'
import html2canvas from 'html2canvas'
import jsPDF from 'jspdf'

export default function ReportExport({ data }) {
  const [isExporting, setIsExporting] = useState(false)

  const handleExport = async () => {
    setIsExporting(true)
    try {
      const dashboardElement = document.getElementById('dashboard-content')
      if (!dashboardElement) return
      
      const canvas = await html2canvas(dashboardElement, {
        scale: 2,
        backgroundColor: '#0a1128', // navy-900
        windowWidth: 1200,
      })
      
      const imgData = canvas.toDataURL('image/png')
      const pdf = new jsPDF({
        orientation: 'p',
        unit: 'mm',
        format: 'a4',
      })
      
      const pdfWidth = pdf.internal.pageSize.getWidth()
      const pdfHeight = (canvas.height * pdfWidth) / canvas.width
      
      pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight)
      pdf.save(`sentiment_report_${data.video_data.title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.pdf`)
      
    } catch (error) {
      console.error("Failed to export PDF", error)
      alert("Failed to generate PDF. Please try again.")
    } finally {
      setIsExporting(false)
    }
  }

  return (
    <button
      onClick={handleExport}
      disabled={isExporting}
      className="flex items-center gap-2 bg-navy-700 hover:bg-navy-600 text-gray-200 px-4 py-2 rounded-lg transition-colors border border-navy-600 disabled:opacity-50"
    >
      {isExporting ? <Loader2 size={16} className="animate-spin" /> : <Download size={16} />}
      <span>Export Report</span>
    </button>
  )
}
