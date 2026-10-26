import Foundation
import PDFKit
import Vision
import AppKit

// Quick diagnostic on PDF1 (first 100 pages) and PDF2 (first 100 pages)
func inspectPDF(path: String, label: String, limit: Int) {
    let doc = PDFDocument(url: URL(fileURLWithPath: path))!
    let n = min(limit, doc.pageCount)
    var prevB = [Float](repeating: 0, count: 75)
    var prevC = [Float](repeating: 0, count: 75)
    print("=== \(label) ===")
    for i in 0..<n {
        let page = doc.page(at: i)!
        let w = 160, h = 210
        let img = page.thumbnail(of: NSSize(width: w, height: h), for: .mediaBox)
        let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil)!
        var raw = [UInt8](repeating: 0, count: w * h * 4)
        let ctx = CGContext(data: &raw, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4, space: CGColorSpaceCreateDeviceRGB(), bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
        ctx.draw(cg, in: CGRect(x: 0, y: 0, width: w, height: h))
        var cH = [Float](repeating: 0, count: 75)
        var bH = [Float](repeating: 0, count: 75)
        var cCnt: Float = 0, bCnt: Float = 0
        for y in 0..<h {
            let ny = Float(y)/Float(h)
            for x in 0..<w {
                let nx = Float(x)/Float(w)
                let idx = (y*w+x)*4
                let r = Float(raw[idx])/255.0, g = Float(raw[idx+1])/255.0, b = Float(raw[idx+2])/255.0
                if (ny < 0.06 || ny > 0.94) && r > 0.95 && g > 0.95 && b > 0.95 { continue }
                let maxC = max(r, max(g, b)), minC = min(r, min(g, b)), d = maxC - minC
                var hue: Float = 0
                if d > 0.001 {
                    if maxC == r { hue = 60 * (((g - b)/d).truncatingRemainder(dividingBy: 6)) }
                    else if maxC == g { hue = 60 * (((b - r)/d) + 2) }
                    else { hue = 60 * (((r - g)/d) + 4) }
                    if hue < 0 { hue += 360 }
                }
                let sat = maxC == 0 ? 0 : d/maxC
                let bin: Int
                if sat < 0.18 || maxC < 0.14 {
                    bin = 72 + (maxC < 0.30 ? 0 : (maxC < 0.60 ? 1 : 2))
                } else {
                    bin = min(7, Int((hue + 15).truncatingRemainder(dividingBy: 360)/45)) * 9 + min(2, Int(sat*3))*3 + min(2, Int(maxC*3))
                }
                if nx >= 0.25 && nx <= 0.75 && ny >= 0.25 && ny <= 0.75 { cH[bin] += 1; cCnt += 1 }
                else if nx < 0.14 || nx > 0.86 || (ny > 0.08 && ny < 0.18) || (ny > 0.82 && ny < 0.92) { bH[bin] += 1; bCnt += 1 }
            }
        }
        for k in 0..<75 { if cCnt > 0 { cH[k] /= cCnt }; if bCnt > 0 { bH[k] /= bCnt } }
        var bSim: Float = 0, cSim: Float = 0, cbSim: Float = 0
        for k in 0..<75 { bSim += min(bH[k], prevB[k]); cSim += min(cH[k], prevC[k]); cbSim += min(cH[k], bH[k]) }
        if i > 0 {
            print(String(format: "P%03d->P%03d: bSim=%.2f cSim=%.2f cbSim=%.2f", i, i+1, bSim, cSim, cbSim))
        }
        prevB = bH; prevC = cH
    }
}
inspectPDF(path: "/Users/ginavillamizar/Downloads/crewstore catalogooo/WhatsApp Image 2026-08-20 at 14.57.50.pdf", label: "PDF2 (509p)", limit: 90)
